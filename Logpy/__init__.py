"""
logpy - Simple logging utilities for Python projects

This package provides utilities for:
- Creating timestamped log files with JSON output
- Finding files by extension in directories
- Deleting log files automatically
"""

from .printtime import printtime, log_message
from .logdeleter import delete_log_files
from .filefinder import find_files_with_extension

__version__ = "0.1.0"
__all__ = ["printtime", "log_message", "delete_log_files", "find_files_with_extension"]
