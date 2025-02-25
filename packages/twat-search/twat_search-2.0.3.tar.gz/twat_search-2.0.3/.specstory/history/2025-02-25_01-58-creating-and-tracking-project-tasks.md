## SpecStory

## Creating and Tracking Project Tasks (25/02/2025, 01:58:58)

_**User**_

Read @TODO.md and in @PROGRESS.md make a simple `- [ ]` items list. Then start implementing, and mark the @PROGRESS.md with `- [x]` items

---

_**Assistant**_

<think>I need to analyze the TODO.md document and create a simple checklist in PROGRESS.md of the tasks that need to be done. Then, I should start implementing the code and mark completed items as I go.

First, let's examine the TODO.md file to understand the requirements.

The TODO.md file contains a detailed specification for a Python package called `twat-search` that provides a unified web search API across multiple search engines. It includes the following:

1. Core goals of the package
2. Module structure
3. Detailed module specifications for files in the structure
4. Example usage

The module structure is:
```
src/twat_search/web/
├── __init__.py     # Package initialization
├── api.py          # Main search API (the user-facing part)
├── config.py       # Configuration (API keys, default parameters)
├── exceptions.py   # Custom exception classes
├── models.py       # Pydantic models for inputs and outputs
├── engines/        # Subpackage for search engine implementations
│   ├── __init__.py
│   ├── base.py     # Abstract base class for search engines
│   ├── brave.py    # Brave Search implementation
│   ├── google.py   # Google Search (SerpAPI) implementation
│   ├── tavily.py   # Tavily Search implementation
│   ├── perplexity.py # Perplexity AI implementation
│   ├── youcom.py   # You.com implementation
│   └── ...         # Other search engines (easily added)
└── utils.py       # Utility functions (e.g., rate limiting)
```

Now, let's look at the PROGRESS.md file to see what's already there. It's mostly empty, so I'll need to create a checklist from scratch.

Let me create a tasks list based on the module structure and requirements:

1. Initialize project structure
2. Create package initialization files
3. Create models.py with Pydantic models for search results
4. Create exceptions.py with custom exception classes
5. Create config.py with configuration classes
6. Create utils.py with utility functions
7. Create engines/base.py with abstract base class and factory functions
8. Create engines/__init__.py to expose engine register functions
9. Implement specific search engines:
   - Brave search engine
   - Google search engine
   - Tavily search engine
   - Perplexity search engine
   - You.com search engine
10. Create api.py with the main search function
11. Add example usage

Now I'll update the PROGRESS.md file with this list using the `- [ ]` format. Then I'll start implementing the code and mark items as completed.

Let's begin with updating PROGRESS.md:</think>I'll read the TODO.md file, create a checklist in PROGRESS.md, and start implementing the code.

---

_****_

```diff
  ---
- this_file: LOG.md
+ this_file: PROGRESS.md
  ---
+ 
+ # Implementation Progress
+ 
+ - [ ] Initialize project structure
+ - [ ] Create package initialization files
+ - [ ] Create models.py with Pydantic models for search results
+ - [ ] Create exceptions.py with custom exception classes
+ - [ ] Create config.py with configuration classes
+ - [ ] Create utils.py with utility functions
+ - [ ] Create engines/base.py with abstract base class and factory functions
+ - [ ] Create engines/__init__.py to expose engine register functions
+ - [ ] Implement search engines:
+   - [ ] Brave search engine
+   - [ ] Google search engine
+   - [ ] Tavily search engine
+   - [ ] Perplexity search engine
+   - [ ] You.com search engine
+ - [ ] Create api.py with the main search function
+ - [ ] Add example usage
  
  
```

---

_****_



Now I'll start implementing the package. Let's begin by creating the project structure.

---

_****_

```bash
mkdir -p src/twat_search/web/engines
```

```
(twat_search) adam@Hamlet twat_search % mkdir -p src/twat_search/w
mkdir -p src/twat_search/web/engines
%                                                                 
(twat_search) adam@Hamlet twat_search %
```

---

_****_



Let's update PROGRESS.md to mark the first item as complete.

---

_****_

```diff
  # Implementation Progress
  
- - [ ] Initialize project structure
+ - [x] Initialize project structure
  - [ ] Create package initialization files
  - [ ] Create models.py with Pydantic models for search results
```

---

_****_





Now, let's create the package initialization files.

---

_****_

```diff
- 
+ #!/usr/bin/env -S uv run -s
+ # /// script
+ # dependencies = ["httpx", "pydantic"]
+ # ///
+ # this_file: src/twat_search/web/__init__.py
+ 
+ """
+ Unified web search API across multiple search engines.
+ 
+ This package provides a single interface for searching across
+ multiple search engines, handling the differences between APIs
+ and providing a consistent result format.
+ """
+ 
+ from .api import search
+ from .models import SearchResult
+ from .config import Config, EngineConfig
+ 
+ __all__ = ["search", "SearchResult", "Config", "EngineConfig"] 
```

---

_****_





Now let's create the engines package initialization file.

---

_****_

```diff
- 
+ # this_file: src/twat_search/web/engines/__init__.py
+ 
+ """
+ Search engine implementations for the web search API.
+ 
+ This package contains implementations for various search engines,
+ each one providing a standard interface for searching and returning results.
+ """
+ 
+ from .base import SearchEngine, register_engine, get_engine
+ 
+ # Import and register all engines
+ from .brave import BraveSearchEngine
+ from .google import GoogleSearchEngine
+ from .tavily import TavilySearchEngine
+ from .perplexity import PerplexitySearchEngine
+ from .youcom import YoucomSearchEngine
+ 
+ __all__ = [
+     "SearchEngine",
+     "register_engine",
+     "get_engine",
+     "BraveSearchEngine",
+     "GoogleSearchEngine",
+     "TavilySearchEngine",
+     "PerplexitySearchEngine",
+     "YoucomSearchEngine",
+ ] 
```

