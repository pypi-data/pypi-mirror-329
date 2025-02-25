# this_file: src/twat_search/web/engines/you.py

"""
You.com Search engine implementation.

This module implements the You.com Search API integration.
"""

import httpx
from typing import Any, ClassVar
from pydantic import BaseModel, ValidationError, HttpUrl, Field

from twat_search.web.config import EngineConfig
from twat_search.web.models import SearchResult
from .base import SearchEngine, register_engine
from twat_search.web.exceptions import EngineError


class YouSearchHit(BaseModel):
    """
    Pydantic model for a single You.com search hit.

    This model is used to validate the response from the You.com API.
    """

    title: str
    url: HttpUrl
    snippet: str = Field(alias="description")


class YouSearchResponse(BaseModel):
    """
    Pydantic model for the entire You.com API response.

    This captures the essential parts of the response.
    """

    hits: list[YouSearchHit]
    search_id: str | None = Field(None, alias="searchId")


@register_engine
class YouSearchEngine(SearchEngine):
    """Implementation of the You.com Web Search API."""

    name = "you"
    env_api_key_names: ClassVar[list[str]] = ["YOU_API_KEY"]

    def __init__(
        self,
        config: EngineConfig,
        num_results: int = 5,
        country: str | None = None,
        language: str | None = None,
        safe_search: bool | None = True,
        time_frame: str | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the You.com search engine.

        Args:
            config: Engine configuration
            num_results: Number of results to return (maps to 'num_web_results')
            country: Country code for results (maps to 'country_code')
            language: Language code for results
            safe_search: Whether to enable safe search
            time_frame: Time frame for results
            **kwargs: Additional You.com-specific parameters
        """
        super().__init__(config)

        # API endpoint
        self.base_url = "https://api.you.com/api/search"

        # Map common parameters to You-specific ones
        num_web_results = kwargs.get("num_web_results", num_results)
        self.num_web_results = num_web_results or self.config.default_params.get(
            "num_web_results", 5
        )

        country_code = kwargs.get("country_code", country)
        self.country_code = country_code or self.config.default_params.get(
            "country_code", None
        )

        self.safe_search = (
            safe_search
            or kwargs.get("safe_search")
            or self.config.default_params.get("safe_search", True)
        )

        # Check if API key is available
        if not self.config.api_key:
            raise EngineError(
                self.name,
                f"You.com API key is required. Set it via one of these env vars: {', '.join(self.env_api_key_names)}",
            )

        # API authentication headers
        self.headers = {
            "X-API-Key": self.config.api_key,
            "Accept": "application/json",
        }

    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a search using the You.com Search API.

        Args:
            query: The search query string

        Returns:
            A list of SearchResult objects

        Raises:
            EngineError: If the search fails
        """
        params: dict[str, Any] = {"q": query, "num_web_results": self.num_web_results}

        # Add optional parameters if they have values
        if self.country_code:
            params["country_code"] = self.country_code
        if self.safe_search is not None:  # Explicit check since it's a boolean
            params["safe_search"] = str(self.safe_search).lower()

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.base_url, headers=self.headers, params=params, timeout=10
                )
                response.raise_for_status()  # Raise HTTPError for bad responses

                data = response.json()
                you_response = YouSearchResponse(**data)

                results = []
                for hit in you_response.hits:
                    try:
                        # Convert to common SearchResult format
                        results.append(
                            SearchResult(
                                title=hit.title,
                                url=hit.url,
                                snippet=hit.snippet,
                                source=self.name,
                                raw=hit.model_dump(
                                    by_alias=True
                                ),  # Include raw result for debugging
                            )
                        )
                    except ValidationError:
                        # Log the specific validation error and skip this result
                        continue

                return results

            except httpx.RequestError as exc:
                raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc
            except httpx.HTTPStatusError as exc:
                raise EngineError(
                    self.name,
                    f"HTTP Status error: {exc.response.status_code} - {exc.response.text}",
                ) from exc
            except ValidationError as exc:
                raise EngineError(self.name, f"Response parsing error: {exc}") from exc


class YouNewsArticle(BaseModel):
    """
    Pydantic model for a single You.com news article.

    This model is used to validate the response from the You.com News API.
    """

    title: str
    url: HttpUrl
    snippet: str = Field(alias="description")
    source: str | None = None
    published_date: str | None = None


class YouNewsResponse(BaseModel):
    """
    Pydantic model for the entire You.com News API response.

    This captures the essential parts of the response.
    """

    articles: list[YouNewsArticle]
    search_id: str | None = Field(None, alias="searchId")


