"""
Sanitisation utility functions for the Twitch bot.
"""
import re
import html
import logging
from typing import Optional, List, Dict, Any

# Set up logger
logger = logging.getLogger(__name__)

def sanitise_input(text: str) -> str:
    """
    Sanitise user input to prevent injection attacks.
    
    Args:
        text: Input text to sanitise
    
    Returns:
        Sanitised text
    """
    if not text:
        return ""
    
    # HTML escape to prevent HTML/script injection
    sanitised = html.escape(text)
    
    # Additional sanitisation if needed for specific contexts
    # (can be expanded based on specific requirements)
    
    return sanitised

def sanitise_path(path: str) -> str:
    """
    Sanitise a file path to prevent directory traversal attacks.
    
    Args:
        path: Path to sanitise
    
    Returns:
        Sanitised path
    """
    # Normalise path
    path = os.path.normpath(path)
    
    # Remove any attempts at directory traversal
    path = re.sub(r'\.\.', '', path)
    
    return path
    
def sanitise_username(username: str) -> str:
    """
    Sanitise a username.
    
    Args:
        username: Username to sanitise
    
    Returns:
        Sanitised username
    """
    if not username:
        return ""
    
    # Remove @ symbol if present
    if username.startswith('@'):
        username = username[1:]
    
    # Remove whitespace
    username = username.strip()
    
    # Remove any potentially problematic characters
    username = re.sub(r'[^\w]', '', username)
    
    return username.lower()

def sanitise_command_args(args_str: str) -> str:
    """
    Sanitise command arguments.
    
    Args:
        args_str: Command arguments string
    
    Returns:
        Sanitised command arguments
    """
    if not args_str:
        return ""
    
    # Basic sanitisation
    args_str = args_str.strip()
    
    # You can add more specific sanitisation rules here
    
    return args_str

def sanitise_for_db(value: str) -> str:
    """
    Sanitise a value for database storage to prevent SQL injection.
    
    Note: This is a basic sanitisation. Always use parameterised queries for database operations.
    
    Args:
        value: Value to sanitise
    
    Returns:
        Sanitised value
    """
    if not value:
        return ""
    
    # Remove potentially dangerous SQL characters
    value = value.replace("'", "''")  # Escape single quotes for SQL
    
    # Additional sanitisation
    value = value.replace(";", "")  # Remove semicolons
    
    return value

def strip_twitch_emotes(message: str) -> str:
    """
    Strip Twitch emotes from a message.
    
    Args:
        message: Message to strip emotes from
    
    Returns:
        Message with emotes removed
    """
    if not message:
        return ""
    
    # This is a simple approach - actual emote detection would require
    # the emote data from Twitch's API
    message = re.sub(r':\w+:', ' ', message)
    
    # Clean up extra whitespace
    message = re.sub(r'\s+', ' ', message).strip()
    
    return message

def sanitise_html(html_content: str) -> str:
    """
    Sanitise HTML content for safe display.
    
    Args:
        html_content: HTML content to sanitise
    
    Returns:
        Sanitised HTML content
    """
    # For comprehensive HTML sanitisation, consider using a dedicated library
    # like bleach. This is a simple implementation.
    
    if not html_content:
        return ""
    
    # Define allowed tags
    allowed_tags = ['b', 'i', 'u', 'strong', 'em']
    
    # Remove all tags except allowed ones
    for tag in allowed_tags:
        # Replace allowed tags with markers
        html_content = html_content.replace(f'<{tag}>', f'__START_{tag}__')
        html_content = html_content.replace(f'</{tag}>', f'__END_{tag}__')
    
    # Remove all HTML tags
    html_content = re.sub(r'<[^>]*>', '', html_content)
    
    # Restore allowed tags
    for tag in allowed_tags:
        html_content = html_content.replace(f'__START_{tag}__', f'<{tag}>')
        html_content = html_content.replace(f'__END_{tag}__', f'</{tag}>')
    
    return html_content

def remove_non_alphanumeric(text: str, allow_spaces: bool = True) -> str:
    """
    Remove non-alphanumeric characters from text.
    
    Args:
        text: Text to process
        allow_spaces: Whether to allow spaces (default: True)
    
    Returns:
        Text with only alphanumeric characters (and optionally spaces)
    """
    if not text:
        return ""
    
    pattern = r'[^a-zA-Z0-9\s]' if allow_spaces else r'[^a-zA-Z0-9]'
    return re.sub(pattern, '', text)

def clean_numeric_string(text: str) -> str:
    """
    Clean a string to retain only numeric characters.
    
    Args:
        text: Text to clean
    
    Returns:
        Text with only numeric characters
    """
    if not text:
        return ""
    
    return re.sub(r'[^0-9]', '', text)