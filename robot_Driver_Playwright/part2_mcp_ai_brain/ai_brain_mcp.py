"""
AI ROBOT DRIVER - STEP 2: THE AI BRAIN WITH MCP
================================================
This program demonstrates:
1. Using Claude AI to determine execution steps dynamically
2. Integrating with Playwright MCP Server for browser control
3. Natural language task processing

Example: "Buy the cheapest blue shirt on this site"
"""

import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Load environment variables
load_dotenv()


class AIRobotDriver:
    """
    AI-Powered Robot Driver that uses Claude to plan and execute browser tasks
    """
    
    def __init__(self):
        """Initialize the AI Robot Driver with Anthropic client"""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not found! "
                "Please set it in your .env file or environment."
            )
        
        self.client = Anthropic(api_key=api_key)
        self.conversation_history = []
        self.playwright = None
        self.browser = None
        self.page = None
        
    def _define_tools(self):
        """Define the tools available to Claude"""
        return [
            {
                "name": "playwright_navigate",
                "description": "Navigate to a URL in the browser",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "The URL to navigate to"
                        }
                    },
                    "required": ["url"]
                }
            },
            {
                "name": "playwright_click",
                "description": "Click an element on the page using a selector",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "selector": {
                            "type": "string",
                            "description": "CSS selector of the element to click"
                        }
                    },
                    "required": ["selector"]
                }
            },
            {
                "name": "playwright_fill",
                "description": "Type text into an input field",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "selector": {
                            "type": "string",
                            "description": "CSS selector of the input field"
                        },
                        "text": {
                            "type": "string",
                            "description": "Text to type into the field"
                        }
                    },
                    "required": ["selector", "text"]
                }
            },
            {
                "name": "playwright_wait",
                "description": "Wait for an element to appear",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "selector": {
                            "type": "string",
                            "description": "CSS selector to wait for"
                        }
                    },
                    "required": ["selector"]
                }
            },
            {
                "name": "playwright_find_cheapest_product",
                "description": "Find the cheapest iPhone product on the page and return its details",
                "input_schema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "playwright_click_cheapest_iphone",
                "description": "Find the cheapest iPhone and click its 'Add to cart' button",
                "input_schema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "playwright_get_page_info",
                "description": "Get accessibility tree and visible elements on the current page. Returns structured data about buttons, inputs, text, and other interactive elements.",
                "input_schema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "playwright_get_text",
                "description": "Get all visible text from the current page",
                "input_schema": {
                    "type": "object",
                    "properties": {}
                }
            }
        ]

    def _execute_tool(self, tool_name: str, tool_input: dict):
        """Execute the tool that Claude requested"""
        try:
            if tool_name == "playwright_navigate":
                url = tool_input.get("url")
                self.page.goto(url)
                return f"Successfully navigated to {url}"
            
            elif tool_name == "playwright_click":
                selector = tool_input.get("selector")
                self.page.click(selector)
                return f"Clicked {selector}"
            
            elif tool_name == "playwright_fill":
                selector = tool_input.get("selector")
                text = tool_input.get("text")
                self.page.fill(selector, text)
                return f"Typed into {selector}"
            
            elif tool_name == "playwright_wait":
                selector = tool_input.get("selector")
                self.page.wait_for_selector(selector, timeout=5000)
                return f"Element appeared: {selector}"
            
            elif tool_name == "playwright_find_cheapest_product":
                try:
                    # Get page text and extract iPhone prices
                    page_text = self.page.inner_text("body")
                    
                    import re
                    # Find all iPhone mentions with prices
                    iphone_pattern = r'(iPhone[^$]*)\s*\$([0-9,]+\.?[0-9]*)'
                    matches = re.findall(iphone_pattern, page_text)
                    
                    products = []
                    for name_part, price_str in matches:
                        try:
                            price = float(price_str.replace(',', ''))
                            name = name_part.strip()
                            products.append({'name': name, 'price': price, 'price_text': f'${price_str}'})
                        except:
                            continue
                    
                    if products:
                        cheapest = min(products, key=lambda x: x['price'])
                        all_prices = [f"{p['name']}: {p['price_text']}" for p in products]
                        return f"Found {len(products)} iPhones: {', '.join(all_prices)}. Cheapest: {cheapest['name']} at {cheapest['price_text']}"
                    else:
                        return f"No iPhone products found in text: {page_text[:500]}"
                        
                except Exception as e:
                    return f"Error finding products: {str(e)}"
            
            elif tool_name == "playwright_click_cheapest_iphone":
                try:
                    # Get page text and find cheapest iPhone
                    page_text = self.page.inner_text("body")
                    
                    import re
                    iphone_pattern = r'(iPhone[^$]*)\s*\$([0-9,]+\.?[0-9]*)'
                    matches = re.findall(iphone_pattern, page_text)
                    
                    products = []
                    for name_part, price_str in matches:
                        try:
                            price = float(price_str.replace(',', ''))
                            name = name_part.strip()
                            products.append({'name': name, 'price': price})
                        except:
                            continue
                    
                    if products:
                        cheapest = min(products, key=lambda x: x['price'])
                        
                        # Find the "Add to cart" button near this iPhone name
                        # Look for elements containing the iPhone name
                        iphone_text = cheapest['name'].split()[0] + " " + cheapest['name'].split()[1]  # e.g. "iPhone XR"
                        
                        # Try different selectors to find the add to cart button
                        selectors_to_try = [
                            f"text='{iphone_text}' >> .. >> text='Add to cart'",
                            f":has-text('{iphone_text}') >> text='Add to cart'",
                            f"div:has-text('{iphone_text}') >> button:has-text('Add to cart')",
                            "button:has-text('Add to cart')"
                        ]
                        
                        for selector in selectors_to_try:
                            try:
                                buttons = self.page.locator(selector).all()
                                if buttons:
                                    buttons[0].click()
                                    return f"Added cheapest iPhone to cart: {cheapest['name']} (${cheapest['price']})"
                            except:
                                continue
                                
                        return f"Found cheapest iPhone {cheapest['name']} but couldn't find its add to cart button"
                    else:
                        return "No iPhone products found to add to cart"
                        
                except Exception as e:
                    return f"Error adding to cart: {str(e)}"
            
            elif tool_name == "playwright_get_page_info":
                page_info = self._get_page_accessibility_tree()
                return page_info
            
            elif tool_name == "playwright_get_text":
                text_content = self.page.inner_text("body")
                return f"Page text: {text_content[:2000]}"
            
            else:
                return f"Unknown tool: {tool_name}"
                
        except Exception as e:
            return f"Error: {str(e)}"

    def _get_page_accessibility_tree(self):
        """
        Get accessibility tree and visible elements - THIS IS THE MCP MAGIC!
        Returns structured info about interactive elements on the page
        """
        try:
            # Get all important elements
            elements_info = {
                "buttons": [],
                "inputs": [],
                "links": [],
                "dropdown_options": [],
                "text": [],
                "page_title": self.page.title()
            }
            
            # Find all buttons and their text
            buttons = self.page.locator("button, [role='button']").all()
            for i, button in enumerate(buttons[:15]):  # Limit to first 15
                try:
                    text = button.inner_text()
                    selector = self._get_selector(button)
                    if text.strip():
                        elements_info["buttons"].append({
                            "index": i,
                            "text": text.strip(),
                            "selector": selector
                        })
                except:
                    pass
            
            # Find all input fields
            inputs = self.page.locator("input, textarea").all()
            for i, inp in enumerate(inputs[:15]):  # Limit to first 15
                try:
                    placeholder = inp.get_attribute("placeholder") or ""
                    input_type = inp.get_attribute("type") or "text"
                    selector = self._get_selector(inp)
                    elements_info["inputs"].append({
                        "index": i,
                        "type": input_type,
                        "placeholder": placeholder,
                        "selector": selector
                    })
                except:
                    pass
            
            # Find all links
            links = self.page.locator("a[href]").all()
            for i, link in enumerate(links[:15]):  # Limit to first 15
                try:
                    text = link.inner_text()
                    href = link.get_attribute("href")
                    selector = self._get_selector(link)
                    if text.strip():
                        elements_info["links"].append({
                            "index": i,
                            "text": text.strip(),
                            "href": href,
                            "selector": selector
                        })
                except:
                    pass
            
            # Find dropdown options if visible
            try:
                options = self.page.locator("[role='option']").all()
                for i, option in enumerate(options[:20]):  # Limit to first 20
                    try:
                        text = option.inner_text()
                        selector = self._get_selector(option)
                        if text.strip():
                            elements_info["dropdown_options"].append({
                                "index": i,
                                "text": text.strip(),
                                "selector": selector
                            })
                    except:
                        pass
            except:
                pass
            
            # Get visible text
            body_text = self.page.inner_text("body")
            elements_info["text"] = body_text[:2000]
            
            return f"Page Info:\n{json.dumps(elements_info, indent=2)}"
            
        except Exception as e:
            return f"Error getting page info: {str(e)}"
    
    def _get_selector(self, element):
        """Get a usable CSS selector for an element"""
        try:
            # Try to get ID
            elem_id = element.get_attribute("id")
            if elem_id:
                return f"#{elem_id}"
            
            # Try to get unique selector via evaluate
            selector = element.evaluate("""
                el => {
                    let path = [];
                    while (el.parentElement) {
                        let selector = el.tagName.toLowerCase();
                        if (el.id) {
                            selector += '#' + el.id;
                            path.unshift(selector);
                            break;
                        } else {
                            let sibling = el;
                            let nth = 1;
                            while (sibling = sibling.previousElementSibling) {
                                if (sibling.tagName.toLowerCase() == selector) nth++;
                            }
                            if (nth > 1) selector += ':nth-of-type(' + nth + ')';
                        }
                        path.unshift(selector);
                        el = el.parentElement;
                    }
                    return path.join(' > ');
                }
            """)
            return selector
        except:
            return "element"

    def execute_task_with_ai(self, goal: str, url: str, max_iterations: int = 5):
        """
        Execute a task using AI to determine steps dynamically
        
        Args:
            goal (str): Plain English description of what to do
            url (str): The website URL to work with
            max_iterations (int): Maximum iterations
            
        Returns:
            dict: Results of the operation
        """
        print(f"AI ROBOT DRIVER - Goal: {goal}")
        print(f"URL: {url}")
        
        result = {
            "success": False,
            "goal": goal,
            "steps_taken": [],
            "error": None
        }
        
        try:
            # Start Playwright
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=True)
            self.page = self.browser.new_page()
            
            # Define the tools Claude can use
            tools = self._define_tools()
            
            # Build system prompt with MCP instructions
            system_prompt = f"""You are an AI web automation agent controlling a browser via Playwright tools.

TASK: {goal}
TARGET: {url}

AVAILABLE TOOLS:
1. playwright_navigate(url) - Go to a website
2. playwright_find_cheapest_product() - Find the cheapest iPhone on the page
3. playwright_click_cheapest_iphone() - Add the cheapest iPhone to cart
4. playwright_get_page_info() - Get structured info about the page
5. playwright_screenshot() - Take a screenshot

SIMPLE WORKFLOW:
1. Navigate to the site
2. Find the cheapest iPhone product
3. Click "Add to cart" for that product
4. Say "TASK_COMPLETE"

IMPORTANT:
- The products are already visible on the main page - no login needed
- Use playwright_find_cheapest_product() to identify the cheapest iPhone
- Use playwright_click_cheapest_iphone() to add it to cart
- Keep it simple - just these 3 steps!

You will receive the current page structure in each step."""
            
            # Initialize conversation
            messages = [
                {
                    "role": "user",
                    "content": f"Please accomplish this task: {goal}"
                }
            ]
            
            # Loop - Claude responds, uses tools, we execute, repeat
            for iteration in range(max_iterations):
                print(f"Iteration {iteration + 1}/{max_iterations}")
                
                # Get Claude's response with tool support
                response = self.client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=1024,
                    system=system_prompt,
                    tools=tools,
                    messages=messages
                )
                
                print(f"  Claude response: {response.stop_reason}")
                
                # Add Claude's response to history
                messages.append({"role": "assistant", "content": response.content})
                
                # Check if Claude wants to use tools
                tool_results = []
                task_complete = False
                
                for block in response.content:
                    # Check for text that signals completion
                    if hasattr(block, 'text'):
                        text = block.text
                        if "TASK_COMPLETE" in text or "completed" in text.lower():
                            task_complete = True
                            result["success"] = True
                            print(f"  Task complete: {text[:100]}")
                    
                    # Handle tool use
                    if block.type == "tool_use":
                        tool_name = block.name
                        tool_input = block.input
                        tool_id = block.id
                        
                        print(f"  Tool: {tool_name} - Input: {tool_input}")
                        
                        # Execute the tool
                        tool_result = self._execute_tool(tool_name, tool_input)
                        print(f"  Result: {tool_result}")
                        
                        # Store result to send back to Claude
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": tool_id,
                            "content": tool_result
                        })
                        
                        result["steps_taken"].append({
                            "iteration": iteration + 1,
                            "tool": tool_name,
                            "result": tool_result
                        })
                
                # If Claude used tools, send results back
                if tool_results:
                    messages.append({
                        "role": "user",
                        "content": tool_results
                    })
                
                # If task is complete, break
                if task_complete:
                    break
                
                # If no tools were called and not complete, ask to continue
                if not tool_results and response.stop_reason == "end_turn":
                    print("No tools called. Asking to continue...")
                    messages.append({
                        "role": "user",
                        "content": "Please continue with the next step or say TASK_COMPLETE."
                    })
                    
        except Exception as e:
            result["error"] = str(e)
            print(f"Error: {e}")
        
        finally:
            # Clean up
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
        
        return result
def simple_demo():
    """
    Demo: Find and buy the cheapest iPhone (no login needed)
    """
    print("MCP Robot Driver Demo - Buy Cheapest iPhone\n")
    
    try:
        driver = AIRobotDriver()
        
        goal = "Find the cheapest iPhone on the page and add it to cart"
        url = "https://bstackdemo.com/"
        
        result = driver.execute_task_with_ai(goal, url, max_iterations=5)
        
        # Print results
        print("\nFINAL RESULTS")
        print(f"Goal: {result['goal']}")
        print(f"Success: {result['success']}")
        print(f"Steps Taken: {len(result['steps_taken'])}")
        for step in result['steps_taken']:
            tool = step['tool']
            result_text = step['result']
            if len(result_text) > 100:
                result_text = result_text[:100] + "..."
            print(f"  {step['iteration']}. {tool}: {result_text}")
        
        if result['error']:
            print(f"Error: {result['error']}")
            
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("1. Get API key from: https://console.anthropic.com/")
        print("2. Create .env file with: ANTHROPIC_API_KEY=your_key_here")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    simple_demo()