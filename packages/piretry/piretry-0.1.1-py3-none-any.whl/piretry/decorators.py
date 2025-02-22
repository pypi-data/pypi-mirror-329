# retry_decorator_pkg/decorators.py

import functools
import asyncio

def retry_decorator(retry_count, error_list):
    """
    A decorator that retries a function if it raises one of the specified errors.
    
    :param retry_count: Number of attempts to retry.
    :param error_list: List of exception classes that should trigger a retry.
    """
    def decorator(func):
        if asyncio.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                attempts = 0
                while attempts < retry_count:
                    try:
                        return await func(*args, **kwargs)
                    except tuple(error_list) as e:
                        attempts += 1
                        print(f"Attempt {attempts} failed with error: {e}. Retrying...")
                        if attempts == retry_count:
                            print("Max retry attempts reached. Raising error.")
                            raise
            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                attempts = 0
                while attempts < retry_count:
                    try:
                        return func(*args, **kwargs)
                    except tuple(error_list) as e:
                        attempts += 1
                        print(f"Attempt {attempts} failed with error: {e}. Retrying...")
                        if attempts == retry_count:
                            print("Max retry attempts reached. Raising error.")
                            raise
            return sync_wrapper
    return decorator
