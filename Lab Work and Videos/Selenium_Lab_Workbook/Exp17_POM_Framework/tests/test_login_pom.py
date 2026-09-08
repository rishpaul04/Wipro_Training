"""
test_login_pom.py - Test class for Login page using POM
Module: Unit Test Frameworks - Page Object Model
Student: Rishita Paul
Date: September 8, 2026

Test class contains only test logic. Uses LoginPage and DashboardPage
page objects for element interaction.
"""

import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Add parent directory to path so we can import pages/utils
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.screenshot import Screenshot


class TestLoginPagePOM(unittest.TestCase):
    """Tests for LoginPage using Page Object Model"""

    def setUp(self):
        """Fresh browser before each test"""
        options = Options()
        options.add_argument("--disable-back-forward-cache")
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()
        self.login_page = LoginPage(self.driver)
        self.dashboard = DashboardPage(self.driver)
        self.screenshot = Screenshot(self.driver)
        self.login_page.open_login_page()

    def tearDown(self):
        """Close browser after each test"""
        self.driver.quit()

    def test_login_page_loads(self):
        """Test login page loads correctly"""
        self.assertTrue(self.login_page.is_login_page())
        self.assertTrue(self.login_page.is_valid_username_displayed())
        self.assertTrue(self.login_page.is_valid_password_displayed())
        self.assertTrue(self.login_page.is_login_button_enabled())
        print("✓ Login page loaded successfully")

    def test_login_with_valid_credentials(self):
        """Test login with valid credentials"""
        self.login_page.login("standard_user", "secret_sauce")
        self.assertTrue(self.login_page.is_login_successful())
        self.assertTrue(self.dashboard.is_loaded())
        print("✓ Valid login successful")

    def test_login_with_invalid_credentials(self):
        """Test login with invalid credentials shows error"""
        self.login_page.login("wrong_user", "wrong_password")
        self.assertFalse(self.login_page.is_login_successful())
        error = self.login_page.get_error_message()
        self.assertTrue(error)
        self.assertIn("Username and password do not match", error)
        print(f"✓ Error message shown: {error[:50]}")

    def test_login_with_locked_user(self):
        """Test login with locked out user"""
        self.login_page.login("locked_out_user", "secret_sauce")
        self.assertFalse(self.login_page.is_login_successful())
        error = self.login_page.get_error_message()
        self.assertTrue(error)
        self.assertIn("locked", error.lower())
        print(f"✓ Locked user error: {error[:50]}")

    def test_login_with_empty_fields(self):
        """Test login with empty fields"""
        self.login_page.click_login_button()
        self.assertFalse(self.login_page.is_login_successful())
        error = self.login_page.get_error_message()
        self.assertTrue(error)
        print(f"✓ Empty fields error: {error[:50]}")

    def test_login_redirects_to_inventory(self):
        """Test login redirects to inventory page"""
        self.login_page.login("standard_user", "secret_sauce")
        url = self.dashboard.get_current_url()
        self.assertIn("/inventory.html", url)
        self.screenshot.capture_full_page("login_success")
        print(f"✓ Redirected to: {url}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
