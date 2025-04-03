import os
import sys
import logging
from enum import Enum
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path
from typing import Dict, Optional, Union, List, Any, Tuple, Callable

try:
    from bot.core.constants import LOGS_DIR
except ImportError:
    LOGS_DIR = Path("logs")


class LogLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class LoggingError(Exception):
    pass


class ConfigurationError(LoggingError):
    pass


class HandlerError(LoggingError):
    pass


def validate_log_level(level: Union[int, str]) -> int:
    if isinstance(level, int):
        standard_levels = [l.value for l in LogLevel]
        if level not in standard_levels and not (0 <= level <= 50):
            raise ConfigurationError(f"Invalid logging level integer: {level}")
        return level
    if isinstance(level, str):
        level_upper = level.upper()
        try:
            return LogLevel[level_upper].value
        except KeyError:
            try:
                return getattr(logging, level_upper)
            except AttributeError:
                raise ConfigurationError(
                    f"Invalid logging level string: {level}")
    raise ConfigurationError(
        f"Logging level must be int or string, got {type(level).__name__}")


def create_log_directory(log_file: Optional[Union[str, Path]] = None) -> Optional[Path]:
    try:
        if log_file:
            log_path = Path(log_file)
            log_dir = log_path.parent
            os.makedirs(log_dir, exist_ok=True)
            return log_path
        elif LOGS_DIR:
            os.makedirs(LOGS_DIR, exist_ok=True)
            return LOGS_DIR / "bot.log"
        return None
    except (PermissionError, OSError) as e:
        raise ConfigurationError(
            f"Cannot create log directory: {str(e)}") from e


def create_formatter(log_format: Optional[str] = None, date_format: Optional[str] = None) -> logging.Formatter:
    if not log_format:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    if not date_format:
        date_format = "%Y-%m-%d %H:%M:%S"
    return logging.Formatter(log_format, date_format)


def add_console_handler(
    logger: logging.Logger,
    formatter: logging.Formatter,
    level: int = logging.NOTSET
) -> logging.Handler:
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    if level != logging.NOTSET:
        console_handler.setLevel(level)
    logger.addHandler(console_handler)
    return console_handler


def add_file_handler(
    logger: logging.Logger,
    log_file: Union[str, Path],
    formatter: logging.Formatter,
    file_rotation: bool = True,
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 5,
    level: int = logging.NOTSET
) -> logging.Handler:
    try:
        if file_rotation:
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding="utf-8",
                delay=True
            )
        else:
            file_handler = logging.handlers.TimedRotatingFileHandler(
                log_file,
                when="midnight",
                backupCount=backup_count,
                encoding="utf-8",
                delay=True
            )
            file_handler.when = "midnight"
        file_handler.setFormatter(formatter)
        if level != logging.NOTSET:
            file_handler.setLevel(level)
        logger.addHandler(file_handler)
        return file_handler
    except (PermissionError, OSError) as e:
        raise HandlerError(f"Cannot create file handler: {str(e)}") from e


def setup_logging(
    level: Union[int, str] = logging.INFO,
    log_file: Optional[Union[str, Path]] = None,
    console: bool = True,
    file_rotation: bool = True,
    max_bytes: int = 10 * 1024 * 1024,  # 10 MB
    backup_count: int = 5,
    log_format: Optional[str] = None,
    date_format: Optional[str] = None,
    console_level: Optional[Union[int, str]] = None,
    file_level: Optional[Union[int, str]] = None,
) -> logging.Logger:
    try:
        validated_level = validate_log_level(level)
        log_path = create_log_directory(log_file)
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        root_logger.setLevel(validated_level)
        formatter = create_formatter(log_format, date_format)
        if console:
            console_handler_level = validate_log_level(
                console_level) if console_level else logging.NOTSET
            add_console_handler(root_logger, formatter, console_handler_level)
        if log_path:
            file_handler_level = validate_log_level(
                file_level) if file_level else logging.NOTSET
            add_file_handler(
                root_logger,
                log_path,
                formatter,
                file_rotation,
                max_bytes,
                backup_count,
                file_handler_level
            )
        logger = logging.getLogger(__name__)
        logger.info("Logging configured successfully")
        return root_logger
    except (ConfigurationError, HandlerError) as e:
        raise
    except Exception as e:
        raise LoggingError(f"Error setting up logging: {str(e)}") from e


def get_module_logger(module_name: str) -> logging.Logger:
    return logging.getLogger(module_name)


def set_log_level(
    level: Union[int, str],
    logger_name: Optional[str] = None
) -> None:
    validated_level = validate_log_level(level)
    logger = logging.getLogger(
        logger_name) if logger_name else logging.getLogger()
    logger.setLevel(validated_level)


class LoggerAdapter(logging.LoggerAdapter):
    def __init__(self, logger: logging.Logger, extra: Optional[Dict] = None):
        super().__init__(logger, extra or {})

    def process(self, msg, kwargs) -> Tuple[str, Dict]:
        extra_context = " ".join(f"{k}={v}" for k, v in self.extra.items())
        if extra_context:
            msg = f"{msg} [{extra_context}]"
        return msg, kwargs


def get_context_logger(module_name: str, **context) -> LoggerAdapter:
    logger = logging.getLogger(module_name)
    return LoggerAdapter(logger, context)


def reset_logging() -> None:
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        handler.close()
        root_logger.removeHandler(handler)
    root_logger.setLevel(logging.WARNING)
