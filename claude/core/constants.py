import os
from pathlib import Path

PROJECT_ROOT = Path(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"
CONFIG_DIR = PROJECT_ROOT / "config"
DEFAULT_ENV_FILE = PROJECT_ROOT / ".env"
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
DB_SCHEMA_FILE = PROJECT_ROOT / "bot" / "db" / "schema.sql"
TWITCH_API_BASE_URL = "https://api.twitch.tv/helix"
TWITCH_AUTH_URL = "https://id.twitch.tv/oauth2/token"
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
USER_RANKS = [
    "viewer",
    "vip",
    "subscriber",
    "moderator",
    "broadcaster",
    "bot_admin",
]
DEFAULT_COMMAND_COOLDOWN = 3
DEFAULT_GLOBAL_COOLDOWN = 1
POINTS_PER_MESSAGE = 10
POINTS_PER_MINUTE = 1
POINTS_PER_BIT = 1
# TODO POINTS_PER_TWITCH_CHANNEL_REWARD