---

_****_







Let's create the parent package initialization file.

---

_****_

```diff
- """twat search plugin"""
+ """
+ TwAT Search package - Tools for web search and information retrieval.
+ 
+ This package provides utilities for searching the web and retrieving information
+ from various sources.
+ """
+ 
+ __version__ = "0.1.0"
  
  from importlib import metadata
- 
- from twat_search.__version__ import version as __version__
  
  __all__ = ["__version__"]
```

---

_****_









Let's fix the parent package initialization file.

---

_****_

```diff
  
  __version__ = "0.1.0"
- 
- from importlib import metadata
  
  __all__ = ["__version__"]
```

---

_****_





Let's update PROGRESS.md to mark the initialization files as complete.

---

_****_

```diff
  
  - [x] Initialize project structure
- - [ ] Create package initialization files
+ - [x] Create package initialization files
  - [ ] Create models.py with Pydantic models for search results
  - [ ] Create exceptions.py with custom exception classes
```

---

_****_







Now, let's create the models.py file for Pydantic models.

---

_****_

```diff
- 
+ # this_file: src/twat_search/web/models.py
+ 
+ """
+ Pydantic models for the web search API.
+ 
+ This module defines the data models used for inputs and outputs
+ in the web search API.
+ """
+ 
+ from typing import Dict, Any, Optional
+ 
+ from pydantic import BaseModel, HttpUrl
+ 
+ 
+ class SearchResult(BaseModel):
+     """
+     Represents a single search result from any search engine.
+     
+     Attributes:
+         title: The title of the search result.
+         url: The URL of the search result.
+         snippet: A short excerpt or description of the search result.
+         source: The name of the search engine that produced this result.
+         rank: Optional ranking position (for future ranking functionality).
+         raw: The raw, unparsed response from the search engine (for debugging).
+     """
+     title: str
+     url: HttpUrl  # Use Pydantic's HttpUrl for URL validation
+     snippet: str
+     source: str
+     rank: Optional[int] = None  # For future ranking functionality
+     raw: Optional[Dict[str, Any]] = None  # Store the raw API response 
```

---

_****_








Now, let's create the exceptions.py file with custom exception classes.

---

_****_

```diff
- 
+ # this_file: src/twat_search/web/exceptions.py
+ 
+ """
+ Custom exceptions for the web search API.
+ 
+ This module defines the custom exceptions used by the web search API
+ for handling errors in a consistent way.
+ """
+ 
+ 
+ class SearchError(Exception):
+     """Base exception for search-related errors."""
+     
+     def __init__(self, message: str) -> None:
+         """
+         Initialize the exception with a message.
+         
+         Args:
+             message: Error message explaining what went wrong
+         """
+         super().__init__(message)
+ 
+ 
+ class EngineError(SearchError):
+     """Error for an issue with a specific search engine."""
+ 
+     def __init__(self, engine_name: str, message: str) -> None:
+         """
+         Initialize the exception with an engine name and message.
+         
+         Args:
+             engine_name: Name of the search engine that encountered the error
+             message: Error message explaining what went wrong
+         """
+         super().__init__(f"Engine '{engine_name}': {message}")
+         self.engine_name = engine_name 
```

---

_****_










Let's update the PROGRESS.md file to mark these tasks as complete.

---

_****_

```diff
  - [x] Initialize project structure
  - [x] Create package initialization files
- - [ ] Create models.py with Pydantic models for search results
- - [ ] Create exceptions.py with custom exception classes
+ - [x] Create models.py with Pydantic models for search results
+ - [x] Create exceptions.py with custom exception classes
  - [ ] Create config.py with configuration classes
  - [ ] Create utils.py with utility functions
```

---

_****_








Now, let's create the config.py file with configuration classes.

---

_****_

```diff
- 
+ # this_file: src/twat_search/web/config.py
+ 
+ """
+ Configuration classes for the web search API.
+ 
+ This module defines the configuration classes used to configure
+ the web search API, including API keys and default parameters for
+ each search engine.
+ """
+ 
+ from typing import Dict, Any, Optional
+ 
+ from pydantic import BaseModel, BaseSettings, Field
+ 
+ 
+ class EngineConfig(BaseModel):
+     """
+     Configuration for a single search engine.
+     
+     Attributes:
+         api_key: API key for the search engine.
+         enabled: Whether the engine is enabled for searches.
+         default_params: Default parameters to use for this engine.
+     """
+     api_key: Optional[str] = None  # Allow engines without API keys
+     enabled: bool = True
+     default_params: Dict[str, Any] = Field(default_factory=dict)
+ 
+ 
+ class Config(BaseSettings):
+     """
+     Overall configuration for the web search API.
+     
+     This class loads configuration from environment variables and .env files.
+     
+     Attributes:
+         engines: Dictionary mapping engine names to their configurations.
+     """
+     engines: Dict[str, EngineConfig] = Field(default_factory=dict)
+ 
+     class Config:
+         """Pydantic configuration for settings."""
+         env_prefix = ""
+         env_file = ".env"
+         env_file_encoding = "utf-8"
+ 
+         @classmethod
+         def customise_sources(
+             cls,
+             init_settings,
+             env_settings,
+             file_secret_settings,
+         ):
+             """Customize the order of settings sources."""
+             return (
+                 init_settings,
+                 env_settings,
+                 file_secret_settings,
+             ) 
```

---

_****_







Now, let's create the utils.py file with the RateLimiter utility.

---

_****_

