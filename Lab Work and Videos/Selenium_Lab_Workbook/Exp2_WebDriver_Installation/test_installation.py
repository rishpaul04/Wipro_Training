"""
Experiment 2: Selenium WebDriver Installation and Setup
Module: Automation with Selenium
Student: Rishita Paul
Date: September 8, 2026
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
import sys
import os

def check_python_version():
    """Check Python version"""
    print("Python Version Check")
    print("-" * 30)
    print(f"Python Version: {sys.version}")
    print(f"Python Path: {sys.executable}")
    print()

def check_selenium_version():
    """Check Selenium version"""
    print("Selenium Version Check")
    print("-" * 30)
    try:
        import selenium
        print(f"Selenium Version: {selenium.__version__}")
    except ImportError:
        print("Selenium not installed!")
    print()

def test_chrome_driver():
    """Test Chrome WebDriver"""
    print("Chrome WebDriver Test")
    print("-" * 30)
    try:
        driver = webdriver.Chrome()
        driver.get("https://www.google.com")
        
        # Get page details
        title = driver.title
        url = driver.current_url
        
        print(f"  Title: {title}")
        print(f"  URL: {url}")
        
        # Perform a simple search
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys("Selenium WebDriver")
        search_box.submit()
        
        import time
        time.sleep(2)
        
        print(f"  Search Results Title: {driver.title}")
        print("  ✓ Chrome test passed!")
        
        driver.quit()
        return True
        
    except Exception as e:
        print(f"  ✗ Chrome test failed: {e}")
        return False

def test_firefox_driver():
    """Test Firefox WebDriver"""
    print("\nFirefox WebDriver Test")
    print("-" * 30)
    try:
        driver = webdriver.Firefox()
        driver.get("https://www.google.com")
        
        title = driver.title
        url = driver.current_url
        
        print(f"  Title: {title}")
        print(f"  URL: {url}")
        
        driver.quit()
        print("  ✓ Firefox test passed!")
        return True
        
    except Exception as e:
        print(f"  ✗ Firefox test failed: {e}")
        return False

def test_edge_driver():
    """Test Edge WebDriver"""
    print("\nEdge WebDriver Test")
    print("-" * 30)
    try:
        driver = webdriver.Edge()
        driver.get("https://www.google.com")
        
        title = driver.title
        url = driver.current_url
        
        print(f"  Title: {title}")
        print(f"  URL: {url}")
        
        driver.quit()
        print("  ✓ Edge test passed!")
        return True
        
    except Exception as e:
        print(f"  ✗ Edge test failed: {e}")
        return False

def test_driver_paths():
    """Check if driver paths are accessible"""
    print("\nDriver Path Check")
    print("-" * 30)
    
    # Common driver locations
    chrome_paths = [
        r"C:\chromedriver\chromedriver.exe",
        r"C:\Program Files\chromedriver\chromedriver.exe",
        os.path.expanduser(r"~\chromedriver\chromedriver.exe")
    ]
    
    firefox_paths = [
        r"C:\geckodriver\geckodriver.exe",
        r"C:\Program Files\geckodriver\geckodriver.exe",
        os.path.expanduser(r"~\geckodriver\geckodriver.exe")
    ]
    
    edge_paths = [
        r"C:\edgedriver\msedgedriver.exe",
        r"C:\Program Files\edgedriver\msedgedriver.exe",
        os.path.expanduser(r"~\edgedriver\msedgedriver.exe")
    ]
    
    print("ChromeDriver:")
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"  ✓ Found: {path}")
        else:
            print(f"  ✗ Not found: {path}")
    
    print("\nGeckoDriver:")
    for path in firefox_paths:
        if os.path.exists(path):
            print(f"  ✓ Found: {path}")
        else:
            print(f"  ✗ Not found: {path}")
    
    print("\nEdgeDriver:")
    for path in edge_paths:
        if os.path.exists(path):
            print(f"  ✓ Found: {path}")
        else:
            print(f"  ✗ Not found: {path}")

if __name__ == "__main__":
    print("=" * 60)
    print("SELENIUM WEBDRIVER INSTALLATION VERIFICATION")
    print("=" * 60)
    print()
    
    # Check versions
    check_python_version()
    check_selenium_version()
    
    # Check driver paths
    test_driver_paths()
    
    print("\n" + "=" * 60)
    print("BROWSER DRIVER TESTS")
    print("=" * 60)
    
    # Test each browser
    results = {}
    results['Chrome'] = test_chrome_driver()
    results['Firefox'] = test_firefox_driver()
    results['Edge'] = test_edge_driver()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    for browser, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{browser}: {status}")
    
    print("=" * 60)
    print("Installation verification completed!")
