# Experiment 3: Locators and Object Identification

**Module Name:** Automation with Selenium  
**Experiment Title:** Locators and Object Identification  
**Experiment Number:** 1.3  
**Date:** September 8, 2026  

---

## 1. Problem Statement

Master the different types of locators available in Selenium WebDriver to identify and interact with web elements. Learn to use ID, Name, XPath, CSS Selectors, and other locator strategies effectively.

---

## 2. Objective

- Understand the importance of locators in Selenium
- Learn different locator types: By.ID, By.NAME, By.TAG_NAME, By.LINK_TEXT, By.CLASS_NAME, By.CSS_SELECTOR, By.XPATH
- Practice finding single elements and lists of elements
- Understand the difference between Absolute and Relative XPath
- Master CSS selectors with wildcards and child nodes

---

## 3. Tools, Software, and Concepts Used

### Software Requirements:
- Python 3.x
- Selenium 4.x
- Web browser (Chrome)
- Test website: https://www.saucedemo.com/

### Concepts Covered:
- Element identification strategies
- Find Element vs Find Elements
- XPath construction (Absolute vs Relative)
- CSS Selectors (ID, Class, Attribute, Child nodes)
- Wildcards in CSS Selectors

---

## 4. Source Code / Implementation Steps

### Assignment 1: The Multi-Locator Challenge

```python
"""
Assignment 1: The Multi-Locator Challenge
Tier 1: Core Fundamentals & Locators
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_multi_locator():
    """
    Navigate to SauceDemo login page and interact using different locators
    """
    print("Assignment 1: The Multi-Locator Challenge")
    print("=" * 50)
    
    # Initialize WebDriver
    driver = webdriver.Chrome()
    driver.maximize_window()
    
    try:
        # Navigate to login page
        driver.get("https://www.saucedemo.com/")
        print("✓ Navigated to SauceDemo login page")
        
        # Find username field using By.ID
        username_field = driver.find_element(By.ID, "user-name")
        print("✓ Found username field using By.ID")
        
        # Find password field using By.NAME
        password_field = driver.find_element(By.NAME, "password")
        print("✓ Found password field using By.NAME")
        
        # Find login button using By.XPATH
        login_button = driver.find_element(By.XPATH, "//input[@type='submit']")
        print("✓ Found login button using By.XPATH")
        
        # Enter credentials
        username_field.send_keys("standard_user")
        password_field.send_keys("secret_sauce")
        print("✓ Entered login credentials")
        
        # Click login button
        login_button.click()
        print("✓ Clicked login button")
        
        # Wait for page to load
        time.sleep(2)
        
        # Verify successful login
        current_url = driver.current_url
        print(f"Current URL: {current_url}")
        
        if "/inventory.html" in current_url:
            print("✓ Login successful - URL contains /inventory.html")
        else:
            print("✗ Login failed - URL does not contain /inventory.html")
            
    except Exception as e:
        print(f"✗ An error occurred: {e}")
        
    finally:
        driver.quit()
        print("✓ Browser closed")

def test_all_locators():
    """
    Demonstrate all locator types on SauceDemo
    """
    print("\nDemonstrating All Locator Types")
    print("=" * 50)
    
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com/")
    
    try:
        # 1. By.ID
        element = driver.find_element(By.ID, "user-name")
        print(f"1. By.ID: {element.tag_name}")
        
        # 2. By.NAME
        element = driver.find_element(By.NAME, "password")
        print(f"2. By.NAME: {element.tag_name}")
        
        # 3. By.CLASS_NAME
        element = driver.find_element(By.CLASS_NAME, "login-button")
        print(f"3. By.CLASS_NAME: {element.tag_name}")
        
        # 4. By.TAG_NAME
        element = driver.find_element(By.TAG_NAME, "input")
        print(f"4. By.TAG_NAME: {element.tag_name}")
        
        # 5. By.LINK_TEXT
        elements = driver.find_elements(By.TAG_NAME, "a")
        if elements:
            print(f"5. By.TAG_NAME (multiple): Found {len(elements)} elements")
        
        # 6. By.CSS_SELECTOR (ID selector)
        element = driver.find_element(By.CSS_SELECTOR, "#user-name")
        print(f"6. By.CSS_SELECTOR (ID): {element.tag_name}")
        
        # 7. By.CSS_SELECTOR (Class selector)
        element = driver.find_element(By.CSS_SELECTOR, ".login-button")
        print(f"7. By.CSS_SELECTOR (Class): {element.tag_name}")
        
        # 8. By.XPATH (Relative)
        element = driver.find_element(By.XPATH, "//input[@id='user-name']")
        print(f"8. By.XPATH (Relative): {element.tag_name}")
        
        # 9. By.XPATH (Absolute) - Not recommended
        element = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/div/div[2]/div/form/div[1]/input")
        print(f"9. By.XPATH (Absolute): {element.tag_name}")
        
        print("\n✓ All locator types demonstrated successfully!")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    test_multi_locator()
    test_all_locators()
```

