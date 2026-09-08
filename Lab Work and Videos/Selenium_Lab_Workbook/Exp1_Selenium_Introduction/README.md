# Experiment 1: Introduction to Selenium

**Module Name:** Automation with Selenium  
**Experiment Title:** Selenium Introduction and Different Flavors  
**Experiment Number:** 1.1  
**Date:** September 8, 2026  

---

## 1. Problem Statement

Understand the fundamentals of Selenium automation testing tool, its evolution, different components/flavors, and why it is preferred for web application testing.

---

## 2. Objective

- Understand what Selenium is and its purpose in software testing
- Learn why Selenium is preferred over other testing tools
- Identify different flavors/components of Selenium (IDE, RC, WebDriver, Grid)
- Understand the limitations of each Selenium component

---

## 3. Tools, Software, and Concepts Used

### Software Requirements:
- Python 3.x
- pip (Python package manager)
- Web browser (Chrome/Firefox/Edge)

### Concepts Covered:
- What is Selenium
- Why use Selenium for automation
- Selenium IDE - Record and playback tool
- Selenium RC (Remote Control) - Legacy testing tool
- Selenium WebDriver - Core automation API
- Selenium Grid - Parallel test execution

---

## 4. Source Code / Implementation Steps

### Step 1: Understanding Selenium Components

**Selenium IDE:**
- Browser extension for Firefox/Chrome
- Record and playback functionality
- No programming knowledge required
- Limited to simple test cases

**Selenium RC:**
- Server-based testing tool
- Supports multiple programming languages
- Requires server setup before execution
- Slower compared to WebDriver

**Selenium WebDriver:**
- Direct browser communication
- Faster execution
- Supports multiple languages (Python, Java, C#, etc.)
- Most widely used component

**Selenium Grid:**
- Parallel test execution
- Cross-browser testing
- Distributed test execution
- Requires hub-node setup

### Step 2: Installation Commands

```bash
# Install Selenium using pip
pip install selenium

# Verify installation
pip show selenium

# Check for updates
pip install --upgrade selenium
```

### Step 3: Create a simple test file

```python
# test_selenium_intro.py
"""
Experiment 1: Introduction to Selenium
Module: Automation with Selenium
"""

# Import Selenium WebDriver
from selenium import webdriver
from selenium.webdriver.common.by import By

def test_selenium_basic():
    """
    Basic test to demonstrate Selenium WebDriver initialization
    """
    print("Selenium Automation Test")
    print("=" * 40)
    
    # Initialize Chrome WebDriver
    driver = webdriver.Chrome()
    
    # Navigate to a website
    driver.get("https://www.google.com")
    
    # Get the title of the page
    title = driver.title
    print(f"Page Title: {title}")
    
    # Verify page loaded
    assert "Google" in title, "Google page not loaded"
    print("✓ Page loaded successfully")
    
    # Close the browser
    driver.quit()
    print("✓ Browser closed successfully")
    print("=" * 40)
    print("Test Completed Successfully!")

if __name__ == "__main__":
    test_selenium_basic()
```

---

## 5. Output with Clearly Labelled Screenshots

### Output Console:
```
Selenium Automation Test
========================================
Page Title: Google
✓ Page loaded successfully
✓ Browser closed successfully
========================================
Test Completed Successfully!
```

### Screenshot References:
- `screenshots/selenium_installation.png` - pip install output
- `screenshots/selenium_basic_test.png` - Test execution output
- `screenshots/selenium_components.png` - Diagram of Selenium components

---

## 6. Brief Result, Observation, and Conclusion

### Result:
Successfully installed and verified Selenium WebDriver. Created a basic test script that initializes the WebDriver, navigates to a website, and performs basic operations.

### Observation:
- Selenium WebDriver provides direct browser communication
- Installation is straightforward using pip
- Python integration is seamless with Selenium
- Basic operations include navigation, title retrieval, and element interaction

### Conclusion:
Selenium WebDriver is the most powerful and widely used component of the Selenium suite. It provides a programming interface to interact with web browsers directly, making it ideal for automation testing of web applications. The installation process is simple, and basic test creation requires minimal code.

---

**References:**
- Selenium Official Documentation: https://www.selenium.dev/documentation/
- Python Selenium Binding: https://pypi.org/project/selenium/
