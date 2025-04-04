"""
Error handling for the bot.

This module defines the error hierarchy and error handling mechanisms.
"""

import logging
import traceback
import sys
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Union

# Type variable for type hinting
T = TypeVar('T')

# Set up logger for this module
logger = logging.getLogger(__name__)


class BotError(Exception):
    """Base exception for all bot errors."""

    def __init__(self, message: str, *args: Any):
        """
        Initialise the error.

        Args:
            message (str): Error message.
            *args: Additional arguments.
        """
        self.message = message
        super().__init__(message, *args)


class ConfigError(BotError):
    """Base exception for configuration-related errors."""
    pass


class DatabaseError(BotError):
    """Base exception for database-related errors."""
    pass


class CommandError(BotError):
    """Base exception for command-related errors."""
    pass


class PlatformError(BotError):
    """Base exception for platform-related errors."""
    pass


class TwitchError(PlatformError):
    """Base exception for Twitch-related errors."""
    pass


class OBSError(PlatformError):
    """Base exception for OBS-related errors."""
    pass


class DiscordError(PlatformError):
    """Base exception for Discord-related errors."""
    pass


class FeatureError(BotError):
    """Base exception for feature-related errors."""
    pass


class ValidationError(BotError):
    """Base exception for validation-related errors."""
    pass


class ErrorContext:
    """
    Context information for an error.

    Provides additional context about where and when an error occurred.
    """

    def __init__(
        self,
        error: Exception,
        source: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        traceback_info: Optional[str] = None
    ):
        """
        Initialise the error context.

        Args:
            error (Exception): The exception that was raised.
            source (Optional[str]): Source of the error (e.g., module name).
            context (Optional[Dict[str, Any]]): Additional context information.
            traceback_info (Optional[str]): Traceback information.
        """
        self.error = error
        self.source = source
        self.context = context or {}

        if traceback_info is None:
            # Get full traceback if not provided
            self.traceback_info = ''.join(traceback.format_exception(
                type(error), error, error.__traceback__
            ))
        else:
            self.traceback_info = traceback_info

    def as_dict(self) -> Dict[str, Any]:
        """
        Convert the error context to a dictionary.

        Returns:
            Dict[str, Any]: Dictionary representation of the error context.
        """
        return {
            'error_type': type(self.error).__name__,
            'error_message': str(self.error),
            'source': self.source,
            'context': self.context,
            'traceback': self.traceback_info
        }


class ErrorHandler:
    """
    Handler for bot errors.

    This class provides methods for registering error handlers and handling errors.
    """

    def __init__(self):
        """Initialise the error handler."""
        # Dictionary mapping error types to handler functions
        self._handlers: Dict[Type[Exception],
                             List[Callable[[ErrorContext], None]]] = {}

        # Default error handler
        self._default_handler: Optional[Callable[[ErrorContext], None]] = None

    def register_handler(
        self,
        error_type: Type[Exception],
        handler: Callable[[ErrorContext], None]
    ) -> None:
        """
        Register an error handler for a specific error type.

        Args:
            error_type (Type[Exception]): Type of exception to handle.
            handler (Callable[[ErrorContext], None]): Function to handle the error.
        """
        if error_type not in self._handlers:
            self._handlers[error_type] = []

        self._handlers[error_type].append(handler)
        logger.debug(f"Registered handler for {error_type.__name__}")

    def set_default_handler(self, handler: Callable[[ErrorContext], None]) -> None:
        """
        Set the default error handler.

        Args:
            handler (Callable[[ErrorContext], None]): Function to handle unhandled errors.
        """
        self._default_handler = handler
        logger.debug("Set default error handler")

    def handle(
        self,
        error: Exception,
        source: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Handle an error.

        Args:
            error (Exception): The exception to handle.
            source (Optional[str]): Source of the error.
            context (Optional[Dict[str, Any]]): Additional context information.
        """
        error_ctx = ErrorContext(error, source, context)

        # Log the error
        logger.error(
            f"Error in {source or 'unknown'}: {str(error)}",
            exc_info=True,
            extra=context
        )

        # Find and call appropriate handlers
        handled = False

        # Check for handlers matching the exact error type
        if type(error) in self._handlers:
            for handler in self._handlers[type(error)]:
                try:
                    handler(error_ctx)
                    handled = True
                except Exception as e:
                    logger.error(
                        f"Error in error handler: {str(e)}", exc_info=True)

        # Check for handlers matching parent error types
        if not handled:
            for error_type, handlers in self._handlers.items():
                if isinstance(error, error_type) and error_type is not type(error):
                    for handler in handlers:
                        try:
                            handler(error_ctx)
                            handled = True
                        except Exception as e:
                            logger.error(
                                f"Error in error handler: {str(e)}", exc_info=True)

        # Use default handler if no specific handler was found or executed
        if not handled and self._default_handler:
            try:
                self._default_handler(error_ctx)
            except Exception as e:
                logger.error(
                    f"Error in default error handler: {str(e)}", exc_info=True)

    def try_except(
        self,
        func: Callable[..., T],
        *args: Any,
        source: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        default: Optional[T] = None,
        **kwargs: Any
    ) -> Optional[T]:
        """
        Execute a function and handle any exceptions.

        Args:
            func (Callable[..., T]): Function to execute.
            *args: Arguments to pass to the function.
            source (Optional[str]): Source of the error.
            context (Optional[Dict[str, Any]]): Additional context information.
            default (Optional[T]): Default value to return if an exception occurs.
            **kwargs: Keyword arguments to pass to the function.

        Returns:
            Optional[T]: Return value of the function or default value if an exception occurs.
        """
        try:
            return func(*args, **kwargs)
        except Exception as e:
            self.handle(e, source, context)
            return default


# Singleton instance of the error handler
_error_handler = ErrorHandler()


def get_error_handler() -> ErrorHandler:
    """
    Get the singleton error handler instance.

    Returns:
        ErrorHandler: Singleton error handler instance.
    """
    return _error_handler


def register_default_handlers(handler: ErrorHandler = None) -> None:
    """
    Register default error handlers.

    Args:
        handler (ErrorHandler): Error handler to register handlers with.
            If None, uses the singleton instance.
    """
    if handler is None:
        handler = get_error_handler()

    # Register a default handler for all exceptions
    def default_handler(ctx: ErrorContext) -> None:
        logger.error(
            f"Unhandled error: {str(ctx.error)}",
            extra=ctx.context
        )

    handler.set_default_handler(default_handler)

    # Register specific handlers for known error types
    def config_error_handler(ctx: ErrorContext) -> None:
        logger.error(
            f"Configuration error: {str(ctx.error)}",
            extra=ctx.context
        )

    handler.register_handler(ConfigError, config_error_handler)

    logger.info("Registered default error handlers")


# Exception utility functions
def get_traceback_str(exc_info=None) -> str:
    """
    Get a string representation of a traceback.

    Args:
        exc_info: Exception info from sys.exc_info(). If None, uses current exception.

    Returns:
        str: String representation of the traceback.
    """
    if exc_info is None:
        exc_info = sys.exc_info()

    return ''.join(traceback.format_exception(*exc_info))


def try_except_decorator(
    source: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
    default: Any = None
):
    """
    Decorator to handle exceptions in a function.

    Args:
        source (Optional[str]): Source of the error.
        context (Optional[Dict[str, Any]]): Additional context information.
        default (Any): Default value to return if an exception occurs.

    Returns:
        Callable: Decorated function.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            return get_error_handler().try_except(
                func, *args,
                source=source or func.__module__,
                context=context,
                default=default,
                **kwargs
            )
        return wrapper
    return decorator
