"""
screenshot.py - Screenshot utility for the POM framework
Module: Unit Test Frameworks - Page Object Model
Student: Rishita Paul
Date: September 8, 2026

Provides screenshot capture methods - full page and element level.
"""

import os
from datetime import datetime


class Screenshot:
    """Screenshot utility class"""

    def __init__(self, driver, default_dir="reports/screenshots"):
        """Initialize with driver and output directory"""
        self.driver = driver
        self.default_dir = default_dir
        self._ensure_directory()

    def _ensure_directory(self):
        """Create screenshot directory if not exists"""
        os.makedirs(self.default_dir, exist_ok=True)

    def _generate_filename(self, name, prefix=""):
        """Generate a timestamp-based filename"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = name.replace(" ", "_").replace("/", "_")
        return f"{prefix}{safe_name}_{timestamp}.png"

    def capture_full_page(self, name="screenshot"):
        """Capture full page screenshot"""
        filename = self._generate_filename(name)
        filepath = os.path.join(self.default_dir, filename)
        self.driver.save_screenshot(filepath)
        return filepath

    def capture_element(self, element, name="element"):
        """Capture element-level screenshot"""
        filename = self._generate_filename(name, prefix="element_")
        filepath = os.path.join(self.default_dir, filename)
        element.screenshot(filepath)
        return filepath

    def capture_failure(self, test_name):
        """Capture screenshot on test failure"""
        return self.capture_full_page(f"FAIL_{test_name}")

    def capture_success(self, test_name):
        """Capture screenshot on test success"""
        return self.capture_full_page(f"PASS_{test_name}")


if __name__ == "__main__":
    from selenium import webdriver
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com/")
    screenshot = Screenshot(driver, "reports/screenshots")
    path = screenshot.capture_full_page("test_demo")
    print(f"✓ Screenshot captured: {path}")
    driver.quit()
