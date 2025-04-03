#!/usr/bin/env python3
"""
Import verification script for the bot packages.

This script verifies:
1. That all exported components from the packages can be properly imported
2. That all functions/classes defined in a module are properly exported in its __init__.py

Usage:
    python scripts/verify_imports.py
"""

import ast
import importlib
import sys
import inspect
import os
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any, Union, NamedTuple

# Add the project root to the Python path if needed
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)


class FunctionDefinition(NamedTuple):
    """Represents a function definition in a module."""
    name: str
    is_public: bool  # True if not starting with _


class ClassDefinition(NamedTuple):
    """Represents a class definition in a module."""
    name: str
    is_public: bool  # True if not starting with _


class ModuleDefinition(NamedTuple):
    """Represents all definitions in a module."""
    functions: List[FunctionDefinition]
    classes: List[ClassDefinition]


class VerificationResult(NamedTuple):
    """Represents the verification result for a module."""
    name: str  # Module path or name
    result_type: str  # 'function', 'class', 'module', 'attribute'
    exists: bool  # Whether it exists/can be imported
    error: Optional[str]  # Error message if not exists


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


def verify_package(package_path: str, attributes: List[str]) -> List[VerificationResult]:
    """
    Verify that all attributes can be imported from a package.

    Args:
        package_path (str): Dot-notation path to the package.
        attributes (List[str]): List of attributes to check.

    Returns:
        List[VerificationResult]: List of verification results.
    """
    results = []

    # First check if the package itself can be imported
    package_success, package_error = check_imports(package_path)
    results.append(VerificationResult(
        name=package_path,
        result_type="module",
        exists=package_success,
        error=package_error
    ))

    if not package_success:
        # If the package can't be imported, don't check attributes
        return results

    # Check each attribute
    for attr in attributes:
        attr_success, attr_error = check_attribute(package_path, attr)
        results.append(VerificationResult(
            name=f"{package_path}.{attr}",
            result_type="attribute",
            exists=attr_success,
            error=attr_error
        ))

    return results


