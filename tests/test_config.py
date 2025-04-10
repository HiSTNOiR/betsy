import os
import sys
from pathlib import Path

# Add the parent directory to sys.path to enable imports
sys.path.append(str(Path(__file__).parent.parent))

from core.config import config, ConfigurationError

def mask_sensitive_value(value):
    if not value or not isinstance(value, str) or len(value) <= 3:
        return value
    
    # Check if there's a comment that's not part of the actual value
    # Only consider # as a comment marker if it has a space before it
    parts = value.split(' #', 1)
    actual_value = parts[0]
    
    return f"***{actual_value[-3:]}"

def test_config():
    # Test basic string values
    print("Basic string values:")
    print(f"BOT_NICK: {config.get('BOT_NICK')}")
    print(f"BOT_PREFIX: {config.get('BOT_PREFIX')}")
    print(f"CHANNEL: {config.get('CHANNEL')}")
    print(f"TMI_TOKEN: {mask_sensitive_value(config.get('TMI_TOKEN'))}")
    print(f"CLIENT_ID: {mask_sensitive_value(config.get('CLIENT_ID'))}")
    
    # Test boolean values
    print("\nBoolean values:")
    print(f"DB_ENABLED: {config.get_boolean('DB_ENABLED')}")
    print(f"OBS_ENABLED: {config.get_boolean('OBS_ENABLED')}")
    print(f"DISCORD_ENABLED: {config.get_boolean('DISCORD_ENABLED')}")
    
    # Test path values
    print("\nPath values:")
    print(f"DB_PATH: {config.get_path('DB_PATH')}")
    
    # Test OBS settings (may be empty if disabled)
    print("\nOBS settings:")
    print(f"OBS_HOST: {config.get('OBS_HOST')}")
    print(f"OBS_PORT: {config.get_int('OBS_PORT')}")
    print(f"OBS_PASSWORD: {mask_sensitive_value(config.get('OBS_PASSWORD'))}")
    
    # Test Discord settings (may be empty if disabled)
    print("\nDiscord settings:")
    print(f"DISCORD_TOKEN: {mask_sensitive_value(config.get('DISCORD_TOKEN'))}")
    print(f"DISCORD_CHANNEL_ID: {mask_sensitive_value(config.get('DISCORD_CHANNEL_ID'))}")
    
    # Test missing key with default
    print("\nMissing key with default:")
    print(f"MISSING_KEY: {config.get('MISSING_KEY', 'default_value')}")
    
    # Test dictionary-like access
    print("\nDictionary-like access:")
    try:
        print(f"BOT_NICK via []: {config['BOT_NICK']}")
        print(f"'BOT_NICK' in config: {'BOT_NICK' in config}")
        print(f"'MISSING_KEY' in config: {'MISSING_KEY' in config}")
    except KeyError as e:
        print(f"KeyError: {e}")
    
    print("\nTest complete!")

if __name__ == "__main__":
    test_config()