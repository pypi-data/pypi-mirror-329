# py-troya-connect

A Python interface for Attachmate Extra Terminal sessions.

## Installation

```bash
pip install py-troya-connect
```

## Basic Usage

```python
from py_troya_connect import ExtraTerminal

# Initialize terminal connection
terminal = ExtraTerminal("1")  # Connect to session 1

# Read screen content
screen_content = terminal.read_screen()
print("Screen content:", screen_content)

# Send a command and get response
terminal.send_command("your_command")
response = terminal.read_screen()
print("Command response:", response)
```

## Session Selection

```python
from py_troya_connect import ExtraTerminal

# List available sessions
terminal = ExtraTerminal("1")
sessions = terminal.list_available_sessions()
print("Available sessions:", sessions)
# Output: [{'index': 1, 'name': 'Session1', 'connected': True}, ...]

# Interactive session selection
session_choice = ExtraTerminal.select_session()
new_terminal = ExtraTerminal(session_choice)
```

## Advanced Usage

```python
from py_troya_connect import ExtraTerminal

# Initialize connection
terminal = ExtraTerminal("1")

# Check system status
status = terminal.check_system_status()
print("System status:", status)

# Send command with special keys
terminal.send_command("command{ENTER}")  # Will be formatted as "command<ENTER>"

# Wait for specific text to appear
if terminal.wait_for_text("Expected text", timeout=30):
    print("Text found!")
    response = terminal.read_screen()
    print("Current screen:", response)
```

## Requirements

- Windows OS
- Attachmate Extra! Terminal
- Python 3.6+
- pywin32

## License

MIT License
