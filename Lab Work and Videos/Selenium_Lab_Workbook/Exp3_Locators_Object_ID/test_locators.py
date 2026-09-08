"""
Experiment 3: Locators and Object Identification
Module: Automation with Selenium
Student: Rishita Paul
Date: September 8, 2026

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
    Navigate to SauceDemo login page and interact using different locators:
    - Username: By.ID
    - Password: By.NAME
    - Login button: By.XPATH
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
        print("✓ Entered username")
        
        password_field.send_keys("secret_sauce")
        print("✓ Entered password")
        
        # Click login button
        login_button.click()
        print("✓ Clicked login button")
        
        # Wait for page to load
        time.sleep(2)
        
        # Verify successful login
        current_url = driver.current_url
        print(f"Current URL: {current_url}")
        
        if "/inventory.html" in current_url:
            print("✓ VALIDATION: Login successful - URL contains /inventory.html")
        else:
            print("✗ VALIDATION: Login failed - URL does not contain /inventory.html")
            
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
        time.sleep(2)
        
        # 1. By.ID
        element = driver.find_element(By.ID, "user-name")
        print(f"1. By.ID: Found element - tag={element.tag_name}")
        
        # 2. By.NAME
        element = driver.find_element(By.NAME, "password")
        print(f"2. By.NAME: Found element - tag={element.tag_name}")
        
        # 3. By.CLASS_NAME
        element = driver.find_element(By.CLASS_NAME, "submit-button")
        print(f"3. By.CLASS_NAME: Found element - tag={element.tag_name}")
        
        # 4. By.TAG_NAME (single)
        element = driver.find_element(By.TAG_NAME, "input")
        print(f"4. By.TAG_NAME: Found element - tag={element.tag_name}")
        
        # 5. By.TAG_NAME (multiple - find_elements)
        elements = driver.find_elements(By.TAG_NAME, "input")
        print(f"5. By.TAG_NAME (multiple): Found {len(elements)} elements")
        
        # 6. By.CSS_SELECTOR (ID selector)
        element = driver.find_element(By.CSS_SELECTOR, "#user-name")
        print(f"6. By.CSS_SELECTOR (ID): Found element - tag={element.tag_name}")
        
        # 7. By.CSS_SELECTOR (Class selector)
        element = driver.find_element(By.CSS_SELECTOR, ".submit-button")
        print(f"7. By.CSS_SELECTOR (Class): Found element - tag={element.tag_name}")
        
        # 8. By.CSS_SELECTOR (Attribute selector)
        element = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
        print(f"8. By.CSS_SELECTOR (Attribute): Found element - tag={element.tag_name}")
        
        # 9. By.CSS_SELECTOR (Child selector)
        element = driver.find_element(By.CSS_SELECTOR, "form > input")
        print(f"9. By.CSS_SELECTOR (Child): Found element - tag={element.tag_name}")
        
        # 10. By.XPATH (Relative)
        element = driver.find_element(By.XPATH, "//input[@id='user-name']")
        print(f"10. By.XPATH (Relative): Found element - tag={element.tag_name}")
        
        # 11. By.XPATH (Contains)
        element = driver.find_element(By.XPATH, "//input[contains(@id,'user')]")
        print(f"11. By.XPATH (Contains): Found element - tag={element.tag_name}")
        
        # 12. By.XPATH (Starts-With)
        element = driver.find_element(By.XPATH, "//input[starts-with(@id,'user')]")
        print(f"12. By.XPATH (Starts-With): Found element - tag={element.tag_name}")
        
        print("\n✓ All locator types demonstrated successfully!")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    test_multi_locator()
    test_all_locators()
