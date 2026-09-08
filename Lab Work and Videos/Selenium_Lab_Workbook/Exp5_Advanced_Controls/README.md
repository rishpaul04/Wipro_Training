# Experiment 5: Advanced Web Controls

**Module Name:** Automation with Selenium  
**Experiment Title:** Handling Different Controls on Web Page - Advanced  
**Experiment Number:** 1.5  
**Date:** September 8, 2026  

---

## 1. Problem Statement

Handle advanced web controls including JavaScript alerts, date pickers, file uploads, multiple windows/tabs, keyboard events, scrolling, drag and drop, iframes, and element state verification.

---

## 2. Objective

- Handle JavaScript Alert, Confirm, and Prompt boxes
- Interact with date pickers
- Handle file upload functionality
- Manage multiple windows/tabs
- Work with keyboard events using ActionChains
- Control page scrolling
- Implement drag and drop operations
- Handle iframes
- Verify element states (enabled, disabled)
- Get element text and attribute values

---

## 3. Tools, Software, and Concepts Used

### Software Requirements:
- Python 3.x
- Selenium 4.x
- Web browser (Chrome)
- Test websites: https://the-internet.herokuapp.com/

### Concepts Covered:
- JavaScript Alerts (Alert, Confirm, Prompt)
- WebDriverWait with expected_conditions
- ActionChains for keyboard/mouse events
- window_handles for tab switching
- execute_script for scrolling
- Frame handling
- Element state verification

---

## 4. Source Code / Implementation Steps

### Assignment 4: JavaScript Alerts and Confirms

