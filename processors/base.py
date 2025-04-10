from typing import Any, Optional, Dict

from core.logging import get_logger
from core.errors import handle_error, ValidationError


class BaseProcessor:
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)

    def process(self, data: Any) -> Optional[Any]:
        try:
            self._validate(data)
            return self._process(data)
        except ValidationError as e:
            handle_error(e)
            self.logger.warning(f"Validation failed: {e}")
            return None
        except Exception as e:
            handle_error(e)
            self.logger.error(f"Processing error: {e}")
            return None

    def _validate(self, data: Any) -> None:
        if data is None:
            raise ValidationError("Input data cannot be None")

    def _process(self, data: Any) -> Any:
        raise NotImplementedError("Subclasses must implement _process method")
