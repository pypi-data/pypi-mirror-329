#!/usr/bin/env python3
"""
Verification script for Browser Use CLI.
Checks if all prerequisites are met for running the application.
"""

import sys
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import local modules
from browser_use_starter.utils import (
    check_dependencies,
    check_chrome_browser,
    print_status
)
from browser_use_starter.config import get_api_key

def check_python_version():
    """
    Check if Python version meets requirements.
    """
    import platform
    required_version = (3, 11)
    current_version = sys.version_info
    
    if current_version >= required_version:
        print_status(f"Python version: {platform.python_version()} (meets requirement of 3.11+)")
        return True
    else:
        print_status(f"Python version: {platform.python_version()} (requires 3.11+)", False)
        return False

def check_uv_installed():
    """
    Check if uv is installed.
    """
    import subprocess
    try:
        result = subprocess.run(["uv", "--version"], capture_output=True, text=True)
        print_status(f"uv package manager installed: {result.stdout.strip()}")
        return True
    except (FileNotFoundError, subprocess.SubprocessError):
        print_status("uv package manager not found", False)
        print("  To install uv: curl -sSf https://install.python-uv.org | python3")
        return False

def check_dependencies_status():
    """
    Check if required dependencies are installed.
    """
    missing = check_dependencies()
    
    if not missing:
        print_status("All required dependencies are installed")
        return True
    else:
        print_status(f"Missing dependencies: {', '.join(missing)}", False)
        print("\nTo install missing packages:")
        print("  uv pip install -e .")
        return False

def check_api_key_status():
    """
    Check if Google API key is configured.
    """
    api_key = get_api_key()
    
    if api_key:
        masked_key = api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:]
        print_status(f"Google API key found: {masked_key}")
        return True
    else:
        print_status("Google API key not found", False)
        print("  You can get your API key from: https://aistudio.google.com/apikey")
        print("  Add it to your user config or environment variables")
        return False

def check_playwright_browsers():
    """
    Check if Playwright browsers are installed.
    """
    try:
        from playwright.sync_api import sync_playwright
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                browser.close()
            print_status("Playwright browsers are installed")
            return True
        except Exception as e:
            print_status(f"Playwright browsers not installed: {str(e)}", False)
            print("  Run: playwright install")
            return False
    except ImportError:
        print_status("Playwright package not installed", False)
        print("  Install with: uv pip install playwright")
        return False

def main():
    """
    Run all verification checks.
    """
    print("\n🔍 Browser Use CLI - Setup Verification\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("UV Package Manager", check_uv_installed),
        ("Required Dependencies", check_dependencies_status),
        ("Chrome Browser", check_chrome_browser),
        ("Google API Key", check_api_key_status),
        ("Playwright Browsers", check_playwright_browsers)
    ]
    
    results = {}
    
    for name, check_func in checks:
        print(f"\n📋 Checking {name}...")
        results[name] = check_func()
    
    # Summary
    print("\n📊 Verification Summary:")
    all_passed = True
    for name, result in results.items():
        status = "PASS" if result else "FAIL"
        if not result:
            all_passed = False
        print(f"  {name}: {status}")
    
    if all_passed:
        print("\n🎉 All checks passed! The system is ready to run browser-use-cli.")
        print("  Try running: python -m browser_use_starter.agent")
    else:
        print("\n⚠️  Some checks failed. Please address the issues above before running the tool.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main()) 