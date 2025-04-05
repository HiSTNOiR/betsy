from typing import Any, Optional, Dict

from core.logging import get_logger
from core.errors import handle_error

class BaseEvent:
    def __init__(self, data: Optional[Dict[str, Any]] = None):
        self.logger = get_logger(self.__class__.__name__)
        self.data = data or {}

    def process(self):
        try:
            self._validate()
            return self._handle()
        except Exception as e:
            handle_error(e, {"event_data": self.data})

    def _validate(self):
        pass

    def _handle(self):
        raise NotImplementedError

    # EXAMPLE IMPLEMENTATION
