"""
Unit tests for bot.core.events.dispatcher module.

This module tests the event dispatcher implementation.
"""

import unittest
import asyncio
from unittest import TestCase
from unittest.mock import AsyncMock, MagicMock, patch

# Import the module under test
from bot.core.events.dispatcher import (
    EventDispatcher, get_event_dispatcher
)
from bot.core.events.base import (
    Event, EventType, EventHandler, EventFilter, EventPriority, CoreEventType
)

# Suppress print output during tests
unittest.main.__defaults__ = (None, True, [], False)


# Mock event type for testing
class TestEventType(EventType):
    TEST_EVENT = 1
    ANOTHER_TEST_EVENT = 2


# Mock event handler for testing
class MockEventHandler(EventHandler):
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


# Mock event filter for testing
class MockEventFilter(EventFilter):
    def __init__(self, pass_through=True):
        self.pass_through = pass_through
        self.filtered_events = []

    def filter_event(self, event):
        self.filtered_events.append(event)
        return event if self.pass_through else None


class CustomTestRunner(unittest.TextTestRunner):
    """
    Custom test runner that supports async test methods.
    """

    def run(self, test):
        """Run the given test case or test suite."""
        result = self._makeResult()

        # Wrap the test in a method that handles async tests
        def run_test(test):
            if hasattr(test, 'run_async'):
                # For async test methods
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    loop.run_until_complete(test.run_async())
                finally:
                    loop.close()
            else:
                # For regular sync test methods
                test(result)

        test(result)
        return result


class AsyncTestCase(TestCase):
    """Base class for async test cases."""

    def __init__(self, methodName='runTest'):
        """
        Initialise the test case with a method name.

        This ensures the dispatcher is created for each test method.
        """
        super().__init__(methodName)
        self.dispatcher = None

    def setUp(self):
        """Set up test environment before each test method."""
        self.dispatcher = EventDispatcher()

    def run(self, result=None):
        """
        Override the run method to support async test methods.

        This method wraps async test methods to run them in an event loop.
        """
        # Check if the test method is async
        test_method = getattr(self, self._testMethodName)
        if asyncio.iscoroutinefunction(test_method):
            # Add a run_async method that will be called by our custom runner
            def run_async():
                return test_method()

            self.run_async = run_async

        # Call the parent class's run method
        return super().run(result)


