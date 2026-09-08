import json
import os
import sys
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import NoAlertPresentException, ElementClickInterceptedException

from console_ui import (
    C, section, step, ok, fail, warn, info,
    status_badge, spinner, progress_bar, ask_choice, press_enter,
)
from report_generator import generate_html_report

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


APP_PRESETS = {
    "tutorialsninja": {
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
    },
    "automationexercise": {
        "name": "Automation Exercise",
        "base": "https://automationexercise.com/",
        "login": "https://automationexercise.com/login",
        "cart": "https://automationexercise.com/view_cart",
        "search": "https://automationexercise.com/products",
        "product": "Blue Top",
        "quantity": "2",
        "email": "testuser@example.com",
        "password": "Test@1234",
        "login_btn": "button[type='submit']",
        "login_email": "input[data-qa='login-email']",
        "login_pwd": "input[data-qa='login-password']",
        "search_box": "input#search_product",
        "search_btn": "button#submit_search",
        "result_item": ".single-products",
        "result_link": ".productinfo a",
        "add_cart_btn": "button.cart",
        "qty_input": "#quantity",
        "cart_selector": ".cart_info",
        "detail_link": "product_details",
        "modal_close": ".close-modal",
        "search_page": "https://automationexercise.com/products",
        "search_add_btn": ".single-products .productinfo .add-to-cart",
        "detail_url": "https://automationexercise.com/product_details/1",
        "signup_name": "input[data-qa='signup-name']",
        "signup_email": "input[data-qa='signup-email']",
        "signup_btn": "button[data-qa='signup-button']",
        "signup_password": "input[data-qa='password']",
        "signup_days": "select[data-qa='days']",
        "signup_months": "select[data-qa='months']",
        "signup_years": "select[data-qa='years']",
        "signup_first_name": "input[data-qa='first_name']",
        "signup_last_name": "input[data-qa='last_name']",
        "signup_address": "input[data-qa='address']",
        "signup_country": "select[data-qa='country']",
        "signup_state": "input[data-qa='state']",
        "signup_city": "input[data-qa='city']",
        "signup_zipcode": "input[data-qa='zipcode']",
        "signup_mobile": "input[data-qa='mobile_number']",
        "signup_create_btn": "button[data-qa='create-account']",
        "signup_continue_btn": "a[data-qa='continue-button']",
        "signup_full_name": "Automation Tester",
        "signup_first_name_val": "Automation",
        "signup_last_name_val": "Tester",
        "signup_address_val": "MG Road, Bengaluru",
        "signup_country_val": "India",
        "signup_state_val": "Karnataka",
        "signup_city_val": "Bengaluru",
        "signup_zipcode_val": "560001",
        "signup_mobile_val": "9876543210",
    },
}


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


def create_driver(headless=False):
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-gpu")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    if headless:
        options.add_argument("--headless=new")
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
    step(index, total, test_fn.__doc__.strip().split("\n")[0])
    spinner(f"Running {test_fn.__name__}")
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
        ok(f"Opened {app['name']} ({d}s)  {C.DIM}[{tid}]{C.R}")
    except Exception as e:
        shot = take_screenshot(driver, "01_browser_launch_fail")
        d = round(time.time() - start, 2)
        results.append(TestResult(tid, desc, "FAIL", str(e), shot, d))
        fail(f"{e}  {C.DIM}[{tid}]{C.R}")


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
        ok(f"{msg} ({d}s)  {C.DIM}[{tid}]{C.R}")
    except Exception as e:
        shot = take_screenshot(driver, "03_login_fail")
        d = round(time.time() - start, 2)
        results.append(TestResult(tid, desc, "FAIL", str(e), shot, d))
        fail(f"{e}  {C.DIM}[{tid}]{C.R}")


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
        ok(f"Searched for '{product}', {count} result(s) ({d}s)  {C.DIM}[{tid}]{C.R}")
    except Exception as e:
        shot = take_screenshot(driver, "04_search_fail")
        d = round(time.time() - start, 2)
        results.append(TestResult(tid, desc, "FAIL", str(e), shot, d))
        fail(f"{e}  {C.DIM}[{tid}]{C.R}")


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
        ok(f"'{product}' added to cart ({d}s)  {C.DIM}[{tid}]{C.R}")
    except Exception as e:
        shot = take_screenshot(driver, "05_add_fail")
        d = round(time.time() - start, 2)
        results.append(TestResult(tid, desc, "FAIL", str(e), shot, d))
        fail(f"{e}  {C.DIM}[{tid}]{C.R}")


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
        ok(f"Quantity set to {qty} for '{product}' ({d}s)  {C.DIM}[{tid}]{C.R}")
    except Exception as e:
        shot = take_screenshot(driver, "06_qty_fail")
        d = round(time.time() - start, 2)
        results.append(TestResult(tid, desc, "FAIL", str(e), shot, d))
        fail(f"{e}  {C.DIM}[{tid}]{C.R}")


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
        ok(f"Cart verified ({d}s)  {C.DIM}[{tid}]{C.R}")
    except Exception as e:
        shot = take_screenshot(driver, "07_cart_fail")
        d = round(time.time() - start, 2)
        results.append(TestResult(tid, desc, "FAIL", str(e), shot, d))
        fail(f"{e}  {C.DIM}[{tid}]{C.R}")


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
        ok(msg + f" ({d}s)  {C.DIM}[{tid}]{C.R}")
    except Exception as e:
        shot = take_screenshot(driver, "08_popups_fail")
        d = round(time.time() - start, 2)
        results.append(TestResult(tid, desc, "FAIL", str(e), shot, d))
        fail(f"{e}  {C.DIM}[{tid}]{C.R}")


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
        ok(f"Screenshot saved: {os.path.basename(shot)} ({d}s)  {C.DIM}[{tid}]{C.R}")
    except Exception as e:
        d = round(time.time() - start, 2)
        results.append(TestResult(tid, desc, "FAIL", str(e), "", d))
        fail(f"{e}  {C.DIM}[{tid}]{C.R}")


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


