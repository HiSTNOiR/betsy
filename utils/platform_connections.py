import threading
import logging
from typing import Any, Optional, Type, TypeVar

T = TypeVar('T')

class SingletonMeta(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]

class SafeSingleton:
    _initialised = False
    _lock = threading.Lock()

    def __init__(self):
        with self._lock:
            if not getattr(self, '_initialised', False):
                self._safe_init()
                self._initialised = True

    def _safe_init(self):
        pass

class PlatformConnection:
    def __init__(self):
        self._lock = threading.Lock()
        self.connection = None
        self.enabled = False
        
    def _connect(self):
        raise NotImplementedError("Subclasses must implement connection logic")

    def reconnect(self):
        if self.enabled:
            self._connect()

    def disconnect(self):
        if self.connection:
            try:
                self._disconnect()
            except Exception as e:
                # Will be imported at runtime to avoid circular imports
                from core.errors import NetworkError, handle_error
                handle_error(NetworkError(f"Disconnection failed: {e}"))
            finally:
                self.connection = None

    def _disconnect(self):
        raise NotImplementedError("Subclasses must implement disconnection logic")

    def is_connected(self):
        return self.connection is not None

def create_singleton_class(cls: Type[T]) -> Type[T]:
    return SingletonMeta(cls.__name__, cls.__bases__, dict(cls.__dict__))