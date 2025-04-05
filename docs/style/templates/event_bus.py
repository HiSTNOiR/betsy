import threading
from typing import Callable, Any, Dict, List

class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._lock = threading.Lock()

    def subscribe(self, event_type: str, callback: Callable):
        with self._lock:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            self._subscribers[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: Callable):
        with self._lock:
            if event_type in self._subscribers:
                self._subscribers[event_type].remove(callback)

    def publish(self, event_type: str, payload: Any = None):
        with self._lock:
            if event_type in self._subscribers:
                for callback in self._subscribers[event_type]:
                    callback(payload)

    # EXAMPLE IMPLEMENTATION