def parse_module_definitions(file_path: str) -> ModuleDefinition:
    """
    Parse a Python file and extract all function and class definitions.

    Args:
        file_path (str): Path to the Python file.

    Returns:
        ModuleDefinition: Object containing the functions and classes.

    Raises:
        Exception: If the file cannot be parsed.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    try:
        module = ast.parse(content)
        functions = []
        classes = []

        # Find all function and class definitions
        for node in ast.walk(module):
            if isinstance(node, ast.FunctionDef):
                is_public = not node.name.startswith("_")
                functions.append(FunctionDefinition(
                    name=node.name, is_public=is_public))
            elif isinstance(node, ast.ClassDef):
                is_public = not node.name.startswith("_")
                classes.append(ClassDefinition(
                    name=node.name, is_public=is_public))

        return ModuleDefinition(functions=functions, classes=classes)
    except Exception as e:
        raise Exception(f"Error parsing {file_path}: {str(e)}")


def get_imports_from_init(init_path: str) -> Set[str]:
    """
    Get all imported names from an __init__.py file.

    Args:
        init_path (str): Path to the __init__.py file.

    Returns:
        Set[str]: Set of imported names.
    """
    imported_names = set()

    try:
        with open(init_path, "r", encoding="utf-8") as f:
            content = f.read()

        module = ast.parse(content)

        # Find all imports
        for node in ast.walk(module):
            if isinstance(node, ast.Import):
                for name in node.names:
                    imported_names.add(name.name)
            elif isinstance(node, ast.ImportFrom):
                for name in node.names:
                    if name.asname:
                        imported_names.add(name.asname)
                    else:
                        imported_names.add(name.name)
            elif isinstance(node, ast.Assign):
                # Handle __all__ = [...] pattern
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "__all__":
                        if isinstance(node.value, ast.List):
                            for elt in node.value.elts:
                                if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                                    imported_names.add(elt.value)
                                # Support for Python < 3.8 where ast.Str was used instead of ast.Constant
                                elif hasattr(ast, 'Str') and isinstance(elt, getattr(ast, 'Str')):
                                    imported_names.add(elt.s)

    except Exception as e:
        print(f"Error parsing {init_path}: {str(e)}")
        return set()

    return imported_names


def check_module_exports(module_dir: str, recursive: bool = True) -> List[VerificationResult]:
    """
    Check if all functions/classes in module files are exported in __init__.py.

    Args:
        module_dir (str): Directory to check.
        recursive (bool): Whether to recursively check subdirectories.

    Returns:
        List[VerificationResult]: List of verification results.
    """
    results = []
    module_path = Path(module_dir)

    # Make sure the directory exists
    if not module_path.exists() or not module_path.is_dir():
        results.append(VerificationResult(
            name=str(module_path),
            result_type="directory",
            exists=False,
            error=f"Directory not found: {module_path}"
        ))
        return results

    # Check if __init__.py exists
    init_path = module_path / "__init__.py"
    if not init_path.exists():
        results.append(VerificationResult(
            name=str(init_path),
            result_type="file",
            exists=False,
            error=f"__init__.py not found in {module_path}"
        ))
        return results

    # Get all imports from __init__.py
    init_imports = get_imports_from_init(str(init_path))

    # Process all Python files in the directory
    for item in module_path.iterdir():
        # Skip __init__.py and non-Python files
        if item.name == "__init__.py" or not item.is_file() or item.suffix != ".py":
            continue

        # Parse the module and get function/class definitions
        try:
            module_defs = parse_module_definitions(str(item))

            # Check that all public functions are exported
            for func in module_defs.functions:
                if func.is_public:
                    if func.name not in init_imports:
                        results.append(VerificationResult(
                            name=f"{module_path.name}.{item.stem}.{func.name}",
                            result_type="function",
                            exists=False,
                            error=f"Function {func.name} in {item.name} is not exported in __init__.py"
                        ))
                    else:
                        results.append(VerificationResult(
                            name=f"{module_path.name}.{item.stem}.{func.name}",
                            result_type="function",
                            exists=True,
                            error=None
                        ))

            # Check that all public classes are exported
            for cls in module_defs.classes:
                if cls.is_public:
                    if cls.name not in init_imports:
                        results.append(VerificationResult(
                            name=f"{module_path.name}.{item.stem}.{cls.name}",
                            result_type="class",
                            exists=False,
                            error=f"Class {cls.name} in {item.name} is not exported in __init__.py"
                        ))
                    else:
                        results.append(VerificationResult(
                            name=f"{module_path.name}.{item.stem}.{cls.name}",
                            result_type="class",
                            exists=True,
                            error=None
                        ))
        except Exception as e:
            results.append(VerificationResult(
                name=f"{module_path.name}.{item.stem}",
                result_type="module",
                exists=False,
                error=f"Error processing {item.name}: {str(e)}"
            ))

    # Recursively check subdirectories if requested
    if recursive:
        for item in module_path.iterdir():
            if item.is_dir() and not item.name.startswith(".") and not item.name.startswith("__"):
                results.extend(check_module_exports(str(item), recursive))

    return results


def display_verification_results(results: List[VerificationResult], show_success: bool = True) -> bool:
    """
    Display verification results.

    Args:
        results (List[VerificationResult]): List of verification results.
        show_success (bool): Whether to show successful verifications.

    Returns:
        bool: True if all checks passed, False otherwise.
    """
    success_count = 0
    failure_count = 0

    # Group by result type for better reporting
    by_type = {
        "module": [],
        "function": [],
        "class": [],
        "attribute": [],
        "directory": [],
        "file": []
    }

    for result in results:
        by_type.get(result.result_type, by_type["module"]).append(result)
        if result.exists:
            success_count += 1
        else:
            failure_count += 1

    # Display results by type
    for type_name, type_results in by_type.items():
        if not type_results:
            continue

        print(f"\n{type_name.capitalize()} verification results:")
        for result in type_results:
            if result.exists:
                if show_success:
                    print(f"✅ {result.name}")
            else:
                print(f"❌ {result.name}: {result.error}")

    print(f"\nResults: {success_count} successful, {failure_count} failed")
    return failure_count == 0


def main() -> int:
    """
    Main function that verifies imports and exports for all packages.

    Returns:
        int: Exit code (0 for success, 1 for failure).
    """
    print("Verifying imports and exports for bot packages...\n")

    all_results = []

    # Core package verification
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

    # Now check module exports in the project
    print("\nChecking module exports in the project...")
    packages_to_check = [
        "bot/core",
        "bot/core/config",
        "bot/core/events",
        "bot/core/lifecycle",
        "bot/utils"
    ]

    export_results = []
    for package in packages_to_check:
        package_path = os.path.join(project_root, package)
        export_results.extend(check_module_exports(package_path))

    # Display all results
    print("\nSummary of import verification:")
    import_success = display_verification_results(all_results)

    print("\nSummary of export verification:")
    export_success = display_verification_results(export_results)

    return 0 if import_success and export_success else 1


if __name__ == "__main__":
    sys.exit(main())
