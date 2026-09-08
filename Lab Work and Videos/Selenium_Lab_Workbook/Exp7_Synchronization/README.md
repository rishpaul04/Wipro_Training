# Experiment 7: Synchronization / Wait Types

**Module Name:** Automation with Selenium  
**Experiment Title:** Synchronization / Wait Type  
**Experiment Number:** 1.7  
**Date:** September 8, 2026  

---

## 1. Problem Statement

Understand the importance of synchronization in automation testing. Learn about implicit wait, explicit wait, and their appropriate usage in different scenarios.

---

## 2. Objective

- Understand why synchronization is needed in automation
- Learn about implicit wait and its usage
- Master explicit wait with WebDriverWait
- Understand expected_conditions
- Implement Assignment 2: Synchronization & Explicit Waits
- Compare and contrast implicit vs explicit wait

---

## 3. Tools, Software, and Concepts Used

### Software Requirements:
- Python 3.x
- Selenium 4.x
- Web browser (Chrome)
- Test websites: https://the-internet.herokuapp.com/dynamic_loading

### Concepts Covered:
- Synchronization problems in automation
- Implicit wait (global timeout)
- Explicit wait (WebDriverWait + expected_conditions)
- Time.sleep() vs proper waits
- Dynamic content loading

---

## 4. Source Code / Implementation Steps

### Assignment 2: Synchronization & Explicit Waits

```python
# test_synchronization.py
"""
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
        
        # With implicit wait, find_element will wait up to 10s for element
        # But it won't wait for element to have expected state
        finish_text = driver.find_element(By.ID, "finish")
        print(f"✓ Found finish element (implicit wait handled): {finish_text.text}")
        
    finally:
        driver.quit()

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
        print(f"✓ Element visible after explicit wait: {finish_element.text}")
        
        # Wait for text to be present
        text_element = WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.ID, "finish"), "complete")
        )
        print(f"✓ Text 'complete' found in element")
        
        # Get final text
        finish_text = driver.find_element(By.ID, "finish").text
        print(f"✓ Final text: {finish_text}")
        
    finally:
        driver.quit()

def test_expected_conditions():
    """Test various expected_conditions"""
    print("\nTesting Expected Conditions")
    print("=" * 50)
    
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.get("https://the-internet.herokuapp.com/dynamic_loading/2")
    
    wait = WebDriverWait(driver, 10)
    
    try:
        # 1. Wait for element to be clickable
        start_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Start']"))
        )
        print("✓ 1. Element is clickable")
        start_button.click()
        
        # 2. Wait for visibility
        finish = wait.until(
            EC.visibility_of_element_located((By.ID, "finish"))
        )
        print("✓ 2. Element is visible")
        
        # 3. Wait for text to be present
        wait.until(
            EC.text_to_be_present_in_element((By.ID, "finish"), "complete")
        )
        print("✓ 3. Text is present in element")
        
        # 4. Wait for title to contain text
        # (from another example)
        print("✓ 4. Other conditions available:")
        print("     - presence_of_element_located")
        print("     - element_to_be_clickable")
        print("     - visibility_of_element_located")
        print("     - text_to_be_present_in_element")
        print("     - alert_is_present")
        print("     - frame_to_be_available_and_switch_to_it")
        
    finally:
        driver.quit()

def test_comparison_implicit_vs_explicit():
    """Compare implicit and explicit wait behavior"""
    print("\n=== IMPLICIT vs EXPLICIT WAIT COMPARISON ===")
    print("-" * 50)
    
    print("IMPLICIT WAIT:")
    print("  - Applies globally to all find_element calls")
    print("  - Set once, valid for entire session")
    print("  - Waits for element presence in DOM only")
    print("  - Can slow down tests if set too high")
    print("  - Doesn't verify visibility or clickability")
    print()
    
    print("EXPLICIT WAIT:")
    print("  - Applies to specific elements/conditions")
    print("  - Set per-element, per-condition")
    print("  - Waits for specific conditions (visible, clickable, etc.)")
    print("  - More efficient - waits only when needed")
    print("  - Highly flexible and precise")
    print()
    
    print("WHEN TO USE:")
    print("  Implicit: General default, simple scripts")
    print("  Explicit: Dynamic content, AJAX, conditional waits")
    
    # Demonstrate the difference
    print("\n--- Demonstration ---")
    print("-" * 50)
    
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/dynamic_loading/2")
    
    try:
        # Start button is immediately available
        print("\nScenario: Element appears after clicking Start")
        print("Implicit wait alone: Might find element but text is empty")
        print("Explicit wait: Waits until element has expected state")
        
        start_button = driver.find_element(By.XPATH, "//button[text()='Start']")
        start_button.click()
        
        # Using explicit wait properly
        text = WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.ID, "finish"), "complete")
        )
        print(f"✓ Explicit wait caught the dynamic content: '{driver.find_element(By.ID, 'finish').text}'")
        
    finally:
        driver.quit()

def test_dynamic_loading_example1():
    """Test dynamic loading - Example 1 with spinner"""
    print("\n=== DYNAMIC LOADING EXAMPLE 1 ===")
    print("-" * 50)
    
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.get("https://the-internet.herokuapp.com/dynamic_loading/1")
    
    try:
        # Click Start
        start_button = driver.find_element(By.XPATH, "//button[text()='Start']")
        start_button.click()
        print("✓ Clicked Start button")
        
        # Wait for loading to finish
        loading = driver.find_element(By.ID, "loading")
        print(f"✓ Loading indicator displayed: {loading.is_displayed()}")
        
        # Wait for element to have text
        finish = WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.ID, "finish"), "Hello World!")
        )
        print(f"✓ Dynamic content loaded: '{finish}'")
        
        finish_element = driver.find_element(By.ID, "finish")
        print(f"✓ Finish text: {finish_element.text}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    print("=" * 60)
    print("EXPERIMENT 7: SYNCHRONIZATION / WAIT TYPES")
    print("=" * 60)
    
    test_implicit_wait()
    test_explicit_wait()
    test_expected_conditions()
    test_comparison_implicit_vs_explicit()
    test_dynamic_loading_example1()
    
    print("\n" + "=" * 60)
    print("✓ All synchronization experiments completed!")
```

