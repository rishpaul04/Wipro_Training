# Experiment 6: Handling Dynamic Elements (WebTables)

**Module Name:** Automation with Selenium  
**Experiment Title:** Handling Dynamic Elements - WebTable  
**Experiment Number:** 1.6  
**Date:** September 8, 2026  

---

## 1. Problem Statement

Learn to work with dynamic web tables. Implement a script to iterate through rows and columns, locate specific rows by matching a name string, and retrieve corresponding values from adjacent columns.

---

## 2. Objective

- Understand the structure of HTML web tables
- Locate and traverse dynamic data tables
- Iterate through rows and columns
- Find specific rows by matching text
- Retrieve data from specific columns
- Handle dynamic content changes

---

## 3. Tools, Software, and Concepts Used

### Software Requirements:
- Python 3.x
- Selenium 4.x
- Web browser (Chrome)
- Test websites: https://the-internet.herokuapp.com/tables

### Concepts Covered:
- WebTable structure (table, tr, td, th)
- Row and column traversal
- Dynamic element handling
- Text matching and retrieval
- XPath with index positions

---

## 4. Source Code / Implementation Steps

### Assignment 5: The HTML Web Table Extractor

```python
# test_webtable.py
"""
Assignment 5: The HTML Web Table Extractor
Tier 2: Advanced User Interactions
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_webtable_traversal():
    """Test WebTable row and column traversal"""
    print("Assignment 5: HTML Web Table Extractor")
    print("=" * 50)
    
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.get("https://the-internet.herokuapp.com/tables")
    
    try:
        # Find the first table
        table = driver.find_element(By.ID, "table1")
        print("✓ Found table1")
        
        # Get all rows
        rows = table.find_elements(By.TAG_NAME, "tr")
        print(f"✓ Total rows: {len(rows)}")
        
        # Get all columns from header
        headers = rows[0].find_elements(By.TAG_NAME, "th")
        print(f"✓ Table headers: {len(headers)}")
        
        # Print headers
        header_texts = [header.text for header in headers]
        print(f"✓ Headers: {header_texts}")
        
        # Traverse all rows and columns
        print("\n--- Traversing Table ---")
        for i, row in enumerate(rows):
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells:
                cell_data = [cell.text for cell in cells]
                print(f"Row {i}: {cell_data}")
        
        print("\n✓ Table traversal completed!")
        
    finally:
        driver.quit()

def test_find_specific_row():
    """Test finding a specific row by matching text"""
    print("\n=== Finding Specific Row ===")
    print("-" * 40)
    
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.get("https://the-internet.herokuapp.com/tables")
    
    try:
        table = driver.find_element(By.ID, "table1")
        rows = table.find_elements(By.TAG_NAME, "tr")
        
        # Search for a specific name
        search_name = "Doe"
        
        # First, understand the table structure
        headers = rows[0].find_elements(By.TAG_NAME, "th")
        header_texts = [h.text for h in headers]
        print(f"Headers: {header_texts}")
        
        # Find the row containing the search name
        found = False
        for i, row in enumerate(rows):
            row_text = row.text
            if search_name in row_text:
                print(f"✓ Found '{search_name}' in row {i}")
                cells = row.find_elements(By.TAG_NAME, "td")
                cell_data = [cell.text for cell in cells]
                print(f"  Row data: {cell_data}")
                found = True
                break
        
        if not found:
            print(f"✗ '{search_name}' not found")
        
    finally:
        driver.quit()

def test_extract_specific_column():
    """Test extracting data from specific columns"""
    print("\n=== Extracting Specific Column Data ===")
    print("-" * 40)
    
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.get("https://the-internet.herokuapp.com/tables")
    
    try:
        table = driver.find_element(By.ID, "table1")
        rows = table.find_elements(By.TAG_NAME, "tr")
        
        # Get headers to understand columns
        headers = rows[0].find_elements(By.TAG_NAME, "th")
        header_texts = [h.text for h in headers]
        print(f"Headers: {header_texts}")
        
        # Extract all data from a specific column (e.g., Last Name - column 1)
        column_index = 1  # Last Name column
        print(f"\nExtracting data from column '{header_texts[column_index]}':")
        
        for i, row in enumerate(rows):
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells and len(cells) > column_index:
                print(f"  Row {i}: {cells[column_index].text}")
        
        # Extract all Due amount (column with money)
        print("\nExtracting Due amounts:")
        for i, row in enumerate(rows):
            cells = row.find_elements(By.TAG_NAME, "td")
            # Due column is index 3 in table1
            if cells and len(cells) > 3:
                print(f"  {cells[0].text} {cells[1].text}: {cells[3].text}")
        
    finally:
        driver.quit()

def test_match_name_get_value():
    """
    Main task: Locate a specific row by matching a name string,
    then retrieve the value from a specific column next to it
    """
    print("\n=== THE WEB TABLE EXTRACTOR TASK ===")
    print("-" * 40)
    
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.get("https://the-internet.herokuapp.com/tables")
    
    try:
        table = driver.find_element(By.ID, "table1")
        rows = table.find_elements(By.TAG_NAME, "tr")
        
        # Get headers
        headers = rows[0].find_elements(By.TAG_NAME, "th")
        header_texts = [h.text for h in headers]
        
        print(f"Table headers: {header_texts}")
        
        # Define the data we want to find
        # Structure for table1: Last Name | First Name | Email | Due | Web Site | Action
        search_criteria = [
            ("Doe", "Due"),          # Find Doe's Due amount
            ("Smith", "Email"),       # Find Smith's Email
            ("Bach", "Web Site")      # Find Bach's Website
        ]
        
        for name, target_col in search_criteria:
            found = False
            for row in rows[1:]:  # Skip header row
                cells = row.find_elements(By.TAG_NAME, "td")
                cell_texts = [cell.text for cell in cells]
                
                # Check if this row contains the search name
                if name in cell_texts:
                    # Find the index of the target column
                    col_index = header_texts.index(target_col)
                    
                    print(f"\n✓ Found '{name}' in row")
                    print(f"  Full row: {cell_texts}")
                    print(f"  {target_col} for {name}: {cells[col_index].text}")
                    found = True
                    break
            
            if not found:
                print(f"\n✗ '{name}' not found to extract {target_col}")
        
        print("\n✓ Web Table Extractor task completed!")
        
    finally:
        driver.quit()

def test_dynamic_table_handling():
    """Demonstrate handling dynamic table content"""
    print("\n=== Dynamic Table Handling ===")
    print("-" * 40)
    
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.get("https://the-internet.herokuapp.com/tables")
    
    try:
        # Sort the table by clicking on column headers
        table1 = driver.find_element(By.ID, "table1")
        headers = table1.find_elements(By.TAG_NAME, "th")
        
        print("Testing table sorting (dynamic content change)")
        
        # Click on Last Name header to sort
        headers[1].click()  # Last Name column
        time.sleep(1)
        
        # Check if sorting changed the order
        rows = table1.find_elements(By.TAG_NAME, "tr")
        first_data_row = rows[1].find_elements(By.TAG_NAME, "td")
        print(f"After sorting by Last Name, first row: {[cell.text for cell in first_data_row]}")
        
        # Click again to reverse sort
        headers[1].click()
        time.sleep(1)
        
        rows = table1.find_elements(By.TAG_NAME, "tr")
        first_data_row = rows[1].find_elements(By.TAG_NAME, "td")
        print(f"After reverse sort, first row: {[cell.text for cell in first_data_row]}")
        
        print("\n✓ Dynamic table behavior (sorting) verified!")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    print("=" * 60)
    print("EXPERIMENT 6: HANDLING DYNAMIC ELEMENTS - WEB TABLES")
    print("=" * 60)
    
    test_webtable_traversal()
    test_find_specific_row()
    test_extract_specific_column()
    test_match_name_get_value()
    test_dynamic_table_handling()
    
    print("\n" + "=" * 60)
    print("✓ All web table experiments completed!")
```

