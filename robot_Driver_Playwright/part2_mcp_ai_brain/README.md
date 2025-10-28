# Part 2: MCP AI Brain (Advanced Challenge)

## Overview
This implements the **Model Context Protocol (MCP)** - an AI-driven approach where Claude AI dynamically determines execution steps based on real-time page context.

## What Makes This Special
Instead of hardcoded steps, Claude AI:
1. **Sees** the page structure (buttons, inputs, text)
2. **Decides** what action to take next
3. **Executes** through your Playwright tools
4. **Adapts** based on results

## The MCP Innovation

### Without MCP (Traditional)
```
You: "Click the login button"
Code: page.click('#login')  // Hardcoded
```

### With MCP (AI-Driven)
```
You: "Buy the cheapest iPhone"
Claude: *analyzes page* → Sees 9 iPhones with prices
Claude: *compares prices* → iPhone XR $499 is cheapest  
Claude: *decides* → "I'll click the add to cart for iPhone XR"
Code: Executes Claude's decision
```

## Architecture

### Core Components

#### 1. **Tool Definitions** (`_define_tools()`)
```python
{
    "name": "playwright_find_cheapest_product",
    "description": "Find the cheapest iPhone product on the page",
    "input_schema": {...}
}
```
Tells Claude what actions are available.

#### 2. **Page Context Extraction** (`_get_page_accessibility_tree()`)
```python
elements_info = {
    "buttons": [{"text": "Add to cart", "selector": ".buy-btn"}],
    "text": "iPhone XR $499.00 iPhone 12 $799.00...",
    "page_title": "StackDemo"
}
```
**This is the MCP magic** - structured page data for Claude.

#### 3. **Tool Execution** (`_execute_tool()`)
```python
elif tool_name == "playwright_find_cheapest_product":
    # Extract all iPhone prices using regex
    # Compare prices numerically  
    # Return cheapest product info
```
Maps Claude's requests to Playwright actions.

#### 4. **AI Decision Loop** (`execute_task_with_ai()`)
```python
for iteration in range(max_iterations):
    # Claude analyzes current page state
    response = self.client.messages.create(tools=tools, ...)
    
    # Execute Claude's chosen tool
    tool_result = self._execute_tool(tool_name, tool_input)
    
    # Send results back to Claude
    # Claude decides next step
```
The orchestration engine.

## How to Run

### Prerequisites
```bash
pip install anthropic playwright python-dotenv
playwright install chromium

# Create .env file with:
ANTHROPIC_API_KEY=your_api_key_here
```

### Execution
```bash
python ai_brain_mcp.py
```

### Expected Flow
```
MCP Robot Driver Demo - Buy Cheapest iPhone

AI ROBOT DRIVER - Goal: Find the cheapest iPhone on the page and add it to cart
URL: https://bstackdemo.com/

Iteration 1/5
  Claude response: tool_use
  Tool: playwright_navigate - Input: {'url': 'https://bstackdemo.com/'}
  Result: Successfully navigated to https://bstackdemo.com/

Iteration 2/5
  Claude response: tool_use
  Tool: playwright_find_cheapest_product - Input: {}
  Result: Found 9 iPhones: iPhone 12: $799.00, iPhone XR: $499.00... Cheapest: iPhone XR at $499.00

Iteration 3/5
  Claude response: tool_use
  Tool: playwright_click_cheapest_iphone - Input: {}
  Result: Added cheapest iPhone to cart: iPhone XR ($499.0)

TASK_COMPLETE
Success: True
```

## Key Features

### 🧠 **Smart Product Analysis**
Uses regex to extract all iPhone prices from page text:
```python
iphone_pattern = r'(iPhone[^$]*)\s*\$([0-9,]+\.?[0-9]*)'
# Finds: "iPhone XR $499.00", "iPhone 12 $799.00", etc.
```

### 🎯 **Intelligent Button Finding**
Multiple fallback strategies to find "Add to cart" buttons:
```python
selectors_to_try = [
    f"text='{iphone_text}' >> .. >> text='Add to cart'",
    f":has-text('{iphone_text}') >> text='Add to cart'", 
    "button:has-text('Add to cart')"
]
```

### 🔄 **Adaptive Decision Making**
Claude sees results and adjusts:
```python
# Claude gets: "Found 9 iPhones... Cheapest: iPhone XR at $499.00"
# Claude decides: "I'll click the cheapest one"
# Result: "Added iPhone XR to cart"
# Claude concludes: "TASK_COMPLETE"
```

## Available Tools

Claude can use these tools automatically:

| Tool | Purpose | Example |
|------|---------|---------|
| `playwright_navigate` | Go to website | `{'url': 'https://site.com'}` |
| `playwright_find_cheapest_product` | Analyze all iPhones | Returns price comparison |
| `playwright_click_cheapest_iphone` | Add cheapest to cart | Clicks the right button |
| `playwright_get_page_info` | See page structure | Returns buttons, inputs, text |
| `playwright_screenshot` | Visual debugging | Saves screenshot.png |

## Customization

### Change the Goal
```python
# In simple_demo() function:
goal = "Find the most expensive phone"           # Custom goal
goal = "Add 3 cheapest items to cart"           # Multiple items  
goal = "Search for Samsung and compare prices"   # Different brand
```

### Add New Tools
```python
# Step 1: Define tool
{
    "name": "my_custom_tool",
    "description": "What it does",
    "input_schema": {"type": "object", "properties": {...}}
}

# Step 2: Add handler
elif tool_name == "my_custom_tool":
    # Your logic here
    return "result"
```

Claude will automatically use your new tool!

## Technical Deep Dive

### The MCP Flow
```
1. User Goal: "Buy cheapest iPhone"
   ↓
2. Claude gets tools list + page context
   ↓ 
3. Claude: "I need to navigate first"
   → Tool: playwright_navigate
   ↓
4. Page loads → Extract structure → Send to Claude
   ↓
5. Claude: "I see 9 iPhones, let me find cheapest"  
   → Tool: playwright_find_cheapest_product
   ↓
6. Result: "iPhone XR $499 is cheapest"
   ↓
7. Claude: "I'll add it to cart"
   → Tool: playwright_click_cheapest_iphone  
   ↓
8. Result: "Added to cart"
   ↓
9. Claude: "TASK_COMPLETE"
```

### Why This Works
- **Context**: Claude sees exact page state
- **Flexibility**: Adapts to any page layout
- **Intelligence**: Makes optimal decisions
- **Reliability**: Uses proven selectors

## Success Metrics
✅ **Dynamic Planning**: Claude creates steps, not hardcoded  
✅ **Page Awareness**: Uses structured page context (MCP)  
✅ **Tool Integration**: Claude calls Playwright functions  
✅ **Price Analysis**: Correctly identifies cheapest iPhone  
✅ **Cart Addition**: Successfully adds item to cart  
✅ **Task Completion**: Recognizes when goal is achieved  

## Comparison to Part 1

| Aspect | Part 1 (Basic) | Part 2 (MCP) |
|--------|----------------|--------------|
| **Decision Making** | Hardcoded steps | AI decides dynamically |
| **Page Awareness** | Blind selectors | Full page context |
| **Adaptability** | Breaks on changes | Adapts to new layouts |
| **Goal Flexibility** | Single purpose | Any natural language goal |
| **Intelligence** | None | Claude AI reasoning |

This demonstrates **modern AI-agent architecture** and **expertise in cutting-edge automation techniques**.