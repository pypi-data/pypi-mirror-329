"""
SerpApi Google search engine implementation.

This module implements the SerpApi Google Search API integration.
"""

import httpx
from typing import Any, ClassVar
from pydantic import BaseModel, ValidationError, HttpUrl

from twat_search.web.config import EngineConfig
from twat_search.web.models import SearchResult
from .base import SearchEngine, register_engine
from twat_search.web.exceptions import EngineError


class SerpApiResult(BaseModel):
    """
    Pydantic model for a single SerpApi Google search result.

    This model is used to validate the response from the SerpApi API.
    """

    title: str
    link: HttpUrl  # SerpApi uses 'link' for URLs
    snippet: str
    position: int | None = None


class SerpApiResponse(BaseModel):
    """
    Pydantic model for the entire SerpApi API response.

    This captures the essential parts of the response.
    """

    organic_results: list[SerpApiResult]
    search_metadata: dict[str, Any]
    search_parameters: dict[str, Any]


@register_engine
class SerpApiSearchEngine(SearchEngine):
    """Implementation of the SerpApi Google Search API."""

    name = "serpapi"
    env_api_key_names: ClassVar[list[str]] = ["SERPAPI_API_KEY"]

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
        Initialize the SerpApi search engine.

        Args:
            config: Engine configuration
            num_results: Number of results to return (maps to 'num')
            country: Country code for results (maps to 'gl')
            language: Language code for results (maps to 'hl')
            safe_search: Whether to enable safe search (maps to 'safe')
            time_frame: Time frame for results (maps to 'time_period')
            **kwargs: Additional SerpApi-specific parameters
        """
        super().__init__(config)
        self.base_url = "https://serpapi.com/search"

        # Consolidate parameter mappings into one dictionary to reduce duplication.
        self._params = {
            "num": kwargs.get("num", num_results)
            or self.config.default_params.get("num", 10),
            "google_domain": kwargs.get("google_domain")
            or self.config.default_params.get("google_domain", "google.com"),
            "gl": kwargs.get("gl", country) or self.config.default_params.get("gl"),
            "hl": kwargs.get("hl", language) or self.config.default_params.get("hl"),
            "safe": self._convert_safe(kwargs.get("safe", safe_search))
            or self.config.default_params.get("safe"),
            "time_period": kwargs.get("time_period", time_frame)
            or self.config.default_params.get("time_period"),
        }

        if not self.config.api_key:
            raise EngineError(
                self.name,
                f"SerpApi API key is required. Set it via one of these env vars: {', '.join(self.env_api_key_names)}",
            )

    def _convert_safe(self, safe: bool | str | None) -> str | None:
        """Convert safe_search boolean to SerpApi string parameter if needed."""
        if isinstance(safe, bool):
            return "active" if safe else "off"
        return safe

    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a search using the SerpApi Google Search API.

        Args:
            query: The search query string

        Returns:
            A list of SearchResult objects

        Raises:
            EngineError: If the search fails
        """
        params = {
            "q": query,
            "api_key": self.config.api_key,
            "engine": "google",
        }
        # Merge in any additional parameters, filtering out None values.
        params.update({k: v for k, v in self._params.items() if v is not None})

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.base_url,
                    params=params,
                    timeout=30,  # SerpApi can be slower
                )
                response.raise_for_status()
                data = response.json()

                # Return empty list if no results found
                if "organic_results" not in data:
                    return []

                serpapi_response = SerpApiResponse(**data)

                results = []
                for result in serpapi_response.organic_results:
                    try:
                        results.append(
                            SearchResult(
                                title=result.title,
                                url=result.link,  # SerpApi uses 'link' instead of 'url'
                                snippet=result.snippet,
                                source=self.name,
                                rank=result.position,  # Use position as rank if available
                                raw=result.model_dump(),  # Include raw result for debugging
                            )
                        )
                    except ValidationError:
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


async def serpapi(
    query: str,
    num_results: int = 5,
    country: str | None = None,
    language: str | None = None,
    safe_search: bool | str | None = True,
    time_frame: str | None = None,
    google_domain: str | None = None,
    api_key: str | None = None,
) -> list[SearchResult]:
    """
    Search using SerpApi Google search.

    Args:
        query: Search query string
        num_results: Number of results to return (1-100)
        country: Country code (e.g., "us", "gb", "fr")
        language: Language code (e.g., "en", "fr", "de")
        safe_search: Whether to enable safe search (True="active", False="off")
        time_frame: Time filter (e.g., "day", "week", "month", "year")
        google_domain: Google domain to use (default: google.com)
        api_key: Optional API key (otherwise use environment variable)

    Returns:
        List of search results
    """
    config = EngineConfig(
        api_key=api_key,
        enabled=True,
    )

    engine = SerpApiSearchEngine(
        config,
        num_results=num_results,
        country=country,
        language=language,
        safe_search=safe_search,
        time_frame=time_frame,
        google_domain=google_domain,
    )

    return await engine.search(query)
