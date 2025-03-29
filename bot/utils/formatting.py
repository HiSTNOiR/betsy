"""
Text formatting utility functions for the bot.

This module provides utility functions for formatting text and numbers.
"""

import re
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Union


def format_number(
    number: Union[int, float],
    decimals: int = 0,
    thousands_separator: str = ",",
    decimal_separator: str = "."
) -> str:
    """
    Format a number with thousands separators and decimals.

    Args:
        number (Union[int, float]): Number to format.
        decimals (int): Number of decimal places.
        thousands_separator (str): Separator for thousands.
        decimal_separator (str): Separator for decimals.

    Returns:
        str: Formatted number as a string.
    """
    if not isinstance(number, (int, float)):
        return str(number)

    # Format the number
    if decimals == 0:
        formatted = f"{int(number):,}".replace(",", thousands_separator)
    else:
        formatted = f"{number:,.{decimals}f}".replace(",", thousands_separator)

    # Replace decimal point if needed
    if decimal_separator != ".":
        formatted = formatted.replace(".", decimal_separator)

    return formatted


def format_currency(
    amount: Union[int, float],
    currency: str = "£",
    decimals: int = 2,
    position: str = "prefix"
) -> str:
    """
    Format a currency amount.

    Args:
        amount (Union[int, float]): Amount to format.
        currency (str): Currency symbol.
        decimals (int): Number of decimal places.
        position (str): Position of the currency symbol ('prefix' or 'suffix').

    Returns:
        str: Formatted currency amount.
    """
    formatted_amount = format_number(amount, decimals)

    if position.lower() == "prefix":
        return f"{currency}{formatted_amount}"
    else:
        return f"{formatted_amount}{currency}"


def pluralise(
    count: int,
    singular: str,
    plural: Optional[str] = None,
    include_count: bool = True
) -> str:
    """
    Pluralise a word based on a count.

    Args:
        count (int): Count to determine pluralisation.
        singular (str): Singular form of the word.
        plural (Optional[str]): Plural form of the word. If None, appends 's' to singular.
        include_count (bool): Whether to include the count in the output.

    Returns:
        str: Pluralised word, optionally with count.
    """
    if plural is None:
        # Default plural form
        if singular.endswith('s') or singular.endswith('x') or singular.endswith('z') or \
           singular.endswith('ch') or singular.endswith('sh'):
            plural = singular + 'es'
        elif singular.endswith('y') and len(singular) > 1 and singular[-2] not in 'aeiou':
            plural = singular[:-1] + 'ies'
        else:
            plural = singular + 's'

    if count == 1:
        word = singular
    else:
        word = plural

    if include_count:
        return f"{count} {word}"
    else:
        return word


def truncate(
    text: str,
    max_length: int,
    suffix: str = "...",
    break_on_word: bool = True
) -> str:
    """
    Truncate text to a maximum length.

    Args:
        text (str): Text to truncate.
        max_length (int): Maximum length.
        suffix (str): Suffix to append to truncated text.
        break_on_word (bool): Whether to break on word boundaries.

    Returns:
        str: Truncated text.
    """
    if not text or len(text) <= max_length:
        return text

    # Adjust max length to account for suffix
    max_length -= len(suffix)

    if max_length <= 0:
        return suffix

    # Truncate text
    truncated = text[:max_length]

    # Break on word boundary if requested
    if break_on_word:
        last_space = truncated.rfind(' ')
        if last_space > max_length // 2:  # Only break if we're not losing too much text
            truncated = truncated[:last_space]

    return truncated + suffix


def format_list(
    items: List[str],
    conjunction: str = "and",
    oxford_comma: bool = True
) -> str:
    """
    Format a list of items as a human-readable string.

    Args:
        items (List[str]): List of items to format.
        conjunction (str): Conjunction to use.
        oxford_comma (bool): Whether to use an Oxford (serial) comma.

    Returns:
        str: Formatted list.
    """
    if not items:
        return ""

    if len(items) == 1:
        return items[0]

    if len(items) == 2:
        return f"{items[0]} {conjunction} {items[1]}"

    if oxford_comma:
        return f"{', '.join(items[:-1])}, {conjunction} {items[-1]}"
    else:
        return f"{', '.join(items[:-1])} {conjunction} {items[-1]}"


