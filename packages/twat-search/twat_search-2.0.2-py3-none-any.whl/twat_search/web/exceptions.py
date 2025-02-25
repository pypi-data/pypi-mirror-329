# this_file: src/twat_search/web/exceptions.py

"""
Custom exceptions for the web search API.

This module defines the custom exceptions used by the web search API
for handling errors in a consistent way.
"""


class SearchError(Exception):
    """Base exception for search-related errors."""

    def __init__(self, message: str) -> None:
        """
        Initialize the exception with a message.

        Args:
            message: Error message explaining what went wrong
        """
        super().__init__(message)


class EngineError(SearchError):
    """Error for an issue with a specific search engine."""

    def __init__(self, engine_name: str, message: str) -> None:
        """
        Initialize the exception with an engine name and message.

        Args:
            engine_name: Name of the search engine that encountered the error
            message: Error message explaining what went wrong
        """
        super().__init__(f"Engine '{engine_name}': {message}")
        self.engine_name = engine_name
