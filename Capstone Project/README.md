# Selenium WebDriver Automation Framework

A Selenium WebDriver automation framework built in Python for the **Wipro Capstone Assignment**.
It automates end-to-end e-commerce flows on two live demo sites:

- **TutorialsNinja Demo** — https://tutorialsninja.com/demo/
- **Automation Exercise** — https://automationexercise.com/

Each site runs 8 automated test cases covering the full purchase journey and produces a
self-contained HTML execution report with charts and screenshot evidence.

## Features

- Interactive menu-driven runner (pick app, run mode, and test set)
- Visible and headless browser modes
- App-aware test logic — one framework, two different demo sites
- **Signup → Logout → Login** flow for Automation Exercise (real account creation)
- Data-driven inputs loaded from `test_data.json` / regenerable `test_data.xlsx`
- Live console feedback: colored statuses, spinner, progress bar
- Auto-generated HTML report (`execution_report.html`) updated on every run:
  - Summary cards (Passed / Failed / Skipped / Pass rate / Duration)
  - Chart.js doughnut + duration bar charts
  - Per-test results table with clickable screenshot thumbnails
- Automatic screenshot pruning — only the latest run's evidence is kept

## Project Structure

```
.
|-- ecommerce_automation.py   # Main framework: presets, 8 tests, menus, orchestration
|-- console_ui.py             # CLI helpers (colors, progress bar, spinners, prompts)
|-- report_generator.py       # Builds execution_report.html + chart script
|-- create_test_data.py       # Regenerates test_data.xlsx from test_data.json
|-- test_data.json            # Data-driven test inputs (source of truth)
|-- test_data.xlsx            # Excel form of test data (created on demand)
|-- requirements.txt          # Pinned dependencies
|-- screenshots/              # Evidence captured during the latest run
`-- execution_report.html     # Latest run report (auto-created)
```

## Prerequisites & Installation

- Python 3.13+
- Google Chrome (matching chromedriver managed by Selenium Manager)

```bash
pip install -r requirements.txt
```

## How to Run

Interactive mode:

```bash
python ecommerce_automation.py
```

Menu flow:

1. **Run Automation Suite** — choose app (TutorialsNinja / Automation Exercise),
   run mode (visible / headless), then all tests or an individual subset
2. **View History / Report** — opens the latest `execution_report.html`
3. **Regenerate Test Data (Excel)** — recreates `test_data.xlsx`
4. **Exit**

Programmatic / CI use:

```python
from ecommerce_automation import run_selected, APP_PRESETS

app = APP_PRESETS["automationexercise"]
results = run_selected(app, list(range(8)), headless=True)
```

## Test Cases

| ID           | Test                        |
|--------------|-----------------------------|
| `TC_LAUNCH`  | Launch browser & navigate   |
| `TC_LOGIN`   | Signup then login           |
| `TC_SEARCH`  | Search for a product        |
| `TC_ADD_CART`| Add product to cart         |
| `TC_UPDATE_QTY` | Update product quantity  |
| `TC_VERIFY_CART` | Verify cart details     |
| `TC_POPUPS`  | Handle popups & alerts      |
| `TC_SCREENSHOT` | Capture screenshot       |

> Note: TutorialsNinja has no self-service account creation, so its login test
> exercises the login form; Automation Exercise performs a full signup then login.

## Report

Every run regenerates `execution_report.html` and prunes older screenshots.
Screenshots embedded in the report are relative links, so the report is portable.