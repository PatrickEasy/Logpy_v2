# Logpy_v2

A simple, reusable Python logging utility for timestamped console output and JSON file logging. Designed for easy integration across multiple personal projects.

## Overview

Logpy_v2 provides lightweight logging utilities with support for complex data structures, file searching, and log management. Perfect for projects that need quick, readable logging without heavy dependencies.

## Features

- **Timestamped Output**: Automatic timestamps on all console output
- **JSON Log Files**: Session-based JSON logs with structured data
- **Smart Data Handling**: Automatic formatting for strings, lists, dicts, and nested structures
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
from Logpy import printtime, log_message, find_files_with_extension, delete_log_files

# Simple timestamped output
printtime("Application started")

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

## API Reference

### `printtime(message, indent=0, log_to_file=True)`

Print timestamped messages with support for nested data structures.

**Parameters:**
- `message` (str, list, set, dict): Content to print
- `indent` (int): Indentation level for nested structures (default: 0)
- `log_to_file` (bool): Whether to save to JSON log file (default: True)

**Examples:**
```python
# Simple message
printtime("Server started on port 8000")

# Nested data with auto-formatting
printtime({
    "user": "admin",
    "permissions": ["read", "write", "delete"]
})

# Console only (no file logging)
printtime("Debug info", log_to_file=False)
```

### `log_message(time, message, folder="logs")`

Directly append a message to the JSON log file.

**Parameters:**
- `time` (str): Timestamp for the log entry
- `message` (str): The message to log
- `folder` (str): Directory for log file (default: "logs")

**Example:**
```python
import datetime
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log_message(timestamp, "Direct log entry")
```

### `find_files_with_extension(directory, extension, recursive=True)`

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

### `delete_log_files(directory=None, recursive=False)`

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

## Usage in Multiple Projects

Since this is designed as a reusable library for your personal projects:

### Option 1: Git Submodule (Recommended)
```bash
cd your-project
git submodule add https://github.com/PatrickEasy/Logpy_v2.git
```

Then import in your code:
```python
from Logpy import printtime, delete_log_files
```

### Option 2: Direct Clone
```bash
cd your-project
git clone https://github.com/PatrickEasy/Logpy_v2.git
```

Add to your Python path or import directly:
```python
import sys
sys.path.insert(0, 'Logpy_v2')
from Logpy import printtime
```

### Option 3: Copy Module
Simply copy the `Logpy/` directory into your project.

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/PatrickEasy/Logpy_v2.git
cd Logpy_v2

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# No additional dependencies needed - uses Python standard library only
```

### Running the Demo

```bash
python Logpy/printtime.py
```

This will demonstrate all functions and create a sample log file.

## Project Structure

```
Logpy_v2/
├── README.md
├── requirements.txt
├── .gitignore
├── venv/              # Virtual environment (excluded from git)
├── logs/              # Generated log files
└── Logpy/
    ├── __init__.py    # Package exports
    └── printtime.py   # Main implementation
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

### Version 2.0.0 (Current)
- Complete rewrite with improved structure
- Added file search utilities with recursive options
- Improved log cleanup functionality
- Better documentation and code comments
- Removed external dependencies

## Author

Patrick Easy

## Support

For issues or questions, please open an issue on the [GitHub repository](https://github.com/PatrickEasy/Logpy_v2/issues).

