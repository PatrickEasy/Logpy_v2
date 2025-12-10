import os

def find_files_with_extension(directory, extension):
    """
    Recursively searches for all files with the given extension in the specified directory.
    
    Args:
    directory (str): The directory path to search in.
    extension (str): The file extension to search for (e.g., '.txt', '.csv').
    
    Returns:
    list: A list of file paths that match the given extension.
    """
    matching_files = []
    
    # Traverse the directory tree
    for root, dirs, files in os.walk(directory):
        # Check each file in the current directory
        for file in files:
            if file.endswith(extension):
                matching_files.append(os.path.join(root, file))
    
    return matching_files

# Example usage:
directory_path = 'my-first-node-project'
file_extension = '.js'  # Change this to the desired extension
matching_files = find_files_with_extension(directory_path, file_extension)

# Output the list of files
for file in matching_files:
    print(file)
