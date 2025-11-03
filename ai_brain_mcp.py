"""AI planning brain that integrates Anthropic Claude with Playwright context.

This module implements the "AI Brain with MCP" optional challenge by combining three
components:

* A RobotDriver helper that can gather product catalog context from the demo site.
* Anthropic's Claude model (via the official SDK) to turn a natural language goal
  into a structured automation plan.
* An execution loop that applies the generated plan via the existing RobotDriver.

The implementation intentionally provides graceful degradation: if the Anthropic API
key is not available or the model response cannot be parsed, it falls back to the
original heuristic strategy selection so the system remains functional. When
available, the LLM produces JSON describing the intended product keyword, selection
strategy, reasoning, and high-level steps.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence

from anthropic import APIError, Anthropic
from dotenv import load_dotenv

from robot_Driver_Playwright.my_robot_driver import (
    ALLOWED_STRATEGIES,
    STRATEGY_MATCH,
    STRATEGY_MAX_PRICE,
    STRATEGY_MIN_PRICE,
    RobotDriver,
    RobotDriverResult,
)

DEFAULT_MODEL = "claude-3-5-sonnet-20241022"

SYSTEM_PROMPT = (
    "You are an AI planning assistant for a Playwright automation agent. "
    "Given a user's goal and a limited snapshot of the current product catalog, "
    "produce a JSON object with the following keys: "
    "product_keyword (string), selection_strategy (match|min_price|max_price), "
    "reasoning (string explanation), and steps (array of short action summaries). "
    "Respond with JSON only."
)


class AIBrainError(RuntimeError):
    """Raised when the AI planner cannot build or execute a plan."""


@dataclass
class AIExecutionPlan:
    """Structured automation plan returned by the LLM (or fallback)."""

    goal: str
    product_keyword: str
    selection_strategy: str
    steps: List[str] = field(default_factory=list)
    reasoning: str = ""
    source: str = "claude"
    raw_response: Optional[Any] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "goal": self.goal,
            "product_keyword": self.product_keyword,
            "selection_strategy": self.selection_strategy,
            "steps": self.steps,
            "reasoning": self.reasoning,
            "source": self.source,
            "raw_response": self.raw_response,
        }


@dataclass
class AIGoalExecution:
    """Full result of an AI-planned automation run."""

    plan: AIExecutionPlan
    catalog: List[Dict[str, Any]]
    result: RobotDriverResult

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plan": self.plan.to_dict(),
            "catalog_sample": [
                {"title": item.get("title"), "price": item.get("price_text")}
                for item in self.catalog
            ],
            "automation_result": {
                "requested_product": self.result.requested_product,
                "matched_product": self.result.matched_product,
                "price": self.result.price,
                "success": self.result.success,
                "selection_strategy": self.result.selection_strategy,
                "error": self.result.error,
            },
        }


class AIPlaywrightBrain:
    """Plan-and-execute controller that coordinates the LLM and RobotDriver."""

    def __init__(
        self,
        *,
        anthropic_client: Optional[Anthropic] = None,
        model: str = DEFAULT_MODEL,
        timeout_ms: int = 10_000,
    ) -> None:
        load_dotenv()
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_client is not None:
            self._client = anthropic_client
        elif api_key:
            self._client = Anthropic(api_key=api_key)
        else:
            self._client = None
        self.model = model
        self.timeout_ms = timeout_ms

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def execute_goal(
        self,
        *,
        goal: str,
        url: str,
        headless: bool = True,
    ) -> AIGoalExecution:
        """Run the AI planning flow end-to-end."""

        catalog_driver = self._new_driver()
        try:
            catalog = catalog_driver.collect_catalog_snapshot(
                url,
                headless=headless,
            )
        except Exception as exc:  # noqa: BLE001 - wrap lower-level errors
            raise AIBrainError(f"Failed to gather catalog snapshot: {exc}") from exc

        if not catalog:
            raise AIBrainError("Unable to gather product catalog for planning")

        plan = self._build_plan(goal=goal, catalog=catalog)

        executor_driver = self._new_driver()
        result = executor_driver.run_complete_task(
            url=url,
            product_name=plan.product_keyword,
            headless=headless,
            selection_strategy=plan.selection_strategy,
        )

        return AIGoalExecution(plan=plan, catalog=catalog, result=result)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _new_driver(self) -> RobotDriver:
        return RobotDriver(timeout_ms=self.timeout_ms)

    def _build_plan(self, *, goal: str, catalog: List[Dict[str, Any]]) -> AIExecutionPlan:
        if self._client is None:
            return self._fallback_plan(goal, catalog, reason="Anthropic API key not configured")

        catalog_summary = self._summarise_catalog(catalog)
        user_prompt = (
            "User goal: "
            f"{goal}\n\n"
            "Catalog sample: "
            f"{catalog_summary}"
        )

        try:
            response = self._client.messages.create(
                model=self.model,
                max_output_tokens=512,
                temperature=0,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_prompt}],
            )
            raw_text = self._extract_text(response)
            plan_payload = json.loads(raw_text)
        except (APIError, json.JSONDecodeError, ValueError) as exc:
            return self._fallback_plan(goal, catalog, reason=str(exc))

        selection_strategy = plan_payload.get("selection_strategy", STRATEGY_MATCH)
        if selection_strategy not in ALLOWED_STRATEGIES:
            selection_strategy = STRATEGY_MATCH

        product_keyword = (
            plan_payload.get("product_keyword")
            or plan_payload.get("product")
            or self._infer_keyword_from_goal(goal)
        )

        steps = plan_payload.get("steps")
        if not isinstance(steps, Sequence):
            steps = ["Start browser", "Log in", "Locate target product", "Report price"]
        steps = [str(step) for step in steps]

        reasoning = plan_payload.get("reasoning") or "Plan generated by Claude"

        return AIExecutionPlan(
            goal=goal,
            product_keyword=product_keyword,
            selection_strategy=selection_strategy,
            steps=steps,
            reasoning=reasoning,
            raw_response=plan_payload,
        )

    def _fallback_plan(self, goal: str, catalog: List[Dict[str, Any]], reason: str) -> AIExecutionPlan:
        lowered_goal = goal.lower()
        selection_strategy = STRATEGY_MATCH
        if "most expensive" in lowered_goal or "highest" in lowered_goal:
            selection_strategy = STRATEGY_MAX_PRICE
        elif any(keyword in lowered_goal for keyword in ("cheapest", "least expensive", "lowest")):
            selection_strategy = STRATEGY_MIN_PRICE

        product_keyword = self._infer_keyword_from_goal(goal)

        steps = [
            "Navigate to demo store",
            "Authenticate with demo credentials",
            f"Gather catalog entries (total: {len(catalog)})",
            f"Select product using strategy '{selection_strategy}'",
        ]

        reasoning = (
            "Fallback heuristic used because the AI planner was unavailable or "
            f"returned an invalid response: {reason}"
        )

        return AIExecutionPlan(
            goal=goal,
            product_keyword=product_keyword,
            selection_strategy=selection_strategy,
            steps=steps,
            reasoning=reasoning,
            source="fallback",
            raw_response=None,
        )

    @staticmethod
    def _extract_text(response: Any) -> str:
        """Flatten the Claude response content into a single text string."""

        if not hasattr(response, "content"):
            raise ValueError("Anthropic response missing content field")
        blocks = getattr(response, "content")
        texts: List[str] = []
        for block in blocks:
            if isinstance(block, dict):
                # Future-proofing for potential dict-based SDK responses
                if block.get("type") == "text":
                    texts.append(str(block.get("text", "")))
            else:
                # Current SDK returns TextBlock objects with .text attribute
                text = getattr(block, "text", "")
                texts.append(str(text))
        combined = "\n".join(filter(None, texts)).strip()
        if not combined:
            raise ValueError("Empty response from Anthropic model")
        return combined

    @staticmethod
    def _summarise_catalog(catalog: List[Dict[str, Any]], *, limit: int = 10) -> str:
        sample = [
            {
                "title": entry.get("title"),
                "price": entry.get("price_text"),
                "price_value": entry.get("price_value"),
            }
            for entry in catalog[:limit]
        ]
        return json.dumps(sample, ensure_ascii=False)

    @staticmethod
    def _infer_keyword_from_goal(goal: str) -> str:
        lowered_goal = goal.lower()
        known_keywords = (
            "iphone",
            "ipad",
            "macbook",
            "samsung",
            "android",
            "pixel",
        )
        for keyword in known_keywords:
            if keyword in lowered_goal:
                return keyword
        return goal.strip() or "iPhone"