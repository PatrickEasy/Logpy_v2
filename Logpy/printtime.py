import datetime
import json
import os
import time as time_module

# Import printing utilities from the sibling module.
# Use a relative import when running as part of the package, and fall back
# to an absolute import when this file is executed as a script.
try:
    from .print_utils import smart_print, C, title, msg, ok, info, err, ask
except ImportError:
    from print_utils import smart_print, C, title, msg, ok, info, err, ask


# Create a unique filename for each run
log_filename = datetime.datetime.now().strftime("log_%Y%m%d_%H%M%S.json")
log_data = []


# Session timer - tracks elapsed time since log session started
_session_start_time = time_module.perf_counter()

# Printing functions are now imported from print_utils module

def _format_elapsed(seconds):

    """
    Format elapsed time in a human-readable way.
    
    """

    if seconds < 1:
        return f"{seconds * 1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.1f}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        return f"{hours}h {minutes}m {secs:.1f}s"


def get_session_elapsed():
    
    """
    Get the elapsed time since the log session started.
    
    Returns:
        float: Elapsed time in seconds.

    """

    return time_module.perf_counter() - _session_start_time


def reset_session_timer():

    """
    Reset the session timer to start from now.
    
    """

    global _session_start_time
    _session_start_time = time_module.perf_counter()


def log_message(time, message, folder="logs", elapsed=None):

    """
    Logs a message with a timestamp to a JSON file. Creates the log file if it doesn't exist.
    
    Args:
    time (str):     The timestamp of the log entry.
    message (str):  The log message.
    folder (str):   The folder to save the log file in. Default is 'logs'.
                    If the folder does not exist, it will be created.
                    If none, the log file will be saved in the current directory.
    elapsed (float): Optional elapsed time in seconds since session start.
                     If provided, adds 'elapsed' and 'elapsed_formatted' to log entry.
    
    """

    log_entry = {
        "time": time,
        "message": message
    }
    
    # Add elapsed time if provided
    if elapsed is not None:
        log_entry["elapsed"] = round(elapsed, 3)
        log_entry["elapsed_formatted"] = _format_elapsed(elapsed)
    
    log_data.append(log_entry)

    if not os.path.exists(folder):
        os.makedirs(folder)

    with open(f"{folder}/{log_filename}", 'w') as log_file:
        json.dump(log_data, log_file, indent=4)


def printtime(message, indent=0, log_to_file=True, include_elapsed=True ,msg_type=False, new_line=True, trailing_newline=True):

    """
    Prints a message to the console with a timestamp. Supports strings, lists, sets, and
    dictionaries. Optionally logs the message to a JSON log file with elapsed time tracking.
    
    Args:
    message (str, list, set, dict): The message to print.
    indent (int):   The indentation level for nested structures.
    log_to_file (bool): If True, logs the message to a JSON file.
    include_elapsed (bool): If True, includes elapsed time since session start in log file.

    """

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elapsed = get_session_elapsed() if include_elapsed else None
    indent_str = "\t" * indent

    if new_line:
        print()  # Print a new line before the message

    if isinstance(message, str):
        log_entry = f"{indent_str}{message}"
        smart_print(f"{current_time} - {log_entry}", msg_type=msg_type)

    elif isinstance(message, (list, set)):
        for item in message:
            printtime(item, indent + 1, log_to_file, include_elapsed, msg_type=msg_type)
        return
    
    elif isinstance(message, dict):
        for key, value in message.items():
            log_entry = f"{indent_str}{key}:"
            smart_print(f"{current_time} - {log_entry}", msg_type=msg_type)
            printtime(value, indent + 1, log_to_file, include_elapsed, msg_type=msg_type)
        return
    
    else:
        log_entry = f"{indent_str}{str(message)}"
        smart_print(f"{current_time} - {log_entry}", msg_type=msg_type)

    # Save log entry to log data with elapsed time
    if log_to_file:
        log_message(current_time, log_entry, elapsed=elapsed)

    if trailing_newline:
        print()  # Print a new line after the message


