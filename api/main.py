import sys
from pathlib import Path
from time import perf_counter
from typing import Literal

# Add parent directory to path to import robot drivers
sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI
from pydantic import BaseModel

from robot_Driver_Playwright.my_robot_driver import RobotDriver

app = FastAPI(
    title="MCP Robot Driver API",
    description="Network-accessible service for Playwright automation",
    version="1.0.0",
)

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

# Endpoints

@app.get("/")
def root():
    return {
        "message": "MCP Robot Driver API - Challenge 2 Complete!",
        "endpoints": {
            "/run-basic": "Run basic hardcoded automation (Part 1)",
            "/run-ai": "Run AI-style automation (simulated)", 
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
    
    Executes predefined steps: navigate → login → find product → extract price
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
    """
    Run AI-style automation (simulated)
    
    Demonstrates how an AI-driven endpoint would work.
    In a full implementation, this would use Claude AI with MCP.
    """
    start_time = perf_counter()

    try:
        # Parse goal to determine product and selection mode
        goal_lower = req.goal.lower()
        strategy: Literal["match", "min_price", "max_price"] = "match"

        if "most expensive" in goal_lower or "highest" in goal_lower:
            strategy = "max_price"
        elif any(phrase in goal_lower for phrase in ("cheapest", "least expensive", "lowest")):
            strategy = "min_price"

        if "iphone" in goal_lower:
            target_product = "iPhone"
        else:
            target_product = "iPhone 12"

        driver = RobotDriver(timeout_ms=10_000)
        result = driver.run_complete_task(
            url=req.url,
            product_name=target_product,
            headless=req.headless,
            selection_strategy=strategy,
        )

        execution_time = perf_counter() - start_time

        return TaskResult(
            success=result.success,
            product=result.matched_product or result.requested_product,
            price=result.price,
            error=result.error,
            approach="AI-guided automation (simulated)",
            execution_time_seconds=round(execution_time, 2),
            selection_strategy=result.selection_strategy,
        )

    except Exception as e:
        execution_time = perf_counter() - start_time
        return TaskResult(
            success=False,
            error=f"API Error: {str(e)}",
            approach="AI-guided automation (simulated)",
            execution_time_seconds=round(execution_time, 2)
        )
