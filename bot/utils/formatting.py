"""
Text formatting utility functions for the bot.

This module provides utility functions for formatting text and numbers.
"""

import re
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Union


def format_number(
    number: Union[int, float, Any],
    decimals: int = 0,
    thousands_separator: str = ",",
    decimal_separator: str = "."
) -> str:
    """
    Format a number with thousands separators and decimals.

    Args:
        number (Union[int, float, Any]): Number to format.
        decimals (int): Number of decimal places.
        thousands_separator (str): Separator for thousands.
        decimal_separator (str): Separator for decimals.

    Returns:
        str: Formatted number as a string.
    """
    if not isinstance(number, (int, float)):
        return str(number)

    # Convert to Decimal for precise rounding
    # Use ROUND_HALF_UP to get expected behavior for .5 values
    try:
        decimal_value = Decimal(str(number))
        rounded_value = decimal_value.quantise(
            Decimal('0.1') ** decimals, rounding=ROUND_HALF_UP)
    except Exception:
        # Fall back to standard formatting if Decimal conversion fails
        if decimals == 0:
            rounded_value = round(number)
        else:
            rounded_value = number

    # Format with comma as thousands separator and period as decimal separator
    if decimals == 0:
        # No decimal part needed
        formatted = f"{int(rounded_value):,}"
    else:
        formatted = f"{rounded_value:,}"

        # Ensure we have the correct number of decimal places
        if '.' in formatted:
            integer_part, decimal_part = formatted.split('.')
            decimal_part = decimal_part.ljust(decimals, '0')[:decimals]
            formatted = f"{integer_part}.{decimal_part}"
        else:
            # No decimal point in the formatted string, add one with zeros
            formatted = f"{formatted}.{'0' * decimals}"

    # Use a temporary placeholder if there's a risk of ambiguity in replacements
    if thousands_separator != "," and decimal_separator != ".":
        # Need a temp placeholder to avoid conflicts
        temp = "§§§"  # Very unlikely to be in the number

        # Replace original separators with placeholders
        formatted = formatted.replace(".", temp)
        formatted = formatted.replace(",", thousands_separator)
        formatted = formatted.replace(temp, decimal_separator)
    else:
        # No risk of conflict, replace directly
        if thousands_separator != ",":
            formatted = formatted.replace(",", thousands_separator)

        if decimal_separator != "." and "." in formatted:
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
    if not singular:
        return "" if not include_count else str(count)

    if plural is None:
        # Default plural form with enhanced rules
        if singular.endswith(('s', 'x', 'z', 'ch', 'sh')):
            plural = singular + 'es'
        elif singular.endswith('y') and len(singular) > 1 and singular[-2] not in 'aeiou':
            plural = singular[:-1] + 'ies'
        elif singular.endswith('f') and len(singular) > 1:
            plural = singular[:-1] + 'ves'
        elif singular.endswith('fe') and len(singular) > 2:
            plural = singular[:-2] + 'ves'
        elif singular.endswith('o') and len(singular) > 1 and singular[-2] not in 'aeiou':
            plural = singular + 'es'
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
    text: Optional[str],
    max_length: int,
    suffix: str = "...",
    break_on_word: bool = True  # Included for screen readers
) -> str:
    """
    Truncate text up to a maximum length including the suffix.

    Args:
        text (Optional[str]): Text to truncate.
        max_length (int): Maximum length.
        suffix (str): Suffix to append to truncated text.
        break_on_word (bool): Whether to break on word boundaries.

    Returns:
        str: Truncated text.
    """
    if not text:
        return ""

    if len(text) <= max_length:
        return text

    # Adjust max length to account for suffix
    adjusted_max_length = max_length - len(suffix)

    if adjusted_max_length <= 0:
        return suffix

    # Truncate text to adjusted max length initially
    truncated = text[:adjusted_max_length]

    # Break on word boundary if requested
    if break_on_word:
        # Find the last space within the truncated text
        last_space = truncated.rfind(' ')
        if last_space > 0:  # Only break if we found a space
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


