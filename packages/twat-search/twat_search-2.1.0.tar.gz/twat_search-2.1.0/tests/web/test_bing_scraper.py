#!/usr/bin/env python3
# this_file: tests/web/test_bing_scraper.py

"""
Tests for the Bing Scraper search engine.

This module contains tests for the BingScraperSearchEngine class and its
associated functionality. The tests use mocking to avoid making actual
network requests during testing.
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from pydantic import HttpUrl
from typing import Any

from twat_search.web.config import EngineConfig
from twat_search.web.engines import BingScraperSearchEngine
from twat_search.web.engines.bing_scraper import bing_scraper
from twat_search.web.exceptions import EngineError
from twat_search.web.models import SearchResult


class MockSearchResult:
    """Mock class to simulate results from BingScraper."""

    def __init__(self, title: str, url: str, description: str = "") -> None:
        """Initialize a mock search result."""
        self.title = title
        self.url = url
        self.description = description


@pytest.fixture
def engine_config() -> EngineConfig:
    """Create a basic engine configuration for testing."""
    return EngineConfig(enabled=True)


@pytest.fixture
def engine(engine_config: EngineConfig) -> BingScraperSearchEngine:
    """Create a Bing Scraper engine instance for testing."""
    return BingScraperSearchEngine(config=engine_config, num_results=5)


@pytest.fixture
def mock_results() -> list[MockSearchResult]:
    """Create a list of mock search results for testing."""
    return [
        MockSearchResult(
            title="Test Result 1",
            url="https://example.com/1",
            description="First test result",
        ),
        MockSearchResult(
            title="Test Result 2",
            url="https://example.com/2",
            description="Second test result",
        ),
    ]


class TestBingScraperEngine:
    """Tests for the Bing Scraper search engine."""

    @patch("twat_search.web.engines.bing_scraper.BingScraper")
    def test_init(self, mock_BingScraper: MagicMock, engine: Any) -> None:
        """Test BingScraperSearchEngine initialization."""
        assert engine.name == "bing-scraper"
        assert engine.max_results == 5
        assert engine.max_retries == 3
        assert engine.delay_between_requests == 1.0
        # Lazy initialization - BingScraper shouldn't be called yet
        mock_BingScraper.assert_not_called()

    @patch("twat_search.web.engines.bing_scraper.BingScraper")
    @pytest.mark.asyncio
    async def test_search_basic(
        self,
        mock_BingScraper: MagicMock,
        engine: BingScraperSearchEngine,
        mock_results: list[MockSearchResult],
    ) -> None:
        """Test basic search functionality."""
        # Setup mock
        mock_instance = MagicMock()
        mock_BingScraper.return_value = mock_instance
        mock_instance.search.return_value = mock_results

        # Perform search
        results = await engine.search("test query")

        # Verify results
        assert len(results) == 2
        assert isinstance(results[0], SearchResult)
        assert results[0].title == "Test Result 1"
        assert str(results[0].url) == "https://example.com/1"
        assert results[0].snippet == "First test result"
        assert results[0].source == "bing-scraper"

        # Verify search parameters
        mock_BingScraper.assert_called_once_with(
            max_retries=3, delay_between_requests=1.0
        )
        mock_instance.search.assert_called_once_with("test query", num_results=5)

    @patch("twat_search.web.engines.bing_scraper.BingScraper")
    @pytest.mark.asyncio
    async def test_custom_parameters(self, mock_BingScraper: MagicMock) -> None:
        """Test custom parameters for engine initialization."""
        # Create engine with custom parameters
        engine = BingScraperSearchEngine(
            config=EngineConfig(enabled=True),
            num_results=10,
            max_retries=5,
            delay_between_requests=2.0,
            # These parameters should be logged but not used
            country="us",
            language="en",
            safe_search="strict",
            time_frame="month",
        )

        # Setup mock
        mock_instance = MagicMock()
        mock_BingScraper.return_value = mock_instance
        mock_instance.search.return_value = []

        # Perform search
        await engine.search("test query")

        # Verify parameters were used correctly
        mock_BingScraper.assert_called_once_with(
            max_retries=5, delay_between_requests=2.0
        )
        mock_instance.search.assert_called_once_with("test query", num_results=10)

    @patch("twat_search.web.engines.bing_scraper.BingScraper")
    @pytest.mark.asyncio
    async def test_invalid_url_handling(
        self, mock_BingScraper: MagicMock, engine: BingScraperSearchEngine
    ) -> None:
        """Test handling of invalid URLs."""
        # Setup mock
        mock_instance = MagicMock()
        mock_BingScraper.return_value = mock_instance

        # Include an invalid URL that will fail HttpUrl validation
        mock_instance.search.return_value = [
            MockSearchResult(
                title="Valid Result",
                url="https://example.com/valid",
                description="Valid URL",
            ),
            MockSearchResult(
                title="Invalid Result",
                url="invalid::/url",  # Invalid URL format
                description="Invalid URL",
            ),
        ]

        # Perform search
        results = await engine.search("test query")

        # Only the valid result should be included
        assert len(results) == 1
        assert results[0].title == "Valid Result"

    @patch("twat_search.web.api.search")
    @pytest.mark.asyncio
    async def test_bing_scraper_convenience_function(
        self, mock_search: AsyncMock
    ) -> None:
        """Test the bing_scraper convenience function."""
        # Setup mock
        mock_results = [
            SearchResult(
                title="Test Result",
                url=HttpUrl("https://example.com"),
                snippet="Test description",
                source="bing-scraper",
            )
        ]
        mock_search.return_value = mock_results

        # Use convenience function
        results = await bing_scraper(
            "test query",
            num_results=10,
            max_retries=5,
            delay_between_requests=2.0,
        )

        # Verify results
        assert results == mock_results

        # Verify the correct parameters were passed to the API
        mock_search.assert_called_once()
        call_args, call_kwargs = mock_search.call_args
        assert call_args[0] == "test query"
        assert call_kwargs["engines"] == ["bing-scraper"]
        assert call_kwargs["num_results"] == 10
        assert call_kwargs["bing_scraper_max_retries"] == 5
        assert call_kwargs["bing_scraper_delay_between_requests"] == 2.0

    @patch("twat_search.web.engines.bing_scraper.BingScraper")
    @pytest.mark.asyncio
    async def test_empty_query(
        self, mock_BingScraper: MagicMock, engine: BingScraperSearchEngine
    ) -> None:
        """Test behavior with empty query string."""
        # Empty query should raise an EngineError
        with pytest.raises(EngineError) as excinfo:
            await engine.search("")

        assert "Search query cannot be empty" in str(excinfo.value)
        mock_BingScraper.assert_not_called()

    @patch("twat_search.web.engines.bing_scraper.BingScraper")
    @pytest.mark.asyncio
    async def test_no_results(
        self, mock_BingScraper: MagicMock, engine: BingScraperSearchEngine
    ) -> None:
        """Test handling of no results returned from BingScraper."""
        # Setup mock to return empty list
        mock_instance = MagicMock()
        mock_BingScraper.return_value = mock_instance
        mock_instance.search.return_value = []

        # Should return empty list without errors
        results = await engine.search("test query")
        assert isinstance(results, list)
        assert len(results) == 0

    @patch("twat_search.web.engines.bing_scraper.BingScraper")
    @pytest.mark.asyncio
    async def test_network_error(
        self, mock_BingScraper: MagicMock, engine: BingScraperSearchEngine
    ) -> None:
        """Test handling of network errors."""
        # Setup mock to raise ConnectionError
        mock_instance = MagicMock()
        mock_BingScraper.return_value = mock_instance
        mock_instance.search.side_effect = ConnectionError("Network timeout")

        # Should raise EngineError with appropriate message
        with pytest.raises(EngineError) as excinfo:
            await engine.search("test query")

        assert "Network error connecting to Bing" in str(excinfo.value)

    @patch("twat_search.web.engines.bing_scraper.BingScraper")
    @pytest.mark.asyncio
    async def test_parsing_error(
        self, mock_BingScraper: MagicMock, engine: BingScraperSearchEngine
    ) -> None:
        """Test handling of parsing errors."""
        # Setup mock to raise RuntimeError
        mock_instance = MagicMock()
        mock_BingScraper.return_value = mock_instance
        mock_instance.search.side_effect = RuntimeError("Failed to parse HTML")

        # Should raise EngineError with appropriate message
        with pytest.raises(EngineError) as excinfo:
            await engine.search("test query")

        assert "Error parsing Bing search results" in str(excinfo.value)

    @patch("twat_search.web.engines.bing_scraper.BingScraper")
    @pytest.mark.asyncio
    async def test_invalid_result_format(
        self, mock_BingScraper: MagicMock, engine: BingScraperSearchEngine
    ) -> None:
        """Test handling of invalid result format."""
        # Setup mock to return results with missing attributes
        mock_instance = MagicMock()
        mock_BingScraper.return_value = mock_instance

        # Create an invalid result object missing required attributes
        class InvalidResult:
            def __init__(self):
                self.some_field = "something"

        mock_instance.search.return_value = [InvalidResult()]

        # Should handle gracefully and return empty list
        results = await engine.search("test query")
        assert isinstance(results, list)
        assert len(results) == 0
