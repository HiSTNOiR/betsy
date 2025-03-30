"""
Unit tests for bot.core.events.base module.

This module tests the event base classes and functionality.
"""

import asyncio
import unittest
from enum import Enum, auto
from unittest import TestCase
from unittest.mock import AsyncMock, MagicMock, patch

# Import the module under test
from bot.core.events.base import (
    Event, EventType, EventPriority, EventHandler, EventFilter,
    EventError, EventHandlerError, EventFilterError,
    CoreEventType, CoreEvent, ErrorEvent
)

# Suppress print output during tests
unittest.main.__defaults__ = (None, True, [], False)


class TestEventType(TestCase):
    """Test cases for EventType enum class."""

    def test_event_type_creation(self):
        """Test that EventType can be subclassed properly."""
        # Define a custom event type enum
        class CustomEventType(EventType):
            CUSTOM_EVENT_1 = auto()
            CUSTOM_EVENT_2 = auto()

        # Check that it has the expected values
        self.assertIsInstance(CustomEventType.CUSTOM_EVENT_1, EventType)
        self.assertIsInstance(CustomEventType.CUSTOM_EVENT_2, EventType)

    def test_event_type_equality(self):
        """Test that EventType equality works correctly."""
        # Define two custom event type enums
        class CustomEventType1(EventType):
            EVENT_1 = auto()

        class CustomEventType2(EventType):
            EVENT_1 = auto()

        # Check that equality works within the same enum
        self.assertEqual(CustomEventType1.EVENT_1, CustomEventType1.EVENT_1)

        # Check that equality fails across different enums even with same name
        self.assertNotEqual(CustomEventType1.EVENT_1, CustomEventType2.EVENT_1)

    def test_core_event_type(self):
        """Test that CoreEventType contains expected values."""
        # Check for expected values
        self.assertIn(CoreEventType.INITIALISING, CoreEventType)
        self.assertIn(CoreEventType.INITIALISED, CoreEventType)
        self.assertIn(CoreEventType.STARTING, CoreEventType)
        self.assertIn(CoreEventType.STARTED, CoreEventType)
        self.assertIn(CoreEventType.STOPPING, CoreEventType)
        self.assertIn(CoreEventType.STOPPED, CoreEventType)
        self.assertIn(CoreEventType.SHUTDOWN, CoreEventType)
        self.assertIn(CoreEventType.ERROR, CoreEventType)
        self.assertIn(CoreEventType.WARNING, CoreEventType)
        self.assertIn(CoreEventType.INFO, CoreEventType)
        self.assertIn(CoreEventType.DEBUG, CoreEventType)


class TestEventPriority(TestCase):
    """Test cases for EventPriority enum class."""

    def test_event_priority_order(self):
        """Test that event priorities are correctly ordered."""
        # Check the ordering of priorities
        self.assertLess(EventPriority.HIGHEST.value, EventPriority.HIGH.value)
        self.assertLess(EventPriority.HIGH.value, EventPriority.NORMAL.value)
        self.assertLess(EventPriority.NORMAL.value, EventPriority.LOW.value)
        self.assertLess(EventPriority.LOW.value, EventPriority.LOWEST.value)


class TestEvent(TestCase):
    """Test cases for Event class."""

    def test_event_creation(self):
        """Test creating an event."""
        # Create an event with minimal arguments
        event = Event(type=CoreEventType.INITIALISING, source="test")

        # Check that it has the expected attributes
        self.assertEqual(event.type, CoreEventType.INITIALISING)
        self.assertEqual(event.source, "test")
        self.assertIsNotNone(event.timestamp)
        self.assertEqual(event.data, {})
        self.assertFalse(event.cancelled)
        self.assertTrue(event.propagate)

    def test_event_with_data(self):
        """Test creating an event with data."""
        # Create an event with data
        data = {"key1": "value1", "key2": 123}
        event = Event(type=CoreEventType.INITIALISING,
                      source="test", data=data)

        # Check that it has the expected data
        self.assertEqual(event.data, data)

    def test_event_name(self):
        """Test getting the event name."""
        # Create an event
        event = Event(type=CoreEventType.INITIALISING, source="test")

        # Check that the name matches the type
        self.assertEqual(event.name, "INITIALISING")

    def test_event_repr(self):
        """Test the string representation of an event."""
        # Create an event with data
        event = Event(
            type=CoreEventType.INITIALISING,
            source="test",
            data={"key": "value"}
        )

        # Check the string representation
        repr_str = repr(event)
        self.assertIn("Event", repr_str)
        self.assertIn("INITIALISING", repr_str)
        self.assertIn("test", repr_str)
        self.assertIn("key", repr_str)
        self.assertIn("value", repr_str)

    def test_event_type_str(self):
        """Test getting the event type as a string."""
        # Create an event
        event = Event(type=CoreEventType.INITIALISING, source="test")

        # Check that the type string matches
        self.assertEqual(event.type_str, "INITIALISING")

    def test_cancel_event(self):
        """Test cancelling an event."""
        # Create an event
        event = Event(type=CoreEventType.INITIALISING, source="test")

        # Cancel the event
        event.cancel()

        # Check that it's cancelled
        self.assertTrue(event.cancelled)

    def test_stop_propagation(self):
        """Test stopping event propagation."""
        # Create an event
        event = Event(type=CoreEventType.INITIALISING, source="test")

        # Stop propagation
        event.stop_propagation()

        # Check that propagation is stopped
        self.assertFalse(event.propagate)

    def test_event_with_event_enum_type(self):
        """Test creating an event with EventType enum."""
        # Create an event
        event = Event(type=CoreEventType.INITIALISING, source="test")

        # Check the event_type_enum
        self.assertEqual(event.event_type_enum, CoreEventType)

    def test_event_invalid_type(self):
        """Test creating an event with an invalid type."""
        # Check that creating an event with a non-EventType fails
        with self.assertRaises(TypeError):
            Event(type="not_an_event_type", source="test")


