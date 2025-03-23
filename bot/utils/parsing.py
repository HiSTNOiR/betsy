"""
Parsing utility functions for the Twitch bot.
"""
import re
import shlex
import logging
from typing import List, Dict, Any, Optional, Tuple, Union, Set

from bot.core.errors import ValidationError

# Set up logger
logger = logging.getLogger(__name__)

def parse_command(message: str, prefix: str = '!') -> Tuple[Optional[str], str]:
    """
    Parse a command from a message.
    
    Args:
        message: Message to parse
        prefix: Command prefix (default: '!')
    
    Returns:
        Tuple of (command, args) or (None, original_message) if no command found
    """
    if not message:
        return None, ""
    
    message = message.strip()
    
    # Check if message starts with prefix
    if not message.startswith(prefix):
        return None, message
    
    # Split into command and arguments
    parts = message[len(prefix):].strip().split(maxsplit=1)
    command = parts[0].lower() if parts else ""
    args = parts[1] if len(parts) > 1 else ""
    
    return command, args

def parse_args(args_str: str) -> List[str]:
    """
    Parse arguments from a string, handling quoted arguments.
    
    Args:
        args_str: Arguments string
    
    Returns:
        List of parsed arguments
    """
    if not args_str:
        return []
    
    try:
        # Use shlex to handle quoted arguments properly
        return shlex.split(args_str)
    except ValueError as e:
        logger.warning(f"Error parsing arguments: {e}")
        # Fallback to simple splitting
        return args_str.split()

def extract_user_and_amount(args_str: str) -> Tuple[Optional[str], Optional[int]]:
    """
    Extract a username and amount from arguments.
    
    Args:
        args_str: Arguments string, expected in the format "username amount"
    
    Returns:
        Tuple of (username, amount) or (None, None) if parsing fails
    """
    args = parse_args(args_str)
    
    if len(args) < 2:
        return None, None
    
    # Get username (first argument)
    username = args[0].lstrip('@')
    
    # Get amount (second argument)
    try:
        amount = int(args[1])
        if amount < 0:
            return username, None
        return username, amount
    except ValueError:
        return username, None

def parse_key_value_pairs(text: str, separator: str = '=', 
                        delimiter: str = ',') -> Dict[str, str]:
    """
    Parse key-value pairs from a string.
    
    Args:
        text: Text containing key-value pairs
        separator: Character separating keys and values (default: '=')
        delimiter: Character separating pairs (default: ',')
    
    Returns:
        Dictionary of key-value pairs
    """
    if not text:
        return {}
    
    result = {}
    pairs = text.split(delimiter)
    
    for pair in pairs:
        if separator in pair:
            key, value = pair.split(separator, 1)
            result[key.strip()] = value.strip()
    
    return result

def extract_targets(args_str: str) -> List[str]:
    """
    Extract target usernames from arguments.
    
    Args:
        args_str: Arguments string
    
    Returns:
        List of target usernames
    """
    args = parse_args(args_str)
    
    # Remove @ symbol from usernames if present
    return [arg.lstrip('@') for arg in args]

def safe_int_conversion(value: Any, default: int = 0) -> int:
    """
    Safely convert a value to integer.
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
    
    Returns:
        Converted integer or default
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def safe_float_conversion(value: Any, default: float = 0.0) -> float:
    """
    Safely convert a value to float.
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
    
    Returns:
        Converted float or default
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def safe_bool_conversion(value: Any, default: bool = False) -> bool:
    """
    Safely convert a value to boolean.
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
    
    Returns:
        Converted boolean or default
    """
    if isinstance(value, bool):
        return value
    
    if isinstance(value, str):
        value = value.lower()
        if value in ('true', 'yes', 'y', '1', 'on'):
            return True
        if value in ('false', 'no', 'n', '0', 'off'):
            return False
    
    try:
        return bool(value)
    except (ValueError, TypeError):
        return default

