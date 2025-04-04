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
    if not isinstance(number, (int, float)):
        return str(number)
    try:
        decimal_value = Decimal(str(number))
        rounded_value = decimal_value.quantise(
            Decimal('0.1') ** decimals, rounding=ROUND_HALF_UP)
    except Exception:
        if decimals == 0:
            rounded_value = round(number)
        else:
            rounded_value = number
    if decimals == 0:
        formatted = f"{int(rounded_value):,}"
    else:
        formatted = f"{rounded_value:,}"
        if '.' in formatted:
            integer_part, decimal_part = formatted.split('.')
            decimal_part = decimal_part.ljust(decimals, '0')[:decimals]
            formatted = f"{integer_part}.{decimal_part}"
        else:
            formatted = f"{formatted}.{'0' * decimals}"
    if thousands_separator != "," and decimal_separator != ".":
        temp = "§§§"
        formatted = formatted.replace(".", temp)
        formatted = formatted.replace(",", thousands_separator)
        formatted = formatted.replace(temp, decimal_separator)
    else:
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
    if not singular:
        return "" if not include_count else str(count)
    if plural is None:
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
    break_on_word: bool = True
) -> str:
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    adjusted_max_length = max_length - len(suffix)
    if adjusted_max_length <= 0:
        return suffix
    truncated = text[:adjusted_max_length]
    if break_on_word:
        last_space = truncated.rfind(' ')
        if last_space > 0:
            truncated = truncated[:last_space]
    return truncated + suffix


def format_list(
    items: List[str],
    conjunction: str = "and",
    oxford_comma: bool = True
) -> str:
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
    if not text:
        return ""
    if strip:
        cleaned = re.sub(r'\s+', ' ', text).strip()
    else:
        leading_spaces = len(text) - len(text.lstrip())
        trailing_spaces = len(text) - len(text.rstrip())
        cleaned_middle = re.sub(r'\s+', ' ', text.strip())
        cleaned = ' ' * leading_spaces + cleaned_middle + ' ' * trailing_spaces
    if lower:
        cleaned = cleaned.lower()
    return cleaned


def capitalise_first(text: Optional[str]) -> str:
    if not text:
        return ""
    return text[0].upper() + text[1:]


def capitalise_words(text: Optional[str], exceptions: Optional[List[str]] = None) -> str:
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
    if not message:
        return ""
    if is_action:
        message = f"* {message}"
    if badges:
        badge_icons = []
        for badge_name, badge_version in badges.items():
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
    if args:
        return f"{prefix}{command} {' '.join(args)}"
    else:
        return f"{prefix}{command}"


def format_time_elapsed(
    elapsed_seconds: Union[int, float, timedelta],
    include_seconds: bool = True
) -> str:
    if isinstance(elapsed_seconds, timedelta):
        elapsed_seconds = elapsed_seconds.total_seconds()
    if elapsed_seconds < 0:
        return "0 seconds"
    days, remainder = divmod(int(elapsed_seconds), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
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
    return format_list(parts, oxford_comma=False)


def format_timestamp_for_humans(
    timestamp: Union[int, float, datetime],
    format_str: str = "%Y-%m-%d %H:%M:%S",
    utc: bool = True
) -> str:
    if timestamp is None:
        return ""
    if isinstance(timestamp, (int, float)):
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
    if size_bytes is None or size_bytes < 0:
        return "0 bytes"
    units = ["bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    unit_index = 0
    while size_bytes >= 1024 and unit_index < len(units) - 1:
        size_bytes /= 1024
        unit_index += 1
    if unit_index == 0:
        return f"{int(size_bytes)} {units[unit_index]}"
    else:
        return f"{size_bytes:.{decimal_places}f} {units[unit_index]}"


def strip_html_tags(text: Optional[str]) -> str:
    if not text:
        return ""
    return re.sub(r'<[^>]+>', '', text)


def escape_markdown(text: Optional[str]) -> str:
    if not text:
        return ""
    markdown_chars = ['\\', '`', '*', '_',
                      '{', '}', '[', ']', '(', ')', '#', '+', '-', '.', '!']
    for char in markdown_chars:
        text = text.replace(char, '\\' + char)
    return text


def format_exception(exception: Exception) -> str:
    if not exception:
        return "Unknown error"
    return f"{type(exception).__name__}: {str(exception)}"


def format_json(
    obj: Any,
    indent: int = 2,
    sort_keys: bool = True
) -> str:
    import json
    return json.dumps(obj, indent=indent, sort_keys=sort_keys, ensure_ascii=False)
