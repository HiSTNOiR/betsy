import logging
from typing import Any, Optional

from core.logging import get_logger
from core.errors import handle_error, ValidationError

class BaseProcessor:
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)

    def process(self, data: Any) -> Optional[Any]:
        try:
            self._validate_input(data)
            return self._process(data)
        except ValidationError as e:
            handle_error(e)
            self.logger.warning(f"Validation failed: {e}")
            return None
        except Exception as e:
            handle_error(e)
            self.logger.error(f"Unexpected error during processing: {e}")
            return None

    def _validate_input(self, data: Any) -> None:
        if data is None:
            raise ValidationError("Input data cannot be None")

    def _process(self, data: Any) -> Any:
        raise NotImplementedError("Subclasses must implement processing logic")

    # EXAMPLE IMPLEMENTATION
    def example_method(self, additional_param: str) -> bool:
        try:
            self.logger.info(f"Executing example method with {additional_param}")
            return True
        except Exception as e:
            handle_error(e)
            self.logger.error(f"Error in example method: {e}")
            return False