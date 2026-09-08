"""
dashboard_page.py - DashboardPage class for the POM framework
Module: Unit Test Frameworks - Page Object Model
Student: Rishita Paul
Date: September 8, 2026

DashboardPage (Inventory) contains only locator definitions and UI methods.
"""

from selenium.webdriver.common.by import By
import time
from .base_page import BasePage


class DashboardPage(BasePage):
    """Dashboard/Inventory page for SauceDemo"""

    # ----- LOCATOR DEFINITIONS -----
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    INVENTORY_LIST = (By.CLASS_NAME, "inventory_list")
    ADD_TO_CART_BACKPACK = (By.ID, "add-to-cart-sauce-labs-backpack")
    ADD_TO_CART_BIKE_LIGHT = (By.ID, "add-to-cart-sauce-labs-bike-light")
    REMOVE_BACKPACK = (By.ID, "remove-sauce-labs-backpack")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    SHOPPING_CART_TITLE = (By.CLASS_NAME, "title")

    # ----- UI ACTIONS -----
    def is_loaded(self):
        """Check if dashboard is loaded"""
        return "/inventory.html" in self.get_current_url()

    def wait_for_dashboard(self):
        """Wait for dashboard to load"""
        self.wait_for_url_contains("inventory")
        self.find_element(*self.INVENTORY_LIST)
        return self

    def get_item_count(self):
        """Get number of inventory items"""
        return len(self.find_elements(*self.INVENTORY_ITEMS))

    def add_backpack_to_cart(self):
        """Add backpack to cart"""
        self.click(*self.ADD_TO_CART_BACKPACK)
        time.sleep(1)
        return self

    def add_bike_light_to_cart(self):
        """Add bike light to cart"""
        self.click(*self.ADD_TO_CART_BIKE_LIGHT)
        time.sleep(1)
        return self

    def remove_backpack_from_cart(self):
        """Remove backpack from cart"""
        self.click(*self.REMOVE_BACKPACK)
        time.sleep(1)
        return self

    def open_cart(self):
        """Open the shopping cart"""
        self.click(*self.CART_LINK)
        time.sleep(1)
        return self

    # ----- VERIFICATION METHODS -----
    def get_cart_count(self):
        """Get number of items in cart"""
        badges = self.find_elements(*self.CART_BADGE)
        if badges:
            return int(badges[0].text)
        return 0

    def has_items_in_cart(self):
        """Check if cart has items"""
        return self.get_cart_count() > 0

    def is_cart_link_displayed(self):
        """Check if cart link is displayed"""
        return self.is_displayed(*self.CART_LINK)

    def is_on_cart_page(self):
        """Check if we're on cart page"""
        return "/cart.html" in self.get_current_url()

    def get_page_title_text(self):
        """Get the page title text"""
        return self.get_text(*self.SHOPPING_CART_TITLE)
