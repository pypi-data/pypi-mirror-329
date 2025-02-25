# this_file: src/twat_search/web/engines/brave.py

"""
Brave Search engine implementation.

This module implements the Brave Search API integration.
"""

import httpx
from typing import Any, ClassVar
from pydantic import BaseModel, ValidationError, HttpUrl

from twat_search.web.config import EngineConfig
from twat_search.web.models import SearchResult
from .base import SearchEngine, register_engine
from twat_search.web.exceptions import EngineError


class BraveResult(BaseModel):
    """
    Pydantic model for a single Brave search result.

    This model is used to validate the response from the Brave API.
    """

    title: str
    url: HttpUrl
    description: str


class BraveResponse(BaseModel):
    """
    Pydantic model for the entire Brave API response.

    This is a simplified model that only captures the essentials.
    """

    web: dict[str, Any]


@register_engine
class BraveSearchEngine(SearchEngine):
    """Implementation of the Brave Search API."""

    name = "brave"
    env_api_key_names: ClassVar[list[str]] = ["BRAVE_API_KEY"]

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
        Initialize Brave Search engine.

        Args:
            config: Engine configuration
            num_results: Number of results to return (maps to 'count')
            country: Country code for results
            language: Language code for results (maps to 'search_lang')
            safe_search: Whether to enable safe search (boolean or string: 'strict', 'moderate', 'off')
            time_frame: Time frame for results (maps to 'freshness')
            **kwargs: Additional Brave-specific parameters
        """
        super().__init__(config)

        # API endpoint
        self.base_url = "https://api.search.brave.com/res/v1/web/search"

        # Map common parameters to Brave-specific ones
        count = kwargs.get("count", num_results)
        self.count = count or self.config.default_params.get("count", 10)

        self.country = (
            country
            or kwargs.get("country")
            or self.config.default_params.get("country", None)
        )

        search_lang = kwargs.get("search_lang", language)
        self.search_lang = search_lang or self.config.default_params.get(
            "search_lang", None
        )

        ui_lang = kwargs.get("ui_lang", language)
        self.ui_lang = ui_lang or self.config.default_params.get("ui_lang", None)

        safe = kwargs.get("safe_search", safe_search)
        # Handle boolean to string conversion for safe_search
        if isinstance(safe, bool) and safe is True:
            safe = "strict"
        elif isinstance(safe, bool) and safe is False:
            safe = "off"
        self.safe_search = safe or self.config.default_params.get("safe_search", None)

        freshness = kwargs.get("freshness", time_frame)
        self.freshness = freshness or self.config.default_params.get("freshness", None)

        # Check if API key is available
        if not self.config.api_key:
            raise EngineError(
                self.name,
                f"Brave API key is required. Set it via one of these env vars: {', '.join(self.env_api_key_names)}",
            )

        self.headers = {
            "Accept": "application/json",
            "X-Subscription-Token": self.config.api_key,
        }

    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a search using the Brave Search API.

        Args:
            query: The search query string

        Returns:
            A list of SearchResult objects

        Raises:
            EngineError: If the search fails
        """
        params: dict[str, Any] = {"q": query, "count": self.count}

        # Add optional parameters if they have values
        if self.country:
            params["country"] = self.country
        if self.search_lang:
            params["search_lang"] = self.search_lang
        if self.ui_lang:
            params["ui_lang"] = self.ui_lang
        if self.safe_search:
            params["safe_search"] = self.safe_search
        if self.freshness:
            params["freshness"] = self.freshness

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.base_url, headers=self.headers, params=params, timeout=10
                )
                response.raise_for_status()  # Raise HTTPError for bad responses

                data = response.json()
                brave_response = BraveResponse(**data)

                results = []
                # Ensure web and results exist
                if brave_response.web and brave_response.web.get("results"):
                    for result in brave_response.web["results"]:
                        try:
                            # Validate and convert to BraveResult
                            brave_result = BraveResult(**result)

                            # Convert to common SearchResult format
                            # The URL is already a validated HttpUrl object from Pydantic
                            results.append(
                                SearchResult(
                                    title=brave_result.title,
                                    url=brave_result.url,
                                    snippet=brave_result.description,
                                    source=self.name,
                                    raw=result,  # Include raw result for debugging
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


class BraveNewsResult(BaseModel):
    """
    Pydantic model for a single Brave News search result.

    This model is used to validate the response from the Brave News API.
    """

    title: str
    url: HttpUrl
    description: str
    published_time: str | None = None
    publisher: str | None = None


class BraveNewsResponse(BaseModel):
    """
    Pydantic model for the entire Brave News API response.

    This is a simplified model that only captures the essentials.
    """

    news: dict[str, Any]


@register_engine
class BraveNewsSearchEngine(SearchEngine):
    """Implementation of the Brave News Search API."""

    name = "brave-news"
    env_api_key_names: ClassVar[list[str]] = ["BRAVE_API_KEY"]

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
        Initialize Brave News search engine.

        Args:
            config: Engine configuration
            num_results: Number of results to return (maps to 'count')
            country: Country code for results
            language: Language code for results (maps to 'search_lang')
            safe_search: Whether to enable safe search (boolean or string: 'strict', 'moderate', 'off')
            time_frame: Time frame for results (maps to 'freshness')
            **kwargs: Additional Brave-specific parameters
        """
        super().__init__(config)

        # API endpoint
        self.base_url = "https://api.search.brave.com/res/v1/news/search"

        # Map common parameters to Brave-specific ones
        count = kwargs.get("count", num_results)
        self.count = count or self.config.default_params.get("count", 10)

        self.country = (
            country
            or kwargs.get("country")
            or self.config.default_params.get("country", None)
        )

        search_lang = kwargs.get("search_lang", language)
        self.search_lang = search_lang or self.config.default_params.get(
            "search_lang", None
        )

        ui_lang = kwargs.get("ui_lang", language)
        self.ui_lang = ui_lang or self.config.default_params.get("ui_lang", None)

        safe = kwargs.get("safe_search", safe_search)
        # Handle boolean to string conversion for safe_search
        if isinstance(safe, bool) and safe is True:
            safe = "strict"
        elif isinstance(safe, bool) and safe is False:
            safe = "off"
        self.safe_search = safe or self.config.default_params.get("safe_search", None)

        freshness = kwargs.get("freshness", time_frame)
        self.freshness = freshness or self.config.default_params.get("freshness", None)

        # Check if API key is available
        if not self.config.api_key:
            raise EngineError(
                self.name,
                f"Brave API key is required. Set it via one of these env vars: {', '.join(self.env_api_key_names)}",
            )

        # API authentication headers
        self.headers = {
            "Accept": "application/json",
            "X-Subscription-Token": self.config.api_key,
        }

    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a news search using the Brave News Search API.

        Args:
            query: The search query string

        Returns:
            A list of SearchResult objects

        Raises:
            EngineError: If the search fails
        """
        params: dict[str, Any] = {"q": query, "count": self.count}

        # Add optional parameters if they have values
        if self.country:
            params["country"] = self.country
        if self.search_lang:
            params["search_lang"] = self.search_lang
        if self.ui_lang:
            params["ui_lang"] = self.ui_lang
        if self.freshness:
            params["freshness"] = self.freshness

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.base_url, headers=self.headers, params=params, timeout=10
                )
                response.raise_for_status()  # Raise HTTPError for bad responses

                data = response.json()
                brave_response = BraveNewsResponse(**data)

                results = []
                # Ensure news and results exist
                if brave_response.news and brave_response.news.get("results"):
                    for result in brave_response.news["results"]:
                        try:
                            # Validate and convert to BraveNewsResult
                            brave_result = BraveNewsResult(**result)

                            # Build a snippet that includes publication info if available
                            snippet = brave_result.description
                            if brave_result.publisher and brave_result.published_time:
                                snippet = f"{snippet} - {brave_result.publisher} ({brave_result.published_time})"
                            elif brave_result.publisher:
                                snippet = f"{snippet} - {brave_result.publisher}"

                            # Convert to common SearchResult format
                            # The URL is already a validated HttpUrl object from Pydantic
                            results.append(
                                SearchResult(
                                    title=brave_result.title,
                                    url=brave_result.url,
                                    snippet=snippet,
                                    source=self.name,
                                    raw=result,  # Include raw result for debugging
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


async def brave(
    query: str,
    num_results: int = 5,
    country: str | None = None,
    language: str | None = None,
    safe_search: bool | str | None = True,
    time_frame: str | None = None,
    api_key: str | None = None,
) -> list[SearchResult]:
    """
    Search Brave web search.

    Args:
        query: Search query string
        num_results: Number of results to return (1-20)
        country: Country code (e.g., "US", "GB", "FR")
        language: Language code (e.g., "en", "fr", "de")
        safe_search: Safe search level (True = strict, False = off, or "moderate")
        time_frame: Time filter (e.g., "past_day", "past_week", "past_month")
        api_key: Optional API key (otherwise use environment variable)

    Returns:
        List of search results
    """
    config = EngineConfig(
        api_key=api_key,
        enabled=True,
    )

    engine = BraveSearchEngine(
        config,
        num_results=num_results,
        country=country,
        language=language,
        safe_search=safe_search,
        time_frame=time_frame,
    )

    return await engine.search(query)


async def brave_news(
    query: str,
    num_results: int = 5,
    country: str | None = None,
    language: str | None = None,
    safe_search: bool | str | None = True,
    time_frame: str | None = None,
    api_key: str | None = None,
) -> list[SearchResult]:
    """
    Search Brave news.

    Args:
        query: Search query string
        num_results: Number of results to return (1-20)
        country: Country code (e.g., "US", "GB", "FR")
        language: Language code (e.g., "en", "fr", "de")
        safe_search: Safe search level (True = strict, False = off, or "moderate")
        time_frame: Time filter (e.g., "past_hour", "past_day", "past_week")
        api_key: Optional API key (otherwise use environment variable)

    Returns:
        List of search results
    """
    config = EngineConfig(
        api_key=api_key,
        enabled=True,
    )

    engine = BraveNewsSearchEngine(
        config,
        num_results=num_results,
        country=country,
        language=language,
        safe_search=safe_search,
        time_frame=time_frame,
    )

    return await engine.search(query)
