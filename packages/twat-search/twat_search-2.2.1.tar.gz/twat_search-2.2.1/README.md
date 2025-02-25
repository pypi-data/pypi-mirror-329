# Twat Search: multi-engine web search aggregator

## Executive summary

Twat Search is a powerful, asynchronous Python package that provides a unified interface to query multiple search engines simultaneously. It facilitates efficient information retrieval by aggregating, normalizing, and processing results from various search providers through a consistent API. This comprehensive documentation serves as a definitive guide for both CLI and Python usage of the package.

## Key features

- **Multi-Engine Search**: A single query can simultaneously search across multiple providers including Brave, Google (via SerpAPI/HasData), Tavily, Perplexity, You.com, Bing (via web scraping), and more
- **Asynchronous Operation**: Leverages `asyncio` for concurrent searches, maximizing speed and efficiency
- **Rate Limiting**: Built-in mechanisms to prevent exceeding API limits of individual search providers
- **Strong Typing**: Full type annotations and Pydantic validation for improved code reliability and maintainability
- **Robust Error Handling**: Custom exception classes for graceful error management
- **Flexible Configuration**: Configure search engines via environment variables, `.env` files, or directly in code
- **Extensible Architecture**: Designed for easy addition of new search engines
- **Command-Line Interface**: Rich, interactive CLI for searching and exploring engine configurations
- **JSON Output**: Supports JSON output for easy integration with other tools

## Installation options

### Full installation

```bash
uv pip install --system twat-search[all]
```

or 

```bash
uv pip install --system twat-search[all]
```


### Selective installation

Install only specific engine dependencies:

```bash
# Example: install only brave and duckduckgo dependencies
pip install "twat-search[brave,duckduckgo]"

# Example: install duckduckgo and bing scraper
pip install "twat-search[duckduckgo,bing_scraper]"
```

After installation, both `Twat Search` and `Twat Search-web` commands should be available in your PATH. Alternatively, you can run:

```bash
python -m twat_search.__main__
python -m twat_search.web.cli
```

## Quick start guide

### Python API

```python
import asyncio
from twat_search.web import search

async def main():
    # Search across all configured engines
    results = await search("quantum computing applications")

    # Print results
    for result in results:
        print(f"[{result.source}] {result.title}")
        print(f"URL: {result.url}")
        print(f"Snippet: {result.snippet}\n")

# Run the async function
asyncio.run(main())
```

### Command line interface

```bash
# Search using all available engines
Twat Search q "climate change solutions"

# Search with specific engines
Twat Search q "machine learning frameworks" --engines brave,tavily

# Get json output
Twat Search q "renewable energy" --json

# Use engine-specific command
Twat Search brave "web development trends" --count 10
```

## Core architecture

### Module structure

```
twat_search/
└── web/
    ├── engines/            # Individual search engine implementations
    │   ├── __init__.py     # Engine registration and availability checks
    │   ├── base.py         # Base SearchEngine class definition
    │   ├── brave.py        # Brave search implementation
    │   ├── bing_scraper.py # Bing scraper implementation
    │   └── ...             # Other engine implementations
    ├── __init__.py         # Module exports
    ├── api.py              # Main search API
    ├── cli.py              # Command-line interface
    ├── config.py           # Configuration handling
    ├── exceptions.py       # Custom exceptions
    ├── models.py           # Data models
    └── utils.py            # Utility functions
```

## Supported search engines

Twat Search provides a consistent interface to the following search engines:

