"""
Custom exceptions for the Twitch bot.
"""

class BotError(Exception):
    """Base exception for all bot-related errors."""
    pass

class ConfigError(BotError):
    """Exception raised for configuration errors."""
    pass

class DatabaseError(BotError):
    """Exception raised for database errors."""
    pass

class TwitchError(BotError):
    """Exception raised for Twitch API errors."""
    pass

class OBSError(BotError):
    """Exception raised for OBS WebSocket errors."""
    pass

class PermissionError(BotError):
    """Exception raised for permission-related errors."""
    pass

class CommandError(BotError):
    """Exception raised for command-related errors."""
    pass

class ValidationError(BotError):
    """Exception raised for validation errors."""
    pass

class ThrottlingError(BotError):
    """Exception raised for throttling-related errors."""
    pass

class CooldownError(BotError):
    """Exception raised when a command is on cooldown."""
    pass

class FeatureDisabledError(BotError):
    """Exception raised when a feature is disabled."""
    pass

class ItemNotFoundError(BotError):
    """Exception raised when an item is not found."""
    pass

class InsufficientPointsError(BotError):
    """Exception raised when a user has insufficient points."""
    pass

class InvalidArgumentError(BotError):
    """Exception raised when invalid arguments are provided."""
    pass

class DuelError(BotError):
    """Exception raised for duel-related errors."""
    pass

class InventoryError(BotError):
    """Exception raised for inventory-related errors."""
    pass

class DOMTError(BotError):
    """Exception raised for Deck of Many Things related errors."""
    pass