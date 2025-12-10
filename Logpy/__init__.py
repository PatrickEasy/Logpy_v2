"""
Logpy - Simple logging utilities for Python projects

This package provides utilities for:
- Creating timestamped log files with JSON output
- Structured console output with timestamps
- Finding files by extension in directories
- Deleting log files automatically

Example usage:
    from Logpy import printtime, log_message, delete_log_files, find_files_with_extension
    
    # Log a simple message
    printtime("Application started")
    
    # Log complex data structures
    printtime({"status": "running", "items": [1, 2, 3]})
    
    # Find all Python files in a directory
    py_files = find_files_with_extension("/path/to/dir", ".py")
    
    # Clean up log files
    delete_log_files("logs")
"""

from .printtime import (
    printtime,
    log_message,
    delete_log_files,
    find_files_with_extension
)

__version__ = "2.0.0"
__author__ = "Patrick Easy"
__all__ = [
    "printtime",
    "log_message",
    "delete_log_files",
    "find_files_with_extension"
]
