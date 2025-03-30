"""
Base event classes for the bot.

This module provides the base Event class and related helpers for the event system.
Events are used for communication between different components of the application without
direct dependencies.
"""

from bot.core.events.base import Event, EventType
from typing import Any, Dict, List, Optional, Set, Type, TypeVar, cast
from enum import Enum
import pkgutil
import logging
import inspect
import importlib
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Dict, Optional, Type, TypeVar, Generic, Union, ClassVar

from bot.utils.time import get_utc_now


class EventType(Enum):
    """
    Base class for event type enumerations.

    Each event category should define its own EventType enum subclass.
    """
    pass


class EventPriority(Enum):
    """
    Priority levels for event handlers.

    Handlers with higher priority (lower numerical value) are executed first.
    """
    HIGHEST = 0
    HIGH = 100
    NORMAL = 200
    LOW = 300
    LOWEST = 400


T = TypeVar('T', bound=EventType)


@dataclass
class Event(Generic[T]):
    """
    Base class for all events.

    Events are the primary means of communication between loosely coupled components.
    Each event has a type, an optional source identifier, and arbitrary data.
    """
    type: T
    source: str = ""
    data: Dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=get_utc_now)
    cancelled: bool = False
    propagate: bool = True

    # Class-level type hint for inheritance
    event_type_enum: ClassVar[Type[EventType]] = EventType

    def __post_init__(self) -> None:
        """Validate the event after initialisation."""
        if not isinstance(self.type, self.event_type_enum):
            raise TypeError(
                f"Event type must be an instance of {self.event_type_enum.__name__}")

    def cancel(self) -> None:
        """Cancel the event to prevent further processing."""
        self.cancelled = True

    def stop_propagation(self) -> None:
        """Stop event propagation to lower-priority handlers."""
        self.propagate = False

    @property
    def name(self) -> str:
        """Get the name of the event type."""
        return self.type.name

    def clone(self) -> 'Event':
        """Create a copy of this event with a new ID."""
        return type(self)(
            type=self.type,
            source=self.source,
            data=self.data.copy(),
            timestamp=self.timestamp,
        )


class EventHandler(ABC):
    """
    Abstract base class for event handlers.

    Event handlers process events of specific types and can be registered with the
    event dispatcher.
    """

    @abstractmethod
    async def handle_event(self, event: Event) -> None:
        """
        Handle an event.

        Args:
            event (Event): The event to handle.
        """
        pass

    @property
    @abstractmethod
    def event_types(self) -> set[EventType]:
        """
        Get the event types this handler can handle.

        Returns:
            set[EventType]: Set of event types.
        """
        pass

    @property
    def priority(self) -> EventPriority:
        """
        Get the priority of this handler.

        Returns:
            EventPriority: The handler priority.
        """
        return EventPriority.NORMAL


class EventFilter(ABC):
    """
    Abstract base class for event filters.

    Event filters can modify or reject events before they are processed by handlers.
    """

    @abstractmethod
    def filter_event(self, event: Event) -> Optional[Event]:
        """
        Filter an event.

        Args:
            event (Event): The event to filter.

        Returns:
            Optional[Event]: The filtered event or None to drop the event.
        """
        pass


class EventError(Exception):
    """Base exception for event-related errors."""
    pass


class EventHandlerError(EventError):
    """Exception raised when an event handler fails."""

    def __init__(self, handler: EventHandler, event: Event, original_error: Exception):
        """
        Initialize the error.

        Args:
            handler (EventHandler): The handler that raised the error.
            event (Event): The event being handled.
            original_error (Exception): The original exception.
        """
        self.handler = handler
        self.event = event
        self.original_error = original_error
        super().__init__(f"Error in event handler {handler.__class__.__name__} "
                         f"for event {event.name}: {str(original_error)}")


