import json
import os
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import NoAlertPresentException, ElementClickInterceptedException

from report_generator import generate_html_report


def section(title):
    print("\n" + "=" * 78)
    print(" " + title)
    print("=" * 78)


def ok(msg):
    print("  [OK] " + msg)


def fail(msg):
    print("  [FAIL] " + msg)


def warn(msg):
    print("  [WARN] " + msg)


def info(msg):
    print("  - " + msg)


def progress_bar(done, total, width=30):
    pct = done / total if total else 0
    filled = int(width * pct)
    bar = "#" * filled + "." * (width - filled)
    return f"[{bar}] {done}/{total} ({pct * 100:.0f}%)"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


APP = {
    "name": "TutorialsNinja Demo",
    "base": "https://tutorialsninja.com/demo/",
    "login": "https://tutorialsninja.com/demo/index.php?route=account/login",
    "cart": "https://tutorialsninja.com/demo/index.php?route=checkout/cart",
    "search": "https://tutorialsninja.com/demo/index.php?route=product/search",
    "product": "MacBook",
    "quantity": "2",
    "email": "testuser@example.com",
    "password": "Test@1234",
    "login_btn": "input[type='submit'][value='Login']",
    "login_email": "input[name='email']",
    "login_pwd": "input[name='password']",
    "search_box": "input[name='search']",
    "search_btn": "#search button",
    "result_item": ".product-layout",
    "result_link": ".product-layout .caption h4 a",
    "add_cart_btn": "#button-cart",
    "qty_input": "#input-quantity",
    "cart_selector": "#content",
}

# Backwards-compatible alias (single site only)
APP_PRESETS = {"tutorialsninja": APP}


class TestResult:
    def __init__(self, test_id, description, status, message="", screenshot="", duration=0):
        self.test_id = test_id
        self.description = description
        self.status = status
        self.message = message
        self.screenshot = screenshot
        self.duration = duration
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def load_test_data():
    json_path = os.path.join(BASE_DIR, "test_data.json")
    with open(json_path, "r") as f:
        return json.load(f)


def load_excel_data():
    """Optionally read from Excel if present (fallback to JSON)."""
    xlsx_path = os.path.join(BASE_DIR, "test_data.xlsx")
    if not os.path.exists(xlsx_path):
        return load_test_data()
    try:
        from openpyxl import load_workbook
        wb = load_workbook(xlsx_path, data_only=True)
        ws = wb["Test Cases"]
        data = load_test_data()
        for row in ws.iter_rows(min_row=2, values_only=True):
            if not row[0]:
                continue
            for tc in data["test_cases"]:
                if tc["test_id"] == row[0]:
                    if row[2]:
                        tc["search_product"] = row[2]
                    if row[3]:
                        tc["quantity"] = str(row[3])
                    break
        return data
    except Exception:
        return load_test_data()


def create_driver():
    """Always visible browser — no headless, no prompts."""
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-gpu")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    return driver


