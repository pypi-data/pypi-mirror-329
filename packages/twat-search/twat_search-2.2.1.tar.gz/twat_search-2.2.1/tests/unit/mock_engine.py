#!/usr/bin/env python
# this_file: tests/unit/mock_engine.py

"""
Mock search engine implementation for testing.

This module provides a mock search engine implementation that can be used
in tests without making actual API calls.
"""

from typing import Any

from pydantic import HttpUrl

from twat_search.web.config import EngineConfig
from twat_search.web.engines.base import SearchEngine, register_engine
from twat_search.web.models import SearchResult


class MockSearchEngine(SearchEngine):
    """Mock search engine for testing."""

    name = "mock"

    def __init__(self, config: EngineConfig, **kwargs: Any) -> None:
        """Initialize mock engine."""
        super().__init__(config, **kwargs)
        self.query_count = 0
        self.should_fail = kwargs.get("should_fail", False)

    async def search(self, query: str) -> list[SearchResult]:
        """Mock search implementation."""
        self.query_count += 1
        if self.should_fail:
            msg = "Mock search failure"
            raise Exception(msg)

        # Use kwargs to control the number of results
        result_count = self.kwargs.get("result_count", 1)
        return [
            SearchResult(
                title=f"Mock Result {i + 1} for {query}",
                url=HttpUrl(f"https://example.com/{i + 1}"),
                snippet=f"This is mock result {i + 1} for query: {query}",
                source=self.name,
            )
            for i in range(result_count)
        ]


# Register the mock engine
register_engine(MockSearchEngine)
