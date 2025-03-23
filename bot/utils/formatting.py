"""
Formatting utility functions for the Twitch bot.
"""
import re
import logging
from typing import Union, Dict, Any, List, Optional

# Set up logger
logger = logging.getLogger(__name__)

def format_points(points: Union[int, str], abbreviate: bool = False) -> str:
    """
    Format points as a string with commas for thousands.
    
    Args:
        points: Points value to format
        abbreviate: Whether to abbreviate large numbers (e.g., 1.5K, 2.3M)
    
    Returns:
        Formatted points string
    """
    try:
        value = int(points)
        
        if abbreviate:
            if value >= 1_000_000_000:
                return f"{value / 1_000_000_000:.1f}B"
            elif value >= 1_000_000:
                return f"{value / 1_000_000:.1f}M"
            elif value >= 1_000:
                return f"{value / 1_000:.1f}K"
        
        return f"{value:,}"
    except (ValueError, TypeError):
        logger.warning(f"Invalid points value: {points}")
        return str(points)

def format_username(username: str) -> str:
    """
    Format a username for consistency.
    
    Args:
        username: Username to format
    
    Returns:
        Formatted username (lowercase, no spaces)
    """
    if not username:
        return ""
    
    # Remove @ symbol if present
    if username.startswith('@'):
        username = username[1:]
    
    # Remove spaces and convert to lowercase
    return username.strip().lower()

def format_command(command: str, prefix: str = '!') -> str:
    """
    Format a command string.
    
    Args:
        command: Command to format
        prefix: Command prefix (default: '!')
    
    Returns:
        Formatted command string
    """
    if not command:
        return ""
    
    # Remove prefix if present (will add it back)
    if command.startswith(prefix):
        command = command[len(prefix):]
    
    # Clean up the command
    command = command.strip().lower()
    
    # Add prefix back
    return f"{prefix}{command}"

def format_duration(seconds: Union[int, float]) -> str:
    """
    Format a duration in seconds as a human-readable string.
    
    Args:
        seconds: Duration in seconds
    
    Returns:
        Formatted duration string (e.g., "2h 30m 15s")
    """
    try:
        total_seconds = int(seconds)
        
        # Handle negative durations
        if total_seconds < 0:
            return "0s"
        
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        parts = []
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        if seconds > 0 or not parts:
            parts.append(f"{seconds}s")
        
        return " ".join(parts)
    except (ValueError, TypeError):
        logger.warning(f"Invalid duration value: {seconds}")
        return "0s"

def format_item_name(item_name: str) -> str:
    """
    Format an item name for consistency and display.
    
    Args:
        item_name: Item name to format
    
    Returns:
        Formatted item name
    """
    if not item_name:
        return ""
    
    # Capitalise each word
    words = item_name.strip().split()
    return " ".join(word.capitalise() for word in words)

def pluralise(word: str, count: int) -> str:
    """
    Pluralise a word based on count.
    
    Args:
        word: Word to pluralise
        count: Count to determine if plural form is needed
    
    Returns:
        Pluralised word if count is not 1
    """
    if count == 1:
        return word
    
    # Simple pluralisation rules
    if word.endswith('s') or word.endswith('x') or word.endswith('z') or word.endswith('ch') or word.endswith('sh'):
        return f"{word}es"
    elif word.endswith('y') and len(word) > 1 and word[-2] not in 'aeiou':
        return f"{word[:-1]}ies"
    else:
        return f"{word}s"

def format_list(items: List[str], conjunction: str = 'and') -> str:
    """
    Format a list of items into a grammatically correct string.
    
    Args:
        items: List of items to format
        conjunction: Conjunction to use (default: 'and')
    
    Returns:
        Formatted list string
    """
    if not items:
        return ""
    
    if len(items) == 1:
        return items[0]
    
    if len(items) == 2:
        return f"{items[0]} {conjunction} {items[1]}"
    
    return f"{', '.join(items[:-1])}, {conjunction} {items[-1]}"

def truncate(text: str, max_length: int = 100, suffix: str = '...') -> str:
    """
    Truncate text to a maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length of truncated text including suffix
        suffix: Suffix to add when truncating (default: '...')
    
    Returns:
        Truncated text
    """
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    # Ensure we have room for the suffix
    max_text_length = max_length - len(suffix)
    if max_text_length <= 0:
        return suffix[:max_length]
    
    return text[:max_text_length] + suffix

def normalise_name(name: str) -> str:
    """
    Normalise a name by removing spaces, special characters, and converting to lowercase.
    Useful for fuzzy matching item names, commands, etc.
    
    Args:
        name: Name to normalise
    
    Returns:
        Normalised name
    """
    if not name:
        return ""
    
    # Remove spaces and special characters, convert to lowercase
    return re.sub(r'[^a-zA-Z0-9]', '', name.lower())

def format_chat_message(message: str, user: str, is_action: bool = False) -> str:
    """
    Format a chat message for display in logs.
    
    Args:
        message: Message content
        user: Username of message sender
        is_action: Whether message is an action (/me command)
    
    Returns:
        Formatted chat message
    """
    if is_action:
        return f"* {user} {message}"
    return f"{user}: {message}"