def parse_duration(duration_str: str) -> Optional[int]:
    """
    Parse a duration string into seconds.
    
    Args:
        duration_str: Duration string (e.g., '1h30m', '45s', '2d')
    
    Returns:
        Duration in seconds or None if parsing fails
    """
    if not duration_str:
        return None
    
    total_seconds = 0
    pattern = re.compile(r'(\d+)([dhms])')
    
    matches = pattern.findall(duration_str.lower())
    if not matches:
        # Try parsing as plain seconds
        try:
            return int(duration_str)
        except ValueError:
            return None
    
    for value, unit in matches:
        try:
            value = int(value)
            if unit == 'd':
                total_seconds += value * 86400  # days to seconds
            elif unit == 'h':
                total_seconds += value * 3600   # hours to seconds
            elif unit == 'm':
                total_seconds += value * 60     # minutes to seconds
            elif unit == 's':
                total_seconds += value          # seconds
        except ValueError:
            logger.warning(f"Invalid value in duration: {value}{unit}")
    
    return total_seconds

def parse_item_name(item_str: str) -> str:
    """
    Parse an item name from a string.
    
    Args:
        item_str: String containing item name
    
    Returns:
        Cleaned item name
    """
    if not item_str:
        return ""
    
    # Remove any special characters and extra whitespace
    item_name = re.sub(r'[^\w\s]', '', item_str).strip()
    
    # Normalise whitespace
    item_name = re.sub(r'\s+', ' ', item_name)
    
    return item_name

def parse_bits_amount(message: str) -> Optional[int]:
    """
    Parse bits amount from a Twitch cheer message.
    
    Args:
        message: Message to parse
    
    Returns:
        Bits amount or None if parsing fails
    """
    # Twitch cheer messages contain patterns like "cheer100", "Cheer1000", etc.
    match = re.search(r'[cC]heer(\d+)', message)
    if match:
        try:
            return int(match.group(1))
        except ValueError:
            return None
    return None

def extract_command_with_targets(message: str, prefix: str = '!') -> Tuple[Optional[str], List[str], str]:
    """
    Extract command, targets, and remaining arguments from a message.
    
    Args:
        message: Message to parse
        prefix: Command prefix (default: '!')
    
    Returns:
        Tuple of (command, targets, remaining_args)
    """
    command, args = parse_command(message, prefix)
    if not command:
        return None, [], args
    
    args_list = parse_args(args)
    targets = []
    remaining = []
    
    # Extract targets (words starting with @)
    for arg in args_list:
        if arg.startswith('@'):
            targets.append(arg[1:])  # Remove @
        else:
            remaining.append(arg)
    
    return command, targets, ' '.join(remaining)

def is_valid_target_for_self(target: str, sender: str) -> bool:
    """
    Check if a target is valid for self-targeting commands.
    
    Args:
        target: Target username
        sender: Sender username
    
    Returns:
        True if target is valid for self-targeting, False otherwise
    """
    # Compare without @ symbol and case-insensitive
    target = target.lstrip('@').lower()
    sender = sender.lstrip('@').lower()
    
    return target != sender

def fuzzy_match_item(item_name: str, item_list: List[str], threshold: float = 0.75) -> Optional[str]:
    """
    Find closest matching item name using fuzzy matching.
    
    Args:
        item_name: Item name to match
        item_list: List of valid item names
        threshold: Similarity threshold (0.0-1.0)
    
    Returns:
        Closest matching item name or None if no match above threshold
    """
    # This is a very simple implementation
    # For better fuzzy matching, consider using libraries like fuzzywuzzy
    
    item_name_lower = item_name.lower()
    
    # Try exact match first
    for item in item_list:
        if item.lower() == item_name_lower:
            return item
    
    # Try prefix match
    for item in item_list:
        if item.lower().startswith(item_name_lower):
            return item
    
    # TODO: Implement proper fuzzy matching with similarity score
    # For now, just return None
    return None