"""
Validation utility functions for the Twitch bot.
"""
import re
import logging
from typing import Union, Optional, List, Dict, Any, Tuple

from bot.core.errors import ValidationError

# Set up logger
logger = logging.getLogger(__name__)

def validate_boolean(value: Union[str, bool]) -> bool:
    """
    Validate and convert a string or boolean value to a boolean.
    
    Args:
        value: String or boolean value to validate and convert
    
    Returns:
        Validated boolean value
    
    Raises:
        ValueError: If value cannot be converted to a valid boolean
    """
    if isinstance(value, bool):
        return value
    
    if isinstance(value, str):
        value = value.lower().strip()
        if value in ('true', 't', 'yes', 'y', '1', 'on'):
            return True
        if value in ('false', 'f', 'no', 'n', '0', 'off'):
            return False
    
    raise ValueError(f"Cannot convert '{value}' to a boolean")

def validate_port(value: Union[str, int]) -> int:
    """
    Validate that a value is a valid port number (1-65535).
    
    Args:
        value: String or integer value to validate
    
    Returns:
        Validated port number as integer
    
    Raises:
        ValueError: If value is not a valid port number
    """
    try:
        port = int(value)
        if port < 1 or port > 65535:
            raise ValueError(f"Port must be between 1 and 65535, got {port}")
        return port
    except (ValueError, TypeError):
        raise ValueError(f"Invalid port number: {value}")

def validate_username(username: str) -> str:
    """
    Validate a Twitch username.
    
    Args:
        username: Twitch username to validate
    
    Returns:
        Validated username (lowercase)
    
    Raises:
        ValidationError: If username is invalid
    """
    if not username:
        raise ValidationError("Username cannot be empty")
    
    # Twitch usernames must be between 4 and 25 characters
    if len(username) < 4 or len(username) > 25:
        raise ValidationError(f"Username must be between 4 and 25 characters: {username}")
    
    # Twitch usernames can only contain alphanumeric characters and underscores
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        raise ValidationError(f"Username can only contain letters, numbers, and underscores: {username}")
    
    # Return lowercase username for consistency
    return username.lower()

def validate_command(command: str) -> str:
    """
    Validate a command string.
    
    Args:
        command: Command string to validate
    
    Returns:
        Validated command string (lowercase)
    
    Raises:
        ValidationError: If command is invalid
    """
    if not command:
        raise ValidationError("Command cannot be empty")
    
    # Remove prefix if present
    if command.startswith('!'):
        command = command[1:]
    
    # Command must be at least 1 character
    if not command:
        raise ValidationError("Command must be at least 1 character long")
    
    # Command can only contain alphanumeric characters and underscores
    if not re.match(r'^[a-zA-Z0-9_]+$', command):
        raise ValidationError(f"Command can only contain letters, numbers, and underscores: {command}")
    
    # Return lowercase command for consistency
    return command.lower()

def validate_integer(value: Union[str, int], min_value: Optional[int] = None, 
                    max_value: Optional[int] = None) -> int:
    """
    Validate that a value is a valid integer within optional range.
    
    Args:
        value: String or integer value to validate
        min_value: Optional minimum value (inclusive)
        max_value: Optional maximum value (inclusive)
    
    Returns:
        Validated integer value
    
    Raises:
        ValueError: If value is not a valid integer or is out of range
    """
    try:
        result = int(value)
        
        if min_value is not None and result < min_value:
            raise ValueError(f"Value must be at least {min_value}, got {result}")
        
        if max_value is not None and result > max_value:
            raise ValueError(f"Value must be at most {max_value}, got {result}")
            
        return result
    except (ValueError, TypeError):
        raise ValueError(f"Invalid integer value: {value}")

def validate_contains_emoji(message: str) -> bool:
    """
    Check if a message contains emoji.
    
    Args:
        message: Message to check
    
    Returns:
        True if message contains emoji, False otherwise
    """
    # Simple emoji regex pattern - can be expanded for more complex patterns
    emoji_pattern = re.compile(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251]+')
    return bool(emoji_pattern.search(message))

def validate_contains_only_numbers(message: str) -> bool:
    """
    Check if a message contains only numbers.
    
    Args:
        message: Message to check
    
    Returns:
        True if message contains only numbers, False otherwise
    """
    return bool(re.match(r'^\d+$', message))

def validate_points(value: Union[str, int]) -> int:
    """
    Validate that a value is a valid points value (non-negative integer).
    
    Args:
        value: String or integer value to validate
    
    Returns:
        Validated points value as integer
    
    Raises:
        ValueError: If value is not a valid points value
    """
    try:
        points = int(value)
        if points < 0:
            raise ValueError(f"Points must be non-negative, got {points}")
        return points
    except (ValueError, TypeError):
        raise ValueError(f"Invalid points value: {value}")

def validate_item_name(item_name: str) -> str:
    """
    Validate an item name.
    
    Args:
        item_name: Item name to validate
    
    Returns:
        Validated item name
    
    Raises:
        ValidationError: If item name is invalid
    """
    if not item_name:
        raise ValidationError("Item name cannot be empty")
    
    # Simple validation - just ensure it's not empty and trim whitespace
    return item_name.strip()

def validate_user_input(user_input: str, allowed_chars: str = 'a-zA-Z0-9_\\s\\-') -> str:
    """
    Validate and sanitise user input to prevent injection attacks.
    
    Args:
        user_input: User input to validate
        allowed_chars: Regex character class of allowed characters
    
    Returns:
        Validated and sanitised user input
    
    Raises:
        ValidationError: If user input contains invalid characters
    """
    if not user_input:
        return ""
    
    # Check for invalid characters
    if not re.match(f'^[{allowed_chars}]+$', user_input):
        # Find the invalid characters for better error message
        invalid_chars = re.findall(f'[^{allowed_chars}]', user_input)
        invalid_chars_str = ', '.join(set(invalid_chars))
        raise ValidationError(f"Input contains invalid characters: {invalid_chars_str}")
    
    # Return sanitised input
    return user_input.strip()