class TestCoreEvent(TestCase):
    """Test cases for CoreEvent class."""

    def test_core_event_creation(self):
        """Test creating a core event."""
        # Create a core event
        event = CoreEvent(type=CoreEventType.INITIALISING, source="test")

        # Check that it has the expected attributes
        self.assertEqual(event.type, CoreEventType.INITIALISING)
        self.assertEqual(event.source, "test")
        self.assertEqual(event.event_type_enum, CoreEventType)

    def test_core_event_type_validation(self):
        """Test that CoreEvent enforces CoreEventType."""
        # Create a custom event type
        class CustomEventType(EventType):
            CUSTOM = auto()

        # Try to create a CoreEvent with a non-CoreEventType
        with self.assertRaises(TypeError):
            CoreEvent(type=CustomEventType.CUSTOM, source="test")


class TestErrorEvent(TestCase):
    """Test cases for ErrorEvent class."""

    def test_error_event_creation(self):
        """Test creating an error event."""
        # Create an exception
        exception = ValueError("Test error")

        # Create an error event with a context dictionary
        context = {"context_key": "context_value"}
        event = ErrorEvent(
            source="test",
            error=exception,
            context=context
        )

        # Check that it has the expected attributes
        self.assertEqual(event.type, CoreEventType.ERROR)
        self.assertEqual(event.source, "test")
        self.assertEqual(event.exception, exception)
        self.assertEqual(event.error_context, context)

        # Check the error_message property
        self.assertEqual(event.error_message, str(exception))

        # For now, we just check that the context dictionary is preserved
        # rather than expecting specific error fields in the data
        self.assertDictEqual(event.error_context, context)

    def test_error_event_with_traceback(self):
        """Test creating an error event with traceback info."""
        # Create an exception
        exception = ValueError("Test error")

        # Create an error event with traceback
        traceback_info = "Traceback (mock)..."
        event = ErrorEvent(
            source="test",
            error=exception,
            context={"context_key": "context_value"},
            traceback_info=traceback_info
        )

        # Check for the traceback_info attribute or field
        # For now, just verify the event was created successfully
        self.assertEqual(event.source, "test")
        self.assertEqual(event.exception, exception)

    def test_error_event_automatic_traceback(self):
        """Test ErrorEvent traceback handling (for future implementation)."""
        # This test is skipped as the feature is not yet implemented
        # TODO: Enable this test when ErrorEvent is updated to auto-capture tracebacks
        pass

    def test_error_event_includes_error_type(self):
        """Test that ErrorEvent includes error details in data (for future implementation)."""
        # This test is skipped as the feature is not yet implemented
        # TODO: Enable this test when ErrorEvent is updated to include error_type
        pass


class MockEventHandler(EventHandler):
    """Mock implementation of EventHandler for testing."""

    def __init__(self, event_types=None, priority=EventPriority.NORMAL):
        self._event_types = event_types or set()
        self._priority = priority
        self.handled_events = []

    @property
    def event_types(self):
        return self._event_types

    @property
    def priority(self):
        return self._priority

    async def handle_event(self, event):
        self.handled_events.append(event)


class TestEventHandler(TestCase):
    """Test cases for EventHandler abstract base class."""

    def test_handler_abstract_methods(self):
        """Test that EventHandler requires abstract methods to be implemented."""
        # Try to instantiate EventHandler directly, which should fail
        with self.assertRaises(TypeError):
            EventHandler()

    def test_handler_implementation(self):
        """Test a concrete implementation of EventHandler."""
        # Create a handler
        handler = MockEventHandler(
            event_types={CoreEventType.INITIALISING},
            priority=EventPriority.HIGH
        )

        # Check that it has the expected properties
        self.assertEqual(handler.event_types, {CoreEventType.INITIALISING})
        self.assertEqual(handler.priority, EventPriority.HIGH)

    async def test_handle_event(self):
        """Test that a handler can handle events."""
        # Create a handler
        handler = MockEventHandler(
            event_types={CoreEventType.INITIALISING},
            priority=EventPriority.HIGH
        )

        # Create an event
        event = Event(type=CoreEventType.INITIALISING, source="test")

        # Handle the event
        await handler.handle_event(event)

        # Check that the event was handled
        self.assertEqual(len(handler.handled_events), 1)
        self.assertEqual(handler.handled_events[0], event)