def clean_text(text: str, strip: bool = True, lower: bool = False) -> str:
    """
    Clean text by removing extra whitespace and optionally converting to lowercase.

    Args:
        text (str): Text to clean.
        strip (bool): Whether to strip leading/trailing whitespace.
        lower (bool): Whether to convert to lowercase.

    Returns:
        str: Cleaned text.
    """
    if not text:
        return ""

    # Replace multiple whitespace with a single space
    cleaned = re.sub(r'\s+', ' ', text)

    if strip:
        cleaned = cleaned.strip()

    if lower:
        cleaned = cleaned.lower()

    return cleaned


def capitalise_first(text: str) -> str:
    """
    Capitalise the first letter of a string.

    Args:
        text (str): Text to capitalise.

    Returns:
        str: Text with first letter capitalised.
    """
    if not text:
        return ""

    return text[0].upper() + text[1:]


def capitalise_words(text: str, exceptions: Optional[List[str]] = None) -> str:
    """
    Capitalise the first letter of each word in a string.

    Args:
        text (str): Text to capitalise.
        exceptions (Optional[List[str]]): List of words to not capitalise.

    Returns:
        str: Text with words capitalised.
    """
    if not text:
        return ""

    exceptions = exceptions or ["a", "an", "the", "and", "but", "or", "for", "nor",
                                "on", "in", "at", "to", "by", "as", "of"]

    words = text.split()
    result = []

    for i, word in enumerate(words):
        if i == 0 or word.lower() not in exceptions:
            result.append(word.capitalize())
        else:
            result.append(word.lower())

    return " ".join(result)


def format_twitch_message(
    message: str,
    emotes: Optional[Dict[str, List[str]]] = None,
    badges: Optional[Dict[str, str]] = None,
    is_action: bool = False
) -> str:
    """
    Format a Twitch message with emotes and badges.

    Args:
        message (str): Message text.
        emotes (Optional[Dict[str, List[str]]]): Emotes in the message.
        badges (Optional[Dict[str, str]]): Badges the user has.
        is_action (bool): Whether the message is an action (/me command).

    Returns:
        str: Formatted message.
    """
    if not message:
        return ""

    # Format action messages
    if is_action:
        message = f"* {message}"

    # Add badge icons
    if badges:
        badge_icons = []
        for badge_name, badge_version in badges.items():
            # Insert badge emoji/icon based on badge type
            # This is a simplified example
            if badge_name == "broadcaster":
                badge_icons.append("📹")
            elif badge_name == "moderator":
                badge_icons.append("🔧")
            elif badge_name == "vip":
                badge_icons.append("💎")
            elif badge_name == "subscriber":
                badge_icons.append("✓")

        if badge_icons:
            message = f"{' '.join(badge_icons)} {message}"

    return message


def format_twitch_command(
    command: str,
    args: Optional[List[str]] = None,
    prefix: str = "!"
) -> str:
    """
    Format a Twitch command with arguments.

    Args:
        command (str): Command name.
        args (Optional[List[str]]): Command arguments.
        prefix (str): Command prefix.

    Returns:
        str: Formatted command.
    """
    if not command:
        return ""

    if args:
        return f"{prefix}{command} {' '.join(args)}"
    else:
        return f"{prefix}{command}"


