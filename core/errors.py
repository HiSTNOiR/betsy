import logging
import sys
import traceback
from enum import Enum
from typing import Dict, Optional, Any, List, Type, Union

from core.config import config
from core.logging import get_logger

logger = get_logger("errors")

class ErrorSeverity(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4

class BetsyError(Exception):
    severity: ErrorSeverity = ErrorSeverity.ERROR
    error_code: str = "E000"
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(message)
    
    def get_error_info(self) -> Dict[str, Any]:
        return {
            "error_code": self.error_code,
            "severity": self.severity.name,
            "message": self.message,
            "details": self.details
        }

class ConfigError(BetsyError):
    severity = ErrorSeverity.CRITICAL
    error_code = "E001"

class DatabaseError(BetsyError):
    severity = ErrorSeverity.ERROR
    error_code = "E002"

class NetworkError(BetsyError):
    severity = ErrorSeverity.ERROR
    error_code = "E003"

class TwitchError(NetworkError):
    error_code = "E003.1"

class OBSError(NetworkError):
    error_code = "E003.2"

class EventBusError(BetsyError):
    severity = ErrorSeverity.ERROR
    error_code = "E004"

class ValidationError(BetsyError):
    severity = ErrorSeverity.WARNING
    error_code = "E005"

class AuthenticationError(BetsyError):
    severity = ErrorSeverity.CRITICAL
    error_code = "E006"

class PermissionError(BetsyError):
    severity = ErrorSeverity.WARNING
    error_code = "E007"

class ResourceNotFoundError(BetsyError):
    severity = ErrorSeverity.WARNING
    error_code = "E008"

class TimeoutError(BetsyError):
    severity = ErrorSeverity.WARNING
    error_code = "E009"

class ErrorHandler:
    _instance = None
    _error_callbacks: Dict[Type[BetsyError], List[callable]] = {}
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ErrorHandler, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.debug_mode = config.get_boolean("DEBUG_MODE", False)
        
    def register_callback(self, error_type: Type[BetsyError], callback: callable) -> None:
        if error_type not in self._error_callbacks:
            self._error_callbacks[error_type] = []
        self._error_callbacks[error_type].append(callback)
    
    def handle_error(self, error: Union[BetsyError, Exception], context: Optional[Dict[str, Any]] = None) -> None:
        if not isinstance(error, BetsyError):
            error = self._convert_to_betsy_error(error)
        
        self._log_error(error, context)
        self._execute_callbacks(error, context)
        
        if self.debug_mode and error.severity in [ErrorSeverity.CRITICAL, ErrorSeverity.ERROR]:
            self._print_debug_info(error, context)
    
    def _convert_to_betsy_error(self, error: Exception) -> BetsyError:
        error_type = type(error).__name__
        message = str(error)
        details = {"original_error_type": error_type}
        
        return BetsyError(
            message=f"Uncategorised error: {message}",
            details=details
        )
    
    def _log_error(self, error: BetsyError, context: Optional[Dict[str, Any]] = None) -> None:
        error_info = error.get_error_info()
        log_message = f"Error {error_info['error_code']}: {error_info['message']}"
        
        if context:
            error_info["context"] = context
        
        if error.severity == ErrorSeverity.DEBUG:
            logger.debug(log_message, extra={"error_info": error_info})
        elif error.severity == ErrorSeverity.INFO:
            logger.info(log_message, extra={"error_info": error_info})
        elif error.severity == ErrorSeverity.WARNING:
            logger.warning(log_message, extra={"error_info": error_info})
        elif error.severity == ErrorSeverity.ERROR:
            logger.error(log_message, extra={"error_info": error_info})
        elif error.severity == ErrorSeverity.CRITICAL:
            logger.critical(log_message, extra={"error_info": error_info})
    
    def _execute_callbacks(self, error: BetsyError, context: Optional[Dict[str, Any]] = None) -> None:
        error_type = type(error)
        
        for base_type, callbacks in self._error_callbacks.items():
            if issubclass(error_type, base_type):
                for callback in callbacks:
                    try:
                        callback(error, context)
                    except Exception as callback_error:
                        logger.error(
                            f"Error in error callback: {callback_error}",
                            extra={"callback": str(callback), "original_error": error.get_error_info()}
                        )
    
    def _print_debug_info(self, error: BetsyError, context: Optional[Dict[str, Any]] = None) -> None:
        print("\n===== ERROR DETAILS =====", file=sys.stderr)
        print(f"Code: {error.error_code}", file=sys.stderr)
        print(f"Severity: {error.severity.name}", file=sys.stderr)
        print(f"Message: {error.message}", file=sys.stderr)
        
        if error.details:
            print("\nDetails:", file=sys.stderr)
            for key, value in error.details.items():
                print(f"  {key}: {value}", file=sys.stderr)
        
        if context:
            print("\nContext:", file=sys.stderr)
            for key, value in context.items():
                print(f"  {key}: {value}", file=sys.stderr)
        
        print("\nTraceback:", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        print("========================\n", file=sys.stderr)

error_handler = ErrorHandler()

def handle_error(error: Union[BetsyError, Exception], context: Optional[Dict[str, Any]] = None) -> None:
    error_handler.handle_error(error, context)

def register_error_callback(error_type: Type[BetsyError], callback: callable) -> None:
    error_handler.register_callback(error_type, callback)