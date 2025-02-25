# twat-search

A powerful Python web search aggregator that combines results from multiple search engines.

## Features

- **Multi-Engine Search**: Unified interface for searching across multiple providers:
  - Brave Search
  - Google Search 
  - Tavily Research
  - Perplexity
  - You.com
- **Async Support**: Concurrent searches across engines
- **Rate Limiting**: Built-in rate limiting per search engine
- **Type Safety**: Full type annotations and runtime validation
- **Error Handling**: Robust error handling and fallbacks
- **Configuration**: Flexible configuration via environment variables or code

## Installation

```bash
pip install twat-search
```

## Quick Start

```python
from twat_search.web import WebSearch

# Initialize with default configuration
search = WebSearch()

# Search across all configured engines
results = await search.q("Python async programming")

# Print results
for result in results:
  print(f"{result.title} ({result.source})")
  print(f"URL: {result.url}")
  print(f"Snippet: {result.snippet}\n")
```

## Configuration

Configure search engines via environment variables:

```bash
# API Keys
BRAVE_API_KEY=...
GOOGLE_API_KEY=...
TAVILY_API_KEY=...
PERPLEXITY_API_KEY=...
YOU_API_KEY=...

# Engine-specific settings
BRAVE_ENABLED=true
GOOGLE_ENABLED=true
TAVILY_ENABLED=true
PERPLEXITY_ENABLED=true
YOU_ENABLED=true
```

Or programmatically:

```python
from twat_search.web import WebSearch, Config

config = Config(
    brave_api_key="...",
    google_enabled=True,
    tavily_enabled=False
)

search = WebSearch(config)
```

## Response Format

Search results are returned as `SearchResult` objects:

```python
@dataclass
class SearchResult:
    title: str           # Result title
    url: HttpUrl        # Validated URL
    snippet: str        # Text snippet/description  
    source: str         # Source search engine
```

## Error Handling

The package provides custom exception classes:

- `SearchError`: Base exception class
- `EngineError`: Engine-specific errors
- `ConfigError`: Configuration errors

## Development Status

Version: 1.8.1

See [TODO.md](TODO.md) for planned improvements and feature roadmap.

## Contributing

Contributions welcome! Please check [TODO.md](TODO.md) for areas that need work.

## License

MIT License - See LICENSE file for details.

