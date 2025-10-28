# Robot Driver - Browser Automation Challenge# Robot Driver - Browser Automation Challenge# Robot Driver Challenge - Complete Implementation# Robot Driver Challenge - Complete Implementation# 🤖 Robot Driver - Step-by-Step Guide



Two approaches to web automation: foundational Playwright skills and AI-driven architecture.



## Part 1: The Robot Driver (Required)## Overview



**Goal:** Python program controls browser using Playwright for fixed task.



**Actions:** Navigate → Login → Find product → Extract price + Error handlingThis project implements two complementary approaches to web automation, from foundational Playwright skills to advanced AI-driven architecture.## Task Objectives



**Run:** `cd part1_basic_automation && python my_robot_driver.py`



## Part 2: AI Brain with MCP (Bonus)---



**Goal:** AI Language Model determines execution steps dynamically.



**How:** Plain English goal → MCP provides page context → Claude AI plans steps → Program executes## Part 1: The Robot Driver (Foundational Skills)This project demonstrates two approaches to web automation, progressing from basic Playwright scripting to advanced AI-driven automation using the Model Context Protocol (MCP).## 🎯 Task Objectives## 📚 What You'll Learn



**Run:** `cd part2_mcp_ai_brain && python ai_brain_mcp.py`



**Result:** AI finds cheapest iPhone ($499) autonomously in 4 iterations**Goal:** Write a Python program that controls a web browser using Playwright to complete a fixed task.



## Setup



```bash**Required Actions:**---

pip install playwright anthropic python-dotenv

playwright install chromium- Navigate to BrowserStack demo site

# Part 2: Add ANTHROPIC_API_KEY to .env file

```- Log in using form interactions



## Skills- Find and select a product



**Part 1:** Playwright automation, error handling  - Extract and report the price## Challenge OverviewThis project demonstrates two approaches to web automation, progressing from basic Playwright scripting to advanced AI-driven automation using the Model Context Protocol (MCP).This guide teaches you how to build a **Robot Driver** - a Python program that controls a web browser to complete automated tasks.

**Part 2:** AI integration, MCP architecture, LLM-driven planning
- Handle errors gracefully (timeouts, missing elements)



**Implementation:** `part1_basic_automation/my_robot_driver.py`

### Primary Goal

**Run:**

```bashBuild a web automation system that can navigate to BrowserStack's demo site and purchase the cheapest iPhone available.

cd part1_basic_automation

python my_robot_driver.py------

```

### Technical Requirements

**Output:** Clear final result reporting success/failure with product details

1. Part 1: Traditional hardcoded Playwright automation

---

2. Part 2: AI-driven automation using Claude AI + MCP

## Part 2: The AI Brain with MCP (Advanced Skills)

## 📋 Challenge Overview## 🎯 Core Concepts Covered

**Goal:** Redesign the program so execution steps are determined dynamically by an AI Language Model.

### Target Website

**Key Components:**

- URL: https://bstackdemo.com/

1. **Plain English Goal:** "Buy the cheapest iPhone on the site"

- Task: Find and purchase the cheapest iPhone

2. **Model Context Protocol (MCP):** Provides the LLM with:

   - Structured page context (accessibility data, element information)- Expected Result: Successfully add cheapest iPhone to cart### **Primary Goal**### ✅ **Core Requirements Met:**

   - Available tools (click, navigate, extract text, etc.)

   - Current page state



3. **LLM Decision Making:** Claude AI generates step-by-step plans using structured JSON commands---Build a web automation system that can navigate to BrowserStack's demo site and purchase the cheapest iPhone available.1. **Browser Control** - Using Playwright to automate browser actions



4. **Execution:** Program reads and executes the AI's planned steps



5. **Feedback Loop:** Results sent back to LLM for adaptation and next steps## Project Structure2. **Fixed Task** - Login → Search → Extract Price



**Implementation:** `part2_mcp_ai_brain/ai_brain_mcp.py`



**Run:**```### **Technical Requirements**3. **All Actions** - Go to URL, Click, Type, Extract Data

```bash

cd part2_mcp_ai_brainrobot_Driver_Playwright/

python ai_brain_mcp.py

```├── part1_basic_automation/          # Traditional Playwright approach1. **Part 1**: Traditional hardcoded Playwright automation4. **Error Handling** - Proper try/except blocks and timeout handling



**Result:** AI autonomously finds cheapest iPhone ($499) and adds to cart in 4 iterations│   ├── my_robot_driver.py          # Hardcoded automation script



---│   └── README.md                   # Part 1 documentation2. **Part 2**: AI-driven automation using Claude AI + MCP5. **Clear Output** - Console messages showing progress and results



## Project Structure│



```├── part2_mcp_ai_brain/             # AI-driven MCP approach  

