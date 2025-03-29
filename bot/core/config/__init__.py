"""
Configuration management package for the bot.

This package provides tools for loading, validating, and accessing configuration
settings from various sources including environment variables and .env files.
"""

from bot.core.config.config import (
    ConfigManager,
    ConfigError,
    ConfigValidationError,
    ConfigNotFoundError,
    get_config,
)
from bot.core.config.validators import (
    validate_required,
    validate_pattern,
    validate_in_list,
    validate_range,
    validate_url,
    validate_path_exists,
    validate_port,
    validate_type,
    validate_enum,
    apply_validator,
    validate_config,
)

__all__ = [
    # Config manager
    "ConfigManager",
    "get_config",

    # Exceptions
    "ConfigError",
    "ConfigValidationError",
    "ConfigNotFoundError",

    # Validators
    "validate_required",
    "validate_pattern",
    "validate_in_list",
    "validate_range",
    "validate_url",
    "validate_path_exists",
    "validate_port",
    "validate_type",
    "validate_enum",
    "apply_validator",
    "validate_config",
]
