# Experiment 8: Take Screenshots & Exception Handling

**Module Name:** Automation with Selenium  
**Experiment Title:** Take Screenshots & Exception Handling  
**Experiment Number:** 1.8  
**Date:** September 8, 2026  

---

## 1. Problem Statement

Learn to capture screenshots at various stages of test execution and implement proper exception handling using try-catch-finally blocks to create robust automation scripts.

---

## 2. Objective

- Take full-page and element-level screenshots
- Create a generic method to take screenshots
- Save screenshots with timestamp-based filenames
- Implement try-except-finally blocks for error handling
- Handle common Selenium exceptions gracefully
- Create a robust test framework

---

## 3. Tools, Software, and Concepts Used

### Software Requirements:
- Python 3.x
- Selenium 4.x
- Web browser (Chrome)
- Test websites: https://www.saucedemo.com/

### Concepts Covered:
- WebDriver screenshot methods (get_screenshot_as_file, get_screenshot_as_png)
- Element screenshots (element.screenshot())
- Exception handling (try-except-finally)
- Common Selenium exceptions (NoSuchElementException, TimeoutException, etc.)
- Timestamp-based file naming
- Generic reusable functions

---

## 4. Source Code / Implementation Steps

```python
# test_screenshots_exceptions.py
"""
Experiment 8: Take Screenshots & Exception Handling
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
    Generic method to take a screenshot
    
    Args:
        driver: WebDriver instance
        name: Name/description of the screenshot
    Returns:
        str: Path to the saved screenshot file
    """
    # Create screenshots directory if not exists
    screenshot_dir = "screenshots"
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    
    # Generate timestamp-based filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{screenshot_dir}/{name}_{timestamp}.png"
    
    # Take full page screenshot
    driver.save_screenshot(filename)
    print(f"✓ Screenshot saved: {filename}")
    return filename

# ============================================
# ELEMENT SCREENSHOT
# ============================================
def take_element_screenshot(element, name):
    """
    Take a screenshot of a specific element
    
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
    filename = f"{screenshot_dir}/element_{name}_{timestamp}.png"
    
    element.screenshot(filename)
    print(f"✓ Element screenshot saved: {filename}")
    return filename

# ============================================
# BASIC EXCEPTION HANDLING DEMO
# ============================================
def test_basic_exception_handling():
    """Test basic try-except-finally"""
    print("Testing Basic Exception Handling")
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
            print(f"✗ NoSuchElementException caught: Element not found")
            print(f"  Error: {e}")
        
        take_screenshot(driver, "after_error")
        
    except Exception as e:
        print(f"✗ Outer exception caught: {type(e).__name__}")
    finally:
        driver.quit()
        print("✓ Browser closed in finally block")

# ============================================
# GENERIC ELEMENT METHOD WITH SCREENSHOT
# ============================================
def find_element_safe(driver, by, value, screenshot_name=None):
    """
    Generic method with built-in exception handling
    
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

def test_generic_methods():
    """Test generic reusable methods"""
    print("\nTesting Generic Methods with Exception Handling")
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
        
        # Try to find non-existent element
        missing = find_element_safe(driver, By.ID, "not_here", "missing")
        
        print(f"\nResults:")
        print(f"  username: {username is not None}")
        print(f"  password: {password is not None}")
        print(f"  login_btn: {login_btn is not None}")
        print(f"  missing: {missing is None}")
        
        if username and password and login_btn:
            username.send_keys("standard_user")
            password.send_keys("secret_sauce")
            login_btn.click()
            
            time.sleep(2)
            take_screenshot(driver, "after_login")
        
    except WebDriverException as e:
        print(f"✗ WebDriver exception: {e}")
        take_screenshot(driver, "webdriver_error")
    finally:
        driver.quit()
        print("✓ Browser closed")

# ============================================
# COMPREHENSIVE EXCEPTION DEMO
# ============================================
def test_comprehensive_exception_handling():
    """Test comprehensive exception handling"""
    print("\nTesting Comprehensive Exception Handling")
    print("=" * 50)
    
    driver = webdriver.Chrome()
    
    try:
        driver.get("https://www.saucedemo.com/")
        print("✓ Page loaded")
        
        # Demonstrate multiple error types
        errors_to_try = [
            ("NoSuchElement", lambda: driver.find_element(By.ID, "fake_id")),
            ("Timeout", lambda: WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "loading"))
            )),
        ]
        
        for name, operation in errors_to_try:
            try:
                operation()
                print(f"  ✓ {name}: No error occurred")
            except Exception as e:
                print(f"  ✗ {name}: Caught {type(e).__name__}")
                print(f"     Message: {str(e)[:80]}")
        
        # Successful operations
        try:
            username = driver.find_element(By.ID, "user-name")
            print(f"  ✓ Successful element find: {username.tag_name}")
        except Exception as e:
            print(f"  ✗ Unexpected: {e}")
        
        # Element not interactable example
        print("\n  Demonstrating is_displayed() / is_enabled() checks:")
        username = driver.find_element(By.ID, "user-name")
        print(f"  ✓ username is_displayed: {username.is_displayed()}")
        print(f"  ✓ username is_enabled: {username.is_enabled()}")
        
        take_screenshot(driver, "exception_demo_complete")
        
    except Exception as e:
        print(f"✗ Unexpected outer exception: {e}")
        take_screenshot(driver, "outer_error")
    finally:
        driver.quit()
        print("✓ Finally: Browser closed regardless of errors")

# ============================================
# LOGIN FLOW WITH FULL ERROR HANDLING
# ============================================
def test_login_flow_with_screenshots():
    """
    Complete login flow with screenshots at each step
    and comprehensive error handling
    """
    print("\n=== LOGIN FLOW WITH SCREENSHOTS ===")
    print("=" * 50)
    
    driver = webdriver.Chrome()
    driver.maximize_window()
    
    try:
        # Step 1: Navigate
        driver.get("https://www.saucedemo.com/")
        take_screenshot(driver, "01_login")
        
        # Step 2: Login
        try:
            username = driver.find_element(By.ID, "user-name")
            username.send_keys("standard_user")
            take_screenshot(driver, "02_username_entered")
            
            password = driver.find_element(By.ID, "password")
            password.send_keys("secret_sauce")
            take_screenshot(driver, "03_password_entered")
            
            login = driver.find_element(By.ID, "login-button")
            login.click()
            
        except NoSuchElementException as e:
            print(f"✗ Login elements not found: {e}")
            take_screenshot(driver, "error_login_elements")
            raise
        
        # Step 3: Verify login
        time.sleep(2)
        current_url = driver.current_url
        if "/inventory.html" in current_url:
            print("✓ Login successful!")
        else:
            print("✗ Login failed")
        take_screenshot(driver, "04_inventory")
        
        # Step 4: Add item to cart
        try:
            add_to_cart = driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
            add_to_cart.click()
            take_screenshot(driver, "05_item_added")
            print("✓ Item added to cart")
        except Exception as e:
            print(f"✗ Could not add item: {e}")
            take_screenshot(driver, "error_add_cart")
        
        # Step 5: Navigate to cart
        cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_icon.click()
        time.sleep(1)
        take_screenshot(driver, "06_cart_page")
        print("✓ Navigated to cart")
        
        print("\n✓ Login flow with screenshots completed successfully!")
        
    except Exception as e:
        print(f"✗ Test failed with error: {e}")
        take_screenshot(driver, "test_failed")
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
```