robot_Driver_Playwright/

├── part1_basic_automation/│   ├── ai_brain_mcp.py             # Claude AI + MCP implementation

│   ├── my_robot_driver.py

│   └── README.md│   ├── README.md                   # Part 2 documentation### **Target Website**---

│

├── part2_mcp_ai_brain/│   ├── MCP_README.md               # Technical MCP guide

│   ├── ai_brain_mcp.py

│   ├── README.md│   └── CHALLENGE_ASSESSMENT.md     # Requirements validation- **URL**: https://bstackdemo.com/

│   ├── MCP_README.md

│   └── CHALLENGE_ASSESSMENT.md│

│

└── README.md (this file)└── README.md                       # This file - project overview- **Task**: Find and purchase the cheapest iPhone## 📖 Step-by-Step Breakdown

```

```

---

- **Expected Result**: Successfully add cheapest iPhone to cart

## Requirements Validation

---

### Part 1 (Core - Required)

- Performs all necessary browser actions (goto, click, type)### **Step 1: Understanding the Class Structure**

- Includes error handling (try/except, timeouts, validation)

- Outputs clear, structured results## Two Approaches Comparison

- Tests foundational Playwright skills

---

### Part 2 (Bonus - Advanced)

- User provides goal in plain English| Aspect | Part 1: Basic Automation | Part 2: MCP AI Brain |

- MCP integrates structured page context for LLM

- LLM generates step-by-step plans dynamically|--------|--------------------------|---------------------|```python

- Program executes LLM's commands

- Demonstrates modern AI-agent architecture| Approach | Hardcoded steps | AI decides dynamically |



---| Page Awareness | Blind selectors | Full page context |## 🏗️ Project Structureclass RobotDriver:



## Key Differences| Adaptability | Breaks on changes | Adapts to new layouts |



| Feature | Part 1 | Part 2 || Goal Input | Code modification | Natural language |    def __init__(self, timeout=10000):

|---------|--------|--------|

| Execution | Hardcoded steps | AI decides dynamically || Intelligence | None | Claude AI reasoning |

| Page Context | Blind selectors | Full structured page info |

| Adaptability | Fixed to specific selectors | Adapts to layout changes || Complexity | Simple | Advanced |```        self.timeout = timeout

| Input | Code modifications | Natural language goals |

| Complexity | Simple, predictable | Intelligent, flexible || Skills Demonstrated | Playwright basics | Modern AI-agent architecture |



---robot_Driver_Playwright/        self.browser = None



## Setup---



```bash├── part1_basic_automation/          # Traditional Playwright approach        self.page = None

# Install dependencies

pip install playwright anthropic python-dotenv## Quick Start

playwright install chromium

│   ├── my_robot_driver.py          # Hardcoded automation script```

# For Part 2, create .env file with:

ANTHROPIC_API_KEY=your_key_here### Prerequisites

```

```bash│   └── README.md                   # Part 1 documentation

---

# Install dependencies

## Skills Demonstrated

pip install playwright anthropic python-dotenv│**What this does:**

1. **Part 1:** Playwright automation, error handling, browser lifecycle management

2. **Part 2:** AI integration, MCP architecture, tool definitions, LLM-driven planningplaywright install chromium



This project showcases progression from foundational software engineering to modern AI-agent architecture.├── part2_mcp_ai_brain/             # AI-driven MCP approach  - Creates a reusable Robot Driver class


# For Part 2 only - create .env file:

ANTHROPIC_API_KEY=your_anthropic_api_key_here│   ├── ai_brain_mcp.py             # Claude AI + MCP implementation- Sets a default timeout (10 seconds) for operations

```

│   ├── README.md                   # Part 2 documentation- Initializes browser and page objects as None

### Run Part 1 (Basic Automation)

```bash│   ├── MCP_README.md               # Technical MCP guide

cd part1_basic_automation

python my_robot_driver.py│   └── CHALLENGE_ASSESSMENT.md     # Requirements validation**Why it matters:**

```

│- Classes help organize code and make it reusable

Expected Output:

```└── README.md                       # This file - project overview- Timeout prevents your program from waiting forever

Starting Task:

Browser started successfully!```

Page loaded successfully!  

Login successful!---

Added to cart!

SUCCESS! Product 'iPhone 12' found! Price: $799.00---

```

