import os
import glob

def delete_log_files(folders=None):
    # Default to the current directory if no folders are specified
    if folders is None:
        folders = [os.getcwd()]
    elif isinstance(folders, str):
        folders = [folders]
    
    log_pattern = "log_*.json"
    
    for folder in folders:
        folder_path = os.path.abspath(folder)
        log_files = glob.glob(os.path.join(folder_path, log_pattern))
        
        if log_files == []:
            print(f"No log files found in {folder_path}")
        else:
            for log_file in log_files:
                try:
                    os.remove(log_file)
                    print(f"Deleted log file: {log_file}")
                except OSError as e:
                    print(f"Error deleting file {log_file}: {e}")

# Example usage:
# delete_log_files()  # Deletes log files in the current directory
# delete_log_files("path/to/your/folder")  # Deletes log files in a specific folder
# delete_log_files(["path/to/your/folder1", "path/to/your/folder2"])  # Deletes log files in multiple folders

if __name__ == "__main__":
    delete_log_files()
    delete_log_files("logs")