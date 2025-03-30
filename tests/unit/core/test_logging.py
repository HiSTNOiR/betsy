"""
Unit tests for the bot's logging module.

This module tests the logging configuration functionality of the bot.
"""

import io
import logging
import os
import pathlib
import sys
import tempfile
import unittest
from unittest import mock
from unittest.mock import patch, MagicMock, call

# Import the module under test
from bot.core.logging import (
    LogLevel, LoggingError, ConfigurationError, HandlerError,
    validate_log_level, create_log_directory, create_formatter,
    add_console_handler, add_file_handler, setup_logging,
    get_module_logger, set_log_level, LoggerAdapter,
    get_context_logger, reset_logging
)


class TestLogLevelValidation(unittest.TestCase):
    """Tests for validate_log_level function."""

    def test_valid_integer_levels(self):
        """Test validation of valid integer logging levels."""
        self.assertEqual(validate_log_level(logging.DEBUG), logging.DEBUG)
        self.assertEqual(validate_log_level(logging.INFO), logging.INFO)
        self.assertEqual(validate_log_level(logging.WARNING), logging.WARNING)
        self.assertEqual(validate_log_level(logging.ERROR), logging.ERROR)
        self.assertEqual(validate_log_level(
            logging.CRITICAL), logging.CRITICAL)

        # Custom level should also work
        self.assertEqual(validate_log_level(15), 15)

    def test_valid_string_levels(self):
        """Test validation of valid string logging levels."""
        self.assertEqual(validate_log_level("DEBUG"), logging.DEBUG)
        self.assertEqual(validate_log_level("INFO"), logging.INFO)
        self.assertEqual(validate_log_level("WARNING"), logging.WARNING)
        self.assertEqual(validate_log_level("ERROR"), logging.ERROR)
        self.assertEqual(validate_log_level("CRITICAL"), logging.CRITICAL)

        # Should work with lowercase too
        self.assertEqual(validate_log_level("debug"), logging.DEBUG)
        self.assertEqual(validate_log_level("info"), logging.INFO)

    def test_invalid_integer_level(self):
        """Test validation rejects invalid integer levels."""
        with self.assertRaises(ConfigurationError):
            validate_log_level(-1)

        with self.assertRaises(ConfigurationError):
            validate_log_level(51)  # Standard levels only go up to 50

    def test_invalid_string_level(self):
        """Test validation rejects invalid string levels."""
        with self.assertRaises(ConfigurationError):
            validate_log_level("INVALID_LEVEL")

    def test_invalid_type(self):
        """Test validation rejects non-int/string types."""
        with self.assertRaises(ConfigurationError):
            validate_log_level(None)

        with self.assertRaises(ConfigurationError):
            validate_log_level([])

        with self.assertRaises(ConfigurationError):
            validate_log_level({})


