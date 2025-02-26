#!/usr/bin/env python3
"""
Test script for Browser Use CLI.
Runs a simple browser automation test to verify functionality.
"""

import asyncio
import sys
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import package modules
from browser_use_starter.utils import print_status
from browser_use_starter.config import get_api_key
from browser_use_starter.agent import run_task, setup_environment

async def run_simple_test():
    """
    Run a simple browser automation test.
    """
    print("\n🔍 Running minimal browser automation test...\n")
    
    # Check for API key
    api_key = get_api_key()
    if not api_key:
        print_status("Google API key not found", False)
        print("  Run 'browser-setup' to configure your API key")
        return False
    
    try:
        # Simple task that should work quickly
        task = "Go to example.com and get the title of the page."
        
        print(f"📋 Test task: {task}")
        print("⏳ Running browser automation (this may take a few seconds)...")
        
        # Run the task
        result = await run_task(task, headless=False)
        
        print("\n✅ Browser automation test completed successfully!")
        print(f"📊 Result: {result}")
        return True
        
    except Exception as e:
        logger.exception("Browser automation test failed")
        print_status(f"Browser automation test failed: {str(e)}", False)
        return False

def main():
    """
    Run the browser test.
    """
    # First run setup to ensure environment is ready
    if not setup_environment():
        print_status("Environment setup failed", False)
        return 1
    
    try:
        result = asyncio.run(run_simple_test())
        return 0 if result else 1
    except KeyboardInterrupt:
        print("\n❌ Test interrupted by user.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 