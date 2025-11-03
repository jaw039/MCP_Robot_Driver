#!/usr/bin/env python3
"""
Example: How to send directions to your Robot Driver API
"""

import json
from typing import Any

import requests

API_BASE = "http://localhost:8000"

def send_basic_task(product_name: str, headless: bool = True) -> dict[str, Any]:
    """Send basic automation task"""
    payload = {
        "product_name": product_name,
        "headless": headless,
        "timeout_ms": 15000
    }
    
    response = requests.post(f"{API_BASE}/run-basic", json=payload, timeout=30)
    return response.json()

def send_ai_task(goal: str, headless: bool = True) -> dict[str, Any]:
    """Send AI-style task with natural language goal"""
    payload = {
        "goal": goal,
        "headless": headless
    }
    
    response = requests.post(f"{API_BASE}/run-ai", json=payload, timeout=30)
    return response.json()


def _print_result(label: str, result: dict[str, Any]) -> None:
    print(f"\n{label}")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    print("Sending directions to Robot Driver API")
    print("=" * 50)

    _print_result("Basic task: Find iPhone 13", send_basic_task("iPhone 13", headless=True))

    _print_result("AI task: Find cheapest iPhone", send_ai_task("Find the cheapest iPhone", headless=True))

    _print_result(
        "Custom AI goal: Find expensive Samsung",
        send_ai_task("Find the most expensive Samsung phone", headless=True),
    )