class EventFilterError(EventError):
    """Exception raised when an event filter fails."""

    def __init__(self, filter_: EventFilter, event: Event, original_error: Exception):
        """
        Initialize the error.

        Args:
            filter_ (EventFilter): The filter that raised the error.
            event (Event): The event being filtered.
            original_error (Exception): The original exception.
        """
        self.filter = filter_
        self.event = event
        self.original_error = original_error
        super().__init__(f"Error in event filter {filter_.__class__.__name__} "
                         f"for event {event.name}: {str(original_error)}")


# Common event types
class CoreEventType(EventType):
    """Core system event types."""
    INITIALISING = auto()
    INITIALISED = auto()
    STARTING = auto()
    STARTED = auto()
    STOPPING = auto()
    STOPPED = auto()
    SHUTDOWN = auto()
    ERROR = auto()


@dataclass
class CoreEvent(Event[CoreEventType]):
    """Event for core system events."""
    event_type_enum: ClassVar[Type[EventType]] = CoreEventType


"""
Event registry for the bot.

This module provides the EventRegistry class, which maintains a registry of all event types
and provides methods for looking up event types and creating events.
"""


# Set up logger for this module
logger = logging.getLogger(__name__)

# Type variable for type hinting
T = TypeVar('T', bound=EventType)
E = TypeVar('E', bound=Event)


class EventRegistryError(Exception):
    """Exception raised for errors in the event registry."""
    pass


