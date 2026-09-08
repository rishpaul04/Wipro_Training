"""
login_page.py - LoginPage class for the POM framework
Module: Unit Test Frameworks - Page Object Model
Student: Rishita Paul
Date: September 8, 2026

LoginPage contains only locator definitions and UI methods.
It follows the Page Object Model pattern where:
- Page classes know about HTML elements
- Page classes contain only UI interaction methods
- Test classes contain only test logic
"""

from selenium.webdriver.common.by import By
import time
from .base_page import BasePage


class LoginPage(BasePage):
    """Login page for SauceDemo"""

    # ----- LOCATOR DEFINITIONS -----
    URL = "https://www.saucedemo.com/"
    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message-container")
    LOGIN_LOGO = (By.CLASS_NAME, "login_logo")

    # ----- UI ACTIONS -----
    def open_login_page(self):
        """Navigate to login page"""
        self.open_url(self.URL)
        self.wait_for_login_page_load()
        return self

    def wait_for_login_page_load(self):
        """Wait for login page to be fully loaded"""
        self.find_element(*self.USERNAME_FIELD)
        self.find_element(*self.PASSWORD_FIELD)
        return self

    def enter_username(self, username):
        """Enter username into the username field"""
        self.type_text(*self.USERNAME_FIELD, username)
        return self

    def enter_password(self, password):
        """Enter password into the password field"""
        self.type_text(*self.PASSWORD_FIELD, password)
        return self

    def click_login_button(self):
        """Click the login button"""
        self.click(*self.LOGIN_BUTTON)
        time.sleep(2)
        return self

    def login(self, username, password):
        """Complete login action"""
        self.open_login_page()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        return self

    def login_with_implicit(self, username, password):
        """Complete login without explicit type (chained)"""
        self.enter_username(username) \
            .enter_password(password) \
            .click_login_button()
        return self

    # ----- VERIFICATION METHODS -----
    def is_login_page(self):
        """Check if we're on login page"""
        return self.is_displayed(*self.LOGIN_BUTTON)

    def is_login_successful(self):
        """Check if login was successful"""
        return "/inventory.html" in self.get_current_url()

    def get_error_message(self):
        """Get error message text if present"""
        if self.is_displayed(*self.ERROR_MESSAGE):
            return self.get_text(*self.ERROR_MESSAGE)
        return ""

    def is_valid_username_displayed(self):
        """Check if username field is displayed"""
        return self.is_displayed(*self.USERNAME_FIELD)

    def is_valid_password_displayed(self):
        """Check if password field is displayed"""
        return self.is_displayed(*self.PASSWORD_FIELD)

    def is_login_button_enabled(self):
        """Check if login button is enabled"""
        return self.is_enabled(*self.LOGIN_BUTTON)
