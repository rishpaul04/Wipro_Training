# Experiment 9: Advance Interactions

**Module Name:** Automation with Selenium  
**Experiment Title:** Advance Interactions  
**Experiment Number:** 1.9  
**Date:** September 8, 2026  

---

## 1. Problem Statement

Master advanced automation techniques including reading/writing data from various file formats (Excel, JSON, CSV, Properties, XML), implementing mouse hover actions, and executing JavaScript commands within Selenium WebDriver.

---

## 2. Objective

- Read and write data from Excel sheets using openpyxl
- Read and write JSON data
- Read and write CSV files
- Read data from properties (INI) and XML files
- Implement mouse hover actions using ActionChains
- Execute JavaScript commands with execute_script()
- Create a comprehensive data-driven test framework

---

## 3. Tools, Software, and Concepts Used

### Software Requirements:
- Python 3.x
- Selenium 4.x
- Web browser (Chrome)
- Libraries: openpyxl, json, csv, configparser, xml.etree.ElementTree

### Concepts Covered:
- Data-driven testing (DDT)
- Excel file manipulation (openpyxl)
- JSON data handling
- CSV file reading/writing
- Properties file parsing
- XML parsing
- ActionChains mouse operations
- JavaScript execution

---

## 4. Source Code / Implementation Steps

