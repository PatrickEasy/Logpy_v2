import datetime
import json
import os


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

if __name__ == "__main__":
    printtime("This is a single message")
    printtime(["This is a list item 1", "This is a list item 2", {"nested_dict_key": "nested_dict_value"}])
    printtime({"key1": "value1", "key2": ["list_item1", "list_item2"], "key3": {"nested_key": "nested_value"}})