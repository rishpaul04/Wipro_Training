"""
Experiment 5: Advanced Web Controls - JavaScript Alerts, Windows, and Iframes
Module: Automation with Selenium
Student: Rishita Paul
Date: September 8, 2026

This covers:
- Assignment 4: JavaScript Alerts and Confirms
- Assignment 6: Windows, Tabs, and Iframes
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

def test_javascript_alert():
    """Test JavaScript Alert - Assignment 4 part 1"""
    print("Assignment 4: JavaScript Alerts")
    print("=" * 50)
    
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.get("https://the-internet.herokuapp.com/javascript_alerts")
    
    try:
        # Test 1: JS Alert
        print("\n--- Test 1: JS Alert ---")
        alert_button = driver.find_element(By.XPATH, "//button[text()='Click for JS Alert']")
        alert_button.click()
        time.sleep(1)
        
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        print(f"✓ Alert text: '{alert.text}'")
        alert.accept()
        print("✓ Alert accepted")
        
        result = driver.find_element(By.ID, "result").text
        print(f"✓ Result: {result}")
        
        # Test 2: JS Confirm - Dismiss
        print("\n--- Test 2: JS Confirm (Dismiss) ---")
        confirm_button = driver.find_element(By.XPATH, "//button[text()='Click for JS Confirm']")
        confirm_button.click()
        time.sleep(1)
        
        confirm = WebDriverWait(driver, 10).until(EC.alert_is_present())
        print(f"✓ Confirm text: '{confirm.text}'")
        confirm.dismiss()
        print("✓ Confirm box dismissed (Cancel clicked)")
        
        result = driver.find_element(By.ID, "result").text
        print(f"✓ Result: {result}")
        
        # Test 3: JS Confirm - Accept
        print("\n--- Test 3: JS Confirm (Accept) ---")
        confirm_button.click()
        time.sleep(1)
        
        confirm = WebDriverWait(driver, 10).until(EC.alert_is_present())
        confirm.accept()
        print("✓ Confirm box accepted (OK clicked)")
        
        result = driver.find_element(By.ID, "result").text
        print(f"✓ Result: {result}")
        
        # Test 4: JS Prompt with text input
        print("\n--- Test 4: JS Prompt (with send_keys) ---")
        prompt_button = driver.find_element(By.XPATH, "//button[text()='Click for JS Prompt']")
        prompt_button.click()
        time.sleep(1)
        
        prompt = WebDriverWait(driver, 10).until(EC.alert_is_present())
        print(f"✓ Prompt text: '{prompt.text}'")
        prompt.send_keys("Rishita Paul")
        print("✓ Text 'Rishita Paul' entered into prompt")
        prompt.accept()
        print("✓ Prompt accepted")
        
        result = driver.find_element(By.ID, "result").text
        print(f"✓ Result: {result}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        driver.quit()
        print("✓ Browser closed")

def test_windows_tabs():
    """Test Windows and Tabs - Assignment 6 part 1"""
    print("\nAssignment 6: Windows and Tabs")
    print("=" * 50)
    
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.get("https://the-internet.herokuapp.com/windows")
    
    try:
        original_window = driver.current_window_handle
        print(f"✓ Original window handle: {original_window[:25]}...")
        print(f"✓ Original title: {driver.title}")
        
        # Open new window/tab
        link = driver.find_element(By.LINK_TEXT, "Click Here")
        link.click()
        time.sleep(2)
        
        # Get all window handles
        all_windows = driver.window_handles
        print(f"✓ Total handles: {len(all_windows)}")
        
        # Switch to new window
        for window in all_windows:
            if window != original_window:
                driver.switch_to.window(window)
                break
        
        # Get new window info
        print(f"✓ New window title: {driver.title}")
        print(f"✓ New window URL: {driver.current_url}")
        
        # Close the new window
        driver.close()
        print("✓ New window closed")
        
        # Switch back to original window
        driver.switch_to.window(original_window)
        print(f"✓ Switched back to: {driver.title}")
        print(f"✓ Current URL: {driver.current_url}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        driver.quit()
        print("✓ Browser closed")

def test_iframes():
    """Test Iframes - Assignment 6 part 2"""
    print("\nAssignment 6: Iframes")
    print("=" * 50)
    
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.get("https://the-internet.herokuapp.com/iframe")
    
    try:
        # Add explicit wait for iframe to load
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "mce_0_ifr"))
        )
        print("✓ Switched to iframe (id: mce_0_ifr)")
        
        # Interact with element inside iframe (TinyMCE contenteditable)
        editor_area = driver.find_element(By.ID, "tinymce")
        
        # Click to focus the contenteditable editor first
        editor_area.click()
        import time as _t
        _t.sleep(0.5)
        
        # Select existing content and delete it
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL)
        actions.send_keys(Keys.DELETE)
        actions.perform()
        print("✓ Cleared existing editor content")
        
        # Enter new text
        editor_area.send_keys("Hello from within the iframe!")
        print("✓ Text entered inside iframe editor")
        
        # Get text from inside iframe
        text = editor_area.text
        print(f"✓ Text in editor: '{text}'")
        
        # Switch back to main content
        driver.switch_to.default_content()
        print("✓ Switched back to main content")
        
        # Verify we're in main frame
        print(f"✓ Page title: {driver.title}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        driver.quit()
        print("✓ Browser closed")

def test_advanced_controls():
    """Additional advanced controls demo"""
    print("\nAdditional Advanced Controls")
    print("=" * 50)
    
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    
    try:
        # Keyboard events
        print("\n--- Keyboard Events ---")
        driver.get("https://the-internet.herokuapp.com/login")
        username = driver.find_element(By.ID, "username")
        
        actions = ActionChains(driver)
        actions.click(username)
        actions.send_keys("KEYBOARD_EVENT_TEST")
        actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL)
        actions.key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL)
        actions.perform()
        print(f"✓ Keyboard actions performed: {username.get_attribute('value')}")
        
        # Scroll operations
        print("\n--- Scroll Operations ---")
        driver.execute_script("window.scrollBy(0, 300)")
        time.sleep(1)
        print("✓ Scrolled down 300px")
        
        driver.execute_script("window.scrollTo(0, 0)")
        print("✓ Scrolled back to top")
        
        # Element state
        print("\n--- Element State ---")
        login_button = driver.find_element(By.CLASS_NAME, "radius")
        print(f"✓ Login button enabled: {login_button.is_enabled()}")
        print(f"✓ Login button displayed: {login_button.is_displayed()}")
        print(f"✓ Login button text: '{login_button.text}'")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        driver.quit()
        print("✓ Browser closed")

if __name__ == "__main__":
    print("=" * 60)
    print("EXPERIMENT 5: ADVANCED WEB CONTROLS")
    print("=" * 60)
    
    test_javascript_alert()
    test_windows_tabs()
    test_iframes()
    test_advanced_controls()
    
    print("\n" + "=" * 60)
    print("✓ All experiments completed!")
