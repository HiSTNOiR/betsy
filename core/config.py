import os
import logging

from dotenv import load_dotenv
from pathlib import Path
from typing import Dict, Any, Optional, Union, List, Set

class ConfigurationError(Exception):
    pass

class Configuration:
    _instance = None
    _loaded = False
    _config: Dict[str, Any] = {}
    _required_keys: Set[str] = {
        'BOT_NICK', 
        'BOT_PREFIX', 
        'CHANNEL'
    }
    _boolean_keys: Set[str] = {
        'DB_ENABLED', 
        'OBS_ENABLED', 
        'DISCORD_ENABLED'
    }
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Configuration, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, env_path: Optional[str] = None):
        if not self._loaded:
            self._load_config(env_path)
            self._loaded = True
    
    def _load_config(self, env_path: Optional[str] = None) -> None:
        if env_path:
            if not os.path.exists(env_path):
                raise ConfigurationError(f"Configuration file not found: {env_path}")
            success = load_dotenv(env_path)
        else:
            env_files = ['.env', '.env.local']
            success = False
            for file in env_files:
                if os.path.exists(file):
                    success = load_dotenv(file)
                    break
                    
        if not success:
            logging.warning("No .env file loaded, using environment variables only")
        
        for key in os.environ:
            if key in self._boolean_keys:
                self._config[key] = self._parse_boolean(os.environ[key])
            else:
                self._config[key] = os.environ[key]
        
        self._validate_config()
    
    def _validate_config(self) -> None:
        missing_keys = self._required_keys - set(self._config.keys())
        if missing_keys:
            raise ConfigurationError(f"Missing required configuration keys: {', '.join(missing_keys)}")
    
    def _parse_boolean(self, value: str) -> bool:
        return value.lower() in ('true', 'yes', '1', 'y', 'on')
    
    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)
    
    def get_boolean(self, key: str, default: bool = False) -> bool:
        value = self._config.get(key)
        if value is None:
            return default
        if isinstance(value, bool):
            return value
        return self._parse_boolean(str(value))
    
    def get_int(self, key: str, default: int = 0) -> int:
        value = self._config.get(key)
        if value is None:
            return default
        try:
            return int(value)
        except (ValueError, TypeError):
            return default
    
    def get_float(self, key: str, default: float = 0.0) -> float:
        value = self._config.get(key)
        if value is None:
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
    
    def get_list(self, key: str, separator: str = ',', default: Optional[List] = None) -> List:
        if default is None:
            default = []
        value = self._config.get(key)
        if value is None:
            return default
        return [item.strip() for item in str(value).split(separator) if item.strip()]
    
    def get_path(self, key: str, default: Optional[str] = None) -> Optional[Path]:
        value = self._config.get(key)
        if value is None:
            return Path(default) if default else None
        return Path(value)
    
    def add_required_keys(self, keys: Union[str, List[str], Set[str]]) -> None:
        if isinstance(keys, str):
            self._required_keys.add(keys)
        else:
            self._required_keys.update(keys)
        self._validate_config()
    
    def reload(self, env_path: Optional[str] = None) -> None:
        self._config.clear()
        self._loaded = False
        self.__init__(env_path)
    
    def __getitem__(self, key: str) -> Any:
        if key not in self._config:
            raise KeyError(f"Configuration key '{key}' not found")
        return self._config[key]
    
    def __contains__(self, key: str) -> bool:
        return key in self._config


config = Configuration()