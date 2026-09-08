"""
Experiment 1: Introduction to Selenium
Module: Automation with Selenium
Student: Rishita Paul
Date: September 8, 2026
"""

# Import Selenium WebDriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def test_selenium_basic():
    """
    Basic test to demonstrate Selenium WebDriver initialization
    and basic operations.
    """
    print("Selenium Automation Test - Experiment 1")
    print("=" * 50)
    
    # Create Chrome options for headless mode (optional)
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Uncomment for headless mode
    
    # Initialize Chrome WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Navigate to a website
        driver.get("https://www.google.com")
        
        # Get the title of the page
        title = driver.title
        print(f"Page Title: {title}")
        
        # Verify page loaded
        assert "Google" in title, "Google page not loaded"
        print("✓ Page loaded successfully")
        
        # Get current URL
        current_url = driver.current_url
        print(f"Current URL: {current_url}")
        
        # Get page source length
        page_source_length = len(driver.page_source)
        print(f"Page source length: {page_source_length} characters")
        
        # Get window size
        window_size = driver.get_window_size()
        print(f"Window size: {window_size['width']}x{window_size['height']}")
        
        print("=" * 50)
        print("✓ All basic operations completed successfully!")
        
    except Exception as e:
        print(f"✗ An error occurred: {e}")
        
    finally:
        # Close the browser
        driver.quit()
        print("✓ Browser closed successfully")

def test_multiple_browsers():
    """
    Test to demonstrate different browser support
    """
    print("\nTesting Different Browsers")
    print("=" * 50)
    
    # List of browsers to test
    browsers = [
        ("Chrome", webdriver.Chrome),
        ("Firefox", webdriver.Firefox),
        ("Edge", webdriver.Edge)
    ]
    
    for browser_name, webdriver_func in browsers:
        try:
            print(f"\nTesting {browser_name}...")
            driver = webdriver_func()
            driver.get("https://www.google.com")
            print(f"  ✓ {browser_name} - Title: {driver.title}")
            driver.quit()
            print(f"  ✓ {browser_name} - Browser closed")
        except Exception as e:
            print(f"  ✗ {browser_name} - Error: {e}")
    
    print("=" * 50)

if __name__ == "__main__":
    # Run basic test
    test_selenium_basic()
    
    # Uncomment to test multiple browsers
    # test_multiple_browsers()
