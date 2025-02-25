# twat-search Web Package - Future Tasks

The basic implementation of the `twat-search` web package is complete.

Tip: Periodically run `./cleanup.py status` to see results of lints and tests.

## 1. Phase 1

### 1.1. Complete Bing Scraper Implementation

- [ ] Fix implementation issues in bing_scraper.py
  - Add proper type annotations to all methods
  - Implement better error handling with appropriate context
- [ ] Complete test coverage for BingScraperSearchEngine
  - Fix skipped tests in test_bing_scraper.py
  - Add tests for error conditions and edge cases
- [ ] Document Bing Scraper functionality
  - Add comprehensive docstrings
  - Include usage examples in README


### 1.2. Documentation and Examples

- [ ] Add comprehensive docstrings to all classes and methods
  - Include parameter descriptions
  - Document exceptions that can be raised
  - Add usage examples
- [ ] Create detailed README examples
  - Basic usage examples for each engine
  - Advanced configuration examples
  - Error handling examples
- [ ] Document environment variable configuration
  - Create a comprehensive list of all supported environment variables
  - Add examples of .env file configuration


## 2. Phase 2

### 2.1. Type Checking Errors

- [ ] Fix missing type stubs for third-party modules
  - `duckduckgo_search` and `scrape_bing` are showing import-not-found errors
  - Create local stub files or install type stubs if available
- [ ] Add type annotations to functions missing them
  - Particularly in bing_scraper.py, need to add annotations to search methods
- [ ] Fix attribute errors in You.py engine
  - "YouBaseEngine" has no attribute errors for num_results_param and base_url
- [ ] Resolve incompatible types in engine assignments in **init**.py
- [ ] Fix the test_config_with_env_vars failure (api_key not being set correctly)

### 2.2. Linting Issues

- [ ] Address boolean parameter warnings (FBT001, FBT002)
  - Consider using keyword-only arguments for boolean parameters
  - Or create specific enum types for boolean options
- [ ] Fix functions with too many parameters (PLR0913)
  - Refactor using parameter objects or configuration objects
  - Consider breaking down complex functions
- [ ] Resolve magic values in code (PLR2004)
  - Replace hardcoded numbers like 100, 5, 10 with named constants
- [ ] Clean up unused imports (F401)
  - Remove or properly use imported modules

### 2.3. Improve Test Framework

- [ ] Implement mock search engines for all providers
  - Create standardized mock responses
  - Enable offline testing without API keys
- [ ] Add integration tests
  - Test the entire search workflow
  - Test concurrent searches across multiple engines
- [ ] Create test fixtures for common configurations
  - Standard API response data
  - Common error cases
- [ ] Fix test_config_with_env_vars failure
  - Debug why environment variables aren't being properly loaded

## 3. Phase 3

### 3.1. Enhance Engine Implementations

- [ ] Standardize error handling across all engines
  - Use consistent error context and messages
  - Properly propagate exceptions with 'from exc'
- [ ] Optimize parameter handling in engines
  - Reduce code duplication in parameter mapping
  - Create utility functions for common parameter conversions
- [ ] Add timeouts to all HTTP requests
  - Ensure all engines have consistent timeout handling
  - Add configurable timeout parameters

## 4. Phase 4

### 4.1. Additional Features

- [ ] Add result caching mechanism
  - Implement optional caching of search results
  - Add configurable cache expiration
- [ ] Implement rate limiting for all engines
  - Ensure all engines respect API rate limits
  - Add configurable backoff strategies
- [ ] Add result normalization
  - Create a more consistent result format across engines
  - Implement result scoring and ranking

### 4.2. Performance Improvements

- [ ] Profile search performance across engines
  - Measure latency and throughput
  - Identify performance bottlenecks
- [ ] Implement connection pooling for HTTP clients
  - Reuse connections where possible
  - Configure appropriate connection limits
- [ ] Add parallelization options for multiple searches
  - Control concurrency limits
  - Implement proper resource cleanup
