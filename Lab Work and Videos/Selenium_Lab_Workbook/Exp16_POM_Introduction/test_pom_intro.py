"""
Experiment 16: Page Object Model Introduction (Assignment 7)
Module: Unit Test Frameworks - Page Object Model
Student: Rishita Paul
Date: September 8, 2026

Assignment 7: Page Object Model (POM) Restructure

Covers:
- Why to have a Framework
- What is Page Object Model
- BasePage and Util Concepts
- Separate page classes containing only locators and UI methods
- Test classes separated from page objects
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# ============================================
# BASE PAGE - Common utilities for all pages
# ============================================
class BasePage:
    """Base class with common web driver utilities"""

    def __init__(self, driver):
        """Initialize with webdriver instance"""
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def find(self, by, value):
        """Find element with wait for presence"""
        return self.wait.until(
            EC.presence_of_element_located((by, value))
        )

    def find_all(self, by, value):
        """Find multiple elements"""
        return self.driver.find_elements(by, value)

    def click(self, by, value):
        """Click element"""
        element = self.wait.until(
            EC.element_to_be_clickable((by, value))
        )
        element.click()

    def type_text(self, by, value, text):
        """Type text into element"""
        element = self.find(by, value)
        element.clear()
        element.send_keys(text)

    def get_text(self, by, value):
        """Get text from element"""
        element = self.wait.until(
            EC.visibility_of_element_located((by, value))
        )
        return element.text

    def get_url(self):
        """Get current URL"""
        return self.driver.current_url

    def wait_for_url_contains(self, text):
        """Wait for URL to contain specific text"""
        return self.wait.until(
            EC.url_contains(text)
        )


# ============================================
# PAGE CLASS - Login page with only locators and methods
# ============================================
class LoginPage(BasePage):
    """Login page - contains locators and UI methods only"""

    # ----- LOCATORS -----
    URL = "https://www.saucedemo.com/"
    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message-container")

    # ----- UI METHODS -----
    def open(self):
        """Navigate to login page"""
        self.driver.get(self.URL)

    def enter_username(self, username):
        """Enter username"""
        self.type_text(*self.USERNAME_FIELD, username)

    def enter_password(self, password):
        """Enter password"""
        self.type_text(*self.PASSWORD_FIELD, password)

    def click_login(self):
        """Click login button"""
        self.click(*self.LOGIN_BUTTON)

    def login(self, username, password):
        """Complete login action"""
        self.open()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        time.sleep(2)

    def get_error_message(self):
        """Get error message text if present"""
        try:
            error = self.find(*self.ERROR_MESSAGE)
            if error.is_displayed():
                return error.text
            return ""
        except Exception:
            return ""

    def is_login_successful(self):
        """Check if login succeeded"""
        return "/inventory.html" in self.driver.current_url


# ============================================
# PAGE CLASS - Dashboard/Inventory page
# ============================================
class DashboardPage(BasePage):
    """Dashboard/Inventory page - contains locators and methods"""

    # ----- LOCATORS -----
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    ADD_TO_CART_BACKPACK = (By.ID, "add-to-cart-sauce-labs-backpack")

    # ----- UI METHODS -----
    def is_loaded(self):
        """Check if dashboard is loaded"""
        return "/inventory.html" in self.driver.current_url

    def get_item_count(self):
        """Get number of inventory items"""
        return len(self.find_all(*self.INVENTORY_ITEMS))

    def add_backpack_to_cart(self):
        """Add backpack to cart"""
        self.click(*self.ADD_TO_CART_BACKPACK)
        time.sleep(1)

    def get_cart_count(self):
        """Get number of items in cart"""
        elements = self.find_all(*self.CART_BADGE)
        if elements:
            return int(elements[0].text)
        return 0

    def open_cart(self):
        """Open shopping cart"""
        self.click(*self.CART_LINK)
        time.sleep(1)


# ============================================
# TEST CLASS - Contains only test logic
# ============================================
class TestLoginPOM:
    """Tests using POM structure"""

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()
        self.login_page = LoginPage(self.driver)
        self.dashboard = DashboardPage(self.driver)

    def test_valid_login(self):
        """Test successful login using POM"""
        print("=" * 60)
        print("TEST: Valid Login via POM")
        print("=" * 60)
        self.login_page.login("standard_user", "secret_sauce")
        assert self.login_page.is_login_successful()
        print("✓ Valid login successful")

    def test_invalid_login(self):
        """Test invalid login using POM"""
        print("\n" + "=" * 60)
        print("TEST: Invalid Login via POM")
        print("=" * 60)
        self.login_page.login("wrong_user", "wrong_pass")
        error = self.login_page.get_error_message()
        assert error, "Error message should be shown"
        print(f"✓ Error message: {error[:50]}")

    def test_dashboard_interaction(self):
        """Test dashboard using POM"""
        print("\n" + "=" * 60)
        print("TEST: Dashboard Interaction via POM")
        print("=" * 60)
        self.login_page.login("standard_user", "secret_sauce")
        assert self.dashboard.is_loaded()
        print(f"✓ Dashboard loaded")

        item_count = self.dashboard.get_item_count()
        print(f"✓ Inventory items: {item_count}")

        self.dashboard.add_backpack_to_cart()
        cart_count = self.dashboard.get_cart_count()
        print(f"✓ Cart count: {cart_count}")
        assert cart_count == 1

    def run_all(self):
        """Run all tests then close browser"""
        try:
            self.test_valid_login()
            self.test_invalid_login()
            self.test_dashboard_interaction()
            print("\n" + "=" * 60)
            print("✓ All POM tests passed!")
        finally:
            self.driver.quit()
            print("Browser closed")


if __name__ == "__main__":
    test = TestLoginPOM()
    test.run_all()
