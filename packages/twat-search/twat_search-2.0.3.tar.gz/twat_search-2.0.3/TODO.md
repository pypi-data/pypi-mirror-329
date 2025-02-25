# twat-search Web Package - Future Tasks

The basic implementation of the `twat-search` web package is complete. 

Tip: Periodically run `./cleanup.py status` to see results of lints and tests. 

## 1. TODO

### 1.1. Add new engine: 

Add new engine `bing-scraper` (in `bing_scraper.py`)

uv pip install --system scrape-bing
https://github.com/AffanShaikhsurab/scraper-bing


>>> from scrape_bing import BingScraper
>>> scraper= BingScraper(
...     max_retries=3,
...     delay_between_requests=1.0
... )
>>> results = scraper.search("Adam Twardoch", num_results=5)
>>> results
[SearchResult(title='Adam Twardoch', url='https://www.twardoch.com/', description='Adam Twardoch | [auf Deutsch] I do font technology, multilingual typography, variable fonts, digital text processing, Unicode and OpenType. I manage software development and provide consulting …'), SearchResult(title='Adam Twardoch – Fontlab Ltd. | LinkedIn', url='https://pl.linkedin.com/in/twardoch', description='Born 1975 in Poland, Adam Twardoch studied business administration and cultural anthropology in Frankfurt (Oder), Germany. Following his passion for fonts and typography, Adam joined …'), SearchResult(title='Półtawski Nowy: przywrócono do życia kolejną perełkę …', url='https://designalley.pl/poltawski-nowy-digitalizacja-kroju/', description='10 gru 2020\xa0· Antykwa zaprojektowana przez Adama Półtawskiego na podstawie badań autora nad postacią graficzną tekstów drukowanych w języku polskim. …'), SearchResult(title='Adam Twardoch - Typoteka', url='https://typoteka.pl/pl/designer/adam-twardoch', description='Dyrektor produktów w firmie FontLab tworzącej cyfrowe narzędzia liternicze. Konsultant m. in. Google, Adobe, Monotype, Corel, Underware, współtwórca serwisu internetowego MyFonts. …'), SearchResult(title='Zamiast Timesa...', url='http://evil.pl/dtp/nietylkotimes.html', description='60 krojów pism przygotowanych specjalnie z myślą o zastosowaniu w składzie książek i gazet -- wyboru dokonał Adam Twardoch Na grupach dyskusyjnych pojawiają się czasem pytania o kroje …')]



# Scrape Bing

A robust Python package for scraping search results from Bing with built-in rate limiting, retry mechanisms, and result cleaning features.

## 2. Features

- 🔍 Clean and structured search results
- 🔄 Automatic retry mechanism for failed requests
- ⏱️ Built-in rate limiting to prevent blocking
- 🧹 URL cleaning and validation
- 🔄 User agent rotation
- 💪 Type hints and proper error handling
- 📝 Comprehensive documentation

## 3. Installation

You can install the package using pip:

```bash
pip install scrape-bing
```

For development installation:

```bash
git clone https://github.com/affanshaikhsurab/scrape-bing.git
cd scrape_bing
pip install -e .
```

## 4. Quick Start

```python
from scrape_bing import BingScraper

# Initialize the searcher
scraper= BingScraper(
    max_retries=3,
    delay_between_requests=1.0
)

# Perform a search
results = scraper.search("python programming", num_results=5)

# Process results
for result in results:
    print(f"\nTitle: {result.title}")
    print(f"URL: {result.url}")
    print(f"Description: {result.description}")
```

## 5. Advanced Usage

### 5.1. Custom Configuration

```python
# Configure with custom parameters
scraper = BingScraper(
    max_retries=5,                # Maximum retry attempts
    delay_between_requests=2.0    # Delay between requests in seconds
)
```

### 5.2. Error Handling

```python
from scrape_bing import BingScraper

scraper = BingScraper()

try:
    results = scraper.search("python programming")
  
except ValueError as e:
    print(f"Invalid input: {e}")
  
except ConnectionError as e:
    print(f"Network error: {e}")
  
except RuntimeError as e:
    print(f"Parsing error: {e}")
```

### 5.3. Search Result Structure

Each search result contains:

- `title`: The title of the search result
- `url`: The cleaned and validated URL
- `description`: The description snippet (if available)

```python
# Access result attributes
for result in results:
    print(result.title)       # Title of the page
    print(result.url)         # Clean URL
    print(result.description) # Description (may be None)
```