def format_time_elapsed(
    elapsed_seconds: Union[int, float, timedelta],
    include_seconds: bool = True
) -> str:
    """
    Format elapsed time in a human-readable format.

    Args:
        elapsed_seconds (Union[int, float, timedelta]): Elapsed time in seconds or as timedelta.
        include_seconds (bool): Whether to include seconds in the output.

    Returns:
        str: Formatted elapsed time.
    """
    if isinstance(elapsed_seconds, timedelta):
        elapsed_seconds = elapsed_seconds.total_seconds()

    # Handle negative times
    if elapsed_seconds < 0:
        return "0 seconds"

    # Calculate time components
    days, remainder = divmod(int(elapsed_seconds), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Build the output
    parts = []

    if days > 0:
        parts.append(f"{days} {pluralise(days, 'day', include_count=False)}")

    if hours > 0 or days > 0:
        parts.append(
            f"{hours} {pluralise(hours, 'hour', include_count=False)}")

    if minutes > 0 or hours > 0 or days > 0:
        parts.append(
            f"{minutes} {pluralise(minutes, 'minute', include_count=False)}")

    if include_seconds and (seconds > 0 or not parts):
        parts.append(
            f"{seconds} {pluralise(seconds, 'second', include_count=False)}")

    if not parts:
        return "0 seconds"

    return format_list(parts)


def format_timestamp_for_humans(
    timestamp: Union[int, float, datetime],
    format_str: str = "%Y-%m-%d %H:%M:%S"
) -> str:
    """
    Format a timestamp as a human-readable date and time.

    Args:
        timestamp (Union[int, float, datetime]): Timestamp to format.
        format_str (str): Format string for datetime.strftime.

    Returns:
        str: Formatted timestamp.
    """
    if isinstance(timestamp, (int, float)):
        dt = datetime.fromtimestamp(timestamp)
    else:
        dt = timestamp

    return dt.strftime(format_str)


def format_bytes(
    size_bytes: Union[int, float],
    decimal_places: int = 2
) -> str:
    """
    Format bytes as a human-readable file size.

    Args:
        size_bytes (Union[int, float]): Size in bytes.
        decimal_places (int): Number of decimal places.

    Returns:
        str: Formatted file size.
    """
    if size_bytes < 0:
        return "0 bytes"

    # Define units
    units = ["bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    unit_index = 0

    # Find the appropriate unit
    while size_bytes >= 1024 and unit_index < len(units) - 1:
        size_bytes /= 1024
        unit_index += 1

    # Format the output
    if unit_index == 0:
        return f"{int(size_bytes)} {units[unit_index]}"
    else:
        return f"{size_bytes:.{decimal_places}f} {units[unit_index]}"


def strip_html_tags(text: str) -> str:
    """
    Strip HTML tags from text.

    Args:
        text (str): Text containing HTML tags.

    Returns:
        str: Text with HTML tags removed.
    """
    if not text:
        return ""

    # Simple HTML tag removal
    return re.sub(r'<[^>]+>', '', text)


def escape_markdown(text: str) -> str:
    """
    Escape Markdown special characters.

    Args:
        text (str): Text to escape.

    Returns:
        str: Text with Markdown characters escaped.
    """
    if not text:
        return ""

    # List of characters to escape
    markdown_chars = ['\\', '`', '*', '_',
                      '{', '}', '[', ']', '(', ')', '#', '+', '-', '.', '!']

    for char in markdown_chars:
        text = text.replace(char, '\\' + char)

    return text


def format_exception(exception: Exception) -> str:
    """
    Format an exception as a human-readable string.

    Args:
        exception (Exception): Exception to format.

    Returns:
        str: Formatted exception.
    """
    return f"{type(exception).__name__}: {str(exception)}"


def format_json(
    obj: Any,
    indent: int = 2,
    sort_keys: bool = True
) -> str:
    """
    Format an object as a JSON string.

    Args:
        obj (Any): Object to format.
        indent (int): Indentation level.
        sort_keys (bool): Whether to sort keys alphabetically.

    Returns:
        str: Formatted JSON string.
    """
    import json
    return json.dumps(obj, indent=indent, sort_keys=sort_keys, ensure_ascii=False)