class TestCreateLogDirectory(unittest.TestCase):
    """Tests for create_log_directory function."""

    def setUp(self):
        """Set up for tests."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

    def test_create_directory_with_log_file(self):
        """Test directory creation with a log file path."""
        log_file = os.path.join(self.temp_dir.name, "logs", "test.log")

        result = create_log_directory(log_file)

        self.assertTrue(os.path.exists(os.path.dirname(log_file)))
        self.assertEqual(result, pathlib.Path(log_file))

    def test_create_directory_with_logs_dir(self):
        """Test directory creation using LOGS_DIR."""
        with patch('bot.core.logging.LOGS_DIR', pathlib.Path(self.temp_dir.name)):
            result = create_log_directory()

            expected_path = pathlib.Path(self.temp_dir.name) / "bot.log"
            self.assertEqual(result, expected_path)

    def test_no_log_file_no_logs_dir(self):
        """Test no directory is created without log_file or LOGS_DIR."""
        with patch('bot.core.logging.LOGS_DIR', None):
            result = create_log_directory()

            self.assertIsNone(result)

    def test_permission_error(self):
        """Test error is raised on permission issue."""
        with patch('os.makedirs', side_effect=PermissionError("Permission denied")):
            with self.assertRaises(ConfigurationError) as context:
                create_log_directory("/some/path/test.log")

            self.assertIn("Permission denied", str(context.exception))


class TestCreateFormatter(unittest.TestCase):
    """Tests for create_formatter function."""

    def test_default_formatter(self):
        """Test creation of formatter with default values."""
        formatter = create_formatter()

        self.assertIsInstance(formatter, logging.Formatter)
        self.assertEqual(
            formatter._fmt, "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        self.assertEqual(formatter.datefmt, "%Y-%m-%d %H:%M:%S")

    def test_custom_formatter(self):
        """Test creation of formatter with custom values."""
        log_format = "%(levelname)s: %(message)s"
        date_format = "%H:%M:%S"

        formatter = create_formatter(log_format, date_format)

        self.assertIsInstance(formatter, logging.Formatter)
        self.assertEqual(formatter._fmt, log_format)
        self.assertEqual(formatter.datefmt, date_format)


class TestConsoleHandler(unittest.TestCase):
    """Tests for add_console_handler function."""

    def setUp(self):
        """Set up for tests."""
        self.logger = logging.getLogger("test_console_handler")
        self.logger.handlers = []  # Clear any existing handlers
        self.formatter = logging.Formatter("%(message)s")

    def test_add_console_handler(self):
        """Test adding a console handler to a logger."""
        add_console_handler(self.logger, self.formatter)

        # Verify a handler was added
        self.assertEqual(len(self.logger.handlers), 1)
        handler = self.logger.handlers[0]

        # Verify it's a StreamHandler with stdout as the stream
        self.assertIsInstance(handler, logging.StreamHandler)
        self.assertEqual(handler.stream, sys.stdout)

        # Verify formatter was set
        self.assertEqual(handler.formatter, self.formatter)

    def test_add_console_handler_with_level(self):
        """Test adding a console handler with a specific level."""
        add_console_handler(self.logger, self.formatter, logging.ERROR)

        handler = self.logger.handlers[0]
        self.assertEqual(handler.level, logging.ERROR)


class TestFileHandler(unittest.TestCase):
    """Tests for add_file_handler function."""

    def setUp(self):
        """Set up for tests."""
        # Use mkdtemp directly to avoid automatic cleanup that can cause issues
        self.temp_dir_path = tempfile.mkdtemp()

        self.log_file = os.path.join(self.temp_dir_path, "test.log")
        self.logger = logging.getLogger("test_file_handler")

        # Make sure to remove any existing handlers
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)

        self.formatter = logging.Formatter("%(message)s")

    def test_add_rotating_file_handler(self):
        """Test adding a rotating file handler."""
        try:
            handler = add_file_handler(
                self.logger,
                self.log_file,
                self.formatter,
                file_rotation=True,
                max_bytes=1000,
                backup_count=3
            )

            # Verify a handler was added
            self.assertEqual(len(self.logger.handlers), 1)

            # Verify it's a RotatingFileHandler
            self.assertIsInstance(
                handler, logging.handlers.RotatingFileHandler)

            # Verify properties
            self.assertEqual(handler.baseFilename, self.log_file)
            self.assertEqual(handler.maxBytes, 1000)
            self.assertEqual(handler.backupCount, 3)

            # Verify formatter
            self.assertEqual(handler.formatter, self.formatter)
        finally:
            # Make sure to close the handler
            for h in self.logger.handlers:
                h.close()
                self.logger.removeHandler(h)

    def test_add_timed_rotating_file_handler(self):
        """Test adding a timed rotating file handler."""
        try:
            handler = add_file_handler(
                self.logger,
                self.log_file,
                self.formatter,
                file_rotation=False,
                backup_count=5
            )

            # Verify a handler was added
            self.assertEqual(len(self.logger.handlers), 1)

            # Verify it's a TimedRotatingFileHandler
            self.assertIsInstance(
                handler, logging.handlers.TimedRotatingFileHandler)

            # Verify properties
            self.assertEqual(handler.baseFilename, self.log_file)
            self.assertEqual(handler.when, "midnight")
            self.assertEqual(handler.backupCount, 5)

            # Verify formatter
            self.assertEqual(handler.formatter, self.formatter)
        finally:
            # Make sure to close the handler
            for h in self.logger.handlers:
                h.close()
                self.logger.removeHandler(h)

    def test_add_file_handler_with_level(self):
        """Test adding a file handler with a specific level."""
        try:
            handler = add_file_handler(
                self.logger,
                self.log_file,
                self.formatter,
                level=logging.WARNING
            )

            self.assertEqual(handler.level, logging.WARNING)
        finally:
            # Make sure to close the handler
            for h in self.logger.handlers:
                h.close()
                self.logger.removeHandler(h)

    def test_file_handler_error(self):
        """Test error handling when adding a file handler fails."""
        with patch('logging.handlers.RotatingFileHandler', side_effect=PermissionError("Permission denied")):
            with self.assertRaises(HandlerError) as context:
                add_file_handler(
                    self.logger,
                    "/some/invalid/path/file.log",
                    self.formatter
                )

            self.assertIn("Permission denied", str(context.exception))

    def tearDown(self):
        """Clean up after tests."""
        # Make sure all handlers are closed
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)

        # Clean up temp directory
        try:
            import shutil
            shutil.rmtree(self.temp_dir_path, ignore_errors=True)
        except:
            pass


class TestSetupLogging(unittest.TestCase):
    """Tests for setup_logging function."""

    def setUp(self):
        """Set up for tests."""
        # Use mkdtemp directly to avoid automatic cleanup that can cause issues
        self.temp_dir_path = tempfile.mkdtemp()
        self.log_file = os.path.join(self.temp_dir_path, "test.log")

        # Save and reset root logger after each test
        self.root_logger = logging.getLogger()
        self.original_handlers = list(self.root_logger.handlers)
        self.original_level = self.root_logger.level

        # Clear handlers before each test
        for handler in self.root_logger.handlers[:]:
            handler.close()  # Properly close handlers
            self.root_logger.removeHandler(handler)

    def tearDown(self):
        """Clean up after tests."""
        # Restore original handlers and level
        for handler in self.root_logger.handlers[:]:
            handler.close()  # Properly close handlers
            self.root_logger.removeHandler(handler)

        for handler in self.original_handlers:
            self.root_logger.addHandler(handler)

        self.root_logger.setLevel(self.original_level)

        # Clean up temp directory
        try:
            import shutil
            shutil.rmtree(self.temp_dir_path, ignore_errors=True)
        except:
            pass

    @patch('bot.core.logging.add_console_handler')
    @patch('bot.core.logging.add_file_handler')
    def test_setup_logging_calls_handlers(self, mock_add_file, mock_add_console):
        """Test setup_logging calls the appropriate handler functions."""
        result = setup_logging(
            level=logging.DEBUG,
            log_file=self.log_file,
            console=True,
            file_rotation=True,
            max_bytes=2000,
            backup_count=4,
            log_format="%(levelname)s: %(message)s",
            date_format="%H:%M:%S"
        )

        # Verify root logger was returned
        self.assertEqual(result, self.root_logger)

        # Verify root logger level was set
        self.assertEqual(self.root_logger.level, logging.DEBUG)

        # Verify console handler was added
        mock_add_console.assert_called_once()

        # Verify file handler was added
        mock_add_file.assert_called_once()

        # Check formatter args (passed to both handlers)
        formatter_arg = mock_add_console.call_args[0][1]
        self.assertEqual(formatter_arg._fmt, "%(levelname)s: %(message)s")
        self.assertEqual(formatter_arg.datefmt, "%H:%M:%S")

    @patch('bot.core.logging.add_console_handler')
    @patch('bot.core.logging.add_file_handler')
    def test_setup_logging_with_specific_handler_levels(self, mock_add_file, mock_add_console):
        """Test setup_logging with specific levels for each handler."""
        setup_logging(
            level=logging.INFO,
            log_file=self.log_file,
            console_level=logging.DEBUG,
            file_level=logging.ERROR
        )

        # Verify root logger level
        self.assertEqual(self.root_logger.level, logging.INFO)

        # Check console handler level
        console_level_arg = mock_add_console.call_args[0][2]
        self.assertEqual(console_level_arg, logging.DEBUG)

        # Check file handler level
        file_level_arg = mock_add_file.call_args[0][6]
        self.assertEqual(file_level_arg, logging.ERROR)

    def test_setup_logging_without_file(self):
        """Test setup_logging without a log file."""
        with patch('bot.core.logging.LOGS_DIR', None):
            with patch('bot.core.logging.add_file_handler') as mock_add_file:
                setup_logging(console=True, log_file=None)

                # Verify file handler was not added
                mock_add_file.assert_not_called()

    def test_setup_logging_without_console(self):
        """Test setup_logging without console output."""
        with patch('bot.core.logging.add_console_handler') as mock_add_console:
            setup_logging(console=False, log_file=self.log_file)

            # Verify console handler was not added
            mock_add_console.assert_not_called()

    def test_setup_logging_error_propagation(self):
        """Test error propagation in setup_logging."""
        with patch('bot.core.logging.validate_log_level', side_effect=ConfigurationError("Invalid level")):
            with self.assertRaises(ConfigurationError) as context:
                setup_logging(level="INVALID")

            self.assertIn("Invalid level", str(context.exception))

    def test_setup_logging_other_exceptions(self):
        """Test handling of other exceptions in setup_logging."""
        with patch('bot.core.logging.validate_log_level', side_effect=RuntimeError("Unexpected error")):
            with self.assertRaises(LoggingError) as context:
                setup_logging()

            self.assertIn("Error setting up logging", str(context.exception))
            self.assertIn("Unexpected error", str(context.exception))


class TestGetModuleLogger(unittest.TestCase):
    """Tests for get_module_logger function."""

    def test_get_module_logger(self):
        """Test getting a logger for a module."""
        module_name = "test_module"
        logger = get_module_logger(module_name)

        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.name, module_name)


class TestSetLogLevel(unittest.TestCase):
    """Tests for set_log_level function."""

    def setUp(self):
        """Set up for tests."""
        # Create a test logger
        self.logger_name = "test_logger"
        self.logger = logging.getLogger(self.logger_name)
        self.original_level = self.logger.level

        # Save root logger level
        self.root_logger = logging.getLogger()
        self.root_original_level = self.root_logger.level

    def tearDown(self):
        """Clean up after tests."""
        # Restore original levels
        self.logger.setLevel(self.original_level)
        self.root_logger.setLevel(self.root_original_level)

    def test_set_log_level_named_logger(self):
        """Test setting log level for a named logger."""
        set_log_level(logging.ERROR, self.logger_name)
        self.assertEqual(self.logger.level, logging.ERROR)

    def test_set_log_level_root_logger(self):
        """Test setting log level for the root logger."""
        set_log_level(logging.WARNING)
        self.assertEqual(self.root_logger.level, logging.WARNING)

    def test_set_log_level_string(self):
        """Test setting log level using a string."""
        set_log_level("DEBUG", self.logger_name)
        self.assertEqual(self.logger.level, logging.DEBUG)

    @patch('bot.core.logging.validate_log_level')
    def test_set_log_level_validation(self, mock_validate):
        """Test that log level is validated."""
        mock_validate.return_value = logging.INFO

        set_log_level("INFO", self.logger_name)

        mock_validate.assert_called_once_with("INFO")
        self.assertEqual(self.logger.level, logging.INFO)


class TestLoggerAdapter(unittest.TestCase):
    """Tests for LoggerAdapter class."""

    def setUp(self):
        """Set up for tests."""
        self.logger = logging.getLogger("test_adapter")

        # Create a string IO to capture log output
        self.log_output = io.StringIO()
        handler = logging.StreamHandler(self.log_output)
        handler.setFormatter(logging.Formatter("%(message)s"))

        # Remove any existing handlers and add our test handler
        for h in self.logger.handlers[:]:
            h.close()
            self.logger.removeHandler(h)

        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    def test_logger_adapter_init(self):
        """Test LoggerAdapter initialization."""
        extra = {"user_id": "123", "command": "test"}

        adapter = LoggerAdapter(self.logger, extra)

        self.assertEqual(adapter.logger, self.logger)
        self.assertEqual(adapter.extra, extra)

    def test_logger_adapter_process(self):
        """Test LoggerAdapter message processing."""
        extra = {"user_id": "123", "command": "test"}
        adapter = LoggerAdapter(self.logger, extra)

        msg, kwargs = adapter.process("Test message", {})

        self.assertEqual(msg, "Test message [user_id=123 command=test]")
        self.assertEqual(kwargs, {})

    def test_logger_adapter_empty_extra(self):
        """Test LoggerAdapter with empty extra dict."""
        adapter = LoggerAdapter(self.logger, {})

        msg, kwargs = adapter.process("Test message", {})

        # Message should remain unchanged
        self.assertEqual(msg, "Test message")
        self.assertEqual(kwargs, {})

    def test_logger_adapter_log(self):
        """Test logging with LoggerAdapter."""
        adapter = LoggerAdapter(self.logger, {"user_id": "123"})

        adapter.info("Test info message")

        log_content = self.log_output.getvalue()
        self.assertIn("Test info message [user_id=123]", log_content)


class TestGetContextLogger(unittest.TestCase):
    """Tests for get_context_logger function."""

    def test_get_context_logger(self):
        """Test getting a context logger."""
        module_name = "test_context_module"
        context = {"user_id": "123", "command": "test"}

        logger = get_context_logger(module_name, **context)

        self.assertIsInstance(logger, LoggerAdapter)
        self.assertEqual(logger.logger.name, module_name)
        self.assertEqual(logger.extra, context)


class TestResetLogging(unittest.TestCase):
    """Tests for reset_logging function."""

    def setUp(self):
        """Set up for tests."""
        # Save original root logger state
        self.root_logger = logging.getLogger()
        self.original_handlers = list(self.root_logger.handlers)
        self.original_level = self.root_logger.level

        # Add a test handler
        self.test_handler = logging.StreamHandler()
        self.root_logger.addHandler(self.test_handler)
        self.root_logger.setLevel(logging.DEBUG)

    def tearDown(self):
        """Clean up after tests."""
        # Restore original handlers and level
        for handler in self.root_logger.handlers[:]:
            handler.close()  # Properly close handlers
            self.root_logger.removeHandler(handler)

        for handler in self.original_handlers:
            self.root_logger.addHandler(handler)

        self.root_logger.setLevel(self.original_level)

    def test_reset_logging(self):
        """Test resetting logging configuration."""
        # Verify test handler is present
        self.assertIn(self.test_handler, self.root_logger.handlers)
        self.assertEqual(self.root_logger.level, logging.DEBUG)

        # Reset logging
        reset_logging()

        # Verify test handler was removed
        self.assertNotIn(self.test_handler, self.root_logger.handlers)

        # Verify level was reset to default
        self.assertEqual(self.root_logger.level, logging.WARNING)


if __name__ == "__main__":
    unittest.main()
