# this_file: src/twat_search/web/utils.py

"""
Utility functions for the web search API.

This module provides utility functions and classes used by the web search API.
"""

import time
import logging

# Set up logging
logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Rate limiter to manage API request frequency.

    This class helps prevent hitting rate limits by spacing out API requests.
    """

    def __init__(self, calls_per_second: int = 10):
        """
        Initialize the rate limiter.

        Args:
            calls_per_second: Maximum number of calls allowed per second
        """
        self.calls_per_second = calls_per_second
        self.call_timestamps: list[float] = []

    def wait_if_needed(self) -> None:
        """
        Wait if necessary to respect the rate limit.

        This method should be called before making an API request.
        """
        now = time.time()

        # Remove timestamps older than 1 second
        self.call_timestamps = [t for t in self.call_timestamps if now - t < 1]

        # If we've made too many calls in the last second, wait
        if len(self.call_timestamps) >= self.calls_per_second:
            sleep_time = 1 - (now - self.call_timestamps[0])
            if sleep_time > 0:
                if sleep_time > 0.1:  # Only log if sleep time is significant
                    logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f}s")
                time.sleep(sleep_time)

        # Record this API call
        self.call_timestamps.append(time.time())
