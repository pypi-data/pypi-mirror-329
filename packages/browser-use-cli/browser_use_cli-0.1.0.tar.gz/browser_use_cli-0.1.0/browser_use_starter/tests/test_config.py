#!/usr/bin/env python3
"""
Test module for config.py.
Tests configuration utilities and API key management.
"""

import os
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

from browser_use_starter.config import (
    get_api_key,
    save_api_key,
    get_chrome_path,
    USER_CONFIG_DIR,
    USER_DATA_DIR,
)


class TestConfig(unittest.TestCase):
    """Test cases for config module."""

    def setUp(self):
        """Set up test environment."""
        # Create a temporary directory for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        
        # Save original paths
        self.original_config_dir = USER_CONFIG_DIR
        self.original_data_dir = USER_DATA_DIR
        
        # Mock environment variables
        self.env_patcher = patch.dict(os.environ, {}, clear=True)
        self.env_patcher.start()

    def tearDown(self):
        """Clean up test environment."""
        self.env_patcher.stop()
        self.temp_dir.cleanup()

    def test_get_api_key_from_env(self):
        """Test retrieving API key from environment variables."""
        # Set environment variable
        os.environ["GOOGLE_API_KEY"] = "test_api_key_env"
        
        # Get API key
        api_key = get_api_key()
        
        # Check result
        self.assertEqual(api_key, "test_api_key_env")

    @patch('browser_use_starter.config.API_KEY_FILE')
    def test_save_and_get_api_key(self, mock_api_key_file):
        """Test saving and retrieving API key from file."""
        # Set up mock file path
        test_key_file = self.temp_path / "api_keys.env"
        mock_api_key_file.exists.return_value = True
        mock_api_key_file.return_value = test_key_file
        
        # Save API key
        with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            save_api_key("GOOGLE_API_KEY", "test_api_key_file")
            
        # Mock reading from file
        with patch('builtins.open', unittest.mock.mock_open(
                read_data="GOOGLE_API_KEY=test_api_key_file\n")) as mock_file:
            mock_api_key_file.exists.return_value = True
            api_key = get_api_key()
            
        # Check result
        self.assertEqual(api_key, "test_api_key_file")

    def test_get_chrome_path(self):
        """Test getting Chrome path."""
        # Just verify it returns something without error
        chrome_path = get_chrome_path()
        # The actual path will depend on the system, so we just check it's a string or None
        self.assertIsInstance(chrome_path, (str, type(None)))


if __name__ == "__main__":
    unittest.main() 