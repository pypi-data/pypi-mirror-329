# this_file: src/twat_search/web/api.py

"""
Main API module for the web search functionality.

This module provides the main search function that allows searching across
multiple engines with a unified interface.
"""

import asyncio
import logging
from typing import Any, Optional

from .config import Config
from .models import SearchResult
from .engines.base import SearchEngine, get_engine
from .exceptions import SearchError

# Set up logging
logger = logging.getLogger(__name__)


async def search(
    query: str,
    engines: list[str] | None = None,
    num_results: int = 5,
    country: str | None = None,
    language: str | None = None,
    safe_search: bool = True,
    time_frame: str | None = None,
    config: Optional["Config"] = None,
    **kwargs: Any,
) -> list[SearchResult]:
    """
    Search across multiple engines.

    Args:
        query: The search query
        engines: List of engine names to use (or None for all enabled)
        num_results: Number of results to request from each engine (default: 5)
        country: Country code for search results
        language: Language code for search results
        safe_search: Whether to enable safe search (default: True)
        time_frame: Time frame for results (e.g., "day", "week", "month")
        config: Optional custom configuration
        **kwargs: Additional engine-specific parameters

    Returns:
        Combined list of search results from all engines

    Raises:
        SearchError: If no engines can be initialized
    """
    flattened_results: list[SearchResult] = []

    try:
        # Load configuration if not provided
        if config is None:
            config = Config()

        # Determine which engines to use
        if not engines:
            engines = list(config.engines.keys())

        if not engines:
            msg = "No search engines configured"
            raise SearchError(msg)

        # Common parameters for all engines
        common_params = {
            "num_results": num_results,
            "country": country,
            "language": language,
            "safe_search": safe_search,
            "time_frame": time_frame,
        }

        # Filter out None values
        common_params = {k: v for k, v in common_params.items() if v is not None}

        # Prepare search tasks
        search_tasks = []
        engine_names = []

        for engine_name in engines:
            try:
                # Get engine configuration
                engine_config = config.engines.get(engine_name)
                if not engine_config:
                    logger.warning(f"Engine '{engine_name}' not configured.")
                    continue

                # Extract engine-specific parameters from kwargs
                engine_params = {
                    k[len(engine_name) + 1 :]: v
                    for k, v in kwargs.items()
                    if k.startswith(engine_name + "_")
                }

                # Add additional parameters that don't have an engine prefix
                engine_params.update(
                    {
                        k: v
                        for k, v in kwargs.items()
                        if not any(k.startswith(e + "_") for e in engines)
                    }
                )

                # Merge common parameters with engine-specific ones
                engine_params = {**common_params, **engine_params}

                # Initialize the engine
                engine_instance: SearchEngine = get_engine(
                    engine_name, engine_config, **engine_params
                )

                logger.info(f"🔍 Querying engine: {engine_name}")
                engine_names.append(engine_name)
                search_tasks.append((engine_name, engine_instance.search(query)))
            except Exception as e:
                logger.error(f"Error initializing engine '{engine_name}': {e}")

        if not search_tasks:
            msg = "No search engines could be initialized"
            raise SearchError(msg)

        # Execute all search tasks concurrently
        search_coroutines = [task for _, task in search_tasks]
        results = await asyncio.gather(*search_coroutines, return_exceptions=True)

        # Process results
        for engine_name, result in zip(engine_names, results, strict=False):
            if isinstance(result, Exception):
                logger.error(f"Search with engine '{engine_name}' failed: {result}")
            elif isinstance(result, list):  # Check if results exist and is a list
                logger.info(f"✅ Engine '{engine_name}' returned {len(result)} results")
                flattened_results.extend(result)
            else:
                logger.info(
                    f"⚠️ Engine '{engine_name}' returned no results or unexpected type: {type(result)}"
                )
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise

    return flattened_results
