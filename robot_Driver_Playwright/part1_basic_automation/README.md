# Part 1: Basic Playwright Automation

## Overview
This is a traditional Playwright automation script that demonstrates fundamental web scraping and interaction skills.

## What It Does
- **Target Site**: BrowserStack Demo (https://bstackdemo.com/)
- **Goal**: Login → Find product → Add to cart → Get price
- **Approach**: Hardcoded step-by-step automation

## Key Features
**Browser Management** - Starts/stops Chromium browser  
**Navigation** - Goes to target website  
**Login Process** - Handles dropdown selections for username/password  
**Product Search** - Finds products by index or name  
**Cart Operations** - Adds items and extracts total price  
**Error Handling** - Robust timeout and exception management  

## Code Structure

### `RobotDriver` Class
```python
class RobotDriver:
    def __init__(self, timeout=10000)           # Initialize with timeout
    def start_browser(self, headless=False)     # Launch browser
    def navigate_to_site(self, url)             # Go to website
    def login(self, username_opt, password_opt) # Handle login dropdowns
    def add_to_cart_by_index(self, index)       # Add product by position
    def get_cart_total(self)                    # Extract final price
    def close_browser(self)                     # Clean up resources
    def run_complete_task(self, ...)            # Orchestrate full workflow
```

## How to Run

### Prerequisites
```bash
pip install playwright python-dotenv
playwright install chromium
```

### Execution
```bash
python my_robot_driver.py
```

### Expected Output
```
Starting Task:
Starting browser...
Browser started successfully!
Navigating to https://bstackdemo.com/
Page loaded successfully!
Logging In...
Clicked sign-in button
Selected username
Selected password
Clicked login button
Login successful!
Adding product #1 to cart...
Selected: iPhone 12
Added to cart!
Getting cart total...
Cart total: $799.00

FINAL RESULTS
SUCCESS! Product 'iPhone 12' found!
Price: $799.00
Task completed successfully!
```

## Technical Implementation

### Login Process
Uses exact selectors for React Select dropdowns:
```python
# Click dropdown triggers
self.page.get_by_text("Select Username").click()
self.page.get_by_text("Select Password").click()

# Select specific options by ID
self.page.locator("#react-select-2-option-0-0").click()  # Username
self.page.locator("#react-select-3-option-0-0").click()  # Password
```

### Product Selection
Reliable index-based approach:
```python
# Get all products
products = self.page.locator('.shelf-item').all()

# Select by index
product = products[product_index]
product_name = product.locator('.shelf-item__title').inner_text()
add_button = product.locator('.shelf-item__buy-btn')
add_button.click()
```

### Error Handling
Comprehensive timeout management:
```python
try:
    self.page.click('#signin', timeout=5000)
    self.page.wait_for_selector('.shelf-item', timeout=5000)
except PlaywrightError:
    print("Timeout: Element not found or page too slow")
    return False
```

## Configuration Options

### Headless Mode
```python
RUN_HEADLESS = False  # Set to True to hide browser window
```

### Product Selection
```python
PRODUCT_INDEX = 0  # 0 = first product, 1 = second, etc.
```

### Timeout Settings
```python
driver = RobotDriver(timeout=10000)  # 10 second default timeout
```

## Strengths of This Approach
- **Predictable**: Same steps every time
- **Fast**: Direct element targeting
- **Reliable**: Uses stable selectors
- **Simple**: Easy to understand and debug

## Limitations
- **Inflexible**: Can't adapt to page changes
- **Hardcoded**: Steps are predetermined
- **No Intelligence**: Doesn't make decisions based on content
- **Brittle**: Breaks if selectors change

## Success Criteria
Successfully logs into demo site  
Selects and adds product to cart  
Extracts cart total price  
Handles errors gracefully  
Clean browser lifecycle management  

This demonstrates solid foundation skills in web automation before moving to AI-driven approaches in Part 2.