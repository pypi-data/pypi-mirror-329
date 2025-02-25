#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["httpx>=0.24.1", "pydantic>=2.0.0", "python-dotenv>=1.0.0", "fire>=0.5.0", "rich>=13.6.0"]
# ///
# this_file: src/twat_search/web/cli.py

"""
CLI tool for performing web searches across multiple engines.

This tool allows you to search the web using various search engines and
displays the results in a formatted table.
"""

import asyncio
import os
import logging
import json as json_lib
from typing import Any, TYPE_CHECKING

# We need to ignore the missing stubs for fire
import fire  # type: ignore
from rich.console import Console
from rich.table import Table
from rich.logging import RichHandler

from twat_search.web.api import search
from twat_search.web.config import Config
from twat_search.web.engines import (
    brave,
    brave_news,
    critique,
    duckduckgo,
    pplx,
    serpapi,
    tavily,
    you,
    you_news,
)

if TYPE_CHECKING:
    from twat_search.web.config import Config


# Custom JSON encoder that handles non-serializable objects
class CustomJSONEncoder(json_lib.JSONEncoder):
    """Custom JSON encoder that converts non-serializable objects to strings."""

    def default(self, o: Any) -> Any:
        """Convert non-serializable objects to strings.

        Args:
            o: The object to convert

        Returns:
            A JSON serializable object
        """
        try:
            return json_lib.JSONEncoder.default(self, o)
        except TypeError:
            # Convert non-serializable objects to their string representation
            return str(o)


# Set up console
console = Console()


