"""
Configuration module for Browser Use CLI.
Centralizes all configuration settings and provides utilities for managing them.
"""

import os
import platform
from pathlib import Path
import logging

# Set up logging - default to WARNING level to hide most logs
logging.basicConfig(
    level=logging.WARNING,  # Default to WARNING to hide most logs
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Application paths
APP_NAME = "browser-use-cli"
APP_DIR = Path(__file__).parent
PROJECT_ROOT = APP_DIR.parent

# User-specific paths
USER_HOME = Path.home()
USER_CONFIG_DIR = USER_HOME / ".config" / APP_NAME
USER_DATA_DIR = USER_HOME / ".local" / "share" / APP_NAME

# Ensure user directories exist
USER_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
USER_DATA_DIR.mkdir(parents=True, exist_ok=True)

# API key storage
API_KEY_FILE = USER_CONFIG_DIR / "api_keys.env"

# LLM settings
DEFAULT_MODEL = "gemini-2.0-flash"
MAX_RETRIES = 5

# Browser settings
DEFAULT_BROWSER = "chrome"
DEFAULT_HEADLESS = False

# Default task
DEFAULT_TASK = "Compare the price of gpt-4o and DeepSeek-V3."

def get_api_key(key_name="GOOGLE_API_KEY"):
    """
    Get API key from environment or user config file.
    Prioritizes environment variables over stored keys.
    """
    # First check environment
    api_key = os.getenv(key_name)
    
    # Then check user config file
    if not api_key and API_KEY_FILE.exists():
        with open(API_KEY_FILE, "r") as f:
            for line in f:
                if line.startswith(f"{key_name}="):
                    api_key = line.strip().split("=", 1)[1]
                    break
    
    return api_key

def save_api_key(key_name, key_value):
    """
    Save API key to user config file.
    """
    # Read existing keys
    existing_keys = {}
    if API_KEY_FILE.exists():
        with open(API_KEY_FILE, "r") as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    existing_keys[k] = v
    
    # Update key
    existing_keys[key_name] = key_value
    
    # Write back all keys
    with open(API_KEY_FILE, "w") as f:
        for k, v in existing_keys.items():
            f.write(f"{k}={v}\n")
    
    # Set permissions to user-only read/write
    if platform.system() != "Windows":
        os.chmod(API_KEY_FILE, 0o600)
    
    logger.info(f"API key '{key_name}' saved to {API_KEY_FILE}")
    return True

def get_chrome_path():
    """
    Get the path to Chrome browser based on the operating system.
    """
    system = platform.system()
    
    if system == "Darwin":  # macOS
        return "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    elif system == "Windows":
        paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ]
        for path in paths:
            if os.path.exists(path):
                return path
    elif system == "Linux":
        paths = [
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable"
        ]
        for path in paths:
            if os.path.exists(path):
                return path
    
    return None 