"""
Tests for the configuration module.
"""
import os
import unittest
from unittest.mock import patch, mock_open
import tempfile
from pathlib import Path

from bot.core.config.config import Config, load_config, get_config
from bot.core.errors import ConfigError

class TestConfig(unittest.TestCase):
    """Tests for the Config class."""
    
    def setUp(self):
        # Create a temporary .env file for testing
        self.env_content = """
BOT_NICK=testbot
BOT_PREFIX=!
CHANNEL=testchannel
TMI_TOKEN=oauth:testtoken
CLIENT_ID=testclientid
DB_ENABLED=true
OBS_ENABLED=false
DISCORD_ENABLED=false
DB_PATH=data/test.db
"""
        # Reset the singleton instance
        from bot.core.config import config
        config._config_instance = None

    def test_load_env(self):
        """Test loading environment variables from a file."""
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp:
            temp.write(self.env_content)
            temp_path = temp.name
        
        try:
            # Test loading from the temporary file
            config = Config(env_path=temp_path)
            
            # Check that values were loaded correctly
            self.assertEqual(config.get('BOT_NICK'), 'testbot')
            self.assertEqual(config.get('BOT_PREFIX'), '!')
            self.assertEqual(config.get('CHANNEL'), 'testchannel')
            self.assertEqual(config.get('TMI_TOKEN'), 'oauth:testtoken')
            self.assertEqual(config.get('CLIENT_ID'), 'testclientid')
            self.assertTrue(config.get('DB_ENABLED'))
            self.assertFalse(config.get('OBS_ENABLED'))
            self.assertFalse(config.get('DISCORD_ENABLED'))
            self.assertEqual(config.get('DB_PATH'), 'data/test.db')
        finally:
            # Clean up the temporary file
            os.unlink(temp_path)
    
    def test_missing_required_env(self):
        """Test handling of missing required environment variables."""
        # Missing BOT_NICK
        env_content = """
BOT_PREFIX=!
CHANNEL=testchannel
TMI_TOKEN=oauth:testtoken
CLIENT_ID=testclientid
"""
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp:
            temp.write(env_content)
            temp_path = temp.name
        
        try:
            # Should raise ConfigError for missing BOT_NICK
            with self.assertRaises(ConfigError):
                Config(env_path=temp_path)
        finally:
            # Clean up the temporary file
            os.unlink(temp_path)
    
    def test_invalid_boolean(self):
        """Test handling of invalid boolean values."""
        # Invalid DB_ENABLED
        env_content = """
BOT_NICK=testbot
BOT_PREFIX=!
CHANNEL=testchannel
TMI_TOKEN=oauth:testtoken
CLIENT_ID=testclientid
DB_ENABLED=invalid
"""
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp:
            temp.write(env_content)
            temp_path = temp.name
        
        try:
            # Should raise ConfigError for invalid DB_ENABLED
            with self.assertRaises(ConfigError):
                Config(env_path=temp_path)
        finally:
            # Clean up the temporary file
            os.unlink(temp_path)
    
    def test_get_method(self):
        """Test the get method with default value."""
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp:
            temp.write(self.env_content)
            temp_path = temp.name
        
        try:
            config = Config(env_path=temp_path)
            
            # Test getting a value that exists
            self.assertEqual(config.get('BOT_NICK'), 'testbot')
            
            # Test getting a value that doesn't exist, with default
            self.assertEqual(config.get('NONEXISTENT', 'default'), 'default')
            
            # Test getting a value that doesn't exist, without default
            self.assertIsNone(config.get('NONEXISTENT'))
        finally:
            # Clean up the temporary file
            os.unlink(temp_path)
    
    def test_getitem(self):
        """Test the __getitem__ method."""
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp:
            temp.write(self.env_content)
            temp_path = temp.name
        
        try:
            config = Config(env_path=temp_path)
            
            # Test getting a value that exists
            self.assertEqual(config['BOT_NICK'], 'testbot')
            
            # Test getting a value that doesn't exist
            with self.assertRaises(KeyError):
                config['NONEXISTENT']
        finally:
            # Clean up the temporary file
            os.unlink(temp_path)
    
    def test_contains(self):
        """Test the __contains__ method."""
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp:
            temp.write(self.env_content)
            temp_path = temp.name
        
        try:
            config = Config(env_path=temp_path)
            
            # Test a key that exists
            self.assertTrue('BOT_NICK' in config)
            
            # Test a key that doesn't exist
            self.assertFalse('NONEXISTENT' in config)
        finally:
            # Clean up the temporary file
            os.unlink(temp_path)
    
    def test_get_all(self):
        """Test the get_all method."""
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp:
            temp.write(self.env_content)
            temp_path = temp.name
        
        try:
            config = Config(env_path=temp_path)
            
            # Test getting all config values
            all_config = config.get_all()
            self.assertEqual(all_config['BOT_NICK'], 'testbot')
            self.assertEqual(all_config['BOT_PREFIX'], '!')
            self.assertEqual(all_config['CHANNEL'], 'testchannel')
            
            # Ensure it's a copy
            all_config['BOT_NICK'] = 'modified'
            self.assertEqual(config.get('BOT_NICK'), 'testbot')
        finally:
            # Clean up the temporary file
            os.unlink(temp_path)
    
    def test_load_config_singleton(self):
        """Test the load_config function returns a singleton instance."""
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp:
            temp.write(self.env_content)
            temp_path = temp.name
        
        try:
            # Load config once
            config1 = load_config(env_path=temp_path)
            
            # Load config again
            config2 = load_config()
            
            # Should be the same instance
            self.assertIs(config1, config2)
            
            # Check get_config also returns the same instance
            config3 = get_config()
            self.assertIs(config1, config3)
        finally:
            # Clean up the temporary file
            os.unlink(temp_path)
    
    def test_get_config_error(self):
        """Test get_config raises error if config not loaded."""
        # Reset the singleton instance
        from bot.core.config import config
        config._config_instance = None
        
        # Should raise ConfigError
        with self.assertRaises(ConfigError):
            get_config()
    
    def test_reload(self):
        """Test the reload method."""
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp:
            temp.write(self.env_content)
            temp_path = temp.name
        
        try:
            config = Config(env_path=temp_path)
            self.assertEqual(config.get('BOT_NICK'), 'testbot')
            
            # Update the environment variable
            os.environ['BOT_NICK'] = 'newbot'
            
            # Reload the config
            config.reload()
            
            # Should have the new value
            self.assertEqual(config.get('BOT_NICK'), 'newbot')
        finally:
            # Clean up the temporary file
            os.unlink(temp_path)
            # Reset the environment variable
            if 'BOT_NICK' in os.environ:
                del os.environ['BOT_NICK']

if __name__ == '__main__':
    unittest.main()