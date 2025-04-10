import threading
from typing import Dict, List, Callable, Any

from core.logging import get_logger
from core.errors import EventBusError, handle_error

logger = get_logger("event_bus")


class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._lock = threading.Lock()

    def subscribe(self, event_type: str, callback: Callable):
        with self._lock:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            self._subscribers[event_type].append(callback)
            logger.debug(f"Subscribed to event: {event_type}")

    def unsubscribe(self, event_type: str, callback: Callable):
        with self._lock:
            if event_type in self._subscribers and callback in self._subscribers[event_type]:
                self._subscribers[event_type].remove(callback)
                logger.debug(f"Unsubscribed from event: {event_type}")

    def publish(self, event_type: str, data: Any = None):
        callbacks = []
        with self._lock:
            if event_type in self._subscribers:
                callbacks = self._subscribers[event_type].copy()

        if callbacks:
            logger.debug(f"Publishing event: {event_type}")
            for callback in callbacks:
                try:
                    callback(data)
                except Exception as e:
                    handle_error(EventBusError(f"Error in event handler: {e}"),
                                 {"event_type": event_type})
        else:
            logger.debug(f"No subscribers for event: {event_type}")

    def has_subscribers(self, event_type: str) -> bool:
        with self._lock:
            return event_type in self._subscribers and bool(self._subscribers[event_type])


# Singleton instance
event_bus = EventBus()