| Engine | Module | API Key Required | Description | Package Extra |
| --- | --- | --- | --- | --- |
| Brave | `brave` | Yes | Web search via Brave Search API | `brave` |
| Brave News | `brave_news` | Yes | News search via Brave API | `brave` |
| You.com | `you` | Yes | Web search via You.com API | - |
| You.com News | `you_news` | Yes | News search via You.com API | - |
| Tavily | `tavily` | Yes | Research-focused search API | `tavily` |
| Perplexity | `pplx` | Yes | AI-powered search with detailed answers | `pplx` |
| SerpAPI | `serpapi` | Yes | Google search results via SerpAPI | `serpapi` |
| HasData Google | `hasdata-google` | Yes | Google search results via HasData API | `hasdata` |
| HasData Google Light | `hasdata-google-light` | Yes | Light version of HasData API | `hasdata` |
| Critique | `critique` | Yes | Visual and textual search capabilities | - |
| DuckDuckGo | `duckduckgo` | No | Privacy-focused search results | `duckduckgo` |
| Bing Scraper | `bing_scraper` | No | Web scraping of Bing search results | `bing_scraper` |

## Detailed usage guide

### Python API

#### The `search()` function

The core function for performing searches is `twat_search.web.search()` :

```python
from twat_search.web import search, Config

# Basic usage
results = await search("python async programming")

# Advanced usage with specific engines and parameters
results = await search(
    query="python async programming",
    engines=["brave", "tavily", "bing_scraper"],
    num_results=5,
    language="en",
    country="US",
    safe_search=True
)
```

Parameters:

- **`query`**: The search query string (required)
- **`engines`**: A list of engine names to use (e.g., `["brave", "tavily"]`). If `None` or empty, all configured engines will be used
- **`config`**: A `Config` object. If `None`, configuration is loaded from environment variables
- **`**kwargs`\*\*: Additional parameters passed to engines. These can be:
  - General parameters applied to all engines (e.g., `num_results=10`)
  - Engine-specific parameters with prefixes (e.g., `brave_count=20`, `tavily_search_depth="advanced"`)

#### Engine-specific functions

Each engine provides a direct function for individual access:

```python
from twat_search.web.engines.brave import brave
from twat_search.web.engines.bing_scraper import bing_scraper

# Using brave search
brave_results = await brave(
    query="machine learning tutorials",
    count=10,
    country="US",
    safe_search=True
)

# Using bing scraper (no api key required)
bing_results = await bing_scraper(
    query="data science projects",
    num_results=10,
    max_retries=3,
    delay_between_requests=1.0
)
```

#### Working with search results

The `SearchResult` model provides a consistent structure across all engines:

```python
from twat_search.web.models import SearchResult
from pydantic import HttpUrl

# Creating a search result
result = SearchResult(
    title="Example Search Result",
    url=HttpUrl("https://example.com"),
    snippet="This is an example search result snippet...",
    source="brave",
    raw={"original_data": "from_engine"}  # Optional raw data
)

# Accessing properties
print(result.title)    # "Example Search Result"
print(result.url)      # "https://example.com/"
print(result.source)   # "brave"
print(result.snippet)  # "This is an example search result snippet..."
```

### Command line interface

The CLI provides convenient access to all search engines through the `Twat Search` command.

#### General search command

```bash
Twat Search q <query> [options]
```

Common options:

- `--engines <engine1,engine2,...>`: Specify engines to use
- `--num_results <n>`: Number of results to return
- `--country <country_code>`: Country to search in (e.g., "US", "GB")
- `--language <lang_code>`: Language to search in (e.g., "en", "es")
- `--safe_search <true|false>`: Enable or disable safe search
- `--json`: Output results in JSON format
- `--verbose`: Enable verbose logging

Engine-specific parameters can be passed with `--<engine>_<param> <value>` , for example:

```bash
Twat Search q "machine learning" --brave_count 15 --tavily_search_depth advanced
```

#### Engine information command

```bash
Twat Search info [engine_name] [--json]
```

- Shows information about available search engines
- If `engine_name` is provided, shows detailed information about that engine
- The `--json` flag outputs in JSON format

#### Engine-specific commands

Each engine has a dedicated command for direct access:

```bash
# Brave search
Twat Search brave "web development trends" --count 10

# Duckduckgo search
Twat Search duckduckgo "privacy tools" --max_results 5

# Bing scraper
Twat Search bing_scraper "python tutorials" --num_results 10

# Critique with image
Twat Search critique --image-url "https://example.com/image.jpg" "Is this image real?"
```

