# this_file: src/twat_search/web/config.py

"""
Configuration for the web search API.

This module defines configuration classes for the web search API, including
settings for each search engine and loading environment variables.
"""

import json
import os
from typing import Any

# Load environment variables from .env file
try:
    from dotenv import load_dotenv

    load_dotenv()  # Load variables from .env file into environment
except ImportError:
    # python-dotenv is optional
    pass

from pydantic import BaseModel, Field


class EngineConfig(BaseModel):
    """Configuration for a single search engine."""

    api_key: str | None = None
    enabled: bool = True
    default_params: dict[str, Any] = Field(default_factory=dict)


class Config:
    """
    Configuration for the web search API.

    Loads settings from environment variables for registered engines.
    """

    def __init__(self, **kwargs: Any) -> None:
        """Initialize with engine configurations from environment variables."""
        # Initialize with empty engines dict or use provided
        self.engines: dict[str, EngineConfig] = kwargs.get("engines", {})

        # Skip auto-loading if we already have engines configured (from kwargs)
        if not self.engines:
            # Process environment variables
            self._load_engine_configs()

    def _load_engine_configs(self) -> None:
        """
        Load engine configurations from environment variables.

        This method only loads configurations for engines that are registered in
        the system, to prevent creating configurations for non-existent engines.

        For tests that need an empty configuration, set _TEST_ENGINE env var.
        """
        # Import here to avoid circular imports
        try:
            from .engines.base import get_registered_engines

            registered_engines = get_registered_engines()
        except ImportError:
            # If engines module isn't loaded yet, use empty dict
            registered_engines = {}

        # Handle empty case for tests
        if "_TEST_ENGINE" in os.environ:
            # Skip loading for tests
            return

        # First load from environment file patterns for each engine
        engine_settings: dict[str, dict[str, Any]] = {}

        # Process registered engines specifically
        for engine_name, engine_class in registered_engines.items():
            if engine_name not in engine_settings:
                engine_settings[engine_name] = {}

            # Check API key environment variables (specific names from engine class)
            for env_name in engine_class.env_api_key_names:
                api_key = os.environ.get(env_name)
                if api_key:
                    engine_settings[engine_name]["api_key"] = api_key
                    break

            # Check enabled environment variables (specific names from engine class)
            for env_name in engine_class.env_enabled_names:
                enabled = os.environ.get(env_name)
                if enabled is not None:
                    engine_settings[engine_name]["enabled"] = enabled.lower() in (
                        "true",
                        "1",
                        "yes",
                    )
                    break

            # Check default params environment variables (specific names from engine class)
            for env_name in engine_class.env_params_names:
                params = os.environ.get(env_name)
                if params:
                    try:
                        engine_settings[engine_name]["default_params"] = json.loads(
                            params
                        )
                    except json.JSONDecodeError:
                        # If JSON parsing fails, use an empty dict
                        engine_settings[engine_name]["default_params"] = {}
                    break

        # Now create or update EngineConfig objects
        for engine_name, settings in engine_settings.items():
            if engine_name in self.engines:
                # Update existing config with new values
                existing_config = self.engines[engine_name]
                for key, value in settings.items():
                    setattr(existing_config, key, value)
            else:
                # Create new config
                self.engines[engine_name] = EngineConfig(**settings)