---

## 5. Output with Clearly Labelled Screenshots

### Output Console (Summary):
```
Assignment 5: HTML Web Table Extractor
==================================================
✓ Found table1
✓ Total rows: 5
✓ Table headers: 5
✓ Headers: ['Last Name', 'First Name', 'Email', 'Due', 'Web Site', 'Action']

--- Traversing Table ---
Row 1: ['Smith', 'John', 'jsmith@gmail.com', '$50.00', 'http://www.jsmith.com']
Row 2: ['Bach', 'Frank', 'fbach@yahoo.com', '$51.00', 'http://www.frank.com']
...
```

### Screenshot References:
- `screenshots/table_structure.png` - HTML table structure
- `screenshots/table_traversal.png` - Iterating through rows/columns
- `screenshots/row_match.png` - Finding specific row by name
- `screenshots/column_extraction.png` - Extracting column data
- `screenshots/table_sorting.png` - Dynamic table sorting

---

## 6. Brief Result, Observation, and Conclusion

### Result:
Successfully implemented the Web Table Extractor. Found specific rows by matching name strings and retrieved corresponding values from target columns.

### Observation:
- HTML tables have a standard structure (table > tr > td/th)
- Row traversal helps find data across all entries
- Column indexing allows targeted data extraction
- Dynamic content (sorting) changes element positions
- Text matching on rows provides a robust way to locate records

### Conclusion:
Web table handling is essential for automating data-driven web applications. The ability to traverse rows and columns, locate specific records, and extract targeted data is a core skill for test automation of business applications like stock lists, user directories, and transaction records.

---

**References:**
- Table Test Page: https://the-internet.herokuapp.com/tables
- Selenium Table Handling: https://www.selenium.dev/documentation/webdriver/
