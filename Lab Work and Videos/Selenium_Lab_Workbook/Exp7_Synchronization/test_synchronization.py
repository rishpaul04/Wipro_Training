"""
Experiment 7: Synchronization / Wait Types
Module: Automation with Selenium
Student: Rishita Paul
Date: September 8, 2026

Assignment 2: Synchronization & Explicit Waits
Tier 1: Core Fundamentals & Locators
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_implicit_wait():
    """Test implicit wait behavior"""
    print("Testing Implicit Wait")
    print("=" * 50)
    
    driver = webdriver.Chrome()
    
    # Set implicit wait - applies to all elements globally
    driver.implicitly_wait(10)
    print("✓ Implicit wait set to 10 seconds")
    
    driver.get("https://the-internet.herokuapp.com/dynamic_loading/2")
    
    try:
        # Click Start button
        start_button = driver.find_element(By.XPATH, "//button[text()='Start']")
        start_button.click()
        print("✓ Clicked Start button")
        
        # With implicit wait, find_element will wait up to 10s for DOM presence
        finish_text = driver.find_element(By.ID, "finish")
        print(f"✓ Found finish element")
        print(f"  Text (may be empty without explicit wait): '{finish_text.text}'")
        print(f"  Displayed: {finish_text.is_displayed()}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        driver.quit()
        print("✓ Browser closed")

def test_explicit_wait():
    """Test explicit wait behavior"""
    print("\nTesting Explicit Wait")
    print("=" * 50)
    
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/dynamic_loading/2")
    
    try:
        # Click Start button
        start_button = driver.find_element(By.XPATH, "//button[text()='Start']")
        start_button.click()
        print("✓ Clicked Start button")
        
        # Explicit wait for element to be visible
        finish_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "finish"))
        )
        print(f"✓ Element visible after explicit wait")
        print(f"  Text: '{finish_element.text}'")
        
        # Wait for text to be present in element
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.ID, "finish"), "Hello World!")
        )
        print("✓ Text 'Hello World!' confirmed in element")
        
        # Get final text
        finish_text = driver.find_element(By.ID, "finish").text
        print(f"✓ Final text: '{finish_text}'")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        driver.quit()
        print("✓ Browser closed")

def test_expected_conditions():
    """Test various expected_conditions"""
    print("\nTesting Expected Conditions")
    print("=" * 50)
    
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.get("https://the-internet.herokuapp.com/dynamic_loading/2")
    
    try:
        wait = WebDriverWait(driver, 10)
        
        # 1. Element to be clickable
        start_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Start']"))
        )
        print("✓ 1. element_to_be_clickable - Start button ready")
        start_button.click()
        
        # 2. Element to be visible
        finish = wait.until(
            EC.visibility_of_element_located((By.ID, "finish"))
        )
        print("✓ 2. visibility_of_element_located - Finish element visible")
        
        # 3. Text to be present in element
        wait.until(
            EC.text_to_be_present_in_element((By.ID, "finish"), "Hello World!")
        )
        print("✓ 3. text_to_be_present_in_element - Text confirmed")
        
        print("\nOther commonly used expected_conditions:")
        print("  - presence_of_element_located")
        print("  - presence_of_all_elements_located")
        print("  - element_to_be_selected")
        print("  - alert_is_present")
        print("  - frame_to_be_available_and_switch_to_it")
        print("  - invisibility_of_element_located")
        print("  - element_to_be_clickable")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        driver.quit()
        print("✓ Browser closed")

def test_comparison():
    """Compare implicit and explicit wait behavior"""
    print("\n=== IMPLICIT vs EXPLICIT WAIT COMPARISON ===")
    print("-" * 50)
    
    print("\nIMPLICIT WAIT:")
    print("  • Global setting - applies to ALL find_element calls")
    print("  • Set once using driver.implicitly_wait(seconds)")
    print("  • Waits for element PRESENCE in DOM only")
    print("  • Doesn't verify element visibility or enabled state")
    print("  • Can slow down tests if set too high")
    
    print("\nEXPLICIT WAIT:")
    print("  • Per-element/per-condition setting")
    print("  • Uses WebDriverWait + expected_conditions")
    print("  • Waits for SPECIFIC conditions")
    print("  • More efficient and precise")
    print("  • Highly recommended for dynamic content")
    
    print("\nRECOMMENDATION:")
    print("  ✓ Use explicit wait for dynamic elements")
    print("  ✓ Use implicit wait as a baseline")
    print("  ✗ Avoid time.sleep() - inefficient and flaky")
    
    # Demonstrate
    print("\n--- DEMONSTRATION ---")
    print("-" * 50)
    
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/dynamic_loading/2")
    
    try:
        start_button = driver.find_element(By.XPATH, "//button[text()='Start']")
        start_button.click()
        print("\n✓ Clicked Start")
        
        # time.sleep approach (not recommended)
        time.sleep(5)
        print("✗ time.sleep(5): Waits fixed 5s - inefficient")
        
        # Explicit wait approach (recommended)
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.ID, "finish"), "Hello World!")
        )
        print("✓ Explicit wait: Waits only until condition met")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        driver.quit()
        print("✓ Browser closed")

def test_dynamic_loading_example1():
    """Test dynamic loading - Example 1"""
    print("\n=== DYNAMIC LOADING - EXAMPLE 1 ===")
    print("-" * 50)
    
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.get("https://the-internet.herokuapp.com/dynamic_loading/1")
    
    try:
        # Check initial state
        print("Checking initial state...")
        start_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button"))
        )
        print(f"  Start button enabled: {start_button.is_enabled()}")
        print(f"  Start button text: '{start_button.text}'")
        
        # Click Start
        start_button.click()
        print("\n✓ Clicked Start button")
        time.sleep(1)
        
        # Check loading indicator
        loading = driver.find_element(By.ID, "loading")
        print(f"  Loading displayed: {loading.is_displayed()}")
        
        # Wait for text to be present (bypasses loading spinner)
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.ID, "finish"), "Hello World!")
        )
        print("✓ Dynamic content loaded with explicit wait!")
        
        finish_element = driver.find_element(By.ID, "finish")
        print(f"  Finish text: '{finish_element.text}'")
        print(f"  Loading displayed after: {loading.is_displayed()}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        driver.quit()
        print("✓ Browser closed")

if __name__ == "__main__":
    print("=" * 60)
    print("EXPERIMENT 7: SYNCHRONIZATION / WAIT TYPES")
    print("=" * 60)
    
    test_implicit_wait()
    test_explicit_wait()
    test_expected_conditions()
    test_comparison()
    test_dynamic_loading_example1()
    
    print("\n" + "=" * 60)
    print("✓ All synchronization experiments completed!")