class SearchCLI:
    """Web search CLI tool that displays results from multiple search engines."""

    def __init__(self) -> None:
        """Initialize SearchCLI with default logging setup."""
        # Set up logging with rich
        self.log_handler = RichHandler(rich_tracebacks=True)
        logging.basicConfig(
            level=logging.CRITICAL,  # Default to CRITICAL level to hide all logs
            format="%(message)s",
            handlers=[self.log_handler],
        )
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.CRITICAL)  # Explicitly set logger level

        # Load environment variables from .env file
        try:
            from dotenv import load_dotenv

            load_dotenv()
            # Use debug level for this message so it only shows in verbose mode
            self.logger.debug("Loaded environment variables from .env file")
        except ImportError:
            # Also use debug level for this warning
            self.logger.debug("python-dotenv not installed, skipping .env loading")

    def _configure_logging(self, verbose: bool = False) -> None:
        """Configure logging based on verbose flag.

        Args:
            verbose: Whether to show detailed logs
        """
        log_level = (
            logging.INFO if verbose else logging.CRITICAL
        )  # Use CRITICAL to hide all logs

        # Update logger levels
        logging.getLogger().setLevel(log_level)
        self.logger.setLevel(log_level)
        self.log_handler.level = log_level

        # Import modules after setting log level

    def _parse_engines(self, engines_arg: Any) -> list[str] | None:
        """Parse engines argument into a list of engine names.

        Handles various formats:
        - String (comma-separated): "brave,google"
        - Tuple or List of strings: ("brave", "google")
        - None: Returns None (use default engines)

        Args:
            engines_arg: The engines argument from the command line

        Returns:
            List of engine names or None
        """
        if engines_arg is None:
            return None

        # Handle string input (from --engines="brave,google")
        if isinstance(engines_arg, str):
            return [e.strip() for e in engines_arg.split(",") if e.strip()]

        # Handle tuple/list input (from --engines brave google)
        if isinstance(engines_arg, list | tuple):
            return [str(e).strip() for e in engines_arg if str(e).strip()]

        # Handle unexpected type by logging and returning None
        self.logger.warning(
            f"Unexpected engines type: {type(engines_arg)}. Using all available engines."
        )
        return None

    async def _run_search(
        self,
        query: str = "president of poland",
        engines: list[str] | None = None,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """Run search across all available engines.

        Args:
            query: The search term to query
            engines: Optional list of specific engines to use
            **kwargs: Additional engine-specific parameters

        Returns:
            List of result dictionaries with engine name, status, and results
        """
        # Import here to ensure logging is configured before import

        self.logger.info(f"🔍 Searching for: {query}")

        try:
            results = await search(query, engines=engines, **kwargs)
            return self._process_results(results)
        except Exception as e:
            self.logger.error(f"❌ Search failed: {e}")
            return []

    def _process_results(self, results: list) -> list[dict[str, Any]]:
        """Process search results into a standardized format for display.

        Args:
            results: List of SearchResult objects

        Returns:
            Processed results with engine name, status, and formatted data
        """
        processed = []

        # Group results by engine
        engine_results: dict[str, list] = {}
        for result in results:
            # Get engine source from result metadata or use 'unknown'
            engine_name = getattr(result, "source", None) or "unknown"
            if engine_name not in engine_results:
                engine_results[engine_name] = []
            engine_results[engine_name].append(result)

        # Process each engine's results
        for engine, engine_results_list in engine_results.items():
            if not engine_results_list:
                processed.append(
                    {
                        "engine": engine,
                        "status": "❌ No results",
                        "url": "N/A",
                        "title": "N/A",
                        "snippet": "N/A",
                        "raw_result": None,  # Add raw result field
                    }
                )
                continue

            # Get the first (top) result
            top_result = engine_results_list[0]
            # Convert URL to string if it's not already
            url = str(top_result.url)
            processed.append(
                {
                    "engine": engine,
                    "status": "✅ Success",
                    "url": url,
                    "title": top_result.title,
                    "snippet": top_result.snippet[:100] + "..."
                    if len(top_result.snippet) > 100
                    else top_result.snippet,
                    "raw_result": getattr(
                        top_result, "raw", None
                    ),  # Store raw result data
                }
            )

        return processed

    def _display_results(
        self, processed_results: list[dict[str, Any]], verbose: bool = False
    ) -> None:
        """Display search results in a rich table.

        Args:
            processed_results: List of processed result dictionaries
            verbose: Whether to show detailed information
        """
        if not processed_results:
            console.print("[bold red]No results found![/bold red]")
            return

        if verbose:
            # Detailed table for verbose mode
            table = Table(title="🌐 Web Search Results")
            table.add_column("Engine", style="cyan", no_wrap=True)
            table.add_column("Status", style="magenta")
            table.add_column("Title", style="green")
            table.add_column("URL", style="blue")

            for result in processed_results:
                table.add_row(
                    result["engine"], result["status"], result["title"], result["url"]
                )
        else:
            # Simplified table for normal mode - just engine and first result
            table = Table(title="🌐 Web Search Results")
            table.add_column("Engine", style="cyan", no_wrap=True)
            table.add_column("Result", style="green")

            for result in processed_results:
                # Skip failed results in non-verbose mode
                if "❌" in result["status"]:
                    continue

                table.add_row(result["engine"], result["title"])

        console.print(table)

    def _display_json_results(self, processed_results: list[dict[str, Any]]) -> None:
        """Display search results in JSON format.

        Args:
            processed_results: List of processed result dictionaries
        """
        # Organize results by engine
        results_by_engine = {}
        for result in processed_results:
            engine = result["engine"]
            results_by_engine[engine] = {
                "status": "success" if "✅" in result["status"] else "error",
                "url": result["url"] if result["url"] != "N/A" else None,
                "title": result["title"] if result["title"] != "N/A" else None,
                "snippet": result["snippet"]
                if result.get("snippet") != "N/A"
                else None,
                "result": result.get("raw_result"),  # Include raw result data
            }

        # Print JSON output directly without using rich console
        # This ensures clean JSON output for piping or programmatic use

    def _display_errors(self, error_messages: list[str]) -> None:
        """Display error messages in a rich table.

        Args:
            error_messages: List of error messages
        """
        if not error_messages:
            return

        table = Table(title="❌ Search Errors")
        table.add_column("Error", style="red")

        for error in error_messages:
            table.add_row(error)

        console.print(table)

    def q(
        self,
        query: str,
        engines: str | list[str] | None = None,
        num_results: int = 5,
        country: str | None = None,
        language: str | None = None,
        safe_search: bool = True,
        time_frame: str | None = None,
        verbose: bool = False,
        json: bool = False,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """
        Search across multiple engines.

        Args:
            query: The search query
            engines: Comma-separated list of engines or list of engine names
            num_results: Number of results per engine (default: 5)
            country: Country code for search results
            language: Language code for search results
            safe_search: Whether to enable safe search (default: True)
            time_frame: Time frame for results (e.g., "day", "week", "month")
            verbose: Whether to display verbose output
            json: Whether to display results in JSON format
            **kwargs: Additional engine-specific parameters

        Returns:
            List of processed search results
        """
        self._configure_logging(verbose)
        engine_list = self._parse_engines(engines)

        # Prepare common parameters
        common_params = {
            "num_results": num_results,
            "country": country,
            "language": language,
            "safe_search": safe_search,
            "time_frame": time_frame,
        }

        # Remove None values
        common_params = {k: v for k, v in common_params.items() if v is not None}

        # Only show status spinner when not in JSON mode
        if json:
            results = asyncio.run(
                self._run_search(query, engine_list, **common_params, **kwargs)
            )
        else:
            with console.status(f"[bold green]Searching for '{query}'...[/bold green]"):
                results = asyncio.run(
                    self._run_search(query, engine_list, **common_params, **kwargs)
                )

        if json:
            self._display_json_results(results)
            # Don't return raw results to avoid double output in json mode
            return []
        else:
            self._display_results(results, verbose)
            return results

    def info(self, engine: str | None = None, json: bool = False) -> None:
        """
        Display information about search engines.

        Args:
            engine: Optional specific engine to show details for.
                   If not provided, lists all available engines.
            json: Whether to display results in JSON format
        """
        try:
            # Import here to ensure logging is configured
            from twat_search.web.config import Config

            # Create a temporary config to see available engines
            config = Config()

            if json:
                # JSON output mode - return structured engine info
                self._display_engines_json(engine, config)
            elif engine is None:
                # List all engines
                self._list_all_engines(config)
            else:
                # Show details for specific engine
                self._show_engine_details(engine, config)

        except Exception as e:
            if not json:
                self.logger.error(f"❌ Failed to display engine information: {e}")
            else:
                # In JSON mode, return error as JSON
                pass

    def _list_all_engines(self, config: "Config") -> None:
        """List all available search engines."""
        table = Table(title="🔎 Available Search Engines")
        table.add_column("Engine", style="cyan", no_wrap=True)
        table.add_column("Enabled", style="magenta")
        table.add_column("API Key Required", style="yellow")

        # Try to get registered engines for more accurate API key requirements
        try:
            from twat_search.web.engines.base import get_registered_engines

            registered_engines = get_registered_engines()
        except ImportError:
            registered_engines = {}

        for engine, engine_config in config.engines.items():
            # First check if the config has an API key set
            api_key_required = (
                hasattr(engine_config, "api_key") and engine_config.api_key is not None
            )

            # If not, check if the engine class has env_api_key_names
            if not api_key_required and engine in registered_engines:
                engine_class = registered_engines.get(engine)
                if engine_class and hasattr(engine_class, "env_api_key_names"):
                    # If the class has non-empty env_api_key_names, it requires an API key
                    api_key_required = bool(engine_class.env_api_key_names)

            table.add_row(
                engine,
                "✅" if engine_config.enabled else "❌",
                "✅" if api_key_required else "❌",
            )

        console.print(table)
        console.print(
            "\n[italic]Run 'info ENGINE_NAME' for more details about a specific engine.[/italic]"
        )

    def _show_engine_details(self, engine_name: str, config: "Config") -> None:
        """Show detailed information about a specific engine."""
        # Check if engine exists in config
        if engine_name not in config.engines:
            console.print(f"[bold red]Engine '{engine_name}' not found![/bold red]")
            console.print("\nAvailable engines:")
            for name in config.engines:
                console.print(f"- {name}")
            return

        # Get engine configuration
        engine_config = config.engines[engine_name]

        # Default API key requirement check
        api_key_required = (
            hasattr(engine_config, "api_key") and engine_config.api_key is not None
        )

        # Try to import the engine class to get more details
        try:
            # Import base engine module
            from twat_search.web.engines.base import get_engine, get_registered_engines

            # Get registered engines to access the class
            registered_engines = get_registered_engines()
            engine_class = registered_engines.get(engine_name)

            # Update API key requirement based on class information
            if (
                not api_key_required
                and engine_class
                and hasattr(engine_class, "env_api_key_names")
            ):
                api_key_required = bool(engine_class.env_api_key_names)

            # Display detailed information
            console.print(f"\n[bold cyan]🔍 Engine: {engine_name}[/bold cyan]")
            console.print(
                f"[bold]Enabled:[/bold] {'✅' if engine_config.enabled else '❌'}"
            )
            console.print(
                f"[bold]API Key Required:[/bold] {'✅' if api_key_required else '❌'}"
            )

            # Show API key environment variables
            if engine_class and hasattr(engine_class, "env_api_key_names"):
                console.print("\n[bold]API Key Environment Variables:[/bold]")
                for env_name in engine_class.env_api_key_names:
                    value_status = "✅" if os.environ.get(env_name) else "❌"
                    console.print(f"  {env_name}: {value_status}")

            # Show default parameters
            console.print("\n[bold]Default Parameters:[/bold]")
            if engine_config.default_params:
                for param, value in engine_config.default_params.items():
                    console.print(f"  {param}: {value}")
            else:
                console.print("  No default parameters specified")

            # Show function information if available
            try:
                # Determine module name - handle special cases like brave-news → brave
                base_engine = engine_name.split("-")[0]
                module_name = f"twat_search.web.engines.{base_engine}"

                # Try to import the module
                import importlib

                engine_module = importlib.import_module(module_name)

                # Check for function with matching name
                function_name = engine_name.replace("-", "_")
                if hasattr(engine_module, function_name):
                    func = getattr(engine_module, function_name)
                    console.print("\n[bold]Function Interface:[/bold]")
                    console.print(
                        f"  [green]{function_name}()[/green] - {func.__doc__.strip().split('\\n')[0]}"
                    )

                    # Show example usage
                    console.print("\n[bold]Example Usage:[/bold]")
                    console.print(
                        f"  [italic]from {module_name} import {function_name}[/italic]"
                    )
                    console.print(
                        f'  [italic]results = await {function_name}("your search query")[/italic]'
                    )
            except (ImportError, AttributeError, IndexError):
                # Function might not exist or have different structure
                pass

        except (ImportError, AttributeError) as e:
            # Fallback to basic information if we can't get detailed info
            console.print(
                f"[bold yellow]Could not load detailed engine information: {e}[/bold yellow]"
            )
            console.print("\n[bold]Basic Configuration:[/bold]")
            console.print(f"Enabled: {'✅' if engine_config.enabled else '❌'}")
            console.print(f"Has API Key: {'✅' if engine_config.api_key else '❌'}")
            console.print(f"Default Parameters: {engine_config.default_params}")

    def _display_engines_json(self, engine: str | None, config: "Config") -> None:
        """Display engine information in JSON format.

        Args:
            engine: Optional specific engine name
            config: Engine configuration
        """
        from twat_search.web.engines.base import get_registered_engines

        try:
            registered_engines = get_registered_engines()
        except ImportError:
            registered_engines = {}

        result = {}

        if engine:
            # Single engine info
            if engine not in config.engines:
                return

            engine_config = config.engines[engine]
            result[engine] = self._get_engine_info(
                engine, engine_config, registered_engines
            )
        else:
            # All engines info
            for engine_name, engine_config in config.engines.items():
                result[engine_name] = self._get_engine_info(
                    engine_name, engine_config, registered_engines
                )

    def _get_engine_info(
        self, engine_name: str, engine_config: Any, registered_engines: dict
    ) -> dict:
        """Get structured information about an engine.

        Args:
            engine_name: Name of the engine
            engine_config: Engine configuration object
            registered_engines: Dictionary of registered engine classes

        Returns:
            Dictionary with engine information
        """
        # Check if API key is required
        api_key_required = False
        api_key_set = False
        env_vars = []

        if hasattr(engine_config, "api_key") and engine_config.api_key is not None:
            api_key_required = True
            api_key_set = True

        # Check if engine class has env_api_key_names
        if engine_name in registered_engines:
            engine_class = registered_engines.get(engine_name)
            if engine_class and hasattr(engine_class, "env_api_key_names"):
                api_key_required = bool(engine_class.env_api_key_names)
                env_vars = [
                    {"name": env_name, "set": bool(os.environ.get(env_name))}
                    for env_name in engine_class.env_api_key_names
                ]

        # Get default parameters
        default_params = {}
        if hasattr(engine_config, "default_params") and engine_config.default_params:
            default_params = engine_config.default_params

        return {
            "enabled": engine_config.enabled
            if hasattr(engine_config, "enabled")
            else False,
            "api_key_required": api_key_required,
            "api_key_set": api_key_set,
            "env_vars": env_vars,
            "default_params": default_params,
        }

    async def critique(
        self,
        query: str,
        num_results: int = 5,
        country: str | None = None,
        language: str | None = None,
        safe_search: bool | None = True,
        time_frame: str | None = None,
        image_url: str | None = None,
        image_base64: str | None = None,
        source_whitelist: str | None = None,
        source_blacklist: str | None = None,
        api_key: str | None = None,
        verbose: bool = False,
        json: bool = False,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """
        Search using Critique Labs AI search.

        Args:
            query: Search query string
            num_results: Number of results to return
            country: Country code
            language: Language code
            safe_search: Whether to enable safe search
            time_frame: Time frame for results
            image_url: URL of an image to include in search
            image_base64: Base64-encoded image to include in search
            source_whitelist: Comma-separated list of domains to include
            source_blacklist: Comma-separated list of domains to exclude
            api_key: API key (otherwise use environment variable)
            verbose: Show detailed output
            json: Return results as JSON
            **kwargs: Additional engine-specific parameters

        Returns:
            List of search results as dictionaries
        """
        self._configure_logging(verbose)

        # Only show status message when not in JSON mode
        console = Console()
        if not json:
            console.print(f"[bold]Searching Critique Labs AI[/bold]: {query}")

        # Convert comma-separated lists to actual lists
        source_whitelist_list = None
        if source_whitelist:
            source_whitelist_list = [s.strip() for s in source_whitelist.split(",")]

        source_blacklist_list = None
        if source_blacklist:
            source_blacklist_list = [s.strip() for s in source_blacklist.split(",")]

        results = await critique(
            query=query,
            num_results=num_results,
            country=country,
            language=language,
            safe_search=safe_search,
            time_frame=time_frame,
            image_url=image_url,
            image_base64=image_base64,
            source_whitelist=source_whitelist_list,
            source_blacklist=source_blacklist_list,
            api_key=api_key,
            **kwargs,
        )

        processed_results = self._process_results(results)

        if json:
            self._display_json_results(processed_results)
            # Don't return raw results to avoid double output in json mode
            return []
        else:
            self._display_results(processed_results, verbose)
            return processed_results

    async def brave(
        self,
        query: str,
        num_results: int = 5,
        country: str | None = None,
        language: str | None = None,
        safe_search: bool | None = True,
        time_frame: str | None = None,
        api_key: str | None = None,
        verbose: bool = False,
        json: bool = False,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """
        Search using Brave Search.

        Args:
            query: Search query string
            num_results: Number of results to return
            country: Country code
            language: Language code
            safe_search: Whether to enable safe search
            time_frame: Time frame for results
            api_key: API key (otherwise use environment variable)
            verbose: Show detailed output
            json: Return results as JSON
            **kwargs: Additional engine-specific parameters

        Returns:
            List of search results as dictionaries
        """
        self._configure_logging(verbose)

        # Only show status message when not in JSON mode
        console = Console()
        if not json:
            console.print(f"[bold]Searching Brave[/bold]: {query}")

        results = await brave(
            query=query,
            num_results=num_results,
            country=country,
            language=language,
            safe_search=safe_search,
            time_frame=time_frame,
            api_key=api_key,
            **kwargs,
        )

        processed_results = self._process_results(results)

        if json:
            self._display_json_results(processed_results)
            # Don't return raw results to avoid double output in json mode
            return []
        else:
            self._display_results(processed_results, verbose)
            return processed_results

    async def brave_news(
        self,
        query: str,
        num_results: int = 5,
        country: str | None = None,
        language: str | None = None,
        safe_search: bool | None = True,
        time_frame: str | None = None,
        api_key: str | None = None,
        verbose: bool = False,
        json: bool = False,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """
        Search using Brave News Search.

        Args:
            query: Search query string
            num_results: Number of results to return
            country: Country code
            language: Language code
            safe_search: Whether to enable safe search
            time_frame: Time frame for results
            api_key: API key (otherwise use environment variable)
            verbose: Show detailed output
            json: Return results as JSON
            **kwargs: Additional engine-specific parameters

        Returns:
            List of search results as dictionaries
        """
        self._configure_logging(verbose)

        # Only show status message when not in JSON mode
        console = Console()
        if not json:
            console.print(f"[bold]Searching Brave News[/bold]: {query}")

        results = await brave_news(
            query=query,
            num_results=num_results,
            country=country,
            language=language,
            safe_search=safe_search,
            time_frame=time_frame,
            api_key=api_key,
            **kwargs,
        )

        processed_results = self._process_results(results)

        if json:
            self._display_json_results(processed_results)
            # Don't return raw results to avoid double output in json mode
            return []
        else:
            self._display_results(processed_results, verbose)
            return processed_results

    async def serpapi(
        self,
        query: str,
        num_results: int = 5,
        country: str | None = None,
        language: str | None = None,
        safe_search: bool | None = True,
        time_frame: str | None = None,
        api_key: str | None = None,
        verbose: bool = False,
        json: bool = False,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """
        Search using SerpAPI (Google Search API).

        Args:
            query: Search query string
            num_results: Number of results to return
            country: Country code
            language: Language code
            safe_search: Whether to enable safe search
            time_frame: Time frame for results
            api_key: API key (otherwise use environment variable)
            verbose: Show detailed output
            json: Return results as JSON
            **kwargs: Additional engine-specific parameters

        Returns:
            List of search results as dictionaries
        """
        self._configure_logging(verbose)

        # Only show status message when not in JSON mode
        console = Console()
        if not json:
            console.print(f"[bold]Searching SerpAPI (Google)[/bold]: {query}")

        results = await serpapi(
            query=query,
            num_results=num_results,
            country=country,
            language=language,
            safe_search=safe_search,
            time_frame=time_frame,
            api_key=api_key,
            **kwargs,
        )

        processed_results = self._process_results(results)

        if json:
            self._display_json_results(processed_results)
            # Don't return raw results to avoid double output in json mode
            return []
        else:
            self._display_results(processed_results, verbose)
            return processed_results

    async def tavily(
        self,
        query: str,
        num_results: int = 5,
        country: str | None = None,
        language: str | None = None,
        safe_search: bool | None = True,
        time_frame: str | None = None,
        api_key: str | None = None,
        search_depth: str = "basic",
        include_domains: str | None = None,
        exclude_domains: str | None = None,
        verbose: bool = False,
        json: bool = False,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """
        Search using Tavily AI Search.

        Args:
            query: Search query string
            num_results: Number of results to return
            country: Country code
            language: Language code
            safe_search: Whether to enable safe search
            time_frame: Time frame for results
            api_key: API key (otherwise use environment variable)
            search_depth: Search depth (basic or comprehensive)
            include_domains: Comma-separated list of domains to include
            exclude_domains: Comma-separated list of domains to exclude
            verbose: Show detailed output
            json: Return results as JSON
            **kwargs: Additional engine-specific parameters

        Returns:
            List of search results as dictionaries
        """
        self._configure_logging(verbose)

        # Only show status message when not in JSON mode
        console = Console()
        if not json:
            console.print(f"[bold]Searching Tavily AI[/bold]: {query}")

        # Convert comma-separated lists to actual lists
        include_domains_list = None
        if include_domains:
            include_domains_list = [s.strip() for s in include_domains.split(",")]

        exclude_domains_list = None
        if exclude_domains:
            exclude_domains_list = [s.strip() for s in exclude_domains.split(",")]

        results = await tavily(
            query=query,
            num_results=num_results,
            country=country,
            language=language,
            safe_search=safe_search,
            time_frame=time_frame,
            api_key=api_key,
            search_depth=search_depth,
            include_domains=include_domains_list,
            exclude_domains=exclude_domains_list,
            **kwargs,
        )

        processed_results = self._process_results(results)

        if json:
            self._display_json_results(processed_results)
            # Don't return raw results to avoid double output in json mode
            return []
        else:
            self._display_results(processed_results, verbose)
            return processed_results

    async def pplx(
        self,
        query: str,
        num_results: int = 5,
        country: str | None = None,
        language: str | None = None,
        safe_search: bool | None = True,
        time_frame: str | None = None,
        api_key: str | None = None,
        model: str | None = None,
        verbose: bool = False,
        json: bool = False,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """
        Search using Perplexity AI.

        Args:
            query: Search query string
            num_results: Number of results to return
            country: Country code
            language: Language code
            safe_search: Whether to enable safe search
            time_frame: Time frame for results
            api_key: API key (otherwise use environment variable)
            model: Model to use (e.g., "sonar-small-online", "sonar-medium-online")
            verbose: Show detailed output
            json: Return results as JSON
            **kwargs: Additional engine-specific parameters

        Returns:
            List of search results as dictionaries
        """
        self._configure_logging(verbose)

        # Only show status message when not in JSON mode
        console = Console()
        if not json:
            console.print(f"[bold]Searching Perplexity AI[/bold]: {query}")

        results = await pplx(
            query=query,
            num_results=num_results,
            country=country,
            language=language,
            safe_search=safe_search,
            time_frame=time_frame,
            api_key=api_key,
            model=model,
            **kwargs,
        )

        processed_results = self._process_results(results)

        if json:
            self._display_json_results(processed_results)
            # Don't return raw results to avoid double output in json mode
            return []
        else:
            self._display_results(processed_results, verbose)
            return processed_results

    async def you(
        self,
        query: str,
        num_results: int = 5,
        country: str | None = None,
        language: str | None = None,
        safe_search: bool | None = True,
        time_frame: str | None = None,
        api_key: str | None = None,
        verbose: bool = False,
        json: bool = False,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """
        Search using You.com Search.

        Args:
            query: Search query string
            num_results: Number of results to return
            country: Country code
            language: Language code
            safe_search: Whether to enable safe search
            time_frame: Time frame for results
            api_key: API key (otherwise use environment variable)
            verbose: Show detailed output
            json: Return results as JSON
            **kwargs: Additional engine-specific parameters

        Returns:
            List of search results as dictionaries
        """
        self._configure_logging(verbose)

        # Only show status message when not in JSON mode
        console = Console()
        if not json:
            console.print(f"[bold]Searching You.com[/bold]: {query}")

        results = await you(
            query=query,
            num_results=num_results,
            country=country,
            language=language,
            safe_search=safe_search,
            time_frame=time_frame,
            api_key=api_key,
            **kwargs,
        )

        processed_results = self._process_results(results)

        if json:
            self._display_json_results(processed_results)
            # Don't return raw results to avoid double output in json mode
            return []
        else:
            self._display_results(processed_results, verbose)
            return processed_results

    async def you_news(
        self,
        query: str,
        num_results: int = 5,
        country: str | None = None,
        language: str | None = None,
        safe_search: bool | None = True,
        time_frame: str | None = None,
        api_key: str | None = None,
        verbose: bool = False,
        json: bool = False,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """
        Search using You.com News Search.

        Args:
            query: Search query string
            num_results: Number of results to return
            country: Country code
            language: Language code
            safe_search: Whether to enable safe search
            time_frame: Time frame for results
            api_key: API key (otherwise use environment variable)
            verbose: Show detailed output
            json: Return results as JSON
            **kwargs: Additional engine-specific parameters

        Returns:
            List of search results as dictionaries
        """
        self._configure_logging(verbose)

        # Only show status message when not in JSON mode
        console = Console()
        if not json:
            console.print(f"[bold]Searching You.com News[/bold]: {query}")

        results = await you_news(
            query=query,
            num_results=num_results,
            country=country,
            language=language,
            safe_search=safe_search,
            time_frame=time_frame,
            api_key=api_key,
            **kwargs,
        )

        processed_results = self._process_results(results)

        if json:
            self._display_json_results(processed_results)
            # Don't return raw results to avoid double output in json mode
            return []
        else:
            self._display_results(processed_results, verbose)
            return processed_results

    async def duckduckgo(
        self,
        query: str,
        num_results: int = 5,
        country: str | None = None,
        language: str | None = None,
        safe_search: bool | None = True,
        time_frame: str | None = None,
        proxy: str | None = None,
        timeout: int = 10,
        verbose: bool = False,
        json: bool = False,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """
        Search using DuckDuckGo search engine.

        Args:
            query: The search query
            num_results: Maximum number of results to return
            country: Optional country code for regional search (maps to 'region')
            language: Optional language code for localized results
            safe_search: Whether to enable safe search filtering
            time_frame: Optional time range for results (d: day, w: week, m: month, y: year)
            proxy: Optional proxy server to use, supports http/https/socks5
            timeout: Request timeout in seconds
            verbose: Whether to show detailed results
            json: Whether to output in JSON format
            **kwargs: Additional DuckDuckGo-specific parameters

        Returns:
            Search results as dictionaries
        """
        self._configure_logging(verbose)
        self.logger.info(f"🔍 Searching DuckDuckGo for: {query}")

        try:
            # Ensure safe_search is a boolean and not None
            actual_safe_search = True if safe_search is None else bool(safe_search)

            results = await duckduckgo(
                query,
                num_results=num_results,
                country=country,
                language=language,
                safe_search=actual_safe_search,
                time_frame=time_frame,
                proxy=proxy,
                timeout=timeout,
                **kwargs,
            )
            processed_results = self._process_results(results)

            if json:
                self._display_json_results(processed_results)
            else:
                self._display_results(processed_results, verbose)
            return processed_results
        except Exception as e:
            error_msg = f"DuckDuckGo search failed: {e}"
            self.logger.error(f"❌ {error_msg}")
            self._display_errors([error_msg])
            return []


def main() -> None:
    """Entry point for the CLI."""
    fire.Fire(SearchCLI())


if __name__ == "__main__":
    main()
