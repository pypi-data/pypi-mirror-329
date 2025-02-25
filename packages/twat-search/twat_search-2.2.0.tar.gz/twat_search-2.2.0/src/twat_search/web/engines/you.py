import httpx
from typing import Any, ClassVar
from pydantic import BaseModel, ValidationError, HttpUrl, Field

from twat_search.web.config import EngineConfig
from twat_search.web.models import SearchResult
from .base import SearchEngine, register_engine
from twat_search.web.exceptions import EngineError


class YouSearchHit(BaseModel):
    title: str
    url: HttpUrl
    snippet: str = Field(alias="description")


class YouSearchResponse(BaseModel):
    hits: list[YouSearchHit]
    search_id: str | None = Field(None, alias="searchId")


class YouNewsArticle(BaseModel):
    title: str
    url: HttpUrl
    snippet: str = Field(alias="description")
    source: str | None = None
    published_date: str | None = None


class YouNewsResponse(BaseModel):
    articles: list[YouNewsArticle]
    search_id: str | None = Field(None, alias="searchId")


class YouBaseEngine(SearchEngine):
    """Base class for You.com search engines, handling common API interaction logic."""

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
        """Initialize the base engine with common parameters."""
        super().__init__(config)

        if not self.config.api_key:
            raise EngineError(
                self.__class__.name,
                f"You.com API key is required. Set it via one of these env vars: {', '.join(self.env_api_key_names)}",
            )

        self.headers = {
            "X-API-Key": self.config.api_key,
            "Accept": "application/json",
        }

        self.num_results = num_results or self.config.default_params.get(
            self.__class__.num_results_param, 5
        )
        self.country_code = country or self.config.default_params.get(
            "country_code", None
        )
        self.safe_search = safe_search or self.config.default_params.get(
            "safe_search", True
        )

    async def _make_api_call(self, query: str) -> dict:
        """Handle the common API call logic."""
        params: dict[str, Any] = {
            "q": query,
            self.__class__.num_results_param: self.num_results,
        }

        if self.country_code:
            params["country_code"] = self.country_code
        if self.safe_search is not None:
            params["safe_search"] = str(self.safe_search).lower()

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.__class__.base_url,
                    headers=self.headers,
                    params=params,
                    timeout=10,
                )
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as exc:
                raise EngineError(
                    self.__class__.name, f"HTTP Request failed: {exc}"
                ) from exc
            except httpx.HTTPStatusError as exc:
                raise EngineError(
                    self.__class__.name,
                    f"HTTP Status error: {exc.response.status_code} - {exc.response.text}",
                ) from exc


@register_engine
class YouSearchEngine(YouBaseEngine):
    """Implementation of the You.com Web Search API."""

    name = "you"
    base_url = "https://api.you.com/api/search"
    num_results_param = "num_web_results"

    async def search(self, query: str) -> list[SearchResult]:
        """Perform a web search using the You.com Search API."""
        data = await self._make_api_call(query)
        try:
            you_response = YouSearchResponse(**data)
            results = []
            for hit in you_response.hits:
                try:
                    results.append(
                        SearchResult(
                            title=hit.title,
                            url=hit.url,
                            snippet=hit.snippet,
                            source=self.__class__.name,
                            raw=hit.model_dump(by_alias=True),
                        )
                    )
                except ValidationError:
                    continue
            return results
        except ValidationError as exc:
            raise EngineError(
                self.__class__.name, f"Response parsing error: {exc}"
            ) from exc


@register_engine
class YouNewsSearchEngine(YouBaseEngine):
    """Implementation of the You.com News Search API."""

    name = "you-news"
    base_url = "https://api.you.com/api/news"
    num_results_param = "num_news_results"

    async def search(self, query: str) -> list[SearchResult]:
        """Perform a news search using the You.com News API."""
        data = await self._make_api_call(query)
        try:
            you_response = YouNewsResponse(**data)
            results = []
            for article in you_response.articles:
                try:
                    snippet = article.snippet
                    if article.source and article.published_date:
                        snippet = (
                            f"{snippet} - {article.source} ({article.published_date})"
                        )
                    elif article.source:
                        snippet = f"{snippet} - {article.source}"
                    results.append(
                        SearchResult(
                            title=article.title,
                            url=article.url,
                            snippet=snippet,
                            source=self.__class__.name,
                            raw=article.model_dump(by_alias=True),
                        )
                    )
                except ValidationError:
                    continue
            return results
        except ValidationError as exc:
            raise EngineError(
                self.__class__.name, f"Response parsing error: {exc}"
            ) from exc


# Backward compatibility alias
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
    """Search You.com web search."""
    config = EngineConfig(api_key=api_key, enabled=True)
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
    """Search You.com news."""
    config = EngineConfig(api_key=api_key, enabled=True)
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
