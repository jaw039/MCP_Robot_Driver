from fastapi import FastAPI
from pydantic import BaseModel
from robot_Driver_Playwright.my_robot_driver import RobotDriver

app = FastAPI(
    title="MCP Robot Driver API",
    description="Trigger the Playwright robot driver via HTTP",
    version="0.1.0",
)

class TaskRequest(BaseModel):
    url: str = "https://bstackdemo.com/"
    product_index: int = 0
    headless: bool = True
    timeout_ms: int = 10_000

class TaskResult(BaseModel):
    success: bool
    product: str | None = None
    price: str | None = None
    error: str | None = None

@app.post("/run-driver", response_model=TaskResult)
def run_driver(req: TaskRequest):
    driver = RobotDriver(timeout=req.timeout_ms)
    result = driver.run_complete_task(
        url=req.url,
        product_index=req.product_index,
        headless=req.headless,
    )
    return result
