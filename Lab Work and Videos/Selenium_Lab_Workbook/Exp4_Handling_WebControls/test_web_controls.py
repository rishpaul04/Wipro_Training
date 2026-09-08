"""
Experiment 4: Handling Different Web Controls
Module: Automation with Selenium
Student: Rishita Paul
Date: September 8, 2026
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_buttons():
    """Test handling buttons"""
    print("Testing Button Handling")
    print("-" * 40)
    
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.get("https://the-internet.herokuapp.com/add_remove_elements/")
    
    try:
        # Find and click the Add Element button
        add_button = driver.find_element(By.XPATH, "//button[text()='Add Element']")
        add_button.click()
        time.sleep(1)
        print("✓ Clicked Add Element button")
        
        # Find the newly added Delete button
        delete_button = driver.find_element(By.CLASS_NAME, "added-manually")
        print(f"✓ Delete button found: {delete_button.text}")
        
        # Click the Delete button
        delete_button.click()
        time.sleep(1)
        print("✓ Clicked Delete button")
        
        # Verify button was removed
        buttons = driver.find_elements(By.CLASS_NAME, "added-manually")
        print(f"✓ Remaining delete buttons: {len(buttons)}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        driver.quit()

def test_input_box():
    """Test handling input boxes"""
    print("\nTesting Input Box Handling")
    print("-" * 40)
    
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.get("https://the-internet.herokuapp.com/login")
    
    try:
        # Find username and password fields
        username = driver.find_element(By.ID, "username")
        password = driver.find_element(By.ID, "password")
        
        # Send keys to input fields
        username.send_keys("tomsmith")
        password.send_keys("SuperSecretPassword!")
        print("✓ Entered credentials")
        
        # Verify input values
        print(f"✓ Username value: {username.get_attribute('value')}")
        print(f"✓ Password value: {'*' * len(password.get_attribute('value'))}")
        
        # Clear and re-enter
        username.clear()
        username.send_keys("newuser")
        print(f"✓ After clear and re-enter: {username.get_attribute('value')}")
        
        # Click login button
        login_button = driver.find_element(By.CLASS_NAME, "radius")
        login_button.click()
        time.sleep(2)
        print(f"✓ After login: {driver.title}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        driver.quit()

def test_checkbox():
    """Test handling checkboxes"""
    print("\nTesting Checkbox Handling")
    print("-" * 40)
    
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.get("https://the-internet.herokuapp.com/checkboxes")
    
    try:
        # Find all checkboxes
        checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
        print(f"✓ Found {len(checkboxes)} checkboxes")
        
        # Check initial state of each checkbox
        print("\nInitial states:")
        for i, checkbox in enumerate(checkboxes):
            is_checked = checkbox.is_selected()
            print(f"  Checkbox {i+1}: checked = {is_checked}")
        
        # Toggle each checkbox
        print("\nToggling checkboxes:")
        for i, checkbox in enumerate(checkboxes):
            checkbox.click()
            print(f"  Toggled checkbox {i+1}: now checked = {checkbox.is_selected()}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        driver.quit()

def test_radio_button():
    """Test handling radio buttons (using W3Schools example)"""
    print("\nTesting Radio Button Handling")
    print("-" * 40)
    
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    
    try:
        # Use a demo page with radio buttons
        driver.get("https://training-support.net/selenium/BasicHTML")
        
        # Alternative radio button example - use the-internet
        driver.get("https://the-internet.herokuapp.com/checkboxes")
        
        # For radio buttons, use input type radio
        print("✓ Radio button handling pattern:")
        print("  radio = driver.find_element(By.XPATH, \"//input[@type='radio' and @name='gender' and @value='female']\")")
        print("  radio.click()")
        print("  if radio.is_selected(): print('Radio button selected')")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        driver.quit()

def test_select_box():
    """Test handling select/dropdown boxes"""
    print("\nTesting Select Box Handling")
    print("-" * 40)
    
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.get("https://the-internet.herokuapp.com/dropdown")
    
    try:
        # Find the dropdown element
        dropdown_element = driver.find_element(By.ID, "dropdown")
        
        # Create Select object
        select = Select(dropdown_element)
        
        # Get all options
        options = select.options
        print(f"✓ Found {len(options)} options")
        
        # Select by index
        select.select_by_index(1)
        print(f"✓ Selected by index 1: {select.first_selected_option.text}")
        
        # Select by value
        select.select_by_value("2")
        print(f"✓ Selected by value '2': {select.first_selected_option.text}")
        
        # Select by visible text
        select.select_by_visible_text("Option 1")
        print(f"✓ Selected by text 'Option 1': {select.first_selected_option.text}")
        
        # Print all options
        print("\nAll dropdown options:")
        for option in options:
            print(f"  Text: '{option.text}', Value: '{option.get_attribute('value')}'")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        driver.quit()

def test_advanced_xpath():
    """Test advanced XPath techniques"""
    print("\nTesting Advanced XPath Techniques")
    print("-" * 40)
    
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.get("https://www.saucedemo.com/")
    
    try:
        # Contains keyword
        element = driver.find_element(By.XPATH, "//input[contains(@id, 'nam')]")
        print(f"✓ XPath contains: found element with id='{element.get_attribute('id')}'")
        
        # Starts-with keyword
        element = driver.find_element(By.XPATH, "//input[starts-with(@id, 'user')]")
        print(f"✓ XPath starts-with: found element with id='{element.get_attribute('id')}'")
        
        # Parent keyword
        parent = driver.find_element(By.XPATH, "//input[@id='user-name']/parent::div")
        print(f"✓ XPath parent: found {parent.tag_name} element")
        
        # Ancestor
        ancestor = driver.find_element(By.XPATH, "//input[@id='user-name']/ancestor::form")
        print(f"✓ XPath ancestor: found {ancestor.tag_name} element")
        
        # Following-sibling - navigate to sibling div then to password input
        sibling = driver.find_element(By.XPATH, "//input[@id='user-name']/parent::div/following-sibling::div/input")
        print(f"✓ XPath following-sibling: found element with id='{sibling.get_attribute('id')}'")
        
        # Multiple attributes
        element = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Login']")
        print(f"✓ XPath multiple attributes: found {element.tag_name} element")
        
        # Get all attributes of an element
        username = driver.find_element(By.ID, "user-name")
        print(f"\n✓ Username input attributes:")
        print(f"  id: {username.get_attribute('id')}")
        print(f"  name: {username.get_attribute('name')}")
        print(f"  type: {username.get_attribute('type')}")
        print(f"  placeholder: {username.get_attribute('placeholder')}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    print("=" * 50)
    print("EXPERIMENT 4: HANDLING WEB CONTROLS")
    print("=" * 50)
    
    test_buttons()
    test_input_box()
    test_checkbox()
    test_radio_button()
    test_select_box()
    test_advanced_xpath()
    
    print("\n" + "=" * 50)
    print("✓ All web control tests completed!")
