"""
Timer utilities for measuring function execution time.

Provides multiple interfaces for timing code execution:
- Context manager for timing code blocks
- Decorator for timing functions
- Manual start/stop for flexible control
- Query elapsed time while running
"""

import time
import functools

try:
    from .printtime import printtime
except ImportError:
    # Fallback for running as script
    from printtime import printtime


class Timer:
    """
    A flexible timer class for measuring execution time.
    
    Can be used as:
    1. Context manager: with Timer("operation"):
    2. Decorator: @Timer.decorator()
    3. Manual: timer.start(), timer.stop(), timer.elapsed()
    
    Features:
    - Zero overhead while running (only calculates time on demand)
    - Query elapsed time while still running
    - Optionally log results using printtime
    - Track multiple named timers simultaneously
    """
    
    # Class-level registry for named timers
    _registry = {}
    
    def __init__(self, name=None, auto_log=True, log_to_file=True):
        """
        Initialize a timer.
        
        Args:
            name (str): Optional name for this timer. Used in logging and registry.
            auto_log (bool): If True, automatically logs results when timer stops.
            log_to_file (bool): If True, logs are written to file (passed to printtime).
        """
        self.name = name or f"Timer_{id(self)}"
        self.auto_log = auto_log
        self.log_to_file = log_to_file
        self.start_time = None
        self.end_time = None
        self._is_running = False
        
    def start(self):
        """Start the timer."""
        self.start_time = time.perf_counter()
        self.end_time = None
        self._is_running = True
        return self
    
    def stop(self):
        """
        Stop the timer and optionally log the result.
        
        Returns:
            float: Elapsed time in seconds.
        """
        if not self._is_running:
            raise RuntimeError(f"Timer '{self.name}' is not running")
        
        self.end_time = time.perf_counter()
        self._is_running = False
        elapsed = self.elapsed()
        
        if self.auto_log:
            self._log_result(elapsed, completed=True)
        
        return elapsed
    
    def elapsed(self):
        """
        Get elapsed time since start.
        Can be called while timer is still running or after it stops.
        
        Returns:
            float: Elapsed time in seconds, or None if timer hasn't started.
        """
        if self.start_time is None:
            return None
        
        end = self.end_time if self.end_time is not None else time.perf_counter()
        return end - self.start_time
    
    def is_running(self):
        """Check if timer is currently running."""
        return self._is_running
    
    def reset(self):
        """Reset the timer to initial state."""
        self.start_time = None
        self.end_time = None
        self._is_running = False
    
    def _log_result(self, elapsed, completed=False):
        """Internal method to log timing results."""
        status = "completed" if completed else "running"
        message = f"Timer '{self.name}' {status}: {self._format_time(elapsed)}"
        printtime(message, log_to_file=self.log_to_file)
    
    @staticmethod
    def _format_time(seconds):
        """Format time in a human-readable way."""
        if seconds is None:
            return "Not started"
        
        if seconds < 1:
            return f"{seconds * 1000:.2f}ms"
        elif seconds < 60:
            return f"{seconds:.2f}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = seconds % 60
            return f"{minutes}m {secs:.2f}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            secs = seconds % 60
            return f"{hours}h {minutes}m {secs:.2f}s"
    
    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
        return False
    
    def __repr__(self):
        """String representation of timer."""
        if self.start_time is None:
            status = "not started"
        elif self._is_running:
            status = f"running ({self._format_time(self.elapsed())})"
        else:
            status = f"completed ({self._format_time(self.elapsed())})"
        return f"<Timer '{self.name}' {status}>"
    
    @classmethod
    def decorator(cls, name=None, auto_log=True, log_to_file=True):
        """
        Decorator for timing function execution.
        
        Args:
            name (str): Optional name for the timer. Defaults to function name.
            auto_log (bool): If True, automatically logs timing results.
            log_to_file (bool): If True, logs are written to file.
        
        Example:
            @Timer.decorator("my_function")
            def my_function():
                time.sleep(1)
        """
        def decorator_wrapper(func):
            timer_name = name or func.__name__
            
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                timer = cls(name=timer_name, auto_log=auto_log, log_to_file=log_to_file)
                timer.start()
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    timer.stop()
            
            return wrapper
        return decorator_wrapper
    
    @classmethod
    def get(cls, name):
        """
        Get a named timer from the registry.
        
        Args:
            name (str): Name of the timer to retrieve.
        
        Returns:
            Timer: The timer instance, or None if not found.
        """
        return cls._registry.get(name)
    
    @classmethod
    def register(cls, name, timer):
        """
        Register a named timer for later retrieval.
        
        Args:
            name (str): Name to register the timer under.
            timer (Timer): Timer instance to register.
        """
        cls._registry[name] = timer
    
    @classmethod
    def unregister(cls, name):
        """
        Remove a timer from the registry.
        
        Args:
            name (str): Name of the timer to remove.
        """
        cls._registry.pop(name, None)
    
    @classmethod
    def clear_registry(cls):
        """Clear all timers from the registry."""
        cls._registry.clear()