class EventRegistry:
    """
    Registry for event types and event classes.

    The registry keeps track of all event types and event classes in the application,
    allowing for dynamic event creation and type lookup.
    """

    def __init__(self):
        """Initialize the event registry."""
        self._event_types: Dict[str, Type[EventType]] = {}
        self._event_classes: Dict[Type[EventType], Type[Event]] = {}
        self._initialized = False

    def initialize(self, package_paths: Optional[List[str]] = None) -> None:
        """
        Initialize the registry by scanning for event types and event classes.

        Args:
            package_paths (Optional[List[str]]): List of package paths to scan for events.
                If None, only the core events are registered.
        """
        if self._initialized:
            logger.warning("Event registry already initialized")
            return

        # Register core event types
        self._register_core_events()

        # Scan for additional event types
        if package_paths:
            for package_path in package_paths:
                self._scan_package_for_events(package_path)

        self._initialized = True
        logger.info(f"Event registry initialized with {len(self._event_types)} event types "
                    f"and {len(self._event_classes)} event classes")

    def _register_core_events(self) -> None:
        """Register core event types from the base module."""
        from bot.core.events.base import CoreEventType, CoreEvent, ErrorEvent

        self.register_event_type(CoreEventType)
        self.register_event_class(CoreEventType, CoreEvent)
        # ErrorEvent is a special case that we also want to register
        self._event_classes[CoreEventType.ERROR] = ErrorEvent

        logger.debug("Registered core event types")

    def _scan_package_for_events(self, package_path: str) -> None:
        """
        Scan a package for event types and event classes.

        Args:
            package_path (str): Path to the package to scan.
        """
        try:
            package = importlib.import_module(package_path)
        except ImportError:
            logger.error(f"Could not import package: {package_path}")
            return

        logger.debug(f"Scanning package: {package_path}")

        # Scan all modules in the package
        for _, module_name, _ in pkgutil.walk_packages(package.__path__, package.__name__ + '.'):
            try:
                module = importlib.import_module(module_name)
                self._scan_module_for_events(module)
            except ImportError:
                logger.error(f"Could not import module: {module_name}")
                continue

    def _scan_module_for_events(self, module: Any) -> None:
        """
        Scan a module for event types and event classes.

        Args:
            module (Any): Module to scan.
        """
        for name, obj in inspect.getmembers(module):
            # Look for EventType subclasses
            if (inspect.isclass(obj) and issubclass(obj, EventType) and
                    obj is not EventType and not inspect.isabstract(obj)):
                self.register_event_type(obj)
                logger.debug(f"Found event type: {obj.__name__}")

            # Look for Event subclasses
            if (inspect.isclass(obj) and issubclass(obj, Event) and
                    obj is not Event and not inspect.isabstract(obj)):
                # Get the event_type_enum from the class
                event_type_enum = getattr(obj, 'event_type_enum', None)
                if event_type_enum and issubclass(event_type_enum, EventType):
                    self.register_event_class(event_type_enum, obj)
                    logger.debug(f"Found event class: {obj.__name__}")

    def register_event_type(self, event_type: Type[T]) -> None:
        """
        Register an event type.

        Args:
            event_type (Type[T]): Event type to register.
        """
        if not issubclass(event_type, EventType):
            raise EventRegistryError(
                f"Invalid event type: {event_type.__name__}")

        self._event_types[event_type.__name__] = event_type
        logger.debug(f"Registered event type: {event_type.__name__}")

    def register_event_class(self, event_type_enum: Type[T], event_class: Type[Event]) -> None:
        """
        Register an event class for an event type.

        Args:
            event_type_enum (Type[T]): Event type enum.
            event_class (Type[Event]): Event class to register.
        """
        if not issubclass(event_type_enum, EventType):
            raise EventRegistryError(
                f"Invalid event type enum: {event_type_enum.__name__}")

        if not issubclass(event_class, Event):
            raise EventRegistryError(
                f"Invalid event class: {event_class.__name__}")

        self._event_classes[event_type_enum] = event_class
        logger.debug(
            f"Registered event class {event_class.__name__} for event type enum {event_type_enum.__name__}")

    def get_event_type(self, name: str) -> Optional[Type[EventType]]:
        """
        Get an event type by name.

        Args:
            name (str): Name of the event type.

        Returns:
            Optional[Type[EventType]]: The event type, or None if not found.
        """
        return self._event_types.get(name)

    def get_event_class(self, event_type_enum: Type[T]) -> Optional[Type[Event]]:
        """
        Get an event class for an event type.

        Args:
            event_type_enum (Type[T]): Event type enum.

        Returns:
            Optional[Type[Event]]: The event class, or None if not found.
        """
        return self._event_classes.get(event_type_enum)

    def create_event(self, event_type_enum: Type[T], event_type: T, **kwargs: Any) -> Event:
        """
        Create an event of the appropriate type.

        Args:
            event_type_enum (Type[T]): Event type enum.
            event_type (T): Event type.
            **kwargs: Additional arguments for the event constructor.

        Returns:
            Event: The created event.

        Raises:
            EventRegistryError: If no event class is registered for the event type.
        """
        event_class = self.get_event_class(event_type_enum)
        if not event_class:
            raise EventRegistryError(
                f"No event class registered for event type: {event_type_enum.__name__}")

        return event_class(type=event_type, **kwargs)

    def get_all_event_types(self) -> List[Type[EventType]]:
        """
        Get all registered event types.

        Returns:
            List[Type[EventType]]: List of all event types.
        """
        return list(self._event_types.values())

    def get_all_event_classes(self) -> List[Type[Event]]:
        """
        Get all registered event classes.

        Returns:
            List[Type[Event]]: List of all event classes.
        """
        return list(self._event_classes.values())


# Singleton instance of the event registry
_event_registry = EventRegistry()


def get_event_registry() -> EventRegistry:
    """
    Get the singleton event registry instance.

    Returns:
        EventRegistry: Singleton event registry instance.
    """
    return _event_registry


@dataclass
class ErrorEvent(CoreEvent):
    """Event for system errors."""
    type: CoreEventType = CoreEventType.ERROR
    exception: Optional[Exception] = None
    error_context: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Add the exception to the event data if provided."""
        super().__post_init__()
        if self.exception is not None:
            self.data["exception"] = {
                "type": type(self.exception).__name__,
                "message": str(self.exception),
            }
        if self.error_context:
            self.data["error_context"] = self.error_context
