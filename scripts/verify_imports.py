#!/usr/bin/env python3
"""
Import verification script for the bot packages.

This script verifies that all exported components from the packages can be
properly imported. It helps catch issues with __init__.py files, such as
missing exports or circular imports.

Usage:
    python scripts/verify_imports.py
"""

import importlib
import sys
from typing import Dict, List, Set, Tuple, Optional
import os

# Add the project root to the Python path if needed
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)


def check_imports(module_path: str) -> Tuple[bool, Optional[str]]:
    """
    Check if a module can be imported.

    Args:
        module_path (str): Dot-notation path to the module to import.

    Returns:
        Tuple[bool, Optional[str]]: (success, error_message)
    """
    try:
        module = importlib.import_module(module_path)
        return True, None
    except ImportError as e:
        return False, str(e)
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"


def check_attribute(module_path: str, attribute: str) -> Tuple[bool, Optional[str]]:
    """
    Check if an attribute can be accessed from a module.

    Args:
        module_path (str): Dot-notation path to the module.
        attribute (str): Attribute to access.

    Returns:
        Tuple[bool, Optional[str]]: (success, error_message)
    """
    try:
        module = importlib.import_module(module_path)
        getattr(module, attribute)
        return True, None
    except ImportError as e:
        return False, f"Import error: {str(e)}"
    except AttributeError as e:
        return False, f"Attribute error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"


def verify_package(package_path: str, attributes: List[str]) -> List[Tuple[str, bool, Optional[str]]]:
    """
    Verify that all attributes can be imported from a package.

    Args:
        package_path (str): Dot-notation path to the package.
        attributes (List[str]): List of attributes to check.

    Returns:
        List[Tuple[str, bool, Optional[str]]]: List of (attribute, success, error_message)
    """
    results = []

    # First check if the package itself can be imported
    package_success, package_error = check_imports(package_path)
    results.append((package_path, package_success, package_error))

    if not package_success:
        # If the package can't be imported, don't check attributes
        return results

    # Check each attribute
    for attr in attributes:
        attr_success, attr_error = check_attribute(package_path, attr)
        results.append((f"{package_path}.{attr}", attr_success, attr_error))

    return results


def display_results(results: List[Tuple[str, bool, Optional[str]]]) -> bool:
    """
    Display verification results.

    Args:
        results (List[Tuple[str, bool, Optional[str]]]): List of (item, success, error_message)

    Returns:
        bool: True if all checks passed, False otherwise.
    """
    success_count = 0
    failure_count = 0

    for item, success, error in results:
        if success:
            print(f"✅ {item}")
            success_count += 1
        else:
            print(f"❌ {item}: {error}")
            failure_count += 1

    print(f"\nResults: {success_count} successful, {failure_count} failed")
    return failure_count == 0


def main() -> int:
    """
    Main function that verifies imports for all packages.

    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    print("Verifying imports for bot packages...\n")

    all_results = []

    # Core package
    core_attrs = [
        "PROJECT_ROOT", "DATA_DIR", "LOGS_DIR", "CONFIG_DIR",
        "DEFAULT_ENV_FILE", "DEFAULT_CONFIG", "DB_SCHEMA_FILE",
        "TWITCH_API_BASE_URL", "TWITCH_AUTH_URL", "FEATURES",
        "USER_RANKS", "DEFAULT_COMMAND_COOLDOWN", "DEFAULT_GLOBAL_COOLDOWN",
        "POINTS_PER_MESSAGE", "POINTS_PER_MINUTE", "POINTS_PER_BIT",
        "BotError", "ConfigError", "DatabaseError", "CommandError",
        "PlatformError", "TwitchError", "OBSError", "DiscordError",
        "FeatureError", "ValidationError", "ErrorContext", "ErrorHandler",
        "get_error_handler", "register_default_handlers", "get_traceback_str",
        "try_except_decorator"
    ]
    all_results.extend(verify_package("bot.core", core_attrs))

    # Config package
    config_attrs = [
        "ConfigManager", "get_config", "ConfigError", "ConfigValidationError",
        "ConfigNotFoundError", "validate_required", "validate_pattern",
        "validate_in_list", "validate_range", "validate_url",
        "validate_path_exists", "validate_port", "validate_type",
        "validate_enum", "apply_validator", "validate_config"
    ]
    all_results.extend(verify_package("bot.core.config", config_attrs))

    # Events package
    events_attrs = [
        "Event", "EventType", "EventPriority", "EventHandler", "EventFilter",
        "EventError", "EventHandlerError", "EventFilterError",
        "CoreEventType", "CoreEvent", "ErrorEvent",
        "EventDispatcher", "get_event_dispatcher",
        "EventRegistry", "EventRegistryError", "get_event_registry",
        "LoggingEventHandler", "ErrorEventHandler", "LifecycleEventHandler",
        "register_global_handlers", "initialise_event_system", "shutdown_event_system"
    ]
    all_results.extend(verify_package("bot.core.events", events_attrs))

    # Lifecycle package
    lifecycle_attrs = [
        "LifecycleManager", "LifecycleState", "LifecycleError", "LifecycleHook",
        "get_lifecycle_manager", "register_config_hooks", "register_logging_hooks",
        "register_error_hooks", "register_database_hooks", "register_platform_hooks",
        "register_command_hooks", "register_feature_hooks", "register_all_hooks"
    ]
    all_results.extend(verify_package("bot.core.lifecycle", lifecycle_attrs))

    # Utils package
    utils_attrs = [
        # Time utilities
        "get_utc_now", "to_utc", "format_datetime", "parse_datetime",
        "format_duration", "parse_duration", "time_until", "time_since",
        "format_relative_time", "is_same_day", "add_time", "format_timestamp",
        "get_date_range",

        # Security utilities
        "generate_random_string", "generate_token", "hash_password",
        "verify_password", "generate_hmac", "verify_hmac", "sanitise_input",
        "sanitise_filename", "sanitise_path", "is_safe_url",
        "is_valid_twitch_username", "is_safe_command", "validate_twitch_token",
        "encrypt_string", "decrypt_string",

        # Formatting utilities
        "format_number", "format_currency", "pluralise", "truncate",
        "format_list", "clean_text", "capitalise_first", "capitalise_words",
        "format_twitch_message", "format_twitch_command", "format_time_elapsed",
        "format_timestamp_for_humans", "format_bytes", "strip_html_tags",
        "escape_markdown", "format_exception", "format_json"
    ]
    all_results.extend(verify_package("bot.utils", utils_attrs))

    # Display all results
    print("\nSummary of import verification:")
    all_success = display_results(all_results)

    return 0 if all_success else 1


if __name__ == "__main__":
    sys.exit(main())
