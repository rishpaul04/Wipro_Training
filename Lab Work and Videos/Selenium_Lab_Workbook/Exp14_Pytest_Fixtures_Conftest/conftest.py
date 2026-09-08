"""
conftest.py - Shared PyTest Fixtures
Module: Unit Test Frameworks - PyTest
Student: Rishita Paul
Date: September 8, 2026

Covers:
- Fixtures for driver initialization and teardown
- Shared fixtures across multiple test files
- conftest.py for project-level fixtures
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


# ============================================
# FIXTURES - Reusable setup/teardown functions
# ============================================

@pytest.fixture(scope="function")
def driver():
    """Fixture: Create and destroy driver for each test function"""
    print("\n  [fixture] Opening browser...")
    _driver = webdriver.Chrome()
    _driver.implicitly_wait(5)
    _driver.maximize_window()
    yield _driver
    print("  [fixture] Closing browser...")
    _driver.quit()


@pytest.fixture(scope="class")
def class_driver():
    """Fixture: Create and destroy driver once per test class"""
    print("\n  [class fixture] Opening browser...")
    _driver = webdriver.Chrome()
    _driver.implicitly_wait(5)
    _driver.maximize_window()
    yield _driver
    print("  [class fixture] Closing browser...")
    _driver.quit()


@pytest.fixture(scope="function")
def sauce_demo_driver(driver):
    """Fixture: Pre-navigate to SauceDemo login page"""
    driver.get("https://www.saucedemo.com/")
    time.sleep(1)
    return driver


@pytest.fixture(scope="function")
def logged_in_driver(driver):
    """Fixture: Pre-logged in driver"""
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)
    return driver


@pytest.fixture(scope="session")
def test_data():
    """Fixture: Provide test data"""
    return {
        "valid_user": {"username": "standard_user", "password": "secret_sauce"},
        "locked_user": {"username": "locked_out_user", "password": "secret_sauce"},
        "problem_user": {"username": "problem_user", "password": "secret_sauce"},
    }
