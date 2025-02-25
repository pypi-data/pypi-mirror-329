# this_file: src/twat_search/web/engines/pplx.py

"""
Perplexity AI search engine implementation.

This module implements the Perplexity AI API integration.
"""

import httpx
from typing import ClassVar, Any
from pydantic import BaseModel, Field, ValidationError
from pydantic.networks import HttpUrl

from twat_search.web.config import EngineConfig
from twat_search.web.models import SearchResult
from .base import SearchEngine, register_engine
from twat_search.web.exceptions import EngineError


class PerplexityResult(BaseModel):
    """
    Pydantic model for a single Perplexity result.
    """

    answer: str = Field(default="")  # Perplexity may sometimes not include all details
    url: str = Field(default="https://perplexity.ai")  # Default URL if none provided
    title: str = Field(default="Perplexity AI Response")  # Default title


@register_engine
class PerplexitySearchEngine(SearchEngine):
    """Implementation of the Perplexity AI API."""

    name = "pplx"
    env_api_key_names: ClassVar[list[str]] = [
        "PERPLEXITYAI_API_KEY",
        "PERPLEXITY_API_KEY",
    ]

    def __init__(
        self,
        config: EngineConfig,
        num_results: int = 5,
        country: str | None = None,
        language: str | None = None,
        safe_search: bool | None = True,
        time_frame: str | None = None,
        model: str | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the Perplexity search engine.
        """
        super().__init__(config)
        self.base_url = "https://api.perplexity.ai/chat/completions"
        self.model = (
            model
            or kwargs.get("model")
            or self.config.default_params.get("model", "pplx-70b-online")
        )
        self.num_results = num_results
        self.country = country
        self.language = language
        self.safe_search = safe_search
        self.time_frame = time_frame

        if not self.config.api_key:
            raise EngineError(
                self.name,
                f"Perplexity API key is required. Set it via one of these env vars: {', '.join(self.env_api_key_names)}.",
            )

        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.config.api_key}",
        }

    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a search using the Perplexity AI API.
        """
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "Be precise and concise. I am an expert and do not need explanation",
                },
                {"role": "user", "content": query},
            ],
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.base_url, headers=self.headers, json=payload, timeout=10
                )
                response.raise_for_status()
                data = response.json()
        except httpx.RequestError as exc:
            raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc
        except httpx.HTTPStatusError as exc:
            raise EngineError(
                self.name,
                f"HTTP Status error: {exc.response.status_code} - {exc.response.text}",
            ) from exc

        results = []
        for choice in data.get("choices", []):
            answer = choice.get("message", {}).get("content", "")
            url = "https://perplexity.ai"
            title = f"Perplexity AI Response: {query[:30]}..."
            try:
                # Validate and build the result using the PerplexityResult model
                pr = PerplexityResult(answer=answer, url=url, title=title)
                url_obj = HttpUrl(pr.url)  # Validate URL format
                results.append(
                    SearchResult(
                        title=pr.title,
                        url=url_obj,
                        snippet=pr.answer,
                        source=self.name,
                        raw=data,
                    )
                )
            except ValidationError:
                continue

        return results


async def pplx(
    query: str,
    num_results: int = 5,
    country: str | None = None,
    language: str | None = None,
    safe_search: bool | None = True,
    time_frame: str | None = None,
    model: str | None = None,
    api_key: str | None = None,
) -> list[SearchResult]:
    """
    Search with Perplexity AI.
    """
    config = EngineConfig(
        api_key=api_key,
        enabled=True,
    )

    engine = PerplexitySearchEngine(
        config,
        num_results=num_results,
        country=country,
        language=language,
        safe_search=safe_search,
        time_frame=time_frame,
        model=model,
    )

    return await engine.search(query)