def find_files_with_extension(directory, extension, recursive=True):

    """
    Searches for all files with the given extension in the specified directory.
    
    Args:
    directory (str): The directory path to search in.
    extension (str): The file extension to search for (e.g., '.txt', '.csv').
    recursive (bool): If True (default), searches recursively in subdirectories.
                      If False, only searches in the specified directory.
    
    Returns:
    list: A list of file paths that match the given extension.

    """

    matching_files = []
    
    if recursive:
        # Traverse the directory tree recursively
        for root, dirs, files in os.walk(directory):
            # Check each file in the current directory
            for file in files:
                if file.endswith(extension):
                    matching_files.append(os.path.join(root, file))
    else:
        # Only search in the specified directory (non-recursive)
        try:
            for file in os.listdir(directory):
                file_path = os.path.join(directory, file)
                # Check if it's a file (not a directory) and has the extension
                if os.path.isfile(file_path) and file.endswith(extension):
                    matching_files.append(file_path)
        except OSError as e:
            smart_print(f"Error accessing directory {directory}: {e}", "err")
    
    return matching_files


def delete_log_files(directory=None, recursive=False):

    """
    Deletes log files matching the pattern 'log_*.json' in the specified directory.
    
    Args:
    directory (str): Directory path to search for log files.
                     If None, uses current working directory.
    recursive (bool): If True, searches recursively in subdirectories.
                     If False (default), only searches in the specified directory.
    
    Returns:
    int: Number of log files deleted.

    """

    # Default to the current directory if no directory is specified
    if directory is None:
        directory = os.getcwd()
    
    directory_path = os.path.abspath(directory)
    
    # Use find_files_with_extension to locate log files
    log_files = find_files_with_extension(directory_path, ".json", recursive=recursive)
    
    # Filter to only include files matching the log pattern
    log_files = [f for f in log_files if os.path.basename(f).startswith("log_")]
    
    if not log_files:
        search_type = "recursively" if recursive else "in"
        smart_print(f"No log files found {search_type} {directory_path}", "info")
        return 0
    
    deleted_count = 0
    for log_file in log_files:
        try:
            os.remove(log_file)
            smart_print(f"Deleted log file: {log_file}", "ok")
            deleted_count += 1
        except OSError as e:
            smart_print(f"Error deleting file {log_file}: {e}", "err")
    
    return deleted_count


# ==============================================================================
# DEMO / TESTING
# ==============================================================================


if __name__ == "__main__":
    print('\n')
    print("=" * 70)
    print("LOGPY DEMONSTRATION")
    print("=" * 70)
    
    # Demo 1: Simple messages
    smart_print("[1] PRINTTIME - Simple messages", "title")
    printtime("This is a single message")
    
    # Demo 2: Lists and nested structures
    smart_print("[2] PRINTTIME - List with nested dictionary", "title")
    printtime([
        "List item 1",
        "List item 2",
        {"nested_key": "nested_value"}
    ])
    
    # Demo 3: Complex dictionaries
    smart_print("[3] PRINTTIME - Complex nested dictionary", "title")
    printtime({
        "key1": "value1",
        "key2": ["list_item1", "list_item2"],
        "key3": {"nested_key": "nested_value"}
    })
    
    # Demo 4: Console-only output
    smart_print("[4] PRINTTIME - Without file logging", "title")
    printtime("This message won't be logged to file", log_to_file=False)
    
    # Demo 5: Direct log entry
    smart_print("[5] LOG_MESSAGE - Direct log entry", "title")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message(current_time, "Direct log entry example")
    printtime("Log message added directly to log file")
    
    # Demo 6: File finding
    smart_print("[6] FIND_FILES_WITH_EXTENSION - Finding Python files", "title")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    py_files = find_files_with_extension(current_dir, ".py")
    printtime(f"Found {len(py_files)} Python file(s) in current directory")
    for file in py_files:
        printtime(f"- {os.path.basename(file)}", indent=1)
    
    # Demo 7: Combined usage scenario
    smart_print("[7] COMBINED USAGE - Real-world scenario", "title")
    printtime("Starting file scan...")
    json_files = find_files_with_extension(os.path.dirname(current_dir), ".json")
    printtime(f"Found {len(json_files)} JSON file(s)")
    if json_files:
        printtime("First 3 JSON files:", indent=0)
        for json_file in json_files[:3]:
            printtime(os.path.basename(json_file), indent=1)
    
    # Demo 8: Log cleanup (commented out for safety)
    smart_print("[8] DELETE_LOG_FILES - Cleanup demonstration", "title")
    printtime("Log cleanup is available but disabled in demo")
    printtime("To enable: delete_log_files('logs', recursive=True)")
    # Uncomment below to actually delete logs:
    deleted = delete_log_files('logs')
    printtime(f"Deleted {deleted} log file(s)", msg_type="info")
    
    print("\n" + "=" * 70)
    printtime(f"Demo complete! View log at: logs/{log_filename}")
    print("=" * 70)
    print('\n')

    #delete_log_files('logs')
