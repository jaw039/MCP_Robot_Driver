"""Utility script to verify MCP Robot Driver API endpoints."""

import json
import time
from typing import Any, Callable

import requests

API_BASE = "http://localhost:8000"

def _print_section(title: str) -> None:
    print(f"\n{title}")
    print("-" * len(title))


def _run_request(
    label: str,
    method: Callable[..., requests.Response],
    endpoint: str,
    payload: dict[str, Any] | None = None,
) -> None:
    _print_section(label)
    try:
        if payload is not None:
            print(f"Request payload:\n{json.dumps(payload, indent=2)}")
            response = method(f"{API_BASE}{endpoint}", json=payload, timeout=30)
        else:
            response = method(f"{API_BASE}{endpoint}", timeout=30)
        print(f"Status: {response.status_code}")
        print(f"Response body:\n{json.dumps(response.json(), indent=2)}")
    except Exception as exc:  # noqa: BLE001 - provide actionable debug output
        print(f"Error during '{label}': {exc}")


def test_api() -> None:
    print("Testing MCP Robot Driver API")
    print("=" * 50)

    _run_request("1) Root endpoint", requests.get, "/")

    _run_request(
        "2) Basic automation",
        requests.post,
        "/run-basic",
        {
            "product_name": "iPhone 12",
            "headless": True,
            "timeout_ms": 15_000,
        },
    )

    _run_request(
        "3) AI-style automation",
        requests.post,
        "/run-ai",
        {
            "goal": "Find the cheapest iPhone",
            "headless": True,
        },
    )

    print("\nAPI testing complete!")
    print("\nAccess interactive docs at: http://localhost:8000/docs")

if __name__ == "__main__":
    print("Waiting 2 seconds for the API server to be ready...")
    time.sleep(2)
    test_api()