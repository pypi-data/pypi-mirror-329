#!/usr/bin/env python
# this_file: tests/unit/web/test_api.py

"""
Unit tests for the twat_search.web.api module.

This module tests the main search function, which is the primary entry point
for the web search functionality.
"""

import asyncio
import contextlib
import logging
from typing import Any, TypeVar
from collections.abc import AsyncGenerator, Awaitable, Callable

import pytest
from pydantic import HttpUrl
from pytest import MonkeyPatch

from twat_search.web.api import search
from twat_search.web.config import Config, EngineConfig
from twat_search.web.engines.base import SearchEngine, register_engine
from twat_search.web.exceptions import SearchError
from twat_search.web.models import SearchResult


# Setup logging for tests
logging.basicConfig(level=logging.DEBUG)


# Fixture type for clarity
T = TypeVar("T")
AsyncFixture = Callable[..., Awaitable[T]]


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


@pytest.fixture
def mock_config() -> Config:
    """Create a Config with a registered mock engine."""
    config = Config()
    config.engines = {
        "mock": EngineConfig(
            api_key="mock_key",
            enabled=True,
            default_params={"result_count": 2},
        )
    }
    return config


@pytest.fixture
async def setup_teardown() -> AsyncGenerator[None, None]:
    """Setup and teardown for tests."""
    # Setup code
    yield
    # Teardown code - allow any pending tasks to complete
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    with contextlib.suppress(asyncio.CancelledError):
        await asyncio.gather(*tasks)


@pytest.mark.asyncio
async def test_search_with_mock_engine(
    mock_config: Config, setup_teardown: None
) -> None:
    """Test search with a mock engine."""
    results = await search("test query", engines=["mock"], config=mock_config)

    assert len(results) == 2
    assert all(isinstance(result, SearchResult) for result in results)
    assert all(result.source == "mock" for result in results)
    assert "test query" in results[0].title


@pytest.mark.asyncio
async def test_search_with_additional_params(
    mock_config: Config, setup_teardown: None
) -> None:
    """Test search with additional parameters."""
    results = await search(
        "test query", engines=["mock"], config=mock_config, result_count=3
    )

    assert len(results) == 3


@pytest.mark.asyncio
async def test_search_with_engine_specific_params(
    mock_config: Config, setup_teardown: None
) -> None:
    """Test search with engine-specific parameters."""
    results = await search(
        "test query", engines=["mock"], config=mock_config, mock_result_count=4
    )

    assert len(results) == 4


@pytest.mark.asyncio
async def test_search_with_no_engines(setup_teardown: None) -> None:
    """Test search with no engines specified raises SearchError."""
    with pytest.raises(SearchError, match="No search engines configured"):
        await search("test query", engines=[])


@pytest.mark.asyncio
async def test_search_with_failing_engine(
    mock_config: Config, setup_teardown: None
) -> None:
    """Test search with a failing engine returns empty results."""
    results = await search(
        "test query", engines=["mock"], config=mock_config, should_fail=True
    )

    assert len(results) == 0


@pytest.mark.asyncio
async def test_search_with_nonexistent_engine(
    mock_config: Config, setup_teardown: None
) -> None:
    """Test search with a non-existent engine raises SearchError."""
    with pytest.raises(SearchError, match="No search engines could be initialized"):
        await search("test query", engines=["nonexistent"], config=mock_config)


@pytest.mark.asyncio
async def test_search_with_disabled_engine(
    mock_config: Config, monkeypatch: MonkeyPatch, setup_teardown: None
) -> None:
    """Test search with a disabled engine raises SearchError."""
    # Disable the mock engine
    mock_config.engines["mock"].enabled = False

    with pytest.raises(SearchError, match="No search engines could be initialized"):
        await search("test query", engines=["mock"], config=mock_config)
