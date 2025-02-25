# this_file: src/twat_search/web/engines/__init__.py

"""
Search engine implementations.

This package contains the implementations of various search engines that
can be used with the twat_search.web API.
"""

# Initialize empty __all__ list
__all__ = []

# Dict to track available engine functions
available_engine_functions = {}

# Import base functionality first
try:
    from .base import register_engine, get_engine, get_registered_engines, SearchEngine

    __all__.extend(
        ["SearchEngine", "register_engine", "get_engine", "get_registered_engines"]
    )
except ImportError:
    pass

# Import each engine module and add its components to __all__ if successful
try:
    from .brave import BraveSearchEngine, BraveNewsSearchEngine, brave, brave_news

    available_engine_functions["brave"] = brave
    available_engine_functions["brave_news"] = brave_news
    __all__.extend(
        ["BraveSearchEngine", "BraveNewsSearchEngine", "brave", "brave_news"]
    )
except ImportError:
    pass

try:
    from .serpapi import SerpApiSearchEngine, serpapi

    available_engine_functions["serpapi"] = serpapi
    __all__.extend(["SerpApiSearchEngine", "serpapi"])
except ImportError:
    pass

try:
    from .tavily import TavilySearchEngine, tavily

    available_engine_functions["tavily"] = tavily
    __all__.extend(["TavilySearchEngine", "tavily"])
except ImportError:
    pass

try:
    from .pplx import PerplexitySearchEngine, pplx

    available_engine_functions["pplx"] = pplx
    __all__.extend(["PerplexitySearchEngine", "pplx"])
except ImportError:
    pass

try:
    from .you import YouSearchEngine, YouNewsSearchEngine, you, you_news

    available_engine_functions["you"] = you
    available_engine_functions["you_news"] = you_news
    __all__.extend(["YouSearchEngine", "YouNewsSearchEngine", "you", "you_news"])
except ImportError:
    pass

try:
    from .critique import CritiqueSearchEngine, critique

    available_engine_functions["critique"] = critique
    __all__.extend(["CritiqueSearchEngine", "critique"])
except ImportError:
    pass

try:
    from .duckduckgo import DuckDuckGoSearchEngine, duckduckgo

    available_engine_functions["duckduckgo"] = duckduckgo
    __all__.extend(["DuckDuckGoSearchEngine", "duckduckgo"])
except ImportError:
    pass

try:
    from .bing_scraper import BingScraperSearchEngine, bing_scraper

    available_engine_functions["bing_scraper"] = bing_scraper
    __all__.extend(["BingScraperSearchEngine", "bing_scraper"])
except ImportError:
    pass


# Add helper functions to the exports
def is_engine_available(engine_name: str) -> bool:
    """Check if an engine is available (its dependencies are installed).

    Args:
        engine_name: Name of the engine to check

    Returns:
        True if the engine is available, False otherwise
    """
    return engine_name in available_engine_functions


def get_engine_function(engine_name: str):
    """Get the function for a specific engine.

    Args:
        engine_name: Name of the engine

    Returns:
        The engine function if available, None otherwise
    """
    return available_engine_functions.get(engine_name)


def get_available_engines() -> list[str]:
    """Get a list of all available engine names.

    Returns:
        List of available engine names
    """
    return list(available_engine_functions.keys())


# Add helper functions to exports
__all__.extend(
    [
        "available_engine_functions",
        "is_engine_available",
        "get_engine_function",
        "get_available_engines",
    ]
)