## Configuration management

### Environment variables

Configure engines using environment variables:

```bash
# Api keys
BRAVE_API_KEY=your_brave_api_key
TAVILY_API_KEY=your_tavily_api_key
PERPLEXITY_API_KEY=your_perplexity_api_key
YOU_API_KEY=your_you_api_key
SERPAPI_API_KEY=your_serpapi_api_key
CRITIQUE_API_KEY=your_critique_api_key
HASDATA_API_KEY=your_hasdata_api_key

# Engine enablement
BRAVE_ENABLED=true
TAVILY_ENABLED=true
PERPLEXITY_ENABLED=true
YOU_ENABLED=true
SERPAPI_ENABLED=true
CRITIQUE_ENABLED=true
DUCKDUCKGO_ENABLED=true
BING_SCRAPER_ENABLED=true
HASDATA_GOOGLE_ENABLED=true

# Default parameters (json format)
BRAVE_DEFAULT_PARAMS={"count": 10, "safesearch": "off"}
TAVILY_DEFAULT_PARAMS={"max_results": 5, "search_depth": "basic"}
PERPLEXITY_DEFAULT_PARAMS={"model": "pplx-7b-online"}
YOU_DEFAULT_PARAMS={"safe_search": true, "count": 8}
SERPAPI_DEFAULT_PARAMS={"num": 10, "gl": "us"}
HASDATA_GOOGLE_DEFAULT_PARAMS={"location": "Austin,Texas,United States", "device_type": "desktop"}
DUCKDUCKGO_DEFAULT_PARAMS={"max_results": 10, "safesearch": "moderate", "time": "d"}
BING_SCRAPER_DEFAULT_PARAMS={"max_retries": 3, "delay_between_requests": 1.0}

# Global default for all engines
NUM_RESULTS=5
```

You can store these in a `.env` file in your project directory, which will be automatically loaded by the library using `python-dotenv` .

### Programmatic configuration

Configure engines programmatically when using the Python API:

```python
from twat_search.web import Config, EngineConfig, search

# Create custom configuration
config = Config(
    engines={
        "brave": EngineConfig(
            api_key="your_brave_api_key",
            enabled=True,
            default_params={"count": 10, "country": "US"}
        ),
        "bing_scraper": EngineConfig(
            enabled=True,
            default_params={"max_retries": 3, "delay_between_requests": 1.0}
        ),
        "tavily": EngineConfig(
            api_key="your_tavily_api_key",
            enabled=True,
            default_params={"search_depth": "advanced"}
        )
    }
)

# Use the configuration
results = await search("quantum computing", config=config)
```

## Engine-specific parameters

Each search engine accepts different parameters. Here's a reference for commonly used ones:

### Brave search

```python
await brave(
    query="search term",
    count=10,              # Number of results (default: 10)
    country="US",          # Country code (ISO 3166-1 alpha-2)
    search_lang="en",      # Search language
    ui_lang="en",          # UI language
    safe_search=True,      # Safe search (True/False)
    freshness="day"        # Time frame (day, week, month)
)
```

### Bing scraper

```python
await bing_scraper(
    query="search term",
    num_results=10,                # Number of results
    max_retries=3,                 # Maximum retry attempts
    delay_between_requests=1.0     # Delay between requests (seconds)
)
```

### Tavily

```python
await tavily(
    query="search term",
    max_results=5,               # Number of results (default: 5)
    search_depth="basic",        # Search depth (basic, advanced)
    include_domains=["example.com"],  # Domains to include
    exclude_domains=["spam.com"],     # Domains to exclude
    include_answer=True,         # Include AI-generated answer
    search_type="search"         # Search type (search, news, etc.)
)
```

### Perplexity (pplx)

```python
await pplx(
    query="search term",
    model="pplx-70b-online"      # Model to use for search
)
```

### You.com

```python
await you(
    query="search term",
    num_results=10,              # Number of results
    country_code="US",           # Country code
    safe_search=True             # Safe search (True/False)
)
```

### Duckduckgo

