from typing import Dict, List, Callable, Type, Any

from events.base import BaseEvent
from event_bus.bus import event_bus
from core.logging import get_logger

logger = get_logger("event_registry")


class EventRegistry:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.event_handlers: Dict[str, List[Callable]] = {}
        self.event_types: Dict[str, Type[BaseEvent]] = {}

    def register_event(self, event_type: str, event_class: Type[BaseEvent]):
        self.event_types[event_type] = event_class
        logger.debug(f"Registered event type: {event_type}")

    def register_handler(self, event_type: str, handler: Callable):
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
        self.event_bus.subscribe(event_type, handler)
        logger.debug(f"Registered handler for event: {event_type}")

    def unregister_handler(self, event_type: str, handler: Callable):
        if event_type in self.event_handlers and handler in self.event_handlers[event_type]:
            self.event_handlers[event_type].remove(handler)
            self.event_bus.unsubscribe(event_type, handler)
            logger.debug(f"Unregistered handler for event: {event_type}")

    def create_and_publish_event(self, event_type: str, data: Any = None):
        if event_type in self.event_types:
            event_class = self.event_types[event_type]
            event = event_class(data)
            processed_data = event.process()
            if processed_data:
                self.event_bus.publish(event_type, processed_data)
        else:
            logger.warning(f"Unknown event type: {event_type}")


# Singleton instance with default event bus
event_registry = EventRegistry(event_bus)
