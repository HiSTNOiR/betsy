"""
Logging configuration for the Twitch bot.
"""
import os
import logging
import logging.handlers
from pathlib import Path
from datetime import datetime
from typing import Optional

# Default log format
DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DEFAULT_LOG_LEVEL = logging.INFO
DEFAULT_LOG_DIR = 'logs'

def setup_logging(
    log_level: int = DEFAULT_LOG_LEVEL,
    log_format: str = DEFAULT_LOG_FORMAT,
    log_dir: Optional[str] = DEFAULT_LOG_DIR,
    console: bool = True,
    log_file: bool = True,
    max_bytes: int = 10485760,  # 10MB
    backup_count: int = 5
) -> None:
    """
    Set up logging for the application.
    
    Args:
        log_level: Logging level (default: INFO)
        log_format: Log message format
        log_dir: Directory for log files (default: 'logs')
        console: Whether to log to console (default: True)
        log_file: Whether to log to file (default: True)
        max_bytes: Maximum size of log file before rotation (default: 10MB)
        backup_count: Number of backup log files to keep (default: 5)
    """
    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Clear existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create formatter
    formatter = logging.Formatter(log_format)
    
    # Add console handler
    if console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
    
    # Add file handler
    if log_file and log_dir:
        # Create log directory if it doesn't exist
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)
        
        # Create rotating file handler
        today = datetime.now().strftime('%Y-%m-%d')
        log_file_path = log_path / f'bot_{today}.log'
        file_handler = logging.handlers.RotatingFileHandler(
            log_file_path,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Create loggers for external libraries with higher log level to reduce noise
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('websocket').setLevel(logging.WARNING)
    logging.getLogger('twitchio').setLevel(logging.WARNING)
    
    # Log startup message
    logging.info("Logging initialised")

def get_logger(name: str) -> logging.Logger:
    """
    Get logger for module.
    
    Args:
        name: Module name
    
    Returns:
        Logger for module
    """
    return logging.getLogger(name)

class LoggingContext:
    """Context manager for temporarily changing log level."""
    
    def __init__(self, logger: logging.Logger, level: int):
        """
        Initialise context manager.
        
        Args:
            logger: Logger to modify
            level: Temporary log level
        """
        self.logger = logger
        self.level = level
        self.old_level = logger.level
    
    def __enter__(self) -> logging.Logger:
        """
        Enter context, set temporary log level.
        
        Returns:
            Modified logger
        """
        self.logger.setLevel(self.level)
        return self.logger
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Exit context, restore original log level.
        
        Args:
            exc_type: Exception type if exception occurred
            exc_val: Exception value if exception occurred
            exc_tb: Exception traceback if exception occurred
        """
        self.logger.setLevel(self.old_level)

def set_debug_mode(enable: bool = True) -> None:
    """
    Enable or disable debug mode (sets root logger to DEBUG level).
    
    Args:
        enable: Whether to enable debug mode (default: True)
    """
    level = logging.DEBUG if enable else DEFAULT_LOG_LEVEL
    logging.getLogger().setLevel(level)
    logging.info(f"Debug mode {'enabled' if enable else 'disabled'}")