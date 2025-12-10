import datetime
import json
import os
import glob

# Create a unique filename for each run
log_filename = datetime.datetime.now().strftime("log_%Y%m%d_%H%M%S.json")
log_data = []

def log_message(time, message, folder="logs"):
    log_entry = {
        "time": time,
        "message": message
    }
    log_data.append(log_entry)

    if not os.path.exists(folder):
        os.makedirs(folder)

    with open(f"{folder}/{log_filename}", 'w') as log_file:
        json.dump(log_data, log_file, indent=4)

def printtime(message, indent=0, log_to_file=True):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    indent_str = "\t" * indent

    if isinstance(message, str):
        log_entry = f"{indent_str}{message}"
        print(f"{current_time} - {log_entry}")
    elif isinstance(message, (list, set)):
        for item in message:
            printtime(item, indent + 1, log_to_file)
        return
    elif isinstance(message, dict):
        for key, value in message.items():
            log_entry = f"{indent_str}{key}:"
            print(f"{current_time} - {log_entry}")
            printtime(value, indent + 1, log_to_file)
        return
    else:
        log_entry = f"{indent_str}{str(message)}"
        print(f"{current_time} - {log_entry}")

    # Save log entry to log data
    if log_to_file:
        log_message(current_time, log_entry)


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
            print(f"Error accessing directory {directory}: {e}")
    
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
        print(f"No log files found {search_type} {directory_path}")
        return 0
    
    deleted_count = 0
    for log_file in log_files:
        try:
            os.remove(log_file)
            print(f"Deleted log file: {log_file}")
            deleted_count += 1
        except OSError as e:
            print(f"Error deleting file {log_file}: {e}")
    
    return deleted_count

if __name__ == "__main__":
    print("=" * 60)
    print("LOGPY DEMONSTRATION")
    print("=" * 60)
    
    # Demonstrate printtime() with different data types
    print("\n1. PRINTTIME - Simple string message:")
    printtime("This is a single message")
    
    print("\n2. PRINTTIME - List with nested dictionary:")
    printtime(["This is a list item 1", "This is a list item 2", {"nested_dict_key": "nested_dict_value"}])
    
    print("\n3. PRINTTIME - Complex nested dictionary:")
    printtime({"key1": "value1", "key2": ["list_item1", "list_item2"], "key3": {"nested_key": "nested_value"}})
    
    print("\n4. PRINTTIME - Without logging to file:")
    printtime("This message won't be logged to file", log_to_file=False)
    
    # Demonstrate log_message() directly
    print("\n5. LOG_MESSAGE - Direct log entry:")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message(current_time, "Direct log entry example")
    printtime("Log message added directly to log file")
    
    # Demonstrate find_files_with_extension()
    print("\n6. FIND_FILES_WITH_EXTENSION - Finding Python files:")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    py_files = find_files_with_extension(current_dir, ".py")
    printtime(f"Found {len(py_files)} Python file(s) in {current_dir}:")
    for file in py_files:
        printtime(f"  - {os.path.basename(file)}", indent=1)
    
    # Demonstrate combined usage
    print("\n7. COMBINED USAGE - Real-world scenario:")
    printtime("Starting file scan...")
    json_files = find_files_with_extension(os.path.dirname(current_dir), ".json")
    printtime(f"Found {len(json_files)} JSON file(s)")
    if json_files:
        printtime("JSON files found:", indent=0)
        for json_file in json_files[:3]:  # Show first 3 only
            printtime(os.path.basename(json_file), indent=1)
    
    print("\n8. DELETE_LOG_FILES - Cleanup demonstration:")
    printtime("Current log file will be preserved for this demo")
    printtime("To delete logs, uncomment the line below:")
    delete_log_files('logs')  # Uncomment to enable deletion
    print("# delete_log_files('logs')")
    
    print("\n" + "=" * 60)
    printtime(f"Demo complete! Check 'logs/{log_filename}' for the log output")
    print("=" * 60)