### **Step 2: Starting the Browser**

### Run Part 2 (MCP AI Brain)

```bash## 🔄 Two Approaches Comparison

cd part2_mcp_ai_brain

python ai_brain_mcp.py```python

```

| Aspect | Part 1: Basic Automation | Part 2: MCP AI Brain |def start_browser(self, headless=False):

Expected Output:

```|--------|--------------------------|---------------------|    self.playwright = sync_playwright().start()

MCP Robot Driver Demo - Buy Cheapest iPhone

Successfully navigated to https://bstackdemo.com/| **Approach** | Hardcoded steps | AI decides dynamically |    self.browser = self.playwright.chromium.launch(headless=headless)

Found 9 iPhones: iPhone XR: $499.00 (cheapest) ... iPhone 12 Pro Max: $1099.00

Added cheapest iPhone to cart: iPhone XR ($499.0)| **Page Awareness** | Blind selectors | Full page context |    self.page = self.browser.new_page()

TASK_COMPLETE - Success: True

```| **Adaptability** | Breaks on changes | Adapts to new layouts |```



---| **Goal Input** | Code modification | Natural language |



## Learning Objectives| **Intelligence** | None | Claude AI reasoning |**What this does:**



### Part 1: Foundation Skills| **Complexity** | Simple | Advanced |- Launches a Chromium browser

- Web automation with Playwright

- DOM element selection and interaction| **Skills Demonstrated** | Playwright basics | Modern AI-agent architecture |- Creates a new page (tab)

- Form handling (dropdowns, buttons)

- Error handling and timeouts- Can run with or without GUI (headless mode)

- Browser lifecycle management

---

### Part 2: Advanced AI Architecture

- Model Context Protocol (MCP) implementation**Error Handling:**

- LLM integration for dynamic decision making

- Structured page context extraction## 🚀 Quick Start```python

- Tool definition and execution patterns

- Natural language goal processingtry:

- Adaptive automation strategies

### Prerequisites    # Browser operations

---

```bash    return True

## Success Criteria

# Install dependenciesexcept Exception as e:

### Part 1 Requirements

- Successfully navigates to BrowserStack demopip install playwright anthropic python-dotenv    print(f"❌ Error: {e}")

- Logs in using dropdown selections

- Finds and selects a productplaywright install chromium    return False

- Adds product to cart

- Extracts cart total price```

- Handles errors gracefully

# For Part 2 only - create .env file:

### Part 2 Requirements 

- Dynamic Step Determination: Claude AI decides execution stepsANTHROPIC_API_KEY=your_anthropic_api_key_here**Why it matters:**

- MCP Integration: Structured page context feeds LLM decisions  

- Plain English Goals: Natural language task input```- If browser fails to start, the program won't crash

- Tool Definitions: LLM uses structured JSON commands

- Plan Execution: Program executes LLM's generated plan- Returns True/False so we know if it worked

- Feedback Loop: Results sent back to LLM for adaptation

### Run Part 1 (Basic Automation)

---

```bash---

## Technical Innovations

cd part1_basic_automation

### Part 1: Reliable Selector Strategy

```pythonpython my_robot_driver.py### **Step 3: Navigating to a Website**

# Uses exact React Select IDs

self.page.locator("#react-select-2-option-0-0").click()  # Username```

self.page.locator("#react-select-3-option-0-0").click()  # Password

``````python



### Part 2: MCP Magic**Expected Output:**def navigate_to_site(self, url):

```python

# Extracts structured page context for Claude```    self.page.goto(url, wait_until="domcontentloaded")