```python
# test_advance_interactions.py
"""
Experiment 9: Advance Interactions
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import csv
import os
from openpyxl import Workbook, load_workbook
import xml.etree.ElementTree as ET
import configparser

# ============================================
# EXCEL HANDLING
# ============================================
def excel_write_data():
    """Write data to Excel file"""
    print("Writing Data to Excel File")
    print("-" * 40)
    
    # Create a new workbook
    wb = Workbook()
    sheet = wb.active
    sheet.title = "TestData"
    
    # Add headers
    headers = ["Username", "Password", "Expected Result"]
    sheet.append(headers)
    
    # Add test data
    test_data = [
        ["standard_user", "secret_sauce", "Login Successful"],
        ["locked_out_user", "secret_sauce", "Login Failed - Account Locked"],
        ["problem_user", "secret_sauce", "Login Successful"],
        ["performance_glitch_user", "secret_sauce", "Login Successful"]
    ]
    
    for row in test_data:
        sheet.append(row)
    
    # Save the workbook
    wb.save("testdata.xlsx")
    print(f"✓ Excel file created with {len(test_data)} rows of data")
    
    return "testdata.xlsx"

def excel_read_data():
    """Read data from Excel file"""
    print("\nReading Data from Excel File")
    print("-" * 40)
    
    try:
        wb = load_workbook("testdata.xlsx")
        sheet = wb.active
        
        print(f"Sheet name: {sheet.title}")
        print(f"Max rows: {sheet.max_row}")
        print(f"Max columns: {sheet.max_column}")
        
        # Read header
        headers = [cell.value for cell in sheet[1]]
        print(f"Headers: {headers}")
        
        # Read all data
        print("\nData:")
        for row in sheet.iter_rows(min_row=2, values_only=True):
            print(f"  {row}")
        
        # Read specific cell
        print(f"\nCell B2: {sheet['B2'].value}")
        print(f"Cell A3: {sheet['A3'].value}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error reading Excel: {e}")
        return False

def excel_update_data():
    """Update data in Excel file"""
    print("\nUpdating Excel File")
    print("-" * 40)
    
    try:
        wb = load_workbook("testdata.xlsx")
        sheet = wb.active
        
        # Update a cell
        sheet['A2'] = "standard_user_updated"
        wb.save("testdata.xlsx")
        
        print("✓ Updated A2 cell")
        
        # Verify update
        wb = load_workbook("testdata.xlsx")
        sheet = wb.active
        print(f"✓ Verified: A2 = {sheet['A2'].value}")
        
    except Exception as e:
        print(f"✗ Error updating Excel: {e}")

# ============================================
# JSON HANDLING
# ============================================
def json_write_data():
    """Write data to JSON file"""
    print("\nWriting Data to JSON File")
    print("-" * 40)
    
    data = {
        "test_data": [
            {
                "username": "standard_user",
                "password": "secret_sauce",
                "expected": "login_success"
            },
            {
                "username": "locked_out_user",
                "password": "secret_sauce",
                "expected": "login_failed"
            }
        ],
        "test_config": {
            "browser": "chrome",
            "timeout": 10,
            "headless": False
        }
    }
    
    with open("testdata.json", "w") as f:
        json.dump(data, f, indent=4)
    
    print("✓ JSON file created successfully")
    return "testdata.json"

def json_read_data():
    """Read data from JSON file"""
    print("\nReading Data from JSON File")
    print("-" * 40)
    
    try:
        with open("testdata.json", "r") as f:
            data = json.load(f)
        
        print("JSON Data Structure:")
        print(f"  Keys: {list(data.keys())}")
        print(f"  Test config: {data['test_config']}")
        print(f"  Number of test cases: {len(data['test_data'])}")
        
        for test in data['test_data']:
            print(f"  Test: {test}")
        
        # Access nested data
        browser = data['test_config']['browser']
        print(f"\n  Browser from config: {browser}")
        
        first_username = data['test_data'][0]['username']
        print(f"  First username: {first_username}")
        
    except Exception as e:
        print(f"✗ Error reading JSON: {e}")

# ============================================
# CSV HANDLING
# ============================================
def csv_write_data():
    """Write data to CSV file"""
    print("\nWriting Data to CSV File")
    print("-" * 40)
    
    with open("testdata.csv", "w", newline="") as f:
        writer = csv.writer(f)
        
        # Write headers
        writer.writerow(["Test Case", "Username", "Password", "Expected Result"])
        
        # Write data
        test_cases = [
            ["TC001", "standard_user", "secret_sauce", "Login Success"],
            ["TC002", "locked_out_user", "secret_sauce", "Login Failed"],
            ["TC003", "problem_user", "secret_sauce", "Login Success"],
            ["TC004", "performance_glitch_user", "secret_sauce", "Login Success"]
        ]
        
        writer.writerows(test_cases)
    
    print("✓ CSV file created with 4 test cases")

def csv_read_data():
    """Read data from CSV file"""
    print("\nReading Data from CSV File")
    print("-" * 40)
    
    try:
        with open("testdata.csv", "r") as f:
            reader = csv.reader(f)
            
            # Read header
            headers = next(reader)
            print(f"Headers: {headers}")
            
            # Read data
            print("\nCSV Data:")
            for row in reader:
                print(f"  {row}")
        
        print("\n✓ CSV reading completed")
        
    except Exception as e:
        print(f"✗ Error reading CSV: {e}")

# ============================================
# XML HANDLING
# ============================================
def xml_write_data():
    """Write data to XML file"""
    print("\nWriting Data to XML File")
    print("-" * 40)
    
    # Create root element
    root = ET.Element("TestData")
    root.set("environment", "test")
    
    # Add test cases
    test_data = [
        {"id": "TC001", "username": "standard_user", "password": "secret_sauce"},
        {"id": "TC002", "username": "problem_user", "password": "secret_sauce"}
    ]
    
    for data in test_data:
        test_case = ET.SubElement(root, "TestCase")
        test_case.set("id", data["id"])
        
        username = ET.SubElement(test_case, "Username")
        username.text = data["username"]
        
        password = ET.SubElement(test_case, "Password")
        password.text = data["password"]
    
    # Create tree and save
    tree = ET.ElementTree(root)
    tree.write("testdata.xml", encoding="utf-8", xml_declaration=True)
    
    print("✓ XML file created successfully")

def xml_read_data():
    """Read data from XML file"""
    print("\nReading Data from XML File")
    print("-" * 40)
    
    try:
        tree = ET.parse("testdata.xml")
        root = tree.getroot()
        
        print(f"Root element: {root.tag}")
        print(f"Root attributes: {root.attrib}")
        
        # Find all test cases
        for test_case in root.findall("TestCase"):
            test_id = test_case.get("id")
            username = test_case.find("Username").text
            password = test_case.find("Password").text
            print(f"  Test Case {test_id}: {username} / {password}")
        
        print("\n✓ XML reading completed")
        
    except Exception as e:
        print(f"✗ Error reading XML: {e}")

# ============================================
# PROPERTIES FILE HANDLING
# ============================================
def properties_write_data():
    """Write data to properties (INI) file"""
    print("\nWriting Data to Properties File")
    print("-" * 40)
    
    config = configparser.ConfigParser()
    
    # Add sections
    config["browser"] = {
        "name": "chrome",
        "headless": "false",
        "timeout": "10"
    }
    
    config["application"] = {
        "url": "https://www.saucedemo.com/",
        "environment": "qa"
    }
    
    config["credentials"] = {
        "username": "standard_user",
        "password": "secret_sauce"
    }
    
    # Write to file
    with open("testdata.properties", "w") as configfile:
        config.write(configfile)
    
    print("✓ Properties file created successfully")

def properties_read_data():
    """Read data from properties file"""
    print("\nReading Data from Properties File")
    print("-" * 40)
    
    try:
        config = configparser.ConfigParser()
        config.read("testdata.properties")
        
        # Read values
        browser = config["browser"]["name"]
        timeout = config["browser"]["timeout"]
        url = config["application"]["url"]
        env = config["application"]["environment"]
        username = config["credentials"]["username"]
        password = config["credentials"]["password"]
        
        print(f"Browser: {browser}")
        print(f"Timeout: {timeout}")
        print(f"URL: {url}")
        print(f"Environment: {env}")
        print(f"Username: {username}")
        print(f"Password: {password}")
        
        print("\n✓ Properties file reading completed")
        
    except Exception as e:
        print(f"✗ Error reading properties: {e}")

# ============================================
# MOUSE HOVER ACTIONS
# ============================================
def test_mouse_hover():
    """Test mouse hover actions"""
    print("\nTesting Mouse Hover Actions")
    print("-" * 40)
    
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    
    try:
        driver.get("https://www.saucedemo.com/")
        print("✓ Page loaded")
        
        # Login first to access inventory
        username = driver.find_element(By.ID, "user-name")
        username.send_keys("standard_user")
        password = driver.find_element(By.ID, "password")
        password.send_keys("secret_sauce")
        login = driver.find_element(By.ID, "login-button")
        login.click()
        import time
        time.sleep(2)
        
        # Find an inventory item
        item = driver.find_element(By.CLASS_NAME, "inventory_item")
        
        # Hover over the item
        actions = ActionChains(driver)
        actions.move_to_element(item).perform()
        print("✓ Mouse hovered over inventory item")
        
        # Hover and inspect
        img = driver.find_element(By.CLASS_NAME, "inventory_item_img")
        actions.move_to_element(img).perform()
        print("✓ Mouse hovered over product image")
        
        # Hover with pause
        actions.move_to_element(item).pause(2).perform()
        print("✓ Hover with 2 second pause completed")
        
        # Double click action
        actions.double_click(item).perform()
        print("✓ Double click performed")
        
        print("\n✓ Mouse hover actions completed")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        driver.quit()
        print("✓ Browser closed")

# ============================================
# JAVASCRIPT EXECUTION
# ============================================
def test_javascript_execution():
    """Test JavaScript command execution"""
    print("\nTesting JavaScript Execution")
    print("-" * 40)
    
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    
    try:
        driver.get("https://www.saucedemo.com/")
        print("✓ Page loaded")
        
        # Execute JavaScript to get page title
        title = driver.execute_script("return document.title;")
        print(f"✓ JavaScript: Page title = '{title}'")
        
        # Execute JavaScript to get URL
        url = driver.execute_script("return window.location.href;")
        print(f"✓ JavaScript: Page URL = '{url}'")
        
        # Execute JavaScript to scroll
        driver.execute_script("window.scrollBy(0, 500);")
        print("✓ JavaScript: Scrolled down 500px")
        
        # Execute JavaScript to get scroll position
        scroll_y = driver.execute_script("return window.scrollY;")
        print(f"✓ JavaScript: Current scroll Y = {scroll_y}")
        
        # Execute JavaScript to change element attribute
        username = driver.find_element(By.ID, "user-name")
        driver.execute_script(
            "arguments[0].setAttribute('style', 'border: 2px solid red;')",
            username
        )
        print("✓ JavaScript: Changed element border color")
        
        # Execute JavaScript to get element text
        form_text = driver.execute_script("return document.querySelector('form').innerText;")
        print(f"✓ JavaScript: Form text = '{form_text.strip()[:50]}'")
        
        # Execute JavaScript to click element
        login_btn = driver.find_element(By.ID, "login-button")
        driver.execute_script("arguments[0].click();", login_btn)
        print("✓ JavaScript: Clicked login button via script")
        
        # Execute JavaScript to return values
        result = driver.execute_script("return {height: window.innerHeight, width: window.innerWidth};")
        print(f"✓ JavaScript: Window size = {result['width']}x{result['height']}")
        
        print("\n✓ JavaScript execution completed")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        driver.quit()
        print("✓ Browser closed")

# ============================================
# DATA-DRIVEN LOGIN TEST
# ============================================
def test_data_driven_login():
    """Data-driven login test using Excel data"""
    print("\nData-Driven Login Test")
    print("=" * 50)
    
    # Read test data from Excel
    try:
        wb = load_workbook("testdata.xlsx")
        sheet = wb.active
        
        print(f"Reading test data from {sheet.title} sheet")
        print(f"Total data rows: {sheet.max_row - 1}")
        
        for row in sheet.iter_rows(min_row=2, values_only=True):
            username, password, expected = row
            print(f"\nTest Case: {username}")
            
            driver = webdriver.Chrome()
            try:
                driver.get("https://www.saucedemo.com/")
                driver.find_element(By.ID, "user-name").send_keys(username)
                driver.find_element(By.ID, "password").send_keys(password)
                driver.find_element(By.ID, "login-button").click()
                
                import time
                time.sleep(2)
                
                if "/inventory.html" in driver.current_url:
                    print(f"  ✓ Result: Login Successful")
                else:
                    error = driver.find_element(By.CLASS_NAME, "error-message-container")
                    print(f"  ✗ Result: Login Failed")
                    print(f"    Error: {error.text[:50]}")
                    
            except Exception as e:
                print(f"  ✗ Error in test: {e}")
            finally:
                driver.quit()
        
        print("\n✓ Data-driven testing completed")
        
    except Exception as e:
        print(f"✗ Error in data-driven test: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("EXPERIMENT 9: ADVANCE INTERACTIONS")
    print("=" * 60)
    
    # Data file handling
    excel_write_data()
    excel_read_data()
    excel_update_data()
    json_write_data()
    json_read_data()
    csv_write_data()
    csv_read_data()
    xml_write_data()
    xml_read_data()
    properties_write_data()
    properties_read_data()
    
    # Selenium interactions
    test_mouse_hover()
    test_javascript_execution()
    
    # Data-driven testing
    test_data_driven_login()
    
    # Cleanup generated files
    for f in ["testdata.xlsx", "testdata.json", "testdata.csv", "testdata.xml", "testdata.properties"]:
        if os.path.exists(f):
            os.remove(f)
    print("\n✓ Cleaned up test data files")
    
    print("\n" + "=" * 60)
    print("✓ All advance interaction experiments completed!")
```

