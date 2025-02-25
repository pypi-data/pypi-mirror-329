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
    is_engine_available,
    get_engine_function,
    get_available_engines,
)

if TYPE_CHECKING:
    from twat_search.web.config import Config


# Custom JSON encoder that handles non-serializable objects
class CustomJSONEncoder(json_lib.JSONEncoder):
    """Custom JSON encoder that converts non-serializable objects to strings."""

    def default(self, o: Any) -> Any:
        try:
            return json_lib.JSONEncoder.default(self, o)
        except TypeError:
            return str(o)


# Set up console
console = Console()


class SearchCLI:
    """
    Command-line interface for web search functionality.

    This class provides a CLI wrapper around the search API, with commands
    for searching, listing available engines, and getting engine information.
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger("twat_search.cli")
        self.log_handler = RichHandler(rich_tracebacks=True)
        self._configure_logging()
        self.console = Console()

        all_possible_engines = [
            "brave",
            "brave_news",
            "serpapi",
            "tavily",
            "pplx",
            "you",
            "you_news",
            "critique",
            "duckduckgo",
            "bing_scraper",
            "hasdata-google",
            "hasdata-google-light",
        ]
        available_engines = get_available_engines()
        missing_engines = [
            engine for engine in all_possible_engines if engine not in available_engines
        ]
        if missing_engines:
            self.logger.warning(
                f"The following engines are not available due to missing dependencies: "
                f"{', '.join(missing_engines)}. "
                f"Install the relevant optional dependencies to use them."
            )

    def _configure_logging(self, verbose: bool = False) -> None:
        """Configure the logging level based on the verbose flag."""
        # When not in verbose mode, silence almost all logs
        level = logging.DEBUG if verbose else logging.CRITICAL

        # Configure the root logger
        logging.basicConfig(
            level=level,
            format="%(message)s",
            handlers=[self.log_handler],
            force=True,
        )

        # Set levels for specific loggers
        self.logger.setLevel(level)

        # Also set levels for other loggers used in the system
        logging.getLogger("twat_search.web.api").setLevel(level)
        logging.getLogger("twat_search.web.engines").setLevel(level)
        logging.getLogger("httpx").setLevel(level)

    def _parse_engines(self, engines_arg: Any) -> list[str] | None:
        if engines_arg is None:
            return None
        if isinstance(engines_arg, str):
            return [e.strip() for e in engines_arg.split(",") if e.strip()]
        if isinstance(engines_arg, list | tuple):
            return [str(e).strip() for e in engines_arg if str(e).strip()]
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
        if engines:
            available = []
            for engine in engines:
                if engine == "all" or is_engine_available(engine):
                    available.append(engine)
                else:
                    self.logger.warning(
                        f"Engine '{engine}' is not available. The dependency may not be installed."
                    )
            engines = available or None

        # Add debug print to see what engines are being used
        if self.logger.level <= logging.DEBUG:
            self.logger.debug(f"Attempting to search with engines: {engines}")

        try:
            results = await search(query=query, engines=engines, **kwargs)
            return self._process_results(results)
        except Exception as e:
            self.logger.error(f"Search failed: {e}")
            self._display_errors([str(e)])
            return []

    def _process_results(self, results: list) -> list[dict[str, Any]]:
        processed = []
        engine_results: dict[str, list] = {}

        # Group results by engine
        for result in results:
            engine_name = getattr(result, "source", None) or "unknown"
            engine_results.setdefault(engine_name, []).append(result)

        # Process all results from each engine
        for engine, engine_results_list in engine_results.items():
            if not engine_results_list:
                processed.append(
                    {
                        "engine": engine,
                        "status": "❌ No results",
                        "url": "N/A",
                        "title": "N/A",
                        "snippet": "N/A",
                        "raw_result": None,
                        "is_first": True,  # Flag to help with UI rendering
                    }
                )
                continue

            # Process all results for the engine, not just the first one
            for idx, result in enumerate(engine_results_list):
                url = str(result.url)
                processed.append(
                    {
                        "engine": engine,
                        "status": "✅ Success",
                        "url": url,
                        "title": result.title,
                        "snippet": result.snippet[:100] + "..."
                        if len(result.snippet) > 100
                        else result.snippet,
                        "raw_result": getattr(result, "raw", None),
                        "is_first": idx == 0,  # Flag to help with UI rendering
                    }
                )
        return processed

    def _display_results(
        self, processed_results: list[dict[str, Any]], verbose: bool = False
    ) -> None:
        if not processed_results:
            console.print("[bold red]No results found![/bold red]")
            return

        # Always use the compact table format unless verbose is specifically requested
        table = Table()  # Remove show_lines=True to eliminate row separator lines
        table.add_column("Engine", style="cyan", no_wrap=True)

        if verbose:
            table.add_column("Status", style="magenta")
            table.add_column("Title", style="green")
            table.add_column("URL", style="blue", overflow="fold")
            for result in processed_results:
                # Only show engine name for the first result of each engine
                engine_display = result["engine"] if result["is_first"] else ""
                table.add_row(
                    engine_display, result["status"], result["title"], result["url"]
                )
        else:
            # Set the URL column to wrap, with enough width to display most URLs
            table.add_column("URL", style="blue", overflow="fold", max_width=70)
            for result in processed_results:
                if "❌" in result["status"]:
                    continue
                table.add_row(result["engine"], result["url"])

        console.print(table)

        # Only print the raw results when verbose is true
        if verbose:
            for result in processed_results:
                if "❌" not in result["status"]:
                    console.print(result)

    def _display_json_results(self, processed_results: list[dict[str, Any]]) -> None:
        """Format and print results as JSON."""
        results_by_engine: dict[str, dict[str, list[dict[str, Any]]]] = {}

        # Group results by engine
        for result in processed_results:
            engine = result["engine"]

            # Initialize engine results list if it doesn't exist
            if engine not in results_by_engine:
                results_by_engine[engine] = {"results": []}

            # Skip error results
            if "❌" in result["status"]:
                continue

            # Add the current result to the engine's results list
            results_by_engine[engine]["results"].append(
                {
                    "url": result["url"] if result["url"] != "N/A" else None,
                    "title": result["title"] if result["title"] != "N/A" else None,
                    "snippet": result.get("snippet")
                    if result.get("snippet") != "N/A"
                    else None,
                    "raw": result.get("raw_result"),
                }
            )

        # Print the JSON output

    def _display_errors(self, error_messages: list[str]) -> None:
        if not error_messages:
            return
        table = Table(title="❌ Search Errors")
        table.add_column("Error", style="red")
        for error in error_messages:
            table.add_row(error)
        console.print(table)

    async def _search_engine(
        self, engine: str, query: str, params: dict, json: bool, verbose: bool
    ) -> list[dict[str, Any]]:
        """
        Execute a search with a specific engine.

        Args:
            engine: Name of the engine to use
            query: Search query
            params: Parameters for the engine
            json: Whether to format output as JSON
            verbose: Whether to display verbose output
        """
        self._configure_logging(verbose)

        if not is_engine_available(engine):
            error_msg = f"{engine.capitalize()} search engine is not available. Make sure the required dependency is installed."
            self.logger.error(error_msg)
            self._display_errors([error_msg])
            return []

        engine_func = get_engine_function(engine)
        if engine_func is None:
            error_msg = (
                f"{engine.capitalize()} search engine function could not be loaded."
            )
            self.logger.error(error_msg)
            self._display_errors([error_msg])
            return []

        friendly_names = {
            "brave": "Brave",
            "brave_news": "Brave News",
            "serpapi": "SerpAPI (Google)",
            "tavily": "Tavily AI",
            "pplx": "Perplexity AI",
            "you": "You.com",
            "you_news": "You.com News",
            "critique": "Critique",
            "duckduckgo": "DuckDuckGo",
            "hasdata-google": "HasData Google",
            "hasdata-google-light": "HasData Google Light",
        }
        friendly = friendly_names.get(engine, engine)
        if not json:
            self.console.print(f"[bold]Searching {friendly}[/bold]: {query}")
        try:
            results = await engine_func(query=query, **params)
            processed_results = self._process_results(results)
            if json:
                self._display_json_results(processed_results)
                return []
            else:
                self._display_results(processed_results, verbose)
                return processed_results
        except Exception as e:
            self.logger.error(f"{friendly} search failed: {e}")
            self._display_errors([str(e)])
            return []

    def q(
        self,
        query: str,
        engines: str | list[str] | None = None,
        engine: str | None = None,  # Add alias for --engine/-e
        e: str | None = None,  # Add alias for -e
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
        Search the web using one or more search engines.

        Args:
            query: The search query
            engines: List of engines to use (comma-separated string or list)
            engine: Alias for engines (--engine flag)
            e: Alias for engines (-e flag)
            num_results: Number of results to return per engine
            country: Country code for regional results
            language: Language code for results
            safe_search: Whether to enable safe search filtering
            time_frame: Time frame for results (e.g., "day", "week", "month")
            verbose: Whether to display verbose output
            json: Whether to return results as JSON
            **kwargs: Additional engine-specific parameters

        Returns:
            List of search results (empty in JSON mode)
        """
        self._configure_logging(verbose)

        # Process engine flags - prioritize them in this order
        if e is not None:
            engines = e
        if engine is not None:
            engines = engine

        engine_list = self._parse_engines(engines)

        common_params = {
            "num_results": num_results,
            "country": country,
            "language": language,
            "safe_search": safe_search,
            "time_frame": time_frame,
        }
        common_params = {k: v for k, v in common_params.items() if v is not None}

        if json:
            results = asyncio.run(
                self._run_search(query, engine_list, **common_params, **kwargs)
            )
        else:
            with self.console.status(
                f"[bold green]Searching for '{query}'...[/bold green]"
            ):
                results = asyncio.run(
                    self._run_search(query, engine_list, **common_params, **kwargs)
                )

        if json:
            self._display_json_results(results)
            return []
        else:
            self._display_results(results, verbose)
            # Only return the actual results if verbose mode is enabled
            # This prevents the CLI from printing the raw results
            if verbose:
                return results
            return []

    def info(self, engine: str | None = None, json: bool = False) -> None:
        try:
            from twat_search.web.config import Config

            config = Config()
            if json:
                self._display_engines_json(engine, config)
            elif engine is None:
                self._list_all_engines(config)
            else:
                self._show_engine_details(engine, config)
        except Exception as e:
            if not json:
                self.logger.error(f"❌ Failed to display engine information: {e}")

    def _list_all_engines(self, config: "Config") -> None:
        table = Table(title="🔎 Available Search Engines")
        table.add_column("Engine", style="cyan", no_wrap=True)
        table.add_column("Enabled", style="magenta")
        table.add_column("API Key Required", style="yellow")
        try:
            from twat_search.web.engines.base import get_registered_engines

            registered_engines = get_registered_engines()
        except ImportError:
            registered_engines = {}
        for engine, engine_config in config.engines.items():
            api_key_required = (
                hasattr(engine_config, "api_key") and engine_config.api_key is not None
            )
            if not api_key_required and engine in registered_engines:
                engine_class = registered_engines.get(engine)
                if engine_class and hasattr(engine_class, "env_api_key_names"):
                    api_key_required = bool(engine_class.env_api_key_names)
            table.add_row(
                engine,
                "✅" if engine_config.enabled else "❌",
                "✅" if api_key_required else "❌",
            )
        self.console.print(table)
        self.console.print(
            "\n[italic]Run 'info ENGINE_NAME' for more details about a specific engine.[/italic]"
        )

    def _show_engine_details(self, engine_name: str, config: "Config") -> None:
        if engine_name not in config.engines:
            self.console.print(
                f"[bold red]Engine '{engine_name}' not found![/bold red]"
            )
            self.console.print("\nAvailable engines:")
            for name in config.engines:
                self.console.print(f"- {name}")
            return
        engine_config = config.engines[engine_name]
        api_key_required = (
            hasattr(engine_config, "api_key") and engine_config.api_key is not None
        )
        try:
            from twat_search.web.engines.base import get_registered_engines

            registered_engines = get_registered_engines()
            engine_class = registered_engines.get(engine_name)
            if (
                not api_key_required
                and engine_class
                and hasattr(engine_class, "env_api_key_names")
            ):
                api_key_required = bool(engine_class.env_api_key_names)
            self.console.print(f"\n[bold cyan]🔍 Engine: {engine_name}[/bold cyan]")
            self.console.print(
                f"[bold]Enabled:[/bold] {'✅' if engine_config.enabled else '❌'}"
            )
            self.console.print(
                f"[bold]API Key Required:[/bold] {'✅' if api_key_required else '❌'}"
            )
            if engine_class and hasattr(engine_class, "env_api_key_names"):
                self.console.print("\n[bold]API Key Environment Variables:[/bold]")
                for env_name in engine_class.env_api_key_names:
                    value_status = "✅" if os.environ.get(env_name) else "❌"
                    self.console.print(f"  {env_name}: {value_status}")
            self.console.print("\n[bold]Default Parameters:[/bold]")
            if engine_config.default_params:
                for param, value in engine_config.default_params.items():
                    self.console.print(f"  {param}: {value}")
            else:
                self.console.print("  No default parameters specified")
            try:
                base_engine = engine_name.split("-")[0]
                module_name = f"twat_search.web.engines.{base_engine}"
                import importlib

                engine_module = importlib.import_module(module_name)
                function_name = engine_name.replace("-", "_")
                if hasattr(engine_module, function_name):
                    func = getattr(engine_module, function_name)
                    self.console.print("\n[bold]Function Interface:[/bold]")
                    self.console.print(
                        f"  [green]{function_name}()[/green] - {func.__doc__.strip().split('\\n')[0]}"
                    )
                    self.console.print("\n[bold]Example Usage:[/bold]")
                    self.console.print(
                        f"  [italic]from {module_name} import {function_name}[/italic]"
                    )
                    self.console.print(
                        f'  [italic]results = await {function_name}("your search query")[/italic]'
                    )
            except (ImportError, AttributeError, IndexError):
                pass
        except (ImportError, AttributeError) as e:
            self.console.print(
                f"[bold yellow]Could not load detailed engine information: {e}[/bold yellow]"
            )
            self.console.print("\n[bold]Basic Configuration:[/bold]")
            self.console.print(f"Enabled: {'✅' if engine_config.enabled else '❌'}")
            self.console.print(
                f"Has API Key: {'✅' if engine_config.api_key else '❌'}"
            )
            self.console.print(f"Default Parameters: {engine_config.default_params}")

    def _display_engines_json(self, engine: str | None, config: "Config") -> None:
        from twat_search.web.engines.base import get_registered_engines

        try:
            registered_engines = get_registered_engines()
        except ImportError:
            registered_engines = {}
        result = {}
        if engine:
            if engine not in config.engines:
                return
            engine_config = config.engines[engine]
            result[engine] = self._get_engine_info(
                engine, engine_config, registered_engines
            )
        else:
            for engine_name, engine_config in config.engines.items():
                result[engine_name] = self._get_engine_info(
                    engine_name, engine_config, registered_engines
                )
        # JSON output (omitted actual printing for brevity)

    def _get_engine_info(
        self, engine_name: str, engine_config: Any, registered_engines: dict
    ) -> dict:
        api_key_required = False
        api_key_set = False
        env_vars = []
        if hasattr(engine_config, "api_key") and engine_config.api_key is not None:
            api_key_required = True
            api_key_set = True
        if engine_name in registered_engines:
            engine_class = registered_engines.get(engine_name)
            if engine_class and hasattr(engine_class, "env_api_key_names"):
                api_key_required = bool(engine_class.env_api_key_names)
                env_vars = [
                    {"name": env_name, "set": bool(os.environ.get(env_name))}
                    for env_name in engine_class.env_api_key_names
                ]
        default_params = (
            engine_config.default_params
            if hasattr(engine_config, "default_params")
            else {}
        )
        return {
            "enabled": engine_config.enabled
            if hasattr(engine_config, "enabled")
            else False,
            "api_key_required": api_key_required,
            "api_key_set": api_key_set,
            "env_vars": env_vars,
            "default_params": default_params,
        }

    def _check_engine_availability(self, engine_name: str) -> bool:
        return is_engine_available(engine_name)

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
        params: dict[str, Any] = {
            "num_results": num_results,
            "country": country,
            "language": language,
            "safe_search": safe_search,
            "time_frame": time_frame,
        }
        if api_key:
            params["api_key"] = api_key
        if image_url:
            params["image_url"] = image_url
        if image_base64:
            params["image_base64"] = image_base64
        if source_whitelist:
            params["source_whitelist"] = [
                s.strip() for s in source_whitelist.split(",") if s.strip()
            ]
        if source_blacklist:
            params["source_blacklist"] = [
                s.strip() for s in source_blacklist.split(",") if s.strip()
            ]
        params.update(kwargs)
        params = {k: v for k, v in params.items() if v is not None}
        return await self._search_engine("critique", query, params, json, verbose)

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
        params = {
            "num_results": num_results,
            "country": country,
            "language": language,
            "safe_search": safe_search,
            "time_frame": time_frame,
        }
        if api_key:
            params["api_key"] = api_key
        params.update(kwargs)
        params = {k: v for k, v in params.items() if v is not None}
        return await self._search_engine("brave", query, params, json, verbose)

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
        params = {
            "num_results": num_results,
            "country": country,
            "language": language,
            "safe_search": safe_search,
            "time_frame": time_frame,
        }
        if api_key:
            params["api_key"] = api_key
        params.update(kwargs)
        params = {k: v for k, v in params.items() if v is not None}
        return await self._search_engine("brave_news", query, params, json, verbose)

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
        params = {
            "num_results": num_results,
            "country": country,
            "language": language,
            "safe_search": safe_search,
            "time_frame": time_frame,
        }
        if api_key:
            params["api_key"] = api_key
        params.update(kwargs)
        params = {k: v for k, v in params.items() if v is not None}
        return await self._search_engine("serpapi", query, params, json, verbose)

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
        params: dict[str, Any] = {
            "num_results": num_results,
            "country": country,
            "language": language,
            "safe_search": safe_search,
            "time_frame": time_frame,
            "api_key": api_key,
            "search_depth": search_depth,
        }
        if include_domains:
            params["include_domains"] = [
                s.strip() for s in include_domains.split(",") if s.strip()
            ]
        if exclude_domains:
            params["exclude_domains"] = [
                s.strip() for s in exclude_domains.split(",") if s.strip()
            ]
        params.update(kwargs)
        params = {k: v for k, v in params.items() if v is not None}
        return await self._search_engine("tavily", query, params, json, verbose)

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
        params = {
            "num_results": num_results,
            "country": country,
            "language": language,
            "safe_search": safe_search,
            "time_frame": time_frame,
            "api_key": api_key,
            "model": model,
        }
        params.update(kwargs)
        params = {k: v for k, v in params.items() if v is not None}
        return await self._search_engine("pplx", query, params, json, verbose)

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
        params = {
            "num_results": num_results,
            "country": country,
            "language": language,
            "safe_search": safe_search,
            "time_frame": time_frame,
            "api_key": api_key,
        }
        params.update(kwargs)
        params = {k: v for k, v in params.items() if v is not None}
        return await self._search_engine("you", query, params, json, verbose)

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
        params = {
            "num_results": num_results,
            "country": country,
            "language": language,
            "safe_search": safe_search,
            "time_frame": time_frame,
            "api_key": api_key,
        }
        params.update(kwargs)
        params = {k: v for k, v in params.items() if v is not None}
        return await self._search_engine("you_news", query, params, json, verbose)

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
        params = {
            "num_results": num_results,
            "region": country,  # remap country -> region
            "safesearch": safe_search,  # remap safe_search -> safesearch
            "time_range": time_frame,  # remap time_frame -> time_range
            "proxy": proxy,
            "timeout": timeout,
        }
        params.update(kwargs)
        params = {k: v for k, v in params.items() if v is not None}
        return await self._search_engine("duckduckgo", query, params, json, verbose)

    async def hasdata_google(
        self,
        query: str,
        num_results: int = 5,
        location: str | None = None,
        device_type: str = "desktop",
        api_key: str | None = None,
        verbose: bool = False,
        json: bool = False,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """
        Search using HasData Google SERP API.

        Args:
            query: Search query string
            num_results: Number of results to return
            location: Location for search (e.g., "Austin,Texas,United States")
            device_type: Device type for search (desktop or mobile)
            api_key: API key to use (overrides environment variable)
            verbose: Whether to display verbose output
            json: Whether to format output as JSON
        """
        params = {
            "num_results": num_results,
            "location": location,
            "device_type": device_type,
            "api_key": api_key,
        }
        params.update(kwargs)
        params = {k: v for k, v in params.items() if v is not None}
        return await self._search_engine("hasdata-google", query, params, json, verbose)

    async def hasdata_google_light(
        self,
        query: str,
        num_results: int = 5,
        location: str | None = None,
        api_key: str | None = None,
        verbose: bool = False,
        json: bool = False,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """
        Search using HasData Google SERP Light API.

        Args:
            query: Search query string
            num_results: Number of results to return
            location: Location for search (e.g., "Austin,Texas,United States")
            api_key: API key to use (overrides environment variable)
            verbose: Whether to display verbose output
            json: Whether to format output as JSON
        """
        params = {
            "num_results": num_results,
            "location": location,
            "api_key": api_key,
        }
        params.update(kwargs)
        params = {k: v for k, v in params.items() if v is not None}
        return await self._search_engine(
            "hasdata-google-light", query, params, json, verbose
        )


def main() -> None:
    fire.Fire(SearchCLI())


if __name__ == "__main__":
    main()
