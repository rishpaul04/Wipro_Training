"""
Experiment 13: PyTest Introduction and Installation
Module: Unit Test Frameworks - PyTest
Student: Rishita Paul
Date: September 8, 2026

Covers:
- Introduction to PyTest
- Installing PyTest
- Naming Conventions
- Test Files, Test Methods, Assertions
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


# ============================================
# PYTEST NAMING CONVENTIONS:
# - Test files: test_*.py
# - Test functions: test_*()
# - Test classes: Test*
# - Test methods: test_*()
# - Assertions: assert statement (no self.assert*)
# ============================================


def test_page_title_google():
    """Test Google page title - no class needed"""
    driver = webdriver.Chrome()
    try:
        driver.get("https://www.google.com")
        assert "Google" in driver.title
        assert driver.current_url.startswith("https://")
    finally:
        driver.quit()


def test_page_url_google():
    """Test Google page URL"""
    driver = webdriver.Chrome()
    try:
        driver.get("https://www.google.com")
        assert "google" in driver.current_url.lower()
    finally:
        driver.quit()


class TestSauceDemoPytest:
    """Test class for SauceDemo using PyTest"""

    def test_saucedemo_page_title(self):
        """Test SauceDemo page title"""
        driver = webdriver.Chrome()
        driver.implicitly_wait(5)
        try:
            driver.get("https://www.saucedemo.com/")
            assert driver.title == "Swag Labs"
        finally:
            driver.quit()

    def test_saucedemo_login_form_exists(self):
        """Test login form elements exist"""
        driver = webdriver.Chrome()
        driver.implicitly_wait(5)
        try:
            driver.get("https://www.saucedemo.com/")
            assert driver.find_element(By.ID, "user-name").is_displayed()
            assert driver.find_element(By.ID, "password").is_displayed()
            assert driver.find_element(By.ID, "login-button").is_displayed()
        finally:
            driver.quit()

    def test_saucedemo_login_success(self):
        """Test successful login"""
        driver = webdriver.Chrome()
        driver.implicitly_wait(5)
        try:
            driver.get("https://www.saucedemo.com/")
            driver.find_element(By.ID, "user-name").send_keys("standard_user")
            driver.find_element(By.ID, "password").send_keys("secret_sauce")
            driver.find_element(By.ID, "login-button").click()
            time.sleep(2)
            assert "/inventory.html" in driver.current_url
        finally:
            driver.quit()

    def test_saucedemo_login_page_elements_count(self):
        """Test number of inputs on login page"""
        driver = webdriver.Chrome()
        driver.implicitly_wait(5)
        try:
            driver.get("https://www.saucedemo.com/")
            inputs = driver.find_elements(By.TAG_NAME, "input")
            assert len(inputs) >= 3
        finally:
            driver.quit()


class TestBingPytest:
    """Additional test class for variety"""

    def test_bing_title(self):
        """Test Bing page title"""
        driver = webdriver.Chrome()
        try:
            driver.get("https://www.bing.com")
            assert "Bing" in driver.title
        finally:
            driver.quit()

    def test_bing_url(self):
        """Test Bing URL"""
        driver = webdriver.Chrome()
        try:
            driver.get("https://www.bing.com")
            assert "bing" in driver.current_url.lower()
        finally:
            driver.quit()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
