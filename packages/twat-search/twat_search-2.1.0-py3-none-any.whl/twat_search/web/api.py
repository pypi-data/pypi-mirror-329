import asyncio
import logging
from typing import Any, Optional

from .config import Config
from .models import SearchResult
from .engines.base import SearchEngine, get_engine
from .exceptions import SearchError

logger = logging.getLogger(__name__)


def get_engine_params(
    engine_name: str, engines: list[str], kwargs: dict, common_params: dict
) -> dict:
    """
    Build engine-specific parameters by merging:
    - parameters prefixed with the engine name,
    - any non-prefixed parameters,
    - and the common parameters.
    """
    engine_specific = {
        k[len(engine_name) + 1 :]: v
        for k, v in kwargs.items()
        if k.startswith(engine_name + "_")
    }
    non_prefixed = {
        k: v
        for k, v in kwargs.items()
        if not any(k.startswith(e + "_") for e in engines)
    }
    return {**common_params, **engine_specific, **non_prefixed}


def init_engine_task(
    engine_name: str,
    config: Config,
    engines: list[str],
    kwargs: dict,
    common_params: dict,
    query: str,
) -> tuple[str, Any] | None:
    """
    Initialize a search engine task. If the engine is not configured or fails
    to initialize (due to missing dependencies, etc.), return None.
    """
    engine_config = config.engines.get(engine_name)
    if not engine_config:
        logger.warning(f"Engine '{engine_name}' not configured.")
        return None

    try:
        engine_params = get_engine_params(engine_name, engines, kwargs, common_params)
        engine_instance: SearchEngine = get_engine(
            engine_name, engine_config, **engine_params
        )
        logger.info(f"🔍 Querying engine: {engine_name}")
        return (engine_name, engine_instance.search(query))
    except (ImportError, KeyError) as e:
        logger.warning(
            f"Engine '{engine_name}' is not available: {e}. The dependency may not be installed."
        )
        return None
    except Exception as e:
        logger.error(f"Error initializing engine '{engine_name}': {e}")
        return None


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
        config = config or Config()
        engines = engines or list(config.engines.keys())
        if not engines:
            msg = "No search engines configured"
            raise SearchError(msg)

        common_params = {
            k: v
            for k, v in {
                "num_results": num_results,
                "country": country,
                "language": language,
                "safe_search": safe_search,
                "time_frame": time_frame,
            }.items()
            if v is not None
        }

        tasks = []
        engine_names = []
        for engine_name in engines:
            task = init_engine_task(
                engine_name, config, engines, kwargs, common_params, query
            )
            if task is not None:
                engine_names.append(task[0])
                tasks.append(task[1])

        if not tasks:
            msg = "No search engines could be initialized. Make sure at least one engine dependency is installed."
            raise SearchError(msg)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for engine_name, result in zip(engine_names, results, strict=False):
            if isinstance(result, Exception):
                logger.error(f"Search with engine '{engine_name}' failed: {result}")
            elif isinstance(result, list):
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