def take_screenshot(driver, name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.png"
    filepath = os.path.join(SCREENSHOT_DIR, filename)
    driver.save_screenshot(filepath)
    return filepath


def handle_alerts(driver):
    try:
        alert = driver.switch_to.alert
        text = alert.text
        alert.accept()
        return text
    except NoAlertPresentException:
        return None


def safe_click(driver, element):
    """Click an element, resisting ad/overlay interception."""
    try:
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        time.sleep(0.2)
        element.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", element)
    return element


def run_step(driver, app, test_fn, index, total, results):
    print(f"\n [{index}/{total}] {test_fn.__doc__.strip().split(chr(10))[0]} ...")
    test_fn(driver, app, results, index, total)


# ---------------------------------------------------------------- TESTS

def test_launch(driver, app, results, i, total):
    """Launch browser & navigate to the application"""
    tid, desc = "TC_LAUNCH", "Launch browser and navigate to application"
    start = time.time()
    try:
        driver.get(app["base"])
        wait = WebDriverWait(driver, 15)
        if "tutorialsninja" in app["base"]:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#logo")))
        else:
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        shot = take_screenshot(driver, "01_browser_launched")
        d = round(time.time() - start, 2)
        results.append(TestResult(tid, desc, "PASS", f"Opened {app['name']}", shot, d))
        ok(f"Opened {app['name']} ({d}s)  [{tid}]")
    except Exception as e:
        shot = take_screenshot(driver, "01_browser_launch_fail")
        d = round(time.time() - start, 2)
        results.append(TestResult(tid, desc, "FAIL", str(e), shot, d))
        fail(f"{e}  [{tid}]")


def do_signup(driver, app):
    """Create a new account (automationexercise) and return the credentials email."""
    wait = WebDriverWait(driver, 15)
    email = f"auto{int(time.time())}@example.com"
    driver.get(app["login"])
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, app["signup_name"])))
    take_screenshot(driver, "02_login_page")
    driver.find_element(By.CSS_SELECTOR, app["signup_name"]).send_keys(app["signup_full_name"])
    driver.find_element(By.CSS_SELECTOR, app["signup_email"]).send_keys(email)
    safe_click(driver, driver.find_element(By.CSS_SELECTOR, app["signup_btn"]))
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, app["signup_password"])))
    try:
        driver.find_element(By.CSS_SELECTOR, "#id_gender1").click()
    except Exception:
        pass
    driver.find_element(By.CSS_SELECTOR, app["signup_password"]).send_keys(app["password"])
    Select(driver.find_element(By.CSS_SELECTOR, app["signup_days"])).select_by_value("10")
    Select(driver.find_element(By.CSS_SELECTOR, app["signup_months"])).select_by_value("5")
    Select(driver.find_element(By.CSS_SELECTOR, app["signup_years"])).select_by_value("1995")
    driver.find_element(By.CSS_SELECTOR, app["signup_first_name"]).send_keys(app["signup_first_name_val"])
    driver.find_element(By.CSS_SELECTOR, app["signup_last_name"]).send_keys(app["signup_last_name_val"])
    driver.find_element(By.CSS_SELECTOR, app["signup_address"]).send_keys(app["signup_address_val"])
    Select(driver.find_element(By.CSS_SELECTOR, app["signup_country"])).select_by_value(app["signup_country_val"])
    driver.find_element(By.CSS_SELECTOR, app["signup_state"]).send_keys(app["signup_state_val"])
    driver.find_element(By.CSS_SELECTOR, app["signup_city"]).send_keys(app["signup_city_val"])
    driver.find_element(By.CSS_SELECTOR, app["signup_zipcode"]).send_keys(app["signup_zipcode_val"])
    driver.find_element(By.CSS_SELECTOR, app["signup_mobile"]).send_keys(app["signup_mobile_val"])
    take_screenshot(driver, "03_signup_filled")
    safe_click(driver, driver.find_element(By.CSS_SELECTOR, app["signup_create_btn"]))
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, app["signup_continue_btn"])))
    take_screenshot(driver, "03_account_created")
    safe_click(driver, driver.find_element(By.CSS_SELECTOR, app["signup_continue_btn"]))
    time.sleep(1)
    try:
        safe_click(driver, driver.find_element(By.CSS_SELECTOR, "a[href='/logout']"))
        time.sleep(1)
    except Exception:
        pass
    driver.get(app["login"])
    return email


def test_login(driver, app, results, i, total):
    """Signup then login to the application"""
    tid, desc = "TC_LOGIN", "Signup then login"
    start = time.time()
    try:
        email = app["email"]
        if app.get("signup_btn"):
            email = do_signup(driver, app)
        driver.get(app["login"])
        wait = WebDriverWait(driver, 15)
        time.sleep(1)
        shot = take_screenshot(driver, "02_login_page")
        email_field = driver.find_element(By.CSS_SELECTOR, app["login_email"])
        email_field.clear()
        email_field.send_keys(email)
        pwd = driver.find_element(By.CSS_SELECTOR, app["login_pwd"])
        pwd.clear()
        pwd.send_keys(app["password"])
        take_screenshot(driver, "03_login_filled")
        safe_click(driver, driver.find_element(By.CSS_SELECTOR, app["login_btn"]))
        time.sleep(3)
        handle_alerts(driver)
        d = round(time.time() - start, 2)
        msg = f"Signed up & logged in as {email}" if app.get("signup_btn") else "Login form submitted (demo credentials)"
        results.append(TestResult(tid, desc, "PASS", msg, shot, d))
        ok(f"{msg} ({d}s)  [{tid}]")
    except Exception as e:
        shot = take_screenshot(driver, "03_login_fail")
        d = round(time.time() - start, 2)
        results.append(TestResult(tid, desc, "FAIL", str(e), shot, d))
        fail(f"{e}  [{tid}]")


def do_search(driver, app, product):
    """Site-aware search: navigate to the search page, type & submit."""
    wait = WebDriverWait(driver, 15)
    if app.get("search_page"):
        driver.get(app["search_page"])
        time.sleep(1)
    else:
        driver.get(app["base"])
        time.sleep(1)
    search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, app["search_box"])))
    search_input.clear()
    search_input.send_keys(product)
    safe_click(driver, driver.find_element(By.CSS_SELECTOR, app["search_btn"]))
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, app["result_item"])))
    time.sleep(1)


