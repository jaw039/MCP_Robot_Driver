#!/usr/bin/env python3
"""
Example: How to send directions to your Robot Driver API
"""

import requests
import json

API_BASE = "http://localhost:8000"

def send_basic_task(product_name, headless=True):
    """Send basic automation task"""
    payload = {
        "product_name": product_name,
        "headless": headless,
        "timeout_ms": 15000
    }
    
    response = requests.post(f"{API_BASE}/run-basic", json=payload)
    return response.json()

def send_ai_task(goal, headless=True):
    """Send AI-style task with natural language goal"""
    payload = {
        "goal": goal,
        "headless": headless
    }
    
    response = requests.post(f"{API_BASE}/run-ai", json=payload)
    return response.json()

if __name__ == "__main__":
    print("🤖 Sending directions to Robot Driver API")
    print("=" * 50)
    
    # Example 1: Basic automation
    print("\n📋 Basic Task: Find iPhone 13")
    result = send_basic_task("iPhone 13", headless=True)
    print(f"✅ Result: {json.dumps(result, indent=2)}")
    
    # Example 2: AI-style automation
    print("\n🧠 AI Task: Find cheapest iPhone")
    result = send_ai_task("Find the cheapest iPhone", headless=True)
    print(f"✅ Result: {json.dumps(result, indent=2)}")
    
    # Example 3: Custom goals
    print("\n🎯 Custom AI Goal: Find expensive Samsung")
    result = send_ai_task("Find the most expensive Samsung phone", headless=True)
    print(f"✅ Result: {json.dumps(result, indent=2)}")