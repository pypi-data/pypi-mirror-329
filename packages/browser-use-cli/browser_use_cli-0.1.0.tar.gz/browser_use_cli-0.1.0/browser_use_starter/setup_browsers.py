#!/usr/bin/env python3
"""
Setup script to install Playwright browsers.
Run this after installing the dependencies.
"""

import sys
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from browser_use_starter.utils import install_playwright_browsers, print_status

def main():
    """
    Install Playwright browsers.
    """
    print("Installing Playwright browsers...")
    
    if install_playwright_browsers():
        print_status("Playwright browsers installed successfully!")
        return 0
    else:
        print_status("Error installing Playwright browsers.", False)
        print("Try running: playwright install")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 