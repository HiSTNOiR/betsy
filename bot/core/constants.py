"""
Constants and enums for the Twitch bot.
"""
from enum import Enum, auto
from typing import Dict, List, Set, Tuple, Any

# Bot version
BOT_VERSION = "0.9.0"

# Command cooldowns (in seconds)
DEFAULT_COMMAND_COOLDOWN = 3
ADMIN_COMMAND_COOLDOWN = 1
POINTS_COMMAND_COOLDOWN = 5
SHOP_COMMAND_COOLDOWN = 5
DUEL_COMMAND_COOLDOWN = 30
DOMT_COMMAND_COOLDOWN = 60

# Points
DEFAULT_MESSAGE_POINTS = 1
DEFAULT_ACTIVE_VIEWER_POINTS = 10
BITS_TO_POINTS_RATIO = 1  # 1 bit = 1 point
POINTS_GIFT_MULTIPLIER = 1.1  # 10% bonus for gifting points

# Duels
DUEL_MIN_POINTS = 10
DUEL_MAX_POINTS = 100000
DUEL_TIMEOUT_SECONDS = 60
UNDERDOG_WIN_CHANCE = 5  # 5% chance
DEFAULT_DURABILITY_LOSS = 1
DUEL_ENVIRONMENT_COUNT = 7

# Shop
ITEM_LEVEL_MAX = 20
DURABILITY_MAX = 10
DURABILITY_MIN = 0

# Deck of Many Things
DOMT_COST_BITS = 1111
DOMT_CARD_COUNT = 21

# Command prefixes
DEFAULT_COMMAND_PREFIX = "!"

# Database
DB_VERSION = 1
DB_BACKUP_INTERVAL_DAYS = 1
DB_RETRY_ATTEMPTS = 3
DB_RETRY_DELAY_SECONDS = 1

# Chat throttling
MESSAGE_QUEUE_SIZE = 100
THROTTLE_MESSAGES_PER_SECOND = 0.7  # Max rate of messages per second
THROTTLE_BURST_SIZE = 3  # Allow burst of this many messages

# OBS
OBS_RECONNECT_ATTEMPTS = 3
OBS_RECONNECT_DELAY_SECONDS = 5

# Easter eggs
EMOTE_COMBO_MIN_USERS = 3
EMOTE_COMBO_REWARD = 100

# Logging
LOG_RETENTION_DAYS = 14

# Cache settings
CACHE_TTL_SECONDS = 300  # 5 minutes
USER_CACHE_SIZE = 1000
COMMAND_CACHE_SIZE = 100
ITEM_CACHE_SIZE = 500

# Paths
DEFAULT_DB_PATH = "data/bot.db"
DEFAULT_LOG_PATH = "logs"
DEFAULT_CONFIG_PATH = ".env"

class MessagePriority(Enum):
    """Enum representing message priority for the output queue."""
    LOW = 0       # Normal responses
    MEDIUM = 1    # Important responses
    HIGH = 2      # Critical responses
    SYSTEM = 3    # System messages (errors, etc.)

class DuelState(Enum):
    """Enum representing the state of a duel."""
    INITIATED = auto()
    ACCEPTED = auto()
    REJECTED = auto()
    TIMED_OUT = auto()
    COMPLETED = auto()
    DRAW = auto()

class DuelEnvironment(Enum):
    """Enum representing duel environments."""
    DESERT = "desert"
    JUNGLE = "jungle"
    SNOW = "snow"
    URBAN = "urban"
    AQUATIC = "aquatic"
    UNDERGROUND = "underground"
    VOLCANIC = "volcanic"

class EventType(Enum):
    """Enum representing event types."""
    BITS = "bits"
    REWARD = "reward"
    COMMAND = "command"
    DISCORD = "discord"
    EMOTE_COMBO = "emote_combo"
    SHIELD_MODE = "shield_mode"
    SUBSCRIPTION = "subscription"
    FOLLOW = "follow"
    RAID = "raid"

class ItemType(Enum):
    """Enum representing item types."""
    WEAPON = "weapon"
    ARMOUR = "armour"
    WEAPON_MOD = "weapon_mod"
    ARMOUR_MOD = "armour_mod"
    TOY = "toy"
    CARD = "card"

class EnvironmentEffect(Enum):
    """Enum representing environment effects."""
    BOON = "boon"
    BUST = "bust"

