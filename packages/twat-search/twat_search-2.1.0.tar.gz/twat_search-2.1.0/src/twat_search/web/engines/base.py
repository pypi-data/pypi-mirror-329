# this_file: src/twat_search/web/engines/base.py

"""
Base class and factory functions for search engines.

This module defines the abstract base class that all search engines must
implement, as well as functions to register and instantiate engines.
"""

import abc
from typing import Any, ClassVar

from twat_search.web.config import EngineConfig
from twat_search.web.models import SearchResult
from twat_search.web.exceptions import SearchError


class SearchEngine(abc.ABC):
    """
    Abstract base class for all search engines.

    All search engine implementations must subclass this and implement
    the search method.
    """

    name: ClassVar[str] = ""  # Class attribute that must be defined by subclasses

    # Class attributes for environment variables
    env_api_key_names: ClassVar[list[str]] = []  # Override with engine-specific names
    env_enabled_names: ClassVar[list[str]] = []  # Override with engine-specific names
    env_params_names: ClassVar[list[str]] = []  # Override with engine-specific names

    def __init__(self, config: EngineConfig, **kwargs: Any) -> None:
        """
        Initialize the search engine with configuration and common parameters.

        Args:
            config: Engine configuration
            **kwargs: Additional engine-specific parameters
        """
        self.config = config
        self.kwargs = kwargs

        # Common parameters with default values
        self.num_results = kwargs.get("num_results", 5)
        self.country = kwargs.get("country", None)
        self.language = kwargs.get("language", None)
        self.safe_search = kwargs.get("safe_search", True)
        self.time_frame = kwargs.get("time_frame", None)

        if not config.enabled:
            msg = f"Engine '{self.name}' is disabled."
            raise SearchError(msg)

    @abc.abstractmethod
    async def search(self, query: str) -> list[SearchResult]:
        """
        Search using this engine.

        Args:
            query: The search query

        Returns:
            List of search results
        """
        pass


# Registry of available search engines
_engine_registry: dict[str, type[SearchEngine]] = {}


def register_engine(engine_class: type[SearchEngine]) -> type[SearchEngine]:
    """
    Register a search engine class.

    Args:
        engine_class: The search engine class to register

    Returns:
        The registered search engine class
    """
    _engine_registry[engine_class.name] = engine_class

    # Auto-generate environment variable names if not explicitly set
    if not hasattr(engine_class, "env_api_key_names"):
        engine_class.env_api_key_names = [f"{engine_class.name.upper()}_API_KEY"]
    if not hasattr(engine_class, "env_enabled_names"):
        engine_class.env_enabled_names = [f"{engine_class.name.upper()}_ENABLED"]
    if not hasattr(engine_class, "env_params_names"):
        engine_class.env_params_names = [f"{engine_class.name.upper()}_DEFAULT_PARAMS"]

    return engine_class


def get_engine(engine_name: str, config: EngineConfig, **kwargs: Any) -> SearchEngine:
    """
    Get a search engine instance by name.

    Args:
        engine_name: The name of the engine to get
        config: Engine configuration
        **kwargs: Additional engine-specific parameters

    Returns:
        An instance of the requested search engine
    """
    engine_class = _engine_registry.get(engine_name)
    if engine_class is None:
        msg = f"Unknown search engine: {engine_name}"
        raise SearchError(msg)

    return engine_class(config, **kwargs)


def get_registered_engines() -> dict[str, type[SearchEngine]]:
    """
    Get a dictionary of all registered search engines.

    Returns:
        Dictionary mapping engine names to engine classes
    """
    return _engine_registry.copy()
