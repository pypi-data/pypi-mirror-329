## SpecStory

## Refactoring Plan and Progress Update (25/02/2025, 07:09:08)

_**User**_

OK, I have refactored@twat_search.txt and now we get these results @CLEANUP.txt 

Task: check @TODO.md and @PROGRESS.md . Write a detailed plan with concrete proposals in @TODO.md, and write a simple itemized list in @PROGRESS.md that reflect that plan 

---

_**Assistant**_

<think>I need to analyze the information provided in the attached files and prepare a detailed plan for `TODO.md` and an updated progress list for `PROGRESS.md`.

From the `twat_search.txt` file, I can see that this is a Python package for web search with support for multiple search engines. It includes implementations for various search engines like Brave, SerpAPI, Tavily, Perplexity, You.com, Critique, DuckDuckGo, and Bing Scraper.

From the `CLEANUP.txt` file, which shows the results of running the `cleanup.py` script, I can see there are several issues that need to be addressed:

1. Type checking errors
2. Linting errors (many related to function parameters, boolean types, etc.)
3. A failing test in `test_config_with_env_vars`

Let me review `TODO.md` and `PROGRESS.md` to understand what tasks have been planned and completed.

`TODO.md` currently has a basic structure but seems to need a detailed plan. It mentions adding a new engine called `bing-scraper`, but from the `CLEANUP.txt` it appears this work might already be in progress.

`PROGRESS.md` shows that the team has completed updating search engines to use unified parameters, and the next steps need to be defined.

Based on this information, I'll create:

1. A detailed plan for `TODO.md` with concrete tasks to address the issues found in the cleanup report, improve the codebase, and add new features.
2. An updated simple itemized list for `PROGRESS.md` that reflects the current state and future plans.

Here's my plan for these files:

### Plan for TODO.md:

1. Address code quality issues
   - Fix type checking errors
   - Resolve linting warnings
   - Fix failing tests

2. Complete Bing Scraper integration
   - Fix implementation issues
   - Add comprehensive tests
   - Ensure proper error handling

3. Improve documentation
   - Add docstrings
   - Create API documentation
   - Update usage examples

4. Enhance test coverage
   - Add tests for all engines
   - Add integration tests
   - Implement mock search engines for testing

5. Implement new features
   - Add more configuration options
   - Improve result handling
   - Consider adding more search engines

### Plan for PROGRESS.md:

- [x] Updated search engines to use unified parameters
- [ ] Fixed type checking and linting issues
- [ ] Completed Bing Scraper implementation
- [ ] Improved documentation
- [ ] Enhanced test coverage
- [ ] Added new features

Now I'll create more detailed content for both files.</think>After reviewing the `twat_search.txt` and `CLEANUP.txt` files, I can see there are several issues that need to be addressed and features to be implemented. I'll update both files with a clear plan of action.

First, I'll create a detailed TODO list with concrete proposals in the TODO.md file:

---

_****_

