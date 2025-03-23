"""
Throttling utility functions for the Twitch bot.
"""
import time
import logging
import threading
from queue import PriorityQueue, Empty
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from bot.core.constants import MessagePriority
from bot.core.errors import ThrottlingError

# Set up logger
logger = logging.getLogger(__name__)

@dataclass(order=True)
class PrioritisedItem:
    """Class for items in priority queue with comparison based on priority."""
    priority: int
    item: Any = field(compare=False)
    timestamp: float = field(default_factory=time.time)

class TokenBucket:
    """Token bucket algorithm for rate limiting."""
    
    def __init__(self, rate: float, max_tokens: int):
        """
        Initialise token bucket.
        
        Args:
            rate: Token refill rate (tokens per second)
            max_tokens: Maximum number of tokens
        """
        self.rate = rate
        self.max_tokens = max_tokens
        self.tokens = max_tokens
        self.last_update = time.time()
        self.lock = threading.RLock()
    
    def _update_tokens(self) -> None:
        """Update token count based on elapsed time."""
        now = time.time()
        elapsed = now - self.last_update
        new_tokens = elapsed * self.rate
        
        with self.lock:
            self.tokens = min(self.max_tokens, self.tokens + new_tokens)
            self.last_update = now
    
    def try_consume(self, tokens: int = 1) -> bool:
        """
        Try to consume tokens.
        
        Args:
            tokens: Number of tokens to consume (default: 1)
        
        Returns:
            True if tokens consumed, False otherwise
        """
        self._update_tokens()
        
        with self.lock:
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False
    
    def get_wait_time(self, tokens: int = 1) -> float:
        """
        Get estimated wait time until tokens are available.
        
        Args:
            tokens: Number of tokens needed (default: 1)
        
        Returns:
            Estimated wait time in seconds
        """
        self._update_tokens()
        
        with self.lock:
            if self.tokens >= tokens:
                return 0.0
            
            needed_tokens = tokens - self.tokens
            return needed_tokens / self.rate

class RateLimiter:
    """Rate limiter for bot actions."""
    
    def __init__(self, rate: float, burst: int):
        """
        Initialise rate limiter.
        
        Args:
            rate: Maximum rate (actions per second)
            burst: Maximum burst size
        """
        self.bucket = TokenBucket(rate, burst)
    
    def check_limit(self, tokens: int = 1) -> None:
        """
        Check if action is rate limited, raising exception if it is.
        
        Args:
            tokens: Number of tokens for action (default: 1)
        
        Raises:
            ThrottlingError: If action would exceed rate limit
        """
        if not self.bucket.try_consume(tokens):
            wait_time = self.bucket.get_wait_time(tokens)
            raise ThrottlingError(f"Rate limited, try again in {wait_time:.2f} seconds")
    
    def wait_if_needed(self, tokens: int = 1) -> float:
        """
        Wait if needed to respect rate limit.
        
        Args:
            tokens: Number of tokens for action (default: 1)
        
        Returns:
            Time waited in seconds
        """
        wait_time = self.bucket.get_wait_time(tokens)
        
        if wait_time > 0:
            time.sleep(wait_time)
            self.bucket.try_consume(tokens)
            return wait_time
        
        self.bucket.try_consume(tokens)
        return 0.0

class MessageQueue:
    """Priority-based message queue with rate limiting."""
    
    def __init__(self, rate: float = 0.7, burst: int = 3, max_queue_size: int = 100):
        """
        Initialise message queue.
        
        Args:
            rate: Maximum message rate (messages per second)
            burst: Maximum burst size
            max_queue_size: Maximum queue size
        """
        self.queue = PriorityQueue(maxsize=max_queue_size)
        self.rate_limiter = RateLimiter(rate, burst)
        self.running = False
        self.thread = None
        self.lock = threading.RLock()
    
    def start(self, message_handler: Callable[[str, MessagePriority], None]) -> None:
        """
        Start message queue processing thread.
        
        Args:
            message_handler: Function to handle messages
        """
        with self.lock:
            if self.running:
                return
            
            self.running = True
            self.message_handler = message_handler
            self.thread = threading.Thread(target=self._process_queue, daemon=True)
            self.thread.start()
            logger.info("Message queue started")
    
    def stop(self) -> None:
        """Stop message queue processing thread."""
        with self.lock:
            if not self.running:
                return
            
            self.running = False
            if self.thread and self.thread.is_alive():
                self.thread.join(timeout=1.0)
            logger.info("Message queue stopped")
    
    def add_message(self, message: str, priority: MessagePriority = MessagePriority.LOW) -> bool:
        """
        Add message to queue.
        
        Args:
            message: Message to add
            priority: Message priority (default: LOW)
        
        Returns:
            True if message added, False if queue full
        """
        try:
            # Lower number = higher priority
            item = PrioritisedItem(priority=priority.value, item=message)
            self.queue.put_nowait(item)
            return True
        except Exception as e:
            logger.warning(f"Failed to add message to queue: {e}")
            return False
    
    def _process_queue(self) -> None:
        """Process messages from queue respecting rate limits."""
        while self.running:
            try:
                # Get message from queue with timeout to allow checking running flag
                item = self.queue.get(timeout=0.1)
                
                # Wait if needed to respect rate limit
                self.rate_limiter.wait_if_needed()
                
                # Send message
                try:
                    self.message_handler(item.item, MessagePriority(item.priority))
                except Exception as e:
                    logger.error(f"Error handling message: {e}")
                
                # Mark task as done
                self.queue.task_done()
            
            except Empty:
                # Queue is empty, just continue
                continue
            except Exception as e:
                logger.error(f"Error processing message queue: {e}")
                # Sleep briefly to avoid tight loop on persistent error
                time.sleep(0.1)

