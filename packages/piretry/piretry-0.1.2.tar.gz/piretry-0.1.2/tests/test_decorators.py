# tests/test_decorators.py

import unittest
import asyncio
import time
import logging
from src.piretry.decorators import retry_decorator

class TestRetryDecorator(unittest.TestCase):

    def setUp(self):
        # Configure logging for tests
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def test_sync_retry_success(self):
        # A function that fails twice with ValueError then succeeds
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
        # A function that always fails
        @retry_decorator(retry_count=3, error_list=[ValueError])
        def func():
            raise ValueError("Always fails")
        
        with self.assertRaises(ValueError):
            func()

    def test_delay_and_backoff(self):
        counter = {"attempts": 0, "last_time": None}

        @retry_decorator(
            retry_count=3,
            error_list=[ValueError],
            delay=0.1,
            backoff_factor=2.0
        )
        def func():
            current_time = time.time()
            if counter["last_time"] is not None:
                # Check if delay was applied (with some tolerance)
                if counter["attempts"] == 1:
                    self.assertGreaterEqual(current_time - counter["last_time"], 0.1)
                elif counter["attempts"] == 2:
                    self.assertGreaterEqual(current_time - counter["last_time"], 0.2)
            
            counter["attempts"] += 1
            counter["last_time"] = current_time
            raise ValueError("Fail")

        with self.assertRaises(ValueError):
            func()

    def test_max_delay(self):
        @retry_decorator(
            retry_count=3,
            error_list=[ValueError],
            delay=0.1,
            max_delay=0.15,
            backoff_factor=2.0
        )
        def func():
            raise ValueError("Fail")

        start_time = time.time()
        with self.assertRaises(ValueError):
            func()
        total_time = time.time() - start_time

        # Total time should be less than if we used full exponential backoff
        # 0.1 + 0.15 + 0.15 = 0.4 instead of 0.1 + 0.2 + 0.4 = 0.7
        self.assertLess(total_time, 0.5)

    def test_on_retry_callback(self):
        callback_data = {"called": 0, "last_attempt": 0}

        def on_retry(error, attempt):
            callback_data["called"] += 1
            callback_data["last_attempt"] = attempt

        @retry_decorator(
            retry_count=3,
            error_list=[ValueError],
            on_retry=on_retry
        )
        def func():
            raise ValueError("Fail")

        with self.assertRaises(ValueError):
            func()

        self.assertEqual(callback_data["called"], 3)
        self.assertEqual(callback_data["last_attempt"], 3)

    async def async_test_cancellation(self):
        cancel_data = {"cancelled": False}

        @retry_decorator(
            retry_count=3,
            error_list=[ValueError],
            delay=0.1
        )
        async def func():
            raise ValueError("Fail")

        async def run_with_cancel():
            try:
                task = asyncio.create_task(func())
                await asyncio.sleep(0.15)  # Wait for first retry to start
                task.cancel()
                await task
            except asyncio.CancelledError:
                cancel_data["cancelled"] = True

        await run_with_cancel()
        self.assertTrue(cancel_data["cancelled"])

    def test_async_cancellation(self):
        asyncio.run(self.async_test_cancellation())

if __name__ == "__main__":
    unittest.main()
