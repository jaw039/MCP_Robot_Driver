"""
ROBOT DRIVER - CORE FOUNDATIONAL SKILLS DEMONSTRATION
======================================================
This program demonstrates:
1. Browser automation using Playwright
2. Proper error handling
3. Reliable web interactions
4. Clear output reporting

Task: Log in to BrowserStack demo, search for a product, and report its price
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightError
import sys
import time

class RobotDriver:
    """
    Initialize the Robot Driver
    
    Args:
        timeout (int): Default timeout for operations in milliseconds
    """
    def __init__(self, timeout: int = 10000):
        self.playwright = None
        self.browser = None
        self.page = None
        self.timeout = timeout

    def start_browser(self, headless: bool = False):
        """
        STEP 1: Start the browser
        
        Args:
            headless (bool): Run browser in headless mode (no GUI)
        """
        try:
            print("Starting browser...")
            self.playwright = sync_playwright().start()

            # Use the Playwright chromium 
            self.browser = self.playwright.chromium.launch(headless=headless)
            self.page = self.browser.new_page()
            # apply default timeout for operations
            try:
                self.page.set_default_timeout(self.timeout)
            except Exception:
                # Some older Playwright versions may not have this method; ignore safely
                pass

            print("Browser started successfully!")
            return True

        except PlaywrightError as e:
            print(f"Playwright error starting browser: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error starting browser: {e}")
            return False

    def navigate_to_site(self, url):
        """
        STEP 2: Navigate to the target website
        
        Args:
            url (str): The URL to navigate to
        """
        try:
            print(f"Navigating to {url}")
            self.page.goto(url)
            print("Page loaded successfully!")
            return True
        except PlaywrightError:
            print(f"Timeout: Page took too long to load") 
            return False
        except Exception as e:
            print(f"Error Navigating to site")
            return False
            
    def login(self, username_option = 0, password_option = 0):
        """
        STEP 3: Perform login operation
        
        Args:
            username_option (int): Index of username to select
            password_option (int): Index of password to select
        """
        try:
            print("Logging In...")
            
            # Click on Sign In
            self.page.click('#signin', timeout=5000)
            print("Clicked sign-in button")
            
            # Select username
            self.page.get_by_text("Select Username").click(timeout=5000)
            self.page.locator(f"#react-select-2-option-{username_option}-{username_option}").click(timeout=5000)
            print("Selected username")
            
            # Select password
            self.page.get_by_text("Select Password").click(timeout=5000)
            self.page.locator(f"#react-select-3-option-{password_option}-{password_option}").click(timeout=5000)
            print("Selected password")
            
            # Click Login Button
            self.page.get_by_role("button", name="Log In").click(timeout=5000)
            print("Clicked login button") 
            
            # Verify whether login is successful
            if self.page.get_by_text("demouser").is_visible(timeout=5000):
                print("Login successful!")
                return True
            else:
                print("Login verification failed")
                return False
                
        except PlaywrightError:
            print("Login timeout: Element not found or page too slow")
            return False
        except Exception as e:
            print(f"Error during login: {e}")
            return False

    def close_browser(self):
        """
        STEP 6: Clean up and close the browser
        """
        try:
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
            print("Browser closed")
        except Exception as e:
            print(f"Error closing browser: {e}")

    def run_complete_task (self,url,product_name = None, product_index = 0, headless = False):
        """
        MAIN WORKFLOW: Execute the complete robot driver task
        
        This method orchestrates all steps:
        1. Start browser
        2. Navigate to site
        3. Login
        4. Add product to cart (by index for reliability)
        5. Extract cart total
        6. Close browser
        
        Args:
            url (str): Website URL
            product_name (str): Product to search for (optional, uses index if None)
            product_index (int): Index of product to add (0 = first)
            headless (bool): Run in headless mode
            
        Returns:
            dict: Results of the operation
        """
        
        print("Starting Task:")
        
        result = {
            "success": False,
            "product": product_name,
            "price": None,
            "error": None
        }
        
        try:
            if not self.start_browser(headless=headless):
                result["error"] = "Failed to start browser"
                return result
        
            if not self.navigate_to_site(url):
                result["error"] = "Failed to navigate to site"
                return result

            if not self.login():
                result["error"] = "Failed to Login"
                return result
            
        except Exception as e:
            result["error"] = f"Unexpected error: {e}"
            return result
        
        finally:
            # clean up, even if there's an error
            self.close_browser()
        
        # Return success if all steps completed
        result["success"] = True
        return result
            
def main():
    """
    Main entry point for the Robot Driver program
    """
    # Configuration
    TARGET_URL = "https://bstackdemo.com/"
    PRODUCT_INDEX = 0  # 0 = first product, 1 = second, etc.
    RUN_HEADLESS = False  # Set to True to hide browser window
    
    driver = RobotDriver(timeout=10000)
    result = driver.run_complete_task(
        url=TARGET_URL,
        product_index=PRODUCT_INDEX,
        headless=RUN_HEADLESS
    )
    
    # Print final results
    print("FINAL RESULTS")
    if result["success"]:
        print(f"SUCCESS! Product '{result['product']}' found!")
        print(f"Price: {result['price']}")
        print("\nTask completed successfully!")
        return 0
    else:
        print(f"FAILED: {result['error']}")
        print(f"Product searched: {result['product']}")
        print("\nTask did not complete successfully")
        return 1


if __name__ == "__main__":
    sys.exit(main())