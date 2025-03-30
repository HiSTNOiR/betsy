"""
Unit tests for bot.core.app module.

This module tests the BetsyBot application class and main function.
"""

import unittest
import sys
import os
from unittest import TestCase
from unittest.mock import (
    patch, MagicMock, mock_open, Mock
)

# Import the module under test
from bot.core.app import BetsyBot, main

# Suppress print output during tests
unittest.main.__defaults__ = (None, True, [], False)


class TestBetsyBot(TestCase):
    """Test cases for the BetsyBot application class."""

    def setUp(self):
        """Set up test environment for each test."""
        # Clear any existing ENV_FILE environment variable
        if 'ENV_FILE' in os.environ:
            del os.environ['ENV_FILE']

    def test_init_without_env_file(self):
        """Test initialising BetsyBot without an environment file."""
        bot = BetsyBot()

        # Verify initial state
        self.assertIsNotNone(bot._lifecycle)
        self.assertIsNone(bot._env_file)

    def test_init_with_env_file(self):
        """Test initialising BetsyBot with an environment file."""
        env_file_path = "/path/to/test/.env"
        bot = BetsyBot(env_file=env_file_path)

        # Verify initial state
        self.assertIsNotNone(bot._lifecycle)
        self.assertEqual(bot._env_file, env_file_path)

    @patch('bot.core.app.register_all_hooks')
    @patch('bot.core.lifecycle.LifecycleManager.run')
    def test_run_success(self, mock_lifecycle_run, mock_register_hooks):
        """Test successful application run."""
        # Create a bot instance
        bot = BetsyBot()

        # Run the bot
        bot.run()

        # Verify that environment setup and hook registration occurred
        self.assertTrue(mock_register_hooks.called)
        self.assertTrue(mock_lifecycle_run.called)

    @patch('bot.core.app.register_all_hooks')
    @patch('bot.core.lifecycle.LifecycleManager.run')
    @patch('sys.exit')
    def test_run_with_exception(self, mock_sys_exit, mock_lifecycle_run, mock_register_hooks):
        """Test application run with an unexpected exception."""
        # Create a bot instance
        bot = BetsyBot()

        # Mock the run method to raise an exception
        mock_lifecycle_run.side_effect = Exception("Test runtime error")

        # Run the bot
        bot.run()

        # Verify that the error was logged and system exited
        mock_sys_exit.assert_called_once_with(1)

    def test_setup_environment_with_env_file(self):
        """Test setting up environment with an env file."""
        env_file_path = "/path/to/test/.env"
        bot = BetsyBot(env_file=env_file_path)

        # Call private method to setup environment
        bot._setup_environment()

        # Verify that ENV_FILE is set in environment
        self.assertEqual(os.environ.get('ENV_FILE'), env_file_path)

    def test_setup_environment_without_env_file(self):
        """Test setting up environment without an env file."""
        bot = BetsyBot()

        # Call private method to setup environment
        bot._setup_environment()

        # Verify that ENV_FILE is not set
        self.assertNotIn('ENV_FILE', os.environ)


class TestMainFunction(TestCase):
    """Test cases for the main function."""

    @patch('bot.core.app.BetsyBot')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_with_default_args(self, mock_parse_args, mock_bot_class):
        """Test main function with default arguments."""
        # Create a mock bot instance
        mock_bot_instance = mock_bot_class.return_value
        mock_bot_instance.run = MagicMock()

        # Set up mock to return default arguments
        mock_parse_args.return_value = Mock(env_file=None)

        # Call main function
        main()

        # Verify bot was created with default (None) env file
        mock_bot_class.assert_called_once_with(env_file=None)

        # Verify bot's run method was called
        mock_bot_instance.run.assert_called_once()

    @patch('bot.core.app.BetsyBot')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_with_custom_env_file(self, mock_parse_args, mock_bot_class):
        """Test main function with a custom environment file."""
        custom_env_path = "/custom/path/to/.env"

        # Create a mock bot instance
        mock_bot_instance = mock_bot_class.return_value
        mock_bot_instance.run = MagicMock()

        # Set up mock to return custom env file argument
        mock_parse_args.return_value = Mock(env_file=custom_env_path)

        # Call main function
        main()

        # Verify bot was created with custom env file
        mock_bot_class.assert_called_once_with(env_file=custom_env_path)

        # Verify bot's run method was called
        mock_bot_instance.run.assert_called_once()


if __name__ == "__main__":
    unittest.main()