class PerUserRateLimiter:
    """Rate limiter for actions on a per-user basis."""
    
    def __init__(self, rate: float, burst: int, cleanup_interval: int = 300):
        """
        Initialise per-user rate limiter.
        
        Args:
            rate: Maximum rate (actions per second)
            burst: Maximum burst size
            cleanup_interval: Interval to clean up inactive users (seconds)
        """
        self.rate = rate
        self.burst = burst
        self.user_buckets: Dict[str, TokenBucket] = {}
        self.lock = threading.RLock()
        self.cleanup_interval = cleanup_interval
        self.last_cleanup = time.time()
    
    def _cleanup_inactive(self) -> None:
        """Clean up inactive user buckets."""
        now = time.time()
        if now - self.last_cleanup < self.cleanup_interval:
            return
        
        with self.lock:
            # Remove buckets that are full (inactive)
            to_remove = []
            for user_id, bucket in self.user_buckets.items():
                bucket._update_tokens()
                if bucket.tokens >= bucket.max_tokens:
                    to_remove.append(user_id)
            
            for user_id in to_remove:
                del self.user_buckets[user_id]
            
            self.last_cleanup = now
    
    def check_limit(self, user_id: str, tokens: int = 1) -> None:
        """
        Check if action for user is rate limited, raising exception if it is.
        
        Args:
            user_id: User ID
            tokens: Number of tokens for action (default: 1)
        
        Raises:
            ThrottlingError: If action would exceed rate limit
        """
        self._cleanup_inactive()
        
        with self.lock:
            if user_id not in self.user_buckets:
                self.user_buckets[user_id] = TokenBucket(self.rate, self.burst)
            
            bucket = self.user_buckets[user_id]
            
            if not bucket.try_consume(tokens):
                wait_time = bucket.get_wait_time(tokens)
                raise ThrottlingError(f"Rate limited for user {user_id}, try again in {wait_time:.2f} seconds")
    
    def wait_if_needed(self, user_id: str, tokens: int = 1) -> float:
        """
        Wait if needed to respect rate limit for user.
        
        Args:
            user_id: User ID
            tokens: Number of tokens for action (default: 1)
        
        Returns:
            Time waited in seconds
        """
        self._cleanup_inactive()
        
        with self.lock:
            if user_id not in self.user_buckets:
                self.user_buckets[user_id] = TokenBucket(self.rate, self.burst)
            
            bucket = self.user_buckets[user_id]
            
            wait_time = bucket.get_wait_time(tokens)
            
            if wait_time > 0:
                time.sleep(wait_time)
                bucket.try_consume(tokens)
                return wait_time
            
            bucket.try_consume(tokens)
            return 0.0

class CommandThrottler:
    """Throttler for command usage."""
    
    def __init__(self):
        """Initialise command throttler."""
        self.cooldowns: Dict[str, Dict[str, float]] = {}
        self.lock = threading.RLock()
    
    def check_cooldown(self, command: str, user_id: str, cooldown_seconds: float) -> bool:
        """
        Check if a command is on cooldown for a user.
        
        Args:
            command: Command name
            user_id: User ID
            cooldown_seconds: Cooldown duration in seconds
        
        Returns:
            True if command is ready to use, False if on cooldown
        """
        with self.lock:
            now = time.time()
            
            # Initialise command dict if needed
            if command not in self.cooldowns:
                self.cooldowns[command] = {}
            
            # Check last use
            last_use = self.cooldowns[command].get(user_id, 0)
            time_since_last = now - last_use
            
            # Return cooldown status
            return time_since_last >= cooldown_seconds
    
    def get_remaining_cooldown(self, command: str, user_id: str, cooldown_seconds: float) -> float:
        """
        Get remaining cooldown time for a command and user.
        
        Args:
            command: Command name
            user_id: User ID
            cooldown_seconds: Cooldown duration in seconds
        
        Returns:
            Remaining cooldown time in seconds (0 if not on cooldown)
        """
        with self.lock:
            now = time.time()
            
            # Initialise command dict if needed
            if command not in self.cooldowns:
                return 0.0
            
            # Check last use
            last_use = self.cooldowns[command].get(user_id, 0)
            time_since_last = now - last_use
            
            # Return remaining time
            if time_since_last >= cooldown_seconds:
                return 0.0
            return cooldown_seconds - time_since_last
    
    def mark_use(self, command: str, user_id: str) -> None:
        """
        Mark a command as used by a user.
        
        Args:
            command: Command name
            user_id: User ID
        """
        with self.lock:
            now = time.time()
            
            # Initialise command dict if needed
            if command not in self.cooldowns:
                self.cooldowns[command] = {}
            
            # Update last use
            self.cooldowns[command][user_id] = now
    
    def reset_cooldown(self, command: str, user_id: str) -> None:
        """
        Reset cooldown for a command and user.
        
        Args:
            command: Command name
            user_id: User ID
        """
        with self.lock:
            if command in self.cooldowns and user_id in self.cooldowns[command]:
                del self.cooldowns[command][user_id]