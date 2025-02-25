#!/usr/bin/env python
# this_file: tests/unit/web/engines/test_base.py

"""
Unit tests for the twat_search.web.engines.base module.

This module tests the base search engine class and factory functions.
"""

import abc

import pytest
from pydantic import HttpUrl

from twat_search.web.config import EngineConfig
from twat_search.web.engines.base import SearchEngine, register_engine, get_engine
from twat_search.web.exceptions import SearchError
from twat_search.web.models import SearchResult


class TestSearchEngine(SearchEngine):
    """Test implementation of the SearchEngine abstract base class."""

    name = "test_engine"

    async def search(self, query: str) -> list[SearchResult]:
        """Test implementation of the search method."""
        return [
            SearchResult(
                title=f"Test Result for {query}",
                url=HttpUrl("https://example.com/test"),
                snippet=f"This is a test result for {query}",
                source=self.name,
            )
        ]


# Register the test engine
register_engine(TestSearchEngine)


class DisabledTestSearchEngine(SearchEngine):
    """Test implementation with disabled status for testing."""

    name = "disabled_engine"

    async def search(self, query: str) -> list[SearchResult]:
        """Search implementation that should never be called."""
        msg = "This should never be called because the engine is disabled"
        raise NotImplementedError(msg)


# Register the disabled test engine
register_engine(DisabledTestSearchEngine)


def test_search_engine_is_abstract() -> None:
    """Test that SearchEngine is an abstract base class."""
    assert abc.ABC in SearchEngine.__mro__
    assert hasattr(SearchEngine, "__abstractmethods__")
    assert "search" in SearchEngine.__abstractmethods__

    # Ensure we can't instantiate SearchEngine directly
    with pytest.raises(TypeError):
        SearchEngine(EngineConfig())  # type: ignore


def test_search_engine_name_class_var() -> None:
    """Test that name is a required class variable."""
    # SearchEngine.name should be defined as a class variable
    assert hasattr(SearchEngine, "name")

    # The default value should be an empty string (not None)
    assert SearchEngine.name == ""

    # Check that our test classes have set the name
    assert TestSearchEngine.name == "test_engine"
    assert DisabledTestSearchEngine.name == "disabled_engine"


def test_engine_registration() -> None:
    """Test that engines are properly registered."""

    # Create a new engine class
    class NewEngine(SearchEngine):
        name = "new_engine"

        async def search(self, query: str) -> list[SearchResult]:
            return []

    # Register it
    returned_class = register_engine(NewEngine)

    # Test that register_engine returns the class (for decorator use)
    assert returned_class is NewEngine

    # Test that we can get the engine from the registry
    engine_instance = get_engine("new_engine", EngineConfig())
    assert isinstance(engine_instance, NewEngine)


def test_get_engine_with_invalid_name() -> None:
    """Test that get_engine raises an error for invalid engine names."""
    with pytest.raises(SearchError, match="Unknown search engine"):
        get_engine("nonexistent_engine", EngineConfig())


def test_get_engine_with_disabled_engine() -> None:
    """Test that get_engine raises an error when engine is disabled."""
    config = EngineConfig(enabled=False)
    with pytest.raises(SearchError, match="is disabled"):
        get_engine("disabled_engine", config)


def test_get_engine_with_config() -> None:
    """Test that get_engine passes config to the engine."""
    config = EngineConfig(
        api_key="test_key",
        enabled=True,
        default_params={"count": 10},
    )

    engine = get_engine("test_engine", config)

    assert engine.config is config
    assert engine.config.api_key == "test_key"
    assert engine.config.default_params == {"count": 10}


def test_get_engine_with_kwargs() -> None:
    """Test that get_engine passes kwargs to the engine."""
    kwargs = {"timeout": 30, "country": "US"}
    engine = get_engine("test_engine", EngineConfig(), **kwargs)

    # Check that kwargs were stored by the engine
    assert engine.kwargs == kwargs
    assert engine.kwargs["timeout"] == 30
    assert engine.kwargs["country"] == "US"
