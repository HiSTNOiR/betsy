"""
Logging configuration for the bot.

This module provides functionality to set up and configure logging throughout the application.
"""

import os
import sys
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path
from typing import Dict, Optional, Union

from bot.core.constants import LOGS_DIR


class LoggingError(Exception):
    """Base exception for logging-related errors."""
    pass


def setup_logging(
    level: Union[int, str] = logging.INFO,
    log_file: Optional[Union[str, Path]] = None,
    console: bool = True,
    file_rotation: bool = True,
    max_bytes: int = 10 * 1024 * 1024,  # 10 MB
    backup_count: int = 5,
    log_format: Optional[str] = None,
    date_format: Optional[str] = None,
) -> logging.Logger:
    """
    Configure logging for the application.

    Args:
        level (Union[int, str]): Logging level.
        log_file (Optional[Union[str, Path]]): Path to log file.
        console (bool): Whether to log to console.
        file_rotation (bool): Whether to use rotating file handler.
        max_bytes (int): Maximum log file size before rotation.
        backup_count (int): Number of backup files to keep.
        log_format (Optional[str]): Custom log format.
        date_format (Optional[str]): Custom date format.

    Returns:
        logging.Logger: Root logger.

    Raises:
        LoggingError: If there is an error setting up logging.
    """
    try:
        # Create logs directory if it doesn't exist
        if log_file:
            log_path = Path(log_file)
            log_dir = log_path.parent
            os.makedirs(log_dir, exist_ok=True)
        elif LOGS_DIR:
            os.makedirs(LOGS_DIR, exist_ok=True)
            log_file = LOGS_DIR / "bot.log"

        # Get the root logger
        root_logger = logging.getLogger()

        # Clear any existing handlers
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        # Set logging level
        if isinstance(level, str):
            level = getattr(logging, level.upper(), logging.INFO)
        root_logger.setLevel(level)

        # Set format for logs
        if not log_format:
            log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        if not date_format:
            date_format = "%Y-%m-%d %H:%M:%S"

        formatter = logging.Formatter(log_format, date_format)

        # Add console handler if requested
        if console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            root_logger.addHandler(console_handler)

        # Add file handler if log_file is provided
        if log_file:
            if file_rotation:
                file_handler = RotatingFileHandler(
                    log_file,
                    maxBytes=max_bytes,
                    backupCount=backup_count,
                    encoding="utf-8",
                )
            else:
                file_handler = TimedRotatingFileHandler(
                    log_file,
                    when="midnight",
                    backupCount=backup_count,
                    encoding="utf-8",
                )
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)

        # Create a logger for this module
        logger = logging.getLogger(__name__)
        logger.info("Logging configured successfully")

        return root_logger

    except Exception as e:
        raise LoggingError(f"Error setting up logging: {str(e)}") from e


def get_module_logger(module_name: str) -> logging.Logger:
    """
    Get a logger for a specific module.

    Args:
        module_name (str): Module name.

    Returns:
        logging.Logger: Logger for the module.
    """
    return logging.getLogger(module_name)


def set_log_level(
    level: Union[int, str],
    logger_name: Optional[str] = None
) -> None:
    """
    Set the logging level for a logger.

    Args:
        level (Union[int, str]): Logging level.
        logger_name (Optional[str]): Logger name. If None, sets level for root logger.
    """
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)

    logger = logging.getLogger(
        logger_name) if logger_name else logging.getLogger()
    logger.setLevel(level)


class LoggerAdapter(logging.LoggerAdapter):
    """
    Custom logger adapter that adds context to log messages.

    This adapter can be used to add custom context to log messages,
    such as user ID, command name, etc.
    """

    def __init__(self, logger: logging.Logger, extra: Optional[Dict] = None):
        """
        Initialize the adapter.

        Args:
            logger (logging.Logger): Logger to adapt.
            extra (Optional[Dict]): Extra context to add to log messages.
        """
        super().__init__(logger, extra or {})

    def process(self, msg, kwargs):
        """
        Process the log message.

        Args:
            msg: Log message.
            kwargs: Keyword arguments for the log method.

        Returns:
            Tuple[str, Dict]: Processed message and arguments.
        """
        extra_context = " ".join(f"{k}={v}" for k, v in self.extra.items())
        if extra_context:
            msg = f"{msg} [{extra_context}]"
        return msg, kwargs


def get_context_logger(module_name: str, **context) -> LoggerAdapter:
    """
    Get a logger with context for a specific module.

    Args:
        module_name (str): Module name.
        **context: Additional context to add to log messages.

    Returns:
        LoggerAdapter: Logger adapter with context.
    """
    logger = logging.getLogger(module_name)
    return LoggerAdapter(logger, context)
