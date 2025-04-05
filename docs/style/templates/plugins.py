import logging

from core.errors import BetsyError, handle_error
from core.logging import get_logger

logger = get_logger("plugins")

class BasePlugin:
    def __init__(self):
        self.enabled = True
        logger.info(f"Initialising {self.__class__.__name__}")

    def load(self):
        try:
            self._validate_config()
        except BetsyError as e:
            handle_error(e)
            self.enabled = False

    def _validate_config(self):
        pass

    # EXAMPLE IMPLEMENTATION
    def example_method(self, *args, **kwargs):
        if not self.enabled:
            logger.warning(f"{self.__class__.__name__} is not enabled")
            return None

        try:
            pass
        except Exception as e:
            handle_error(BetsyError(f"Error in example method: {e}"))