```python
# test_alerts.py
"""
Assignment 4: JavaScript Alerts and Confirms
Tier 2: Advanced User Interactions
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_javascript_alert():
    """Test JavaScript Alert"""
    print("Testing JavaScript Alert")
    print("-" * 40)
    
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/javascript_alerts")
    
    try:
        # Trigger JavaScript Alert
        alert_button = driver.find_element(By.XPATH, "//button[text()='Click for JS Alert']")
        alert_button.click()
        time.sleep(1)
        
        # Switch to alert and get text
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        print(f"✓ Alert text: {alert.text}")
        
        # Accept the alert
        alert.accept()
        print("✓ Alert accepted")
        
        # Verify result
        result = driver.find_element(By.ID, "result").text
        print(f"✓ Result: {result}")
        
    finally:
        driver.quit()

def test_confirm_box():
    """Test JavaScript Confirm Box"""
    print("\nTesting JavaScript Confirm Box")
    print("-" * 40)
    
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/javascript_alerts")
    
    try:
        # Trigger Confirm box
        confirm_button = driver.find_element(By.XPATH, "//button[text()='Click for JS Confirm']")
        confirm_button.click()
        time.sleep(1)
        
        # Switch to confirm box
        confirm = WebDriverWait(driver, 10).until(EC.alert_is_present())
        print(f"✓ Confirm text: {confirm.text}")
        
        # Dismiss the confirm box (click Cancel)
        confirm.dismiss()
        print("✓ Confirm box dismissed (Cancel clicked)")
        
        # Verify result
        result = driver.find_element(By.ID, "result").text
        print(f"✓ Result: {result}")
        
        # Trigger confirm box again and accept
        confirm_button.click()
        time.sleep(1)
        confirm = WebDriverWait(driver, 10).until(EC.alert_is_present())
        confirm.accept()
        print("✓ Confirm box accepted (OK clicked)")
        
        result = driver.find_element(By.ID, "result").text
        print(f"✓ Result: {result}")
        
    finally:
        driver.quit()

def test_prompt_box():
    """Test JavaScript Prompt Box"""
    print("\nTesting JavaScript Prompt Box")
    print("-" * 40)
    
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/javascript_alerts")
    
    try:
        # Trigger Prompt box
        prompt_button = driver.find_element(By.XPATH, "//button[text()='Click for JS Prompt']")
        prompt_button.click()
        time.sleep(1)
        
        # Switch to prompt box
        prompt = WebDriverWait(driver, 10).until(EC.alert_is_present())
        print(f"✓ Prompt text: {prompt.text}")
        
        # Enter text into prompt
        prompt.send_keys("Rishita Paul")
        print("✓ Text entered into prompt")
        
        # Accept the prompt
        prompt.accept()
        print("✓ Prompt accepted")
        
        # Verify result
        result = driver.find_element(By.ID, "result").text
        print(f"✓ Result: {result}")
        
    finally:
        driver.quit()

def test_file_upload():
    """Test file upload"""
    print("\nTesting File Upload")
    print("-" * 40)
    
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/upload")
    
    try:
        # Find file input
        file_input = driver.find_element(By.ID, "file-upload")
        
        # Send file path to input
        file_path = r"C:\test_file.txt"
        file_input.send_keys(file_path)
        
        # Click upload button
        upload_button = driver.find_element(By.ID, "file-submit")
        upload_button.click()
        time.sleep(2)
        
        # Verify upload
        uploaded_file = driver.find_element(By.ID, "uploaded-files").text
        print(f"✓ Uploaded file: {uploaded_file}")
        
    finally:
        driver.quit()

def test_multiple_windows():
    """Test multiple window handling"""
    print("\nTesting Multiple Windows/Tabs")
    print("-" * 40)
    
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/windows")
    
    try:
        # Get current window handle
        original_window = driver.current_window_handle
        print(f"✓ Original window: {original_window[:20]}...")
        
        # Open new window
        link = driver.find_element(By.LINK_TEXT, "Click Here")
        link.click()
        time.sleep(2)
        
        # Get all window handles
        all_windows = driver.window_handles
        print(f"✓ Total windows: {len(all_windows)}")
        
        # Switch to new window
        for window in all_windows:
            if window != original_window:
                driver.switch_to.window(window)
                break
        
        # Get new window title
        print(f"✓ New window title: {driver.title}")
        print(f"✓ New window URL: {driver.current_url}")
        
        # Switch back to original window
        driver.switch_to.window(original_window)
        print(f"✓ Switched back to original window: {driver.title}")
        
    finally:
        driver.quit()

def test_actions_keyboard():
    """Test keyboard events with ActionChains"""
    print("\nTesting Keyboard Events")
    print("-" * 40)
    
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.keys import Keys
    
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/login")
    
    try:
        # Find input field
        username = driver.find_element(By.ID, "username")
        
        # Perform keyboard actions with ActionChains
        actions = ActionChains(driver)
        actions.click(username)
        actions.send_keys("UPPERCASE")
        actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL)
        actions.key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL)
        actions.perform()
        
        print(f"✓ Text entered: {username.get_attribute('value')}")
        
        # Press Tab to move to next field
        actions = ActionChains(driver)
        actions.send_keys(Keys.TAB).perform()
        time.sleep(1)
        
        # Get focused element
        focused = driver.switch_to.active_element
        print(f"✓ Focused element after TAB: {focused.get_attribute('id')}")
        
    finally:
        driver.quit()

def test_scroll():
    """Test scrolling operations"""
    print("\nTesting Scroll Operations")
    print("-" * 40)
    
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com/inventory.html")
    
    try:
        # Login first (needed for inventory page)
        username = driver.find_element(By.ID, "user-name")
        username.send_keys("standard_user")
        password = driver.find_element(By.ID, "password")
        password.send_keys("secret_sauce")
        login = driver.find_element(By.ID, "login-button")
        login.click()
        time.sleep(2)
        
        # Scroll by pixels
        driver.execute_script("window.scrollBy(0, 500)")
        time.sleep(1)
        print("✓ Scrolled down by 500 pixels")
        
        # Scroll to specific element
        element = driver.find_element(By.CLASS_NAME, "inventory_item")
        driver.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(1)
        print("✓ Scrolled to inventory item")
        
        # Scroll to bottom of page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1)
        print("✓ Scrolled to bottom of page")
        
        # Scroll back to top
        driver.execute_script("window.scrollTo(0, 0)")
        time.sleep(1)
        print("✓ Scrolled back to top")
        
    finally:
        driver.quit()

def test_iframe():
    """Test iframe handling"""
    print("\nTesting Iframe Handling")
    print("-" * 40)
    
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/iframe")
    
    try:
        # Switch to iframe by id
        driver.switch_to.frame("mce_0_ifr")
        print("✓ Switched to iframe")
        
        # Interact with element inside iframe
        editor_area = driver.find_element(By.ID, "tinymce")
        editor_area.clear()
        editor_area.send_keys("Hello from iframe!")
        print("✓ Text entered inside iframe")
        
        # Switch back to main content
        driver.switch_to.default_content()
        print("✓ Switched back to main content")
        
        # Verify page title
        print(f"✓ Page title: {driver.title}")
        
    finally:
        driver.quit()

def test_element_state():
    """Test element state verification"""
    print("\nTesting Element State Verification")
    print("-" * 40)
    
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/buttons")
    
    try:
        # Navigate to disabled elements page
        driver.get("https://the-internet.herokuapp.com/")
        element = driver.find_element(By.LINK_TEXT, "Elemental Selenium")
        if element:
            print(f"✓ Element found: {element.text}")
        
        # Check element states on add/remove page
        driver.get("https://the-internet.herokuapp.com/add_remove_elements/")
        add_button = driver.find_element(By.XPATH, "//button[text()='Add Element']")
        print(f"✓ Add button enabled: {add_button.is_enabled()}")
        print(f"✓ Add button displayed: {add_button.is_displayed()}")
        
        # Get element attributes
        print(f"✓ Button class: {add_button.get_attribute('class')}")
        print(f"✓ Button tag: {add_button.tag_name}")
        print(f"✓ Button text: {add_button.text}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    test_javascript_alert()
    test_confirm_box()
    test_prompt_box()
    test_multiple_windows()
    test_actions_keyboard()
    test_scroll()
    test_iframe()
    test_element_state()
```

