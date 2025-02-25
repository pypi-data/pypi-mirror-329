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

    results: list[CritiqueResult] = Field(default_factory=list)
    response: str | None = None
    structured_output: dict[str, Any] | None = None


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
        """
        super().__init__(config)

        self.base_url = "https://api.critique-labs.ai/v1/search"
        self.num_results = num_results
        self.country = country
        self.language = language
        self.safe_search = safe_search
        self.time_frame = time_frame

        self.image_url = image_url or kwargs.get("image_url")
        self.image_base64 = image_base64 or kwargs.get("image_base64")
        self.source_whitelist = source_whitelist or kwargs.get("source_whitelist")
        self.source_blacklist = source_blacklist or kwargs.get("source_blacklist")
        self.output_format = output_format or kwargs.get("output_format")

        if not self.config.api_key:
            raise EngineError(
                self.name,
                f"Critique Labs API key is required. Set it via one of these env vars: {', '.join(self.env_api_key_names)}",
            )

        self.headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.config.api_key,
        }

    async def _convert_image_url_to_base64(self, image_url: str) -> str:
        """
        Convert an image URL to base64 encoding.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(image_url, timeout=30)
                response.raise_for_status()
                encoded = base64.b64encode(response.content).decode("utf-8")
                return f"data:image/jpeg;base64,{encoded}"
        except httpx.RequestError as e:
            raise EngineError(self.name, f"Failed to fetch image from URL: {e}")
        except Exception as e:
            raise EngineError(self.name, f"Error processing image: {e}")

    async def _build_payload(self, query: str) -> dict[str, Any]:
        """
        Build the API payload from the search query and optional parameters.
        """
        payload: dict[str, Any] = {"prompt": query}

        # Handle image input (prioritize base64 over URL)
        if self.image_base64:
            payload["image"] = self.image_base64
        elif self.image_url:
            payload["image"] = await self._convert_image_url_to_base64(self.image_url)

        # Add optional parameters if provided
        if self.source_whitelist:
            payload["source_whitelist"] = self.source_whitelist
        if self.source_blacklist:
            payload["source_blacklist"] = self.source_blacklist
        if self.output_format:
            payload["output_format"] = self.output_format

        return payload

    def _build_result(self, item: CritiqueResult, rank: int) -> SearchResult:
        """
        Convert a single CritiqueResult into a SearchResult.
        """
        try:
            url_obj = (
                HttpUrl(item.url) if item.url else HttpUrl("https://critique-labs.ai")
            )
        except ValidationError:
            url_obj = HttpUrl("https://critique-labs.ai")

        return SearchResult(
            title=item.title or f"Result {rank}",
            url=url_obj,
            snippet=item.summary,
            source=self.name,
            rank=rank,
            raw=item.dict(),
        )

    def _parse_results(self, data: dict[str, Any]) -> list[SearchResult]:
        """
        Parse the API response data into a list of SearchResult objects.
        """
        critique_data = CritiqueResponse(
            results=data.get("results", []),
            response=data.get("response"),
            structured_output=data.get("structured_output"),
        )
        results: list[SearchResult] = []

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

        for idx, item in enumerate(critique_data.results, 1):
            try:
                results.append(self._build_result(item, idx))
            except ValidationError:
                continue

        return results

    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a search using the Critique Labs API.
        """
        payload = await self._build_payload(query)

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
                return self._parse_results(data)
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
    """
    config = EngineConfig(api_key=api_key, enabled=True)
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