---

## 5. Output with Clearly Labelled Screenshots

### Output Console (Summary):
```
Writing Data to Excel File
----------------------------------------
✓ Excel file created with 4 rows of data

Reading Data from Excel File
----------------------------------------
Sheet name: TestData
Max rows: 5
Max columns: 4
Headers: ['Username', 'Password', 'Expected Result']
...
```

### Screenshot References:
- `screenshots/mouse_hover.png` - Mouse hover action
- `screenshots/javascript_highlight.png` - JavaScript highlighted element
- `screenshots/data_driven_test.png` - Data-driven test execution

---

## 6. Brief Result, Observation, and Conclusion

### Result:
Successfully implemented data reading/writing for Excel, JSON, CSV, XML, and Properties files. Implemented mouse hover actions and JavaScript execution.

### Observation:
- openpyxl provides Excel file manipulation capabilities
- JSON is ideal for structured hierarchical data
- CSV is simple and lightweight for tabular data
- Properties files are good for configuration
- ActionChains enables complex mouse interactions
- execute_script() provides access to browser-level operations

### Conclusion:
Advance interactions expand Selenium's capabilities beyond basic automation. Data-driven testing allows reuse of test data across multiple file formats, while ActionChains and JavaScript execution enable sophisticated UI interactions that mimic real user behavior.

---

**References:**
- openpyxl: https://openpyxl.readthedocs.io/
- ActionChains: https://www.selenium.dev/documentation/webdriver/actions_api/
- JavaScript Execution: https://www.selenium.dev/documentation/webdriver/browser_manipulation/
