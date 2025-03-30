"""
Unit tests for bot.core.errors module.

This module tests the error handling and context mechanisms.
"""

import unittest
import sys
from unittest import TestCase
from unittest.mock import patch, MagicMock

# Import the module under test
from bot.core.errors import (
    BotError,
    ConfigError,
    DatabaseError,
    CommandError,
    ErrorContext,
    ErrorHandler,
    get_error_handler,
    register_default_handlers,
    get_traceback_str,
    try_except_decorator
)

# Suppress print output during tests
unittest.main.__defaults__ = (None, True, [], False)


class TestBotErrors(TestCase):
    """Test cases for custom error classes."""

    def test_base_bot_error(self):
        """Test the base BotError with a custom message."""
        error_msg = "Test bot error message"
        error = BotError(error_msg)

        self.assertEqual(str(error), error_msg)
        self.assertEqual(error.message, error_msg)

    def test_config_error(self):
        """Test ConfigError inherits from BotError."""
        error_msg = "Configuration error occurred"
        error = ConfigError(error_msg)

        self.assertTrue(isinstance(error, BotError))
        self.assertEqual(str(error), error_msg)

    def test_database_error(self):
        """Test DatabaseError inherits from BotError."""
        error_msg = "Database operation failed"
        error = DatabaseError(error_msg)

        self.assertTrue(isinstance(error, BotError))
        self.assertEqual(str(error), error_msg)

    def test_command_error(self):
        """Test CommandError inherits from BotError."""
        error_msg = "Command execution error"
        error = CommandError(error_msg)

        self.assertTrue(isinstance(error, BotError))
        self.assertEqual(str(error), error_msg)


class TestErrorContext(TestCase):
    """Test cases for ErrorContext class."""

    def setUp(self):
        """Set up test environment for each test."""
        self.test_error = ValueError("Test error")
        self.test_source = "test_module"
        self.test_context = {"key": "value"}

    def test_error_context_init(self):
        """Test initialising ErrorContext with minimal arguments."""
        context = ErrorContext(self.test_error)

        self.assertEqual(context.error, self.test_error)
        self.assertIsNone(context.source)
        self.assertEqual(context.context, {})
        self.assertIn("ValueError: Test error", context.traceback_info)

    def test_error_context_with_source_and_context(self):
        """Test initialising ErrorContext with full arguments."""
        context = ErrorContext(
            self.test_error,
            source=self.test_source,
            context=self.test_context
        )

        self.assertEqual(context.error, self.test_error)
        self.assertEqual(context.source, self.test_source)
        self.assertEqual(context.context, self.test_context)
        self.assertIn("ValueError: Test error", context.traceback_info)

    def test_error_context_as_dict(self):
        """Test converting ErrorContext to dictionary."""
        context = ErrorContext(
            self.test_error,
            source=self.test_source,
            context=self.test_context
        )

        context_dict = context.as_dict()
        self.assertEqual(context_dict['error_type'], 'ValueError')
        self.assertEqual(context_dict['error_message'], 'Test error')
        self.assertEqual(context_dict['source'], self.test_source)
        self.assertEqual(context_dict['context'], self.test_context)
        self.assertIn("ValueError: Test error", context_dict['traceback'])


class TestErrorHandler(TestCase):
    """Test cases for ErrorHandler class."""

    def setUp(self):
        """Set up test environment for each test."""
        self.error_handler = ErrorHandler()

    def test_register_handler(self):
        """Test registering a handler for a specific error type."""
        mock_handler = MagicMock()

        self.error_handler.register_handler(ValueError, mock_handler)

        # Verify the handler is registered
        self.assertIn(ValueError, self.error_handler._handlers)
        self.assertIn(mock_handler, self.error_handler._handlers[ValueError])

    def test_set_default_handler(self):
        """Test setting a default error handler."""
        mock_default_handler = MagicMock()

        self.error_handler.set_default_handler(mock_default_handler)

        self.assertEqual(self.error_handler._default_handler,
                         mock_default_handler)

    @patch('logging.Logger.error')
    def test_handle_with_specific_handler(self, mock_log_error):
        """Test handling an error with a specific handler."""
        mock_handler = MagicMock()
        test_error = ValueError("Test error")

        self.error_handler.register_handler(ValueError, mock_handler)
        self.error_handler.handle(test_error, source="test_module")

        # Verify the specific handler was called
        mock_handler.assert_called_once()
        mock_log_error.assert_called_once()

    @patch('logging.Logger.error')
    def test_handle_with_default_handler(self, mock_log_error):
        """Test handling an error with the default handler."""
        mock_default_handler = MagicMock()
        test_error = ValueError("Test error")

        self.error_handler.set_default_handler(mock_default_handler)
        self.error_handler.handle(test_error, source="test_module")

        # Verify the default handler was called
        mock_default_handler.assert_called_once()
        mock_log_error.assert_called_once()

    def test_try_except_success(self):
        """Test try_except with a successful function call."""
        def test_func(x, y):
            return x + y

        result = self.error_handler.try_except(test_func, 2, 3)
        self.assertEqual(result, 5)

    @patch('logging.Logger.error')
    def test_try_except_with_exception(self, mock_log_error):
        """Test try_except with a function that raises an exception."""
        def test_func(x, y):
            raise ValueError("Test error")

        result = self.error_handler.try_except(test_func, 2, 3, default=10)
        self.assertEqual(result, 10)
        mock_log_error.assert_called_once()


class TestErrorUtilities(TestCase):
    """Test cases for error utility functions."""

    def test_get_traceback_str(self):
        """Test get_traceback_str function."""
        try:
            raise ValueError("Test traceback")
        except ValueError as e:
            traceback_str = get_traceback_str()

        self.assertIn("ValueError: Test traceback", traceback_str)
        self.assertIn("test_get_traceback_str", traceback_str)

    def test_try_except_decorator(self):
        """Test try_except_decorator."""
        @try_except_decorator(source="test_module", default=10)
        def test_func():
            raise ValueError("Test error")

        result = test_func()
        self.assertEqual(result, 10)


class TestDefaultHandlers(TestCase):
    """Test cases for default error handlers."""

    @patch('logging.Logger.info')
    @patch('logging.Logger.error')
    def test_register_default_handlers(self, mock_log_error, mock_log_info):
        """Test registering default handlers."""
        error_handler = ErrorHandler()
        register_default_handlers(error_handler)

        # Verify default and specific handlers are set
        self.assertIsNotNone(error_handler._default_handler)
        self.assertTrue(len(error_handler._handlers[ConfigError]) > 0)

        # Trigger a default handler call
        error_handler.handle(ConfigError("Test config error"))

        # Check that error was logged multiple times
        self.assertEqual(mock_log_error.call_count, 2)

        # Verify the content of the first error log
        first_call = mock_log_error.call_args_list[0]
        self.assertIn("Error in unknown", first_call[0][0])

        # Verify the content of the second error log
        second_call = mock_log_error.call_args_list[1]
        self.assertIn("Configuration error", second_call[0][0])


if __name__ == "__main__":
    unittest.main()
