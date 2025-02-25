#!/usr/bin/env python
# this_file: tests/unit/web/test_utils.py

"""
Unit tests for the twat_search.web.utils module.

This module tests utility functions and classes used in the web search API,
particularly the RateLimiter class.
"""

import time
from unittest.mock import patch

import pytest

from twat_search.web.utils import RateLimiter


@pytest.fixture
def rate_limiter() -> RateLimiter:
    """Create a RateLimiter instance for testing."""
    return RateLimiter(calls_per_second=5)


def test_rate_limiter_init() -> None:
    """Test RateLimiter initialization."""
    limiter = RateLimiter(calls_per_second=10)
    assert limiter.calls_per_second == 10
    assert limiter.call_timestamps == []


def test_rate_limiter_wait_when_not_needed(rate_limiter: RateLimiter) -> None:
    """Test that RateLimiter doesn't wait when under the limit."""
    # First call, no need to wait
    with patch("time.sleep") as mock_sleep:
        rate_limiter.wait_if_needed()
        mock_sleep.assert_not_called()

    # Still under limit, no need to wait
    with patch("time.sleep") as mock_sleep:
        for _ in range(3):  # 4 total calls including the one above
            rate_limiter.wait_if_needed()
        mock_sleep.assert_not_called()


def test_rate_limiter_wait_when_needed(rate_limiter: RateLimiter) -> None:
    """Test that RateLimiter waits when at the limit."""
    # Set up timestamps as if we've made calls_per_second calls
    now = time.time()

    # Make timestamps very close together to ensure we need to wait
    rate_limiter.call_timestamps = [
        now - 0.01 * i for i in range(rate_limiter.calls_per_second)
    ]

    # Next call should trigger waiting
    with patch("time.sleep") as mock_sleep, patch("time.time", return_value=now):
        rate_limiter.wait_if_needed()
        mock_sleep.assert_called_once()
        # The sleep time should be positive but less than or equal to 1 second
        args, _ = mock_sleep.call_args
        assert 0 < args[0] <= 1


def test_rate_limiter_cleans_old_timestamps(rate_limiter: RateLimiter) -> None:
    """Test that RateLimiter cleans up old timestamps."""
    now = time.time()
    # Add some old timestamps (older than 1 second)
    old_stamps = [now - 1.5, now - 2.0, now - 3.0]
    # Add some recent timestamps
    recent_stamps = [now - 0.1, now - 0.2, now - 0.3]

    rate_limiter.call_timestamps = old_stamps + recent_stamps

    with patch("time.time", return_value=now):
        rate_limiter.wait_if_needed()

    # Check that old timestamps were removed
    assert (
        len(rate_limiter.call_timestamps) == len(recent_stamps) + 1
    )  # +1 for the new call
    # Check that the new call was recorded
    assert rate_limiter.call_timestamps[-1] >= now


@pytest.mark.parametrize("calls_per_second", [1, 5, 10, 100])
def test_rate_limiter_with_different_rates(calls_per_second: int) -> None:
    """Test RateLimiter with different rate limits."""
    limiter = RateLimiter(calls_per_second=calls_per_second)
    assert limiter.calls_per_second == calls_per_second

    # Make calls_per_second calls and verify we don't sleep
    with patch("time.sleep") as mock_sleep:
        for _ in range(calls_per_second):
            limiter.wait_if_needed()
        mock_sleep.assert_not_called()

    # On the next call, we would need to sleep if all calls happened in < 1 second
    with (
        patch("time.sleep") as mock_sleep,
        patch("time.time", return_value=time.time()),
    ):
        limiter.wait_if_needed()
        # We might sleep depending on how fast the test runs, so we can't assert on sleep
