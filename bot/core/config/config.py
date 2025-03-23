"""
Configuration loader module for the Twitch bot.
Loads configuration from .env file and provides access to configuration values.
"""
import os
import logging
from dotenv import load_dotenv
from pathlib import Path
from typing import Dict, Any, Optional, Union, cast

from bot.core.errors import ConfigError
from bot.utils.validation import validate_boolean, validate_port

# Set up logger
logger = logging.getLogger(__name__)

class Config:
    """Configuration manager for the bot."""
    
    def __init__(self, env_path: Optional[str] = None):
        """
        Initialise the configuration manager.
        
        Args:
            env_path: Optional path to .env file. If None, will search in current directory.
        """
        self._config: Dict[str, Any] = {}
        self._load_env(env_path)
        self._process_config()
        
    def _load_env(self, env_path: Optional[str] = None) -> None:
        """
        Load environment variables from .env file.
        
        Args:
            env_path: Optional path to .env file. If None, will search in current directory.
        
        Raises:
            ConfigError: If .env file cannot be found or loaded.
        """
        try:
            if env_path:
                env_file = Path(env_path)
                if not env_file.exists():
                    raise ConfigError(f"Environment file not found at {env_path}")
                load_dotenv(dotenv_path=env_path)
            else:
                load_dotenv()
                
            logger.info("Environment variables loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load environment variables: {e}")
            raise ConfigError(f"Failed to load environment variables: {e}")
    
    def _process_config(self) -> None:
        """
        Process environment variables into appropriate configuration values.
        
        Raises:
            ConfigError: If required configuration values are missing or invalid.
        """
        # Bot settings
        self._config['BOT_NICK'] = self._get_required_env('BOT_NICK')
        self._config['BOT_PREFIX'] = self._get_required_env('BOT_PREFIX')
        self._config['CHANNEL'] = self._get_required_env('CHANNEL')
        
        # Twitch API credentials
        self._config['TMI_TOKEN'] = self._get_required_env('TMI_TOKEN')
        self._config['CLIENT_ID'] = self._get_required_env('CLIENT_ID')
        
        # Feature flags
        self._config['DB_ENABLED'] = validate_boolean(
            self._get_env('DB_ENABLED', 'false')
        )
        self._config['OBS_ENABLED'] = validate_boolean(
            self._get_env('OBS_ENABLED', 'false')
        )
        self._config['DISCORD_ENABLED'] = validate_boolean(
            self._get_env('DISCORD_ENABLED', 'false')
        )
        
        # Database settings (only processed if DB_ENABLED is True)
        if self._config['DB_ENABLED']:
            self._config['DB_PATH'] = self._get_required_env('DB_PATH')
        
        # OBS WebSocket settings (only processed if OBS_ENABLED is True)
        if self._config['OBS_ENABLED']:
            self._config['OBS_HOST'] = self._get_required_env('OBS_HOST')
            obs_port = self._get_required_env('OBS_PORT')
            try:
                self._config['OBS_PORT'] = validate_port(obs_port)
            except ValueError as e:
                raise ConfigError(f"Invalid OBS_PORT: {e}")
            self._config['OBS_PASSWORD'] = self._get_required_env('OBS_PASSWORD')
        
        # Discord settings (only processed if DISCORD_ENABLED is True)
        if self._config['DISCORD_ENABLED']:
            self._config['DISCORD_TOKEN'] = self._get_required_env('DISCORD_TOKEN')
            self._config['DISCORD_CHANNEL_ID'] = self._get_required_env('DISCORD_CHANNEL_ID')
            
        logger.info("Configuration processed successfully")
    
    def _get_env(self, key: str, default: Optional[str] = None) -> str:
        """
        Get environment variable, with optional default value.
        
        Args:
            key: Environment variable name
            default: Default value if not found
        
        Returns:
            Environment variable value or default
        """
        value = os.getenv(key, default)
        if value is None:
            return ''
        return value
    
    def _get_required_env(self, key: str) -> str:
        """
        Get required environment variable.
        
        Args:
            key: Environment variable name
        
        Returns:
            Environment variable value
        
        Raises:
            ConfigError: If environment variable is not set
        """
        value = os.getenv(key)
        if value is None or value == '':
            logger.error(f"Required environment variable '{key}' is not set")
            raise ConfigError(f"Required environment variable '{key}' is not set")
        return value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if not found
        
        Returns:
            Configuration value or default
        """
        return self._config.get(key, default)
    
    def __getitem__(self, key: str) -> Any:
        """
        Get configuration value using dictionary syntax.
        
        Args:
            key: Configuration key
        
        Returns:
            Configuration value
        
        Raises:
            KeyError: If configuration key is not found
        """
        if key not in self._config:
            raise KeyError(f"Configuration key '{key}' not found")
        return self._config[key]
    
    def __contains__(self, key: str) -> bool:
        """
        Check if configuration contains key.
        
        Args:
            key: Configuration key
        
        Returns:
            True if configuration contains key, False otherwise
        """
        return key in self._config
    
    def get_all(self) -> Dict[str, Any]:
        """
        Get all configuration values.
        
        Returns:
            Dictionary of all configuration values
        """
        return self._config.copy()
    
    def reload(self) -> None:
        """
        Reload configuration from environment variables.
        """
        self._process_config()
        logger.info("Configuration reloaded successfully")

# Create singleton instance
_config_instance: Optional[Config] = None

def load_config(env_path: Optional[str] = None) -> Config:
    """
    Load configuration and return singleton instance.
    
    Args:
        env_path: Optional path to .env file
    
    Returns:
        Config instance
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = Config(env_path)
    return _config_instance

def get_config() -> Config:
    """
    Get singleton configuration instance.
    
    Returns:
        Config instance
    
    Raises:
        ConfigError: If configuration has not been loaded
    """
    if _config_instance is None:
        raise ConfigError("Configuration has not been loaded. Call load_config() first.")
    return _config_instance