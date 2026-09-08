"""
config.py - Configuration utility for the POM framework
Module: Unit Test Frameworks - Page Object Model
Student: Rishita Paul
Date: September 8, 2026

Reads configuration settings from properties/config files.
"""

import configparser
import os
import json


class Config:
    """Configuration utility class"""

    def __init__(self, config_path=None):
        """Initialize config from file or defaults"""
        if config_path and os.path.exists(config_path):
            self.config = configparser.ConfigParser()
            self.config.read(config_path)
        else:
            self.config = None
            self.defaults = self._get_default_config()

    def _get_default_config(self):
        """Return default configuration"""
        return {
            "base_url": "https://www.saucedemo.com/",
            "browser": "chrome",
            "implicit_wait": 5,
            "explicit_wait": 10,
            "username": "standard_user",
            "password": "secret_sauce",
            "screenshot_dir": "reports/screenshots",
        }

    def get(self, section, key, default=None):
        """Get config value"""
        try:
            if self.config:
                return self.config.get(section, key)
            return self.defaults.get(key, default)
        except Exception:
            return default

    def get_base_url(self):
        """Get base URL"""
        return self.get("application", "base_url")

    def get_browser(self):
        """Get browser name"""
        return self.get("browser", "name")

    def get_implicit_wait(self):
        """Get implicit wait time"""
        return int(self.get("browser", "implicit_wait"))

    def get_credentials(self):
        """Get default credentials"""
        return {
            "username": self.get("credentials", "username"),
            "password": self.get("credentials", "password")
        }


if __name__ == "__main__":
    # Create a sample config file
    config = configparser.ConfigParser()
    config["application"] = {"base_url": "https://www.saucedemo.com/"}
    config["browser"] = {"name": "chrome", "implicit_wait": "5", "explicit_wait": "10"}
    config["credentials"] = {"username": "standard_user", "password": "secret_sauce"}

    os.makedirs("testdata", exist_ok=True)
    with open("testdata/config.properties", "w") as f:
        config.write(f)

    print("✓ Sample config file created: testdata/config.properties")

    # Test reading config
    cfg = Config("testdata/config.properties")
    print(f"✓ Base URL: {cfg.get_base_url()}")
    print(f"✓ Browser: {cfg.get_browser()}")
    print(f"✓ Implicit wait: {cfg.get_implicit_wait()}")
    creds = cfg.get_credentials()
    print(f"✓ Username: {creds['username']}")
    print(f"✓ Password: {creds['password']}")