```diff
- 
+ # this_file: src/twat_search/web/utils.py
+ 
+ """
+ Utility functions for the web search API.
+ 
+ This module provides utility functions and classes used by the web search API.
+ """
+ 
+ import time
+ import logging
+ from typing import List
+ 
+ # Set up logging
+ logger = logging.getLogger(__name__)
+ 
+ 
+ class RateLimiter:
+     """
+     Rate limiter to manage API request frequency.
+     
+     This class helps prevent hitting rate limits by spacing out API requests.
+     """
+ 
+     def __init__(self, calls_per_second: int = 10):
+         """
+         Initialize the rate limiter.
+         
+         Args:
+             calls_per_second: Maximum number of calls allowed per second
+         """
+         self.calls_per_second = calls_per_second
+         self.call_timestamps: List[float] = []
+ 
+     def wait_if_needed(self) -> None:
+         """
+         Wait if necessary to respect the rate limit.
+         
+         This method should be called before making an API request.
+         """
+         now = time.time()
+ 
+         # Remove timestamps older than 1 second
+         self.call_timestamps = [t for t in self.call_timestamps if now - t < 1]
+ 
+         # If we've made too many calls in the last second, wait
+         if len(self.call_timestamps) >= self.calls_per_second:
+             sleep_time = 1 - (now - self.call_timestamps[0])
+             if sleep_time > 0:
+                 if sleep_time > 0.1:  # Only log if sleep time is significant
+                     logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f}s")
+                 time.sleep(sleep_time)
+ 
+         # Record this API call
+         self.call_timestamps.append(time.time()) 
```

---

_****_











Let's update PROGRESS.md to mark these tasks as complete.

---

_****_

```diff
  - [x] Create models.py with Pydantic models for search results
  - [x] Create exceptions.py with custom exception classes
- - [ ] Create config.py with configuration classes
- - [ ] Create utils.py with utility functions
+ - [x] Create config.py with configuration classes
+ - [x] Create utils.py with utility functions
  - [ ] Create engines/base.py with abstract base class and factory functions
  - [ ] Create engines/__init__.py to expose engine register functions
```

---

_****_












Now, let's create the engines/base.py file with the abstract base class and factory functions.

---

_****_

```diff
- 
+ # this_file: src/twat_search/web/engines/base.py
+ 
+ """
+ Base class and factory functions for search engines.
+ 
+ This module defines the abstract base class that all search engines must
+ implement, as well as functions to register and instantiate engines.
+ """
+ 
+ import abc
+ from typing import Dict, List, Type, Any, ClassVar
+ 
+ from ..config import EngineConfig
+ from ..models import SearchResult
+ from ..exceptions import EngineError, SearchError
+ 
+ 
+ class SearchEngine(abc.ABC):
+     """
+     Abstract base class for all search engines.
+     
+     All search engine implementations must subclass this and implement
+     the search method.
+     """
+     
+     name: ClassVar[str]  # Class attribute that must be defined by subclasses
+ 
+     def __init__(self, config: EngineConfig, **kwargs: Any) -> None:
+         """
+         Initialize the search engine with its configuration.
+         
+         Args:
+             config: Configuration for this search engine
+             **kwargs: Additional engine-specific parameters
+         
+         Raises:
+             SearchError: If the engine is disabled
+         """
+         self.config = config
+         self.kwargs = kwargs  # Store for later use
+         
+         if not self.config.enabled:
+             raise SearchError(f"Engine '{self.name}' is disabled.")
+ 
+     @abc.abstractmethod
+     async def search(self, query: str) -> List[SearchResult]:
+         """
+         Perform a search and return a list of SearchResult objects.
+         
+         Args:
+             query: The search query string
+             
+         Returns:
+             A list of SearchResult objects
+             
+         Raises:
+             EngineError: If the search fails
+         """
+         ...
+ 
+ 
+ # Registry of available search engines
+ _engine_registry: Dict[str, Type[SearchEngine]] = {}
+ 
+ 
+ def register_engine(engine_class: Type[SearchEngine]) -> Type[SearchEngine]:
+     """
+     Register a search engine class.
+     
+     This is typically used as a decorator on search engine classes.
+     
+     Args:
+         engine_class: The search engine class to register
+         
+     Returns:
+         The same search engine class (for decorator use)
+     """
+     _engine_registry[engine_class.name] = engine_class
+     return engine_class
+ 
+ 
+ def get_engine(engine_name: str, config: EngineConfig, **kwargs: Any) -> SearchEngine:
+     """
+     Factory function to get an instance of a search engine.
+     
+     Args:
+         engine_name: The name of the engine (e.g., "brave", "google")
+         config: The EngineConfig object for this engine
+         **kwargs: Additional parameters to pass to the engine constructor
+         
+     Returns:
+         An instance of the SearchEngine subclass
+         
+     Raises:
+         SearchError: If the engine is not found
+     """
+     engine_class = _engine_registry.get(engine_name)
+     if engine_class is None:
+         raise SearchError(f"Unknown search engine: {engine_name}")
+ 
+     return engine_class(config, **kwargs) 
```

---

_****_













Now, let's implement the Brave search engine.

---

_****_

