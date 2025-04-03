import asyncio
import traceback
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any, Dict, Optional, Set, Type, TypeVar, Union, cast
import logging
logger = logging.getLogger(__name__)
T = TypeVar('T', bound='Event')


class EventType(Enum):
    pass


class EventPriority(Enum):
    HIGHEST = 0
    HIGH = 25
    NORMAL = 50
    LOW = 75
    LOWEST = 100


class CoreEventType(EventType):
    INITIALISING = auto()
    INITIALISED = auto()
    STARTING = auto()
    STARTED = auto()
    STOPPING = auto()
    STOPPED = auto()
    SHUTDOWN = auto()
    ERROR = auto()
    WARNING = auto()
    INFO = auto()
    DEBUG = auto()


class Event:
    def __init__(
        self,
        type: EventType,
        source: Optional[str] = None,
        timestamp: Optional[float] = None,
        data: Optional[Dict[str, Any]] = None
    ):
        if not isinstance(type, EventType):
            raise TypeError(
                f"Event type must be an instance of EventType, got {type.__class__.__name__}")
        self.type = type
        self.source = source
        if timestamp is None:
            import time
            self.timestamp = time.time()
        else:
            self.timestamp = timestamp
        self.data = data or {}
        self.cancelled = False
        self.propagate = True

    @property
    def name(self) -> str:
        return self.type_str

    @property
    def type_str(self) -> str:
        return self.type.name

    @property
    def event_type_enum(self) -> Type[EventType]:
        return self.type.__class__

    def cancel(self) -> None:
        self.cancelled = True

    def stop_propagation(self) -> None:
        self.propagate = False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(type={self.type_str}, source={self.source}, data={self.data})"


class CoreEvent(Event):
    def __init__(
        self,
        type: CoreEventType,
        source: Optional[str] = None,
        timestamp: Optional[float] = None,
        data: Optional[Dict[str, Any]] = None
    ):
        if not isinstance(type, CoreEventType):
            raise TypeError(
                f"Core event type must be an instance of CoreEventType, got {type.__class__.__name__}")
        super().__init__(type, source, timestamp, data)


class ErrorEvent(CoreEvent):
    def __init__(
        self,
        source: Optional[str] = None,
        error: Optional[Exception] = None,
        context: Optional[Dict[str, Any]] = None,
        traceback_info: Optional[str] = None,
        timestamp: Optional[float] = None
    ):
        data = context or {}
        if error:
            data["error"] = str(error)
            data["error_type"] = error.__class__.__name__
        if traceback_info:
            data["traceback"] = traceback_info
        elif error and error.__traceback__:
            data["traceback"] = ''.join(traceback.format_exception(
                type(error), error, error.__traceback__
            ))
        super().__init__(CoreEventType.ERROR, source, timestamp, data)
        self.exception = error
        self.error_context = context or {}

    @property
    def error_message(self) -> str:
        return self.data.get("error", "Unknown error")


class EventHandler(ABC):
    @property
    @abstractmethod
    def event_types(self) -> Set[EventType]:
        pass

    @property
    @abstractmethod
    def priority(self) -> EventPriority:
        pass

    @abstractmethod
    async def handle_event(self, event: Event) -> None:
        pass


class EventFilter(ABC):
    @abstractmethod
    def filter_event(self, event: Event) -> Optional[Event]:
        pass


class EventError(Exception):
    pass


class EventHandlerError(EventError):
    def __init__(self, handler: EventHandler, event: Event, original_error: Exception):
        self.handler = handler
        self.event = event
        self.original_error = original_error
        message = (
            f"Error in event handler {handler.__class__.__name__} for event "
            f"{event.type_str} from {event.source or 'unknown'}: {str(original_error)}"
        )

        super().__init__(message)


class EventFilterError(EventError):
    def __init__(self, filter: EventFilter, event: Event, original_error: Exception):
        self.filter = filter
        self.event = event
        self.original_error = original_error
        message = (
            f"Error in event filter {filter.__class__.__name__} for event "
            f"{event.type_str} from {event.source or 'unknown'}: {str(original_error)}"
        )
        super().__init__(message)
