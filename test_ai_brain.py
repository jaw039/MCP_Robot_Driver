#!/usr/bin/env python3
"""
Test the AI Brain integration with the /run-ai endpoint.

This script tests both scenarios:
1. With ANTHROPIC_API_KEY set (uses Claude for planning)
2. Without ANTHROPIC_API_KEY (uses fallback heuristics)
"""

import json
import os
import time

import requests

API_BASE = "http://localhost:8000"


def print_section(title: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}\n")


def test_ai_endpoint(test_name: str, goal: str, headless: bool = True) -> None:
    """Test the /run-ai endpoint with a specific goal."""
    print(f"\nTest: {test_name}")
    print(f"   Goal: '{goal}'")
    print(f"   Headless: {headless}")
    
    payload = {
        "goal": goal,
        "headless": headless,
    }
    
    try:
        print("\nSending request...")
        start_time = time.time()
        response = requests.post(f"{API_BASE}/run-ai", json=payload, timeout=120)
        elapsed = time.time() - start_time

        print(f"Status: {response.status_code}")
        print(f"Response time: {elapsed:.2f}s")

        result = response.json()
        
        # Print key results
        print(f"\nResult summary:")
        print(f"   Success: {result.get('success')}")
        print(f"   Product: {result.get('product')}")
        print(f"   Price: {result.get('price')}")
        print(f"   Strategy: {result.get('selection_strategy')}")
        print(f"   Approach: {result.get('approach')}")
        
        if result.get('error'):
            print(f"   Error: {result.get('error')}")
        
        # Print AI Plan details if available
        if result.get('plan'):
            plan = result['plan']
            print(f"\nAI plan details:")
            print(f"   Source: {plan.get('source')} (Claude or fallback)")
            print(f"   Product Keyword: {plan.get('product_keyword')}")
            print(f"   Strategy: {plan.get('selection_strategy')}")
            print(f"   Reasoning: {plan.get('reasoning')}")
            
            if plan.get('steps'):
                print(f"\n   Planned steps:")
                for i, step in enumerate(plan['steps'], 1):
                    print(f"      {i}. {step}")
        
        # Print catalog sample if available
        if result.get('catalog_sample'):
            print(f"\nCatalog sample ({len(result['catalog_sample'])} items):")
            for item in result['catalog_sample'][:3]:  # Show first 3
                print(f"   - {item.get('title')}: {item.get('price')}")
        
        print(f"\nFull JSON response:")
        print(json.dumps(result, indent=2))
        
    except requests.exceptions.Timeout:
        print("Request timed out after 120 seconds")
    except Exception as e:
        print(f"Error: {e}")


def check_api_key() -> bool:
    """Check if ANTHROPIC_API_KEY is set."""
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    has_key = bool(api_key and api_key.strip())
    
    if has_key:
        print("ANTHROPIC_API_KEY is set")
        print("   Using Claude AI for planning")
    else:
        print("ANTHROPIC_API_KEY is not set")
        print("   Using fallback heuristics")
    
    return has_key


def main():
    print_section("AI Brain Integration Test")
    
    # Check API key status
    has_api_key = check_api_key()
    
    # Wait for server
    print("\nChecking if the API server is ready...")
    time.sleep(1)
    
    try:
        response = requests.get(f"{API_BASE}/", timeout=5)
        if response.status_code == 200:
            print("API server is ready!")
        else:
            print(f"API returned status {response.status_code}")
            return
    except Exception as e:
        print(f"Cannot connect to API server: {e}")
        print("   Make sure the server is running: uvicorn api.main:app --reload")
        return
    
    # Test Cases
    print_section("Test 1: Find Cheapest iPhone")
    test_ai_endpoint(
        "Cheapest iPhone Test",
        "Find the cheapest iPhone and add it to cart",
        headless=True
    )
    
    print_section("Test 2: Most Expensive Product")
    test_ai_endpoint(
        "Most Expensive Test",
        "What is the most expensive Samsung device?",
        headless=True
    )
    
    print_section("Test 3: Specific Product Match")
    test_ai_endpoint(
        "Specific Product Test",
        "Find the iPhone 12 Pro",
        headless=True
    )
    
    print_section("Testing Complete!")
    print("\nWhat to look for:")
    print("   1. Check the 'source' field in the plan:")
    if has_api_key:
        print("      - Should be 'claude' (using AI)")
        print("      - Reasoning should be detailed and context-aware")
    else:
        print("      - Will be 'fallback' (using heuristics)")
        print("      - Reasoning explains why fallback was used")
    print("   2. Verify the selection_strategy matches the goal")
    print("   3. Check that the product and price were found successfully")
    print("   4. Review the catalog_sample to see what products are available")
    
    print("\nTo test with Claude AI:")
    print("   1. Get an API key from https://console.anthropic.com/")
    print("   2. Create a .env file with: ANTHROPIC_API_KEY=your_key_here")
    print("   3. Run this test again")
    
    print("\nView API docs at: http://localhost:8000/docs")


if __name__ == "__main__":
    main()