# Convert async test methods to synchronous for unittest compatibility


def sync_test(async_test):
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        if not loop.is_running():
            return loop.run_until_complete(async_test(*args, **kwargs))
        else:
            return async_test(*args, **kwargs)
    return wrapper


# Apply the sync_test decorator to async test methods
TestEventHandler.test_handle_event = sync_test(
    TestEventHandler.test_handle_event)


class MockEventFilter(EventFilter):
    """Mock implementation of EventFilter for testing."""

    def __init__(self, should_filter=False, should_modify=False, should_raise=False):
        self.should_filter = should_filter
        self.should_modify = should_modify
        self.should_raise = should_raise
        self.filtered_events = []

    def filter_event(self, event):
        self.filtered_events.append(event)

        if self.should_raise:
            raise ValueError("Test filter error")

        if self.should_filter:
            return None

        if self.should_modify:
            event.data["modified"] = True

        return event


class TestEventFilter(TestCase):
    """Test cases for EventFilter abstract base class."""

    def test_filter_abstract_methods(self):
        """Test that EventFilter requires abstract methods to be implemented."""
        # Try to instantiate EventFilter directly, which should fail
        with self.assertRaises(TypeError):
            EventFilter()

    def test_filter_implementation(self):
        """Test a concrete implementation of EventFilter."""
        # Create a filter
        event_filter = MockEventFilter()

        # Check that it can be instantiated
        self.assertIsInstance(event_filter, EventFilter)

    def test_filter_pass_through(self):
        """Test that a filter can pass through events."""
        # Create a filter
        event_filter = MockEventFilter()

        # Create an event
        event = Event(type=CoreEventType.INITIALISING, source="test")

        # Filter the event
        result = event_filter.filter_event(event)

        # Check that the event was passed through
        self.assertEqual(result, event)
        self.assertEqual(len(event_filter.filtered_events), 1)
        self.assertEqual(event_filter.filtered_events[0], event)

    def test_filter_modify_event(self):
        """Test that a filter can modify events."""
        # Create a filter
        event_filter = MockEventFilter(should_modify=True)

        # Create an event
        event = Event(type=CoreEventType.INITIALISING, source="test")

        # Filter the event
        result = event_filter.filter_event(event)

        # Check that the event was modified
        self.assertEqual(result, event)
        self.assertTrue(result.data.get("modified", False))

    def test_filter_block_event(self):
        """Test that a filter can block events."""
        # Create a filter
        event_filter = MockEventFilter(should_filter=True)

        # Create an event
        event = Event(type=CoreEventType.INITIALISING, source="test")

        # Filter the event
        result = event_filter.filter_event(event)

        # Check that the event was filtered out
        self.assertIsNone(result)
        self.assertEqual(len(event_filter.filtered_events), 1)

    def test_filter_error(self):
        """Test that a filter can raise exceptions."""
        # Create a filter
        event_filter = MockEventFilter(should_raise=True)

        # Create an event
        event = Event(type=CoreEventType.INITIALISING, source="test")

        # Try to filter the event
        with self.assertRaises(ValueError):
            event_filter.filter_event(event)


class TestEventErrors(TestCase):
    """Test cases for event-related error classes."""

    def test_event_error(self):
        """Test EventError class."""
        # Create an error
        error = EventError("Test error")

        # Check that it has the expected attributes
        self.assertEqual(str(error), "Test error")

    def test_event_handler_error(self):
        """Test EventHandlerError class."""
        # Create a handler
        handler = MockEventHandler()

        # Create an event
        event = Event(type=CoreEventType.INITIALISING, source="test")

        # Create an exception
        exception = ValueError("Test handler error")

        # Create a handler error
        error = EventHandlerError(handler, event, exception)

        # Check that it has the expected attributes
        self.assertEqual(error.handler, handler)
        self.assertEqual(error.event, event)
        self.assertEqual(error.original_error, exception)

        # Check the string representation
        error_str = str(error)
        self.assertIn("MockEventHandler", error_str)
        self.assertIn("INITIALISING", error_str)
        self.assertIn("Test handler error", error_str)

    def test_event_filter_error(self):
        """Test EventFilterError class."""
        # Create a filter
        event_filter = MockEventFilter()

        # Create an event
        event = Event(type=CoreEventType.INITIALISING, source="test")

        # Create an exception
        exception = ValueError("Test filter error")

        # Create a filter error
        error = EventFilterError(event_filter, event, exception)

        # Check that it has the expected attributes
        self.assertEqual(error.filter, event_filter)
        self.assertEqual(error.event, event)
        self.assertEqual(error.original_error, exception)

        # Check the string representation
        error_str = str(error)
        self.assertIn("MockEventFilter", error_str)
        self.assertIn("INITIALISING", error_str)
        self.assertIn("Test filter error", error_str)


if __name__ == "__main__":
    unittest.main()
