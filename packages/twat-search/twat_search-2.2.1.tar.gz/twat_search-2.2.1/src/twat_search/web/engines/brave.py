import httpx
from typing import Any, ClassVar
from pydantic import BaseModel, ValidationError, HttpUrl

from twat_search.web.config import EngineConfig
from twat_search.web.models import SearchResult
from .base import SearchEngine, register_engine
from twat_search.web.exceptions import EngineError


# Pydantic models for individual results
class BraveResult(BaseModel):
    title: str
    url: HttpUrl
    description: str


class BraveNewsResult(BaseModel):
    title: str
    url: HttpUrl
    description: str
    published_time: str | None = None
    publisher: str | None = None


# Base class that encapsulates common functionality for both search and news engines.
class BaseBraveEngine(SearchEngine):
    env_api_key_names: ClassVar[list[str]] = ["BRAVE_API_KEY"]
    base_url: str  # Must be defined by subclass.
    response_key: str  # "web" for normal search, "news" for news search.
    result_model: type[BaseModel]  # Either BraveResult or BraveNewsResult.

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
        super().__init__(config)
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
        if isinstance(safe, bool):
            safe = "strict" if safe else "off"
        self.safe_search = safe or self.config.default_params.get("safe_search", None)
        freshness = kwargs.get("freshness", time_frame)
        self.freshness = freshness or self.config.default_params.get("freshness", None)

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
        params: dict[str, Any] = {"q": query, "count": self.count}
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
                response.raise_for_status()
                data = response.json()
                results = []
                section = data.get(self.response_key, {})
                if section.get("results"):
                    for result in section["results"]:
                        try:
                            parsed = self.result_model(**result)
                            results.append(self.convert_result(parsed, result))
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

    def convert_result(self, parsed: BaseModel, raw: dict[str, Any]) -> SearchResult:
        snippet = parsed.description
        # For news results, append publisher and published_time information if available.
        if self.response_key == "news":
            publisher = getattr(parsed, "publisher", None)
            published_time = getattr(parsed, "published_time", None)
            if publisher and published_time:
                snippet = f"{snippet} - {publisher} ({published_time})"
            elif publisher:
                snippet = f"{snippet} - {publisher}"
        return SearchResult(
            title=parsed.title,
            url=parsed.url,
            snippet=snippet,
            source=self.name,
            raw=raw,
        )


@register_engine
class BraveSearchEngine(BaseBraveEngine):
    name = "brave"
    base_url = "https://api.search.brave.com/res/v1/web/search"
    response_key = "web"
    result_model = BraveResult


@register_engine
class BraveNewsSearchEngine(BaseBraveEngine):
    name = "brave-news"
    base_url = "https://api.search.brave.com/res/v1/news/search"
    response_key = "news"
    result_model = BraveNewsResult


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
    config = EngineConfig(api_key=api_key, enabled=True)
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
    config = EngineConfig(api_key=api_key, enabled=True)
    engine = BraveNewsSearchEngine(
        config,
        num_results=num_results,
        country=country,
        language=language,
        safe_search=safe_search,
        time_frame=time_frame,
    )
    return await engine.search(query)
