"""
Logpy - Simple logging and timing utilities for Python projects

This package provides utilities for:
- Creating timestamped log files with JSON output and automatic elapsed time tracking
- Structured console output with timestamps
- Flexible function and code block timing (decorator, context manager, manual)
- Session elapsed time tracking for all log entries
- Finding files by extension in directories
- Deleting log files automatically

Example usage:
    from Logpy import printtime, Timer, timed, get_session_elapsed
    import time
    
    # Log with automatic session elapsed time tracking
    printtime("Application started")  # Shows elapsed: 0s in log file
    time.sleep(1)
    printtime("1 second later")  # Shows elapsed: 1.0s in log file
    
    # Time a function with decorator
    @timed("process_data")
    def process_data(items):
        return len(items)
    
    # Time a code block with context manager
    with Timer("database_query"):
        results = query_database()
    
    # Manual timer for long operations with progress checks
    timer = Timer("processing", auto_log=False)
    timer.start()
    for item in items:
        process(item)
        if timer.elapsed() > 60:
            print(f"Still running: {timer.elapsed():.1f}s")
    timer.stop()
    
    # Check session elapsed time
    print(f"Total session time: {get_session_elapsed():.2f}s")
    
    # Find all Python files in a directory
    py_files = find_files_with_extension("/path/to/dir", ".py")
    
    # Clean up log files
    delete_log_files("logs")
"""

from .printtime import (
    printtime,
    log_message,
    delete_log_files,
    find_files_with_extension,
    get_session_elapsed,
    reset_session_timer
)

from .timer import (
    Timer,
    timed
)

__version__ = "2.1.0"
__author__ = "Patrick Easy"
__all__ = [
    "printtime",
    "log_message",
    "delete_log_files",
    "find_files_with_extension",
    "get_session_elapsed",
    "reset_session_timer",
    "Timer",
    "timed"
]
