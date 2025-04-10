from abc import ABC, abstractmethod

from event_bus.bus import event_bus
from core.logging import get_logger


class BaseSubscriber(ABC):
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.logger = get_logger(self.__class__.__name__)

    @abstractmethod
    def subscribe(self):
        pass

    def unsubscribe(self, event_type, callback):
        self.event_bus.unsubscribe(event_type, callback)
