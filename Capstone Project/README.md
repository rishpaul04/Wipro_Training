# Selenium WebDriver Automation Framework

A Selenium WebDriver automation framework in Python for the **Wipro Capstone Project**.
It automates an end-to-end e-commerce flow on the live demo site:

- **TutorialsNinja Demo** — https://tutorialsninja.com/demo/

Each run executes 8 sequential test cases covering launch, login, search, cart, popups and screenshots, and regenerates a self-contained HTML execution report with charts and screenshot evidence.

## Features

- Single-site framework targeting TutorialsNinja Demo (config in `APP` dict in `ecommerce_automation.py`)
- Always-visible maximized Chrome (`create_driver()` in `ecommerce_automation.py:117`) — no headless / menu prompts
- 8 sequential tests (`ALL_TESTS` in `ecommerce_automation.py:451`)
- Overlay-resistant clicks via `safe_click()` + JS fallback, alert handling via `handle_alerts()`
- Simple console feedback: `section()`, `ok()`, `fail()`, `warn()`, `info()`, text `progress_bar()`
- Auto-generated HTML report via `generate_html_report()` (`report_generator.py:6`):
  - Summary cards (Total / Passed / Failed / Skipped / Total Duration)
  - Chart.js doughnut (pass/fail distribution) + horizontal bar (duration per test)
  - Per-test results table with clickable screenshot thumbnails (relative `screenshots/*.png` links)
- Automatic screenshot pruning — `prune_screenshots()` (`report_generator.py:207`) deletes PNGs not referenced by the latest report
- Optional test-data export: `create_test_data.py` builds a styled `test_data.xlsx` from `test_data.json`

## Project Structure

```
.
|-- ecommerce_automation.py   # APP config, TestResult, 8 tests, run_selected(), main()
|-- report_generator.py       # generate_html_report() + prune_screenshots()
|-- create_test_data.py       # create_excel_from_json() -> test_data.xlsx (3 sheets)
|-- test_data.json            # Reference test data (TC001-TC004, credentials, urls)
|-- requirements.txt          # selenium, openpyxl, colorama
|-- screenshots/              # Timestamped PNG evidence from latest run
`-- execution_report.html     # Latest run report (regenerated every run)
```

> Note: `load_test_data()` / `load_excel_data()` (`ecommerce_automation.py:86`) exist for JSON/Excel-driven inputs, but the current `run_selected()` / `main()` flow uses the hardcoded `APP` dict (`ecommerce_automation.py:49`). `test_data.json` is the source of truth for `create_test_data.py` and documents the intended inputs/credentials/URLs.

## Prerequisites & Installation

- Python 3.x
- Google Chrome (chromedriver is managed automatically by Selenium Manager)

```bash
pip install -r requirements.txt
```

Dependencies (`requirements.txt`):

```
selenium==4.27.1
openpyxl==3.1.5
colorama==0.4.6
```

## How to Run

Run the full suite (visible browser, no arguments/menus):

```bash
python ecommerce_automation.py
```

What happens in `main()` (`ecommerce_automation.py:508`):

1. Prints `EXECUTING TESTS - TutorialsNinja Demo (Visible)`
2. Calls `run_selected()` — creates driver, runs all 8 tests in order, quits driver
3. Calls `generate_html_report(results, APP["name"])` → overwrites `execution_report.html` and prunes `screenshots/`
4. Prints `EXECUTION SUMMARY` via `show_status()` with counts, duration, pass rate, and per-test list

Generate the Excel test-data file (optional):

```bash
python create_test_data.py
```

This reads `test_data.json` and writes `test_data.xlsx` with sheets: `Test Cases`, `Credentials`, `URLs`.

Programmatic use (same single-site behaviour — extra args kept for compatibility only):

```python
from ecommerce_automation import run_selected
results = run_selected()  # runs all 8 TutorialsNinja tests in visible Chrome
```

## Test Cases

Defined in `ecommerce_automation.py:451` (`ALL_TESTS`), executed in this order:

| # | Label in code | Test ID | Description (in code) |
|---|---------------|---------|-----------------------|
| 1 | Launch Browser | `TC_LAUNCH` | Launch browser and navigate to application |
| 2 | Login (Signup first) | `TC_LOGIN` | Signup then login |
| 3 | Search Product | `TC_SEARCH` | Search for a product |
| 4 | Add to Cart | `TC_ADD_CART` | Add product to cart |
| 5 | Update Quantity | `TC_UPDATE_QTY` | Update product quantity |
| 6 | Verify Cart | `TC_VERIFY_CART` | Verify cart details |
| 7 | Popups | `TC_POPUPS` | Handle popups & alerts |
| 8 | Screenshot | `TC_SCREENSHOT` | Capture screenshot |

Current behaviour notes (matching code):

- `TC_LAUNCH`: opens `APP["base"]`, waits for `#logo`, saves `01_browser_launched_<timestamp>.png`.
- `TC_LOGIN`: opens `APP["login"]`, fills `APP["email"]` / `APP["password"]` (`testuser@example.com` / `Test@1234`), submits login form. Signup branch (`do_signup()`) only triggers if `APP` contains signup selectors — the current TutorialsNinja `APP` does not, so it is a login-form submission.
- `TC_SEARCH` / `TC_ADD_CART` / `TC_UPDATE_QTY`: search for `APP["product"]` (`MacBook`), open first result link, use `#button-cart` and `#input-quantity` with quantity `APP["quantity"]` (`2`).
- `TC_VERIFY_CART`: opens `APP["cart"]`, waits for `#content`.
- `TC_POPUPS`: accepts any present alert, otherwise passes with "No alerts present".
- `TC_SCREENSHOT`: re-opens base URL and saves `09_screenshot_captured_<timestamp>.png`.
- Every test records `TestResult(test_id, description, PASS/FAIL, message, screenshot, duration)` and never skips — `SKIP` is only counted for display.

## Test Data

`test_data.json`:

- `test_cases`: TC001 (login), TC002 (search `MacBook`), TC003 (add + quantity `2`), TC004 (verify cart) with `expected_result` strings
- `credentials`: `my_account_url`, `email`, `password`
- `urls`: `base_url`, `search_url`, `cart_url`

`create_test_data.py:7` (`create_excel_from_json`) converts this to `test_data.xlsx` with styled headers, borders, and auto-sized columns.

## Report

- Output: `execution_report.html` in the project root (overwritten every run).
- Screenshots: `screenshots/<name>_YYYYMMDD_HHMMSS.png`, embedded as relative links so the report is portable if moved with the folder.
- Open it directly in a browser after a run to see summary cards, charts, and evidence thumbnails.
