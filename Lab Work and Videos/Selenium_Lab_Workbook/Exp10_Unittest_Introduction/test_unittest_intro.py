"""
Experiment 10: Unittest Introduction
Module: Unit Test Frameworks - Unittest
Student: Rishita Paul
Date: September 8, 2026

Covers:
- Unittest Introduction
- First Test Case with Selenium
"""

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class TestSeleniumBasic(unittest.TestCase):
    """First test case using unittest framework"""

    def setUp(self):
        """Run before each test method"""
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()

    def tearDown(self):
        """Run after each test method"""
        self.driver.quit()

    def test_page_title_google(self):
        """Test to verify Google page title"""
        self.driver.get("https://www.google.com")
        self.assertIn("Google", self.driver.title)

    def test_page_url_google(self):
        """Test to verify Google page URL"""
        self.driver.get("https://www.google.com")
        self.assertTrue(self.driver.current_url.startswith("https://"))

    def test_saucedemo_page_title(self):
        """Test to verify SauceDemo page title"""
        self.driver.get("https://www.saucedemo.com/")
        self.assertEqual(self.driver.title, "Swag Labs")

    def test_saucedemo_login_form_exists(self):
        """Test to verify login form elements exist"""
        self.driver.get("https://www.saucedemo.com/")
        username = self.driver.find_element(By.ID, "user-name")
        password = self.driver.find_element(By.ID, "password")
        login_btn = self.driver.find_element(By.ID, "login-button")
        self.assertTrue(username.is_displayed())
        self.assertTrue(password.is_displayed())
        self.assertTrue(login_btn.is_displayed())

    def test_saucedemo_login_success(self):
        """Test successful login on SauceDemo"""
        self.driver.get("https://www.saucedemo.com/")
        self.driver.find_element(By.ID, "user-name").send_keys("standard_user")
        self.driver.find_element(By.ID, "password").send_keys("secret_sauce")
        self.driver.find_element(By.ID, "login-button").click()
        time.sleep(2)
        self.assertIn("/inventory.html", self.driver.current_url)


if __name__ == "__main__":
    unittest.main(verbosity=2)