```diff
  ## TODO
  
+ ### 1. Fix Code Quality Issues
+ 
+ #### 1.1. Type Checking Errors
+ - [ ] Fix missing type stubs for third-party modules
+   - `duckduckgo_search` and `scrape_bing` are showing import-not-found errors
+   - Create local stub files or install type stubs if available
+ - [ ] Add type annotations to functions missing them
+   - Particularly in bing_scraper.py, need to add annotations to search methods
+ - [ ] Fix attribute errors in You.py engine
+   - "YouBaseEngine" has no attribute errors for num_results_param and base_url
+ - [ ] Resolve incompatible types in engine assignments in __init__.py
+ - [ ] Fix the test_config_with_env_vars failure (api_key not being set correctly)
+ 
+ #### 1.2. Linting Issues
+ - [ ] Address boolean parameter warnings (FBT001, FBT002)
+   - Consider using keyword-only arguments for boolean parameters
+   - Or create specific enum types for boolean options
+ - [ ] Fix functions with too many parameters (PLR0913)
+   - Refactor using parameter objects or configuration objects
+   - Consider breaking down complex functions
+ - [ ] Resolve magic values in code (PLR2004)
+   - Replace hardcoded numbers like 100, 5, 10 with named constants
+ - [ ] Clean up unused imports (F401)
+   - Remove or properly use imported modules
+ 
+ ### 2. Complete Bing Scraper Implementation
+ 
+ - [ ] Fix implementation issues in bing_scraper.py
+   - Add proper type annotations to all methods
+   - Implement better error handling with appropriate context
+ - [ ] Complete test coverage for BingScraperSearchEngine
+   - Fix skipped tests in test_bing_scraper.py
+   - Add tests for error conditions and edge cases
+ - [ ] Document Bing Scraper functionality
+   - Add comprehensive docstrings
+   - Include usage examples in README
+ 
+ ### 3. Improve Test Framework
+ 
+ - [ ] Implement mock search engines for all providers
+   - Create standardized mock responses
+   - Enable offline testing without API keys
+ - [ ] Add integration tests
+   - Test the entire search workflow
+   - Test concurrent searches across multiple engines
+ - [ ] Create test fixtures for common configurations
+   - Standard API response data
+   - Common error cases
+ - [ ] Fix test_config_with_env_vars failure
+   - Debug why environment variables aren't being properly loaded
+ 
+ ### 4. Enhance Engine Implementations
+ 
+ - [ ] Standardize error handling across all engines
+   - Use consistent error context and messages
+   - Properly propagate exceptions with 'from exc'
+ - [ ] Optimize parameter handling in engines
+   - Reduce code duplication in parameter mapping
+   - Create utility functions for common parameter conversions
+ - [ ] Add timeouts to all HTTP requests
+   - Ensure all engines have consistent timeout handling
+   - Add configurable timeout parameters
+ 
+ ### 5. Documentation and Examples
+ 
+ - [ ] Add comprehensive docstrings to all classes and methods
+   - Include parameter descriptions
+   - Document exceptions that can be raised
+   - Add usage examples
+ - [ ] Create detailed README examples
+   - Basic usage examples for each engine
+   - Advanced configuration examples
+   - Error handling examples
+ - [ ] Document environment variable configuration
+   - Create a comprehensive list of all supported environment variables
+   - Add examples of .env file configuration
+ 
+ ### 6. Additional Features
+ 
+ - [ ] Add result caching mechanism
+   - Implement optional caching of search results
+   - Add configurable cache expiration
+ - [ ] Implement rate limiting for all engines
+   - Ensure all engines respect API rate limits
+   - Add configurable backoff strategies
+ - [ ] Add result normalization
+   - Create a more consistent result format across engines
+   - Implement result scoring and ranking
+ 
+ ### 7. Performance Improvements
+ 
+ - [ ] Profile search performance across engines
+   - Measure latency and throughput
+   - Identify performance bottlenecks
+ - [ ] Implement connection pooling for HTTP clients
+   - Reuse connections where possible
+   - Configure appropriate connection limits
+ - [ ] Add parallelization options for multiple searches
+   - Control concurrency limits
+   - Implement proper resource cleanup
+ 
  
```

---

_****_



Now, let me update the PROGRESS.md file with a simple itemized list that reflects the plan:

---

_****_

```diff
  ---
  
+ ## Completed
+ - [x] Defined common parameters in base `SearchEngine` class
  - [x] Updated search engines to use unified parameters
- - [ ] Next step
+ - [x] Added support for multiple search engines (Brave, Tavily, Perplexity, You.com, SerpAPI, Critique, DuckDuckGo)
+ - [x] Implemented initial version of Bing Scraper engine
+ - [x] Created basic testing infrastructure
+ 
+ ## In Progress
+ - [ ] Fixing type checking and linting issues identified in cleanup report
+ - [ ] Completing Bing Scraper implementation and tests
+ - [ ] Addressing failing test in config environment variable loading
+ 
+ ## Upcoming
+ - [ ] Enhancing test framework with mocks and fixtures
+ - [ ] Standardizing error handling across all engines
+ - [ ] Improving documentation and adding comprehensive examples
+ - [ ] Implementing performance optimizations
+ - [ ] Adding advanced features (caching, rate limiting, result normalization)
+ 
+ ## Known Issues
+ - Environment variable loading not working correctly in tests
+ - Missing type annotations in several modules
+ - Excessive parameter counts in engine initialization methods
+ - Skipped tests for asynchronous components
+ 
+ See [TODO.md](TODO.md) for the detailed task breakdown and implementation plans.
  
```

---

_****_



I've updated both files based on my analysis of the codebase and the cleanup report:

1. **TODO.md** now contains a comprehensive, actionable plan organized into seven main categories:
   - Code quality fixes for type checking and linting issues
   - Completion of the Bing Scraper implementation
   - Improvements to the test framework
   - Enhancements to engine implementations
   - Documentation and examples
   - Additional features
   - Performance improvements

   Each category contains specific tasks with concrete proposals and implementation suggestions.

2. **PROGRESS.md** now shows a clearer picture of the project's status with:
   - Completed tasks showing what has been accomplished
   - In-progress tasks highlighting current work
   - Upcoming tasks aligned with the TODO plan
   - Known issues that need to be addressed

The plans focus particularly on fixing the immediate issues identified in the cleanup report while also providing a roadmap for future enhancements. The failing test for environment variable loading is specifically addressed in both files, as this appears to be a critical issue.

Would you like me to focus on any particular section of the plan in more detail, or perhaps create implementation strategies for specific high-priority items?

---



---

