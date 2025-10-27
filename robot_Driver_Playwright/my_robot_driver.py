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
    def __init__(self, timeout: int = 10000):
        self.playwright = None
        self.browser = None
        self.page = None
        self.timeout = timeout

    def start_browser(self, headless: bool = False):
        """
        Start Playwright and launch a Chromium browser.
        Returns True on success, False on failure.
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

    def close_browser(self):
        """Close browser and stop Playwright if running."""
        try:
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
            print("Browser closed")
        except Exception as e:
            print(f"Error closing browser: {e}")


def main():
    """runner to start the browser and exit so the script shows output."""
    driver = RobotDriver()
    ok = driver.start_browser(headless=False)
    if not ok:
        print("Failed to start browser.")
        return 1
    # Keep browser open for a short moment to test our function 
    print("Browser is running (will close in 2s)...")
    time.sleep(2)
    driver.close_browser()
    return 0


if __name__ == "__main__":
    sys.exit(main())