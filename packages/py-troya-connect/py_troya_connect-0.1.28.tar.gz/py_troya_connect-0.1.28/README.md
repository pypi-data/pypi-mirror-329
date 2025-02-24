# py-troya-connect

A Python interface for Attachmate Extra Terminal sessions.

## Installation

```bash
pip install py-troya-connect
```

## Quick Start

```python
from py_troya_connect import ExtraTerminal

# Connect to first available session
terminal = ExtraTerminal("1")

# Send command and read response
terminal.send_command("your_command")
screen_text = terminal.read_screen()
```

## Interactive Session Selection

```python
# Let user choose session
session_choice = ExtraTerminal.select_session()
terminal = ExtraTerminal(session_choice)

# Read current screen
screen_text = terminal.read_screen()
```

## Error Handling

```python
from py_troya_connect import ExtraTerminal, TerminalBusyError

try:
    terminal = ExtraTerminal("1")
    terminal.send_command("command")
    
    # Wait for specific text with timeout
    if terminal.wait_for_text("Expected text", timeout=10):
        print("Text found!")
except TerminalBusyError:
    print("Terminal is busy")
```

## System Status Check

```python
terminal = ExtraTerminal("1")
status = terminal.check_system_status()
# Returns: {'Extra Version': '1.0', 'Session Count': 2, 'Available Sessions': ['Session1', 'Session2']}
```

## Requirements

- Windows OS
- Attachmate Extra! Terminal
- Python 3.6+
- pywin32

## License

MIT License
