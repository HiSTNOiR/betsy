"""
Unit tests for bot.core.config module.

This module tests the configuration management implementation.
"""

import os
import unittest
import tempfile
from unittest import TestCase
from unittest.mock import patch

# Import the module under test
from bot.core.config import (
    ConfigManager,
    ConfigError,
    ConfigNotFoundError,
    ConfigValidationError,
    get_config
)

# Suppress print output during tests
unittest.main.__defaults__ = (None, True, [], False)


class TestConfigManager(TestCase):
    """Test cases for ConfigManager class."""

    def setUp(self):
        """Set up test environment."""
        # Create a fresh ConfigManager for each test
        self.config = ConfigManager()

    def test_initial_state(self):
        """Test the initial state of the ConfigManager."""
        self.assertFalse(self.config._loaded)
        self.assertEqual(self.config._config, {})
        self.assertEqual(self.config._required_keys, set())

    def test_load_from_env(self):
        """Test loading configuration from environment variables."""
        # Set some test environment variables
        with patch.dict(os.environ, {
            'BETSY_TEST_KEY1': 'value1',
            'BETSY_TEST_KEY2': 'value2',
            'UNRELATED_KEY': 'ignored'
        }):
            self.config.load()

            # Verify loaded configuration
            self.assertTrue(self.config._loaded)
            self.assertEqual(self.config.get('test_key1'), 'value1')
            self.assertEqual(self.config.get('test_key2'), 'value2')
            self.assertIsNone(self.config.get('unrelated_key'))

    def test_load_from_env_file(self):
        """Test loading configuration from a .env file."""
        # Create a temporary .env file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_env:
            temp_env.write("""
            # Comment line
            BETSY_TEST_KEY1=file_value1
            BETSY_TEST_KEY2=file_value2
            """)
            temp_env.flush()

        try:
            # Clear existing environment to isolate test
            with patch.dict(os.environ, clear=True):
                self.config.load(temp_env.name)

                # Verify loaded configuration
                self.assertTrue(self.config._loaded)
                self.assertEqual(self.config.get('test_key1'), 'file_value1')
                self.assertEqual(self.config.get('test_key2'), 'file_value2')
        finally:
            # Clean up the temporary file
            os.unlink(temp_env.name)

    def test_get_int(self):
        """Test getting integer configuration values."""
        # Manually set loaded to True for testing
        self.config._loaded = True

        # Create a config with test values
        self.config.set('test_int', '42')

        # Test integer conversion
        self.assertEqual(self.config.get_int('test_int'), 42)

        # Test with default value
        self.assertEqual(self.config.get_int('non_existent', 100), 100)

        # Test float value raises validation error
        self.config.set('test_float_int', '3.14')
        with self.assertRaises(ConfigValidationError):
            self.config.get_int('test_float_int')

        # Test non-numeric value raises validation error
        self.config.set('test_non_int', 'not_an_int')
        with self.assertRaises(ConfigValidationError):
            self.config.get_int('test_non_int')

    def test_get_float(self):
        """Test getting float configuration values."""
        # Manually set loaded to True for testing
        self.config._loaded = True

        # Create a config with test values
        self.config.set('test_float', '3.14')

        # Test float conversion
        self.assertAlmostEqual(self.config.get_float('test_float'), 3.14)

        # Test with default value
        self.assertAlmostEqual(self.config.get_float(
            'non_existent', 100.5), 100.5)

        # Test invalid float
        self.config.set('test_non_float', 'not_a_float')
        with self.assertRaises(ConfigValidationError):
            self.config.get_float('test_non_float')

    def test_get_bool(self):
        """Test getting boolean configuration values."""
        # Manually set loaded to True for testing
        self.config._loaded = True

        # Test true values
        true_values = ['true', 'yes', '1', 'y', 'on']
        for val in true_values:
            self.config.set('test_bool', val)
            self.assertTrue(self.config.get_bool(
                'test_bool'), f"Failed for {val}")

        # Test false values
        false_values = ['false', 'no', '0', 'n', 'off']
        for val in false_values:
            self.config.set('test_bool', val)
            self.assertFalse(self.config.get_bool(
                'test_bool'), f"Failed for {val}")

        # Test invalid bool
        self.config.set('test_bool', 'not_a_bool')
        with self.assertRaises(ConfigValidationError):
            self.config.get_bool('test_bool')

    def test_get_list(self):
        """Test getting list configuration values."""
        # Manually set loaded to True for testing
        self.config._loaded = True

        # Test default comma separator
        self.config.set('test_list', 'a,b,c')
        self.assertEqual(
            self.config.get_list('test_list'),
            ['a', 'b', 'c']
        )

        # Test custom separator
        self.config.set('test_custom_sep', 'a;b;c')
        self.assertEqual(
            self.config.get_list('test_custom_sep', separator=';'),
            ['a', 'b', 'c']
        )

        # Test single value
        self.config.set('test_single', 'single')
        self.assertEqual(
            self.config.get_list('test_single'),
            ['single']
        )

        # Test list input
        self.config.set('test_list_input', ['x', 'y', 'z'])
        self.assertEqual(
            self.config.get_list('test_list_input'),
            ['x', 'y', 'z']
        )

    def test_get_typed(self):
        """Test getting configuration values with specific types."""
        # Manually set loaded to True for testing
        self.config._loaded = True

        # Create a config with test values
        self.config.set('test_int', '42')
        self.config.set('test_float', '3.14')

        # Test various type conversions
        self.assertEqual(self.config.get_typed('test_int', int), 42)
        self.assertAlmostEqual(
            self.config.get_typed('test_float', float), 3.14)
        self.assertEqual(self.config.get_typed('test_int', str), '42')

        # Test with default value
        self.assertEqual(self.config.get_typed(
            'non_existent', str, 'default'), 'default')

        # Test invalid type conversion
        class CustomType:
            def __init__(self, val):
                raise ValueError(f"Cannot convert {val}")

        with self.assertRaises(ConfigValidationError):
            self.config.get_typed('test_int', CustomType)

    def test_required_keys(self):
        """Test handling of required configuration keys."""
        # Create a config with a required key
        with patch.dict(os.environ, {'BETSY_REQUIRED_KEY': 'test_value'}):
            # Mark a key as required before loading
            try:
                self.config.get('required_key', required=True)
            except ConfigNotFoundError:
                # This is expected before loading
                pass

            # Load configuration
            self.config.load()

            # Verify required key
            self.assertEqual(self.config.get(
                'required_key', required=True), 'test_value')

    def test_reset(self):
        """Test resetting the configuration manager."""
        # Set some values
        with patch.dict(os.environ, {'BETSY_TEST_KEY': 'value'}):
            # Modify the test to not call get with required before load
            # Load the configuration
            self.config.load()

            # Mark a key as required after loading
            self.config.get('test_key', required=True)

            # Verify loaded state
            self.assertTrue(self.config._loaded)
            self.assertGreater(len(self.config._config), 0)
            self.assertGreater(len(self.config._required_keys), 0)

            # Reset
            self.config.reset()

            # Verify reset state
            self.assertFalse(self.config._loaded)
            self.assertEqual(self.config._config, {})
            self.assertEqual(self.config._required_keys, set())

    def test_get_all(self):
        """Test getting all configuration values."""
        # Manually set loaded to True for testing
        self.config._loaded = True

        # Set some test values
        self.config.set('key1', 'value1')
        self.config.set('key2', 'value2')

        # Get all values
        all_configs = self.config.get_all()

        # Verify contents
        self.assertEqual(all_configs.get('key1'), 'value1')
        self.assertEqual(all_configs.get('key2'), 'value2')

    def test_set_and_get(self):
        """Test setting and getting a configuration value."""
        # Manually set loaded to True for testing
        self.config._loaded = True

        # Set a value
        self.config.set('custom_key', 'custom_value')

        # Get the value
        self.assertEqual(self.config.get('custom_key'), 'custom_value')

    def test_nonexistent_key(self):
        """Test getting a non-existent key."""
        # Manually set loaded to True for testing
        self.config._loaded = True

        # Get non-existent key with no default
        self.assertIsNone(self.config.get('non_existent_key'))

        # Get non-existent key with default
        self.assertEqual(self.config.get(
            'non_existent_key', 'default'), 'default')


class TestConfigSingleton(TestCase):
    """Test cases for the configuration singleton."""

    def test_get_config(self):
        """Test that get_config returns the singleton instance."""
        # Get the config
        config1 = get_config()
        config2 = get_config()

        # Check that it's the same instance
        self.assertIs(config1, config2)


if __name__ == "__main__":
    unittest.main()