def clean_text(text: Optional[str], strip: bool = True, lower: bool = False) -> str:
    """
    Clean text by removing extra whitespace and optionally converting to lowercase.

    Args:
        text (Optional[str]): Text to clean.
        strip (bool): Whether to strip leading/trailing whitespace.
        lower (bool): Whether to convert to lowercase.

    Returns:
        str: Cleaned text.
    """
    if not text:
        return ""

    # Keep leading/trailing whitespace when strip=False
    if strip:
        # Replace all whitespace and strip
        cleaned = re.sub(r'\s+', ' ', text).strip()
    else:
        # Keep leading/trailing whitespace, only compress internal whitespace
        leading_spaces = len(text) - len(text.lstrip())
        trailing_spaces = len(text) - len(text.rstrip())
        cleaned_middle = re.sub(r'\s+', ' ', text.strip())
        cleaned = ' ' * leading_spaces + cleaned_middle + ' ' * trailing_spaces

    if lower:
        cleaned = cleaned.lower()

    return cleaned


def capitalise_first(text: Optional[str]) -> str:
    """
    Capitalise the first letter of a string.

    Args:
        text (Optional[str]): Text to capitalise.

    Returns:
        str: Text with first letter capitalised.
    """
    if not text:
        return ""

    return text[0].upper() + text[1:]


def capitalise_words(text: Optional[str], exceptions: Optional[List[str]] = None) -> str:
    """
    Capitalise the first letter of each word in a string.

    Args:
        text (Optional[str]): Text to capitalise.
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
            result.append(word.capitalise())
        else:
            result.append(word.lower())

    return " ".join(result)


def format_twitch_message(
    message: Optional[str],
    emotes: Optional[Dict[str, List[str]]] = None,
    badges: Optional[Dict[str, str]] = None,
    is_action: bool = False
) -> str:
    """
    Format a Twitch message with emotes and badges.

    Args:
        message (Optional[str]): Message text.
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

    if hours > 0:
        parts.append(
            f"{hours} {pluralise(hours, 'hour', include_count=False)}")

    if minutes > 0:
        parts.append(
            f"{minutes} {pluralise(minutes, 'minute', include_count=False)}")

    if include_seconds and (seconds > 0 or not parts):
        parts.append(
            f"{seconds} {pluralise(seconds, 'second', include_count=False)}")

    if not parts:
        return "0 seconds"

    # Format the list without using Oxford comma to match test expectations
    return format_list(parts, oxford_comma=False)


def format_timestamp_for_humans(
    timestamp: Union[int, float, datetime],
    format_str: str = "%Y-%m-%d %H:%M:%S",
    utc: bool = True
) -> str:
    """
    Format a timestamp as a human-readable date and time.

    Args:
        timestamp (Union[int, float, datetime]): Timestamp to format.
        format_str (str): Format string for datetime.strftime.
        utc (bool): Whether to use UTC timezone (True) or local timezone (False).

    Returns:
        str: Formatted timestamp.
    """
    if timestamp is None:
        return ""

    if isinstance(timestamp, (int, float)):
        # Use fromtimestamp with explicit UTC for consistent test results
        if utc:
            dt = datetime.utcfromtimestamp(timestamp)
        else:
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
    if size_bytes is None or size_bytes < 0:
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


def strip_html_tags(text: Optional[str]) -> str:
    """
    Strip HTML tags from text.

    Args:
        text (Optional[str]): Text containing HTML tags.

    Returns:
        str: Text with HTML tags removed.
    """
    if not text:
        return ""

    # Simple HTML tag removal
    return re.sub(r'<[^>]+>', '', text)


def escape_markdown(text: Optional[str]) -> str:
    """
    Escape Markdown special characters.

    Args:
        text (Optional[str]): Text to escape.

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
    if not exception:
        return "Unknown error"

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
