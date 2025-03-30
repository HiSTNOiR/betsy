"""
Base event classes for the bot.

This module defines the base event classes and types used throughout the application.
"""

import asyncio
import traceback
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any, Dict, Optional, Set, Type, TypeVar, Union, cast

import logging

# Set up logger for this module
logger = logging.getLogger(__name__)

# Type variable for type hinting
T = TypeVar('T', bound='Event')


class EventType(Enum):
    """
    Base class for event type enums.

    All event types should subclass this enum to ensure type safety.
    """
    pass


class EventPriority(Enum):
    """
    Priority for event handlers.

    Handlers with higher priority (lower numerical value) are executed first.
    """
    HIGHEST = 0
    HIGH = 25
    NORMAL = 50
    LOW = 75
    LOWEST = 100


class CoreEventType(EventType):
    """
    Core event types used by the application.

    These events represent lifecycle and system-level events.
    """
    # Lifecycle events
    INITIALISING = auto()
    INITIALISED = auto()
    STARTING = auto()
    STARTED = auto()
    STOPPING = auto()
    STOPPED = auto()
    SHUTDOWN = auto()

    # System events
    ERROR = auto()
    WARNING = auto()
    INFO = auto()
    DEBUG = auto()


class Event:
    """
    Base class for all events.

    Events are used to communicate between different parts of the application.
    """

    def __init__(
        self,
        type: EventType,
        source: Optional[str] = None,
        timestamp: Optional[float] = None,
        data: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the event.

        Args:
            type (EventType): Type of the event.
            source (Optional[str]): Source of the event.
            timestamp (Optional[float]): Timestamp of the event.
            data (Optional[Dict[str, Any]]): Additional event data.

        Raises:
            TypeError: If the event type is not an instance of EventType.
        """
        if not isinstance(type, EventType):
            raise TypeError(
                f"Event type must be an instance of EventType, got {type.__class__.__name__}")

        self.type = type
        self.source = source

        # Set timestamp if not provided
        if timestamp is None:
            import time
            self.timestamp = time.time()
        else:
            self.timestamp = timestamp

        # Set data if provided, otherwise empty dict
        self.data = data or {}

        # Event flow control
        self.cancelled = False
        self.propagate = True

    @property
    def name(self) -> str:
        """
        Get the name of the event.

        Returns:
            str: Event name.
        """
        return self.type_str

    @property
    def type_str(self) -> str:
        """
        Get the event type as a string.

        Returns:
            str: Event type string.
        """
        return self.type.name

    @property
    def event_type_enum(self) -> Type[EventType]:
        """
        Get the event type enum class.

        Returns:
            Type[EventType]: Event type enum class.
        """
        return self.type.__class__

    def cancel(self) -> None:
        """
        Cancel the event.

        Cancelled events should not be processed further.
        """
        self.cancelled = True

    def stop_propagation(self) -> None:
        """
        Stop event propagation.

        Stops the event from being passed to other handlers.
        """
        self.propagate = False

    def __repr__(self) -> str:
        """
        Get a string representation of the event.

        Returns:
            str: String representation.
        """
        return f"{self.__class__.__name__}(type={self.type_str}, source={self.source}, data={self.data})"


class CoreEvent(Event):
    """
    Event for core system events.

    These events are used for system-level communication.
    """

    def __init__(
        self,
        type: CoreEventType,
        source: Optional[str] = None,
        timestamp: Optional[float] = None,
        data: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the core event.

        Args:
            type (CoreEventType): Type of the core event.
            source (Optional[str]): Source of the event.
            timestamp (Optional[float]): Timestamp of the event.
            data (Optional[Dict[str, Any]]): Additional event data.

        Raises:
            TypeError: If the event type is not an instance of CoreEventType.
        """
        if not isinstance(type, CoreEventType):
            raise TypeError(
                f"Core event type must be an instance of CoreEventType, got {type.__class__.__name__}")

        super().__init__(type, source, timestamp, data)


class ErrorEvent(CoreEvent):
    """
    Event for error reporting.

    These events are used to report errors throughout the system.
    """

    def __init__(
        self,
        source: Optional[str] = None,
        error: Optional[Exception] = None,
        context: Optional[Dict[str, Any]] = None,
        traceback_info: Optional[str] = None,
        timestamp: Optional[float] = None
    ):
        """
        Initialize the error event.

        Args:
            source (Optional[str]): Source of the error.
            error (Optional[Exception]): The exception that occurred.
            context (Optional[Dict[str, Any]]): Additional context information.
            traceback_info (Optional[str]): Traceback information as a string.
            timestamp (Optional[float]): Timestamp of the event.
        """
        data = context or {}

        # Add error information to data
        if error:
            data["error"] = str(error)
            data["error_type"] = error.__class__.__name__

        # Add traceback information if available
        if traceback_info:
            data["traceback"] = traceback_info
        elif error and error.__traceback__:
            data["traceback"] = ''.join(traceback.format_exception(
                type(error), error, error.__traceback__
            ))

        # Initialize as a core event with ERROR type
        super().__init__(CoreEventType.ERROR, source, timestamp, data)

        # Store the original exception for reference
        self.exception = error
        self.error_context = context or {}

    @property
    def error_message(self) -> str:
        """
        Get the error message.

        Returns:
            str: Error message.
        """
        return self.data.get("error", "Unknown error")


class EventHandler(ABC):
    """
    Base class for event handlers.

    Event handlers process events based on their type and priority.
    """

    @property
    @abstractmethod
    def event_types(self) -> Set[EventType]:
        """
        Get the event types this handler can handle.

        Returns:
            Set[EventType]: Set of event types this handler can handle.
                              Empty set means it handles all events.
        """
        pass

    @property
    @abstractmethod
    def priority(self) -> EventPriority:
        """
        Get the priority of this handler.

        Returns:
            EventPriority: Priority value.
        """
        pass

    @abstractmethod
    async def handle_event(self, event: Event) -> None:
        """
        Handle an event.

        Args:
            event (Event): The event to handle.
        """
        pass


class EventFilter(ABC):
    """
    Base class for event filters.

    Event filters can modify or block events before they reach handlers.
    """

    @abstractmethod
    def filter_event(self, event: Event) -> Optional[Event]:
        """
        Filter an event.

        Args:
            event (Event): The event to filter.

        Returns:
            Optional[Event]: The filtered event, or None to block the event.
        """
        pass


class EventError(Exception):
    """Base exception for event-related errors."""
    pass


class EventHandlerError(EventError):
    """Exception raised when an event handler fails."""

    def __init__(self, handler: EventHandler, event: Event, original_error: Exception):
        """
        Initialize the event handler error.

        Args:
            handler (EventHandler): The handler that failed.
            event (Event): The event being handled.
            original_error (Exception): The original error that occurred.
        """
        self.handler = handler
        self.event = event
        self.original_error = original_error

        message = (
            f"Error in event handler {handler.__class__.__name__} for event "
            f"{event.type_str} from {event.source or 'unknown'}: {str(original_error)}"
        )

        super().__init__(message)


class EventFilterError(EventError):
    """Exception raised when an event filter fails."""

    def __init__(self, filter: EventFilter, event: Event, original_error: Exception):
        """
        Initialize the event filter error.

        Args:
            filter (EventFilter): The filter that failed.
            event (Event): The event being filtered.
            original_error (Exception): The original error that occurred.
        """
        self.filter = filter
        self.event = event
        self.original_error = original_error

        message = (
            f"Error in event filter {filter.__class__.__name__} for event "
            f"{event.type_str} from {event.source or 'unknown'}: {str(original_error)}"
        )

        super().__init__(message)
