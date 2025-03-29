"""
Configuration management for the bot.

This module provides the ConfigManager class which handles loading and accessing
configuration values from various sources including .env files and environment variables.
"""

import os
import logging
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Type, TypeVar, Set

# Type variable for type hinting
T = TypeVar('T')

# Set up logger for this module
logger = logging.getLogger(__name__)


class ConfigError(Exception):
    """Base exception for configuration-related errors."""
    pass


class ConfigValidationError(ConfigError):
    """Exception raised when a configuration value is invalid."""
    pass


class ConfigNotFoundError(ConfigError):
    """Exception raised when a required configuration value is not found."""
    pass


class ConfigManager:
    """
    Manages loading and accessing configuration from various sources.

    The ConfigManager implements a multi-source configuration system with validation,
    type conversion, and default values. It supports loading from environment variables
    and .env files.

    Attributes:
        _config (Dict[str, Any]): Internal dictionary storing configuration values.
        _env_prefix (str): Prefix for environment variables.
        _loaded (bool): Flag indicating if configuration has been loaded.
        _required_keys (Set[str]): Set of required configuration keys.
    """

    def __init__(self, env_prefix: str = "BETSY_"):
        """
        Initialize the ConfigManager.

        Args:
            env_prefix (str): Prefix for environment variables.
        """
        self._config: Dict[str, Any] = {}
        self._env_prefix = env_prefix
        self._loaded = False
        self._required_keys: Set[str] = set()

    def load(self, env_file: Optional[Union[str, Path]] = None) -> None:
        """
        Load configuration from environment variables and optionally from a .env file.

        Args:
            env_file (Optional[Union[str, Path]]): Path to .env file.

        Raises:
            ConfigError: If there is an error loading the configuration.
        """
        try:
            # Load .env file if provided
            if env_file:
                self._load_env_file(env_file)

            # Load from environment variables
            self._load_from_env()

            # Mark as loaded
            self._loaded = True

            # Check required keys
            self._check_required_keys()

            logger.info("Configuration loaded successfully")
        except Exception as e:
            logger.error(f"Error loading configuration: {str(e)}")
            raise ConfigError(f"Error loading configuration: {str(e)}") from e

    def _load_env_file(self, env_file: Union[str, Path]) -> None:
        """
        Load configuration from a .env file.

        Args:
            env_file (Union[str, Path]): Path to .env file.

        Raises:
            ConfigError: If there is an error loading the .env file.
        """
        try:
            path = Path(env_file) if isinstance(env_file, str) else env_file

            if not path.exists():
                logger.warning(
                    f"Environment file {path} does not exist, skipping")
                return

            logger.info(f"Loading configuration from {path}")

            with open(path, 'r') as f:
                for line in f:
                    line = line.strip()

                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue

                    # Parse key-value pair
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()

                        # Remove quotes if present
                        if value and (
                            (value.startswith('"') and value.endswith('"')) or
                            (value.startswith("'") and value.endswith("'"))
                        ):
                            value = value[1:-1]

                        # Set environment variable if not already set
                        if key not in os.environ:
                            os.environ[key] = value

            logger.debug(f"Loaded configuration from {path}")
        except Exception as e:
            logger.error(f"Error loading .env file {env_file}: {str(e)}")
            raise ConfigError(f"Error loading .env file: {str(e)}") from e

    def _load_from_env(self) -> None:
        """
        Load configuration from environment variables.

        Environment variables are filtered based on the configured prefix.
        """
        logger.info("Loading configuration from environment variables")

        for key, value in os.environ.items():
            if key.startswith(self._env_prefix):
                # Remove prefix and convert to lowercase
                config_key = key[len(self._env_prefix):].lower()
                self._config[config_key] = value

    def _check_required_keys(self) -> None:
        """
        Check if all required configuration keys are present.

        Raises:
            ConfigNotFoundError: If a required key is missing.
        """
        missing_keys = [
            key for key in self._required_keys if key not in self._config]
        if missing_keys:
            error_msg = f"Missing required configuration keys: {', '.join(missing_keys)}"
            logger.error(error_msg)
            raise ConfigNotFoundError(error_msg)

    def get(self, key: str, default: Any = None, required: bool = False) -> Any:
        """
        Get a configuration value.

        Args:
            key (str): Configuration key.
            default (Any): Default value to return if key is not found.
            required (bool): Whether the key is required.

        Returns:
            Any: Configuration value.

        Raises:
            ConfigNotFoundError: If the key is required but not found.
        """
        if not self._loaded:
            logger.warning("Configuration not loaded yet, call load() first")

        # Convert key to lowercase for consistency
        key = key.lower()

        # Mark as required for future validation if needed
        if required:
            self._required_keys.add(key)

        # Check if key exists
        if key not in self._config:
            if required:
                error_msg = f"Required configuration key not found: {key}"
                logger.error(error_msg)
                raise ConfigNotFoundError(error_msg)
            return default

        return self._config[key]

    def get_int(self, key: str, default: Optional[int] = None, required: bool = False) -> Optional[int]:
        """
        Get a configuration value as an integer.

        Args:
            key (str): Configuration key.
            default (Optional[int]): Default value to return if key is not found.
            required (bool): Whether the key is required.

        Returns:
            Optional[int]: Configuration value as an integer.

        Raises:
            ConfigValidationError: If the value cannot be converted to an integer.
            ConfigNotFoundError: If the key is required but not found.
        """
        value = self.get(key, default, required)

        if value is None:
            return None

        try:
            return int(value)
        except (ValueError, TypeError):
            error_msg = f"Configuration value for {key} is not a valid integer: {value}"
            logger.error(error_msg)
            raise ConfigValidationError(error_msg)

    def get_float(self, key: str, default: Optional[float] = None, required: bool = False) -> Optional[float]:
        """
        Get a configuration value as a float.

        Args:
            key (str): Configuration key.
            default (Optional[float]): Default value to return if key is not found.
            required (bool): Whether the key is required.

        Returns:
            Optional[float]: Configuration value as a float.

        Raises:
            ConfigValidationError: If the value cannot be converted to a float.
            ConfigNotFoundError: If the key is required but not found.
        """
        value = self.get(key, default, required)

        if value is None:
            return None

        try:
            return float(value)
        except (ValueError, TypeError):
            error_msg = f"Configuration value for {key} is not a valid float: {value}"
            logger.error(error_msg)
            raise ConfigValidationError(error_msg)

    def get_bool(self, key: str, default: Optional[bool] = None, required: bool = False) -> Optional[bool]:
        """
        Get a configuration value as a boolean.

        Args:
            key (str): Configuration key.
            default (Optional[bool]): Default value to return if key is not found.
            required (bool): Whether the key is required.

        Returns:
            Optional[bool]: Configuration value as a boolean.

        Raises:
            ConfigValidationError: If the value cannot be converted to a boolean.
            ConfigNotFoundError: If the key is required but not found.
        """
        value = self.get(key, default, required)

        if value is None:
            return None

        if isinstance(value, bool):
            return value

        if isinstance(value, str):
            # Convert string to boolean
            value = value.lower()
            if value in ('true', 'yes', '1', 'y', 'on'):
                return True
            if value in ('false', 'no', '0', 'n', 'off'):
                return False

        error_msg = f"Configuration value for {key} is not a valid boolean: {value}"
        logger.error(error_msg)
        raise ConfigValidationError(error_msg)

    def get_list(
        self,
        key: str,
        default: Optional[List[str]] = None,
        required: bool = False,
        separator: str = ','
    ) -> Optional[List[str]]:
        """
        Get a configuration value as a list of strings.

        Args:
            key (str): Configuration key.
            default (Optional[List[str]]): Default value to return if key is not found.
            required (bool): Whether the key is required.
            separator (str): Separator used to split the string.

        Returns:
            Optional[List[str]]: Configuration value as a list of strings.

        Raises:
            ConfigNotFoundError: If the key is required but not found.
        """
        value = self.get(key, default, required)

        if value is None:
            return None

        if isinstance(value, list):
            return [str(item) for item in value]

        if isinstance(value, str):
            return [item.strip() for item in value.split(separator) if item.strip()]

        return [str(value)]

    def get_typed(
        self,
        key: str,
        type_: Type[T],
        default: Optional[T] = None,
        required: bool = False
    ) -> Optional[T]:
        """
        Get a configuration value with a specific type.

        Args:
            key (str): Configuration key.
            type_ (Type[T]): Type to convert the value to.
            default (Optional[T]): Default value to return if key is not found.
            required (bool): Whether the key is required.

        Returns:
            Optional[T]: Configuration value with the specified type.

        Raises:
            ConfigValidationError: If the value cannot be converted to the specified type.
            ConfigNotFoundError: If the key is required but not found.
        """
        value = self.get(key, default, required)

        if value is None:
            return None

        try:
            return type_(value)
        except (ValueError, TypeError):
            error_msg = f"Configuration value for {key} cannot be converted to {type_.__name__}: {value}"
            logger.error(error_msg)
            raise ConfigValidationError(error_msg)

    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.

        Args:
            key (str): Configuration key.
            value (Any): Configuration value.
        """
        # Convert key to lowercase for consistency
        key = key.lower()
        self._config[key] = value

    def get_all(self) -> Dict[str, Any]:
        """
        Get all configuration values.

        Returns:
            Dict[str, Any]: Dictionary of all configuration values.
        """
        return self._config.copy()

    def reset(self) -> None:
        """Reset the configuration manager."""
        self._config = {}
        self._loaded = False
        self._required_keys = set()


# Create a singleton instance of the ConfigManager
config_manager = ConfigManager()


def get_config() -> ConfigManager:
    """
    Get the singleton ConfigManager instance.

    Returns:
        ConfigManager: Singleton ConfigManager instance.
    """
    return config_manager
