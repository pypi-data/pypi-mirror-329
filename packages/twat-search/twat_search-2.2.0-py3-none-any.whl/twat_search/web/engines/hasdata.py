# this_file: src/twat_search/web/engines/hasdata.py

"""
HasData search engine implementation.

This module implements search engines that use the HasData APIs:
- hasdata-google: Full Google SERP API
- hasdata-google-light: Light version of Google SERP API
"""

import httpx
import json
from typing import Any, ClassVar
from pydantic import BaseModel, ValidationError, HttpUrl

from twat_search.web.config import EngineConfig
from twat_search.web.models import SearchResult
from .base import SearchEngine, register_engine
from twat_search.web.exceptions import EngineError


# Pydantic models for HasData Google search results
class HasDataGoogleResult(BaseModel):
    """Model for a single HasData Google search result."""

    title: str
    url: HttpUrl
    snippet: str

    @classmethod
    def from_api_result(cls, result: dict[str, Any]) -> "HasDataGoogleResult":
        """Convert API result to a model instance."""
        return cls(
            title=result.get("title", ""),
            url=result.get("link", ""),
            snippet=result.get("snippet", ""),
        )


# Base class for HasData engines
class HasDataBaseEngine(SearchEngine):
    """Base class for HasData search engines."""

    env_api_key_names: ClassVar[list[str]] = ["HASDATA_API_KEY"]
    base_url: str  # Must be defined by subclass
    supports_device_type: ClassVar[bool] = (
        False  # Default value, will be overridden by subclasses
    )

    def __init__(
        self,
        config: EngineConfig,
        num_results: int = 5,
        location: str | None = None,
        device_type: str | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the HasData search engine.

        Args:
            config: Engine configuration with API key
            num_results: Number of results to return
            location: Search location (e.g., "Austin,Texas,United States")
            device_type: Device type for search (e.g., "desktop", "mobile")
            **kwargs: Additional parameters
        """
        super().__init__(config)
        self.num_results = num_results
        self.location = (
            location
            or kwargs.get("location")
            or self.config.default_params.get("location")
        )
        self.device_type = (
            device_type
            or kwargs.get("device_type")
            or self.config.default_params.get("device_type", "desktop")
        )

        if not self.config.api_key:
            raise EngineError(
                self.name,
                f"HasData API key is required. Set it via one of these env vars: {', '.join(self.env_api_key_names)}",
            )

        self.headers = {
            "x-api-key": self.config.api_key,
        }

    async def search(self, query: str) -> list[SearchResult]:
        """
        Search using HasData API.

        Args:
            query: The search query

        Returns:
            List of search results

        Raises:
            EngineError: If the search request fails
        """
        params: dict[str, Any] = {"q": query}

        if self.location:
            params["location"] = self.location

        if self.device_type and self.supports_device_type:
            params["deviceType"] = self.device_type

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.base_url,
                    headers=self.headers,
                    params=params,
                    timeout=10,
                )
                response.raise_for_status()
                data = response.json()

                # Parse the organic results from the response
                results = []
                organic_results = data.get("organicResults", [])

                for i, result in enumerate(organic_results):
                    if i >= self.num_results:
                        break

                    try:
                        parsed = HasDataGoogleResult.from_api_result(result)
                        results.append(
                            SearchResult(
                                title=parsed.title,
                                url=parsed.url,
                                snippet=parsed.snippet,
                                source=self.name,
                                rank=i + 1,
                                raw=result,
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
            except json.JSONDecodeError as exc:
                raise EngineError(self.name, f"Invalid JSON response: {exc}") from exc


@register_engine
class HasDataGoogleEngine(HasDataBaseEngine):
    """HasData Google SERP search engine."""

    name = "hasdata-google"
    base_url = "https://api.hasdata.com/scrape/google/serp"
    supports_device_type: ClassVar[bool] = True


@register_engine
class HasDataGoogleLightEngine(HasDataBaseEngine):
    """HasData Google SERP Light search engine."""

    name = "hasdata-google-light"
    base_url = "https://api.hasdata.com/scrape/google-light/serp"
    supports_device_type: ClassVar[bool] = False


async def hasdata_google(
    query: str,
    num_results: int = 5,
    location: str | None = None,
    device_type: str = "desktop",
    api_key: str | None = None,
) -> list[SearchResult]:
    """
    Search using HasData Google SERP API.

    Args:
        query: Search query string
        num_results: Number of results to return
        location: Location for search (e.g., "Austin,Texas,United States")
        device_type: Device type (desktop or mobile)
        api_key: Optional API key (otherwise use environment variable)

    Returns:
        List of search results
    """
    config = EngineConfig(api_key=api_key, enabled=True)
    engine = HasDataGoogleEngine(
        config,
        num_results=num_results,
        location=location,
        device_type=device_type,
    )
    return await engine.search(query)


async def hasdata_google_light(
    query: str,
    num_results: int = 5,
    location: str | None = None,
    api_key: str | None = None,
) -> list[SearchResult]:
    """
    Search using HasData Google SERP Light API.

    Args:
        query: Search query string
        num_results: Number of results to return
        location: Location for search (e.g., "Austin,Texas,United States")
        api_key: Optional API key (otherwise use environment variable)

    Returns:
        List of search results
    """
    config = EngineConfig(api_key=api_key, enabled=True)
    engine = HasDataGoogleLightEngine(
        config,
        num_results=num_results,
        location=location,
    )
    return await engine.search(query)
