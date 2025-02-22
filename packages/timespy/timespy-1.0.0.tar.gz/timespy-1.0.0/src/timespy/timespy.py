import time
import functools

def timer(func):
    """Profiler decorator to measure execution time of functions."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        wrapper.exec_time = end_time - start_time  # Store execution time in wrapper.exec_time
        return result
    
    wrapper.exec_time = 0  # Initialize exec_time before function execution
    return wrapper

