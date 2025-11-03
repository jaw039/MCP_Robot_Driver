import sys
from pathlib import Path
from time import perf_counter
from typing import Any, Literal

# Add parent directory to path to import robot drivers
sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI
from pydantic import BaseModel

from ai_brain_mcp import AIBrainError, AIPlaywrightBrain
from robot_Driver_Playwright.my_robot_driver import RobotDriver

app = FastAPI(
    title="MCP Robot Driver API",
    description="Network-accessible service for Playwright automation",
    version="1.0.0",
)

ai_brain = AIPlaywrightBrain()

# Request Models
class BasicTaskRequest(BaseModel):
    url: str = "https://bstackdemo.com/"
    product_name: str = "iPhone 12"
    headless: bool = True
    timeout_ms: int = 10_000
    selection_strategy: Literal["match", "min_price", "max_price"] = "match"

class AITaskRequest(BaseModel):
    goal: str = "Find the cheapest iPhone and add it to cart"
    url: str = "https://bstackdemo.com/"
    headless: bool = True

# Response Models  
class TaskResult(BaseModel):
    success: bool
    product: str | None = None
    price: str | None = None
    error: str | None = None
    approach: str
    execution_time_seconds: float | None = None
    selection_strategy: str | None = None
    plan: dict[str, Any] | None = None
    catalog_sample: list[dict[str, Any]] | None = None

# Endpoints

@app.get("/")
def root():
    return {
        "message": "MCP Robot Driver API - Challenge 2 Complete!",
        "endpoints": {
            "/run-basic": "Run basic hardcoded automation (Part 1)",
            "/run-ai": "Run AI-style automation (Claude with fallback)", 
            "/docs": "Interactive API documentation"
        },
        "features": [
            "Network-accessible automation service",
            "RESTful API with JSON",
            "Error handling and timeouts",
            "Easy setup with requirements.txt",
            "Auto-generated documentation"
        ]
    }

@app.post("/run-basic", response_model=TaskResult)
def run_basic_driver(req: BasicTaskRequest):
    """
    Run basic hardcoded Playwright automation
    
    Executes predefined steps: navigate -> login -> find product -> extract price
    """
    start_time = perf_counter()

    try:
        driver = RobotDriver(timeout_ms=req.timeout_ms)
        result = driver.run_complete_task(
            url=req.url,
            product_name=req.product_name,
            headless=req.headless,
            selection_strategy=req.selection_strategy,
        )

        execution_time = perf_counter() - start_time

        return TaskResult(
            success=result.success,
            product=result.matched_product or result.requested_product,
            price=result.price,
            error=result.error,
            approach="Basic Playwright automation",
            execution_time_seconds=round(execution_time, 2),
            selection_strategy=result.selection_strategy,
        )

    except Exception as e:
        execution_time = perf_counter() - start_time
        return TaskResult(
            success=False,
            error=f"API Error: {str(e)}",
            approach="Basic Playwright automation",
            execution_time_seconds=round(execution_time, 2)
        )

@app.post("/run-ai", response_model=TaskResult)
def run_ai_driver(req: AITaskRequest):
    """Run AI-driven automation using Anthropic Claude with graceful fallback."""
    start_time = perf_counter()

    try:
        execution = ai_brain.execute_goal(goal=req.goal, url=req.url, headless=req.headless)

        execution_time = perf_counter() - start_time

        catalog_sample = [
            {"title": item.get("title"), "price": item.get("price_text"), "price_value": item.get("price_value")}
            for item in execution.catalog[:5]
        ]

        return TaskResult(
            success=execution.result.success,
            product=execution.result.matched_product or execution.result.requested_product,
            price=execution.result.price,
            error=execution.result.error,
            approach="AI-guided automation (Claude with fallback)",
            execution_time_seconds=round(execution_time, 2),
            selection_strategy=execution.result.selection_strategy,
            plan=execution.plan.to_dict(),
            catalog_sample=catalog_sample,
        )

    except AIBrainError as brain_error:
        execution_time = perf_counter() - start_time
        return TaskResult(
            success=False,
            error=f"AI planning error: {brain_error}",
            approach="AI-guided automation (Claude with fallback)",
            execution_time_seconds=round(execution_time, 2)
        )

    except Exception as e:
        execution_time = perf_counter() - start_time
        return TaskResult(
            success=False,
            error=f"API Error: {str(e)}",
            approach="AI-guided automation (Claude with fallback)",
            execution_time_seconds=round(execution_time, 2)
        )