def timed(name=None, auto_log=True, log_to_file=True):
    """
    Convenience decorator for timing functions.
    Alias for Timer.decorator() with a shorter name.
    
    Args:
        name (str): Optional name for the timer.
        auto_log (bool): If True, automatically logs timing results.
        log_to_file (bool): If True, logs are written to file.
    
    Example:
        @timed("my_function")
        def my_function():
            time.sleep(1)
    """
    return Timer.decorator(name=name, auto_log=auto_log, log_to_file=log_to_file)


# ==============================================================================
# DEMO / TESTING
# ==============================================================================

if __name__ == "__main__":
    import time as time_module
    
    print("=" * 70)
    print("TIMER DEMONSTRATION")
    print("=" * 70)
    
    # Demo 1: Context manager
    print("\n[1] CONTEXT MANAGER - Timing a code block")
    with Timer("sleep_operation"):
        time_module.sleep(0.5)
    
    # Demo 2: Manual start/stop
    print("\n[2] MANUAL CONTROL - Start, check, stop")
    timer = Timer("manual_timer")
    timer.start()
    time_module.sleep(0.3)
    printtime(f"Elapsed so far: {timer._format_time(timer.elapsed())}", log_to_file=False)
    time_module.sleep(0.2)
    elapsed = timer.stop()
    printtime(f"Final time: {timer._format_time(elapsed)}", log_to_file=False)
    
    # Demo 3: Decorator
    print("\n[3] DECORATOR - Timing a function")
    
    @Timer.decorator("decorated_function")
    def slow_function(duration):
        """A slow function for demonstration."""
        time_module.sleep(duration)
        return "Done"
    
    result = slow_function(0.4)
    printtime(f"Function returned: {result}", log_to_file=False)
    
    # Demo 4: Short decorator syntax
    print("\n[4] TIMED DECORATOR - Short syntax")
    
    @timed("quick_function")
    def quick_function():
        time_module.sleep(0.1)
        return "Quick!"
    
    result = quick_function()
    
    # Demo 5: Recursive function
    print("\n[5] RECURSIVE FUNCTION - Fibonacci with timing")
    
    @timed("fibonacci", auto_log=False)
    def fibonacci(n):
        if n <= 1:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)
    
    timer = Timer("fibonacci_total")
    timer.start()
    result = fibonacci(10)
    elapsed = timer.stop()
    printtime(f"Fibonacci(10) = {result}", log_to_file=False)
    
    # Demo 6: Long-running process with progress checks
    print("\n[6] LONG-RUNNING PROCESS - With progress checks")
    timer = Timer("long_process", auto_log=False)
    timer.start()
    
    for i in range(5):
        time_module.sleep(0.2)
        elapsed = timer.elapsed()
        printtime(f"Step {i+1}/5 - Elapsed: {timer._format_time(elapsed)}", log_to_file=False)
    
    final_time = timer.stop()
    printtime(f"Process complete in {timer._format_time(final_time)}", log_to_file=False)
    
    # Demo 7: Multiple simultaneous timers
    print("\n[7] MULTIPLE TIMERS - Tracking different operations")
    Timer.register("operation_a", Timer("Operation A", auto_log=False).start())
    time_module.sleep(0.2)
    Timer.register("operation_b", Timer("Operation B", auto_log=False).start())
    time_module.sleep(0.3)
    
    timer_a = Timer.get("operation_a")
    timer_b = Timer.get("operation_b")
    
    printtime(f"Operation A: {timer_a._format_time(timer_a.elapsed())}", log_to_file=False)
    printtime(f"Operation B: {timer_b._format_time(timer_b.elapsed())}", log_to_file=False)
    
    timer_a.stop()
    timer_b.stop()
    Timer.clear_registry()
    
    # Demo 8: No logging timer
    print("\n[8] NO LOGGING - Silent timing")
    with Timer("silent_timer", auto_log=False, log_to_file=False) as t:
        time_module.sleep(0.1)
    printtime(f"Silent timer elapsed: {t._format_time(t.elapsed())}", log_to_file=False)
    
    # Demo 9: Time formatting
    print("\n[9] TIME FORMATTING - Various durations")
    test_times = [0.0005, 0.05, 1.5, 65.3, 3725.8]
    for t in test_times:
        printtime(f"{t}s = {Timer._format_time(t)}", log_to_file=False)
    
    print("\n" + "=" * 70)
    printtime("Timer demonstration complete!")
    print("=" * 70)
