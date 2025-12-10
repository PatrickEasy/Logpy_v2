# Timer Usage Guide

The `Timer` class provides flexible timing capabilities for measuring function execution time with zero overhead while running.

## Key Features

- **Zero overhead while running** - Only calculates time when you request it
- **Query elapsed time while running** - Check progress without stopping the timer
- **Multiple usage patterns** - Context manager, decorator, or manual control
- **Works with recursive functions** - Each invocation is independent
- **Works with long-running processes** - GUIs, servers, indefinite loops
- **Automatic logging integration** - Uses `printtime()` for consistent output
- **Human-readable formatting** - Displays times as ms, seconds, minutes, or hours

## Quick Examples

### Context Manager (Simplest)

```python
from Logpy import Timer

# Time a block of code
with Timer("database_query"):
    result = db.execute(query)
```

### Decorator (For Functions)

```python
from Logpy import timed

@timed("process_data")
def process_data(items):
    # Your code here
    return processed_items

# Timer automatically logs when function completes
result = process_data(my_items)
```

### Manual Control (Most Flexible)

```python
from Logpy import Timer

timer = Timer("long_operation", auto_log=False)
timer.start()

while processing:
    do_work()
    # Check progress without stopping
    if timer.elapsed() > 60:
        print(f"Still running: {timer.elapsed():.1f}s")

elapsed = timer.stop()
print(f"Completed in {elapsed:.2f}s")
```

## Usage Patterns

### 1. Timing a Simple Code Block

```python
from Logpy import Timer
import time

with Timer("sleep_test"):
    time.sleep(2)

# Output: Timer 'sleep_test' completed: 2.00s
```

### 2. Timing a Function with Decorator

```python
from Logpy import timed

@timed("calculate_fibonacci")
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

result = fibonacci(30)
# Output: Timer 'calculate_fibonacci' completed: 512.33ms
```

### 3. Checking Progress During Execution

```python
from Logpy import Timer

timer = Timer("data_processing", auto_log=False)
timer.start()

for i, item in enumerate(large_dataset):
    process(item)
    
    # Check every 100 items
    if i % 100 == 0:
        elapsed = timer.elapsed()
        print(f"Processed {i} items in {elapsed:.1f}s")

timer.stop()
```

### 4. Long-Running GUI Application

```python
from Logpy import Timer

class MyApplication:
    def __init__(self):
        self.uptime_timer = Timer("app_uptime", auto_log=False)
        self.uptime_timer.start()
    
    def get_uptime(self):
        """Check how long the app has been running."""
        return self.uptime_timer.elapsed()
    
    def on_status_check(self):
        uptime = self.get_uptime()
        print(f"Application uptime: {Timer._format_time(uptime)}")

# App can run indefinitely, checking uptime whenever needed
```

### 5. Multiple Simultaneous Timers

```python
from Logpy import Timer

# Track different operations
download_timer = Timer("download", auto_log=False).start()
process_timer = Timer("processing", auto_log=False).start()

# Do work...

print(f"Download: {download_timer.elapsed():.2f}s")
print(f"Processing: {process_timer.elapsed():.2f}s")

download_timer.stop()
process_timer.stop()
```

### 6. Using the Timer Registry

```python
from Logpy import Timer

# Register timers for global access
Timer.register("global_op", Timer("global_op", auto_log=False).start())

# Access from anywhere in your code
def check_progress():
    timer = Timer.get("global_op")
    if timer and timer.is_running():
        print(f"Elapsed: {timer.elapsed():.2f}s")

# Clean up
Timer.get("global_op").stop()
Timer.unregister("global_op")
```

### 7. Recursive Functions

```python
from Logpy import timed

@timed("recursive_search")
def deep_search(node, target):
    if node.value == target:
        return node
    
    for child in node.children:
        result = deep_search(child, target)
        if result:
            return result
    
    return None

# Each call is timed independently
result = deep_search(root, target_value)
```

### 8. Silent Timing (No Logging)

```python
from Logpy import Timer

# Timer that doesn't log anything
with Timer("silent", auto_log=False, log_to_file=False) as t:
    expensive_operation()

# Manually get the time
elapsed = t.elapsed()
print(f"Operation took {elapsed:.2f}s")
```

## API Reference

### Timer Class

#### Constructor

```python
Timer(name=None, auto_log=True, log_to_file=True)
```

**Parameters:**
- `name` (str): Optional name for the timer. Defaults to unique ID.
- `auto_log` (bool): If True, automatically logs when timer stops.
- `log_to_file` (bool): If True, logs are written to file via printtime.