```diff
- 
+ # this_file: src/twat_search/web/engines/brave.py
+ 
+ """
+ Brave Search engine implementation.
+ 
+ This module implements the Brave Search API integration.
+ """
+ 
+ import httpx
+ from typing import List, Optional, Dict, Any
+ from pydantic import BaseModel, ValidationError, HttpUrl
+ 
+ from ..config import EngineConfig
+ from ..models import SearchResult
+ from .base import SearchEngine, register_engine
+ from ..exceptions import EngineError
+ 
+ 
+ class BraveResult(BaseModel):
+     """
+     Pydantic model for a single Brave search result.
+     
+     This model is used to validate the response from the Brave API.
+     """
+     title: str
+     url: HttpUrl
+     description: str
+ 
+ 
+ class BraveResponse(BaseModel):
+     """
+     Pydantic model for the entire Brave API response.
+     
+     This is a simplified model that only captures the essentials.
+     """
+     web: Dict[str, Any]
+ 
+ 
+ @register_engine
+ class BraveSearchEngine(SearchEngine):
+     """Implementation of the Brave Search API."""
+     
+     name = "brave"
+ 
+     def __init__(self, config: EngineConfig, count: Optional[int] = None) -> None:
+         """
+         Initialize the Brave search engine.
+         
+         Args:
+             config: Configuration for this search engine
+             count: Number of results to return (overrides config)
+             
+         Raises:
+             EngineError: If the API key is missing
+         """
+         super().__init__(config)
+         self.base_url = "https://api.search.brave.com/res/v1/web/search"
+         
+         # Use provided count if available, otherwise, use default from config
+         self.count = count or self.config.default_params.get("count", 10)
+         
+         if not self.config.api_key:
+             raise EngineError(
+                 self.name,
+                 "Brave API key is required. Set it in the config or via the BRAVE_API_KEY env var.",
+             )
+             
+         self.headers = {
+             "Accept": "application/json",
+             "X-Subscription-Token": self.config.api_key,
+         }
+ 
+     async def search(self, query: str) -> List[SearchResult]:
+         """
+         Perform a search using the Brave Search API.
+         
+         Args:
+             query: The search query string
+             
+         Returns:
+             A list of SearchResult objects
+             
+         Raises:
+             EngineError: If the search fails
+         """
+         params = {"q": query, "count": self.count}
+         
+         async with httpx.AsyncClient() as client:
+             try:
+                 response = await client.get(
+                     self.base_url, headers=self.headers, params=params, timeout=10
+                 )
+                 response.raise_for_status()  # Raise HTTPError for bad responses
+                 
+                 data = response.json()
+                 brave_response = BraveResponse(**data)
+ 
+                 results = []
+                 # Ensure web and results exist
+                 if brave_response.web and brave_response.web.get("results"):
+                     for result in brave_response.web["results"]:
+                         try:
+                             # Validate and convert to BraveResult
+                             brave_result = BraveResult(**result)
+                             
+                             # Convert to common SearchResult format
+                             results.append(
+                                 SearchResult(
+                                     title=brave_result.title,
+                                     url=str(brave_result.url),
+                                     snippet=brave_result.description,
+                                     source=self.name,
+                                     raw=result,  # Include raw result for debugging
+                                 )
+                             )
+                         except ValidationError as e:
+                             # Log the specific validation error and skip this result
+                             print(f"Validation Error for Brave result: {e}\nProblematic result: {result}")
+                             continue
+                 
+                 return results
+ 
+             except httpx.RequestError as exc:
+                 raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc
+             except httpx.HTTPStatusError as exc:
+                 raise EngineError(
+                     self.name,
+                     f"HTTP Status error: {exc.response.status_code} - {exc.response.text}",
+                 ) from exc
+             except ValidationError as exc:
+                 raise EngineError(self.name, f"Response parsing error: {exc}") from exc 
```

---

_****_














Now, let's implement the Google search engine.

---

_****_

```diff
- 
+ # this_file: src/twat_search/web/engines/google.py
+ 
+ """
+ Google Search engine implementation (via SerpAPI).
+ 
+ This module implements the Google Search API integration using SerpAPI.
+ """
+ 
+ import httpx
+ from typing import List, Optional, Dict, Any
+ from pydantic import BaseModel, HttpUrl, ValidationError
+ 
+ from ..config import EngineConfig
+ from ..models import SearchResult
+ from .base import SearchEngine, register_engine
+ from ..exceptions import EngineError
+ 
+ 
+ class GoogleResult(BaseModel):
+     """
+     Pydantic model for a single Google search result.
+     
+     This model is used to validate results from the SerpAPI response.
+     """
+     title: str
+     link: HttpUrl
+     snippet: str
+ 
+ 
+ class GoogleResponse(BaseModel):
+     """
+     Pydantic model for the entire Google API response.
+     
+     This is a simplified model that focuses on organic results.
+     """
+     organic_results: List[GoogleResult]
+ 
+ 
+ @register_engine
+ class GoogleSearchEngine(SearchEngine):
+     """Implementation of the Google Search API via SerpAPI."""
+     
+     name = "google"
+ 
+     def __init__(self, config: EngineConfig, count: Optional[int] = None) -> None:
+         """
+         Initialize the Google search engine.
+         
+         Args:
+             config: Configuration for this search engine
+             count: Number of results to return (overrides config)
+             
+         Raises:
+             EngineError: If the API key is missing
+         """
+         super().__init__(config)
+         self.base_url = "https://serpapi.com/search"
+         
+         # Use provided count if available, otherwise, use default from config
+         self.count = count or self.config.default_params.get("count", 10)
+         
+         if not self.config.api_key:
+             raise EngineError(
+                 self.name,
+                 "Google (SerpAPI) API key is required. Set it in config or via the SERPAPI_API_KEY env var.",
+             )
+ 
+     async def search(self, query: str) -> List[SearchResult]:
+         """
+         Perform a search using the Google Search API via SerpAPI.
+         
+         Args:
+             query: The search query string
+             
+         Returns:
+             A list of SearchResult objects
+             
+         Raises:
+             EngineError: If the search fails
+         """
+         params = {
+             "q": query,
+             "api_key": self.config.api_key,
+             "num": self.count,
+         }
+         
+         async with httpx.AsyncClient() as client:
+             try:
+                 response = await client.get(self.base_url, params=params, timeout=10)
+                 response.raise_for_status()
+                 
+                 data = response.json()
+                 google_response = GoogleResponse(**data)  # Parse entire response
+                 
+                 results = []
+                 for result in google_response.organic_results:
+                     try:
+                         # Convert to common SearchResult format
+                         results.append(
+                             SearchResult(
+                                 title=result.title,
+                                 url=str(result.link),  # Convert HttpUrl to string
+                                 snippet=result.snippet,
+                                 source=self.name,
+                                 raw=result.model_dump(),  # Include the raw result
+                             )
+                         )
+                     except ValidationError as e:
+                         # Log the specific validation error and skip this result
+                         print(f"Validation Error for Google result: {e}\nProblematic result: {result}")
+                         continue
+                 
+                 return results
+ 
+             except httpx.RequestError as exc:
+                 raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc
+             except httpx.HTTPStatusError as exc:
+                 raise EngineError(
+                     self.name,
+                     f"HTTP Status error: {exc.response.status_code} - {exc.response.text}",
+                 ) from exc
+             except ValidationError as exc:
+                 raise EngineError(self.name, f"Response parsing error: {exc}") from exc 
```

