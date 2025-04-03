import os
import logging
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Type, TypeVar, Set

T = TypeVar('T')
logger = logging.getLogger(__name__)


class ConfigError(Exception):
    pass


class ConfigValidationError(ConfigError):
    pass


class ConfigNotFoundError(ConfigError):
    pass


class ConfigManager:
    def __init__(self, env_prefix: str = "BETSY_"):
        self._config: Dict[str, Any] = {}
        self._env_prefix = env_prefix
        self._loaded = False
        self._required_keys: Set[str] = set()

    def load(self, env_file: Optional[Union[str, Path]] = None) -> None:
        try:
            if env_file:
                self._load_env_file(env_file)
            self._load_from_env()
            self._loaded = True
            self._check_required_keys()
            logger.info("Configuration loaded successfully")
        except Exception as e:
            logger.error(f"Error loading configuration: {str(e)}")
            raise ConfigError(f"Error loading configuration: {str(e)}") from e

    def _load_env_file(self, env_file: Union[str, Path]) -> None:
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
                    if not line or line.startswith('#'):
                        continue
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        if value and (
                            (value.startswith('"') and value.endswith('"')) or
                            (value.startswith("'") and value.endswith("'"))
                        ):
                            value = value[1:-1]
                        if key not in os.environ:
                            os.environ[key] = value
            logger.debug(f"Loaded configuration from {path}")
        except Exception as e:
            logger.error(f"Error loading .env file {env_file}: {str(e)}")
            raise ConfigError(f"Error loading .env file: {str(e)}") from e

    def _load_from_env(self) -> None:
        logger.info("Loading configuration from environment variables")
        for key, value in os.environ.items():
            if key.startswith(self._env_prefix):
                # Remove prefix and convert to lowercase
                config_key = key[len(self._env_prefix):].lower()
                self._config[config_key] = value

    def _check_required_keys(self) -> None:
        missing_keys = [
            key for key in self._required_keys if key not in self._config]
        if missing_keys:
            error_msg = f"Missing required configuration keys: {', '.join(missing_keys)}"
            logger.error(error_msg)
            raise ConfigNotFoundError(error_msg)

    def get(self, key: str, default: Any = None, required: bool = False) -> Any:
        if not self._loaded:
            logger.warning("Configuration not loaded yet, call load() first")
        key = key.lower()
        if required:
            self._required_keys.add(key)
        if key not in self._config:
            if required:
                error_msg = f"Required configuration key not found: {key}"
                logger.error(error_msg)
                raise ConfigNotFoundError(error_msg)
            return default
        return self._config[key]

    def get_int(self, key: str, default: Optional[int] = None, required: bool = False) -> Optional[int]:
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
        value = self.get(key, default, required)
        if value is None:
            return None
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
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
        key = key.lower()
        self._config[key] = value

    def get_all(self) -> Dict[str, Any]:
        return self._config.copy()

    def reset(self) -> None:
        self._config = {}
        self._loaded = False
        self._required_keys = set()


config_manager = ConfigManager()


def get_config() -> ConfigManager:
    return config_manager
