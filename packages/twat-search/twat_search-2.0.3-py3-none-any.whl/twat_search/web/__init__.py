#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["httpx", "pydantic"]
# ///
# this_file: src/twat_search/web/__init__.py

"""
Unified web search API across multiple search engines.

This package provides a single interface for searching across
multiple search engines, handling the differences between APIs
and providing a consistent result format.
"""

# Initialize empty __all__ list
__all__ = []

# Import core functionality first
try:
    from .api import search
    from .models import SearchResult
    from .config import Config, EngineConfig

    __all__.extend(["Config", "EngineConfig", "SearchResult", "search"])
except ImportError:
    pass

# Import search engines with try-except blocks to handle optional dependencies
try:
    from .engines import brave, brave_news

    __all__.extend(["brave", "brave_news"])
except ImportError:
    pass

try:
    from .engines import pplx

    __all__.extend(["pplx"])
except ImportError:
    pass

try:
    from .engines import serpapi

    __all__.extend(["serpapi"])
except ImportError:
    pass

try:
    from .engines import tavily

    __all__.extend(["tavily"])
except ImportError:
    pass

try:
    from .engines import you, you_news

    __all__.extend(["you", "you_news"])
except ImportError:
    pass

try:
    from .engines import critique

    __all__.extend(["critique"])
except ImportError:
    pass

try:
    from .engines import duckduckgo

    __all__.extend(["duckduckgo"])
except ImportError:
    pass

try:
    from .engines import bing_scraper

    __all__.extend(["bing_scraper"])
except ImportError:
    pass
