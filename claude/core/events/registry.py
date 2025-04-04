import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Callable, TypeVar
logger = logging.getLogger(__name__)
T = TypeVar('T', bound='Event')


class EventRegistryError(Exception):
    pass


@dataclass
class Event:
    type: str
    source: Optional[str] = None
    timestamp: Optional[float] = None
    data: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.type:
            raise ValueError("Event type cannot be empty")
        if self.timestamp is None:
            import time
            self.timestamp = time.time()

    def get_type(self) -> str:
        return self.type

    def get_data(self) -> Dict[str, Any]:
        return self.data


class EventRegistry:
    def __init__(self):
        self._handlers: Dict[str, List[Callable[[Event], None]]] = {}
        self._global_handlers: List[Callable[[Event], None]] = []
        self._event_types: Set[str] = set()

    def register_event_type(self, event_type: str) -> None:
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
        if event_type is None:
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
        if event_type is None:
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
        if event_type not in self._event_types:
            return []
        return self._handlers[event_type].copy()

    def get_global_handlers(self) -> List[Callable[[Event], None]]:
        return self._global_handlers.copy()

    def clear(self) -> None:
        self._handlers = {}
        self._global_handlers = []
        self._event_types = set()
        logger.debug("Cleared event registry")

    def get_registered_types(self) -> Set[str]:
        return self._event_types.copy()

    def initialise(self, package_paths: Optional[List[str]] = None) -> None:
        try:
            if not package_paths:
                logger.info(
                    "No package paths provided, skipping event discovery")
                return
            for package_path in package_paths:
                logger.debug(f"Scanning package for events: {package_path}")
            logger.info("Event registry initialised")
        except Exception as e:
            error_msg = f"Error initializing event registry: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise EventRegistryError(error_msg) from e


_event_registry = EventRegistry()


def get_event_registry() -> EventRegistry:
    return _event_registry
