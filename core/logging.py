import logging
import logging.handlers
import os
import sys

from pathlib import Path
from typing import Dict, Optional, Union, List, Literal

from core.config import config, ConfigurationError

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class LoggingManager:
    _instance = None
    _initialised = False
    _loggers: Dict[str, logging.Logger] = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LoggingManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialised:
            self._configure_defaults()
            self._initialised = True

    def _configure_defaults(self) -> None:
        try:
            self.log_dir = config.get_path('LOG_DIR', 'logs')
            self.log_level = config.get('LOG_LEVEL', 'INFO').upper()
            self.log_format = config.get('LOG_FORMAT',
                                         '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            self.max_bytes = config.get_int(
                'LOG_MAX_BYTES', 5 * 1024 * 1024)  # 5MB default
            self.backup_count = config.get_int('LOG_BACKUP_COUNT', 5)
            self.console_output = config.get_boolean(
                'LOG_CONSOLE_OUTPUT', True)

            os.makedirs(self.log_dir, exist_ok=True)

            # Handle UTF-8 encoding for console output in Windows
            if self.console_output:
                import sys
                if sys.platform == 'win32':
                    import codecs
                    sys.stdout.reconfigure(encoding='utf-8')
                    sys.stderr.reconfigure(encoding='utf-8')

        except (ConfigurationError, OSError) as e:
            print(f"Error configuring logging: {e}", file=sys.stderr)
            # Set fallback values
            self.log_dir = Path('logs')
            self.log_level = "INFO"
            self.log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            self.max_bytes = 5 * 1024 * 1024
            self.backup_count = 5
            self.console_output = True
            os.makedirs(self.log_dir, exist_ok=True)

    def get_logger(self, name: str) -> logging.Logger:
        if name in self._loggers:
            return self._loggers[name]

        logger = logging.getLogger(name)

        # Avoid duplicate handlers
        if logger.handlers:
            self._loggers[name] = logger
            return logger

        logger.setLevel(self._get_log_level(self.log_level))

        # File handler with rotation
        file_path = self.log_dir / f"{name}.log"
        file_handler = logging.handlers.RotatingFileHandler(
            file_path,
            maxBytes=self.max_bytes,
            backupCount=self.backup_count,
            encoding='utf-8'  # Ensure UTF-8 encoding for file output
        )
        formatter = logging.Formatter(self.log_format)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Console handler if enabled
        if self.console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        self._loggers[name] = logger
        return logger

    def update_log_level(self, name: str, level: Union[LogLevel, int]) -> None:
        if name not in self._loggers:
            raise ValueError(f"Logger '{name}' not found")

        if isinstance(level, str):
            level = self._get_log_level(level)

        self._loggers[name].setLevel(level)

    def update_all_log_levels(self, level: Union[LogLevel, int]) -> None:
        if isinstance(level, str):
            level = self._get_log_level(level)

        for logger in self._loggers.values():
            logger.setLevel(level)

    def _get_log_level(self, level: str) -> int:
        levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL
        }

        return levels.get(level.upper(), logging.INFO)

    def disable_console_logging(self, name: Optional[str] = None) -> None:
        if name:
            loggers = [self._loggers[name]] if name in self._loggers else []
        else:
            loggers = list(self._loggers.values())

        for logger in loggers:
            for handler in logger.handlers[:]:
                if isinstance(handler, logging.StreamHandler) and handler.stream in (sys.stdout, sys.stderr):
                    logger.removeHandler(handler)

    def enable_console_logging(self, name: Optional[str] = None) -> None:
        if name:
            loggers = [self._loggers[name]] if name in self._loggers else []
        else:
            loggers = list(self._loggers.values())

        for logger in loggers:
            has_console_handler = any(
                isinstance(handler, logging.StreamHandler) and
                handler.stream in (sys.stdout, sys.stderr)
                for handler in logger.handlers
            )

            if not has_console_handler:
                console_handler = logging.StreamHandler(sys.stdout)
                console_handler.setFormatter(
                    logging.Formatter(self.log_format))
                logger.addHandler(console_handler)

    def add_handler(self, name: str, handler: logging.Handler) -> None:
        if name not in self._loggers:
            raise ValueError(f"Logger '{name}' not found")

        self._loggers[name].addHandler(handler)

    def remove_all_handlers(self, name: str) -> None:
        if name not in self._loggers:
            raise ValueError(f"Logger '{name}' not found")

        logger = self._loggers[name]
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)


logging_manager = LoggingManager()


def get_logger(name: str) -> logging.Logger:
    return logging_manager.get_logger(name)
