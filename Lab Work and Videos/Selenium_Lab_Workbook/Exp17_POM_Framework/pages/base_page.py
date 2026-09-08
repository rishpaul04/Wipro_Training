"""
base_page.py - BasePage class for the POM framework
Module: Unit Test Frameworks - Page Object Model
Student: Rishita Paul
Date: September 8, 2026

The BasePage class provides common web driver methods that all
page classes inherit. This encapsulates common utility methods.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BasePage:
    """Base page class with common web driver utilities"""

    def __init__(self, driver, timeout=10):
        """Initialize base page with driver and default timeout"""
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout)

    # ----- Element Finding Methods -----
    def find_element(self, by, value):
        """Find element with wait for presence"""
        return self.wait.until(
            EC.presence_of_element_located((by, value))
        )

    def find_elements(self, by, value):
        """Find multiple elements"""
        return self.driver.find_elements(by, value)

    def find_visible(self, by, value):
        """Find element and wait for visibility"""
        return self.wait.until(
            EC.visibility_of_element_located((by, value))
        )

    # ----- Interaction Methods -----
    def click(self, by, value):
        """Click an element (JS click for reliability on React SPAs)"""
        element = self.wait.until(
            EC.element_to_be_clickable((by, value))
        )
        self.driver.execute_script("arguments[0].click();", element)

    def type_text(self, by, value, text):
        """Type text into a field (React-safe JS setter with native fallback)"""
        element = self.find_element(by, value)
        for _ in range(3):
            self.driver.execute_script(
                "var el = arguments[0];"
                "var setter = Object.getOwnPropertyDescriptor("
                "window.HTMLInputElement.prototype, 'value').set;"
                "setter.call(el, arguments[1]);"
                "el.dispatchEvent(new Event('input', {bubbles: true}));"
                "el.dispatchEvent(new Event('change', {bubbles: true}));",
                element, text)
            if element.get_attribute("value") == text:
                return
            element = self.find_element(by, value)
            element.clear()
            element.send_keys(text)
            if element.get_attribute("value") == text:
                return
            element = self.find_element(by, value)

    def clear_text(self, by, value):
        """Clear text from a field"""
        element = self.find_element(by, value)
        element.clear()

    def get_text(self, by, value):
        """Get text from a visible element"""
        element = self.find_visible(by, value)
        return element.text

    def get_attribute_value(self, by, value, attribute):
        """Get attribute value from element"""
        element = self.find_element(by, value)
        return element.get_attribute(attribute)

    def is_displayed(self, by, value):
        """Check if element is displayed"""
        try:
            element = self.find_element(by, value)
            return element.is_displayed()
        except Exception:
            return False

    def is_enabled(self, by, value):
        """Check if element is enabled"""
        try:
            element = self.find_element(by, value)
            return element.is_enabled()
        except Exception:
            return False

    def is_selected(self, by, value):
        """Check if element is selected"""
        try:
            element = self.find_element(by, value)
            return element.is_selected()
        except Exception:
            return False

    # ----- Navigation Methods -----
    def open_url(self, url):
        """Open a URL"""
        self.driver.get(url)
        return self

    def get_current_url(self):
        """Get current URL"""
        return self.driver.current_url

    def get_page_title(self):
        """Get page title"""
        return self.driver.title

    def wait_for_url_contains(self, text):
        """Wait until URL contains specified text"""
        return self.wait.until(EC.url_contains(text))

    # ----- Browser Methods -----
    def navigate_back(self):
        """Navigate browser back"""
        self.driver.back()

    def navigate_forward(self):
        """Navigate browser forward"""
        self.driver.forward()

    def refresh_page(self):
        """Refresh the page"""
        self.driver.refresh()

    def maximize_window(self):
        """Maximize the browser window"""
        self.driver.maximize_window()
