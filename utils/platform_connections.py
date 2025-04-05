"""
Thread-safe singleton
Configurable platform connections
"""

import threading
import logging

from typing import Any, Optional, Type, TypeVar

from core.errors import NetworkError, handle_error
from core.config import config
from core.logging import get_logger

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

class PlatformConnection(SafeSingleton):
    def __init__(self):
        super().__init__()
        self.logger = get_logger(self.__class__.__name__.lower())
        self.connection = None
        self.enabled = False

    def _safe_init(self):
        self.enabled = config.get_boolean(f"{self.__class__.__name__.upper()}_ENABLED", False)
        if self.enabled:
            self._connect()

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
                handle_error(NetworkError(f"Disconnection failed: {e}"))
            finally:
                self.connection = None

    def _disconnect(self):
        raise NotImplementedError("Subclasses must implement disconnection logic")

    def is_connected(self):
        return self.connection is not None

class TwitchConnection(PlatformConnection):
    def _connect(self):
        try:
            # Twitch-specific connection logic
            # TODO Example placeholders:
            self.connection = None  # Replace with actual Twitch connection
            self.logger.info("Twitch connection established")
        except Exception as e:
            handle_error(NetworkError(f"Twitch connection failed: {e}"))
            self.connection = None

    def _disconnect(self):
        # TODO Twitch-specific disconnection logic
        pass

class OBSConnection(PlatformConnection):
    def _connect(self):
        try:
            # OBS-specific connection logic
            # TODO Example placeholders:
            self.connection = None  # Replace with actual OBS connection
            self.logger.info("OBS connection established")
        except Exception as e:
            handle_error(NetworkError(f"OBS connection failed: {e}"))
            self.connection = None

    def _disconnect(self):
        # TODO OBS-specific disconnection logic
        pass

def create_singleton_class(cls: Type[T]) -> Type[T]:
    return SingletonMeta(cls.__name__, cls.__bases__, dict(cls.__dict__))