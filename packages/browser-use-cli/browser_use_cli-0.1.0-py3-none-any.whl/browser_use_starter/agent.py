"""
Browser Use CLI - Command-line tool for browser automation tasks
Main agent module that handles browser automation tasks.
"""

import asyncio
import argparse
import os
import sys
import logging
import datetime

# Set up logging - default to WARNING level to hide most logs
logging.basicConfig(
    level=logging.WARNING,  # Default to WARNING to hide most logs
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import local modules
from browser_use_starter.utils import (
    check_dependencies, 
    install_dependencies, 
    check_chrome_browser,
    install_playwright_browsers,
    print_status,
    print_header,
    print_result,
    console
)
from browser_use_starter.config import (
    DEFAULT_TASK, 
    DEFAULT_MODEL, 
    MAX_RETRIES,
    get_api_key,
    save_api_key,
    USER_DATA_DIR
)

def setup_environment():
    """
    Set up the environment for running the agent.
    Checks dependencies, browser, and API key.
    Returns True if setup is successful, False otherwise.
    """
    print_header("Browser Use CLI Setup", "Checking environment and dependencies...")
    
    # Check dependencies
    missing_packages = check_dependencies()
    if missing_packages:
        console.print(f"[warning]The following required packages are not installed: [highlight]{', '.join(missing_packages)}")
        choice = input("Would you like to install them now? (y/n): ")
        if choice.lower() == 'y':
            if not install_dependencies(missing_packages):
                print_status("Cannot proceed without the required packages.", success=False)
                return False
        else:
            print_status("Cannot proceed without the required packages.", success=False)
            return False
    else:
        print_status("All required packages are installed")
    
    # Check for Chrome browser
    if not check_chrome_browser():
        console.print("[error]Chrome browser is required for this application to work.")
        console.print("[info]Please install Chrome browser from: [link]https://www.google.com/chrome/[/link]")
        return False
    else:
        print_status("Chrome browser is installed")
    
    # Check for API key
    api_key = get_api_key()
    if not api_key:
        console.print("[warning]Google API key not found.")
        console.print("[info]You can get your API key from: [link]https://aistudio.google.com/apikey[/link]")
        api_key = input("Please enter your Google API key: ")
        if not api_key:
            print_status("Cannot proceed without an API key.", success=False)
            return False
        
        # Save API key to user config
        save_api_key("GOOGLE_API_KEY", api_key)
        print_status("API key saved successfully")
        
        # Also set it in the environment for the current session
        os.environ["GOOGLE_API_KEY"] = api_key
    else:
        print_status("API key found")
    
    # Install Playwright browsers if needed
    try:
        import playwright
        try:
            # Check if browsers are already installed
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                browser = p.chromium.launch()
                browser.close()
            logger.info("Playwright browsers are already installed")
            print_status("Playwright browsers are already installed")
        except Exception:
            # Install browsers if not already installed
            console.print("[info]Installing Playwright browsers (required for browser automation)...")
            if not install_playwright_browsers():
                console.print("[warning]Warning: Failed to install Playwright browsers.")
                console.print("[warning]Some features may not work correctly.")
    except ImportError:
        logger.warning("Playwright not installed, skipping browser installation")
    
    return True

async def run_task(task, headless=False):
    """
    Run a browser automation task.
    """
    # Import here to avoid circular imports
    from dotenv import load_dotenv
    from langchain_google_genai import ChatGoogleGenerativeAI
    from browser_use import Agent, Browser, BrowserConfig
    from browser_use_starter.config import USER_DATA_DIR
    import datetime
    
    # Load environment variables (for API keys)
    load_dotenv()
    
    # Initialize LLM
    llm = ChatGoogleGenerativeAI(
        model=DEFAULT_MODEL,
        max_retries=MAX_RETRIES,
    )
    
    logger.info(f"Running task: {task}")
    
    # Create browser configuration
    browser_config = BrowserConfig(
        headless=headless,
        disable_security=True  # Helps with cross-site iFrames and other functionality
    )
    
    # Create browser with the configuration
    browser = Browser(config=browser_config)
    
    # Create and run agent
    agent = Agent(
        task=task,
        llm=llm,
        browser=browser
    )
    
    try:
        with console.status(f"[info]Running browser task: {task}", spinner="dots"):
            result = await agent.run()
            
        # Create timestamp for unique filenames
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create output directory if it doesn't exist
        output_dir = USER_DATA_DIR / "recordings"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save history and create GIF
        history_file = output_dir / f"history_{timestamp}.json"
        gif_file = output_dir / f"recording_{timestamp}.gif"
        
        # Save history to JSON file
        agent.save_history(history_file)
        
        # Create GIF from history
        agent.create_history_gif(str(gif_file))
        
        # Return a dictionary with the result and file paths
        return {
            "result": result,
            "history_file": str(history_file),
            "gif_file": str(gif_file)
        }
    finally:
        # Make sure to close the browser
        await browser.close()

def main():
    """
    Main entry point for the CLI.
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Run browser automation tasks from the command line")
    parser.add_argument("task", nargs="?", default=None, help="The task to perform in the browser")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument("--setup", action="store_true", help="Run setup only without executing a task")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()
    
    # Set debug logging if requested
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Print welcome message
    print_header(
        "Browser Use CLI", 
        "A command-line tool for browser automation tasks powered by AI"
    )
    
    # Run setup
    if not setup_environment():
        console.print("[error]Setup failed. Please fix the issues and try again.")
        sys.exit(1)
    
    # If setup only, exit after setup
    if args.setup:
        print_status("Setup completed successfully.")
        sys.exit(0)
    
    # If no task is provided via CLI, use the default example task
    task = args.task or DEFAULT_TASK
    
    print_header(f"Running Browser Task", f"Task: {task}")
    if args.headless:
        console.print("[info]Running in headless mode (browser will not be visible)")
    
    try:
        result = asyncio.run(run_task(task, headless=args.headless))
        print_status("Task completed successfully!")
        print_result(result, "Task Result")
        return 0
    except KeyboardInterrupt:
        console.print("\n[warning]Task interrupted by user.")
        return 1
    except Exception as e:
        logger.exception("Error running task")
        console.print(f"\n[error]Error running task: {str(e)}")
        return 1

def main_setup():
    """
    Entry point for the setup command.
    Runs only the setup process without executing a task.
    """
    parser = argparse.ArgumentParser(description="Set up the Browser Use CLI environment")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()
    
    # Set debug logging if requested
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    print_header("Browser Use CLI Setup", "Setting up the environment...")
    
    if setup_environment():
        console.print("\n[success]✅ Setup completed successfully!")
        console.print("\n[info]You can now run browser automation tasks with:")
        console.print("[highlight]  browser-task \"Your task here\"")
        return 0
    else:
        console.print("\n[error]❌ Setup failed. Please address the issues above and try again.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 