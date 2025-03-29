"""
Configuration validators for the bot.

This module provides validation functions for configuration values.
"""

import re
import logging
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, TypeVar

from bot.core.config.config import ConfigValidationError

# Type variable for type hinting
T = TypeVar('T')

# Set up logger for this module
logger = logging.getLogger(__name__)


def validate_required(value: Any) -> bool:
    """
    Validate that a value is not None or empty.

    Args:
        value (Any): Value to validate.

    Returns:
        bool: True if the value is valid, False otherwise.
    """
    if value is None:
        return False

    if isinstance(value, str) and not value.strip():
        return False

    if isinstance(value, (list, dict, tuple, set)) and not value:
        return False

    return True


def validate_pattern(pattern: str) -> Callable[[str], bool]:
    """
    Create a validator function that checks if a string matches a regex pattern.

    Args:
        pattern (str): Regular expression pattern.

    Returns:
        Callable[[str], bool]: Validator function.
    """
    compiled_pattern = re.compile(pattern)

    def validator(value: str) -> bool:
        if not isinstance(value, str):
            return False
        return bool(compiled_pattern.match(value))

    return validator


def validate_in_list(valid_values: List[Any]) -> Callable[[Any], bool]:
    """
    Create a validator function that checks if a value is in a list.

    Args:
        valid_values (List[Any]): List of valid values.

    Returns:
        Callable[[Any], bool]: Validator function.
    """
    def validator(value: Any) -> bool:
        return value in valid_values

    return validator


def validate_range(min_value: Optional[float] = None, max_value: Optional[float] = None) -> Callable[[Union[int, float]], bool]:
    """
    Create a validator function that checks if a numeric value is within a range.

    Args:
        min_value (Optional[float]): Minimum value (inclusive).
        max_value (Optional[float]): Maximum value (inclusive).

    Returns:
        Callable[[Union[int, float]], bool]: Validator function.
    """
    def validator(value: Union[int, float]) -> bool:
        if not isinstance(value, (int, float)):
            return False

        if min_value is not None and value < min_value:
            return False

        if max_value is not None and value > max_value:
            return False

        return True

    return validator


def validate_url(value: str) -> bool:
    """
    Validate that a value is a valid URL.

    Args:
        value (str): Value to validate.

    Returns:
        bool: True if the value is a valid URL, False otherwise.
    """
    if not isinstance(value, str):
        return False

    # Simple URL validation, can be enhanced with more complex regex
    pattern = r'^(https?|wss?|ftp)://.+$'
    return bool(re.match(pattern, value))


def validate_path_exists(value: str) -> bool:
    """
    Validate that a path exists.

    Args:
        value (str): Path to validate.

    Returns:
        bool: True if the path exists, False otherwise.
    """
    if not isinstance(value, str):
        return False

    import os.path
    return os.path.exists(value)


def validate_port(value: Any) -> bool:
    """
    Validate that a value is a valid port number.

    Args:
        value (Any): Value to validate.

    Returns:
        bool: True if the value is a valid port number, False otherwise.
    """
    if not isinstance(value, (int, str)):
        return False

    try:
        port = int(value)
        return 1 <= port <= 65535
    except (ValueError, TypeError):
        return False


def validate_type(type_: type) -> Callable[[Any], bool]:
    """
    Create a validator function that checks if a value is of a specific type.

    Args:
        type_ (type): Expected type.

    Returns:
        Callable[[Any], bool]: Validator function.
    """
    def validator(value: Any) -> bool:
        return isinstance(value, type_)

    return validator


def validate_enum(enum_type: Any) -> Callable[[Any], bool]:
    """
    Create a validator function that checks if a value is a valid enum value.

    Args:
        enum_type (Any): Enum class.

    Returns:
        Callable[[Any], bool]: Validator function.
    """
    def validator(value: Any) -> bool:
        try:
            enum_type(value)
            return True
        except (ValueError, TypeError):
            return False

    return validator


def apply_validator(
    key: str,
    value: T,
    validator: Callable[[T], bool],
    error_message: str = "Invalid configuration value"
) -> T:
    """
    Apply a validator to a value and raise an exception if invalid.

    Args:
        key (str): Configuration key.
        value (T): Value to validate.
        validator (Callable[[T], bool]): Validator function.
        error_message (str): Error message if validation fails.

    Returns:
        T: The validated value.

    Raises:
        ConfigValidationError: If the value is invalid.
    """
    if not validator(value):
        full_error = f"{error_message}: {key}={value}"
        logger.error(full_error)
        raise ConfigValidationError(full_error)

    return value


def validate_config(config_dict: Dict[str, Any], validators: Dict[str, List[Tuple[Callable, str]]]) -> Dict[str, Any]:
    """
    Validate multiple configuration values.

    Args:
        config_dict (Dict[str, Any]): Dictionary of configuration values.
        validators (Dict[str, List[Tuple[Callable, str]]]): Dictionary mapping 
            configuration keys to lists of (validator, error_message) tuples.

    Returns:
        Dict[str, Any]: The validated configuration dictionary.

    Raises:
        ConfigValidationError: If any validation fails.
    """
    validated_config = {}

    for key, value in config_dict.items():
        if key in validators:
            for validator, error_message in validators[key]:
                value = apply_validator(key, value, validator, error_message)

        validated_config[key] = value

    return validated_config
