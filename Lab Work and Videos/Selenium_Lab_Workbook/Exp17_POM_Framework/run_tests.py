"""
run_tests.py - Run all POM framework tests
Module: Unit Test Frameworks - Page Object Model
Student: Rishita Paul
Date: September 8, 2026
"""

import unittest
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import test modules
from tests.test_login_pom import TestLoginPagePOM
from tests.test_dashboard_pom import TestDashboardPagePOM


def create_suite():
    """Create a combined test suite"""
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    print("=" * 70)
    print("RUNNING PAGE OBJECT MODEL (POM) TEST SUITE")
    print("=" * 70)

    # Add all tests from login test class
    suite.addTests(loader.loadTestsFromTestCase(TestLoginPagePOM))
    print(f"Added TestLoginPagePOM ({loader.loadTestsFromTestCase(TestLoginPagePOM).countTestCases()} tests)")

    # Add all tests from dashboard test class
    suite.addTests(loader.loadTestsFromTestCase(TestDashboardPagePOM))
    print(f"Added TestDashboardPagePOM ({loader.loadTestsFromTestCase(TestDashboardPagePOM).countTestCases()} tests)")

    return suite


if __name__ == "__main__":
    print("\n--- Testing Utilities ---")
    print("-" * 70)

    # Test config utility
    from utils.config import Config
    config = Config("testdata/config.properties")
    print(f"✓ Config utility: URL={config.get_base_url()}")

    # Test CSV utility
    from utils.csv_reader import CSVReader
    csv_reader = CSVReader()
    csv_path = csv_reader.create_sample_csv("testdata/login_data.csv")
    csv_data = csv_reader.read_csv_as_dict(csv_path)
    print(f"✓ CSV utility: {len(csv_data)} rows loaded")

    print("\n--- Running POM Test Suite ---")
    runner = unittest.TextTestRunner(verbosity=2)
    suite = create_suite()
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.wasSuccessful():
        print("\n✓ ALL POM TESTS PASSED!")
    else:
        print("\n✗ SOME TESTS FAILED")
