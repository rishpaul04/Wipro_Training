"""
Experiment 9: Advance Interactions
Module: Automation with Selenium
Student: Rishita Paul
Date: September 8, 2026

Covers:
- Reading/Writing data from Excel, JSON, CSV, XML, Properties files
- Mouse hover actions
- JavaScript execution
- Data-driven testing
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import csv
import os
import time
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
        
        print(f"  Sheet name: {sheet.title}")
        print(f"  Max rows: {sheet.max_row}")
        print(f"  Max columns: {sheet.max_column}")
        
        headers = [cell.value for cell in sheet[1]]
        print(f"  Headers: {headers}")
        
        print("  Data:")
        for row in sheet.iter_rows(min_row=2, values_only=True):
            print(f"    {row}")
        
        print(f"  Cell B2: {sheet['B2'].value}")
        print(f"  Cell A3: {sheet['A3'].value}")
        
        return True
    except Exception as e:
        print(f"  ✗ Error reading Excel: {e}")
        return False

def excel_update_data():
    """Update data in Excel file"""
    print("\nUpdating Excel File")
    print("-" * 40)
    
    try:
        wb = load_workbook("testdata.xlsx")
        sheet = wb.active
        sheet['A2'] = "standard_user_updated"
        wb.save("testdata.xlsx")
        
        wb = load_workbook("testdata.xlsx")
        sheet = wb.active
        print(f"✓ Updated & verified: A2 = {sheet['A2'].value}")
    except Exception as e:
        print(f"  ✗ Error updating Excel: {e}")

# ============================================
# JSON HANDLING
# ============================================
def json_write_data():
    """Write data to JSON file"""
    print("\nWriting Data to JSON File")
    print("-" * 40)
    
    data = {
        "test_data": [
            {"username": "standard_user", "password": "secret_sauce", "expected": "login_success"},
            {"username": "locked_out_user", "password": "secret_sauce", "expected": "login_failed"}
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

def json_read_data():
    """Read data from JSON file"""
    print("\nReading Data from JSON File")
    print("-" * 40)
    
    try:
        with open("testdata.json", "r") as f:
            data = json.load(f)
        
        print(f"  Top-level keys: {list(data.keys())}")
        print(f"  Config: {data['test_config']}")
        print(f"  Test cases: {len(data['test_data'])}")
        
        for test in data['test_data']:
            print(f"    {test}")
        
        print(f"  Browser from config: {data['test_config']['browser']}")
        print(f"  First username: {data['test_data'][0]['username']}")
    except Exception as e:
        print(f"  ✗ Error reading JSON: {e}")

# ============================================
# CSV HANDLING
# ============================================
def csv_write_data():
    """Write data to CSV file"""
    print("\nWriting Data to CSV File")
    print("-" * 40)
    
    with open("testdata.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Test Case", "Username", "Password", "Expected Result"])
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
            headers = next(reader)
            print(f"  Headers: {headers}")
            print("  Data:")
            for row in reader:
                print(f"    {row}")
        print("  ✓ CSV reading completed")
    except Exception as e:
        print(f"  ✗ Error reading CSV: {e}")

# ============================================
# XML HANDLING
# ============================================
def xml_write_data():
    """Write data to XML file"""
    print("\nWriting Data to XML File")
    print("-" * 40)
    
    root = ET.Element("TestData")
    root.set("environment", "test")
    
    test_data = [
        {"id": "TC001", "username": "standard_user", "password": "secret_sauce"},
        {"id": "TC002", "username": "problem_user", "password": "secret_sauce"}
    ]
    
    for data in test_data:
        test_case = ET.SubElement(root, "TestCase")
        test_case.set("id", data["id"])
        ET.SubElement(test_case, "Username").text = data["username"]
        ET.SubElement(test_case, "Password").text = data["password"]
    
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
        
        print(f"  Root: {root.tag} (env={root.get('environment')})")
        for test_case in root.findall("TestCase"):
            test_id = test_case.get("id")
            username = test_case.find("Username").text
            password = test_case.find("Password").text
            print(f"    {test_id}: {username} / {password}")
        print("  ✓ XML reading completed")
    except Exception as e:
        print(f"  ✗ Error reading XML: {e}")

# ============================================
# PROPERTIES FILE HANDLING
# ============================================
def properties_write_data():
    """Write data to properties (INI) file"""
    print("\nWriting Data to Properties File")
    print("-" * 40)
    
    config = configparser.ConfigParser()
    config["browser"] = {"name": "chrome", "headless": "false", "timeout": "10"}
    config["application"] = {"url": "https://www.saucedemo.com/", "environment": "qa"}
    config["credentials"] = {"username": "standard_user", "password": "secret_sauce"}
    
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
        
        print(f"  Browser: {config['browser']['name']}")
        print(f"  Timeout: {config['browser']['timeout']}")
        print(f"  URL: {config['application']['url']}")
        print(f"  Environment: {config['application']['environment']}")
        print(f"  Username: {config['credentials']['username']}")
        print("  ✓ Properties file reading completed")
    except Exception as e:
        print(f"  ✗ Error reading properties: {e}")

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
        
        # Login to access inventory
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        time.sleep(2)
        
        # Hover over inventory item
        item = driver.find_element(By.CLASS_NAME, "inventory_item")
        actions = ActionChains(driver)
        actions.move_to_element(item).perform()
        print("✓ Mouse hovered over inventory item")
        
        # Hover over product image
        img = driver.find_element(By.CLASS_NAME, "inventory_item_img")
        actions.move_to_element(img).perform()
        print("✓ Mouse hovered over product image")
        
        # Hover with pause
        actions.move_to_element(item).pause(2).perform()
        print("✓ Hover with 2 second pause completed")
        
        print("✓ Mouse hover actions completed")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    finally:
        driver.quit()
        print("  ✓ Browser closed")

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
        
        # Get page title
        title = driver.execute_script("return document.title;")
        print(f"✓ JS: Page title = '{title}'")
        
        # Get page URL
        url = driver.execute_script("return window.location.href;")
        print(f"✓ JS: Page URL = '{url}'")
        
        # Scroll down
        driver.execute_script("window.scrollBy(0, 500);")
        print("✓ JS: Scrolled down 500px")
        
        # Change element style
        username = driver.find_element(By.ID, "user-name")
        driver.execute_script(
            "arguments[0].setAttribute('style', 'border: 2px solid red;')",
            username
        )
        print("✓ JS: Changed element border to red")
        
        # Get window size
        result = driver.execute_script(
            "return {height: window.innerHeight, width: window.innerWidth};"
        )
        print(f"✓ JS: Window size = {result['width']}x{result['height']}")
        
        print("✓ JavaScript execution completed")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    finally:
        driver.quit()
        print("  ✓ Browser closed")

# ============================================
# DATA-DRIVEN LOGIN TEST
# ============================================
def test_data_driven_login():
    """Data-driven login test using Excel data"""
    print("\nData-Driven Login Test (using Excel data)")
    print("=" * 50)
    
    try:
        wb = load_workbook("testdata.xlsx")
        sheet = wb.active
        
        print(f"  Reading from '{sheet.title}' sheet, {sheet.max_row - 1} data rows")
        
        for row in sheet.iter_rows(min_row=2, values_only=True):
            username, password, expected = row
            print(f"\n  Test Case: {username}")
            
            driver = webdriver.Chrome()
            try:
                driver.get("https://www.saucedemo.com/")
                driver.find_element(By.ID, "user-name").send_keys(username)
                driver.find_element(By.ID, "password").send_keys(password)
                driver.find_element(By.ID, "login-button").click()
                time.sleep(2)
                
                if "/inventory.html" in driver.current_url:
                    print(f"    ✓ Result: Login Successful (as expected: {expected})")
                else:
                    print(f"    ✗ Result: Login Failed (expected: {expected})")
            except Exception as e:
                print(f"    ✗ Error: {e}")
            finally:
                driver.quit()
        
        print("\n  ✓ Data-driven testing completed")
    except Exception as e:
        print(f"  ✗ Error: {e}")

def cleanup_test_files():
    """Remove generated test data files"""
    print("\nCleaning Up Test Data Files")
    print("-" * 40)
    
    files = ["testdata.xlsx", "testdata.json", "testdata.csv", "testdata.xml", "testdata.properties"]
    for f in files:
        if os.path.exists(f):
            os.remove(f)
            print(f"  ✓ Removed {f}")
    
    print("  ✓ Cleanup completed")

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
    
    # Cleanup
    cleanup_test_files()
    
    print("\n" + "=" * 60)
    print("✓ All advance interaction experiments completed!")