---

_****_











Now let's implement the Tavily search engine.

---

_****_

```diff
- 
+ # this_file: src/twat_search/web/engines/tavily.py
+ 
+ """
+ Tavily Search engine implementation.
+ 
+ This module implements the Tavily Search API integration.
+ """
+ 
+ import httpx
+ from typing import List, Optional, Dict, Any
+ from pydantic import BaseModel, ValidationError
+ 
+ from ..config import EngineConfig
+ from ..models import SearchResult
+ from .base import SearchEngine, register_engine
+ from ..exceptions import EngineError
+ 
+ 
+ class TavilySearchResult(BaseModel):
+     """
+     Pydantic model for a single Tavily search result.
+     
+     This model is used to validate results from the Tavily API.
+     """
+     title: str
+     url: str  # Use str instead of HttpUrl as Tavily might return non-standard URLs
+     content: str  # Tavily returns content, not just a snippet
+ 
+ 
+ class TavilySearchResponse(BaseModel):
+     """
+     Pydantic model for the entire Tavily API response.
+     
+     This model focuses on the results array.
+     """
+     results: List[TavilySearchResult]
+ 
+ 
+ @register_engine
+ class TavilySearchEngine(SearchEngine):
+     """Implementation of the Tavily Search API."""
+     
+     name = "tavily"
+ 
+     def __init__(self, config: EngineConfig, max_results: Optional[int] = None) -> None:
+         """
+         Initialize the Tavily search engine.
+         
+         Args:
+             config: Configuration for this search engine
+             max_results: Maximum number of results to return (overrides config)
+             
+         Raises:
+             EngineError: If the API key is missing
+         """
+         super().__init__(config)
+         self.base_url = "https://api.tavily.com/search"
+         
+         # Use provided max_results if available, otherwise use default from config
+         self.max_results = max_results or self.config.default_params.get("max_results", 5)
+         
+         if not self.config.api_key:
+             raise EngineError(
+                 self.name,
+                 "Tavily API key is required. Set it in the config or via the TAVILY_API_KEY env var.",
+             )
+ 
+     async def search(self, query: str) -> List[SearchResult]:
+         """
+         Perform a search using the Tavily Search API.
+         
+         Args:
+             query: The search query string
+             
+         Returns:
+             A list of SearchResult objects
+             
+         Raises:
+             EngineError: If the search fails
+         """
+         headers = {"Content-Type": "application/json"}
+         payload = {
+             "api_key": self.config.api_key,
+             "query": query,
+             "max_results": self.max_results,
+         }
+         
+         async with httpx.AsyncClient() as client:
+             try:
+                 response = await client.post(
+                     self.base_url, headers=headers, json=payload, timeout=10
+                 )
+                 response.raise_for_status()
+                 
+                 data = response.json()
+                 tavily_response = TavilySearchResponse(**data)
+ 
+                 results = []
+                 for result in tavily_response.results:
+                     try:
+                         # Convert to common SearchResult format
+                         results.append(
+                             SearchResult(
+                                 title=result.title,
+                                 url=result.url,  # URLs are already strings
+                                 snippet=result.content[:500],  # Limit snippet length
+                                 source=self.name,
+                                 raw=result.model_dump(),
+                             )
+                         )
+                     except ValidationError as e:
+                         # Log the specific validation error and skip this result
+                         print(f"Validation Error for Tavily result: {e}\nProblematic result: {result}")
+                         continue
+                 
+                 return results
+ 
+             except httpx.RequestError as exc:
+                 raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc
+             except httpx.HTTPStatusError as exc:
+                 raise EngineError(
+                     self.name,
+                     f"HTTP Status error: {exc.response.status_code} - {exc.response.text}",
+                 ) from exc
+             except ValidationError as exc:
+                 raise EngineError(self.name, f"Response parsing error: {exc}") from exc 
```

---

_****_













Let's update the PROGRESS.md file to mark our progress.

---

_****_



---

_****_






Let me try again with the PROGRESS.md file:

---

_****_

```diff
  - [x] Create config.py with configuration classes
  - [x] Create utils.py with utility functions
- - [ ] Create engines/base.py with abstract base class and factory functions
- - [ ] Create engines/__init__.py to expose engine register functions
+ - [x] Create engines/base.py with abstract base class and factory functions
+ - [x] Create engines/__init__.py to expose engine register functions
  - [ ] Implement search engines:
-   - [ ] Brave search engine
-   - [ ] Google search engine
-   - [ ] Tavily search engine
+   - [x] Brave search engine
+   - [x] Google search engine
+   - [x] Tavily search engine
    - [ ] Perplexity search engine
    - [ ] You.com search engine
```

---

_****_









Now let's implement the Perplexity search engine.

---

