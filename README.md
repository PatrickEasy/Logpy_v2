# Logpy_v2

A simple, reusable Python logging utility for timestamped console output, JSON file logging, and function timing. Designed for easy integration across multiple personal projects.

## Overview

Logpy_v2 provides lightweight logging utilities with support for complex data structures, automatic session timing, flexible function timing, file searching, and log management. Perfect for projects that need quick, readable logging without heavy dependencies.

## Features

- **Timestamped Output**: Automatic timestamps on all console output
- **Session Time Tracking**: Automatically tracks elapsed time for each log entry since session start
- **JSON Log Files**: Session-based JSON logs with structured data and timing information
- **Smart Data Handling**: Automatic formatting for strings, lists, dicts, and nested structures
- **Flexible Timer Class**: Multiple timing patterns - decorator, context manager, and manual control
- **Zero-Overhead Timing**: Query elapsed time without active monitoring
- **Works with Recursive Functions**: Each function call is timed independently
- **Long-Running Process Support**: Check progress without stopping timer
- **File Utilities**: Search for files by extension with recursive/non-recursive options
- **Log Management**: Clean up old log files easily
- **Zero Dependencies**: Uses only Python standard library

## Installation

### From Private GitHub Repository (Recommended)

Add to your project's `requirements.txt`:

```
# Using SSH (recommended for private repos)
git+ssh://git@github.com/PatrickEasy/Logpy_v2.git

# Or using HTTPS with personal access token
git+https://github.com/PatrickEasy/Logpy_v2.git
```

Then install:
```bash
pip install -r requirements.txt
```

**Note for private repos**: Ensure you have SSH keys configured or use a GitHub Personal Access Token for authentication.

### From Source

```bash
git clone https://github.com/PatrickEasy/Logpy_v2.git
cd Logpy_v2
pip install -e .
```

## Quick Start

```python
from Logpy import printtime, Timer, timed, get_session_elapsed
import time

# Simple timestamped output with automatic session elapsed time tracking
printtime("Application started")  # Logs: time, message, elapsed: 0s

time.sleep(1)
printtime("1 second later")  # Logs: time, message, elapsed: 1.0s

# Time a function with decorator
@timed("process_data")
def process_data(items):
    time.sleep(0.5)
    return len(items)

result = process_data([1, 2, 3])  # Automatically logs: "Timer 'process_data' completed: 500ms"

# Time a code block with context manager
with Timer("database_query"):
    # Your database query here
    time.sleep(0.3)
    results = ["result1", "result2"]

# Manual timer for long-running operations with progress checks
timer = Timer("processing", auto_log=False)
timer.start()
for i, item in enumerate(range(100)):
    # Process item...
    if i % 25 == 0:  # Check progress periodically
        printtime(f"Progress: {i}% - Running for {timer.elapsed():.1f}s")
elapsed = timer.stop()
printtime(f"Processing complete in {elapsed:.2f}s")

# Check total session elapsed time
printtime(f"Total session time: {get_session_elapsed():.2f}s")

# Log complex structures with automatic formatting
printtime({
    "status": "running",
    "config": {
        "debug": True,
        "items": [1, 2, 3]
    }
})

# Find files by extension
py_files = find_files_with_extension("/path/to/dir", ".py")
printtime(f"Found {len(py_files)} Python files")

# Clean up old logs
deleted = delete_log_files("logs", recursive=True)
printtime(f"Deleted {deleted} log files")
```

### Log File Output

Each log entry automatically includes elapsed time since session start:

```json
[
    {
        "time": "2025-12-10 14:30:45",
        "message": "Application started",
        "elapsed": 0.0,
        "elapsed_formatted": "0ms"
    },
    {
        "time": "2025-12-10 14:30:46",
        "message": "1 second later",
        "elapsed": 1.002,
        "elapsed_formatted": "1.00s"
    },
    {
        "time": "2025-12-10 14:30:46",
        "message": "Timer 'process_data' completed: 500.25ms",
        "elapsed": 1.503,
        "elapsed_formatted": "1.50s"
    }
]
```

## API Reference

### Session Timing Functions

#### `get_session_elapsed()`

Get the elapsed time since the current log session started (when the module was imported).

**Returns:** `float` - Elapsed time in seconds

**Example:**
```python
from Logpy import get_session_elapsed
import time

time.sleep(2)
elapsed = get_session_elapsed()
print(f"Session has been running for {elapsed:.2f}s")
```

