#!/bin/bash

echo "🧪 Testing MCP Robot Driver API"
echo "================================="

# Test basic automation
echo ""
echo "1️⃣ Testing Basic Automation:"
echo "Command: Find iPhone 12"

curl -X POST "http://localhost:8000/run-basic" \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "iPhone 12",
    "headless": true,
    "timeout_ms": 15000
  }' | python -m json.tool

echo ""
echo "================================="

# Test AI automation  
echo ""
echo "2️⃣ Testing AI-Style Automation:"
echo "Command: Find cheapest iPhone"

curl -X POST "http://localhost:8000/run-ai" \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Find the cheapest iPhone",
    "headless": true
  }' | python -m json.tool

echo ""
echo "🎉 Testing complete!"
echo "💡 View interactive docs: http://localhost:8000/docs"