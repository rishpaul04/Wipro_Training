"""
csv_reader.py - CSV data reading utility for the POM framework
Module: Unit Test Frameworks - Page Object Model
Student: Rishita Paul
Date: September 8, 2026

Utility to read CSV test data files.
"""

import csv
import os


class CSVReader:
    """Utility class for reading CSV test data"""

    def __init__(self, filepath=None):
        """Initialize with optional filepath"""
        self.filepath = filepath

    def read_csv_as_dict(self, filepath=None):
        """Read CSV file and return list of dicts"""
        path = filepath or self.filepath
        if not path or not os.path.exists(path):
            raise FileNotFoundError(f"CSV file not found: {path}")

        data = []
        with open(path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(dict(row))
        return data

    def read_csv_as_lists(self, filepath=None):
        """Read CSV file and return list of lists"""
        path = filepath or self.filepath
        if not path or not os.path.exists(path):
            raise FileNotFoundError(f"CSV file not found: {path}")

        data = []
        with open(path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                data.append(row)
        return data

    def create_sample_csv(self, filepath="testdata/login_data.csv"):
        """Create a sample CSV test data file"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["username", "password", "expected"])
            writer.writerow(["standard_user", "secret_sauce", "success"])
            writer.writerow(["locked_out_user", "secret_sauce", "locked_out"])
            writer.writerow(["problem_user", "secret_sauce", "success"])
            writer.writerow(["wrong_user", "wrong_pass", "error_message"])
        return filepath

    def get_count(self, filepath=None):
        """Get number of data rows in CSV"""
        data = self.read_csv_as_dict(filepath)
        return len(data)


if __name__ == "__main__":
    reader = CSVReader()
    filepath = reader.create_sample_csv()
    print(f"✓ Sample CSV created: {filepath}")
    data = reader.read_csv_as_dict(filepath)
    for row in data:
        print(f"  {row}")
    print(f"✓ Total rows: {len(data)}")
