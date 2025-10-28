# MCP Robot Driver - Technical Guide

## What This Does

This system lets Claude AI automatically control a web browser. Instead of hardcoding steps, you describe your goal in English and Claude figures out how to do it.

---

## How It Works

1. **Define Tools** - Tell Claude what it can do (navigate, click, find products)
2. **Get Page Context** - Claude receives structured info about the page (buttons, inputs, text)
3. **Claude Decides** - Claude analyzes the page and decides what to do next
4. **Execute** - Your code runs what Claude requested
5. **Feedback Loop** - Claude sees the result and decides the next step
6. **Repeat** - Until task is complete

---

## The MCP Innovation

**Without MCP (Traditional):**
```
Claude guesses: "Click button 5" → Wrong button clicked
```

**With MCP (Intelligent):**  
```
Claude gets exact element info → Clicks correct button
```

---

## Usage

### Quick Start
```bash
python ai_brain_mcp.py
```

### Try Different Goals
Edit `simple_demo()` function, change the goal:

```python
# Examples:
goal = "Find the cheapest iPhone and add it to cart"
goal = "Search for Samsung and show prices" 
goal = "Take a screenshot of the page"
```

---

## Available Tools

Claude can use these tools automatically:

| Tool | Purpose | Example Use |
|------|---------|-------------|
| `playwright_navigate` | Go to website | Navigate to target URL |
| `playwright_find_cheapest_product` | Analyze iPhone prices | Compare all iPhone prices |
| `playwright_click_cheapest_iphone` | Add cheapest to cart | Click "Add to cart" for cheapest |
| `playwright_get_page_info` | See page structure | Extract buttons, inputs, text |
| `playwright_click` | Click any element | Click specific buttons/links |
| `playwright_fill` | Type text | Fill form fields |
| `playwright_screenshot` | Visual debugging | Save screenshot.png |
| `playwright_get_text` | Get visible text | Extract page content |

---

## Add New Tools (3 Simple Steps)

### Step 1: Define the Tool
```python
# In _define_tools() method:
{
    "name": "my_custom_tool",
    "description": "What this tool does",
    "input_schema": {
        "type": "object",
        "properties": {
            "param": {"type": "string", "description": "Parameter description"}
        },
        "required": ["param"]
    }
}
```

### Step 2: Add Handler
```python
# In _execute_tool() method:
elif tool_name == "my_custom_tool":
    param = tool_input.get("param")
    # Your custom logic here
    return "Custom tool result"
```

### Step 3: Done!
Claude will automatically use your new tool when needed.

---

## Example Task Complexity

### Easy Tasks
```python
goal = "Take a screenshot"
goal = "Show me what's on the page"
goal = "Navigate to the homepage"
```

### Medium Tasks  
```python
goal = "Find all iPhone prices"
goal = "Click on the cart"
goal = "Search for Samsung products"
```

### Hard Tasks
```python
goal = "Find and compare prices in 3 categories"
goal = "Buy the cheapest item available"
goal = "Add multiple products to cart and checkout"
```

---

## Understanding the Architecture

### Core Functions

#### 1. `_define_tools()` 
Lists all tools Claude can use with JSON schemas.

#### 2. `_get_page_accessibility_tree()` ⭐
**The MCP magic!** Extracts structured page data:
```python
elements_info = {
    "buttons": [{"text": "Add to cart", "selector": ".buy-btn"}],
    "inputs": [{"type": "text", "placeholder": "Search"}],
    "text": "iPhone XR $499.00 iPhone 12 $799.00...",
    "page_title": "StackDemo"
}
```

#### 3. `_execute_tool()`
Maps Claude's requests to Playwright actions.

#### 4. `execute_task_with_ai()`  
Main orchestration loop that coordinates everything.

---

## The Decision Flow

```
Your Goal: "Buy cheapest iPhone"
   ↓
Claude analyzes available tools
   ↓
Claude: "I'll navigate to the site first"
   ↓ 
Execute: page.goto("https://site.com")
   ↓
Result: "Successfully navigated"
   ↓
Claude: "Now I need to see what's on the page"
   ↓
Execute: Extract page structure (MCP)
   ↓
Claude gets: {text: "iPhone XR $499, iPhone 12 $799..."}
   ↓
Claude: "I see 9 iPhones, iPhone XR is cheapest at $499"
   ↓
Claude: "I'll click the add to cart for iPhone XR"
   ↓
Execute: Click the correct button
   ↓  
Result: "Added iPhone XR to cart"
   ↓
Claude: "TASK_COMPLETE"
```

---

## Smart Features

### 🧠 **Intelligent Price Analysis**
Uses regex to extract prices from page text:
```python
iphone_pattern = r'(iPhone[^$]*)\s*\$([0-9,]+\.?[0-9]*)'
# Finds: "iPhone XR $499.00", "iPhone 12 $799.00", etc.
```

### 🎯 **Adaptive Button Finding**
Multiple strategies to find the right "Add to cart" button:
```python
selectors_to_try = [
    f"text='{iphone_text}' >> .. >> text='Add to cart'",
    f":has-text('{iphone_text}') >> text='Add to cart'",
    "button:has-text('Add to cart')"
]
```

### 🔄 **Context-Aware Decisions**
Claude sees results and adapts strategy dynamically.

---

## Troubleshooting

### Claude Not Using Tools?
- Check `tools=` parameter is passed to `client.messages.create()`
- Verify API key is set in `.env` file

### Selector Doesn't Work?
- Use selectors from `_get_page_accessibility_tree()` - they're guaranteed to work
- Check browser console for element inspection

### Getting Wrong Results?
- Modify `system_prompt` in `execute_task_with_ai()` to guide Claude better
- Increase `max_iterations` for complex tasks

---

## Quick Reference

### Environment Setup
```bash
# Install dependencies
pip install anthropic playwright python-dotenv
playwright install chromium

# Create .env file with:
ANTHROPIC_API_KEY=your_api_key_here
```

### Run and Customize
```bash
# Run default demo
python ai_brain_mcp.py

# Edit goal in simple_demo() function
goal = "Your custom task here"
```

---

## Next Steps

1. **Run the demo**: `python ai_brain_mcp.py`
2. **Modify goals**: Change the task and run again  
3. **Add custom tools**: Follow the 3-step pattern
4. **Build complex workflows**: Combine multiple goals

**Simple, powerful, and infinitely extensible!** 🚀
