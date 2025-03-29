"""
Lifecycle management package for the bot.

This package provides tools for managing the application's lifecycle,
including initialisation, startup, shutdown, and error handling.
"""

from bot.core.lifecycle.manager import (
    LifecycleManager,
    LifecycleState,
    LifecycleError,
    LifecycleHook,
    get_lifecycle_manager,
)
from bot.core.lifecycle.hooks import (
    register_config_hooks,
    register_logging_hooks,
    register_error_hooks,
    register_database_hooks,
    register_platform_hooks,
    register_command_hooks,
    register_feature_hooks,
    register_all_hooks,
)

__all__ = [
    # Lifecycle manager
    "LifecycleManager",
    "LifecycleState",
    "LifecycleError",
    "LifecycleHook",
    "get_lifecycle_manager",

    # Lifecycle hooks
    "register_config_hooks",
    "register_logging_hooks",
    "register_error_hooks",
    "register_database_hooks",
    "register_platform_hooks",
    "register_command_hooks",
    "register_feature_hooks",
    "register_all_hooks",
]
