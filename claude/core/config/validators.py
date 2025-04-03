import re
import logging
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, TypeVar

from bot.core.config.config import ConfigValidationError
T = TypeVar('T')
logger = logging.getLogger(__name__)


def validate_required(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str) and not value.strip():
        return False
    if isinstance(value, (list, dict, tuple, set)) and not value:
        return False
    return True


def validate_pattern(pattern: str) -> Callable[[str], bool]:
    compiled_pattern = re.compile(pattern)

    def validator(value: str) -> bool:
        if not isinstance(value, str):
            return False
        return bool(compiled_pattern.match(value))
    return validator


def validate_in_list(valid_values: List[Any]) -> Callable[[Any], bool]:
    def validator(value: Any) -> bool:
        return value in valid_values
    return validator


def validate_range(min_value: Optional[float] = None, max_value: Optional[float] = None) -> Callable[[Union[int, float]], bool]:
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
    if not isinstance(value, str):
        return False
    pattern = r'^(https?|wss?|ftp)://.+$'
    return bool(re.match(pattern, value))


def validate_path_exists(value: str) -> bool:
    if not isinstance(value, str):
        return False
    import os.path
    return os.path.exists(value)


def validate_port(value: Any) -> bool:
    if not isinstance(value, (int, str)):
        return False
    try:
        port = int(value)
        return 1 <= port <= 65535
    except (ValueError, TypeError):
        return False


def validate_type(type_: type) -> Callable[[Any], bool]:
    def validator(value: Any) -> bool:
        return isinstance(value, type_)
    return validator


def validate_enum(enum_type: Any) -> Callable[[Any], bool]:
    def validator(value: Any) -> bool:
        if isinstance(value, enum_type):
            return True
        if isinstance(value, str):
            try:
                enum_type[value]
                return True
            except (KeyError, TypeError):
                pass
        try:
            enum_type(value)
            return True
        except (ValueError, TypeError):
            if isinstance(value, str):
                try:
                    numeric_val = int(value)
                    enum_type(numeric_val)
                    return True
                except (ValueError, TypeError):
                    pass
        return False
    return validator


def apply_validator(
    key: str,
    value: T,
    validator: Callable[[T], bool],
    error_message: str = "Invalid configuration value"
) -> T:
    if not validator(value):
        full_error = f"{error_message}: {key}={value}"
        logger.error(full_error)
        raise ConfigValidationError(full_error)
    return value


def validate_config(config_dict: Dict[str, Any], validators: Dict[str, List[Tuple[Callable, str]]]) -> Dict[str, Any]:
    validated_config = {}
    for key, value in config_dict.items():
        if key in validators:
            for validator, error_message in validators[key]:
                value = apply_validator(key, value, validator, error_message)
        validated_config[key] = value
    return validated_config
