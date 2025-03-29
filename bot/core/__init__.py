"""
Core package for the bot.

This package provides essential system components with well-defined responsibilities,
including configuration management, logging, error handling, and lifecycle management.
"""

from bot.core.constants import (
    PROJECT_ROOT,
    DATA_DIR,
    LOGS_DIR,
    CONFIG_DIR,
    DEFAULT_ENV_FILE,
    DEFAULT_CONFIG,
    DB_SCHEMA_FILE,
    TWITCH_API_BASE_URL,
    TWITCH_AUTH_URL,
    FEATURES,
    USER_RANKS,
    DEFAULT_COMMAND_COOLDOWN,
    DEFAULT_GLOBAL_COOLDOWN,
    POINTS_PER_MESSAGE,
    POINTS_PER_MINUTE,
    POINTS_PER_BIT,
)
from bot.core.errors import (
    BotError,
    ConfigError,
    DatabaseError,
    CommandError,
    PlatformError,
    TwitchError,
    OBSError,
    DiscordError,
    FeatureError,
    ValidationError,
    ErrorContext,
    ErrorHandler,
    get_error_handler,
    register_default_handlers,
    get_traceback_str,
    try_except_decorator,
)

__all__ = [
    # Constants
    "PROJECT_ROOT",
    "DATA_DIR",
    "LOGS_DIR",
    "CONFIG_DIR",
    "DEFAULT_ENV_FILE",
    "DEFAULT_CONFIG",
    "DB_SCHEMA_FILE",
    "TWITCH_API_BASE_URL",
    "TWITCH_AUTH_URL",
    "FEATURES",
    "USER_RANKS",
    "DEFAULT_COMMAND_COOLDOWN",
    "DEFAULT_GLOBAL_COOLDOWN",
    "POINTS_PER_MESSAGE",
    "POINTS_PER_MINUTE",
    "POINTS_PER_BIT",

    # Error handling
    "BotError",
    "ConfigError",
    "DatabaseError",
    "CommandError",
    "PlatformError",
    "TwitchError",
    "OBSError",
    "DiscordError",
    "FeatureError",
    "ValidationError",
    "ErrorContext",
    "ErrorHandler",
    "get_error_handler",
    "register_default_handlers",
    "get_traceback_str",
    "try_except_decorator",
]