_****_

```diff
- 
+ # this_file: src/twat_search/web/engines/perplexity.py
+ 
+ """
+ Perplexity AI search engine implementation.
+ 
+ This module implements the Perplexity AI API integration.
+ """
+ 
+ import httpx
+ from typing import List, Optional, Dict, Any
+ from pydantic import BaseModel, Field, ValidationError
+ 
+ from ..config import EngineConfig
+ from ..models import SearchResult
+ from .base import SearchEngine, register_engine
+ from ..exceptions import EngineError
+ 
+ 
+ class PerplexityResult(BaseModel):
+     """
+     Pydantic model for a single Perplexity result.
+     
+     This model is used to validate the response content.
+     """
+     answer: str = Field(default="")  # Perplexity may sometimes not include all details
+     url: str = Field(default="https://perplexity.ai")  # Default URL if none provided
+     title: str = Field(default="Perplexity AI Response")  # Default title
+ 
+ 
+ class PerplexityResponse(BaseModel):
+     """
+     Pydantic model for the Perplexity API response structure.
+     """
+     answers: List[PerplexityResult]  # Expect a list based on the API spec
+ 
+ 
+ @register_engine
+ class PerplexitySearchEngine(SearchEngine):
+     """Implementation of the Perplexity AI API."""
+     
+     name = "perplexity"
+ 
+     def __init__(self, config: EngineConfig, model: Optional[str] = None) -> None:
+         """
+         Initialize the Perplexity search engine.
+         
+         Args:
+             config: Configuration for this search engine
+             model: Model to use for search (overrides config)
+             
+         Raises:
+             EngineError: If the API key is missing
+         """
+         super().__init__(config)
+         self.base_url = "https://api.perplexity.ai/chat/completions"
+         
+         # Use provided model if available, otherwise use default from config
+         self.model = model or self.config.default_params.get(
+             "model", "llama-3.1-sonar-large-128k-online"
+         )
+         
+         if not self.config.api_key:
+             raise EngineError(
+                 self.name,
+                 "Perplexity API key is required. Set it in config or the PERPLEXITYAI_API_KEY env var.",
+             )
+             
+         self.headers = {
+             "accept": "application/json",
+             "content-type": "application/json",
+             "authorization": f"Bearer {self.config.api_key}",
+         }
+ 
+     async def search(self, query: str) -> List[SearchResult]:
+         """
+         Perform a search using the Perplexity AI API.
+         
+         Args:
+             query: The search query string
+             
+         Returns:
+             A list of SearchResult objects
+             
+         Raises:
+             EngineError: If the search fails
+         """
+         payload = {
+             "model": self.model,
+             "messages": [
+                 {
+                     "role": "system",
+                     "content": "Be precise and concise. I am an expert and do not need explanation",
+                 },
+                 {"role": "user", "content": query},
+             ],
+         }
+ 
+         async with httpx.AsyncClient() as client:
+             try:
+                 response = await client.post(
+                     self.base_url, headers=self.headers, json=payload, timeout=10
+                 )
+                 response.raise_for_status()
+                 
+                 data = response.json()
+                 
+                 # Adapt the parsing logic to Perplexity's response format
+                 # We wrap the response in a structure that matches our expected model
+                 perplexity_response = PerplexityResponse(
+                     answers=[
+                         {
+                             "answer": choice["message"]["content"],
+                             "url": "https://perplexity.ai",
+                             "title": f"Perplexity AI Response: {query[:30]}...",
+                         }
+                         for choice in data.get("choices", [])
+                     ]
+                 )
+ 
+                 results = []
+                 for result in perplexity_response.answers:
+                     try:
+                         # Convert to common SearchResult format
+                         results.append(
+                             SearchResult(
+                                 title=result.title,
+                                 url=result.url,  # URLs are already strings
+                                 snippet=result.answer,  # Use the answer as the snippet
+                                 source=self.name,
+                                 raw=data,  # Include raw API response
+                             )
+                         )
+                     except ValidationError as e:
+                         # Log the specific validation error and skip this result
+                         print(f"Validation Error for Perplexity result: {e}\nProblematic result: {result}")
+                         continue
+                 
+                 return results
+ 
+             except httpx.RequestError as exc:
+                 raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc
+             except httpx.HTTPStatusError as exc:
+                 raise EngineError(
+                     self.name,
+                     f"HTTP Status error: {exc.response.status_code} - {exc.response.text}",
+                 ) from exc
+             except ValidationError as exc:
+                 raise EngineError(self.name, f"Response parsing error: {exc}") from exc 
```

---

_****_














Now let's implement the You.com search engine.

---

_****_

