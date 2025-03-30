"""
Unit tests for bot.core.events.handlers module.

This module tests the event handlers implementation.
"""

import unittest
from unittest import TestCase
from unittest.mock import MagicMock, patch
import logging

# Import the module under test
from bot.core.events.handlers import (
    LoggingEventHandler,
    ErrorEventHandler,
    LifecycleEventHandler,
    register_global_handlers
)

# Import dependencies for testing
from bot.core.events.base import (
    Event,
    CoreEventType,
    ErrorEvent,
    EventPriority
)
from bot.core.errors import ErrorContext

# Suppress print output during tests
unittest.main.__defaults__ = (None, True, [], False)


class TestLoggingEventHandler(TestCase):
    """Test cases for LoggingEventHandler."""

    def setUp(self):
        """Set up test environment."""
        self.handler = LoggingEventHandler(level=logging.DEBUG)

    def test_event_types(self):
        """Test that event types is an empty set (handles all events)."""
        self.assertEqual(self.handler.event_types, set())

    def test_priority(self):
        """Test that the priority is HIGH."""
        self.assertEqual(self.handler.priority, EventPriority.HIGH)

    @patch('logging.log')
    async def test_handle_event(self, mock_log):
        """Test handling an event logs the correct information."""
        # Create a test event
        event = Event(type=CoreEventType.INITIALISING,
                      source="test_source", data={"key": "value"})

        # Call handle_event
        await self.handler.handle_event(event)

        # Verify logging
        mock_log.assert_called_once_with(
            logging.DEBUG,
            f"Event received: {event.name} from {event.source} with data: {event.data}"
        )


class TestErrorEventHandler(TestCase):
    """Test cases for ErrorEventHandler."""

    def setUp(self):
        """Set up test environment."""
        self.handler = ErrorEventHandler()

    def test_event_types(self):
        """Test that event types contains only ERROR event type."""
        self.assertEqual(self.handler.event_types, {CoreEventType.ERROR})

    def test_priority(self):
        """Test that the priority is HIGHEST."""
        self.assertEqual(self.handler.priority, EventPriority.HIGHEST)

    @patch('bot.core.events.handlers.get_error_handler')
    @patch('logging.error')
    async def test_handle_error_event(self, mock_log_error, mock_get_error_handler):
        """Test handling a valid error event."""
        # Create a mock error handler
        mock_error_handler = MagicMock()
        mock_get_error_handler.return_value = mock_error_handler

        # Create a test exception
        test_exception = ValueError("Test error")

        # Create an error event
        error_event = ErrorEvent(
            source="test_source",
            error=test_exception,
            context={"context_key": "context_value"},
            traceback_info="Test traceback"
        )

        # Call handle_event
        await self.handler.handle_event(error_event)

        # Verify logging
        mock_log_error.assert_called_once_with(
            f"Error event received from {error_event.source}: {str(test_exception)}"
        )

        # Verify error handler called
        mock_error_handler.handle.assert_called_once()

        # Check the error context passed to the handler
        context = mock_error_handler.handle.call_args[0][1]
        self.assertIsInstance(context, ErrorContext)
        self.assertEqual(context.error, test_exception)
        self.assertEqual(context.source, "test_source")
        self.assertEqual(context.context, {"context_key": "context_value"})

    @patch('logging.warning')
    async def test_handle_non_error_event(self, mock_log_warning):
        """Test handling a non-error event."""
        # Create a non-error event
        event = Event(type=CoreEventType.INITIALISING, source="test_source")

        # Call handle_event
        await self.handler.handle_event(event)

        # Verify warning logged
        mock_log_warning.assert_called_once_with(
            f"Non-ErrorEvent received in ErrorEventHandler: {event.name}"
        )

    @patch('logging.error')
    async def test_handle_event_error(self, mock_log_error):
        """Test error handling within the event handler itself."""
        # Create an error event that will cause an exception
        class BrokenErrorEvent(ErrorEvent):
            def __init__(self):
                super().__init__()
                # Cause exception by making exception None but still requiring it
                self.exception = None

        # Call handle_event with a problematic event
        await self.handler.handle_event(BrokenErrorEvent())

        # Verify that the error is logged
        mock_log_error.assert_called_once()


class TestLifecycleEventHandler(TestCase):
    """Test cases for LifecycleEventHandler."""

    def setUp(self):
        """Set up test environment."""
        self.handler = LifecycleEventHandler()

    def test_event_types(self):
        """Test that event types contains all lifecycle event types."""
        expected_types = {
            CoreEventType.INITIALISING,
            CoreEventType.INITIALISED,
            CoreEventType.STARTING,
            CoreEventType.STARTED,
            CoreEventType.STOPPING,
            CoreEventType.STOPPED,
            CoreEventType.SHUTDOWN
        }
        self.assertEqual(self.handler.event_types, expected_types)

    def test_priority(self):
        """Test that the priority is NORMAL."""
        self.assertEqual(self.handler.priority, EventPriority.NORMAL)

    @patch('logging.info')
    async def test_handle_lifecycle_events(self, mock_log_info):
        """Test handling all lifecycle events."""
        lifecycle_events = [
            (CoreEventType.INITIALISING, "System is initialising"),
            (CoreEventType.INITIALISED, "System initialisation complete"),
            (CoreEventType.STARTING, "System is starting"),
            (CoreEventType.STARTED, "System startup complete"),
            (CoreEventType.STOPPING, "System is stopping"),
            (CoreEventType.STOPPED, "System has stopped"),
            (CoreEventType.SHUTDOWN, "System is shutting down")
        ]

        for event_type, expected_log in lifecycle_events:
            # Create an event
            event = Event(type=event_type, source="test_source")

            # Reset mock
            mock_log_info.reset_mock()

            # Call handle_event
            await self.handler.handle_event(event)

            # Verify logging
            mock_log_info.assert_any_call(
                f"Lifecycle event: {event.name} from {event.source}"
            )
            mock_log_info.assert_any_call(expected_log)


class TestRegisterGlobalHandlers(TestCase):
    """Test cases for register_global_handlers function."""

    @patch('bot.core.events.dispatcher.get_event_dispatcher')
    @patch('bot.core.events.handlers.logger')
    def test_register_global_handlers(self, mock_logger, mock_get_dispatcher):
        """Test registering global handlers."""
        # Create a mock dispatcher
        mock_dispatcher = MagicMock()
        mock_get_dispatcher.return_value = mock_dispatcher

        # Call the function
        register_global_handlers()

        # Verify handlers registered
        self.assertEqual(mock_dispatcher.register_handler.call_count, 3)

        # Verify logging
        mock_logger.info.assert_called_once_with(
            "Global event handlers registered")


if __name__ == "__main__":
    unittest.main()