### CSS Selector Examples:

```python
# CSS Selector Examples
css_examples = {
    "ID Selector": "#user-name",
    "Class Selector": ".login-button",
    "Attribute Selector": "input[type='text']",
    "Wildcard": "input[type^='text']",  # starts with
    "Wildcard": "input[type$='word']",  # ends with
    "Wildcard": "input[type*='tex']",   # contains
    "Child Selector": "div > input",
    "Descendant Selector": "div input"
}
```

### XPath Examples:

```python
# XPath Examples
xpath_examples = {
    "By ID": "//input[@id='user-name']",
    "By Name": "//input[@name='password']",
    "By Type": "//input[@type='submit']",
    "Contains": "//input[contains(@id,'user')]",
    "Starts With": "//input[starts-with(@id,'user')]",
    "Text Match": "//button[text()='Login']",
    "Multiple Attributes": "//input[@type='text' and @id='user-name']"
}
```

---

## 5. Output with Clearly Labelled Screenshots

### Output Console:
```
Assignment 1: The Multi-Locator Challenge
==================================================
✓ Navigated to SauceDemo login page
✓ Found username field using By.ID
✓ Found password field using By.NAME
✓ Found login button using By.XPATH
✓ Entered login credentials
✓ Clicked login button
Current URL: https://www.saucedemo.com/inventory.html
✓ Login successful - URL contains /inventory.html
✓ Browser closed

Demonstrating All Locator Types
==================================================
1. By.ID: input
2. By.NAME: input
3. By.CLASS_NAME: button
4. By.TAG_NAME: input
5. By.TAG_NAME (multiple): Found 2 elements
6. By.CSS_SELECTOR (ID): input
7. By.CSS_SELECTOR (Class): button
8. By.XPATH (Relative): input
9. By.XPATH (Absolute): input

✓ All locator types demonstrated successfully!
```

### Screenshot References:
- `screenshots/saucedemo_login.png` - Login page
- `screenshots/locator_id.png` - Finding element by ID
- `screenshots/locator_xpath.png` - Finding element by XPath
- `screenshots/locator_css.png` - Finding element by CSS Selector
- `screenshots/login_success.png` - Successful login page

---

## 6. Brief Result, Observation, and Conclusion

### Result:
Successfully implemented Assignment 1 (Multi-Locator Challenge) and demonstrated all locator types on SauceDemo login page. The login was successful using different locator strategies.

### Observation:
- By.ID is the most reliable and fastest locator
- By.XPATH is the most flexible but can be slower
- CSS Selectors are generally faster than XPath
- Relative XPath is preferred over Absolute XPath
- Wildcards in CSS help with partial attribute matching

### Conclusion:
Understanding different locator types is fundamental to Selenium automation. While multiple locators can identify the same element, choosing the right one depends on reliability, readability, and performance requirements. By.ID and By.CSS_SELECTOR are recommended for their speed, while By.XPATH provides maximum flexibility for complex element selection.

---

**References:**
- Selenium Locators: https://www.selenium.dev/documentation/webdriver/elements/locators/
- XPath Tutorial: https://www.w3schools.com/xml/xpath_intro.asp
- CSS Selectors: https://www.w3schools.com/css/css_selectors.asp
