# this_file: src/twat_search/web/engines/tavily.py

"""
Tavily Search engine implementation.

This module implements the Tavily Search API integration.
"""

import httpx
import textwrap
from typing import Any, ClassVar
from pydantic import BaseModel, ValidationError
from pydantic.networks import HttpUrl

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
    url: str  # Tavily might return non-standard URLs, so we use str
    content: str  # Tavily returns full content, not just a snippet
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

        All external parameters and API signatures remain unchanged.
        """
        super().__init__(config)
        self.base_url = "https://api.tavily.com/search"

        # Helper to apply default values from config if no value was provided.
        def get_default(value, key, fallback):
            return (
                value
                if value is not None
                else self.config.default_params.get(key, fallback)
            )

        # Map common parameters to Tavily-specific ones
        self.max_results = get_default(
            kwargs.get("max_results", num_results), "max_results", 5
        )
        self.search_depth = get_default(search_depth, "search_depth", "basic")
        self.include_domains = get_default(include_domains, "include_domains", None)
        self.exclude_domains = get_default(exclude_domains, "exclude_domains", None)
        self.include_answer = get_default(include_answer, "include_answer", False)
        self.max_tokens = get_default(max_tokens, "max_tokens", None)
        self.search_type = get_default(search_type, "search_type", "search")

        # Store unused unified parameters for future compatibility.
        self.country = country
        self.language = language
        self.safe_search = safe_search
        self.time_frame = time_frame

        # Prepare headers.
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        if not self.config.api_key:
            raise EngineError(
                self.name,
                f"Tavily API key is required. Set it via one of these env vars: {', '.join(self.env_api_key_names)}",
            )

    def _build_payload(self, query: str) -> dict:
        """
        Build the payload for the Tavily API request.
        """
        payload = {
            "api_key": self.config.api_key,
            "query": query,
            "max_results": self.max_results,
            "search_depth": self.search_depth,
            "type": self.search_type,
        }
        if self.include_domains is not None:
            payload["include_domains"] = self.include_domains
        if self.exclude_domains is not None:
            payload["exclude_domains"] = self.exclude_domains
        if self.include_answer is not None:
            payload["include_answer"] = self.include_answer
        if self.max_tokens is not None:
            payload["max_tokens"] = self.max_tokens
        return payload

    def _convert_result(self, item: dict, rank: int) -> SearchResult | None:
        """
        Convert a single Tavily result dict to a SearchResult object.
        """
        try:
            validated_url = HttpUrl(item.get("url", ""))
            return SearchResult(
                title=item.get("title", ""),
                url=validated_url,
                snippet=textwrap.shorten(
                    item.get("content", "").strip(), width=500, placeholder="..."
                ),
                source=self.name,
                rank=rank,
                raw=item,
            )
        except ValidationError:
            return None

    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a search using the Tavily API.

        Returns:
            A list of SearchResult objects.
        """
        payload = self._build_payload(query)

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.base_url, headers=self.headers, json=payload, timeout=10
                )
                response.raise_for_status()
                data = response.json()
            except httpx.HTTPStatusError as e:
                raise EngineError(self.name, f"HTTP error: {e}")
            except httpx.RequestError as e:
                raise EngineError(self.name, f"Request error: {e}")
            except Exception as e:
                raise EngineError(self.name, f"Error: {e!s}")

        results = []
        # Attempt to use Pydantic validation for a cleaner conversion.
        try:
            parsed_response = TavilySearchResponse.parse_obj(data)
            items = [item.dict() for item in parsed_response.results]
        except ValidationError:
            items = data.get("results", [])

        for idx, item in enumerate(items, start=1):
            converted = self._convert_result(item, idx)
            if converted:
                results.append(converted)

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

    This function’s API and signature remain identical.
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
