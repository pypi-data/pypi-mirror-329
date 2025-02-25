# this_file: src/twat_search/web/engines/__init__.py

"""
Search engine implementations.

This package contains the implementations of various search engines that
can be used with the twat_search.web API.
"""

from .base import register_engine, get_engine, get_registered_engines, SearchEngine
from .brave import BraveSearchEngine, BraveNewsSearchEngine, brave, brave_news
from .serpapi import SerpApiSearchEngine, serpapi
from .tavily import TavilySearchEngine, tavily
from .pplx import PerplexitySearchEngine, pplx
from .you import YouSearchEngine, YouNewsSearchEngine, you, you_news
from .critique import CritiqueSearchEngine, critique
from .duckduckgo import DuckDuckGoSearchEngine, duckduckgo

__all__ = [
    "BraveNewsSearchEngine",
    # Engine classes
    "BraveSearchEngine",
    "CritiqueSearchEngine",
    "DuckDuckGoSearchEngine",
    "PerplexitySearchEngine",
    # Base classes and functions
    "SearchEngine",
    "SerpApiSearchEngine",
    "TavilySearchEngine",
    "YouNewsSearchEngine",
    "YouSearchEngine",
    # Convenience functions
    "brave",
    "brave_news",
    "critique",
    "duckduckgo",
    "get_engine",
    "get_registered_engines",
    "pplx",
    "register_engine",
    "serpapi",
    "tavily",
    "you",
    "you_news",
]
