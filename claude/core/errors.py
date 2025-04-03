import logging
import traceback
import sys
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Union

T = TypeVar('T')
logger = logging.getLogger(__name__)


class BotError(Exception):
    def __init__(self, message: str, *args: Any):
        self.message = message
        super().__init__(message, *args)


class ConfigError(BotError):
    pass


class DatabaseError(BotError):
    pass


class CommandError(BotError):
    pass


class PlatformError(BotError):
    pass


class TwitchError(PlatformError):
    pass


class OBSError(PlatformError):
    pass


class DiscordError(PlatformError):
    pass


class FeatureError(BotError):
    pass


class ValidationError(BotError):
    pass


class ErrorContext:
    def __init__(
        self,
        error: Exception,
        source: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        traceback_info: Optional[str] = None
    ):
        self.error = error
        self.source = source
        self.context = context or {}
        if traceback_info is None:
            self.traceback_info = ''.join(traceback.format_exception(
                type(error), error, error.__traceback__
            ))
        else:
            self.traceback_info = traceback_info

    def as_dict(self) -> Dict[str, Any]:
        return {
            'error_type': type(self.error).__name__,
            'error_message': str(self.error),
            'source': self.source,
            'context': self.context,
            'traceback': self.traceback_info
        }


class ErrorHandler:
    def __init__(self):
        self._handlers: Dict[Type[Exception],
                             List[Callable[[ErrorContext], None]]] = {}
        self._default_handler: Optional[Callable[[ErrorContext], None]] = None

    def register_handler(
        self,
        error_type: Type[Exception],
        handler: Callable[[ErrorContext], None]
    ) -> None:
        if error_type not in self._handlers:
            self._handlers[error_type] = []

        self._handlers[error_type].append(handler)
        logger.debug(f"Registered handler for {error_type.__name__}")

    def set_default_handler(self, handler: Callable[[ErrorContext], None]) -> None:
        self._default_handler = handler
        logger.debug("Set default error handler")

    def handle(
        self,
        error: Exception,
        source: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        error_ctx = ErrorContext(error, source, context)
        logger.error(
            f"Error in {source or 'unknown'}: {str(error)}",
            exc_info=True,
            extra=context
        )
        handled = False
        if type(error) in self._handlers:
            for handler in self._handlers[type(error)]:
                try:
                    handler(error_ctx)
                    handled = True
                except Exception as e:
                    logger.error(
                        f"Error in error handler: {str(e)}", exc_info=True)
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
        try:
            return func(*args, **kwargs)
        except Exception as e:
            self.handle(e, source, context)
            return default


_error_handler = ErrorHandler()


def get_error_handler() -> ErrorHandler:
    return _error_handler


def register_default_handlers(handler: ErrorHandler = None) -> None:
    if handler is None:
        handler = get_error_handler()

    def default_handler(ctx: ErrorContext) -> None:
        logger.error(
            f"Unhandled error: {str(ctx.error)}",
            extra=ctx.context
        )
    handler.set_default_handler(default_handler)

    def config_error_handler(ctx: ErrorContext) -> None:
        logger.error(
            f"Configuration error: {str(ctx.error)}",
            extra=ctx.context
        )
    handler.register_handler(ConfigError, config_error_handler)
    logger.info("Registered default error handlers")


def get_traceback_str(exc_info=None) -> str:
    if exc_info is None:
        exc_info = sys.exc_info()
    return ''.join(traceback.format_exception(*exc_info))


def try_except_decorator(
    source: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
    default: Any = None
):
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
