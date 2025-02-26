"""
Utility functions for Browser Use CLI.
Contains helper functions for dependency checking, browser detection, etc.
"""

import sys
import subprocess
import importlib.util
import logging
import platform
from pathlib import Path
import re

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.theme import Theme
from rich.style import Style
from rich.text import Text

from browser_use_starter.config import get_chrome_path

logger = logging.getLogger(__name__)

# Create a custom theme for consistent styling
custom_theme = Theme({
    "info": "bold cyan",
    "success": "bold green",
    "warning": "bold yellow",
    "error": "bold red",
    "highlight": "bold magenta",
})

# Create a console with the custom theme
console = Console(theme=custom_theme)

def check_dependencies():
    """
    Check if all required dependencies are installed.
    Returns a list of missing packages.
    """
    missing_packages = []
    
    # Required packages and their import names
    dependencies = {
        "browser-use": "browser_use",
        "langchain-google-genai": "langchain_google_genai",
        "python-dotenv": "dotenv",
        "playwright": "playwright"
    }
    
    with console.status("[info]Checking dependencies...", spinner="dots"):
        for package_name, module_name in dependencies.items():
            if importlib.util.find_spec(module_name) is None:
                missing_packages.append(package_name)
                logger.warning(f"Required package '{package_name}' is not installed")
    
    return missing_packages

def install_dependencies(missing_packages, use_uv=True):
    """
    Install missing dependencies.
    Returns True if successful, False otherwise.
    """
    if not missing_packages:
        return True
    
    console.print(Panel(f"[info]Installing missing packages: [highlight]{', '.join(missing_packages)}", 
                        title="Dependency Installation", 
                        border_style="cyan"))
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            if use_uv:
                # Check if uv is installed
                subprocess.run(["uv", "--version"], check=True, capture_output=True)
                
                # Install packages using uv
                for package in missing_packages:
                    task = progress.add_task(f"[cyan]Installing {package} using uv...", total=None)
                    subprocess.check_call(["uv", "pip", "install", package])
                    progress.update(task, completed=True, description=f"[green]Installed {package}")
                
                console.print("[success]All required packages installed successfully")
                return True
            else:
                # Use pip as fallback
                for package in missing_packages:
                    task = progress.add_task(f"[cyan]Installing {package} using pip...", total=None)
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                    progress.update(task, completed=True, description=f"[green]Installed {package}")
                
                console.print("[success]All required packages installed successfully")
                return True
    except subprocess.CalledProcessError as e:
        console.print(f"[error]Failed to install dependencies: {str(e)}")
        logger.error(f"Failed to install dependencies: {str(e)}")
        return False

def check_chrome_browser():
    """
    Check if Chrome browser is installed on the system.
    Returns True if Chrome is found, False otherwise.
    """
    system = platform.system()
    chrome_path = get_chrome_path()
    
    with console.status("[info]Checking for Chrome browser...", spinner="dots"):
        if chrome_path and Path(chrome_path).exists():
            logger.info(f"Chrome browser found at: {chrome_path}")
            return True
        
        try:
            if system == "Darwin":  # macOS
                subprocess.run(["open", "-a", "Google Chrome"], check=True, capture_output=True)
                return True
            elif system == "Windows":
                subprocess.run(["where", "chrome"], check=True, capture_output=True)
                return True
            elif system == "Linux":
                subprocess.run(["which", "google-chrome"], check=True, capture_output=True)
                return True
        except subprocess.CalledProcessError:
            logger.warning(f"Google Chrome browser not found on {system}")
            return False
        
        return False

def install_playwright_browsers():
    """
    Install Playwright browsers.
    Returns True if successful, False otherwise.
    """
    console.print("[info]Installing Playwright browsers...")
    
    try:
        with console.status("[info]Installing Chromium browser...", spinner="dots"):
            subprocess.check_call(["playwright", "install", "chromium"])
        
        console.print("[success]Playwright browsers installed successfully")
        logger.info("Playwright browsers installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"[error]Failed to install Playwright browsers: {str(e)}")
        logger.error(f"Failed to install Playwright browsers: {str(e)}")
        return False
    except FileNotFoundError:
        console.print("[error]Playwright not found. Make sure to install it first")
        logger.error("Playwright not found. Make sure to install it first")
        return False

def print_status(message, success=True):
    """
    Print status messages with color coding.
    """
    if success:
        prefix = "✅"
        style = "success"
    else:
        prefix = "❌"
        style = "error"
    
    console.print(f"{prefix} [{style}]{message}")
    
    # Also log the message
    if success:
        logger.info(message)
    else:
        logger.error(message)

def print_header(title, subtitle=None):
    """
    Print a styled header for CLI commands.
    """
    console.print()
    text = Text(title, style="bold cyan")
    console.print(Panel(text, border_style="cyan"))
    if subtitle:
        console.print(f"[cyan]{subtitle}")
    console.print()

def print_result(result, title="Result"):
    """
    Print a result in a styled panel.
    Extract and display only the relevant information from the task result.
    """
    console.print()
    
    # Check if result is a dictionary with our custom format
    if isinstance(result, dict) and "result" in result:
        agent_result = result["result"]
        history_file = result.get("history_file")
        gif_file = result.get("gif_file")
    else:
        agent_result = result
        history_file = None
        gif_file = None
    
    # Try to extract the final result text
    final_result = None
    
    try:
        # Check if this is an AgentHistoryList object by looking at its string representation
        result_str = str(agent_result)
        if "AgentHistoryList" in result_str and "extracted_content" in result_str:
            # Extract the final result using string parsing as a fallback
            # Look for patterns like: extracted_content='The current time is...'
            matches = re.findall(r"extracted_content='([^']*)'", result_str)
            if matches:
                # Get the last match which is likely the final result
                final_result = matches[-1]
            
            # If we couldn't extract it with regex, try to access it as an object
            if not final_result and hasattr(agent_result, 'all_results') and agent_result.all_results:
                for action_result in reversed(agent_result.all_results):
                    if hasattr(action_result, 'is_done') and action_result.is_done:
                        final_result = action_result.extracted_content
                        break
                
                # If no is_done=True result found, use the last result
                if not final_result:
                    final_result = agent_result.all_results[-1].extracted_content
    except Exception as e:
        # If any error occurs during extraction, log it and fall back to the default
        logger.warning(f"Error extracting result: {str(e)}")
    
    # Display the extracted result or fall back to the raw result
    if final_result:
        console.print(Panel(final_result, title=title, border_style="green"))
    else:
        console.print(Panel(str(agent_result), title=title, border_style="green"))
    
    # Display file locations if available
    if gif_file:
        console.print(f"[info]GIF recording saved to: [link]{gif_file}[/link]")
    
    if history_file:
        console.print(f"[info]History log saved to: [link]{history_file}[/link]")
    
    console.print() 