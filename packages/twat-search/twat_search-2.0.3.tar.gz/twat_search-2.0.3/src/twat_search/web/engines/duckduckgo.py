#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["duckduckgo-search"]
# ///
# this_file: src/twat_search/web/engines/duckduckgo.py

"""
DuckDuckGo Search engine implementation.

This module implements the DuckDuckGo search API integration using the duckduckgo_search library.
"""

import logging
from typing import Any, ClassVar

from duckduckgo_search import DDGS
from pydantic import BaseModel, HttpUrl, ValidationError

from twat_search.web.config import EngineConfig
from twat_search.web.exceptions import EngineError
from twat_search.web.models import SearchResult
from .base import SearchEngine, register_engine

# Set up logging
logger = logging.getLogger(__name__)


class DuckDuckGoResult(BaseModel):
    """
    Pydantic model for a single DuckDuckGo search result.

    This model is used to validate the response from the DuckDuckGo API.
    """

    title: str
    href: HttpUrl
    body: str


@register_engine
class DuckDuckGoSearchEngine(SearchEngine):
    """Implementation of the DuckDuckGo Search API."""

    name = "duckduckgo"
    env_api_key_names: ClassVar[list[str]] = []  # No API key needed

    def __init__(
        self,
        config: EngineConfig,
        num_results: int = 5,
        country: str | None = None,
        language: str | None = None,
        safe_search: bool | str | None = True,
        time_frame: str | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize DuckDuckGo Search engine.

        Args:
            config: Engine configuration
            num_results: Number of results to return (maps to 'max_results')
            country: Country code for results (maps to 'region')
            language: Language code for results (not directly used by DuckDuckGo API, but kept for interface consistency)
            safe_search: Whether to enable safe search
            time_frame: Time frame for results (maps to 'timelimit')
            **kwargs: Additional DuckDuckGo-specific parameters
        """
        super().__init__(config, **kwargs)

        # Map common parameters to DuckDuckGo-specific ones
        max_results = kwargs.get("max_results", num_results)
        self.max_results = max_results or self.config.default_params.get(
            "max_results", 10
        )

        # Map country to region parameter in duckduckgo_search
        region = kwargs.get("region", country)
        self.region = region or self.config.default_params.get("region", None)

        # Store language parameter even though DuckDuckGo API doesn't directly use it
        # This is kept for consistency with other search engines
        self.language = language or self.config.default_params.get("language", None)
        if self.language:
            logger.debug(
                f"Language '{self.language}' set but not directly used by DuckDuckGo API"
            )

        # DuckDuckGo supports various time limits
        timelimit = kwargs.get("timelimit", time_frame)
        self.timelimit = timelimit or self.config.default_params.get("timelimit", None)

        # Convert time_frame to timelimit format if provided
        if self.timelimit and not kwargs.get("timelimit"):
            # Map common time_frame formats to DuckDuckGo timelimit
            time_mapping = {
                "day": "d",
                "week": "w",
                "month": "m",
                "year": "y",
            }
            self.timelimit = time_mapping.get(self.timelimit.lower(), self.timelimit)

        # Map safe_search to safesearch parameter
        # DuckDuckGo has a simple boolean safe search
        self.safesearch = kwargs.get("safesearch", safe_search)
        if isinstance(self.safesearch, str):
            if self.safesearch.lower() in ["off", "false"]:
                self.safesearch = False
            else:
                self.safesearch = True

        # Proxy support
        self.proxy = kwargs.get("proxy") or self.config.default_params.get(
            "proxy", None
        )
        self.timeout = kwargs.get("timeout") or self.config.default_params.get(
            "timeout", 10
        )

    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a search using the DuckDuckGo Search API.

        Args:
            query: The search query string

        Returns:
            A list of SearchResult objects

        Raises:
            EngineError: If the search fails
        """
        try:
            # Create DDGS instance with optional proxy
            ddgs = DDGS(proxy=self.proxy, timeout=self.timeout)

            # Convert parameters to format expected by DDGS.text()
            params = {
                "keywords": query,
                "max_results": self.max_results,
            }

            # Add optional parameters if they have values
            if self.region:
                params["region"] = self.region
            if self.timelimit:
                params["timelimit"] = self.timelimit
            if self.safesearch is not None:
                params["safesearch"] = self.safesearch

            # Call the duckduckgo_search library
            raw_results = ddgs.text(**params)

            results = []
            for result in raw_results:
                try:
                    # Validate and convert response
                    ddg_result = DuckDuckGoResult(
                        title=result["title"],
                        href=result["href"],
                        body=result["body"],
                    )

                    # Convert to common SearchResult format
                    results.append(
                        SearchResult(
                            title=ddg_result.title,
                            url=ddg_result.href,
                            snippet=ddg_result.body,
                            source=self.name,
                            raw=result,  # Include raw result for debugging
                        )
                    )
                except ValidationError as exc:
                    logger.warning(f"Validation error for result: {exc}")
                    continue

            return results

        except Exception as exc:
            raise EngineError(self.name, f"Search failed: {exc}") from exc


async def duckduckgo(
    query: str,
    num_results: int = 5,
    country: str | None = None,
    language: str | None = None,
    safe_search: bool = True,
    time_frame: str | None = None,
    proxy: str | None = None,
    timeout: int = 10,
    **kwargs: Any,
) -> list[SearchResult]:
    """
    Search using DuckDuckGo.

    This is a convenience function for searching with DuckDuckGo.

    Args:
        query: The search query
        num_results: Number of results to return
        country: Country code for results (maps to 'region')
        language: Language code for results (not directly used by DuckDuckGo API, but kept for consistency)
        safe_search: Whether to enable safe search
        time_frame: Time frame for results (maps to 'timelimit')
        proxy: Optional proxy to use for the request
        timeout: Timeout for the request in seconds
        **kwargs: Additional parameters to pass to the search engine

    Returns:
        A list of search results

    Raises:
        EngineError: If the search fails or the API key is missing
    """
    from twat_search.web.api import search

    return await search(
        query,
        engines=["duckduckgo"],
        num_results=num_results,
        country=country,
        language=language,
        safe_search=safe_search,
        time_frame=time_frame,
        duckduckgo_proxy=proxy,
        duckduckgo_timeout=timeout,
        **kwargs,
    )