#### `reset_session_timer()`

Reset the session timer to start from now. Useful when you want to restart timing without reimporting the module.

**Example:**
```python
from Logpy import reset_session_timer, printtime

printtime("First message")
# ... do some work ...
reset_session_timer()
printtime("Timer reset, this will show 0s elapsed")
```

### Timer Class and Functions

#### `Timer(name=None, auto_log=True, log_to_file=True)`

Flexible timer class for measuring execution time of specific operations.

**Parameters:**
- `name` (str): Optional name for the timer. Defaults to unique ID.
- `auto_log` (bool): If True, automatically logs when timer stops.
- `log_to_file` (bool): If True, logs are written to file via printtime.

**Usage:**
```python
# Context manager
with Timer("operation"):
    do_work()

# Manual control
timer = Timer("task", auto_log=False)
timer.start()
while working:
    do_work()
    # Check progress without stopping
    if timer.elapsed() > 60:
        print(f"Still running: {timer.elapsed():.1f}s")
elapsed = timer.stop()
print(f"Completed in {elapsed:.2f}s")

# Decorator
@Timer.decorator("function_name")
def my_function():
    pass
```

**Methods:**
- `start()` - Start timing, returns self for chaining
- `stop()` - Stop and return elapsed time in seconds
- `elapsed()` - Get current elapsed time (works while running or after stopped)
- `is_running()` - Check if timer is currently active
- `reset()` - Reset to initial state

**Class Methods:**
- `Timer.decorator(name, auto_log, log_to_file)` - Returns function decorator
- `Timer.get(name)` - Get a named timer from registry
- `Timer.register(name, timer)` - Register timer for global access
- `Timer.unregister(name)` - Remove timer from registry
- `Timer.clear_registry()` - Clear all registered timers

**Static Methods:**
- `Timer._format_time(seconds)` - Format seconds to human-readable string

See [TIMER.md](TIMER.md) for complete Timer documentation with advanced examples.

#### `timed(name=None, auto_log=True, log_to_file=True)`

Decorator shorthand for timing functions.

**Example:**
```python
@timed("process_data")
def process_data(items):
    # Automatically logs execution time
    return processed_items
```

### Logging Functions

#### `printtime(message, indent=0, log_to_file=True, include_elapsed=True)`

Print timestamped messages with support for nested data structures. Automatically tracks and logs elapsed time since session start.

**Parameters:**
- `message` (str, list, set, dict): Content to print
- `indent` (int): Indentation level for nested structures (default: 0)
- `log_to_file` (bool): Whether to save to JSON log file (default: True)
- `include_elapsed` (bool): Whether to include session elapsed time in log file (default: True)

**Examples:**
```python
# Simple message with automatic elapsed time tracking
printtime("Server started on port 8000")

# Nested data with auto-formatting
printtime({
    "user": "admin",
    "permissions": ["read", "write", "delete"]
})

# Console only (no file logging)
printtime("Debug info", log_to_file=False)

# Log without elapsed time tracking
printtime("Manual timestamp only", include_elapsed=False)
```

#### `log_message(time, message, folder="logs", elapsed=None)`

Directly append a message to the JSON log file.

**Parameters:**
- `time` (str): Timestamp for the log entry
- `message` (str): The message to log
- `folder` (str): Directory for log file (default: "logs")
- `elapsed` (float): Optional elapsed time in seconds to include in log

**Example:**
```python
import datetime
from Logpy import log_message, get_session_elapsed

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
elapsed = get_session_elapsed()
log_message(timestamp, "Direct log entry", elapsed=elapsed)
```

### File Utilities

#### `find_files_with_extension(directory, extension, recursive=True)`

Find all files with a specific extension in a directory.

**Parameters:**
- `directory` (str): Path to search in
- `extension` (str): File extension to match (e.g., ".py", ".json")
- `recursive` (bool): Search subdirectories (default: True)

**Returns:** List of file paths

**Examples:**
```python
# Find all Python files recursively
py_files = find_files_with_extension("/project", ".py")

# Find JSON files in directory only (not subdirectories)
json_files = find_files_with_extension("/data", ".json", recursive=False)
```

#### `delete_log_files(directory=None, recursive=False)`

Delete all log files matching the pattern `log_*.json`.

**Parameters:**
- `directory` (str): Directory to search (default: current directory)
- `recursive` (bool): Search subdirectories (default: False)

**Returns:** Number of files deleted (int)

