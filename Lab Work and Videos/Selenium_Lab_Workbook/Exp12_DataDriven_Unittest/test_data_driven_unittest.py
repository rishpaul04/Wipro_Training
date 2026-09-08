"""
Experiment 12: Data-Driven Automation with Unittest (Assignment 8)
Module: Unit Test Frameworks - Unittest
Student: Rishita Paul
Date: September 8, 2026

Assignment 8: Data-Driven Automation (DDT)
Tier: Unittest

Task: Build a login script that reads multiple test cases from an external source
(Excel file via pandas or JSON/CSV file) and asserts proper validation errors.
"""

import unittest
import json
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# ============================================
# TEST DATA (simulating external file read)
# ============================================
def get_test_data_json():
    """Load test data from JSON file"""
    test_data = [
        {"username": "standard_user", "password": "secret_sauce", "expected": "success"},
        {"username": "locked_out_user", "password": "secret_sauce", "expected": "locked_out"},
        {"username": "wrong_user", "password": "wrong_pass", "expected": "error_message"},
        {"username": "", "password": "secret_sauce", "expected": "error_message"},
        {"username": "standard_user", "password": "", "expected": "error_message"},
        {"username": "", "password": "", "expected": "error_message"},
    ]
    return test_data


def get_test_data_csv():
    """Load test data from CSV"""
    test_data = []
    # Create CSV file for demonstration
    with open("login_test_data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "password", "expected"])
        writer.writerow(["standard_user", "secret_sauce", "success"])
        writer.writerow(["locked_out_user", "secret_sauce", "locked_out"])
        writer.writerow(["wrong_user", "wrong_pass", "error_message"])

    with open("login_test_data.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            test_data.append(row)
    return test_data


def get_test_data_excel():
    """Load test data from Excel using openpyxl"""
    from openpyxl import Workbook, load_workbook

    # Create Excel file
    wb = Workbook()
    sheet = wb.active
    sheet.title = "LoginTests"
    sheet.append(["username", "password", "expected"])
    sheet.append(["standard_user", "secret_sauce", "success"])
    sheet.append(["locked_out_user", "secret_sauce", "locked_out"])
    sheet.append(["problem_user", "secret_sauce", "success"])
    wb.save("login_test_data.xlsx")

    # Read back
    test_data = []
    wb = load_workbook("login_test_data.xlsx")
    sheet = wb.active
    headers = [cell.value for cell in sheet[1]]
    for row in sheet.iter_rows(min_row=2, values_only=True):
        test_data.append(dict(zip(headers, row)))
    return test_data


class TestLoginDataDriven(unittest.TestCase):
    """Data-Driven Login Tests using Unittest"""

    def setUp(self):
        """Run before each test - fresh browser for clean state"""
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()
        self.driver.get("https://www.saucedemo.com/")

    def tearDown(self):
        """Run after each test - close browser"""
        self.driver.quit()

    def _do_login(self, username, password):
        """Helper method to perform login with proper waits"""
        wait = WebDriverWait(self.driver, 10)

        # Wait for page to be ready before interacting
        user_field = wait.until(
            EC.presence_of_element_located((By.ID, "user-name"))
        )
        user_field.clear()
        user_field.send_keys(username)

        password_field = self.driver.find_element(By.ID, "password")
        password_field.clear()
        password_field.send_keys(password)

        login_button = wait.until(
            EC.element_to_be_clickable((By.ID, "login-button"))
        )
        login_button.click()

        # Wait for the page to settle (either redirect or error message)
        try:
            wait.until(lambda d: "/inventory.html" in d.current_url or
                       self._get_error_message() != "")
        except Exception:
            pass

    def _get_error_message(self):
        """Helper to get error message text"""
        try:
            error_element = self.driver.find_element(By.CSS_SELECTOR, ".error-message-container")
            return error_element.text if error_element.is_displayed() else ""
        except Exception:
            return ""

    # ---- Test with JSON data ----
    def test_login_json_data(self):
        """Test login using JSON test data"""
        test_cases = get_test_data_json()
        print(f"\nRunning {len(test_cases)} JSON test cases")

        for i, tc in enumerate(test_cases):
            with self.subTest(i=i, username=tc["username"]):
                self.driver.get("https://www.saucedemo.com/")
                self._do_login(tc["username"], tc["password"])

                if tc["expected"] == "success":
                    self.assertIn("/inventory.html", self.driver.current_url,
                                  f"Login should succeed for {tc['username']}")
                elif tc["expected"] == "locked_out":
                    error = self._get_error_message()
                    self.assertTrue(len(error) > 0,
                                    f"Locked out error should appear for {tc['username']}")
                elif tc["expected"] == "error_message":
                    error = self._get_error_message()
                    self.assertTrue(len(error) > 0,
                                    f"Error message should appear for {tc['username']}")

                print(f"  [PASS] {tc['username']} - {tc['expected']}")
                self.driver.get("https://www.saucedemo.com/")

    # ---- Test with CSV data ----
    def test_login_csv_data(self):
        """Test login using CSV test data"""
        test_cases = get_test_data_csv()
        print(f"\nRunning {len(test_cases)} CSV test cases")

        for i, tc in enumerate(test_cases):
            with self.subTest(i=i, username=tc["username"]):
                self.driver.get("https://www.saucedemo.com/")
                self._do_login(tc["username"], tc["password"])

                if tc["expected"] == "success":
                    self.assertIn("/inventory.html", self.driver.current_url,
                                  f"Login should succeed for {tc['username']}")
                elif tc["expected"] == "locked_out":
                    error = self._get_error_message()
                    self.assertTrue(len(error) > 0,
                                    f"Locked out error should appear for {tc['username']}")
                elif tc["expected"] == "error_message":
                    error = self._get_error_message()
                    self.assertTrue(len(error) > 0,
                                    f"Error message should appear for {tc['username']}")

                print(f"  [PASS] {tc['username']} - {tc['expected']}")
                self.driver.get("https://www.saucedemo.com/")

    # ---- Test with Excel data ----
    def test_login_excel_data(self):
        """Test login using Excel test data"""
        test_cases = get_test_data_excel()
        print(f"\nRunning {len(test_cases)} Excel test cases")

        for i, tc in enumerate(test_cases):
            with self.subTest(i=i, username=tc["username"]):
                self.driver.get("https://www.saucedemo.com/")
                self._do_login(tc["username"], tc["password"])

                if tc["expected"] == "success":
                    self.assertIn("/inventory.html", self.driver.current_url,
                                  f"Login should succeed for {tc['username']}")
                elif tc["expected"] == "locked_out":
                    error = self._get_error_message()
                    self.assertTrue(len(error) > 0,
                                    f"Locked out error should appear for {tc['username']}")
                elif tc["expected"] == "error_message":
                    error = self._get_error_message()
                    self.assertTrue(len(error) > 0,
                                    f"Error message should appear for {tc['username']}")

                print(f"  [PASS] {tc['username']} - {tc['expected']}")
                self.driver.get("https://www.saucedemo.com/")

    def cleanup_files(self):
        """Remove generated test data files"""
        for f in ["login_test_data.csv", "login_test_data.xlsx"]:
            if os.path.exists(f):
                os.remove(f)


if __name__ == "__main__":
    unittest.main(verbosity=2)