## 6. API Reference

### 6.1. BingSearch Class

```python
class BingScraper:
    def __init__(self, max_retries: int = 3, delay_between_requests: float = 1.0):
        """
        Initialize the BingSearch scraper.
  
        Args:
            max_retries: Maximum number of retry attempts for failed requests
            delay_between_requests: Minimum delay between requests in seconds
        """
        pass

    def search(self, query: str, num_results: int = 10) -> List[SearchResult]:
        """
        Perform a Bing search and return results.
  
        Args:
            query: Search query string
            num_results: Maximum number of results to return
  
        Returns:
            List of SearchResult objects
  
        Raises:
            ValueError: If query is empty
            ConnectionError: If network connection fails
            RuntimeError: If parsing fails
        """
        pass
```

### 6.2. SearchResult Class

```python
@dataclass
class SearchResult:
    title: str                    # Title of the search result
    url: str                      # Cleaned URL
    description: Optional[str]     # Description (may be None)
```

## 7. Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 8. Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
python -m pytest tests/
```

## 9. License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 10. Acknowledgments

- Beautiful Soup 4 for HTML parsing
- Requests library for HTTP requests
- Python typing for type hints

## 11. Support

If you encounter any issues or have questions, please file an issue on the GitHub repository.


### 11.1. Testing Plan

The following tests should be implemented to ensure the robustness and reliability of the package:

#### 11.1.1. Unit Tests

##### Core API
- Test `search` function
  - Test with single engine
  - Test with multiple engines
  - Test with custom configuration
  - Test with engine-specific parameters
  - Test error handling (no engines, all engines fail)
  - Test empty result handling

##### Models
- Test `SearchResult` model
  - Test validation of URLs (valid and invalid)
  - Test serialization/deserialization

##### Configuration
- Test `Config` class
  - Test loading from environment variables
  - Test loading from .env file
  - Test default configuration
- Test `EngineConfig` class
  - Test enabled/disabled functionality
  - Test default parameters

##### Utilities
- Test `RateLimiter` class
  - Test it properly limits requests to specified rate
  - Test with different rate limits
  - Test behavior under high load

##### Exceptions
- Test `SearchError` and `EngineError` classes
  - Test proper error message formatting
  - Test exception hierarchy

#### 11.1.2. Engine-specific Tests

For each search engine implementation (Brave, Google, Tavily, Perplexity, You.com):

- Test initialization
  - Test with valid configuration
  - Test with missing API key
  - Test with custom parameters
- Test search method
  - Test with mock responses (happy path)
  - Test error handling
    - Connection errors
    - API errors (rate limits, invalid requests)
    - Authentication errors
    - Timeout errors
  - Test response parsing
    - Valid responses
    - Malformed responses
    - Empty responses
- Test parameter unification
  - Test mapping of common parameters to engine-specific ones
  - Test default values
  - Test type conversions (especially for safe_search parameter)

#### 11.1.3. Integration Tests

- Test the entire search flow
  - Test search across multiple engines
  - Test fallback behavior when some engines fail
  - Test rate limiting in real-world scenarios

#### 11.1.4. Type Checking Tests

- Add tests to verify type hints are correct
- Fix existing mypy type errors identified in CLEANUP.txt
  - Fix HttpUrl validation issues
  - Fix BaseSettings issues in config.py
  - Fix missing return type annotations

#### 11.1.5. Performance Tests

- Benchmark search performance
  - Measure latency across different engines
  - Test with concurrent searches
  - Test with rate limiting

#### 11.1.6. Mock Implementation

Create mock implementations for testing that don't require actual API calls:

```python
# Example mock implementation
@register_engine
class MockSearchEngine(SearchEngine):
    name = "mock"
    
    async def search(self, query: str) -> list[SearchResult]:
        # Return predictable test results
        return [
            SearchResult(
                title="Mock Result 1",
                url="https://example.com/1",
                snippet="This is a mock result for testing",
                source=self.name
            )
        ]
```

#### 11.1.7. Test Utilities

- Create helper functions for testing
  - Mock response generators
  - Configuration helpers
  - Test data generators

#### 11.1.8. Continuous Integration

- Add GitHub workflow for running tests
- Add coverage reporting
- Add type checking to CI pipeline

Tests!!! FIXME Describe here in detail the planned tests before implementing them 

