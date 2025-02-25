# this_file: src/twat_search/web/engines/critique.py

"""
Critique Labs search engine implementation.

This module implements the Critique Labs AI API integration.
"""

import httpx
import base64
from typing import Any, ClassVar
from pydantic import BaseModel, ValidationError, HttpUrl, Field

from twat_search.web.config import EngineConfig
from twat_search.web.models import SearchResult
from .base import SearchEngine, register_engine
from twat_search.web.exceptions import EngineError


class CritiqueResult(BaseModel):
    """
    Pydantic model for a single Critique Labs search result.

    This model is used to validate the response content.
    """

    url: str = Field(default="")  # URL of the result source
    title: str = Field(default="")  # Title of the result
    summary: str = Field(default="")  # Summary or snippet from the result
    source: str = Field(default="")  # Source of the result
    relevance_score: float | None = None  # Relevance score if available


class CritiqueResponse(BaseModel):
    """
    Pydantic model for the Critique Labs API response structure.
    """

    results: list[CritiqueResult] = Field(default_factory=list)  # List of results
    response: str | None = None  # Main response text from the API
    structured_output: dict[str, Any] | None = None  # Any structured output returned


@register_engine
class CritiqueSearchEngine(SearchEngine):
    """Implementation of the Critique Labs AI Search API."""

    name = "critique"
    env_api_key_names: ClassVar[list[str]] = [
        "CRITIQUE_LABS_API_KEY",
        "CRITIQUE_API_KEY",
    ]

    def __init__(
        self,
        config: EngineConfig,
        num_results: int = 5,
        country: str | None = None,
        language: str | None = None,
        safe_search: bool | None = True,
        time_frame: str | None = None,
        image_url: str | None = None,
        image_base64: str | None = None,
        source_whitelist: list[str] | None = None,
        source_blacklist: list[str] | None = None,
        output_format: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the Critique Labs search engine.

        Args:
            config: Engine configuration
            num_results: Number of results to return (saved for future compatibility)
            country: Country code for results (saved for future compatibility)
            language: Language code for results (saved for future compatibility)
            safe_search: Whether to enable safe search (saved for future compatibility)
            time_frame: Time frame for results (saved for future compatibility)
            image_url: URL of an image to include in the search
            image_base64: Base64-encoded image data to include in the search
            source_whitelist: List of domains to include in search results
            source_blacklist: List of domains to exclude from search results
            output_format: Structured output format specification
            **kwargs: Additional Critique-specific parameters
        """
        super().__init__(config)

        # API endpoint
        self.base_url = "https://api.critique-labs.ai/v1/search"

        # Store common parameters for possible future API updates
        self.num_results = num_results
        self.country = country
        self.language = language
        self.safe_search = safe_search
        self.time_frame = time_frame

        # Critique-specific parameters
        self.image_url = image_url or kwargs.get("image_url")
        self.image_base64 = image_base64 or kwargs.get("image_base64")
        self.source_whitelist = source_whitelist or kwargs.get("source_whitelist")
        self.source_blacklist = source_blacklist or kwargs.get("source_blacklist")
        self.output_format = output_format or kwargs.get("output_format")

        # Check if API key is available
        if not self.config.api_key:
            raise EngineError(
                self.name,
                f"Critique Labs API key is required. Set it via one of these env vars: {', '.join(self.env_api_key_names)}",
            )

        # API authentication headers
        self.headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.config.api_key,
        }

    async def _convert_image_url_to_base64(self, image_url: str) -> str:
        """
        Convert an image URL to base64 encoding.

        Args:
            image_url: URL of the image to convert

        Returns:
            Base64-encoded image data as a string

        Raises:
            EngineError: If the image cannot be fetched or converted
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(image_url, timeout=30)
                response.raise_for_status()

                # Convert image content to base64
                base64_encoded_image = base64.b64encode(response.content).decode(
                    "utf-8"
                )
                return f"data:image/jpeg;base64,{base64_encoded_image}"
        except httpx.RequestError as e:
            raise EngineError(self.name, f"Failed to fetch image from URL: {e}")
        except Exception as e:
            raise EngineError(self.name, f"Error processing image: {e}")

    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a search using the Critique Labs API.

        Args:
            query: The search query string (prompt)

        Returns:
            A list of SearchResult objects

        Raises:
            EngineError: If the search fails
        """
        # Prepare the request payload
        payload: dict[str, Any] = {
            "prompt": query,
        }

        # Handle image input (prioritize base64 over URL)
        if self.image_base64:
            payload["image"] = self.image_base64
        elif self.image_url:
            # Convert URL to base64 if URL is provided
            payload["image"] = await self._convert_image_url_to_base64(self.image_url)

        # Add optional parameters if they have values
        if self.source_whitelist:
            payload["source_whitelist"] = self.source_whitelist
        if self.source_blacklist:
            payload["source_blacklist"] = self.source_blacklist
        if self.output_format:
            payload["output_format"] = self.output_format

        # Make the API request
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.base_url,
                    headers=self.headers,
                    json=payload,
                    timeout=60,  # Longer timeout for image processing
                )
                response.raise_for_status()
                data = response.json()

                # Extract and process results
                results = []

                # Handle possible response formats
                critique_data = CritiqueResponse(
                    results=data.get("results", []),
                    response=data.get("response"),
                    structured_output=data.get("structured_output"),
                )

                # If API doesn't return results but has a response, create a single result
                if not critique_data.results and critique_data.response:
                    results.append(
                        SearchResult(
                            title="Critique Labs AI Response",
                            url=HttpUrl("https://critique-labs.ai"),
                            snippet=critique_data.response,
                            source=self.name,
                            raw=data,
                        )
                    )

                # Process any results returned by the API
                for idx, item in enumerate(critique_data.results, 1):
                    try:
                        # Convert string URL to HttpUrl
                        url_obj = (
                            HttpUrl(item.url)
                            if item.url
                            else HttpUrl("https://critique-labs.ai")
                        )

                        # Create SearchResult object
                        results.append(
                            SearchResult(
                                title=item.title or f"Result {idx}",
                                url=url_obj,
                                snippet=item.summary,
                                source=self.name,
                                rank=idx,
                                raw=item.dict(),
                            )
                        )
                    except ValidationError:
                        # Skip invalid results
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
            except Exception as exc:
                raise EngineError(self.name, f"Search failed: {exc}") from exc


async def critique(
    query: str,
    num_results: int = 5,
    country: str | None = None,
    language: str | None = None,
    safe_search: bool | None = True,
    time_frame: str | None = None,
    image_url: str | None = None,
    image_base64: str | None = None,
    source_whitelist: list[str] | None = None,
    source_blacklist: list[str] | None = None,
    output_format: dict[str, Any] | None = None,
    api_key: str | None = None,
) -> list[SearchResult]:
    """
    Search using Critique Labs AI.

    Args:
        query: Search query string (prompt)
        num_results: Number of results (saved for future compatibility)
        country: Country code (saved for future compatibility)
        language: Language code (saved for future compatibility)
        safe_search: Safe search setting (saved for future compatibility)
        time_frame: Time filter (saved for future compatibility)
        image_url: URL of an image to include in the search
        image_base64: Base64-encoded image data to include in the search
        source_whitelist: List of domains to include in search results
        source_blacklist: List of domains to exclude from search results
        output_format: Structured output format specification
        api_key: Optional API key (otherwise use environment variable)

    Returns:
        List of search results
    """
    config = EngineConfig(
        api_key=api_key,
        enabled=True,
    )

    engine = CritiqueSearchEngine(
        config,
        num_results=num_results,
        country=country,
        language=language,
        safe_search=safe_search,
        time_frame=time_frame,
        image_url=image_url,
        image_base64=image_base64,
        source_whitelist=source_whitelist,
        source_blacklist=source_blacklist,
        output_format=output_format,
    )

    return await engine.search(query)
