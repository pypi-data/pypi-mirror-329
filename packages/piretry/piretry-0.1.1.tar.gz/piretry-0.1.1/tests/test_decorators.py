# tests/test_decorators.py

import unittest
from src.decorators import retry_decorator

class TestRetryDecorator(unittest.TestCase):

    def test_sync_retry_success(self):
        # A function that fails twice with ValueError then succeeds.
        counter = {"attempts": 0}

        @retry_decorator(retry_count=3, error_list=[ValueError])
        def func():
            counter["attempts"] += 1
            if counter["attempts"] < 3:
                raise ValueError("Temporary failure")
            return "Success"

        result = func()
        self.assertEqual(result, "Success")
        self.assertEqual(counter["attempts"], 3)

    def test_sync_retry_fail(self):
        # A function that always fails.
        @retry_decorator(retry_count=3, error_list=[ValueError])
        def func():
            raise ValueError("Always fails")
        
        with self.assertRaises(ValueError):
            func()

if __name__ == "__main__":
    unittest.main()
