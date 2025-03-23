"""
Cooldown utility functions for the Twitch bot.
"""
import time
import logging
import threading
from enum import Enum, auto
from typing import Dict, Any, Optional, Union, Callable, Tuple

from bot.core.errors import CooldownError
from bot.utils.time_utils import get_current_timestamp, format_duration

# Set up logger
logger = logging.getLogger(__name__)

class BucketType(Enum):
    """Enum representing cooldown bucket types."""
    DEFAULT = auto()    # Global cooldown
    USER = auto()       # Per-user cooldown
    CHANNEL = auto()    # Per-channel cooldown
    USER_CHANNEL = auto()  # Per-user-per-channel cooldown

class Cooldown:
    """Class for managing command cooldowns."""
    
    def __init__(self, rate: int, per: float):
        """
        Initialise cooldown.
        
        Args:
            rate: Number of uses allowed in time period
            per: Time period in seconds
        """
        self.rate = rate
        self.per = per
        self.reset()
    
    def reset(self) -> None:
        """Reset cooldown state."""
        self._tokens = self.rate
        self._last = 0.0
    
    def get_tokens(self) -> int:
        """
        Get current number of tokens.
        
        Returns:
            Current token count
        """
        return self._tokens
    
    def update_rate_limit(self) -> Optional[float]:
        """
        Update rate limit and return remaining cooldown if token consumed.
        
        Returns:
            Cooldown remaining in seconds or None if not rate limited
        """
        current = get_current_timestamp()
        tokens = self._tokens
        
        # Update token count based on time passed
        if tokens < self.rate:
            time_passed = current - self._last
            tokens_to_add = int(time_passed // self.per)
            
            if tokens_to_add > 0:
                tokens = min(self.rate, tokens + tokens_to_add)
        
        # Check if we can consume a token
        if tokens == 0:
            self._last = current
            return self.per - ((current - self._last) % self.per)
        
        # Consume a token
        self._tokens = tokens - 1
        self._last = current
        return None
    
    def get_retry_after(self) -> float:
        """
        Get time in seconds until next token is available.
        
        Returns:
            Time in seconds until next token
        """
        current = get_current_timestamp()
        
        if self._tokens == 0:
            return self.per - ((current - self._last) % self.per)
        
        return 0.0

class CooldownManager:
    """Manager for command cooldowns."""
    
    def __init__(self):
        """Initialise cooldown manager."""
        self.cooldowns: Dict[str, Dict[str, Cooldown]] = {}
        self.lock = threading.RLock()
    
    def _get_bucket_key(self, command: str, 
                       user_id: Optional[str] = None,
                       channel_id: Optional[str] = None,
                       bucket_type: BucketType = BucketType.DEFAULT) -> str:
        """
        Get key for cooldown bucket.
        
        Args:
            command: Command name
            user_id: User ID (required for USER and USER_CHANNEL bucket types)
            channel_id: Channel ID (required for CHANNEL and USER_CHANNEL bucket types)
            bucket_type: Bucket type
        
        Returns:
            Bucket key
        """
        if bucket_type == BucketType.DEFAULT:
            return "global"
        elif bucket_type == BucketType.USER:
            if not user_id:
                raise ValueError("User ID is required for USER bucket type")
            return f"user:{user_id}"
        elif bucket_type == BucketType.CHANNEL:
            if not channel_id:
                raise ValueError("Channel ID is required for CHANNEL bucket type")
            return f"channel:{channel_id}"
        elif bucket_type == BucketType.USER_CHANNEL:
            if not user_id or not channel_id:
                raise ValueError("User ID and Channel ID are required for USER_CHANNEL bucket type")
            return f"user:{user_id}:channel:{channel_id}"
        else:
            raise ValueError(f"Unknown bucket type: {bucket_type}")
    
    def get_bucket(self, command: str, bucket_key: str) -> Optional[Cooldown]:
        """
        Get cooldown bucket.
        
        Args:
            command: Command name
            bucket_key: Bucket key
        
        Returns:
            Cooldown bucket or None if not found
        """
        with self.lock:
            return self.cooldowns.get(command, {}).get(bucket_key)
    
    def add_bucket(self, command: str, bucket_key: str, rate: int, per: float) -> Cooldown:
        """
        Add cooldown bucket.
        
        Args:
            command: Command name
            bucket_key: Bucket key
            rate: Number of uses allowed in time period
            per: Time period in seconds
        
        Returns:
            Created cooldown bucket
        """
        with self.lock:
            if command not in self.cooldowns:
                self.cooldowns[command] = {}
            
            bucket = Cooldown(rate, per)
            self.cooldowns[command][bucket_key] = bucket
            return bucket
    
    def get_or_create_bucket(self, command: str, bucket_key: str, rate: int, per: float) -> Cooldown:
        """
        Get existing bucket or create new one.
        
        Args:
            command: Command name
            bucket_key: Bucket key
            rate: Number of uses allowed in time period
            per: Time period in seconds
        
        Returns:
            Cooldown bucket
        """
        with self.lock:
            bucket = self.get_bucket(command, bucket_key)
            if bucket is None:
                bucket = self.add_bucket(command, bucket_key, rate, per)
            return bucket
    
    def reset_bucket(self, command: str, bucket_key: str) -> bool:
        """
        Reset cooldown bucket.
        
        Args:
            command: Command name
            bucket_key: Bucket key
        
        Returns:
            True if bucket was reset, False if not found
        """
        with self.lock:
            bucket = self.get_bucket(command, bucket_key)
            if bucket is not None:
                bucket.reset()
                return True
            return False
    
    def remove_bucket(self, command: str, bucket_key: str) -> bool:
        """
        Remove cooldown bucket.
        
        Args:
            command: Command name
            bucket_key: Bucket key
        
        Returns:
            True if bucket was removed, False if not found
        """
        with self.lock:
            if command in self.cooldowns and bucket_key in self.cooldowns[command]:
                del self.cooldowns[command][bucket_key]
                
                # Clean up empty command dict
                if not self.cooldowns[command]:
                    del self.cooldowns[command]
                
                return True
            return False
    
    def check_cooldown(self, command: str, 
                     rate: int, 
                     per: float,
                     user_id: Optional[str] = None,
                     channel_id: Optional[str] = None,
                     bucket_type: BucketType = BucketType.DEFAULT) -> None:
        """
        Check if command is on cooldown, raising an error if it is.
        
        Args:
            command: Command name
            rate: Number of uses allowed in time period
            per: Time period in seconds
            user_id: User ID
            channel_id: Channel ID
            bucket_type: Bucket type
        
        Raises:
            CooldownError: If command is on cooldown
        """
        with self.lock:
            bucket_key = self._get_bucket_key(command, user_id, channel_id, bucket_type)
            bucket = self.get_or_create_bucket(command, bucket_key, rate, per)
            
            retry_after = bucket.update_rate_limit()
            if retry_after is not None:
                if retry_after < 0.001:  # Prevent negative cooldowns
                    retry_after = 0.001
                
                remaining = format_duration(retry_after)
                raise CooldownError(
                    f"Command '{command}' is on cooldown. Try again in {remaining}.", 
                    remaining=retry_after
                )
    
    def reset_cooldown(self, command: str, 
                     user_id: Optional[str] = None,
                     channel_id: Optional[str] = None,
                     bucket_type: BucketType = BucketType.DEFAULT) -> bool:
        """
        Reset cooldown for a command.
        
        Args:
            command: Command name
            user_id: User ID
            channel_id: Channel ID
            bucket_type: Bucket type
        
        Returns:
            True if cooldown was reset, False if not found
        """
        with self.lock:
            bucket_key = self._get_bucket_key(command, user_id, channel_id, bucket_type)
            return self.reset_bucket(command, bucket_key)
    
    def get_cooldown_remaining(self, command: str, 
                             rate: int, 
                             per: float,
                             user_id: Optional[str] = None,
                             channel_id: Optional[str] = None,
                             bucket_type: BucketType = BucketType.DEFAULT) -> float:
        """
        Get remaining cooldown time for a command.
        
        Args:
            command: Command name
            rate: Number of uses allowed in time period
            per: Time period in seconds
            user_id: User ID
            channel_id: Channel ID
            bucket_type: Bucket type
        
        Returns:
            Remaining cooldown time in seconds (0 if not on cooldown)
        """
        with self.lock:
            bucket_key = self._get_bucket_key(command, user_id, channel_id, bucket_type)
            bucket = self.get_bucket(command, bucket_key)
            
            if bucket is None:
                return 0.0
            
            return bucket.get_retry_after()