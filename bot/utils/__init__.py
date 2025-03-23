"""
Utility functions for the Twitch bot.
"""

from bot.utils.cooldown import Cooldown, CooldownManager, BucketType
from bot.utils.formatting import (
    format_points, format_username, format_command,
    format_duration, format_item_name, pluralise,
    format_list, truncate, normalise_name, format_chat_message
)
from bot.utils.parsing import (
    parse_command, parse_args, extract_user_and_amount,
    parse_key_value_pairs, extract_targets, safe_int_conversion,
    safe_float_conversion, safe_bool_conversion, parse_duration,
    parse_item_name, parse_bits_amount, extract_command_with_targets,
    is_valid_target_for_self, fuzzy_match_item
)
from bot.utils.permissions import UserRole, Permission, PermissionManager
from bot.utils.queue import (
    PriorityMessageQueue, CommandQueue, DuelQueue, TaskQueue
)
from bot.utils.random_utils import (
    random_choice, random_choices, random_sample, random_int,
    random_float, random_string, shuffle_list, weighted_choice,
    random_bool, random_element_from_dict, calculate_random_odds,
    generate_seed, set_seed
)
from bot.utils.sanitisation import (
    sanitise_input, sanitise_username, sanitise_command_args,
    sanitise_for_db, strip_twitch_emotes, sanitise_html,
    remove_non_alphanumeric, clean_numeric_string
)
from bot.utils.security import (
    generate_secure_token, hash_password, verify_password,
    sanitise_path, is_valid_oauth_token, mask_sensitive_data,
    is_safe_string, rate_limit_key
)
from bot.utils.throttling import (
    TokenBucket, RateLimiter, MessageQueue, PerUserRateLimiter,
    CommandThrottler
)
from bot.utils.time_utils import (
    get_current_timestamp, get_current_datetime, get_formatted_datetime,
    parse_datetime, datetime_to_timestamp, timestamp_to_datetime,
    get_time_difference, get_time_difference_seconds, is_expired,
    get_random_delay, sleep, with_timeout, get_time_until,
    format_timedelta, get_cooldown_end_time, format_cooldown_remaining
)
from bot.utils.validation import (
    validate_boolean, validate_port, validate_username,
    validate_command, validate_integer, validate_contains_emoji,
    validate_contains_only_numbers, validate_points, validate_item_name,
    validate_user_input
)