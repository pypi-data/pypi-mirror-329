# retry_decorator_pkg/decorators.py

import functools
import asyncio
import logging
import time
from typing import List, Type, Union, Callable, TypeVar, Any

# Set up logging
logger = logging.getLogger(__name__)

T = TypeVar('T')

def retry_decorator(
    retry_count: int,
    error_list: List[Type[Exception]],
    delay: float = 1.0,
    max_delay: float = None,
    backoff_factor: float = 1.0,
    on_retry: Callable[[Exception, int], None] = None
):
    """
    A decorator that retries a function if it raises one of the specified errors.
    
    Args:
        retry_count: Number of attempts to retry.
        error_list: List of exception classes that should trigger a retry.
        delay: Initial delay between retries in seconds (default: 1.0).
        max_delay: Maximum delay between retries in seconds (default: None).
        backoff_factor: Multiplier for delay after each retry (default: 1.0).
        on_retry: Optional callback function called after each retry with the exception and attempt number.
    """
    def get_next_delay(attempt: int) -> float:
        """Calculate the next delay using exponential backoff."""
        current_delay = delay * (backoff_factor ** (attempt - 1))
        if max_delay is not None:
            current_delay = min(current_delay, max_delay)
        return current_delay

    async def handle_retry_async(func: Callable[..., Any], args: tuple, kwargs: dict, attempts: int) -> Any:
        """Handle retry logic for async functions."""
        while True:
            try:
                return await func(*args, **kwargs)
            except asyncio.CancelledError:
                # Always propagate cancellation
                raise
            except tuple(error_list) as e:
                attempts[0] += 1
                if attempts[0] >= retry_count:
                    logger.error(f"Max retry attempts ({retry_count}) reached. Raising error.", exc_info=True)
                    raise

                current_delay = get_next_delay(attempts[0])
                logger.warning(
                    f"Attempt {attempts[0]} failed with error: {str(e)}. "
                    f"Retrying in {current_delay:.2f} seconds..."
                )
                
                if on_retry:
                    on_retry(e, attempts[0])
                
                try:
                    await asyncio.sleep(current_delay)
                except asyncio.CancelledError:
                    logger.info("Retry operation cancelled during delay")
                    raise

    def handle_retry_sync(func: Callable[..., Any], args: tuple, kwargs: dict, attempts: int) -> Any:
        """Handle retry logic for sync functions."""
        while True:
            try:
                return func(*args, **kwargs)
            except tuple(error_list) as e:
                attempts[0] += 1
                if attempts[0] >= retry_count:
                    logger.error(f"Max retry attempts ({retry_count}) reached. Raising error.", exc_info=True)
                    raise

                current_delay = get_next_delay(attempts[0])
                logger.warning(
                    f"Attempt {attempts[0]} failed with error: {str(e)}. "
                    f"Retrying in {current_delay:.2f} seconds..."
                )
                
                if on_retry:
                    on_retry(e, attempts[0])
                    
                time.sleep(current_delay)

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        if asyncio.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> T:
                attempts = [0]
                return await handle_retry_async(func, args, kwargs, attempts)
            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> T:
                attempts = [0]
                return handle_retry_sync(func, args, kwargs, attempts)
            return sync_wrapper

    return decorator