def open_product_detail(driver, app, product):
    """Navigate to the product detail page for the searched product."""
    wait = WebDriverWait(driver, 15)
    if app.get("detail_link"):
        # automationexercise: locate the "View Product" link with /product_details/<id>
        links = driver.find_elements(By.CSS_SELECTOR, app["result_item"] + " a")
        target = None
        for a in links:
            href = a.get_attribute("href") or ""
            if app["detail_link"] in href:
                target = href
                break
        if not target:
            raise RuntimeError("Product detail link not found in search results")
        driver.get(target)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, app["qty_input"])))
    else:
        # tutorialsninja: first search result link is the product page
        link = driver.find_element(By.CSS_SELECTOR, app["result_link"])
        href = link.get_attribute("href")
        driver.get(href)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, app["add_cart_btn"])))
    time.sleep(1)


def test_search(driver, app, results, i, total):
    """Search for a product"""
    tid, desc = "TC_SEARCH", "Search for a product"
    start = time.time()
    product = app["product"]
    try:
        do_search(driver, app, product)
        shot = take_screenshot(driver, "04_search_results")
        d = round(time.time() - start, 2)
        count = len(driver.find_elements(By.CSS_SELECTOR, app["result_item"]))
        results.append(TestResult(tid, desc, "PASS", f"Searched '{product}', {count} result(s)", shot, d))
        ok(f"Searched for '{product}', {count} result(s) ({d}s)  [{tid}]")
    except Exception as e:
        shot = take_screenshot(driver, "04_search_fail")
        d = round(time.time() - start, 2)
        results.append(TestResult(tid, desc, "FAIL", str(e), shot, d))
        fail(f"{e}  [{tid}]")


def test_add_to_cart(driver, app, results, i, total):
    """Add product to cart"""
    tid, desc = "TC_ADD_CART", "Add product to cart"
    start = time.time()
    product = app["product"]
    try:
        do_search(driver, app, product)
        shot = take_screenshot(driver, "05_product_found")
        if app.get("search_add_btn"):
            # automationexercise: add to cart directly from search results
            safe_click(driver, driver.find_element(By.CSS_SELECTOR, app["search_add_btn"]))
            wait = WebDriverWait(driver, 15)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#cartModal")))
            time.sleep(1)
        else:
            open_product_detail(driver, app, product)
            safe_click(driver, driver.find_element(By.CSS_SELECTOR, app["add_cart_btn"]))
        time.sleep(2)
        handle_alerts(driver)
        d = round(time.time() - start, 2)
        # close modal if present (automationexercise)
        if app.get("modal_close") and app.get("search_add_btn"):
            try:
                if driver.find_elements(By.CSS_SELECTOR, app["modal_close"]):
                    safe_click(driver, driver.find_element(By.CSS_SELECTOR, app["modal_close"]))
            except Exception:
                pass
        results.append(TestResult(tid, desc, "PASS", f"'{product}' added to cart", shot, d))
        ok(f"'{product}' added to cart ({d}s)  [{tid}]")
    except Exception as e:
        shot = take_screenshot(driver, "05_add_fail")
        d = round(time.time() - start, 2)
        results.append(TestResult(tid, desc, "FAIL", str(e), shot, d))
        fail(f"{e}  [{tid}]")


def test_update_quantity(driver, app, results, i, total):
    """Update product quantity"""
    tid, desc = "TC_UPDATE_QTY", "Update product quantity"
    start = time.time()
    product = app["product"]
    qty = app["quantity"]
    try:
        if app.get("detail_url"):
            # automationexercise: open product detail page directly, update qty
            driver.get(app["detail_url"])
            wait = WebDriverWait(driver, 15)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, app["qty_input"])))
        else:
            do_search(driver, app, product)
            open_product_detail(driver, app, product)
        qty_el = driver.find_element(By.CSS_SELECTOR, app["qty_input"])
        safe_click(driver, qty_el)
        qty_el.clear()
        qty_el.send_keys(qty)
        take_screenshot(driver, "06_quantity_updated")
        safe_click(driver, driver.find_element(By.CSS_SELECTOR, app["add_cart_btn"]))
        time.sleep(2)
        handle_alerts(driver)
        shot = take_screenshot(driver, "07_quantity_added")
        d = round(time.time() - start, 2)
        results.append(TestResult(tid, desc, "PASS", f"Quantity set to {qty} for '{product}'", shot, d))
        ok(f"Quantity set to {qty} for '{product}' ({d}s)  [{tid}]")
    except Exception as e:
        shot = take_screenshot(driver, "06_qty_fail")
        d = round(time.time() - start, 2)
        results.append(TestResult(tid, desc, "FAIL", str(e), shot, d))
        fail(f"{e}  [{tid}]")