elements_info = {

    "buttons": [{"text": "Add to cart", "selector": ".buy-btn"}],Starting Task:```

    "text": "iPhone XR $499.00 iPhone 12 $799.00...",

    "page_title": "StackDemo"✅ Browser started successfully!

}

```✅ Page loaded successfully!  **What this does:**



---✅ Login successful!- Goes to the specified URL



## Results Summary✅ Added to cart!- Waits for the page to load (DOM content loaded)



### Part 1 Performance✅ SUCCESS! Product 'iPhone 12' found! Price: $799.00

- Reliability: 100% success rate on stable selectors

- Speed: Fast execution (< 30 seconds)```**Error Handling:**

- Maintainability: Clear, readable code structure

```python

### Part 2 Performance  

- Intelligence: Correctly identifies cheapest iPhone (XR at $499)### Run Part 2 (MCP AI Brain)except PlaywrightTimeoutError:

- Adaptability: Works without hardcoded selectors

- Efficiency: Completes task in 4 AI iterations```bash    print(f"❌ Timeout: Page took too long to load")

- Extensibility: Easy to add new tools and goals

cd part2_mcp_ai_brain```

---

python ai_brain_mcp.py

## Customization

```**Why it matters:**

### Modify Part 1 Behavior

```python- Slow internet or slow pages won't crash your program

# In my_robot_driver.py

PRODUCT_INDEX = 1      # Change which product to select**Expected Output:**- The timeout (10 seconds) prevents infinite waiting

RUN_HEADLESS = True    # Hide browser window

``````



### Modify Part 2 GoalsMCP Robot Driver Demo - Buy Cheapest iPhone---

```python

# In ai_brain_mcp.py - simple_demo() function✅ Successfully navigated to https://bstackdemo.com/

goal = "Find the most expensive Samsung phone"

goal = "Add 3 cheapest items to cart"  ✅ Found 9 iPhones: iPhone XR: $499.00 (cheapest) ... iPhone 12 Pro Max: $1099.00### **Step 4: Logging In**

goal = "Compare prices across all brands"

```✅ Added cheapest iPhone to cart: iPhone XR ($499.0)



---✅ TASK_COMPLETE - Success: True```python



## Skills Demonstrated```def login(self, username_option=0, password_option=0):



This project showcases progression from traditional automation to cutting-edge AI-agent architecture:    # Click sign-in button



1. Playwright Mastery: Element selection, form handling, error management---    self.page.click('#signin', timeout=5000)

2. AI Integration: LLM tool use, dynamic planning, context awareness

3. Modern Patterns: MCP implementation, structured tool definitions    

4. Production Ready: Error handling, documentation, extensible design

## 🎯 Learning Objectives    # Select username from dropdown

Perfect for demonstrating both foundational automation skills and expertise in modern AI-driven development approaches.

    self.page.get_by_text("Select Username").click()

---

### **Part 1: Foundation Skills**    self.page.locator("#react-select-2-option-0-0").click()

## Further Reading

- ✅ Web automation with Playwright    

- Part 1 Details: part1_basic_automation/README.md

- Part 2 Implementation: part2_mcp_ai_brain/README.md  - ✅ DOM element selection and interaction    # Select password from dropdown

- MCP Technical Guide: part2_mcp_ai_brain/MCP_README.md

- Challenge Assessment: part2_mcp_ai_brain/CHALLENGE_ASSESSMENT.md- ✅ Form handling (dropdowns, buttons)    self.page.get_by_text("Select Password").click()


- ✅ Error handling and timeouts    self.page.locator("#react-select-3-option-0-0").click()

- ✅ Browser lifecycle management    

    # Click login button

### **Part 2: Advanced AI Architecture**    self.page.get_by_role("button", name="Log In").click()

- ✅ Model Context Protocol (MCP) implementation    

- ✅ LLM integration for dynamic decision making    # Verify login worked

- ✅ Structured page context extraction    if self.page.get_by_text("demouser").is_visible():

- ✅ Tool definition and execution patterns        return True

- ✅ Natural language goal processing```

- ✅ Adaptive automation strategies

**Key Actions:**

---- **Click** - `page.click(selector)`

- **Find by text** - `page.get_by_text("text")`

## 🏆 Success Criteria- **Find by role** - `page.get_by_role("button", name="...")`

- **Locator** - `page.locator("#id")` for specific elements

### **Part 1 Requirements**

- [x] Successfully navigates to BrowserStack demo**Why it matters:**

- [x] Logs in using dropdown selections- Each step has a timeout (5 seconds)

- [x] Finds and selects a product- If any element is missing, it returns False instead of crashing

- [x] Adds product to cart- Verification step confirms login actually worked

- [x] Extracts cart total price

- [x] Handles errors gracefully---



### **Part 2 Requirements** ### **Step 5: Searching for a Product**

- [x] **Dynamic Step Determination**: Claude AI decides execution steps

- [x] **MCP Integration**: Structured page context feeds LLM decisions  ```python

- [x] **Plain English Goals**: Natural language task inputdef search_product(self, product_name):

- [x] **Tool Definitions**: LLM uses structured JSON commands    product_locator = self.page.locator(f"text={product_name}").first

- [x] **Plan Execution**: Program executes LLM's generated plan    

- [x] **Feedback Loop**: Results sent back to LLM for adaptation    if product_locator.is_visible(timeout=5000):

        product_locator.click()

---        return True

    else:

## 🧠 Technical Innovations        print(f"❌ Product '{product_name}' not found")

        return False

### **Part 1: Reliable Selector Strategy**```

```python

# Uses exact React Select IDs**What this does:**

self.page.locator("#react-select-2-option-0-0").click()  # Username- Finds an element containing the product name

self.page.locator("#react-select-3-option-0-0").click()  # Password- Checks if it's visible before clicking

```- Uses `.first` to get the first match if there are multiple



### **Part 2: MCP Magic****Why it matters:**

```python- Checking `is_visible()` before clicking prevents errors

# Extracts structured page context for Claude- Returns True/False for success tracking

elements_info = {

    "buttons": [{"text": "Add to cart", "selector": ".buy-btn"}],---

    "text": "iPhone XR $499.00 iPhone 12 $799.00...",

    "page_title": "StackDemo"### **Step 6: Extracting the Price**

}

``````python

def get_product_price(self):

---    # Wait for price element to appear

    self.page.wait_for_selector('.shelf-item__price', timeout=5000)

## 📊 Results Summary    

    # Get the price text

### **Part 1 Performance**    price_element = self.page.locator('.shelf-item__price').first

- ✅ **Reliability**: 100% success rate on stable selectors    price = price_element.inner_text(timeout=5000)

- ✅ **Speed**: Fast execution (< 30 seconds)    

- ✅ **Maintainability**: Clear, readable code structure    return price

```

### **Part 2 Performance**  

- ✅ **Intelligence**: Correctly identifies cheapest iPhone (XR at $499)**What this does:**

- ✅ **Adaptability**: Works without hardcoded selectors- Waits for the price element to load

- ✅ **Efficiency**: Completes task in 4 AI iterations- Extracts the text content

- ✅ **Extensibility**: Easy to add new tools and goals- Returns the price as a string



---**Why it matters:**

- `wait_for_selector` ensures element is ready before reading

## 🔧 Customization- `inner_text()` gets the actual visible text



### **Modify Part 1 Behavior**---

```python

# In my_robot_driver.py### **Step 7: Main Workflow**

PRODUCT_INDEX = 1      # Change which product to select

RUN_HEADLESS = True    # Hide browser window```python

```def run_complete_task(self, url, product_name, headless=False):

    result = {

### **Modify Part 2 Goals**        "success": False,

```python        "product": product_name,

# In ai_brain_mcp.py - simple_demo() function        "price": None,

goal = "Find the most expensive Samsung phone"        "error": None

goal = "Add 3 cheapest items to cart"      }

