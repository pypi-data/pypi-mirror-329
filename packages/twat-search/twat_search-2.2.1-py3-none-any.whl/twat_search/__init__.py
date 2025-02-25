"""
TwAT Search package - Tools for web search and information retrieval.

This package provides utilities for searching the web and retrieving information
from various sources.
"""

# Initialize empty __all__ list
__all__ = []

# Include version
try:
    from .__version__ import version as __version__

    __all__.append("__version__")
except ImportError:
    __version__ = "0.1.0"  # Fallback version
    __all__.append("__version__")

# Import submodules if available
try:
    from . import web

    __all__.append("web")
except ImportError:
    pass
