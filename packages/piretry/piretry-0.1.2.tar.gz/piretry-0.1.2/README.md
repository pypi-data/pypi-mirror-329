# piretry

A Python package that provides a robust and flexible retry decorator for both synchronous and asynchronous functions. The decorator allows you to automatically retry function calls when specific exceptions occur, with configurable delay, exponential backoff, and proper logging.

## Features

- Support for both synchronous and asynchronous functions
- Configurable retry count and delay between retries
- Exponential backoff with optional maximum delay cap
- Proper handling of asyncio cancellation
- Built-in logging with configurable levels
- Custom retry callback support
- Type hints for better IDE support
- Python 3.12+ support

## Installation

You can install the package using pip:

```bash
pip install piretry
```

## Usage

### Basic Example

```python
from piretry import retry_decorator
import logging

# Configure logging (recommended)
logging.basicConfig(level=logging.INFO)

# Retry a function 3 times if it raises ValueError or ConnectionError
@retry_decorator(retry_count=3, error_list=[ValueError, ConnectionError])
def my_function():
    # Your code here
    pass
```

### Advanced Example with All Options

```python
from piretry import retry_decorator
import logging

@retry_decorator(
    retry_count=3,                    # Maximum number of retry attempts
    error_list=[ValueError],          # List of exceptions to catch
    delay=1.0,                        # Initial delay between retries (seconds)
    max_delay=5.0,                    # Maximum delay cap (seconds)
    backoff_factor=2.0,               # Multiply delay by this factor after each retry
    on_retry=lambda e, attempt: print(f"Custom handling of retry {attempt}")  # Optional callback
)
def advanced_function():
    # Your code here
    pass
```

### Async Function Example

```python
from piretry import retry_decorator
import asyncio
import logging

@retry_decorator(
    retry_count=3,
    error_list=[ValueError, ConnectionError],
    delay=1.0,
    backoff_factor=2.0
)
async def my_async_function():
    # Your async code here
    pass

# Run the async function
async def main():
    await my_async_function()

asyncio.run(main())
```

### Parameters

- `retry_count` (int): Number of retry attempts before giving up
- `error_list` (List[Type[Exception]]): List of exception classes that should trigger a retry
- `delay` (float, optional): Initial delay between retries in seconds. Defaults to 1.0
- `max_delay` (float, optional): Maximum delay cap for exponential backoff. Defaults to None (no cap)
- `backoff_factor` (float, optional): Multiplier for delay after each retry. Defaults to 1.0
- `on_retry` (Callable[[Exception, int], None], optional): Callback function called after each retry with the exception and attempt number

### Behavior

1. The decorator will attempt to execute the function
2. If an exception from the specified `error_list` occurs:
   - Log a warning with attempt number and error details
   - Calculate next delay using exponential backoff if configured
   - Call the on_retry callback if provided
   - Wait for the calculated delay
   - Retry the function if attempts remain
   - Raise the final exception if max attempts are reached
3. For async functions:
   - Properly handles asyncio.CancelledError during execution and delay
   - Ensures proper task cancellation
4. Logs all retry attempts and errors using Python's logging framework

## Example with Real Use Case

```python
import logging
from piretry import retry_decorator
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)

@retry_decorator(
    retry_count=3,
    error_list=[requests.exceptions.RequestException],
    delay=1.0,
    max_delay=5.0,
    backoff_factor=2.0,
    on_retry=lambda e, attempt: print(f"Request failed, attempt {attempt}")
)
def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# Usage
try:
    data = fetch_data('https://api.example.com/data')
except requests.exceptions.RequestException as e:
    print(f"Failed to fetch data after all retries: {e}")
```

## Requirements

- Python >= 3.12
- setuptools >= 75.8.0

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