```python
await duckduckgo(
    query="search term",
    max_results=10,              # Number of results
    region="us-en",              # Region code
    safesearch=True,             # Safe search (True/False)
    timelimit="m",               # Time limit (d=day, w=week, m=month)
    timeout=10                   # Request timeout (seconds)
)
```

### Critique (with image)

```python
await critique(
    query="Is this image real?",
    image_url="https://example.com/image.jpg",  # URL to image
    # OR
    image_base64="base64_encoded_image_data",   # Base64 encoded image
    source_whitelist=["trusted-site.com"],      # Optional domain whitelist
    source_blacklist=["untrusted-site.com"],    # Optional domain blacklist
    output_format="text"                        # Output format
)
```

## Error handling framework

Twat Search provides custom exception classes for proper error handling:

```python
from twat_search.web.exceptions import SearchError, EngineError

try:
    results = await search("quantum computing")
except EngineError as e:
    print(f"Engine-specific error: {e}")
    # e.g., "Engine 'brave': API key is required"
except SearchError as e:
    print(f"General search error: {e}")
    # e.g., "No search engines configured"
```

The exception hierarchy:

- `SearchError`: Base class for all search-related errors
- `EngineError`: Subclass for engine-specific errors, includes the engine name in the message

Typical error scenarios:

- Missing API keys
- Network errors
- Rate limiting
- Invalid responses
- Configuration errors

## Advanced usage techniques

### Concurrent searches

Search across multiple engines concurrently:

```python
import asyncio
from twat_search.web.engines.brave import brave
from twat_search.web.engines.tavily import tavily

async def search_multiple(query):
    brave_task = brave(query)
    tavily_task = tavily(query)

    results = await asyncio.gather(brave_task, tavily_task, return_exceptions=True)

    brave_results, tavily_results = [], []
    if isinstance(results[0], list):
        brave_results = results[0]
    if isinstance(results[1], list):
        tavily_results = results[1]

    return brave_results + tavily_results

# Usage
results = await search_multiple("artificial intelligence")
```

### Custom engine parameters

Specify engine-specific parameters in the unified search function:

```python
from twat_search.web import search

results = await search(
    "machine learning",
    engines=["brave", "tavily", "bing_scraper"],
    # Common parameters
    num_results=10,
    country="US",

    # Engine-specific parameters
    brave_count=15,
    brave_freshness="week",
    tavily_search_depth="advanced",
    bing_scraper_max_retries=5
)
```

### Rate limiting

Use the built-in rate limiter to avoid hitting API limits:

```python
from twat_search.web.utils import RateLimiter

# Create a rate limiter with 5 calls per second
limiter = RateLimiter(calls_per_second=5)

# Use in an async context
async def rate_limited_search():
    for query in ["python", "javascript", "rust", "golang"]:
        limiter.wait_if_needed()  # Wait if necessary
        results = await search(query)
        # Process results...
```

## Development guide

### Running tests

```bash
# Install test dependencies
pip install "twat-search[test]"

# Run tests
pytest

# Run with coverage
pytest --cov=src/twat_search

# Run tests in parallel
pytest -n auto
```

### Adding a new search engine

To add a new search engine:

1. Create a new file in `src/twat_search/web/engines/`
2. Implement a class that inherits from `SearchEngine`
3. Implement the required methods and register the engine

Example:

```python
from pydantic import HttpUrl
from twat_search.web.engines.base import SearchEngine, register_engine
from twat_search.web.models import SearchResult
from twat_search.web.config import EngineConfig

@register_engine
class MyNewSearchEngine(SearchEngine):
    name = "my_new_engine"
    env_api_key_names = ["MY_NEW_ENGINE_API_KEY"]

    def __init__(self, config: EngineConfig, **kwargs) -> None:
        super().__init__(config, **kwargs)
        # Initialize engine-specific parameters

    async def search(self, query: str) -> list[SearchResult]:
        # Implement search logic
        return [
            SearchResult(
                title="My Result",
                url=HttpUrl("https://example.com"),
                snippet="Result snippet",
                source=self.name
            )
        ]

# Convenience function
async def my_new_engine(query: str, **kwargs):
    # Implement convenience function
    # ...
```

