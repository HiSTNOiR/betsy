from typing import Dict, Any

from abc import ABC, abstractmethod

from core.logging import get_logger
from core.errors import handle_error


class BasePublisher(ABC):
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        self.enabled = False

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    def _publish_event(self, event_type: str, data: Dict[str, Any] = None):
        try:
            from event_bus.registry import event_registry
            event_registry.create_and_publish_event(event_type, data)
        except Exception as e:
            handle_error(e, {"event_type": event_type, "data": data})
