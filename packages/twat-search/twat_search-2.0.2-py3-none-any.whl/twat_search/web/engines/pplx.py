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

    This model is used to validate the response content.
    """

    answer: str = Field(default="")  # Perplexity may sometimes not include all details
    url: str = Field(default="https://perplexity.ai")  # Default URL if none provided
    title: str = Field(default="Perplexity AI Response")  # Default title


class PerplexityResponse(BaseModel):
    """
    Pydantic model for the Perplexity API response structure.
    """

    answers: list[PerplexityResult]  # Expect a list based on the API spec


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

        Args:
            config: Engine configuration
            num_results: Number of results to return (not directly used by Perplexity)
            country: Country code for results (not directly used by Perplexity)
            language: Language code for results (not directly used by Perplexity)
            safe_search: Whether to enable safe search (not directly used by Perplexity)
            time_frame: Time frame for results (not directly used by Perplexity)
            model: Perplexity model to use
            **kwargs: Additional Perplexity-specific parameters
        """
        super().__init__(config)

        # API endpoint
        self.base_url = "https://api.perplexity.ai/chat/completions"

        # Perplexity-specific parameters
        self.model = (
            model
            or kwargs.get("model")
            or self.config.default_params.get("model", "pplx-70b-online")
        )

        # Store common parameters for possible future use
        self.num_results = num_results
        self.country = country
        self.language = language
        self.safe_search = safe_search
        self.time_frame = time_frame

        # Check if API key is available
        if not self.config.api_key:
            raise EngineError(
                self.name,
                f"Perplexity API key is required. Set it via one of these env vars: {', '.join(self.env_api_key_names)}.",
            )

        # API authentication headers
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.config.api_key}",
        }

    async def search(self, query: str) -> list[SearchResult]:
        """
        Perform a search using the Perplexity AI API.

        Args:
            query: The search query string

        Returns:
            A list of SearchResult objects

        Raises:
            EngineError: If the search fails
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

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.base_url, headers=self.headers, json=payload, timeout=10
                )
                response.raise_for_status()

                data = response.json()

                # Create individual PerplexityResult objects first
                answers_list = []
                for choice in data.get("choices", []):
                    answer = choice["message"]["content"]
                    url = "https://perplexity.ai"
                    title = f"Perplexity AI Response: {query[:30]}..."

                    # Create a proper PerplexityResult object
                    answers_list.append(
                        PerplexityResult(answer=answer, url=url, title=title)
                    )

                # Now use the list of PerplexityResult objects
                perplexity_response = PerplexityResponse(answers=answers_list)

                results = []
                for result in perplexity_response.answers:
                    try:
                        # Use HttpUrl constructor directly with the URL string
                        url_obj = HttpUrl(result.url)

                        # Convert to common SearchResult format
                        results.append(
                            SearchResult(
                                title=result.title,
                                url=url_obj,  # Use HttpUrl object
                                snippet=result.answer,  # Use the answer as the snippet
                                source=self.name,
                                raw=data,  # Include raw API response
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

    Args:
        query: Search query string
        num_results: Number of results (not directly used by Perplexity)
        country: Country code (not directly used by Perplexity)
        language: Language code (not directly used by Perplexity)
        safe_search: Safe search setting (not directly used by Perplexity)
        time_frame: Time filter (not directly used by Perplexity)
        model: Perplexity model to use (default: "pplx-70b-online")
        api_key: Optional API key (otherwise use environment variable)

    Returns:
        List of search results
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
