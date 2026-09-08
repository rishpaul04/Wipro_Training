"""
Experiment 6: Handling Dynamic Elements - Web Tables
Module: Automation with Selenium
Student: Rishita Paul
Date: September 8, 2026

Assignment 5: The HTML Web Table Extractor
Tier 2: Advanced User Interactions
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
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
        
        # Get headers
        headers = rows[0].find_elements(By.TAG_NAME, "th")
        header_texts = [header.text for header in headers]
        print(f"✓ Headers: {header_texts}")
        
        # Traverse all rows and columns
        print("\n--- Traversing Table ---")
        for i, row in enumerate(rows):
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells:
                cell_data = [cell.text for cell in cells]
                print(f"  Row {i}: {cell_data}")
        
        print("\n✓ Table traversal completed!")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        driver.quit()
        print("✓ Browser closed")

def test_match_name_get_value():
    """
    Main task: Locate a specific row by matching a name string,
    then retrieve the value from a specific column next to it
    """
    print("\n=== THE WEB TABLE EXTRACTOR TASK ===")
    print("-" * 50)
    
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
        
        # Search criteria: (name to find, column to extract)
        search_criteria = [
            ("Smith", "Due"),          # Find Smith's Due amount
            ("Bach", "Email"),          # Find Bach's Email
            ("Conway", "Web Site"),     # Find Conway's Website
            ("Doe", "Due")              # Find Doe's Due amount
        ]
        
        print("\nResults:")
        print("-" * 50)
        
        for name, target_col in search_criteria:
            found = False
            for row in rows[1:]:  # Skip header row
                cells = row.find_elements(By.TAG_NAME, "td")
                cell_texts = [cell.text for cell in cells]
                
                # Check if this row contains the search name
                if name in cell_texts:
                    # Find the index of the target column
                    col_index = header_texts.index(target_col)
                    
                    # Get the value from the target column
                    target_value = cells[col_index].text if col_index < len(cells) else "N/A"
                    
                    print(f"  '{name}' → {target_col}: {target_value}")
                    found = True
                    break
            
            if not found:
                print(f"  '{name}' → {target_col}: NOT FOUND")
        
        print("-" * 50)
        print("\n✓ Web Table Extractor task completed!")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        driver.quit()
        print("✓ Browser closed")

def test_find_specific_row_details():
    """Get full details of a specific person from the table"""
    print("\n=== Get Full Details of a Person ===")
    print("-" * 50)
    
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.get("https://the-internet.herokuapp.com/tables")
    
    try:
        table = driver.find_element(By.ID, "table1")
        rows = table.find_elements(By.TAG_NAME, "tr")
        headers = rows[0].find_elements(By.TAG_NAME, "th")
        header_texts = [h.text for h in headers]
        
        # Find Frank Bach's full record
        search_name = "Bach"
        
        for row in rows[1:]:
            cells = row.find_elements(By.TAG_NAME, "td")
            cell_texts = [cell.text for cell in cells]
            
            if search_name in cell_texts:
                print(f"\nFound complete record for '{search_name}':")
                for header, value in zip(header_texts, cell_texts):
                    print(f"  {header}: {value}")
                break
        
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        driver.quit()

def test_dynamic_table_sorting():
    """Demonstrate handling dynamic table content (sorting)"""
    print("\n=== Dynamic Table Behavior (Sorting) ===")
    print("-" * 50)
    
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.get("https://the-internet.herokuapp.com/tables")
    
    try:
        table = driver.find_element(By.ID, "table1")
        headers = table.find_elements(By.TAG_NAME, "th")
        
        print("Table headers (clickable for sorting):")
        for i, header in enumerate(headers):
            print(f"  {i}: {header.text}")
        
        # Click on Last Name header to sort ascending
        print("\n✓ Clicking 'Last Name' header to sort...")
        headers[1].click()
        time.sleep(1)
        
        # Check new first row
        rows = table.find_elements(By.TAG_NAME, "tr")
        first_row = rows[1].find_elements(By.TAG_NAME, "td")
        print(f"  After ascending sort, first row: {[c.text for c in first_row]}")
        
        # Click again to sort descending
        print("\n✓ Clicking 'Last Name' header again for reverse sort...")
        headers[1].click()
        time.sleep(1)
        
        rows = table.find_elements(By.TAG_NAME, "tr")
        first_row = rows[1].find_elements(By.TAG_NAME, "td")
        print(f"  After descending sort, first row: {[c.text for c in first_row]}")
        
        print("\n✓ Dynamic behavior (sorting) demonstrated!")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        driver.quit()

def test_get_all_due_amounts():
    """Extract all Due amounts and compute total"""
    print("\n=== Extract All Due Amounts ===")
    print("-" * 50)
    
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.get("https://the-internet.herokuapp.com/tables")
    
    try:
        table = driver.find_element(By.ID, "table1")
        rows = table.find_elements(By.TAG_NAME, "tr")
        headers = rows[0].find_elements(By.TAG_NAME, "th")
        header_texts = [h.text for h in headers]
        
        # Find the Due column index
        due_col = header_texts.index("Due") if "Due" in header_texts else -1
        
        if due_col >= 0:
            print(f"Found '{header_texts[due_col]}' column at index {due_col}")
            
            total = 0.0
            amounts = []
            
            for row in rows[1:]:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) > due_col:
                    amount_text = cells[due_col].text
                    # Store raw text for comparison
                    amounts.append(amount_text)
            
            print(f"  Due amounts: {amounts}")
            print(f"  Total records: {len(amounts)}")
            print("\n✓ All due amounts extracted successfully!")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    print("=" * 60)
    print("EXPERIMENT 6: HANDLING DYNAMIC ELEMENTS - WEB TABLES")
    print("=" * 60)
    
    test_webtable_traversal()
    test_match_name_get_value()
    test_find_specific_row_details()
    test_get_all_due_amounts()
    test_dynamic_table_sorting()
    
    print("\n" + "=" * 60)
    print("✓ All web table experiments completed!")