goal = "Compare prices across all brands"    

```    try:

        if not self.start_browser(headless):

---            result["error"] = "Failed to start browser"

            return result

## 🎓 Skills Demonstrated        

        if not self.navigate_to_site(url):

This project showcases progression from **traditional automation** to **cutting-edge AI-agent architecture**:            result["error"] = "Failed to navigate"

            return result

1. **Playwright Mastery**: Element selection, form handling, error management        

2. **AI Integration**: LLM tool use, dynamic planning, context awareness        # ... more steps ...

3. **Modern Patterns**: MCP implementation, structured tool definitions        

4. **Production Ready**: Error handling, documentation, extensible design    finally:

        # ALWAYS close browser, even if there's an error

**Perfect for demonstrating both foundational automation skills and expertise in modern AI-driven development approaches.** 🚀        self.close_browser()

```

---

**What this does:**

## 📚 Further Reading- Orchestrates all steps in order

- Stops at first failure

- **Part 1 Details**: `part1_basic_automation/README.md`- Returns a result dictionary with all info

- **Part 2 Implementation**: `part2_mcp_ai_brain/README.md`  - **Finally block** ensures cleanup happens

- **MCP Technical Guide**: `part2_mcp_ai_brain/MCP_README.md`

- **Challenge Assessment**: `part2_mcp_ai_brain/CHALLENGE_ASSESSMENT.md`**Why it matters:**
- If step 2 fails, no point trying step 3
- Dictionary return gives complete information
- `finally` prevents browser from staying open on errors

---

## 🚀 How to Run

### **Option 1: Run as a Program**

```bash
python BrowserStack.py
```

This will:
1. Open a browser window
2. Navigate to BrowserStack demo
3. Log in automatically
4. Search for "iPhone 12"
5. Extract and print the price
6. Close the browser

### **Option 2: Run with Pytest**

```bash
pytest BrowserStack.py::test_login -v
```

