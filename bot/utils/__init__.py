"""
Utility package for the bot.

This package provides utility functions used throughout the application.
"""

# Time utilities
from bot.utils.time import (
    get_utc_now,
    to_utc,
    format_datetime,
    parse_datetime,
    format_duration,
    parse_duration,
    time_until,
    time_since,
    format_relative_time,
    is_same_day,
    add_time,
    format_timestamp,
    get_date_range,
)

# Security utilities
from bot.utils.security import (
    generate_random_string,
    generate_token,
    hash_password,
    verify_password,
    generate_hmac,
    verify_hmac,
    sanitise_input,
    sanitise_filename,
    sanitise_path,
    is_safe_url,
    is_valid_twitch_username,
    is_safe_command,
    validate_twitch_token,
    encrypt_string,
    decrypt_string,
)

# Formatting utilities
from bot.utils.formatting import (
    format_number,
    format_currency,
    pluralise,
    truncate,
    format_list,
    clean_text,
    capitalise_first,
    capitalise_words,
    format_twitch_message,
    format_twitch_command,
    format_time_elapsed,
    format_timestamp_for_humans,
    format_bytes,
    strip_html_tags,
    escape_markdown,
    format_exception,
    format_json,
)

__all__ = [
    # Time utilities
    "get_utc_now",
    "to_utc",
    "format_datetime",
    "parse_datetime",
    "format_duration",
    "parse_duration",
    "time_until",
    "time_since",
    "format_relative_time",
    "is_same_day",
    "add_time",
    "format_timestamp",
    "get_date_range",

    # Security utilities
    "generate_random_string",
    "generate_token",
    "hash_password",
    "verify_password",
    "generate_hmac",
    "verify_hmac",
    "sanitise_input",
    "sanitise_filename",
    "sanitise_path",
    "is_safe_url",
    "is_valid_twitch_username",
    "is_safe_command",
    "validate_twitch_token",
    "encrypt_string",
    "decrypt_string",

    # Formatting utilities
    "format_number",
    "format_currency",
    "pluralise",
    "truncate",
    "format_list",
    "clean_text",
    "capitalise_first",
    "capitalise_words",
    "format_twitch_message",
    "format_twitch_command",
    "format_time_elapsed",
    "format_timestamp_for_humans",
    "format_bytes",
    "strip_html_tags",
    "escape_markdown",
    "format_exception",
    "format_json",
]
