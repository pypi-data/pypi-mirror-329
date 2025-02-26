# Browser Use CLI

A command-line tool for browser automation tasks using LLMs.

## Prerequisites

- Python 3.11 or higher (required by browser-use)
- Google Chrome browser
- Google API key (get one from https://aistudio.google.com/apikey)
- `uv` package manager (recommended)

## Installation

### Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/sanjeed5/browser-use-cli.git
   cd browser-use-cli
   ```

2. Install `uv` if you don't have it already:
   ```bash
   curl -sSf https://install.python-uv.org | python3
   ```

3. Create and activate a virtual environment (recommended):
   ```bash
   uv venv --python 3.11
   # For Mac/Linux:
   source .venv/bin/activate
   # For Windows:
   .venv\Scripts\activate
   ```

4. Install the package:
   
   Using uv (recommended):
   ```bash
   uv pip install -e .
   ```
   
   Or using pip:
   ```bash
   pip install -e .
   ```

5. Run the setup command to configure your environment:
   ```bash
   browser-setup
   ```
   
   This will:
   - Check for required dependencies and install them if needed
   - Verify Chrome browser installation
   - Set up your Google API key
   - Install Playwright browsers

## Getting a Google API Key

To use this application, you need a Google API key for the Gemini model:

1. Visit [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Create a new API key
3. Add the API key to your `.env` file or enter it when prompted

## Testing Installation

To verify if the installation will work properly on your system or someone else's laptop, we've provided testing tools:

### Quick Verification

Run the verification script to check all prerequisites:

```bash
python -m browser_use_starter.verify_setup
```

### Complete Installation Test

For a comprehensive test that verifies all components:

- On Unix/macOS:
  ```bash
  chmod +x scripts/test_installation.sh
  ./scripts/test_installation.sh
  ```

- On Windows:
  ```
  scripts\test_installation.bat
  ```

For detailed testing instructions, see [docs/TESTING.md](docs/TESTING.md).

## Usage

Once installed, you can run browser tasks from anywhere in your terminal:

```bash
# Run with a specific task
browser-task "Go to google.com and search for the weather in New York"

# Run with the default example task
browser-task

# Run in headless mode (browser not visible)
browser-task --headless "Go to google.com and search for the weather"

# Enable debug logging
browser-task --debug "Your task here"
```

### Direct Module Execution

You can also run the agent module directly:

```bash
# Using uv (recommended)
uv run -m browser_use_starter.agent "Compare the price of gpt-4o and DeepSeek-V3"

# Using python
python -m browser_use_starter.agent "Compare the price of gpt-4o and DeepSeek-V3"

# Without specifying a task (uses default example)
python -m browser_use_starter.agent
```

## Examples

Here are some example tasks you can try:

- `browser-task "Go to amazon.com and search for wireless headphones under $100"`
- `browser-task "Go to youtube.com and find the most popular video about machine learning"`
- `browser-task "Go to wikipedia.com and find information about the Eiffel Tower"`
- `browser-task "Compare the price of gpt-4o and DeepSeek-V3"`

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```
GOOGLE_API_KEY=your_api_key_here
```

The application will prompt you to enter the API key if it's not found in the environment variables.

## Features

- Automatic dependency checking and installation
- Chrome browser detection
- Secure API key management
- Seamless browser automation using LLMs
- Headless mode support
- Detailed logging

## Configuration

API keys are stored securely in your user configuration directory:
- Linux/macOS: `~/.config/browser-use-cli/api_keys.env`
- Windows: `%USERPROFILE%\.config\browser-use-cli\api_keys.env`

## Troubleshooting

- Make sure Google Chrome is installed on your system
- Ensure all required packages are installed
- Check that your Google API key is valid and has access to the Gemini model
- If you encounter issues, refer to the [Browser Use documentation](https://docs.browser-use.com/quickstart)

## License

MIT