```diff
- 
+ # this_file: src/twat_search/web/engines/youcom.py
+ 
+ """
+ You.com Search engine implementation.
+ 
+ This module implements the You.com Search API integration.
+ """
+ 
+ import httpx
+ from typing import List, Optional, Dict, Any
+ from pydantic import BaseModel, ValidationError
+ 
+ from ..config import EngineConfig
+ from ..models import SearchResult
+ from .base import SearchEngine, register_engine
+ from ..exceptions import EngineError
+ 
+ 
+ class YoucomResult(BaseModel):
+     """
+     Pydantic model for a single You.com search result.
+     
+     This model is used to validate results from the You.com API.
+     """
+     title: str
+     url: str  # Use str instead of HttpUrl for flexibility
+     snippet: str
+ 
+ 
+ class YoucomResponse(BaseModel):
+     """
+     Pydantic model for the You.com API response.
+     
+     This model focuses on the results array.
+     """
+     results: List[YoucomResult] = []  # Default to empty list if not found
+ 
+ 
+ @register_engine
+ class YoucomSearchEngine(SearchEngine):
+     """Implementation of the You.com Search API."""
+     
+     name = "youcom"
+ 
+     def __init__(self, config: EngineConfig, count: Optional[int] = None) -> None:
+         """
+         Initialize the You.com search engine.
+         
+         Args:
+             config: Configuration for this search engine
+             count: Number of results to return (overrides config)
+             
+         Raises:
+             EngineError: If the API key is missing
+         """
+         super().__init__(config)
+         self.base_url = "https://api.ydc-index.io/search"
+         
+         # Use provided count if available, otherwise, use default from config
+         self.count = count or self.config.default_params.get("count", 10)
+         
+         if not self.config.api_key:
+             raise EngineError(
+                 self.name,
+                 "You.com API key is required. Set it in config or the YOUCOM_API_KEY env var.",
+             )
+             
+         self.headers = {"X-API-Key": self.config.api_key}
+ 
+     async def search(self, query: str) -> List[SearchResult]:
+         """
+         Perform a search using the You.com Search API.
+         
+         Args:
+             query: The search query string
+             
+         Returns:
+             A list of SearchResult objects
+             
+         Raises:
+             EngineError: If the search fails
+         """
+         params = {"query": query, "limit": self.count}  # Limit is for you.com
+         
+         async with httpx.AsyncClient() as client:
+             try:
+                 response = await client.get(
+                     self.base_url, headers=self.headers, params=params, timeout=10
+                 )
+                 response.raise_for_status()
+                 
+                 data = response.json()
+                 youcom_response = YoucomResponse(**data)  # Use Pydantic model
+ 
+                 results = []
+                 # Iterate safely with the Pydantic model
+                 for result in youcom_response.results:
+                     try:
+                         # Convert to common SearchResult format
+                         results.append(
+                             SearchResult(
+                                 title=result.title,
+                                 url=result.url,  # URLs are already strings
+                                 snippet=result.snippet,
+                                 source=self.name,
+                                 raw=result.model_dump(),  # Include raw result
+                             )
+                         )
+                     except ValidationError as e:
+                         # Log the specific validation error and skip this result
+                         print(f"Validation Error for Youcom result: {e}\nProblematic result: {result}")
+                         continue
+                 
+                 return results
+ 
+             except httpx.RequestError as exc:
+                 raise EngineError(self.name, f"HTTP Request failed: {exc}") from exc
+             except httpx.HTTPStatusError as exc:
+                 raise EngineError(
+                     self.name,
+                     f"HTTP Status error: {exc.response.status_code} - {exc.response.text}",
+                 ) from exc
+             except ValidationError as exc:
+                 raise EngineError(self.name, f"Response parsing error: {exc}") from exc 
```

---

_****_












Now, let's implement the main API module.

---

_****_

```diff
- 
+ # this_file: src/twat_search/web/api.py
+ 
+ """
+ Main API module for the web search functionality.
+ 
+ This module provides the main search function that allows searching across
+ multiple engines with a unified interface.
+ """
+ 
+ import asyncio
+ import logging
+ from typing import List, Optional, Dict, Any
+ 
+ from .config import Config
+ from .models import SearchResult
+ from .engines.base import SearchEngine, get_engine
+ from .exceptions import SearchError
+ 
+ # Set up logging
+ logger = logging.getLogger(__name__)
+ 
+ 
+ async def search(
+     query: str,
+     engines: Optional[List[str]] = None,
+     config: Optional[Config] = None,
+     **kwargs: Any,
+ ) -> List[SearchResult]:
+     """
+     Performs a web search using the specified search engines.
+ 
+     This function provides a unified interface to search across multiple engines
+     and returns results in a consistent format.
+ 
+     Args:
+         query: The search query string.
+         engines: A list of engine names to use (e.g., ["brave", "google"]).
+                  If None, use all configured engines.
+         config: A Config object. If None, use the default configuration.
+         **kwargs: Engine-specific parameters (override defaults).
+                  Use engine_param to override for all engines.
+                  Use engine_name_param to override for a specific engine.
+ 
+     Returns:
+         A list of SearchResult objects.
+ 
+     Raises:
+         SearchError: If no engines are configured or if all searches fail.
+     """
+     # Load configuration if not provided
+     if config is None:
+         config = Config()
+ 
+     # Use all configured engines if none specified
+     if engines is None:
+         engines = list(config.engines.keys())
+ 
+     if not engines:
+         raise SearchError("No search engines configured.")
+ 
+     # Create search tasks for each engine
+     search_tasks = []
+     for engine_name in engines:
+         try:
+             engine_config = config.engines.get(engine_name)
+             if engine_config is None:
+                 logger.warning(f"Engine '{engine_name}' not configured.")
+                 continue
+ 
+             # Get engine-specific overrides from kwargs
+             # example: brave_count=10 would override count just for Brave
+             engine_kwargs = {
+                 k[len(engine_name) + 1:]: v
+                 for k, v in kwargs.items()
+                 if k.startswith(engine_name + "_")
+             }
+             
+             # Copy general kwargs (without engine prefix)
+             general_kwargs = {
+                 k: v for k, v in kwargs.items() 
+                 if not any(k.startswith(e + "_") for e in engines)
+             }
+             
+             # Merge general kwargs and engine-specific kwargs
+             # Engine-specific kwargs take precedence
+             merged_kwargs = {**general_kwargs, **engine_kwargs}
+ 
+             # Create the engine instance
+             engine_instance: SearchEngine = get_engine(
+                 engine_name, engine_config, **merged_kwargs
+             )
+             
+             # Add the search task
+             search_tasks.append((engine_name, engine_instance.search(query)))
+             
+         except Exception as e:
+             # Log and continue with other engines
+             logger.error(f"Error initializing engine '{engine_name}': {e}")
+             continue
+ 
+     if not search_tasks:
+         raise SearchError("No search engines could be initialized.")
+ 
+     # Run all searches concurrently
+     engine_names = [name for name, _ in search_tasks]
+     search_coroutines = [task for _, task in search_tasks]
+     results = await asyncio.gather(*search_coroutines, return_exceptions=True)
+ 
+     # Process results
+     flattened_results: List[SearchResult] = []
+     for engine_name, result in zip(engine_names, results):
+         if isinstance(result, Exception):
+             logger.error(f"Search with engine '{engine_name}' failed: {result}")
+         elif result:  # Check if results exist
+             flattened_results.extend(result)
+ 
+     return flattened_results 
```

