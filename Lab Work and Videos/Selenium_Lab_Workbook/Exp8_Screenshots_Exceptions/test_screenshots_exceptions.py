"""
Experiment 8: Take Screenshots & Exception Handling
Module: Automation with Selenium
Student: Rishita Paul
Date: September 8, 2026
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementNotInteractableException,
    WebDriverException
)
import os
import time
from datetime import datetime

# ============================================
# GENERIC SCREENSHOT METHOD
# ============================================
def take_screenshot(driver, name):
    """
    Generic method to take a screenshot.
    
    Args:
        driver: WebDriver instance
        name: Name/description of the screenshot
    Returns:
        str: Path to the saved screenshot file
    """
    screenshot_dir = "screenshots"
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(screenshot_dir, f"{name}_{timestamp}.png")
    
    driver.save_screenshot(filename)
    print(f"✓ Screenshot saved: {filename}")
    return filename

# ============================================
# ELEMENT SCREENSHOT
# ============================================
def take_element_screenshot(element, name):
    """
    Take a screenshot of a specific element.
    
    Args:
        element: WebElement to capture
        name: Name/description
    Returns:
        str: Path to the saved screenshot
    """
    screenshot_dir = "screenshots"
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(screenshot_dir, f"element_{name}_{timestamp}.png")
    
    element.screenshot(filename)
    print(f"✓ Element screenshot saved: {filename}")
    return filename

# ============================================
# GENERIC ELEMENT METHOD WITH EXCEPTION HANDLING
# ============================================
def find_element_safe(driver, by, value, screenshot_name=None):
    """
    Generic method with built-in exception handling.
    
    Args:
        driver: WebDriver instance
        by: Locator strategy (By.ID, By.NAME, etc.)
        value: Locator value
        screenshot_name: Optional screenshot on failure
    Returns:
        WebElement or None
    """
    try:
        element = driver.find_element(by, value)
        print(f"✓ Found element: {value}")
        return element
    except NoSuchElementException:
        print(f"✗ Element not found: {value}")
        if screenshot_name:
            take_screenshot(driver, f"notfound_{screenshot_name}")
        return None
    except Exception as e:
        print(f"✗ Unexpected error finding {value}: {type(e).__name__}")
        if screenshot_name:
            take_screenshot(driver, f"error_{screenshot_name}")
        return None

# ============================================
# TEST 1: BASIC EXCEPTION HANDLING
# ============================================
def test_basic_exception_handling():
    """Test basic try-except-finally"""
    print("Test 1: Basic Exception Handling")
    print("=" * 50)
    
    driver = webdriver.Chrome()
    try:
        driver.get("https://www.saucedemo.com/")
        print("✓ Page loaded")
        
        # Try to find a non-existent element
        try:
            element = driver.find_element(By.ID, "non_existent_element")
            print(f"✓ Element found: {element}")
        except NoSuchElementException as e:
            print("✗ NoSuchElementException caught: Element not found")
            print(f"  Exception type: {type(e).__name__}")
        
        take_screenshot(driver, "basic_error_demo")
        
    except Exception as e:
        print(f"✗ Outer exception caught: {type(e).__name__}")
    finally:
        driver.quit()
        print("✓ Finally block: Browser closed")

# ============================================
# TEST 2: GENERIC METHODS
# ============================================
def test_generic_methods():
    """Test generic reusable methods"""
    print("\nTest 2: Generic Methods with Exception Handling")
    print("=" * 50)
    
    driver = webdriver.Chrome()
    
    try:
        driver.get("https://www.saucedemo.com/")
        print("✓ Navigated to SauceDemo")
        take_screenshot(driver, "login_page")
        
        # Use generic method to find elements
        username = find_element_safe(driver, By.ID, "user-name", "username")
        password = find_element_safe(driver, By.NAME, "password", "password")
        login_btn = find_element_safe(driver, By.ID, "login-button", "login")
        
        # Try to find non-existent element (will trigger screenshot)
        missing = find_element_safe(driver, By.ID, "not_here", "missing")
        
        print(f"\nResults:")
        print(f"  username found: {username is not None}")
        print(f"  password found: {password is not None}")
        print(f"  login_btn found: {login_btn is not None}")
        print(f"  missing found: {missing is not None}")
        
        # Perform login if elements found
        if username and password and login_btn:
            username.send_keys("standard_user")
            password.send_keys("secret_sauce")
            login_btn.click()
            time.sleep(2)
            take_screenshot(driver, "after_successful_login")
            print(f"\n✓ Login completed, URL: {driver.current_url}")
        
    except WebDriverException as e:
        print(f"✗ WebDriver exception: {e}")
        take_screenshot(driver, "webdriver_error")
    finally:
        driver.quit()
        print("✓ Browser closed")

# ============================================
# TEST 3: COMPREHENSIVE EXCEPTION DEMO
# ============================================
def test_comprehensive_exception_handling():
    """Test comprehensive exception handling"""
    print("\nTest 3: Comprehensive Exception Handling")
    print("=" * 50)
    
    driver = webdriver.Chrome()
    
    try:
        driver.get("https://www.saucedemo.com/")
        print("✓ Page loaded")
        
        # Demonstrate NoSuchElementException
        print("\n  --- NoSuchElementException ---")
        try:
            driver.find_element(By.ID, "fake_element")
        except NoSuchElementException:
            print("  ✓ Caught: NoSuchElementException")
            take_screenshot(driver, "no_such_element")
        
        # Demonstrate TimeoutException
        print("\n  --- TimeoutException ---")
        try:
            WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "loading"))
            )
        except TimeoutException:
            print("  ✓ Caught: TimeoutException (3s wait expired)")
            take_screenshot(driver, "timeout")
        
        # Demonstrate successful operation
        print("\n  --- Successful Operation ---")
        username = driver.find_element(By.ID, "user-name")
        print(f"  ✓ Successful: Found {username.tag_name} element")
        
        # Check element state
        print("\n  --- Element State Checks ---")
        print(f"  is_displayed: {username.is_displayed()}")
        print(f"  is_enabled: {username.is_enabled()}")
        
        take_screenshot(driver, "exception_demo_complete")
        
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        take_screenshot(driver, "outer_error")
    finally:
        driver.quit()
        print("✓ Finally block: Browser closed regardless of outcome")

# ============================================
# TEST 4: LOGIN FLOW WITH SCREENSHOTS
# ============================================
def test_login_flow_with_screenshots():
    """Complete login flow with screenshots at each step"""
    print("\nTest 4: Login Flow with Screenshots & Error Handling")
    print("=" * 50)
    
    driver = webdriver.Chrome()
    driver.maximize_window()
    
    try:
        # Step 1: Navigate
        driver.get("https://www.saucedemo.com/")
        take_screenshot(driver, "01_login_page")
        print("✓ Navigated to login page")
        
        # Step 2: Enter credentials
        username = find_element_safe(driver, By.ID, "user-name")
        if username:
            username.send_keys("standard_user")
            take_screenshot(driver, "02_username_entered")
            
            password = find_element_safe(driver, By.ID, "password")
            password.send_keys("secret_sauce")
            take_screenshot(driver, "03_password_entered")
        
        # Step 3: Login
        login = find_element_safe(driver, By.ID, "login-button")
        if login:
            login.click()
            print("✓ Login button clicked")
            time.sleep(2)
            take_screenshot(driver, "04_after_login")
        
        # Step 4: Verify
        if "/inventory.html" in driver.current_url:
            print("✓ Login successful!")
        else:
            print("✗ Login failed - unexpected URL")
            take_screenshot(driver, "login_failed")
        
        # Step 5: Add to cart (element-level screenshot)
        try:
            add_btn = driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
            take_element_screenshot(add_btn, "add_to_cart_button")
            add_btn.click()
            print("✓ Item added to cart")
        except NoSuchElementException:
            print("✗ Add to cart button not found")
        except Exception as e:
            print(f"✗ Element screenshot error: {e}")
        
        # Step 6: Go to cart
        try:
            cart = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
            cart.click()
            time.sleep(1)
            take_screenshot(driver, "05_cart_page")
            print("✓ Navigated to cart")
        except NoSuchElementException:
            print("✗ Cart link not found")
            take_screenshot(driver, "cart_not_found")
        
        print("\n✓ Complete login flow with screenshots completed!")
        
    except Exception as e:
        print(f"✗ Test failed: {type(e).__name__}: {e}")
        take_screenshot(driver, "test_failure")
    finally:
        driver.quit()
        print("✓ Finally: Browser closed")

if __name__ == "__main__":
    print("=" * 60)
    print("EXPERIMENT 8: SCREENSHOTS & EXCEPTION HANDLING")
    print("=" * 60)
    
    test_basic_exception_handling()
    test_generic_methods()
    test_comprehensive_exception_handling()
    test_login_flow_with_screenshots()
    
    print("\n" + "=" * 60)
    print("✓ All screenshot and exception experiments completed!")
    print("  Screenshots are saved in the 'screenshots' folder")