#### Methods

**`start()`**
- Start the timer
- Returns: self (for chaining)

**`stop()`**
- Stop the timer and optionally log result
- Returns: elapsed time in seconds (float)

**`elapsed()`**
- Get elapsed time since start
- Can be called while running or after stopped
- Returns: elapsed time in seconds (float), or None if not started

**`is_running()`**
- Check if timer is currently running
- Returns: bool

**`reset()`**
- Reset timer to initial state
- Returns: None

#### Class Methods

**`Timer.decorator(name=None, auto_log=True, log_to_file=True)`**
- Returns a decorator for timing functions
- Parameters same as constructor

**`Timer.get(name)`**
- Get a named timer from registry
- Returns: Timer instance or None

**`Timer.register(name, timer)`**
- Register a timer for global access

**`Timer.unregister(name)`**
- Remove timer from registry

**`Timer.clear_registry()`**
- Clear all registered timers

### Convenience Functions

**`timed(name=None, auto_log=True, log_to_file=True)`**

Shorter alias for `Timer.decorator()`.

```python
from Logpy import timed

@timed("my_function")
def my_function():
    pass
```

## Time Formatting

The Timer automatically formats times in human-readable format:

- Less than 1 second: `512.33ms`
- Less than 1 minute: `2.50s`
- Less than 1 hour: `1m 5.30s`
- 1 hour or more: `1h 2m 5.80s`

Access formatting directly:

```python
formatted = Timer._format_time(125.5)  # "2m 5.50s"
```

## Integration with printtime

Timer automatically integrates with `printtime()` for consistent logging:

```python
from Logpy import Timer, printtime

with Timer("operation"):
    # Your code
    pass

# Timer output uses same timestamp format as printtime
# 2025-12-10 14:30:45 - Timer 'operation' completed: 1.23s
```

## Best Practices

### For Short Functions
Use the decorator:
```python
@timed("function_name")
def my_function():
    pass
```

### For Code Blocks
Use context manager:
```python
with Timer("block_name"):
    # code
    pass
```

### For Long-Running Processes
Use manual control with progress checks:
```python
timer = Timer("process", auto_log=False)
timer.start()

while running:
    work()
    if should_check_progress():
        print(f"Running for {timer.elapsed():.1f}s")

timer.stop()
```

### For Recursive Functions
Each function call gets its own timer automatically when using the decorator:
```python
@timed("recursive_function")
def recursive_function(n):
    if n <= 0:
        return
    recursive_function(n - 1)
```

### For Multiple Operations
Use the registry for global access:
```python
# Start
Timer.register("operation_a", Timer("operation_a").start())

# Check from anywhere
timer = Timer.get("operation_a")
if timer:
    print(f"Elapsed: {timer.elapsed():.2f}s")

# Clean up
Timer.get("operation_a").stop()
Timer.unregister("operation_a")
```

## Performance Notes

- **Zero overhead while running**: Timer only stores start time, no active monitoring
- **Minimal memory**: Each timer instance uses ~100 bytes
- **No background threads**: All calculations are on-demand
- **Thread-safe reads**: `elapsed()` can be safely called from different threads
- **Not thread-safe for start/stop**: Don't start/stop the same timer from multiple threads

## Common Use Cases

### Web Server Response Times
```python
@timed("api_handler")
def handle_request(request):
    return process_request(request)
```

### Database Queries
```python
with Timer("database_query"):
    results = db.query(sql)
```

### Batch Processing Progress
```python
timer = Timer("batch", auto_log=False)
timer.start()

for i, item in enumerate(items):
    process(item)
    if i % 1000 == 0:
        print(f"Progress: {i}/{len(items)} - {timer.elapsed():.1f}s")

timer.stop()
```

### Application Uptime
```python
class App:
    def __init__(self):
        self.uptime = Timer("uptime", auto_log=False).start()
    
    def get_uptime(self):
        return Timer._format_time(self.uptime.elapsed())
```

### Performance Testing
```python
# Compare different approaches
with Timer("approach_a"):
    method_a()

with Timer("approach_b"):
    method_b()
```

## Troubleshooting

**Timer not logging:**
- Check `auto_log=True` (default)
- Check `log_to_file=True` (default)
- Ensure timer.stop() is called

**Can't query elapsed time:**
- Make sure timer.start() was called
- Check timer.is_running() or timer.elapsed() is not None

**Timer shows "not started":**
- Call timer.start() before timer.elapsed()

**Multiple timers interfering:**
- Each Timer instance is independent
- Use unique names or the registry for tracking
