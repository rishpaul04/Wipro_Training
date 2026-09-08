# Experiment 2: Selenium WebDriver Installation

**Module Name:** Automation with Selenium  
**Experiment Title:** Selenium WebDriver Introduction and Installation  
**Experiment Number:** 1.2  
**Date:** September 8, 2026  

---

## 1. Problem Statement

Set up a complete Selenium WebDriver development environment with Python 3, including installation of required packages, browser drivers, and verification of the setup.

---

## 2. Objective

- Install Python 3.x and required packages
- Install Selenium WebDriver using pip
- Download and configure browser drivers (ChromeDriver, GeckoDriver, EdgeDriver)
- Set up system path for drivers
- Verify installation by running tests in different browsers

---

## 3. Tools, Software, and Concepts Used

### Software Requirements:
- Python 3.x (latest version)
- pip (Python package manager)
- Web browsers: Google Chrome, Mozilla Firefox, Microsoft Edge
- Browser drivers: ChromeDriver, GeckoDriver, EdgeDriver
- IDE: VS Code or PyCharm

### Concepts Covered:
- Selenium 4 WebDriver architecture
- WebDriver installation with Python 3
- System path configuration for drivers
- Running tests in different browsers

---

## 4. Source Code / Implementation Steps

### Step 1: Install Python 3

```bash
# Check Python version
python --version

# Install pip if not installed
python -m ensurepip --upgrade
```

### Step 2: Install Selenium

```bash
# Install Selenium
pip install selenium

# Install specific version
pip install selenium==4.15.0

# Verify installation
pip show selenium
```

### Step 3: Download Browser Drivers

**ChromeDriver:**
1. Check Chrome version: `chrome://version/`
2. Download from: https://chromedriver.chromium.org/downloads
3. Extract and place in system path

**GeckoDriver (Firefox):**
1. Download from: https://github.com/mozilla/geckodriver/releases
2. Extract and place in system path

**EdgeDriver:**
1. Check Edge version: `edge://version/`
2. Download from: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
3. Extract and place in system path

### Step 4: System Path Configuration

**Windows:**
1. Right-click on "This PC" → Properties
2. Advanced system settings → Environment Variables
3. Edit Path variable and add driver location

**Alternative - Set in Python:**
```python
import os
os.environ["PATH"] += os.pathsep + r"C:\path\to\drivers"
```

### Step 5: Test Installation

```python
# test_installation.py
"""
Experiment 2: WebDriver Installation Verification
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService

def test_chrome():
    """Test Chrome WebDriver"""
    print("Testing Chrome WebDriver...")
    driver = webdriver.Chrome()
    driver.get("https://www.google.com")
    print(f"  Chrome - Title: {driver.title}")
    driver.quit()
    print("  ✓ Chrome test passed")

def test_firefox():
    """Test Firefox WebDriver"""
    print("Testing Firefox WebDriver...")
    driver = webdriver.Firefox()
    driver.get("https://www.google.com")
    print(f"  Firefox - Title: {driver.title}")
    driver.quit()
    print("  ✓ Firefox test passed")

def test_edge():
    """Test Edge WebDriver"""
    print("Testing Edge WebDriver...")
    driver = webdriver.Edge()
    driver.get("https://www.google.com")
    print(f"  Edge - Title: {driver.title}")
    driver.quit()
    print("  ✓ Edge test passed")

if __name__ == "__main__":
    print("=" * 50)
    print("Selenium WebDriver Installation Verification")
    print("=" * 50)
    
    try:
        test_chrome()
    except Exception as e:
        print(f"  ✗ Chrome test failed: {e}")
    
    try:
        test_firefox()
    except Exception as e:
        print(f"  ✗ Firefox test failed: {e}")
    
    try:
        test_edge()
    except Exception as e:
        print(f"  ✗ Edge test failed: {e}")
    
    print("=" * 50)
    print("Installation verification completed!")
```

---

## 5. Output with Clearly Labelled Screenshots

### Output Console:
```
==================================================
Selenium WebDriver Installation Verification
==================================================
Testing Chrome WebDriver...
  Chrome - Title: Google
  ✓ Chrome test passed
Testing Firefox WebDriver...
  Firefox - Title: Google
  ✓ Firefox test passed
Testing Edge WebDriver...
  Edge - Title: Google
  ✓ Edge test passed
==================================================
Installation verification completed!
```

### Screenshot References:
- `screenshots/python_installation.png` - Python version check
- `screenshots/selenium_install.png` - pip install selenium output
- `screenshots/driver_download.png` - Browser driver download pages
- `screenshots/path_configuration.png` - Environment variables setup
- `screenshots/chrome_test.png` - Chrome test execution
- `screenshots/firefox_test.png` - Firefox test execution
- `screenshots/edge_test.png` - Edge test execution

---

## 6. Brief Result, Observation, and Conclusion

### Result:
Successfully installed and configured Selenium WebDriver with Python 3. Verified installation by running tests in Chrome, Firefox, and Edge browsers.

### Observation:
- Selenium 4 provides seamless integration with Python 3
- Browser drivers are required for each browser type
- System path configuration is essential for driver detection
- All three browsers (Chrome, Firefox, Edge) work correctly with Selenium

### Conclusion:
The Selenium WebDriver development environment is now fully set up. The installation includes Python 3, Selenium package, and browser drivers for Chrome, Firefox, and Edge. This environment is ready for developing and executing automation test scripts.

---

**References:**
- Selenium Python Bindings: https://www.selenium.dev/selenium/docs/api/py/
- ChromeDriver: https://chromedriver.chromium.org/
- GeckoDriver: https://github.com/mozilla/geckodriver
