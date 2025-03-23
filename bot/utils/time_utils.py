"""
Time utility functions for the Twitch bot.
"""
import time
import logging
import random
from datetime import datetime, timedelta, timezone
from typing import Optional, Union, Callable, Any, Dict, List

# Set up logger
logger = logging.getLogger(__name__)

def get_current_timestamp() -> float:
    """
    Get current Unix timestamp.
    
    Returns:
        Current timestamp as float
    """
    return time.time()

def get_current_datetime() -> datetime:
    """
    Get current datetime with timezone info (UTC).
    
    Returns:
        Current datetime
    """
    return datetime.now(timezone.utc)

def get_formatted_datetime(dt: Optional[datetime] = None, 
                         format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    Format a datetime object as string.
    
    Args:
        dt: Datetime to format (default: current time)
        format_str: Format string (default: '%Y-%m-%d %H:%M:%S')
    
    Returns:
        Formatted datetime string
    """
    if dt is None:
        dt = get_current_datetime()
    
    return dt.strftime(format_str)

def parse_datetime(datetime_str: str, 
                 format_str: str = '%Y-%m-%d %H:%M:%S') -> Optional[datetime]:
    """
    Parse a datetime string to a datetime object.
    
    Args:
        datetime_str: Datetime string to parse
        format_str: Format string (default: '%Y-%m-%d %H:%M:%S')
    
    Returns:
        Parsed datetime object or None if parsing fails
    """
    try:
        return datetime.strptime(datetime_str, format_str)
    except ValueError as e:
        logger.warning(f"Failed to parse datetime '{datetime_str}': {e}")
        return None

def datetime_to_timestamp(dt: datetime) -> float:
    """
    Convert a datetime object to Unix timestamp.
    
    Args:
        dt: Datetime to convert
    
    Returns:
        Unix timestamp
    """
    return dt.timestamp()

def timestamp_to_datetime(timestamp: float) -> datetime:
    """
    Convert a Unix timestamp to datetime object.
    
    Args:
        timestamp: Unix timestamp
    
    Returns:
        Datetime object
    """
    return datetime.fromtimestamp(timestamp, timezone.utc)

def get_time_difference(dt1: datetime, dt2: datetime) -> timedelta:
    """
    Get time difference between two datetime objects.
    
    Args:
        dt1: First datetime
        dt2: Second datetime
    
    Returns:
        Time difference as timedelta
    """
    return abs(dt1 - dt2)

def get_time_difference_seconds(dt1: datetime, dt2: datetime) -> float:
    """
    Get time difference between two datetime objects in seconds.
    
    Args:
        dt1: First datetime
        dt2: Second datetime
    
    Returns:
        Time difference in seconds
    """
    return abs((dt1 - dt2).total_seconds())

def is_expired(timestamp: float, expiry_seconds: float) -> bool:
    """
    Check if a timestamp has expired.
    
    Args:
        timestamp: Timestamp to check
        expiry_seconds: Expiry time in seconds
    
    Returns:
        True if timestamp has expired, False otherwise
    """
    return (get_current_timestamp() - timestamp) > expiry_seconds

def get_random_delay(min_seconds: float = 0.5, max_seconds: float = 3.0) -> float:
    """
    Get a random delay between min and max seconds.
    
    Args:
        min_seconds: Minimum delay in seconds
        max_seconds: Maximum delay in seconds
    
    Returns:
        Random delay in seconds
    """
    return random.uniform(min_seconds, max_seconds)

def sleep(seconds: float) -> None:
    """
    Sleep for the specified number of seconds.
    
    Args:
        seconds: Number of seconds to sleep
    """
    time.sleep(seconds)

def with_timeout(func: Callable, timeout: float, *args: Any, **kwargs: Any) -> Any:
    """
    Execute a function with a timeout.
    
    Args:
        func: Function to execute
        timeout: Timeout in seconds
        *args: Arguments to pass to function
        **kwargs: Keyword arguments to pass to function
    
    Returns:
        Result of function or None if timeout
    
    Raises:
        TimeoutError: If function execution exceeds timeout
    """
    # This is a simplified implementation
    # For more robust timeout handling, consider using concurrent.futures or similar
    
    start_time = get_current_timestamp()
    result = func(*args, **kwargs)
    execution_time = get_current_timestamp() - start_time
    
    if execution_time > timeout:
        logger.warning(f"Function {func.__name__} exceeded timeout of {timeout}s (took {execution_time:.2f}s)")
        raise TimeoutError(f"Function {func.__name__} timed out after {execution_time:.2f}s")
    
    return result

def get_time_until(target_time: datetime) -> timedelta:
    """
    Get time remaining until a target time.
    
    Args:
        target_time: Target datetime
    
    Returns:
        Time remaining as timedelta
    """
    now = get_current_datetime()
    if target_time < now:
        return timedelta(0)
    return target_time - now

def get_cooldown_end_time(cooldown_seconds: float) -> datetime:
    """
    Calculate when a cooldown will end.
    
    Args:
        cooldown_seconds: Cooldown duration in seconds
    
    Returns:
        Datetime when cooldown ends
    """
    return get_current_datetime() + timedelta(seconds=cooldown_seconds)

def format_cooldown_remaining(end_time: datetime) -> str:
    """
    Format remaining cooldown time.
    
    Args:
        end_time: Cooldown end time
    
    Returns:
        Formatted cooldown time string
    """
    remaining = get_time_until(end_time)
    return format_timedelta(remaining)