class TestEventDispatcher(AsyncTestCase):
    """Test cases for EventDispatcher class."""

    async def test_publish_and_process_event(self):
        """Test publishing and processing an event."""
        # Create a mock handler
        handler = MockEventHandler(event_types={TestEventType.TEST_EVENT})
        self.dispatcher.register_handler(handler)

        # Create an event
        event = Event(type=TestEventType.TEST_EVENT, source="test_source")

        # Start processing and publish the event
        await self.dispatcher.start_processing()
        await self.dispatcher.publish(event)

        # Wait a moment for processing
        await asyncio.sleep(0.1)

        # Stop processing
        await self.dispatcher.stop_processing()

        # Check that the event was handled
        self.assertEqual(len(handler.handled_events), 1)
        self.assertEqual(handler.handled_events[0], event)

    async def test_publish_now(self):
        """Test publishing and processing an event immediately."""
        # Create a mock handler
        handler = MockEventHandler(event_types={TestEventType.TEST_EVENT})
        self.dispatcher.register_handler(handler)

        # Create an event
        event = Event(type=TestEventType.TEST_EVENT, source="test_source")

        # Publish now
        await self.dispatcher.publish_now(event)

        # Check that the event was handled
        self.assertEqual(len(handler.handled_events), 1)
        self.assertEqual(handler.handled_events[0], event)

    async def test_generic_handler(self):
        """Test registering a generic handler that handles all events."""
        # Create a generic handler
        handler = MockEventHandler()
        self.dispatcher.register_handler(handler)

        # Create an event
        event = Event(type=TestEventType.TEST_EVENT, source="test_source")

        # Start processing and publish the event
        await self.dispatcher.start_processing()
        await self.dispatcher.publish(event)

        # Wait a moment for processing
        await asyncio.sleep(0.1)

        # Stop processing
        await self.dispatcher.stop_processing()

        # Check that the event was handled
        self.assertEqual(len(handler.handled_events), 1)
        self.assertEqual(handler.handled_events[0], event)

    async def test_event_filter(self):
        """Test event filtering."""
        # Create a filter that passes the event
        passing_filter = MockEventFilter(pass_through=True)
        self.dispatcher.register_filter(passing_filter)

        # Create a handler
        handler = MockEventHandler(event_types={TestEventType.TEST_EVENT})
        self.dispatcher.register_handler(handler)

        # Create an event
        event = Event(type=TestEventType.TEST_EVENT, source="test_source")

        # Start processing and publish the event
        await self.dispatcher.start_processing()
        await self.dispatcher.publish(event)

        # Wait a moment for processing
        await asyncio.sleep(0.1)

        # Stop processing
        await self.dispatcher.stop_processing()

        # Check filter and handler
        self.assertEqual(len(passing_filter.filtered_events), 1)
        self.assertEqual(len(handler.handled_events), 1)

    def test_handler_priority(self):
        """Test handler priority order."""
        # Create multiple handlers with different priorities
        highest_priority_handler = MockEventHandler(
            event_types={TestEventType.TEST_EVENT},
            priority=EventPriority.HIGHEST
        )
        high_priority_handler = MockEventHandler(
            event_types={TestEventType.TEST_EVENT},
            priority=EventPriority.HIGH
        )
        normal_priority_handler = MockEventHandler(
            event_types={TestEventType.TEST_EVENT},
            priority=EventPriority.NORMAL
        )
        low_priority_handler = MockEventHandler(
            event_types={TestEventType.TEST_EVENT},
            priority=EventPriority.LOW
        )
        lowest_priority_handler = MockEventHandler(
            event_types={TestEventType.TEST_EVENT},
            priority=EventPriority.LOWEST
        )

        # Register handlers in a random order
        handlers_to_register = [
            low_priority_handler,
            normal_priority_handler,
            highest_priority_handler,
            lowest_priority_handler,
            high_priority_handler
        ]
        for handler in handlers_to_register:
            self.dispatcher.register_handler(handler)

        # Directly get and check handlers to verify priority
        event = Event(type=TestEventType.TEST_EVENT)
        handlers = self.dispatcher._get_handlers_for_event(event)

        # Check that the handlers are sorted correctly
        self.assertEqual(len(handlers), 5)

        # Verify the sorting order based on priority value
        expected_priorities = [
            EventPriority.HIGHEST,
            EventPriority.HIGH,
            EventPriority.NORMAL,
            EventPriority.LOW,
            EventPriority.LOWEST
        ]

        # Verify sorting and priorities
        for i, (expected_priority, handler) in enumerate(zip(expected_priorities, handlers)):
            self.assertEqual(
                handler.priority,
                expected_priority,
                f"Handler at index {i} does not have the expected priority. "
                f"Expected {expected_priority}, got {handler.priority}"
            )

        # Additional verification of sorting
        self.assertTrue(
            all(
                handlers[i].priority.value <= handlers[i+1].priority.value
                for i in range(len(handlers)-1)
            ),
            "Handlers are not sorted in ascending order of priority value"
        )

    def test_unregister_handler(self):
        """Test unregistering a handler."""
        # Create a handler
        handler = MockEventHandler(event_types={TestEventType.TEST_EVENT})
        self.dispatcher.register_handler(handler)

        # Unregister the handler
        self.dispatcher.unregister_handler(handler)

        # Check that no handlers exist for the event type
        handlers = self.dispatcher._get_handlers_for_event(
            Event(type=TestEventType.TEST_EVENT)
        )
        self.assertEqual(len(handlers), 0)

    def test_unregister_filter(self):
        """Test unregistering a filter."""
        # Create a filter
        event_filter = MockEventFilter()
        self.dispatcher.register_filter(event_filter)

        # Unregister the filter
        self.dispatcher.unregister_filter(event_filter)

        # Check that no filters remain
        self.assertEqual(len(self.dispatcher._filters), 0)

    def test_clear_handlers(self):
        """Test clearing all handlers."""
        # Register some handlers
        handler1 = MockEventHandler(event_types={TestEventType.TEST_EVENT})
        handler2 = MockEventHandler(
            event_types={TestEventType.ANOTHER_TEST_EVENT})
        generic_handler = MockEventHandler()

        self.dispatcher.register_handler(handler1)
        self.dispatcher.register_handler(handler2)
        self.dispatcher.register_handler(generic_handler)

        # Clear handlers
        self.dispatcher.clear_handlers()

        # Check that all handlers are removed
        self.assertEqual(len(self.dispatcher._handlers), 0)
        self.assertEqual(len(self.dispatcher._generic_handlers), 0)

    def test_clear_filters(self):
        """Test clearing all filters."""
        # Register some filters
        filter1 = MockEventFilter()
        filter2 = MockEventFilter()

        self.dispatcher.register_filter(filter1)
        self.dispatcher.register_filter(filter2)

        # Clear filters
        self.dispatcher.clear_filters()

        # Check that all filters are removed
        self.assertEqual(len(self.dispatcher._filters), 0)

    def test_get_queue_size(self):
        """Test getting the event queue size."""
        # The initial queue size should be 0
        self.assertEqual(self.dispatcher.get_queue_size(), 0)


class TestSingleton(TestCase):
    """Test cases for the dispatcher singleton."""

    def test_get_event_dispatcher(self):
        """Test that get_event_dispatcher returns the singleton instance."""
        # Get the dispatcher
        dispatcher1 = get_event_dispatcher()
        dispatcher2 = get_event_dispatcher()

        # Check that it's the same instance
        self.assertIs(dispatcher1, dispatcher2)


if __name__ == "__main__":
    # Use a custom test runner that supports async tests
    runner = CustomTestRunner()
    suite = unittest.TestLoader().loadTestsFromModule(__import__(__name__))
    runner.run(suite)
