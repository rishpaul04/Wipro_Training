"""
Experiment 11: Unittest SetUp/TearDown, Assert Methods, Test Suite
Module: Unit Test Frameworks - Unittest
Student: Rishita Paul
Date: September 8, 2026

Covers:
- Class Level SetUp and TearDown
- All Assert Methods
- Creating and running Test Suites
"""

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os


class TestAssertMethods(unittest.TestCase):
    """Demonstrate all unittest assert methods"""

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()
        self.driver.get("https://www.saucedemo.com/")

    def tearDown(self):
        self.driver.quit()

    def test_assertEqual(self):
        """assertEqual - checks if two values are equal"""
        self.assertEqual(self.driver.title, "Swag Labs")
        self.assertEqual(self.driver.current_url, "https://www.saucedemo.com/")
        print("  assertEqual: Title matches expected value")

    def test_assertNotEqual(self):
        """assertNotEqual - checks if two values are NOT equal"""
        self.assertNotEqual(self.driver.title, "Google")
        self.assertNotEqual(self.driver.current_url, "https://www.google.com/")
        print("  assertNotEqual: Title differs from Google")

    def test_assertTrue(self):
        """assertTrue - checks if condition is True"""
        username = self.driver.find_element(By.ID, "user-name")
        self.assertTrue(username.is_displayed())
        self.assertTrue(username.is_enabled())
        print("  assertTrue: Element is displayed and enabled")

    def test_assertFalse(self):
        """assertFalse - checks if condition is False"""
        self.driver.find_element(By.ID, "user-name").send_keys("test")
        # Error text should NOT be present before clicking login
        element = self.driver.find_element(By.CSS_SELECTOR, ".error-message-container")
        self.assertFalse("Username and password do not match" in element.text)
        print("  assertFalse: No error message text before login attempt")

    def test_assertIn(self):
        """assertIn - checks if value is in collection"""
        self.assertIn("saucedemo", self.driver.current_url)
        self.assertIn("Swag Labs", self.driver.title)
        print("  assertIn: URL contains expected string")

    def test_assertIsNotNone(self):
        """assertIsNotNone - checks if value is not None"""
        element = self.driver.find_element(By.ID, "user-name")
        self.assertIsNotNone(element)
        self.assertIsNotNone(element.get_attribute("id"))
        self.assertIsNotNone(element.get_attribute("type"))
        print("  assertIsNotNone: Element and attributes are not None")

    def test_assertRaises(self):
        """assertRaises - checks if exception is raised"""
        with self.assertRaises(Exception):
            self.driver.find_element(By.ID, "non_existent_element_xyz")
        print("  assertRaises: NoSuchElementException raised as expected")


class TestLoginValidation(unittest.TestCase):
    """Test login validations using assert methods"""

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()

    def tearDown(self):
        self.driver.quit()

    def test_valid_login(self):
        """Test valid credentials"""
        self.driver.get("https://www.saucedemo.com/")
        self.driver.find_element(By.ID, "user-name").send_keys("standard_user")
        self.driver.find_element(By.ID, "password").send_keys("secret_sauce")
        self.driver.find_element(By.ID, "login-button").click()
        time.sleep(2)
        self.assertIn("/inventory.html", self.driver.current_url)

    def test_invalid_credentials_show_error(self):
        """Test invalid credentials show error"""
        self.driver.get("https://www.saucedemo.com/")
        self.driver.find_element(By.ID, "user-name").send_keys("wrong_user")
        self.driver.find_element(By.ID, "password").send_keys("wrong_pass")
        self.driver.find_element(By.ID, "login-button").click()
        time.sleep(1)
        error = self.driver.find_element(By.CSS_SELECTOR, ".error-message-container")
        self.assertTrue(error.is_displayed())
        self.assertIn("Username and password do not match", error.text)

    def test_empty_credentials_show_error(self):
        """Test empty credentials show error"""
        self.driver.get("https://www.saucedemo.com/")
        self.driver.find_element(By.ID, "login-button").click()
        time.sleep(1)
        error = self.driver.find_element(By.CSS_SELECTOR, ".error-message-container")
        self.assertTrue(error.is_displayed())


def create_test_suite():
    """Create a custom test suite"""
    suite = unittest.TestSuite()

    # Add specific tests
    suite.addTest(TestAssertMethods("test_assertEqual"))
    suite.addTest(TestAssertMethods("test_assertNotEqual"))
    suite.addTest(TestAssertMethods("test_assertTrue"))
    suite.addTest(TestAssertMethods("test_assertFalse"))
    suite.addTest(TestAssertMethods("test_assertIn"))
    suite.addTest(TestAssertMethods("test_assertIsNotNone"))
    suite.addTest(TestAssertMethods("test_assertRaises"))
    suite.addTest(TestLoginValidation("test_valid_login"))
    suite.addTest(TestLoginValidation("test_invalid_credentials_show_error"))

    return suite


def create_all_tests_suite():
    """Create suite with ALL tests using loadTestsFromTestCase"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestAssertMethods))
    suite.addTests(loader.loadTestsFromTestCase(TestLoginValidation))

    return suite


if __name__ == "__main__":
    print("=" * 60)
    print("Running Custom Test Suite")
    print("=" * 60)
    runner = unittest.TextTestRunner(verbosity=2)
    suite = create_test_suite()
    runner.run(suite)

    print("\n" + "=" * 60)
    print("Running ALL Tests via TestSuite")
    print("=" * 60)
    runner = unittest.TextTestRunner(verbosity=2)
    all_suite = create_all_tests_suite()
    runner.run(all_suite)
