#!/usr/bin/env python3
"""
Test script for the MCP Robot Driver API
Run this after starting the API server to verify it works
"""

import requests
import json
import time

API_BASE = "http://localhost:8000"

def test_api():
    print("🧪 Testing MCP Robot Driver API")
    print("=" * 50)
    
    # Test 1: Root endpoint
    print("\n1️⃣ Testing root endpoint...")
    try:
        response = requests.get(f"{API_BASE}/")
        print(f"✅ Status: {response.status_code}")
        print(f"📋 Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Test 2: Basic automation
    print("\n2️⃣ Testing basic automation...")
    try:
        payload = {
            "product_name": "iPhone 12",
            "headless": True,
            "timeout_ms": 15000
        }
        
        print(f"📤 Sending: {json.dumps(payload, indent=2)}")
        response = requests.post(f"{API_BASE}/run-basic", json=payload)
        print(f"✅ Status: {response.status_code}")
        print(f"📋 Response: {json.dumps(response.json(), indent=2)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: AI-style automation  
    print("\n3️⃣ Testing AI-style automation...")
    try:
        payload = {
            "goal": "Find the cheapest iPhone",
            "headless": True
        }
        
        print(f"📤 Sending: {json.dumps(payload, indent=2)}")
        response = requests.post(f"{API_BASE}/run-ai", json=payload)
        print(f"✅ Status: {response.status_code}")
        print(f"📋 Response: {json.dumps(response.json(), indent=2)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n🎉 API testing complete!")
    print("\n💡 Access interactive docs at: http://localhost:8000/docs")

if __name__ == "__main__":
    print("⏳ Waiting 2 seconds for API server to be ready...")
    time.sleep(2)
    test_api()