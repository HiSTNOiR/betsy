from abc import ABC, abstractmethod
from core.logging import get_logger
from core.errors import handle_error, NetworkError

class GenericReader(ABC):
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        self.enabled = False
        self.connection = None

    @abstractmethod
    def _connect(self):
        pass

    @abstractmethod
    def _read(self):
        pass

    def start(self):
        try:
            if not self.enabled:
                return
            self._connect()
        except Exception as e:
            handle_error(NetworkError(f"Connection failed: {e}"))

    def stop(self):
        if self.connection:
            try:
                self.connection.close()
            except Exception as e:
                handle_error(NetworkError(f"Disconnection failed: {e}"))
            finally:
                self.connection = None
    
    # EXAMPLE IMPLEMENTATION