# Command access levels
COMMAND_ACCESS_LEVELS = {
    "admin": {"broadcaster", "bot_admin"},
    "mod": {"broadcaster", "bot_admin", "moderator"},
    "elevated": {"broadcaster", "bot_admin", "moderator", "vip"},
    "sub": {"broadcaster", "bot_admin", "moderator", "vip", "subscriber"},
    "all": {"broadcaster", "bot_admin", "moderator", "vip", "subscriber", "viewer"}
}

# Error messages
ERROR_MESSAGES = {
    "permission_denied": "Sorry @{user}, you don't have permission to use this command.",
    "cooldown": "Slow down @{user}! This command is on cooldown for {time}.",
    "insufficient_points": "Sorry @{user}, you don't have enough XP. You need {amount} XP.",
    "invalid_args": "Sorry @{user}, that's not the right way to use this command. Try: {usage}",
    "item_not_found": "Sorry @{user}, I couldn't find '{item}'.",
    "user_not_found": "Sorry @{user}, I couldn't find user '{target}'.",
    "self_target": "Nice try @{user}, but you can't target yourself with this command!",
    "duel_already_active": "Sorry @{user}, you already have an active duel challenge.",
    "invalid_amount": "Sorry @{user}, that's not a valid amount. Please use a number between {min} and {max}.",
    "db_error": "Oops! Something went wrong with my database. Please try again later.",
    "already_owned": "Sorry @{user}, you already own {item}.",
    "generic_error": "Oops! Something went wrong. Please try again later."
}

# Success messages
SUCCESS_MESSAGES = {
    "points_check": "@{user}, you have {points} XP.",
    "points_give": "@{user}, you gave {amount} XP to @{target}. Aren't you generous!",
    "points_received": "@{user}, you received {amount} XP from @{source}!",
    "item_purchase": "@{user}, you've purchased {item} for {cost} XP. Enjoy!",
    "duel_challenge": "@{challenger} has challenged @{target} to a duel for {amount} XP! Type !accept to battle or wait {timeout} seconds to decline.",
    "duel_accept": "The duel between @{challenger} and @{target} has begun! Place your bets!",
    "duel_win": "@{winner} has defeated @{loser} in a duel and claimed {amount} XP!",
    "duel_draw": "The duel between @{challenger} and @{target} ended in a draw! The pot of {amount} XP remains for the next duel.",
    "duel_reject": "@{target} has declined @{challenger}'s duel challenge.",
    "duel_timeout": "@{target} didn't respond to @{challenger}'s duel challenge in time.",
    "upgrade_success": "@{user}, you've upgraded to {item}. Congrats!"
}

# Help messages
HELP_MESSAGES = {
    "points": "Check your XP with !points or !xp",
    "give": "Give XP to another user with !give <username> <amount>",
    "shop": "Check out what's available in the shop with !shop",
    "buy": "Buy items with !buy <item_name>",
    "upgrade": "Upgrade your gear with !upgrade <weapon|armour>",
    "modify": "Apply mods to your gear with !modify <mod_name>",
    "duel": "Challenge another user to a duel with !duel <username> <amount>",
    "inventory": "Check your inventory with !inventory",
    "gear": "Check your current gear with !gear",
    "toys": "Check your toys with !toys",
    "cards": "Check your Deck of Many Things cards with !cards",
    "commands": "View available commands with !commands",
    "help": "Get help for a specific command with !help <command>"
}

# Item categories
ITEM_CATEGORIES = {
    "armour": {
        "name": "Armour",
        "description": "Protective gear to reduce damage in duels",
        "db_table": "armour"
    },
    "weapon": {
        "name": "Weapons",
        "description": "Offensive equipment to increase damage in duels",
        "db_table": "weapons"
    },
    "armour_mod": {
        "name": "Armour Modifications",
        "description": "Modifications to improve your armour",
        "db_table": "armour_mods"
    },
    "weapon_mod": {
        "name": "Weapon Modifications",
        "description": "Modifications to improve your weapon",
        "db_table": "weapon_mods"
    },
    "toy": {
        "name": "Toys",
        "description": "Fun items to interact with other users",
        "db_table": "toys"
    },
    "card": {
        "name": "Cards",
        "description": "Cards from the Deck of Many Things",
        "db_table": "user_cards"
    }
}