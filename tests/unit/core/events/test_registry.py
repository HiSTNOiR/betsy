"""
Unit tests for bot.core.events.registry module.

This module tests the event registry implementation.
"""

import unittest
from unittest import TestCase
from unittest.mock import MagicMock, patch

# Import the module under test
from bot.core.events.registry import (
    Event, EventRegistry, EventRegistryError, get_event_registry
)

# Suppress print output during tests
unittest.main.__defaults__ = (None, True, [], False)


class TestEvent(TestCase):
    """Test cases for Event class in registry module."""

    def test_event_creation(self):
        """Test creating an event."""
        # Create an event with minimal arguments
        event = Event(type="test_event", source="test")

        # Check that it has the expected attributes
        self.assertEqual(event.type, "test_event")
        self.assertEqual(event.source, "test")
        self.assertIsNotNone(event.timestamp)
        self.assertEqual(event.data, {})

    def test_event_with_data(self):
        """Test creating an event with data."""
        # Create an event with data
        data = {"key1": "value1", "key2": 123}
        event = Event(type="test_event", source="test", data=data)

        # Check that it has the expected data
        self.assertEqual(event.data, data)

    def test_get_type(self):
        """Test get_type method."""
        # Create an event
        event = Event(type="test_event", source="test")

        # Check get_type
        self.assertEqual(event.get_type(), "test_event")

    def test_get_data(self):
        """Test get_data method."""
        # Create an event with data
        data = {"key1": "value1", "key2": 123}
        event = Event(type="test_event", source="test", data=data)

        # Check get_data
        self.assertEqual(event.get_data(), data)

    def test_empty_type_validation(self):
        """Test that an event cannot be created with an empty type."""
        # Try to create an event with an empty type
        with self.assertRaises(ValueError):
            Event(type="", source="test")


class TestEventRegistry(TestCase):
    """Test cases for EventRegistry class."""

    def setUp(self):
        """Set up test environment."""
        self.registry = EventRegistry()

    def test_register_event_type(self):
        """Test registering an event type."""
        # Register an event type
        self.registry.register_event_type("test_event")

        # Check that it was registered
        self.assertIn("test_event", self.registry.get_registered_types())
        self.assertEqual(len(self.registry.get_handlers("test_event")), 0)

    def test_register_empty_event_type(self):
        """Test that an empty event type cannot be registered."""
        # Try to register an empty event type
        with self.assertRaises(EventRegistryError):
            self.registry.register_event_type("")

    def test_register_duplicate_event_type(self):
        """Test registering an event type that is already registered."""
        # Register an event type
        self.registry.register_event_type("test_event")

        # Register it again
        self.registry.register_event_type("test_event")

        # Check that it's still registered
        self.assertIn("test_event", self.registry.get_registered_types())

    def test_register_handler(self):
        """Test registering an event handler."""
        # Register an event type
        self.registry.register_event_type("test_event")

        # Create a handler
        def handler(event):
            pass

        # Register the handler
        self.registry.register_handler("test_event", handler)

        # Check that it was registered
        handlers = self.registry.get_handlers("test_event")
        self.assertEqual(len(handlers), 1)
        self.assertEqual(handlers[0], handler)

    def test_register_handler_for_unregistered_type(self):
        """Test registering a handler for an unregistered event type."""
        # Create a handler
        def handler(event):
            pass

        # Try to register for an unregistered type
        with self.assertRaises(EventRegistryError):
            self.registry.register_handler("unregistered_event", handler)

    def test_register_global_handler(self):
        """Test registering a global handler."""
        # Create a handler
        def handler(event):
            pass

        # Register as a global handler
        self.registry.register_handler(None, handler)

        # Check that it was registered
        global_handlers = self.registry.get_global_handlers()
        self.assertEqual(len(global_handlers), 1)
        self.assertEqual(global_handlers[0], handler)

    def test_unregister_handler(self):
        """Test unregistering an event handler."""
        # Register an event type
        self.registry.register_event_type("test_event")

        # Create a handler
        def handler(event):
            pass

        # Register the handler
        self.registry.register_handler("test_event", handler)

        # Unregister the handler
        result = self.registry.unregister_handler("test_event", handler)

        # Check that it was unregistered
        self.assertTrue(result)
        self.assertEqual(len(self.registry.get_handlers("test_event")), 0)

    def test_unregister_nonexistent_handler(self):
        """Test unregistering a handler that is not registered."""
        # Register an event type
        self.registry.register_event_type("test_event")

        # Create handlers
        def handler1(event):
            pass

        def handler2(event):
            pass

        # Register handler1
        self.registry.register_handler("test_event", handler1)

        # Try to unregister handler2
        result = self.registry.unregister_handler("test_event", handler2)

        # Check that the result is False
        self.assertFalse(result)
        self.assertEqual(len(self.registry.get_handlers("test_event")), 1)

    def test_unregister_global_handler(self):
        """Test unregistering a global handler."""
        # Create a handler
        def handler(event):
            pass

        # Register as a global handler
        self.registry.register_handler(None, handler)

        # Unregister the handler
        result = self.registry.unregister_handler(None, handler)

        # Check that it was unregistered
        self.assertTrue(result)
        self.assertEqual(len(self.registry.get_global_handlers()), 0)

    def test_clear(self):
        """Test clearing the registry."""
        # Register event types and handlers
        self.registry.register_event_type("test_event1")
        self.registry.register_event_type("test_event2")

        def handler1(event):
            pass

        def handler2(event):
            pass

        self.registry.register_handler("test_event1", handler1)
        self.registry.register_handler("test_event2", handler2)
        self.registry.register_handler(None, handler1)

        # Clear the registry
        self.registry.clear()

        # Check that everything was cleared
        self.assertEqual(len(self.registry.get_registered_types()), 0)
        self.assertEqual(len(self.registry.get_global_handlers()), 0)

    def test_get_handlers_for_unregistered_type(self):
        """Test getting handlers for an unregistered event type."""
        # Check that it returns an empty list
        handlers = self.registry.get_handlers("unregistered_event")
        self.assertEqual(len(handlers), 0)

    def test_initialise_with_package_paths(self):
        """Test initializing the registry with package paths."""
        # Mock package paths
        package_paths = ["bot.package1", "bot.package2"]

        # Call initialise
        self.registry.initialise(package_paths)

        # No assertions needed as the actual scanning logic is not implemented


class TestSingleton(TestCase):
    """Test cases for the registry singleton."""

    def test_get_event_registry(self):
        """Test that get_event_registry returns the singleton instance."""
        # Get the registry
        registry1 = get_event_registry()
        registry2 = get_event_registry()

        # Check that it's the same instance
        self.assertIs(registry1, registry2)


if __name__ == "__main__":
    unittest.main()
