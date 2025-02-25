#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["fire>=0.5.0", "rich>=13.6.0"]
# ///
# this_file: src/twat_search/__main__.py

"""
Main entry point for the TWAT Search CLI.
"""

import logging
from typing import Any, TypeVar

import fire  # type: ignore
from rich.console import Console
from rich.logging import RichHandler

# Set up logging with rich
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
logger = logging.getLogger(__name__)
console = Console()

# Define types for the CLI components
SearchCLIType = TypeVar("SearchCLIType")


class TwatSearchCLI:
    """TWAT Search Command Line Interface."""

    def __init__(self) -> None:
        """Initialize the TWAT Search CLI."""
        # Try to import the web CLI module
        try:
            from twat_search.web import cli as web_cli

            self.web: Any = web_cli.SearchCLI()
        except (ImportError, AttributeError) as e:
            # Create a placeholder if the web CLI is not available
            logger.error(f"Web CLI not available: {e!s}")
            logger.error("Make sure twat_search.web.cli is properly installed.")
            self.web = self._cli_error

    def _cli_error(self, *args: Any, **kwargs: Any) -> int:  # noqa: ARG002
        """Placeholder function when web CLI is not available.

        Args are ignored but necessary to match any possible call signature.
        """
        console.print(
            "[bold red]Web CLI not available. Make sure twat_search.web.cli is properly installed.[/bold red]"
        )
        return 1

    def version(self) -> str:
        """Display the version of the TWAT Search tool."""
        try:
            from twat_search.__version__ import version

            return f"TWAT Search version {version}"
        except ImportError:
            return "TWAT Search (version not available)"


def main() -> None:
    """Main entry point for the TWAT Search CLI."""
    fire.Fire(TwatSearchCLI(), name="twat-search")


if __name__ == "__main__":
    main()