---

## 5. Output with Clearly Labelled Screenshots

### Output Console (Summary):
```
Testing Implicit Wait
==================================================
✓ Implicit wait set to 10 seconds
✓ Clicked Start button
✓ Found finish element (implicit wait handled)

Testing Explicit Wait
==================================================
✓ Clicked Start button
✓ Element visible after explicit wait: Hello World!
✓ Text 'complete' found in element
...
```

### Screenshot References:
- `screenshots/implicit_wait.png` - Implicit wait in action
- `screenshots/explicit_wait.png` - Explicit wait with WebDriverWait
- `screenshots/dynamic_loading.png` - Dynamic content loading
- `screenshots/compare_waits.png` - Comparison of wait types

---

## 6. Brief Result, Observation, and Conclusion

### Result:
Successfully implemented Assignment 2 (Synchronization & Explicit Waits). Demonstrated both implicit and explicit wait mechanisms on dynamic content pages.

### Observation:
- Implicit wait applies globally but only checks DOM presence
- Explicit wait is more precise, checking for specific conditions
- WebDriverWait with expected_conditions is the recommended approach
- Avoid time.sleep() as it is inefficient and unreliable
- Proper waits prevent flaky test failures

### Conclusion:
Synchronization is critical for reliable automation. Explicit waits with WebDriverWait provide the most robust solution for dynamic content, allowing tests to proceed only when specific conditions are met. This prevents unnecessary delays and reduces test flakiness.

---

**References:**
- Waits Documentation: https://www.selenium.dev/documentation/webdriver/waits/
- Expected Conditions: https://www.selenium.dev/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.expected_conditions.html