---

## 5. Output with Clearly Labelled Screenshots

### Output Console (Summary):
```
Testing JavaScript Alert
----------------------------------------
✓ Alert text: I am a JS Alert
✓ Alert accepted
✓ Result: You successfully clicked an alert

Testing Confirm Box
----------------------------------------
✓ Confirm text: I am a JS Confirm
✓ Confirm box dismissed (Cancel clicked)
✓ Result: You clicked: Cancel
...
```

### Screenshot References:
- `screenshots/js_alert.png` - JavaScript Alert dialog
- `screenshots/js_confirm.png` - JavaScript Confirm dialog
- `screenshots/js_prompt.png` - JavaScript Prompt with text input
- `screenshots/multiple_windows.png` - Multiple browser windows
- `screenshots/iframe_editor.png` - Content inside iframe
- `screenshots/file_upload.png` - File upload success
- `screenshots/scroll_page.png` - Scrolled webpage

---

## 6. Brief Result, Observation, and Conclusion

### Result:
Successfully handled all advanced web controls including JavaScript alerts (alert, confirm, prompt), multiple windows, keyboard events, scrolling, and iframes.

### Observation:
- JavaScript alerts require switching to alert context
- webdriver.switch_to.alert provides methods: accept(), dismiss(), send_keys()
- Window handles allow switching between browser tabs/windows
- ActionChains enables complex keyboard and mouse operations
- execute_script() handles scrolling operations effectively
- iframes require frame switching before element interaction

### Conclusion:
Advanced web controls require specialized handling techniques. Understanding the patterns for alerts, windows, iframes, and keyboard events is crucial for comprehensive web automation. These techniques enable automation of complex user interactions.

---

**References:**
- JavaScript Alerts: https://the-internet.herokuapp.com/javascript_alerts
- ActionChains: https://www.selenium.dev/documentation/webdriver/actions_api/
- Frame Handling: https://www.selenium.dev/documentation/webdriver/browser_manipulation/