---

_****_
















Let's update the PROGRESS.md file to mark our progress.

---

_****_

```diff
  - [x] Create engines/base.py with abstract base class and factory functions
  - [x] Create engines/__init__.py to expose engine register functions
- - [ ] Implement search engines:
+ - [x] Implement search engines:
    - [x] Brave search engine
    - [x] Google search engine
    - [x] Tavily search engine
-   - [ ] Perplexity search engine
-   - [ ] You.com search engine
- - [ ] Create api.py with the main search function
+   - [x] Perplexity search engine
+   - [x] You.com search engine
+ - [x] Create api.py with the main search function
  - [ ] Add example usage
  
```

---

_****_










Finally, let's create an example usage file.

---

_****_

```diff
- 
+ #!/usr/bin/env -S uv run -s
+ # /// script
+ # dependencies = ["httpx>=0.24.1", "pydantic>=2.0.0", "python-dotenv>=1.0.0"]
+ # ///
+ # this_file: src/twat_search/web/example.py
+ 
+ """
+ Example usage of the web search API.
+ 
+ This script demonstrates how to use the web search API with different 
+ configurations and search engines.
+ """
+ 
+ import asyncio
+ import os
+ import logging
+ from typing import List
+ 
+ # Set up logging
+ logging.basicConfig(
+     level=logging.INFO,
+     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
+ )
+ logger = logging.getLogger(__name__)
+ 
+ # Load environment variables from .env file
+ try:
+     from dotenv import load_dotenv
+     load_dotenv()
+     logger.info("Loaded environment variables from .env file")
+ except ImportError:
+     logger.warning("python-dotenv not installed, skipping .env loading")
+ 
+ # Import the search API
+ from twat_search.web.api import search
+ from twat_search.web.models import SearchResult
+ from twat_search.web.config import Config, EngineConfig
+ 
+ 
+ async def display_results(results: List[SearchResult], title: str) -> None:
+     """Display search results in a readable format."""
+     print(f"\n--- {title} ---")
+     print(f"Found {len(results)} results")
+     
+     for i, result in enumerate(results, 1):
+         print(f"\n{i}. {result.title}")
+         print(f"   URL: {result.url}")
+         print(f"   Source: {result.source}")
+         print(f"   Snippet: {result.snippet[:150]}...")  # Truncate long snippets
+ 
+ 
+ async def example_default_config() -> None:
+     """Example using default configuration."""
+     try:
+         results = await search("latest news about AI")
+         await display_results(results, "Default Configuration")
+     except Exception as e:
+         logger.error(f"Example failed: {e}")
+ 
+ 
+ async def example_specific_engines() -> None:
+     """Example using only specific engines."""
+     try:
+         results = await search("population of Tokyo", engines=["brave", "google"])
+         await display_results(results, "Specific Engines (Brave, Google)")
+     except Exception as e:
+         logger.error(f"Example failed: {e}")
+ 
+ 
+ async def example_override_params() -> None:
+     """Example overriding default parameters."""
+     try:
+         results = await search(
+             "best Python libraries for data science",
+             brave_count=5,  # Brave-specific override
+             google_count=3,  # Google-specific override
+             count=10,        # Default for all other engines
+         )
+         await display_results(results, "Override Parameters")
+     except Exception as e:
+         logger.error(f"Example failed: {e}")
+ 
+ 
+ async def example_custom_config() -> None:
+     """Example using custom configuration."""
+     try:
+         # Create a custom configuration
+         config = Config(
+             engines={
+                 "brave": EngineConfig(
+                     api_key=os.environ.get("BRAVE_API_KEY"),
+                     enabled=True,
+                     default_params={"count": 5},
+                 ),
+                 "tavily": EngineConfig(
+                     api_key=os.environ.get("TAVILY_API_KEY"),
+                     enabled=True,
+                     default_params={"max_results": 3},
+                 ),
+             }
+         )
+         
+         results = await search("machine learning tutorials", config=config)
+         await display_results(results, "Custom Configuration")
+     except Exception as e:
+         logger.error(f"Example failed: {e}")
+ 
+ 
+ async def main() -> None:
+     """Run all examples."""
+     logger.info("Starting web search examples")
+     
+     # Print available API keys for debugging
+     api_keys = {
+         "BRAVE_API_KEY": bool(os.environ.get("BRAVE_API_KEY")),
+         "SERPAPI_API_KEY": bool(os.environ.get("SERPAPI_API_KEY")),
+         "TAVILY_API_KEY": bool(os.environ.get("TAVILY_API_KEY")),
+         "PERPLEXITYAI_API_KEY": bool(os.environ.get("PERPLEXITYAI_API_KEY")),
+         "YOUCOM_API_KEY": bool(os.environ.get("YOUCOM_API_KEY")),
+     }
+     logger.info(f"API keys available: {api_keys}")
+     
+     # Run examples
+     await example_default_config()
+     await example_specific_engines()
+     await example_override_params()
+     await example_custom_config()
+     
+     logger.info("All examples completed")
+ 
+ 
+ if __name__ == "__main__":
+     asyncio.run(main()) 
```

---

_****_



---



---