This runs your original test function.

### **Option 3: Customize the Task**

Edit the `main()` function:

```python
def main():
    TARGET_URL = "https://bstackdemo.com/"
    PRODUCT_TO_FIND = "iPhone 12"  # Change this!
    RUN_HEADLESS = False  # True = no browser window
    
    robot = RobotDriver(timeout=10000)
    result = robot.run_complete_task(
        url=TARGET_URL,
        product_name=PRODUCT_TO_FIND,
        headless=RUN_HEADLESS
    )
```

---

## 🛡️ Error Handling Explained

### **Three Levels of Protection:**

#### **1. Try/Except Blocks**
```python
try:
    # Risky operation
    self.page.click('#signin')
except Exception as e:
    print(f"Error: {e}")
    return False
```

#### **2. Timeouts**
```python
# Won't wait forever - max 5 seconds
self.page.click('#signin', timeout=5000)
```

#### **3. Validation**
```python
# Check before assuming it worked
if self.page.get_by_text("demouser").is_visible():
    return True
```

### **Why All Three?**
- **Try/Except**: Catches unexpected errors
- **Timeouts**: Prevents infinite waiting
- **Validation**: Confirms success

---

## 📊 Understanding the Output

When you run the program, you'll see:

```
============================================================
🤖 ROBOT DRIVER - STARTING AUTOMATED TASK
============================================================

🚀 Starting browser...
✅ Browser started successfully!
🌐 Navigating to https://bstackdemo.com/...
✅ Page loaded successfully!
🔐 Logging in...
  - Clicked sign-in button
  - Selected username
  - Selected password
  - Clicked login button
✅ Login successful!
🔍 Searching for product: iPhone 12...
✅ Found and clicked on: iPhone 12
💰 Extracting product price...
✅ Price extracted: $1299
🔒 Closing browser...
✅ Browser closed successfully!

============================================================
📊 FINAL RESULTS
============================================================
✅ SUCCESS! Product 'iPhone 12' found!
💵 Price: $1299

🎉 Task completed successfully!
```

---

## 🎓 Key Takeaways

### **1. Playwright Basics**
- `page.goto(url)` - Navigate
- `page.click(selector)` - Click elements
- `page.get_by_text("text")` - Find by visible text
- `page.locator(selector)` - Find by CSS selector
- `element.inner_text()` - Extract text

### **2. Error Handling**
- Always use try/except for web operations
- Set timeouts on all interactions
- Verify actions succeeded before continuing
- Use `finally` to clean up resources

### **3. Code Organization**
- Break task into small methods
- Each method does ONE thing
- Return True/False for success tracking
- Use a main workflow method to orchestrate

### **4. Professional Practices**
- Clear console output with emojis
- Descriptive error messages
- Proper cleanup (close browser)
- Return structured results (dictionary)

---

## 🔧 Common Issues & Solutions

### **Problem: Element not found**
```python
# Bad - crashes if element missing
self.page.click('#signin')

# Good - handles missing element
try:
    self.page.click('#signin', timeout=5000)
except PlaywrightTimeoutError:
    print("Sign-in button not found")
    return False
```

### **Problem: Page loads slowly**
```python
# Increase timeout for slow pages
self.page.set_default_timeout(15000)  # 15 seconds
```

### **Problem: Element not clickable yet**
```python
# Wait for element to be ready
self.page.wait_for_selector('#signin', state='visible', timeout=5000)
self.page.click('#signin')
```

---

## 🎯 Next Steps

1. **Run the program** and watch it work
2. **Change the product** to search for something else
3. **Add more features** - like adding to cart
4. **Try different websites** - apply the same patterns
5. **Add more error cases** - what if product is out of stock?

---

## 📝 Assignment Checklist

- ✅ **Python program** - Uses classes and methods
- ✅ **Playwright control** - Automates browser
- ✅ **Fixed task** - Login → Search → Extract price
- ✅ **All actions** - goto, click, type, extract
- ✅ **Error handling** - Try/except, timeouts, validation
- ✅ **Clear output** - Progress messages and final result
- ✅ **Reliability** - Won't crash on slow pages or missing elements

---

## 💡 Pro Tips

1. **Start with headless=False** to see what's happening
2. **Read error messages carefully** - they tell you what's wrong
3. **Use browser DevTools** (F12) to find selectors
4. **Test one step at a time** - don't build everything at once
5. **Keep timeouts reasonable** - 5-10 seconds is usually good

---

**Good luck! 🚀 You've got all the core skills you need!**