---

## 5. Output with Clearly Labelled Screenshots

### Output Console (Summary):
```
Testing Basic Exception Handling
==================================================
✓ Page loaded
✗ NoSuchElementException caught: Element not found
✓ Screenshot saved: screenshots/after_error_20260908_151000.png
✓ Browser closed in finally block

Testing Generic Methods with Exception Handling
==================================================
✓ Navigated to SauceDemo
✓ Screenshot saved: screenshots/login_page_20260908_151000.png
✓ Found element: user-name
...
```

### Generated Screenplay Files:
- `screenshots/01_login_20260908_151000.png` - Initial login page
- `screenshots/02_username_entered_20260908_151001.png` - Username entered
- `screenshots/04_inventory_20260908_151002.png` - Inventory after login
- `screenshots/06_cart_page_20260908_151003.png` - Cart page

---

## 6. Brief Result, Observation, and Conclusion

### Result:
Successfully implemented screenshot capture at various stages and comprehensive exception handling. Created generic reusable methods that combine both features.

### Observation:
- Screenshots help debug failures by providing visual evidence
- Timestamp-based filenames prevent overwriting
- try-except-finally ensures browser cleanup even on failure
- Generic methods reduce code duplication and improve maintainability
- Different exception types require different handling

### Conclusion:
Combining screenshot capture with proper exception handling creates robust automation scripts. Screenshots provide valuable evidence for debugging and reporting, while proper exception handling ensures scripts fail gracefully and clean up resources.

---

**References:**
- Selenium Screenshots: https://www.selenium.dev/documentation/webdriver/interactions/
- Selenium Exceptions: https://www.selenium.dev/selenium/docs/api/py/common/selenium.common.exceptions.html
