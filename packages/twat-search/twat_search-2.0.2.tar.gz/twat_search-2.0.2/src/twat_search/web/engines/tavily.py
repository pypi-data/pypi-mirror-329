# this_file: src/twat_search/web/engines/tavily.py

"""
Tavily Search engine implementation.

This module implements the Tavily Search API integration.
"""

import httpx
from typing import Any, ClassVar
from pydantic import BaseModel, ValidationError
from pydantic.networks import HttpUrl
import textwrap

from twat_search.web.config import EngineConfig
from twat_search.web.models import SearchResult
from .base import SearchEngine, register_engine
from twat_search.web.exceptions import EngineError


class TavilySearchResult(BaseModel):
    """
    Pydantic model for a single Tavily search result.

    This model is used to validate results from the Tavily API.
    """

    title: str
    url: str  # Use str instead of HttpUrl as Tavily might return non-standard URLs
    content: str  # Tavily returns content, not just a snippet
    score: float | None = None  # Relevance score, if available


class TavilySearchResponse(BaseModel):
    """
    Pydantic model for the entire Tavily API response.

    This model focuses on the results array.
    """

    results: list[TavilySearchResult]
    query: str
    search_id: str | None = None


@register_engine
class TavilySearchEngine(SearchEngine):
    """Implementation of the Tavily AI Search API."""

    name = "tavily"
    env_api_key_names: ClassVar[list[str]] = ["TAVILY_API_KEY"]

    def __init__(
        self,
        config: EngineConfig,
        num_results: int = 5,
        country: str | None = None,
        language: str | None = None,
        safe_search: bool | None = True,
        time_frame: str | None = None,
        search_depth: str = "basic",
        include_domains: list[str] | None = None,
        exclude_domains: list[str] | None = None,
        include_answer: bool = False,
        max_tokens: int | None = None,
        search_type: str = "search",
        **kwargs: Any,
    ) -> None:
        """
        Initialize the Tavily Search engine.

        Args:
            config: Engine configuration
            num_results: Number of results to return (maps to 'max_results')
            country: Country code for results (not directly used by Tavily)
            language: Language code for results (not directly used by Tavily)
            safe_search: Whether to enable safe search (not directly used by Tavily)
            time_frame: Time frame for results (not directly used by Tavily)
            search_depth: Search depth, either "basic" or "advanced"
            include_domains: List of domains to include in search
            exclude_domains: List of domains to exclude from search
            include_answer: Whether to include an AI-generated answer
            max_tokens: Maximum number of tokens for the answer
            search_type: Type of search ("search" or "news")
            **kwargs: Additional Tavily-specific parameters
        """
        super().__init__(config)

        self.base_url = "https://api.tavily.com/search"

        # Map common parameters to Tavily-specific ones
        max_results = kwargs.get("max_results", num_results)
        self.max_results = max_results or self.config.default_params.get(
            "max_results", 5
        )

        self.search_depth = search_depth or self.config.default_params.get(
            "search_depth", "basic"
        )
        self.include_domains = include_domains or self.config.default_params.get(
            "include_domains", None
        )
        self.exclude_domains = exclude_domains or self.config.default_params.get(
            "exclude_domains", None
        )
        self.include_answer = include_answer or self.config.default_params.get(
            "include_answer", False
        )
        self.max_tokens = max_tokens or self.config.default_params.get(
            "max_tokens", None
        )
        self.search_type = search_type or self.config.default_params.get(
            "search_type", "search"
        )

        # Store unused unified parameters for future compatibility
        self.country = country
        self.language = language
        self.safe_search = safe_search
        self.time_frame = time_frame

        # Prepare headers
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        # Check if API key is available
        if not self.config.api_key:
            raise EngineError(
                self.name,
                f"Tavily API key is required. Set it via one of these env vars: {', '.join(self.env_api_key_names)}",
            )

    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a search using the Tavily API.

        Args:
            query: The search query string

        Returns:
            A list of SearchResult objects

        Raises:
            EngineError: If the search fails
        """
        payload = {
            "api_key": self.config.api_key,
            "query": query,
            "max_results": self.max_results,
            "search_depth": self.search_depth,
            "type": self.search_type,
        }

        if self.include_domains:
            payload["include_domains"] = self.include_domains
        if self.exclude_domains:
            payload["exclude_domains"] = self.exclude_domains
        if self.include_answer:
            payload["include_answer"] = self.include_answer
        if self.max_tokens:
            payload["max_tokens"] = self.max_tokens

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.base_url, headers=self.headers, json=payload, timeout=10
                )
                response.raise_for_status()
                result = response.json()
            except httpx.HTTPStatusError as e:
                raise EngineError(self.name, f"HTTP error: {e}")
            except httpx.RequestError as e:
                raise EngineError(self.name, f"Request error: {e}")
            except Exception as e:
                raise EngineError(self.name, f"Error: {e!s}")

        results = []
        for idx, item in enumerate(result.get("results", []), 1):
            # Get the URL string
            url_str = item.get("url", "")

            try:
                # Convert to HttpUrl - this will validate the URL
                url = HttpUrl(url_str)

                results.append(
                    SearchResult(
                        title=item.get("title", ""),
                        url=url,
                        snippet=textwrap.shorten(
                            item.get("content", "").strip(),
                            width=500,
                            placeholder="...",
                        ),
                        source=self.name,
                        rank=idx,
                        raw=item,
                    )
                )
            except ValidationError:
                # Skip invalid URLs
                continue

        return results


async def tavily(
    query: str,
    num_results: int = 5,
    country: str | None = None,
    language: str | None = None,
    safe_search: bool | None = True,
    time_frame: str | None = None,
    search_depth: str = "basic",
    include_domains: list[str] | None = None,
    exclude_domains: list[str] | None = None,
    include_answer: bool = False,
    max_tokens: int | None = None,
    search_type: str = "search",
    api_key: str | None = None,
) -> list[SearchResult]:
    """
    Search using Tavily AI search.

    Args:
        query: Search query string
        num_results: Number of results to return
        country: Country code (not directly used by Tavily)
        language: Language code (not directly used by Tavily)
        safe_search: Whether to enable safe search (not directly used by Tavily)
        time_frame: Time filter (not directly used by Tavily)
        search_depth: Search depth, either "basic" or "advanced"
        include_domains: List of domains to include in search
        exclude_domains: List of domains to exclude from search
        include_answer: Whether to include an AI-generated answer
        max_tokens: Maximum number of tokens for the answer
        search_type: Type of search ("search" or "news")
        api_key: Optional API key (otherwise use environment variable)

    Returns:
        List of search results
    """
    config = EngineConfig(
        api_key=api_key,
        enabled=True,
    )

    engine = TavilySearchEngine(
        config,
        num_results=num_results,
        country=country,
        language=language,
        safe_search=safe_search,
        time_frame=time_frame,
        search_depth=search_depth,
        include_domains=include_domains,
        exclude_domains=exclude_domains,
        include_answer=include_answer,
        max_tokens=max_tokens,
        search_type=search_type,
    )

    return await engine.search(query)
