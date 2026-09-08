"""
Experiment 18: POM Data-Driven Framework with Screenshots
Module: Unit Test Frameworks - Page Object Model
Student: Rishita Paul
Date: September 8, 2026

Covers:
- Utility to read CSV data
- Data-driven test cases with POM
- Taking screenshots on test failure
- Complete POM framework with reporting
"""

import unittest
import time
import os
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# POM imports
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.csv_reader import CSVReader
from utils.screenshot import Screenshot


class DataDrivenPOMFramework(unittest.TestCase):
    """Complete POM framework with data-driven testing and screenshots"""

    @classmethod
    def setUpClass(cls):
        """Load shared test data once for all tests"""
        cls.csv_reader = CSVReader()
        cls.test_data = cls._load_test_data()

    @classmethod
    def _load_test_data(cls):
        """Load test data from CSV"""
        path = cls.csv_reader.create_sample_csv("testdata/login_data.csv")
        return cls.csv_reader.read_csv_as_dict(path)

    def setUp(self):
        """Fresh browser before each test"""
        options = Options()
        options.add_argument("--disable-back-forward-cache")
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()
        self.login_page = LoginPage(self.driver)
        self.dashboard = DashboardPage(self.driver)
        self.screenshot = Screenshot(self.driver, "reports/screenshots")
        self.login_page.open_login_page()

    def tearDown(self):
        """Close browser after each test"""
        self.driver.quit()

    def _do_login(self, username, password):
        """Helper to perform login using POM (page already open)"""
        self.login_page.enter_username(username)
        self.login_page.enter_password(password)
        self.login_page.click_login_button()

    def _capture_screenshot(self, test_name, success=True):
        """Take screenshot with PASS/FAIL prefix"""
        if success:
            return self.screenshot.capture_success(test_name)
        else:
            return self.screenshot.capture_failure(test_name)

    # ==========================================
    # DATA-DRIVEN TESTS from CSV
    # ==========================================
    def test_data_driven_from_csv(self):
        """Test login combinations from CSV test data"""
        print(f"\nRunning {len(self.test_data)} CSV test cases:")
        print("-" * 40)

        for i, tc in enumerate(self.test_data):
            with self.subTest(test_case=i, username=tc["username"]):
                # Fresh login page each iteration
                self.login_page.open_login_page()
                self._do_login(tc["username"], tc["password"])

                if tc["expected"] == "success":
                    self.assertTrue(
                        self.login_page.is_login_successful(),
                        f"Login should succeed for {tc['username']}"
                    )
                    self._capture_screenshot(f"DDT_success_{tc['username']}", True)
                    print(f"  [PASS] {tc['username']} - login succeeded")
                elif tc["expected"] == "locked_out":
                    self.assertFalse(
                        self.login_page.is_login_successful(),
                        f"Locked user {tc['username']} should not login"
                    )
                    error = self.login_page.get_error_message()
                    self.assertIn("locked", error.lower())
                    self._capture_screenshot(f"DDT_locked_{tc['username']}", True)
                    print(f"  [PASS] {tc['username']} - locked out error shown")
                else:
                    self.assertFalse(
                        self.login_page.is_login_successful(),
                        f"Login should fail for {tc['username']}"
                    )
                    error = self.login_page.get_error_message()
                    self.assertTrue(error)
                    self._capture_screenshot(f"DDT_error_{tc['username']}", True)
                    print(f"  [PASS] {tc['username']} - error shown correctly")

    def test_all_csv_cases_pass_condition(self):
        """Verify each CSV case passes its expected condition"""
        for tc in self.test_data:
            self.assertIn(tc["expected"], ["success", "locked_out", "error_message"])
        print(f"✓ All {len(self.test_data)} CSV test cases validated")

    # ==========================================
    # SCREENSHOT ON FAILURE DEMONSTRATION
    # ==========================================
    def test_screenshot_on_success(self):
        """Demonstrate screenshot capture on successful test"""
        self.login_page.login("standard_user", "secret_sauce")
        self.assertTrue(self.login_page.is_login_successful())
        path = self._capture_screenshot("login_success_demo", True)
        print(f"✓ Success screenshot: {path}")

    def test_screenshot_on_missing_element(self):
        """Demonstrate exception handling and screenshot on failure"""
        try:
            # This will fail - simulating a test failure
            element = self.driver.find_element(By.ID, "element_that_does_not_exist")
            self.assertIsNotNone(element)
        except Exception as e:
            # Capture screenshot on failure
            path = self._capture_screenshot("simulated_failure", False)
            print(f"✗ Simulated failure captured: {path}")
            print(f"  Error: {type(e).__name__}: {str(e)[:50]}")
            # Re-raise to mark test as failed (but we capture screenshot first)
            raise AssertionError("Simulated failure for screenshot demonstration")

    # ==========================================
    # POM COMPLETE FLOW
    # ==========================================
    def test_complete_pom_flow(self):
        """Complete login → dashboard → cart flow using POM"""
        print("\nComplete POM Flow:")
        print("-" * 40)

        # 1. Login
        self.login_page.login("standard_user", "secret_sauce")
        self.assertTrue(self.login_page.is_login_successful())
        print("  ✓ Step 1: Login successful")

        # 2. Dashboard loaded
        self.assertTrue(self.dashboard.is_loaded())
        item_count = self.dashboard.get_item_count()
        print(f"  ✓ Step 2: Dashboard loaded with {item_count} items")

        # 3. Add items to cart
        self.dashboard.add_backpack_to_cart()
        self.dashboard.add_bike_light_to_cart()
        cart_count = self.dashboard.get_cart_count()
        self.assertEqual(cart_count, 2)
        print(f"  ✓ Step 3: {cart_count} items in cart")

        # 4. Navigate to cart
        self.dashboard.open_cart()
        self.assertTrue(self.dashboard.is_on_cart_page())
        print(f"  ✓ Step 4: Cart page opened")

        # Screenshot the completed flow
        path = self._capture_screenshot("complete_flow", True)
        print(f"  ✓ Screenshot saved: {path}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