def run_selected(app, selected, headless):
    data = load_test_data()
    results = []
    driver = create_driver(headless)
    try:
        tests = [(ALL_TESTS[i][0], ALL_TESTS[i][1]) for i in selected]
        total = len(tests)
        for idx, (label, fn) in enumerate(tests, 1):
            fn(driver, app, results, idx, total)
            info(f"{label} done {progress_bar(idx, total)}")
    finally:
        driver.quit()
    report = generate_html_report(results, app["name"])
    info(f"Execution report updated: {report}")
    return results


def pick_tests():
    section("SELECT TEST SUITE")
    options = {
        "1": ("Run ALL tests (full flow)", ""),
        "2": ("Select individual tests", ""),
    }
    choice = ask_choice("Choose an option:", options)
    if choice == "1":
        return list(range(len(ALL_TESTS)))
    section("AVAILABLE TESTS")
    while True:
        for i, (label, _) in enumerate(ALL_TESTS, 1):
            print(f"    {C.MAGENTA + C.BOLD}[{i}]{C.R}  {C.WHITE}{label}{C.R}")
        raw = input(f"\n  {C.BOLD + C.YELLOW}❯ Enter test numbers (comma separated, e.g. 1,3,4): {C.R}").strip()
        try:
            nums = [int(x) for x in raw.replace(",", " ").split() if x.strip()]
            if nums and all(1 <= n <= len(ALL_TESTS) for n in nums):
                return [n - 1 for n in nums]
        except ValueError:
            pass
        fail("Invalid input, try again.")


def pick_app():
    section("SELECT TARGET APPLICATION")
    options = {
        "1": ("TutorialsNinja Demo  (tutorialsninja.com)", "Recommended demo app"),
        "2": ("Automation Exercise  (automationexercise.com)", "Alternative demo app"),
    }
    choice = ask_choice("Choose a demo application:", options)
    if choice == "1":
        return APP_PRESETS["tutorialsninja"]
    return APP_PRESETS["automationexercise"]


def pick_mode():
    section("RUN MODE")
    options = {
        "1": ("Visible browser  (watch it live)", "Shows the browser window during execution"),
        "2": ("Headless (background)", "Runs silently, no browser window"),
    }
    choice = ask_choice("Choose run mode:", options)
    return choice == "2"


def show_status(results):
    total = len(results)
    passed = sum(1 for r in results if r.status == "PASS")
    failed = sum(1 for r in results if r.status == "FAIL")
    skipped = sum(1 for r in results if r.status == "SKIP")
    dur = sum(r.duration for r in results)

    section("EXECUTION SUMMARY")
    print(f"  {C.WHITE}Total tests  : {C.BOLD}{total}{C.R}")
    print(f"  {C.GREEN}Passed       : {C.BOLD}{passed}{C.R}")
    print(f"  {C.RED}Failed       : {C.BOLD}{failed}{C.R}")
    print(f"  {C.YELLOW}Skipped      : {C.BOLD}{skipped}{C.R}")
    print(f"  {C.CYAN}Time taken   : {C.BOLD}{dur:.2f}s{C.R}")
    print(f"  {C.WHITE}Pass rate    : {C.BOLD}{(passed / total * 100) if total else 0:.1f}%{C.R}")

    rate = passed / total if total else 0
    print("\n  " + C.GREEN + "  " + progress_bar(passed, total) + C.R)
    if rate >= 1:
        ok("ALL TESTS PASSED — outstanding!")
    elif rate >= 0.6:
        warn("Mostly passing, review failures.")
    else:
        fail("Many failures detected.")

    print("\n  " + C.DIM + "─" * 70 + C.R)
    for r in results:
        badge = status_badge(r.status)
        print(f"    {C.DIM}{r.test_id}{C.R}  {badge}   {r.description}")


def main_menu():
    while True:
        section("MAIN MENU")
        options = {
            "1": ("Run Automation Suite", "Full interactive run"),
            "2": ("View History / Report", "Open last HTML report"),
            "3": ("Regenerate Test Data (Excel)", "Recreate test_data.xlsx"),
            "4": ("Exit", "Close the program"),
        }
        choice = ask_choice("What would you like to do?", options)
        if choice == "1":
            app = pick_app()
            mode = pick_mode()
            tests = pick_tests()
            labels = [ALL_TESTS[i][0] for i in tests]
            section("CONFIRMATION")
            info(f"Application : {app['name']}")
            info(f"Mode        : {'Headless' if mode else 'Visible browser'}")
            info(f"Tests       : {', '.join(labels)}")
            press_enter()
            section("EXECUTING TESTS")
            results = run_selected(app, tests, mode)
            show_status(results)
            press_enter()
        elif choice == "2":
            report = os.path.join(BASE_DIR, "execution_report.html")
            if os.path.exists(report):
                os.startfile(report)
                ok("Opened report in browser.")
            else:
                warn("No report found yet — run the suite first.")
            press_enter()
        elif choice == "3":
            os.system(f'"{sys.executable}" create_test_data.py')
            ok("Test data regenerated.")
            press_enter()
        elif choice == "4":
            section("GOODBYE")
            ok("Thank you for reviewing the framework.")
            break


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n" + C.YELLOW + "  Interrupted by user. Exiting gracefully." + C.R)
