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

logger = logging.getLogger(__name__)


class DuckDuckGoResult(BaseModel):
    """
    Pydantic model for a single DuckDuckGo search result.
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
            config: Engine configuration.
            num_results: Number of results to return.
            country: Country code for results.
            language: Language code (not directly used by DuckDuckGo).
            safe_search: Whether to enable safe search.
            time_frame: Time frame for results.
            **kwargs: Additional DuckDuckGo-specific parameters.
        """
        super().__init__(config, **kwargs)
        (
            self.max_results,
            self.region,
            self.language,
            self.timelimit,
            self.safesearch,
            self.proxy,
            self.timeout,
        ) = self._map_init_params(
            num_results, country, language, safe_search, time_frame, kwargs, self.config
        )
        if self.language:
            logger.debug(
                f"Language '{self.language}' set but not directly used by DuckDuckGo API"
            )

    @staticmethod
    def _map_init_params(
        num_results: int,
        country: str | None,
        language: str | None,
        safe_search: bool | str | None,
        time_frame: str | None,
        kwargs: dict[str, Any],
        config: EngineConfig,
    ) -> tuple[int, str | None, str | None, str | None, bool, str | None, int]:
        """
        Map and normalize initialization parameters.
        """
        max_results = kwargs.get(
            "max_results", num_results
        ) or config.default_params.get("max_results", 10)
        region = kwargs.get("region", country) or config.default_params.get(
            "region", None
        )
        lang = language or config.default_params.get("language", None)
        timelimit = kwargs.get("timelimit", time_frame) or config.default_params.get(
            "timelimit", None
        )
        if timelimit and not kwargs.get("timelimit"):
            time_mapping = {"day": "d", "week": "w", "month": "m", "year": "y"}
            timelimit = time_mapping.get(timelimit.lower(), timelimit)
        safesearch = kwargs.get("safesearch", safe_search)
        if isinstance(safesearch, str):
            safesearch = False if safesearch.lower() in ["off", "false"] else True
        proxy = kwargs.get("proxy") or config.default_params.get("proxy", None)
        timeout = kwargs.get("timeout") or config.default_params.get("timeout", 10)
        return max_results, region, lang, timelimit, safesearch, proxy, timeout

    def _convert_result(self, raw: dict[str, Any]) -> SearchResult | None:
        """
        Convert a raw DuckDuckGo result to a SearchResult.
        """
        try:
            ddg_result = DuckDuckGoResult(
                title=raw["title"],
                href=raw["href"],
                body=raw["body"],
            )
            return SearchResult(
                title=ddg_result.title,
                url=ddg_result.href,
                snippet=ddg_result.body,
                source=self.name,
                raw=raw,
            )
        except ValidationError as exc:
            logger.warning(f"Validation error for result: {exc}")
            return None

    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a search using the DuckDuckGo Search API.

        Args:
            query: The search query string.

        Returns:
            A list of SearchResult objects.

        Raises:
            EngineError: If the search fails.
        """
        try:
            ddgs = DDGS(proxy=self.proxy, timeout=self.timeout)
            params = {"keywords": query, "max_results": self.max_results}
            if self.region:
                params["region"] = self.region
            if self.timelimit:
                params["timelimit"] = self.timelimit
            if self.safesearch is not None:
                params["safesearch"] = self.safesearch

            raw_results = ddgs.text(**params)
            results = []
            for raw in raw_results:
                converted = self._convert_result(raw)
                if converted:
                    results.append(converted)
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

    This convenience function uses the DuckDuckGo engine with the given parameters.

    Args:
        query: The search query.
        num_results: Number of results to return.
        country: Country code for results.
        language: Language code.
        safe_search: Whether to enable safe search.
        time_frame: Time frame for results.
        proxy: Optional proxy to use.
        timeout: Request timeout in seconds.
        **kwargs: Additional parameters.

    Returns:
        A list of search results.

    Raises:
        EngineError: If the search fails.
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
