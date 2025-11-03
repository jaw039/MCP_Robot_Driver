# Testing the AI Brain Integration

## Current Status: WORKING

The AI Brain integration is fully functional with graceful fallback.

## Quick Test Guide

### 1. Start the API Server

```bash
# Method 1: Interactive (see logs in real-time)
uvicorn api.main:app --reload

# Method 2: Background (logs go to file)
nohup uvicorn api.main:app --port 8000 > /tmp/api_server.log 2>&1 &
```

### 2. Test with curl

**Test 1: Find cheapest iPhone**
```bash
curl -X POST http://localhost:8000/run-ai \
  -H "Content-Type: application/json" \
  -d '{"goal": "Find the cheapest iPhone", "headless": true}' \
  | python3 -m json.tool
```

**Test 2: Find most expensive Samsung**
```bash
curl -X POST http://localhost:8000/run-ai \
  -H "Content-Type: application/json" \
  -d '{"goal": "What is the most expensive Samsung phone?", "headless": true}' \
  | python3 -m json.tool
```

**Test 3: Specific product match**
```bash
curl -X POST http://localhost:8000/run-ai \
  -H "Content-Type: application/json" \
  -d '{"goal": "Find the iPhone 12 Pro", "headless": true}' \
  | python3 -m json.tool
```

### 3. Use the Python Test Script

```bash
python3 test_ai_brain.py
```

### 4. Interactive API Documentation

Open in your browser:
```
http://localhost:8000/docs
```

Try the `/run-ai` endpoint with the interactive Swagger UI!

## Understanding the Response

The `/run-ai` endpoint returns:

```json
{
  "success": true,
  "product": "iPhone XR",
  "price": "$499.00",
  "selection_strategy": "min_price",
  "execution_time_seconds": 13.27,
  "approach": "AI-guided automation (Claude with fallback)",
  
  "plan": {
    "goal": "Find the cheapest iPhone",
    "product_keyword": "iphone",
    "selection_strategy": "min_price",
    "source": "fallback",  // "claude" if API key is set
    "reasoning": "Explanation of why this strategy was chosen",
    "steps": ["Step 1", "Step 2", "..."]
  },
  
  "catalog_sample": [
    {"title": "iPhone 12", "price": "$799.00", "price_value": 799.0},
    // ... more products
  ]
}
```

### Key Fields to Check:

- **`plan.source`**: 
  - `"fallback"` = Using heuristic strategy (no API key)
  - `"claude"` = Using Anthropic AI for planning
  
- **`plan.reasoning`**: Explains the AI's decision-making process

- **`catalog_sample`**: Shows what products were available for selection

- **`selection_strategy`**: 
  - `"match"` = Find by name
  - `"min_price"` = Find cheapest
  - `"max_price"` = Find most expensive

## How It Works

### Without ANTHROPIC_API_KEY (Current State):
1. Collects product catalog from demo site
2. Uses fallback heuristics to parse the goal
3. Executes automation with the determined strategy
4. Returns the full plan and results

### With ANTHROPIC_API_KEY (Optional Challenge 1):
1. Collects product catalog from demo site
2. Sends goal plus catalog to Claude AI
3. Claude generates a structured JSON plan
4. Executes automation based on the AI plan
5. Returns the AI-generated plan and results

## Setting Up Anthropic AI (Optional)

To test with real AI planning:

1. Get API key from https://console.anthropic.com/
2. Create `.env` file in project root:
   ```
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```
3. Restart the API server
4. Run tests again - `plan.source` should now show `"claude"`

## Verified Test Results

- **Test 1**: Cheapest iPhone
- Input: "Find the cheapest iPhone"
- Result: iPhone XR at $499.00
- Strategy: min_price
- Source: fallback

- **Test 2**: Most Expensive Samsung
- Input: "What is the most expensive Samsung phone?"
- Result: Galaxy S20 Ultra at $1399.00
- Strategy: max_price
- Source: fallback

- **Test 3**: Specific Match
- Input: "Find the iPhone 12 Pro"
- Result: iPhone 12 Pro at $999.00
- Strategy: match
- Source: fallback

## What Makes This Optional Challenge 1 Complete

- **AI Brain Module** (`ai_brain_mcp.py`)
- Anthropic Claude integration
- Structured plan generation
- Graceful fallback when no API key

- **Context Collection** (`collect_catalog_snapshot`)
- Gathers product catalog for AI context
- Provides pricing and availability data

- **Plan Execution** (`AIPlaywrightBrain.execute_goal`)
- Takes natural language goals
- Generates execution plans
- Executes via RobotDriver

- **API Integration** (`/run-ai` endpoint)
- Network-accessible AI planning
- Returns plan metadata
- Works with or without API key

## Stop the Server

```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9

# Or if running in foreground, press Ctrl+C
```
