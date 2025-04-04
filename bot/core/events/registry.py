"""
Event registry for the bot.

This module provides a registry for events and event handlers.
"""

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Callable, TypeVar

# Set up logger for this module
logger = logging.getLogger(__name__)

# Type variable for type hinting event types
T = TypeVar('T', bound='Event')


class EventRegistryError(Exception):
    """Base exception for registry-related errors."""
    pass


@dataclass
class Event:
    """
    Base class for all events.

    Events are used to communicate between different parts of the application.
    """
    type: str
    source: Optional[str] = None
    timestamp: Optional[float] = None
    data: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate and initialise the event after creation."""
        if not self.type:
            raise ValueError("Event type cannot be empty")

        # Set timestamp if not provided
        if self.timestamp is None:
            import time
            self.timestamp = time.time()

    def get_type(self) -> str:
        """
        Get the event type.

        Returns:
            str: Event type.
        """
        return self.type

    def get_data(self) -> Dict[str, Any]:
        """
        Get the event data.

        Returns:
            Dict[str, Any]: Event data.
        """
        return self.data


class EventRegistry:
    """
    Registry for events and event handlers.

    The registry maintains a mapping of event types to handler functions.
    """

    def __init__(self):
        """Initialise the event registry."""
        self._handlers: Dict[str, List[Callable[[Event], None]]] = {}
        self._global_handlers: List[Callable[[Event], None]] = []
        self._event_types: Set[str] = set()

    def register_event_type(self, event_type: str) -> None:
        """
        Register an event type.

        Args:
            event_type (str): Event type to register.

        Raises:
            EventRegistryError: If the event type is already registered.
        """
        if not event_type:
            raise EventRegistryError("Event type cannot be empty")

        if event_type in self._event_types:
            logger.warning(f"Event type already registered: {event_type}")
            return

        self._event_types.add(event_type)
        self._handlers[event_type] = []
        logger.debug(f"Registered event type: {event_type}")

    def register_handler(
        self,
        event_type: Optional[str],
        handler: Callable[[Event], None]
    ) -> None:
        """
        Register an event handler.

        Args:
            event_type (Optional[str]): Event type to handle. If None, registers a global handler.
            handler (Callable[[Event], None]): Handler function.

        Raises:
            EventRegistryError: If the event type is not registered.
        """
        if event_type is None:
            # Register a global handler
            self._global_handlers.append(handler)
            logger.debug(
                f"Registered global event handler: {handler.__name__}")
            return

        if event_type not in self._event_types:
            raise EventRegistryError(
                f"Event type not registered: {event_type}")

        self._handlers[event_type].append(handler)
        logger.debug(
            f"Registered handler for event type {event_type}: {handler.__name__}")

    def unregister_handler(
        self,
        event_type: Optional[str],
        handler: Callable[[Event], None]
    ) -> bool:
        """
        Unregister an event handler.

        Args:
            event_type (Optional[str]): Event type. If None, unregisters from global handlers.
            handler (Callable[[Event], None]): Handler function.

        Returns:
            bool: True if the handler was unregistered, False otherwise.
        """
        if event_type is None:
            # Unregister from global handlers
            if handler in self._global_handlers:
                self._global_handlers.remove(handler)
                logger.debug(
                    f"Unregistered global event handler: {handler.__name__}")
                return True
            return False

        if event_type not in self._event_types:
            logger.warning(f"Event type not registered: {event_type}")
            return False

        if handler in self._handlers[event_type]:
            self._handlers[event_type].remove(handler)
            logger.debug(
                f"Unregistered handler for event type {event_type}: {handler.__name__}")
            return True

        return False

    def get_handlers(self, event_type: str) -> List[Callable[[Event], None]]:
        """
        Get all handlers for an event type.

        Args:
            event_type (str): Event type.

        Returns:
            List[Callable[[Event], None]]: List of handler functions.
        """
        if event_type not in self._event_types:
            return []

        return self._handlers[event_type].copy()

    def get_global_handlers(self) -> List[Callable[[Event], None]]:
        """
        Get all global handlers.

        Returns:
            List[Callable[[Event], None]]: List of global handler functions.
        """
        return self._global_handlers.copy()

    def clear(self) -> None:
        """Clear all registered event types and handlers."""
        self._handlers = {}
        self._global_handlers = []
        self._event_types = set()
        logger.debug("Cleared event registry")

    def get_registered_types(self) -> Set[str]:
        """
        Get all registered event types.

        Returns:
            Set[str]: Set of registered event types.
        """
        return self._event_types.copy()

    def initialise(self, package_paths: Optional[List[str]] = None) -> None:
        """
        Initialise the event registry by scanning packages for events.

        Args:
            package_paths (Optional[List[str]]): List of package paths to scan for events.

        Raises:
            EventRegistryError: If there is an error initializing the registry.
        """
        try:
            if not package_paths:
                logger.info(
                    "No package paths provided, skipping event discovery")
                return

            for package_path in package_paths:
                logger.debug(f"Scanning package for events: {package_path}")
                # Implement package scanning logic here

            logger.info("Event registry initialised")
        except Exception as e:
            error_msg = f"Error initializing event registry: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise EventRegistryError(error_msg) from e


# Singleton instance of the event registry
_event_registry = EventRegistry()


def get_event_registry() -> EventRegistry:
    """
    Get the singleton event registry instance.

    Returns:
        EventRegistry: Singleton event registry instance.
    """
    return _event_registry
