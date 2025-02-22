# piretry

A Python package that provides a simple and flexible retry decorator for both synchronous and asynchronous functions. The decorator allows you to automatically retry function calls when specific exceptions occur.

## Features

- Support for both synchronous and asynchronous functions
- Configurable retry count
- Customizable exception handling
- Detailed retry attempt logging
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

# Retry a function 3 times if it raises ValueError or ConnectionError
@retry_decorator(retry_count=3, error_list=[ValueError, ConnectionError])
def my_function():
    # Your code here
    pass

# The function will be retried up to 3 times if it raises the specified exceptions
```

### Async Function Example

```python
from piretry import retry_decorator
import asyncio

@retry_decorator(retry_count=3, error_list=[ValueError, ConnectionError])
async def my_async_function():
    # Your async code here
    pass

# Run the async function
asyncio.run(my_async_function())
```

### Parameters

- `retry_count`: Number of retry attempts before giving up (integer)
- `error_list`: List of exception classes that should trigger a retry

### Behavior

1. The decorator will attempt to execute the function
2. If an exception from the specified `error_list` occurs, it will:
   - Print a message indicating the attempt number and error
   - Retry the function if attempts remain
   - Raise the final exception if max attempts are reached
3. If the function succeeds, it returns the result immediately

## Example with Real Use Case

```python
from piretry import retry_decorator
import requests

@retry_decorator(retry_count=3, error_list=[requests.exceptions.RequestException])
def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# Usage
try:
    data = fetch_data('https://api.example.com/data')
except requests.exceptions.RequestException as e:
    print(f"Failed to fetch data after 3 attempts: {e}")
```

## Requirements

- Python >= 3.12
- setuptools >= 75.8.0

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
