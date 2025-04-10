import threading
import logging
from typing import Any, Optional, Type, TypeVar

from core.logging import get_logger
from core.errors import handle_error, BetsyError

logger = get_logger("utils_module")

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

    def __new__(cls, *args: Any, **kwargs: Any):
        if not hasattr(cls, '_instance'):
            with cls._lock:
                if not hasattr(cls, '_instance'):
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        with self._lock:
            if not self._initialised:
                try:
                    self._safe_init()
                    self._initialised = True
                except Exception as e:
                    handle_error(BetsyError(f"Initialisation failed: {e}"))

    def _safe_init(self):
        pass

    # EXAMPLE IMPLEMENTATION
    def optional_method(self, param: str) -> Optional[str]:
        try:
            if not param:
                raise ValueError("Invalid parameter")
            return param.upper()
        except Exception as e:
            logger.warning(f"Method failed: {e}")
            return None