**Examples:**
```python
# Delete logs in specific directory
delete_log_files("logs")

# Delete logs recursively
count = delete_log_files("logs", recursive=True)

# Delete logs in current directory
delete_log_files()
```

## Log File Format

Logs are saved as JSON files with the naming pattern `log_YYYYMMDD_HHMMSS.json`. Each entry includes timestamps and elapsed time:

```json
[
    {
        "time": "2025-12-10 14:30:45",
        "message": "Application started",
        "elapsed": 0.0,
        "elapsed_formatted": "0ms"
    },
    {
        "time": "2025-12-10 14:30:46",
        "message": "Processing 100 items",
        "elapsed": 1.234,
        "elapsed_formatted": "1.23s"
    },
    {
        "time": "2025-12-10 14:31:50",
        "message": "Timer 'database_query' completed: 325.50ms",
        "elapsed": 65.789,
        "elapsed_formatted": "1m 5.8s"
    }
]
```

**Fields:**
- `time` - Human-readable timestamp (YYYY-MM-DD HH:MM:SS)
- `message` - The log message
- `elapsed` - Seconds since session start (3 decimal precision)
- `elapsed_formatted` - Human-readable elapsed time (e.g., "1m 5.8s")

## Usage in Multiple Projects

The recommended way to use Logpy in other projects is via pip installation from the GitHub repository. See [USAGE.md](USAGE.md) for complete installation instructions.

### Quick Setup

Add to your project's `requirements.txt`:
```
git+ssh://git@github.com/PatrickEasy/Logpy_v2.git
```

Then install:
```bash
pip install -r requirements.txt
```

Import in your code:
```python
from Logpy import printtime, Timer, timed, get_session_elapsed
```

See [USAGE.md](USAGE.md) for authentication options, CI/CD integration, and troubleshooting.

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/PatrickEasy/Logpy_v2.git
cd Logpy_v2

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode
pip install -e .

# No additional dependencies needed - uses Python standard library only
```

### Running Demos

```bash
# Printtime and logging demo
python Logpy/printtime.py

# Timer demo
python Logpy/timer.py
```

Both demos will create sample log files showing all features.

## Project Structure

```
Logpy_v2/
├── README.md              # Main documentation
├── USAGE.md              # Installation and requirements.txt guide
├── TIMER.md              # Complete Timer documentation
├── requirements.txt      # No dependencies (Python stdlib only)
├── pyproject.toml        # Package configuration for pip
├── .gitignore
├── venv/                 # Virtual environment (excluded from git)
├── logs/                 # Generated log files
└── Logpy/
    ├── __init__.py       # Package exports
    ├── printtime.py      # Logging and session timing
    └── timer.py          # Timer class implementation
```

## Log File Format

Logs are saved as JSON files with the naming pattern `log_YYYYMMDD_HHMMSS.json`:

```json
[
    {
        "time": "2025-12-10 14:30:45",
        "message": "Application started"
    },
    {
        "time": "2025-12-10 14:30:46",
        "message": "Processing complete"
    }
]
```

## Contributing

This is a personal project, but suggestions and improvements are welcome. Feel free to open issues or submit pull requests.

## License

MIT License - feel free to use this in your personal projects.

## Changelog

### Version 2.1.0 (Current)
- **New**: Timer class with decorator, context manager, and manual control
- **New**: Automatic session elapsed time tracking for all log entries
- **New**: `get_session_elapsed()` and `reset_session_timer()` functions
- **New**: Human-readable time formatting (ms, seconds, minutes, hours)
- **Enhanced**: `printtime()` now includes `include_elapsed` parameter
- **Enhanced**: `log_message()` now accepts optional `elapsed` parameter
- **Enhanced**: Log files now include `elapsed` and `elapsed_formatted` fields
- **Enhanced**: Complete Timer documentation in TIMER.md
- **Enhanced**: Package now installable via pip from GitHub
- Added file search utilities with recursive options
- Improved log cleanup functionality
- Better documentation and code comments
- Zero external dependencies (Python stdlib only)

## Author

Patrick Easy

## Support

For issues or questions, please open an issue on the [GitHub repository](https://github.com/PatrickEasy/Logpy_v2/issues).

## Additional Documentation

- [USAGE.md](USAGE.md) - Complete guide for using Logpy in other projects via requirements.txt
- [TIMER.md](TIMER.md) - Comprehensive Timer documentation with advanced examples and use cases

