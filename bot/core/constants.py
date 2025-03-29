"""
Global constants for the bot.

This module defines global constants used throughout the bot.
"""

import os
from pathlib import Path

# Project directories
PROJECT_ROOT = Path(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"
CONFIG_DIR = PROJECT_ROOT / "config"

# Environment file
DEFAULT_ENV_FILE = PROJECT_ROOT / ".env"

# Default configuration values
DEFAULT_CONFIG = {
    "bot_nick": "BetsyBot",
    "bot_prefix": "!",
    "channel": "",
    "log_level": "INFO",
    "db_enabled": "false",
    "obs_enabled": "false",
    "discord_enabled": "false",
    "db_path": str(DATA_DIR / "bot.db"),
}

# Database constants
DB_SCHEMA_FILE = PROJECT_ROOT / "bot" / "db" / "schema.sql"

# Platform constants
TWITCH_API_BASE_URL = "https://api.twitch.tv/helix"
TWITCH_AUTH_URL = "https://id.twitch.tv/oauth2/token"

# Feature flags
FEATURES = [
    "points",
    "shop",
    "inventory",
    "duel",
    "domt",
    "obs_actions",
    "easter_eggs",
    "dungeon",
    "betsy_vault",
    "shield_mode",
    "todo",
    "chat_log",
    "ai",
]

# User ranks
USER_RANKS = [
    "viewer",
    "vip",
    "subscriber",
    "moderator",
    "broadcaster",
    "bot_admin",
]

# Command cooldown defaults (in seconds)
DEFAULT_COMMAND_COOLDOWN = 3
DEFAULT_GLOBAL_COOLDOWN = 1

# Points constants
POINTS_PER_MESSAGE = 10
POINTS_PER_MINUTE = 1
POINTS_PER_BIT = 1
# TODO POINTS_PER_TWITCH_CHANNEL_REWARD
