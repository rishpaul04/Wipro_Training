"""
Experiment 14: PyTest Fixtures and conftest.py
Module: Unit Test Frameworks - PyTest
Student: Rishita Paul
Date: September 8, 2026

Covers:
- PyTest fixtures with different scopes
- conftest.py for shared fixtures
- Fixtures for driver initialization and teardown
- Subtests and parameterized tests
"""

import pytest
from selenium.webdriver.common.by import By
import time


# ============================================
# Tests using function-scoped driver fixture
# ============================================

class TestLoginWithFixtures:
    """Tests using driver fixture from conftest.py"""

    def test_page_title(self, driver):
        """Each test gets its own browser instance"""
        driver.get("https://www.saucedemo.com/")
        assert driver.title == "Swag Labs"
        print(f"  [test] Title: {driver.title}")

    def test_login_form_elements(self, sauce_demo_driver):
        """Using pre-navigated SauceDemo fixture"""
        assert sauce_demo_driver.find_element(By.ID, "user-name").is_displayed()
        assert sauce_demo_driver.find_element(By.ID, "password").is_displayed()
        assert sauce_demo_driver.find_element(By.ID, "login-button").is_displayed()
        print("  [test] All login form elements displayed")

    def test_valid_login(self, sauce_demo_driver):
        """Test valid login with fixture"""
        sauce_demo_driver.find_element(By.ID, "user-name").send_keys("standard_user")
        sauce_demo_driver.find_element(By.ID, "password").send_keys("secret_sauce")
        sauce_demo_driver.find_element(By.ID, "login-button").click()
        time.sleep(2)
        assert "/inventory.html" in sauce_demo_driver.current_url
        print(f"  [test] URL after login: {sauce_demo_driver.current_url}")

    def test_invalid_login(self, sauce_demo_driver):
        """Test invalid login with fixture"""
        sauce_demo_driver.find_element(By.ID, "user-name").send_keys("wrong_user")
        sauce_demo_driver.find_element(By.ID, "password").send_keys("wrong_pass")
        sauce_demo_driver.find_element(By.ID, "login-button").click()
        time.sleep(1)
        error = sauce_demo_driver.find_element(By.CSS_SELECTOR, ".error-message-container")
        assert error.is_displayed()
        print(f"  [test] Error message: {error.text}")


class TestInventoryWithFixtures:
    """Tests using logged_in_driver fixture"""

    def test_inventory_page_title(self, logged_in_driver):
        """Verify inventory page title after login"""
        assert "/inventory.html" in logged_in_driver.current_url
        print(f"  [test] On inventory page: {logged_in_driver.current_url}")

    def test_inventory_items_count(self, logged_in_driver):
        """Count items on inventory page"""
        items = logged_in_driver.find_elements(By.CLASS_NAME, "inventory_item")
        assert len(items) > 0
        print(f"  [test] Found {len(items)} items")

    def test_add_to_cart(self, logged_in_driver):
        """Test adding item to cart"""
        add_btn = logged_in_driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
        add_btn.click()
        time.sleep(1)
        badge = logged_in_driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        assert badge.text == "1"
        print(f"  [test] Cart badge: {badge.text}")


class TestDataDrivenWithFixtures:
    """Data-driven tests using test_data fixture"""

    def test_data_driven_login(self, driver, test_data):
        """Test multiple login scenarios with fixture data"""
        for name, credentials in test_data.items():
            driver.get("https://www.saucedemo.com/")
            driver.find_element(By.ID, "user-name").send_keys(credentials["username"])
            driver.find_element(By.ID, "password").send_keys(credentials["password"])
            driver.find_element(By.ID, "login-button").click()
            time.sleep(2)

            if credentials["username"] == "standard_user" or credentials["username"] == "problem_user":
                assert "/inventory.html" in driver.current_url, f"{name} login should succeed"
                print(f"  [{name}] Login succeeded")
            else:
                error = driver.find_element(By.CSS_SELECTOR, ".error-message-container")
                assert error.is_displayed(), f"{name} should show error"
                print(f"  [{name}] Error displayed as expected")

            driver.get("https://www.saucedemo.com/")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