@register_engine
class YouNewsSearchEngine(SearchEngine):
    """Implementation of the You.com News Search API."""

    name = "you-news"
    env_api_key_names: ClassVar[list[str]] = ["YOU_API_KEY"]

    def __init__(
        self,
        config: EngineConfig,
        num_results: int = 5,
        country: str | None = None,
        language: str | None = None,
        safe_search: bool | None = True,
        time_frame: str | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the You.com news search engine.

        Args:
            config: Engine configuration
            num_results: Number of results to return (maps to 'num_news_results')
            country: Country code for results (maps to 'country_code')
            language: Language code for results
            safe_search: Whether to enable safe search
            time_frame: Time frame for results
            **kwargs: Additional You.com-specific parameters
        """
        super().__init__(config)

        # API endpoint
        self.base_url = "https://api.you.com/api/news"

        # Map common parameters to You-specific ones
        num_news_results = kwargs.get("num_news_results", num_results)
        self.num_news_results = num_news_results or self.config.default_params.get(
            "num_news_results", 5
        )

        country_code = kwargs.get("country_code", country)
        self.country_code = country_code or self.config.default_params.get(
            "country_code", None
        )

        self.safe_search = (
            safe_search
            or kwargs.get("safe_search")
            or self.config.default_params.get("safe_search", True)
        )

        # Check if API key is available
        if not self.config.api_key:
            raise EngineError(
                self.name,
                f"You.com API key is required. Set it via one of these env vars: {', '.join(self.env_api_key_names)}",
            )

        # API authentication headers
        self.headers = {
            "X-API-Key": self.config.api_key,
            "Accept": "application/json",
        }

    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a news search using the You.com News API.

        Args:
            query: The search query string

        Returns:
            A list of SearchResult objects

        Raises:
            EngineError: If the search fails
        """
        params: dict[str, Any] = {"q": query, "num_news_results": self.num_news_results}

        # Add optional parameters if they have values
        if self.country_code:
            params["country_code"] = self.country_code
        if self.safe_search is not None:  # Explicit check since it's a boolean
            params["safe_search"] = str(self.safe_search).lower()

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.base_url, headers=self.headers, params=params, timeout=10
                )
                response.raise_for_status()  # Raise HTTPError for bad responses

                data = response.json()
                you_response = YouNewsResponse(**data)

                results = []
                for article in you_response.articles:
                    try:
                        # Build a richer snippet if we have source and date
                        snippet = article.snippet
                        if article.source and article.published_date:
                            snippet = f"{snippet} - {article.source} ({article.published_date})"
                        elif article.source:
                            snippet = f"{snippet} - {article.source}"

                        # Convert to common SearchResult format
                        results.append(
                            SearchResult(
                                title=article.title,
                                url=article.url,
                                snippet=snippet,
                                source=self.name,
                                raw=article.model_dump(
                                    by_alias=True
                                ),  # Include raw result for debugging
                            )
                        )
                    except ValidationError:
                        # Log the specific validation error and skip this result
                        continue

                return results

            except httpx.RequestError as exc:
                raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc
            except httpx.HTTPStatusError as exc:
                raise EngineError(
                    self.name,
                    f"HTTP Status error: {exc.response.status_code} - {exc.response.text}",
                ) from exc
            except ValidationError as exc:
                raise EngineError(self.name, f"Response parsing error: {exc}") from exc


# For backward compatibility
YoucomSearchEngine = YouSearchEngine


async def you(
    query: str,
    num_results: int = 5,
    country: str | None = None,
    language: str | None = None,
    safe_search: bool | None = True,
    time_frame: str | None = None,
    api_key: str | None = None,
) -> list[SearchResult]:
    """
    Search You.com web search.

    Args:
        query: Search query string
        num_results: Number of results to return (1-20)
        country: Country code (e.g., "US", "GB", "FR")
        language: Language code (e.g., "en", "fr", "de")
        safe_search: Whether to enable safe search
        time_frame: Time filter (not used in You.com)
        api_key: Optional API key (otherwise use environment variable)

    Returns:
        List of search results
    """
    config = EngineConfig(
        api_key=api_key,
        enabled=True,
    )

    engine = YouSearchEngine(
        config,
        num_results=num_results,
        country=country,
        language=language,
        safe_search=safe_search,
        time_frame=time_frame,
    )

    return await engine.search(query)


async def you_news(
    query: str,
    num_results: int = 5,
    country: str | None = None,
    language: str | None = None,
    safe_search: bool | None = True,
    time_frame: str | None = None,
    api_key: str | None = None,
) -> list[SearchResult]:
    """
    Search You.com news.

    Args:
        query: Search query string
        num_results: Number of results to return (1-20)
        country: Country code (e.g., "US", "GB", "FR")
        language: Language code (e.g., "en", "fr", "de")
        safe_search: Whether to enable safe search
        time_frame: Time filter (not used in You.com)
        api_key: Optional API key (otherwise use environment variable)

    Returns:
        List of search results
    """
    config = EngineConfig(
        api_key=api_key,
        enabled=True,
    )

    engine = YouNewsSearchEngine(
        config,
        num_results=num_results,
        country=country,
        language=language,
        safe_search=safe_search,
        time_frame=time_frame,
    )

    return await engine.search(query)


# Alias for backward compatibility
youcom = you
