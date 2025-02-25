#!/usr/bin/env python
# this_file: tests/unit/web/test_exceptions.py

"""
Unit tests for the twat_search.web.exceptions module.

This module tests the custom exceptions used in the web search API.
"""

from twat_search.web.exceptions import SearchError, EngineError


def test_search_error() -> None:
    """Test the SearchError exception."""
    error_message = "Test search error"
    exception = SearchError(error_message)

    assert str(exception) == error_message
    assert isinstance(exception, Exception)


def test_engine_error() -> None:
    """Test the EngineError exception."""
    engine_name = "test_engine"
    error_message = "Test engine error"
    exception = EngineError(engine_name, error_message)

    # Check that the error message includes the engine name
    assert str(exception) == f"Engine '{engine_name}': {error_message}"
    assert exception.engine_name == engine_name

    # Check inheritance
    assert isinstance(exception, SearchError)
    assert isinstance(exception, Exception)


def test_engine_error_inheritance() -> None:
    """Test that EngineError can be caught as SearchError."""
    try:
        msg = "test_engine"
        raise EngineError(msg, "Test error")
    except SearchError as e:
        # Only check engine_name if it's EngineError
        if isinstance(e, EngineError):
            assert e.engine_name == "test_engine"


def test_search_error_as_base_class() -> None:
    """Test using SearchError as a base class for exception handling."""
    exceptions = []

    try:
        msg = "General search error"
        raise SearchError(msg)
    except SearchError as e:
        exceptions.append(e)

    try:
        msg = "brave"
        raise EngineError(msg, "API key missing")
    except SearchError as e:
        exceptions.append(e)

    assert len(exceptions) == 2
    assert isinstance(exceptions[0], SearchError)
    assert isinstance(exceptions[1], EngineError)
    assert "General search error" in str(exceptions[0])
    assert "Engine 'brave': API key missing" in str(exceptions[1])
