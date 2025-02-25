#!/usr/bin/env python
# this_file: tests/unit/web/test_config.py

"""
Unit tests for the twat_search.web.config module.

This module tests the configuration classes used for search engine settings.
"""

from pytest import MonkeyPatch

from twat_search.web.config import Config, EngineConfig


def test_engine_config_defaults() -> None:
    """Test EngineConfig with default values."""
    config = EngineConfig()

    assert config.api_key is None
    assert config.enabled is True
    assert config.default_params == {}


def test_engine_config_values() -> None:
    """Test EngineConfig with custom values."""
    config = EngineConfig(
        api_key="test_key",
        enabled=False,
        default_params={"count": 10, "include_domains": ["example.com"]},
    )

    assert config.api_key == "test_key"
    assert config.enabled is False
    assert config.default_params == {"count": 10, "include_domains": ["example.com"]}


def test_config_defaults(isolate_env_vars: None) -> None:
    """Test Config with default values."""
    config = Config()

    assert isinstance(config.engines, dict)
    assert len(config.engines) == 0


def test_config_with_env_vars(
    monkeypatch: MonkeyPatch, env_vars_for_brave: None
) -> None:
    """Test Config loads settings from environment variables."""
    # Create config
    config = Config()

    # Check the brave engine was configured
    assert "brave" in config.engines
    brave_config = config.engines["brave"]
    assert brave_config.api_key == "test_brave_key"
    assert brave_config.enabled is True
    assert brave_config.default_params == {"count": 10}


def test_config_with_direct_initialization() -> None:
    """Test Config can be initialized directly with engines."""
    custom_config = Config(
        engines={
            "test_engine": EngineConfig(
                api_key="direct_key", enabled=True, default_params={"count": 5}
            )
        }
    )

    assert "test_engine" in custom_config.engines
    assert custom_config.engines["test_engine"].api_key == "direct_key"
    assert custom_config.engines["test_engine"].default_params == {"count": 5}


def test_config_env_vars_override_direct_config(monkeypatch: MonkeyPatch) -> None:
    """Test environment variables do not override direct config."""
    # Set environment variables
    monkeypatch.setenv("BRAVE_API_KEY", "env_key")

    # Create config with direct values (should take precedence)
    custom_config = Config(
        engines={
            "brave": EngineConfig(
                api_key="direct_key", enabled=True, default_params={"count": 5}
            )
        }
    )

    # Check that direct config was not overridden
    assert custom_config.engines["brave"].api_key == "direct_key"
