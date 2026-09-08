"""
test_dashboard_pom.py - Test class for Dashboard page using POM
Module: Unit Test Frameworks - Page Object Model
Student: Rishita Paul
Date: September 8, 2026
"""

import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


class TestDashboardPagePOM(unittest.TestCase):
    """Tests for Dashboard page using Page Object Model"""

    def setUp(self):
        """Fresh browser and login before each test"""
        options = Options()
        options.add_argument("--disable-back-forward-cache")
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()
        self.login_page = LoginPage(self.driver)
        self.dashboard = DashboardPage(self.driver)
        self.login_page.login("standard_user", "secret_sauce")

    def tearDown(self):
        """Close browser after each test"""
        self.driver.quit()

    def test_dashboard_loads(self):
        """Test dashboard loads after login"""
        self.assertTrue(self.dashboard.is_loaded())
        self.assertTrue(self.dashboard.is_cart_link_displayed())
        self.assertGreater(self.dashboard.get_item_count(), 0)
        print(f"✓ Dashboard loaded with {self.dashboard.get_item_count()} items")

    def test_add_and_remove_item(self):
        """Test add item to cart and remove it"""
        # Initially cart is empty
        self.assertEqual(self.dashboard.get_cart_count(), 0)

        # Add item to cart
        self.dashboard.add_backpack_to_cart()
        self.assertEqual(self.dashboard.get_cart_count(), 1)
        print(f"✓ Item added, cart count: {self.dashboard.get_cart_count()}")

        # Remove item from cart
        self.dashboard.remove_backpack_from_cart()
        self.assertEqual(self.dashboard.get_cart_count(), 0)
        print(f"✓ Item removed, cart count: {self.dashboard.get_cart_count()}")

    def test_open_cart(self):
        """Test opening the shopping cart"""
        self.dashboard.add_backpack_to_cart()
        self.dashboard.open_cart()
        self.assertTrue(self.dashboard.is_on_cart_page())
        print(f"✓ Cart page opened: {self.dashboard.get_current_url()}")

    def test_add_multiple_items(self):
        """Test adding multiple items to cart"""
        self.dashboard.add_backpack_to_cart()
        self.dashboard.add_bike_light_to_cart()
        self.assertEqual(self.dashboard.get_cart_count(), 2)
        print(f"✓ Two items in cart: {self.dashboard.get_cart_count()}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
