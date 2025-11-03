"""Core robot driver for Challenge 1 requirements."""

from __future__ import annotations

import argparse
import sys
from contextlib import suppress
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


PRODUCT_CARD_SELECTOR = ".shelf-item"
PRODUCT_TITLE_SELECTOR = ".shelf-item__title"
PRODUCT_PRICE_SELECTOR = ".shelf-item__price .val"

SIGN_IN_BUTTON_SELECTOR = "#signin"
USERNAME_MENU_TEXT = "Select Username"
PASSWORD_MENU_TEXT = "Select Password"
USERNAME_OPTION_PREFIX = "react-select-2-option"
PASSWORD_OPTION_PREFIX = "react-select-3-option"

STRATEGY_MATCH = "match"
STRATEGY_MIN_PRICE = "min_price"
STRATEGY_MAX_PRICE = "max_price"
ALLOWED_STRATEGIES = [STRATEGY_MATCH, STRATEGY_MIN_PRICE, STRATEGY_MAX_PRICE]


@dataclass
class RobotDriverResult:
    """Represents the outcome of a robot driver run."""

    requested_product: str
    matched_product: Optional[str]
    price: Optional[str]
    success: bool
    selection_strategy: str
    error: Optional[str] = None


class RobotDriver:
    """Encapsulates the BrowserStack demo automation logic."""

    def __init__(self, timeout_ms: int = 10_000) -> None:
        self.timeout_ms = timeout_ms
        self._playwright = None
        self._browser = None
        self.page = None

    # ------------------------------------------------------------------
    # Browser lifecycle helpers
    # ------------------------------------------------------------------
    def _start_browser(self, headless: bool) -> bool:
        try:
            print("Starting browser...")
            self._playwright = sync_playwright().start()
            self._browser = self._playwright.chromium.launch(headless=headless)
            self.page = self._browser.new_page()
            with suppress(Exception):
                self.page.set_default_timeout(self.timeout_ms)
            print("Browser started successfully.")
            return True
        except PlaywrightTimeoutError as exc:
            print(f"Playwright timeout while starting browser: {exc}")
        except Exception as exc:  # noqa: BLE001 - provide user friendly message
            print(f"Unexpected error starting browser: {exc}")
        return False

    def _close_browser(self) -> None:
        with suppress(Exception):
            if self._browser:
                self._browser.close()
        with suppress(Exception):
            if self._playwright:
                self._playwright.stop()
        print("Browser closed")

    # ------------------------------------------------------------------
    # Core automation steps
    # ------------------------------------------------------------------
    def _navigate(self, url: str) -> bool:
        try:
            print(f"Navigating to {url}")
            self.page.goto(url, wait_until="networkidle")
            print("Page loaded successfully.")
            return True
        except PlaywrightTimeoutError:
            print("Timeout: page took too long to load")
        except Exception as exc:  # noqa: BLE001
            print(f"Error navigating to site: {exc}")
        return False

    def _login(self, username_index: int, password_index: int) -> bool:
        try:
            print("Logging in...")
            self.page.click(SIGN_IN_BUTTON_SELECTOR, timeout=5_000)
            self._select_drop_down_option(USERNAME_MENU_TEXT, USERNAME_OPTION_PREFIX, username_index)
            self._select_drop_down_option(PASSWORD_MENU_TEXT, PASSWORD_OPTION_PREFIX, password_index)
            self.page.get_by_role("button", name="Log In").click(timeout=5_000)
            if self.page.get_by_text("demouser").is_visible(timeout=5_000):
                print("Login successful.")
                return True
            print("Login verification failed")
        except PlaywrightTimeoutError:
            print("Login timeout: element not found or page too slow")
        except Exception as exc:  # noqa: BLE001
            print(f"Error during login: {exc}")
        return False

    def _select_drop_down_option(self, menu_text: str, option_prefix: str, option_index: int) -> None:
        menu = self.page.get_by_text(menu_text)
        menu.click(timeout=5_000)
        option_selector = f"#{option_prefix}-{option_index}-{option_index}"
        self.page.locator(option_selector).click(timeout=5_000)

    def _locate_product(
        self,
        product_name: str,
        strategy: str,
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        try:
            print(f"Searching for product: {product_name} (strategy: {strategy})")
            self.page.wait_for_selector(PRODUCT_CARD_SELECTOR, timeout=10_000)
            entries = self._collect_catalog_entries()
            if not entries:
                print("No products found on the page")
                return False, None, "Price not available"

            if strategy == STRATEGY_MAX_PRICE:
                return self._select_by_price(entries, product_name, max)
            if strategy == STRATEGY_MIN_PRICE:
                return self._select_by_price(entries, product_name, min)
            return self._select_by_name(entries, product_name)
        except PlaywrightTimeoutError:
            print("Timeout waiting for products to load")
            return False, None, "Timed out waiting for products"
        except Exception as exc:  # noqa: BLE001
            print(f"Error searching for product: {exc}")
            return False, None, "Error occurred"

    def _collect_catalog_entries(self) -> List[dict]:
        entries: List[dict] = []
        cards = self.page.locator(PRODUCT_CARD_SELECTOR)
        total_cards = cards.count()
        for index in range(total_cards):
            card = cards.nth(index)
            try:
                title = card.locator(PRODUCT_TITLE_SELECTOR).inner_text().strip()
            except Exception:
                continue

            price_text = self._extract_price(card)
            price_value = self._parse_price(price_text)
            entries.append(
                {
                    "title": title,
                    "price_text": price_text,
                    "price_value": price_value,
                }
            )
        return entries

    def _select_by_price(
        self,
        entries: List[dict],
        product_name: str,
        reducer,
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        keyword = product_name.strip().lower()
        filtered = [entry for entry in entries if keyword and keyword in entry["title"].lower()]
        target_pool = filtered or entries
        target_pool = [entry for entry in target_pool if entry["price_value"] is not None]

        if not target_pool:
            print("Unable to determine product prices from catalog")
            return False, None, "Price not available"

        selected = reducer(target_pool, key=lambda entry: entry["price_value"])
        print(
            f"Selected product by price: {selected['title']} at {selected['price_text']}"
        )
        return True, selected["title"], selected["price_text"]

    def _select_by_name(
        self,
        entries: List[dict],
        product_name: str,
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        normalized_target = product_name.strip().lower()
        best_partial: Optional[Tuple[str, str]] = None

        for index, entry in enumerate(entries):
            title = entry["title"]
            price_text = entry["price_text"]
            normalized_title = title.lower().strip()
            print(f"Checking product {index + 1}: '{title}'")

            if normalized_title == normalized_target:
                return True, title, price_text

            if normalized_target and normalized_target in normalized_title and best_partial is None:
                best_partial = (title, price_text)

        if best_partial:
            match_title, match_price = best_partial
            print(f"Using closest match: {match_title}")
            return True, match_title, match_price

        print(f"Product '{product_name}' not found")
        return False, None, "Product not found"

    def _extract_price(self, card) -> str:
        try:
            price_text = card.locator(PRODUCT_PRICE_SELECTOR).inner_text().strip()
            if price_text:
                print(f"Product price: {price_text}")
                return price_text
        except Exception:
            pass
        return "Price not available"

    @staticmethod
    def _parse_price(price_text: str) -> Optional[float]:
        if not price_text or price_text == "Price not available":
            return None
        stripped = price_text.replace("$", "").replace(",", "").strip()
        try:
            return float(stripped)
        except ValueError:
            return None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def collect_catalog_snapshot(
        self,
        url: str,
        *,
        headless: bool = True,
        username_index: int = 0,
        password_index: int = 0,
    ) -> List[Dict[str, Any]]:
        """Gather the current product catalog without making a selection."""

        print("Collecting catalog snapshot for AI planning")

        if not self._start_browser(headless=headless):
            raise RuntimeError("Failed to start Playwright while gathering catalog snapshot")

        try:
            if not self._navigate(url):
                raise RuntimeError("Navigation failed during catalog snapshot")

            if not self._login(username_index=username_index, password_index=password_index):
                raise RuntimeError("Login failed during catalog snapshot")

            self.page.wait_for_selector(PRODUCT_CARD_SELECTOR, timeout=10_000)
            entries = self._collect_catalog_entries()
            return entries
        finally:
            self._close_browser()

    def run_complete_task(
        self,
        url: str,
        product_name: str = "iPhone 12",
        *,
        headless: bool = True,
        username_index: int = 0,
        password_index: int = 0,
        selection_strategy: str = STRATEGY_MATCH,
    ) -> RobotDriverResult:
        print("Starting Robot Driver Task")
        print(f"Target: {product_name}")

        if selection_strategy not in ALLOWED_STRATEGIES:
            raise ValueError(
                f"Unsupported selection strategy '{selection_strategy}'. "
                f"Choose from {ALLOWED_STRATEGIES}."
            )

        if not self._start_browser(headless=headless):
            return RobotDriverResult(
                requested_product=product_name,
                matched_product=None,
                price=None,
                success=False,
                selection_strategy=selection_strategy,
                error="Failed to start browser",
            )

        try:
            if not self._navigate(url):
                return RobotDriverResult(
                    requested_product=product_name,
                    matched_product=None,
                    price=None,
                    success=False,
                    selection_strategy=selection_strategy,
                    error="Failed to navigate to site",
                )

            if not self._login(username_index=username_index, password_index=password_index):
                return RobotDriverResult(
                    requested_product=product_name,
                    matched_product=None,
                    price=None,
                    success=False,
                    selection_strategy=selection_strategy,
                    error="Failed to login",
                )

            found, matched_name, price = self._locate_product(
                product_name,
                strategy=selection_strategy,
            )
            if not found or not price or price == "Price not available":
                return RobotDriverResult(
                    requested_product=product_name,
                    matched_product=matched_name,
                    price=price if price != "Price not available" else None,
                    success=False,
                    selection_strategy=selection_strategy,
                    error="Failed to extract product price",
                )

            print(f"SUCCESS! Found {matched_name} - Price: {price}")
            return RobotDriverResult(
                requested_product=product_name,
                matched_product=matched_name,
                price=price,
                success=True,
                selection_strategy=selection_strategy,
            )
        finally:
            self._close_browser()


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Robot Driver core task")
    parser.add_argument("--product", default="iPhone 12", help="Product name or keyword to search for")
    parser.add_argument("--url", default="https://bstackdemo.com/", help="Target site URL")
    parser.add_argument("--headless", dest="headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument("--show-browser", dest="headless", action="store_false", help="Display the browser window")
    parser.set_defaults(headless=True)
    parser.add_argument(
        "--strategy",
        choices=ALLOWED_STRATEGIES,
        default=STRATEGY_MATCH,
        help="Product selection strategy",
    )
    parser.add_argument("--timeout", type=int, default=10_000, help="Default timeout in milliseconds")
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    driver = RobotDriver(timeout_ms=args.timeout)
    result = driver.run_complete_task(
        url=args.url,
        product_name=args.product,
        headless=args.headless,
        selection_strategy=args.strategy,
    )

    print("\nFINAL RESULTS")
    print("-" * 50)
    if result.success:
        print(f"SUCCESS! Product '{result.matched_product or result.requested_product}' found.")
        print(f"Price: {result.price}")
        print("\nTask completed successfully.")
        return 0

    print(f"FAILED: {result.error}")
    print(f"Product searched: {result.requested_product}")
    print(f"Strategy used: {result.selection_strategy}")
    print("\nTask did not complete successfully.")
    return 1


if __name__ == "__main__":
    sys.exit(main())