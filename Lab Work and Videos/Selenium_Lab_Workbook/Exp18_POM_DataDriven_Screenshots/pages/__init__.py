"""
pages/__init__.py - Page classes package
"""

from .base_page import BasePage
from .login_page import LoginPage
from .dashboard_page import DashboardPage

__all__ = ["BasePage", "LoginPage", "DashboardPage"]