### Development setup

To contribute to `Twat Search` , follow these steps:

1. Clone the repository:

```bash
   git clone https://github.com/twardoch/Twat Search.git
   cd Twat Search
```

2. Set up the virtual environment with `uv`:

```bash
   uv venv
   source .venv/bin/activate
```

3. Install development dependencies:

```bash
   uv pip install -e ".[test,dev]"
```

4. Run tests:

```bash
   uv run pytest
```

5. Run type checking:

```bash
   uv run mypy src tests
```

6. Run linting:

```bash
   uv run ruff check src tests
```

7. Use `cleanup.py` for project maintenance:

```bash
   python cleanup.py status
```

## Troubleshooting guide

### Api key issues

If you're encountering API key errors:

1. Verify the API key is set correctly in environment variables
2. Check the API key format is valid for the specific provider
3. Ensure the API key has the necessary permissions
4. For engines that require API keys, verify the key is set via one of these methods:
   - Environment variable (e.g., `BRAVE_API_KEY` )
   - `.env` file
   - Programmatic configuration

### Rate limiting problems

If you're being rate limited by search providers:

1. Reduce the number of concurrent requests
2. Use the `RateLimiter` utility to space out requests
3. Consider upgrading your API plan with the provider
4. Add delay between requests for engines that support it (e.g., `delay_between_requests` for Bing Scraper)

### No results returned

If you're not getting results:

1. Check that the engine is enabled (`ENGINE_ENABLED=true`)
2. Verify your query is not empty or too restrictive
3. Try with safe search disabled to see if content filtering is the issue
4. Check for engine-specific errors in the logs (use `--verbose` flag with CLI)
5. Ensure you have the required dependencies installed for the engine

### Common error messages

- `"Engine 'X': API key is required"`: The engine requires an API key that hasn't been configured
- `"No search engines configured"`: No engines are enabled or available
- `"Unknown search engine: X"`: The specified engine name is invalid
- `"Engine 'X': is disabled"`: The engine is registered but disabled in configuration

## Development status

Version: 1.8.1

Twat Search is actively developed. See [PROGRESS.md](PROGRESS.md) for completed tasks and [TODO.md](TODO.md) for planned features and improvements.

## Contributing

Contributions are welcome! Please check [TODO.md](TODO.md) for areas that need work. Submit pull requests or open issues on GitHub. Key areas for contribution:

- Adding new search engines
- Improving test coverage
- Enhancing documentation
- Optimizing performance
- Implementing advanced features (e.g., caching, result normalization)

## License

Twat Search is released under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Appendix: available engines and requirements

| Engine | Package Extra | API Key Required | Environment Variable | Notes |
| --- | --- | --- | --- | --- |
| Brave | `brave` | Yes | `BRAVE_API_KEY` | General web search engine |
| Brave News | `brave` | Yes | `BRAVE_API_KEY` | News-specific search |
| You.com | - | Yes | `YOU_API_KEY` | AI-powered web search |
| You.com News | - | Yes | `YOU_API_KEY` | News-specific search |
| Tavily | `tavily` | Yes | `TAVILY_API_KEY` | Research-focused search |
| Perplexity | `pplx` | Yes | `PPLX_API_KEY` | AI-powered search with detailed answers |
| SerpAPI | `serpapi` | Yes | `SERPAPI_API_KEY` | Google search results API |
| HasData Google | `hasdata` | Yes | `HASDATA_API_KEY` | Google search results API |
| HasData Google Light | `hasdata` | Yes | `HASDATA_API_KEY` | Lightweight Google search API |
| Critique | - | Yes | `CRITIQUE_API_KEY` | Supports image analysis |
| DuckDuckGo | `duckduckgo` | No | - | Privacy-focused search |
| Bing Scraper | `bing_scraper` | No | - | Uses web scraping techniques |