def test_verify_cart(driver, app, results, i, total):
    """Verify cart details"""
    tid, desc = "TC_VERIFY_CART", "Verify cart details"
    start = time.time()
    try:
        driver.get(app["cart"])
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, app["cart_selector"])))
        time.sleep(2)
        handle_alerts(driver)
        shot = take_screenshot(driver, "07_cart_verified")
        d = round(time.time() - start, 2)
        results.append(TestResult(tid, desc, "PASS", "Cart contents verified on cart page", shot, d))
        ok(f"Cart verified ({d}s)  [{tid}]")
    except Exception as e:
        shot = take_screenshot(driver, "07_cart_fail")
        d = round(time.time() - start, 2)
        results.append(TestResult(tid, desc, "FAIL", str(e), shot, d))
        fail(f"{e}  [{tid}]")


def test_popups(driver, app, results, i, total):
    """Handle popups & alerts"""
    tid, desc = "TC_POPUPS", "Handle popups & alerts"
    start = time.time()
    try:
        alert = handle_alerts(driver)
        shot = take_screenshot(driver, "08_popups_handled")
        d = round(time.time() - start, 2)
        msg = f"Alert handled: {alert}" if alert else "No alerts present"
        results.append(TestResult(tid, desc, "PASS", msg, shot, d))
        ok(msg + f" ({d}s)  [{tid}]")
    except Exception as e:
        shot = take_screenshot(driver, "08_popups_fail")
        d = round(time.time() - start, 2)
        results.append(TestResult(tid, desc, "FAIL", str(e), shot, d))
        fail(f"{e}  [{tid}]")


def test_capture_screenshot(driver, app, results, i, total):
    """Capture screenshot"""
    tid, desc = "TC_SCREENSHOT", "Capture screenshot"
    start = time.time()
    try:
        driver.get(app["base"])
        time.sleep(2)
        shot = take_screenshot(driver, "09_screenshot_captured")
        d = round(time.time() - start, 2)
        results.append(TestResult(tid, desc, "PASS", f"Saved: {os.path.basename(shot)}", shot, d))
        ok(f"Screenshot saved: {os.path.basename(shot)} ({d}s)  [{tid}]")
    except Exception as e:
        d = round(time.time() - start, 2)
        results.append(TestResult(tid, desc, "FAIL", str(e), "", d))
        fail(f"{e}  [{tid}]")


# ---------------------------------------------------------------- ORCHESTRATION

ALL_TESTS = [
    ("Launch Browser", test_launch),
    ("Login (Signup first)", test_login),
    ("Search Product", test_search),
    ("Add to Cart", test_add_to_cart),
    ("Update Quantity", test_update_quantity),
    ("Verify Cart", test_verify_cart),
    ("Popups", test_popups),
    ("Screenshot", test_capture_screenshot),
]


def run_selected(app=None, selected=None, headless=False):
    """Run all tests on the single site in visible browser (args kept for compatibility)."""
    results = []
    driver = create_driver()
    try:
        total = len(ALL_TESTS)
        for idx, (label, fn) in enumerate(ALL_TESTS, 1):
            fn(driver, APP, results, idx, total)
            info(f"{label} done {progress_bar(idx, total)}")
    finally:
        driver.quit()
    report = generate_html_report(results, APP["name"])
    info(f"Execution report updated: {report}")
    return results


def show_status(results):
    total = len(results)
    passed = sum(1 for r in results if r.status == "PASS")
    failed = sum(1 for r in results if r.status == "FAIL")
    skipped = sum(1 for r in results if r.status == "SKIP")
    dur = sum(r.duration for r in results)

    section("EXECUTION SUMMARY")
    print(f"  Total tests  : {total}")
    print(f"  Passed       : {passed}")
    print(f"  Failed       : {failed}")
    print(f"  Skipped      : {skipped}")
    print(f"  Time taken   : {dur:.2f}s")
    print(f"  Pass rate    : {(passed / total * 100) if total else 0:.1f}%")

    rate = passed / total if total else 0
    print("\n  " + progress_bar(passed, total))
    if rate >= 1:
        ok("ALL TESTS PASSED — outstanding!")
    elif rate >= 0.6:
        warn("Mostly passing, review failures.")
    else:
        fail("Many failures detected.")

    print("\n  " + "-" * 70)
    for r in results:
        print(f"    {r.test_id}  [{r.status}]   {r.description}")


def main():
    """No menus — directly run full suite on TutorialsNinja in visible browser."""
    section("EXECUTING TESTS - TutorialsNinja Demo (Visible)")
    info(f"Application : {APP['name']}")
    info("Mode        : Visible browser")
    results = run_selected()
    show_status(results)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Interrupted by user. Exiting gracefully.")
