"""
Tests for the throttling utility module.
"""
import unittest
from unittest.mock import patch, MagicMock
import time
import threading
from queue import Empty

from bot.utils.throttling import (
    PrioritisedItem, TokenBucket, RateLimiter,
    MessageQueue, PerUserRateLimiter, CommandThrottler
)
from bot.core.constants import MessagePriority
from bot.core.errors import ThrottlingError

class TestPrioritisedItem(unittest.TestCase):
    """Tests for PrioritisedItem class."""
    
    def test_ordering(self):
        """Test item ordering based on priority."""
        # Lower priority value means higher priority
        item1 = PrioritisedItem(priority=1, item="high priority")
        item2 = PrioritisedItem(priority=2, item="medium priority")
        item3 = PrioritisedItem(priority=3, item="low priority")
        
        # Compare items
        self.assertLess(item1, item2)
        self.assertLess(item2, item3)
        self.assertGreater(item3, item1)
        
        # Same priority, different items (should be equal)
        item4 = PrioritisedItem(priority=1, item="another high priority")
        self.assertEqual(item1, item4)
    
    def test_non_comparable_fields(self):
        """Test that item and timestamp are not used for comparison."""
        # Items with same priority but different timestamps and items
        item1 = PrioritisedItem(priority=1, item="item1", timestamp=100.0)
        item2 = PrioritisedItem(priority=1, item="item2", timestamp=200.0)
        
        # Should be equal because only priority is compared
        self.assertEqual(item1, item2)

class TestTokenBucket(unittest.TestCase):
    """Tests for TokenBucket class."""
    
    def setUp(self):
        """Set up for each test."""
        self.bucket = TokenBucket(rate=1.0, max_tokens=5)
    
    def test_init(self):
        """Test initialisation."""
        self.assertEqual(self.bucket.rate, 1.0)
        self.assertEqual(self.bucket.max_tokens, 5)
        self.assertEqual(self.bucket.tokens, 5)
    
    @patch('time.time')
    def test_update_tokens(self, mock_time):
        """Test token update based on elapsed time."""
        # Setup
        self.bucket.tokens = 0
        self.bucket.last_update = 100.0
        
        # 5 seconds have passed
        mock_time.return_value = 105.0
        self.bucket._update_tokens()
        
        # Should have 5 tokens now (rate = 1.0 tokens/second)
        self.assertEqual(self.bucket.tokens, 5)
        self.assertEqual(self.bucket.last_update, 105.0)
        
        # Should not exceed max_tokens
        mock_time.return_value = 115.0
        self.bucket._update_tokens()
        self.assertEqual(self.bucket.tokens, 5)
    
    @patch('time.time')
    def test_try_consume(self, mock_time):
        """Test token consumption."""
        mock_time.return_value = 100.0
        self.bucket.tokens = 5
        self.bucket.last_update = 100.0
        
        # Consume 3 tokens (should succeed)
        self.assertTrue(self.bucket.try_consume(3))
        self.assertEqual(self.bucket.tokens, 2)
        
        # Consume 3 more tokens (should fail)
        self.assertFalse(self.bucket.try_consume(3))
        self.assertEqual(self.bucket.tokens, 2)
        
        # Time passes, refill tokens
        mock_time.return_value = 102.0
        self.assertTrue(self.bucket.try_consume(1))
        self.assertEqual(self.bucket.tokens, 3)
    
    @patch('time.time')
    def test_get_wait_time(self, mock_time):
        """Test wait time calculation."""
        mock_time.return_value = 100.0
        self.bucket.tokens = 2
        self.bucket.last_update = 100.0
        
        # Need 2 tokens (we have 2, so wait time is 0)
        self.assertEqual(self.bucket.get_wait_time(2), 0.0)
        
        # Need 4 tokens (we have 2, need 2 more at 1 token/second)
        self.assertEqual(self.bucket.get_wait_time(4), 2.0)
        
        # Tokens refill over time
        mock_time.return_value = 101.0
        self.assertEqual(self.bucket.get_wait_time(4), 1.0)

class TestRateLimiter(unittest.TestCase):
    """Tests for RateLimiter class."""
    
    def setUp(self):
        """Set up for each test."""
        self.limiter = RateLimiter(rate=1.0, burst=3)
    
    @patch('bot.utils.throttling.TokenBucket')
    def test_check_limit(self, mock_bucket):
        """Test rate limit checking."""
        # Setup mock bucket
        mock_instance = mock_bucket.return_value
        
        # No rate limiting
        mock_instance.try_consume.return_value = True
        self.limiter.check_limit()  # Should not raise an exception
        
        # Rate limited
        mock_instance.try_consume.return_value = False
        mock_instance.get_wait_time.return_value = 2.0
        with self.assertRaises(ThrottlingError):
            self.limiter.check_limit()
    
    @patch('bot.utils.throttling.TokenBucket')
    @patch('time.sleep')
    def test_wait_if_needed(self, mock_sleep, mock_bucket):
        """Test waiting for rate limit."""
        # Setup mock bucket
        mock_instance = mock_bucket.return_value
        
        # No waiting needed
        mock_instance.get_wait_time.return_value = 0.0
        wait_time = self.limiter.wait_if_needed()
        self.assertEqual(wait_time, 0.0)
        mock_sleep.assert_not_called()
        
        # Wait needed
        mock_instance.get_wait_time.return_value = 2.0
        wait_time = self.limiter.wait_if_needed()
        self.assertEqual(wait_time, 2.0)
        mock_sleep.assert_called_with(2.0)

class TestMessageQueue(unittest.TestCase):
    """Tests for MessageQueue class."""
    
    def setUp(self):
        """Set up for each test."""
        self.message_handler = MagicMock()
        self.queue = MessageQueue(rate=1.0, burst=3)
    
    def tearDown(self):
        """Clean up after each test."""
        if self.queue.running:
            self.queue.stop()
    
    def test_start_stop(self):
        """Test starting and stopping the queue."""
        # Start queue
        self.queue.start(self.message_handler)
        self.assertTrue(self.queue.running)
        self.assertIsNotNone(self.queue.thread)
        
        # Start again (should do nothing)
        thread = self.queue.thread
        self.queue.start(self.message_handler)
        self.assertIs(self.queue.thread, thread)
        
        # Stop queue
        self.queue.stop()
        self.assertFalse(self.queue.running)
    
    @patch('bot.utils.throttling.PriorityQueue')
    def test_add_message(self, mock_queue):
        """Test adding messages to queue."""
        # Setup mock queue
        mock_instance = mock_queue.return_value
        
        # Add message (success)
        mock_instance.put_nowait.return_value = None
        result = self.queue.add_message("test message")
        self.assertTrue(result)
        
        # Add message (queue full)
        mock_instance.put_nowait.side_effect = Exception("Queue full")
        result = self.queue.add_message("test message")
        self.assertFalse(result)
    
    @patch('bot.utils.throttling.PriorityQueue')
    def test_process_queue(self, mock_queue):
        """Test message processing from queue."""
        # Setup
        self.queue.message_handler = self.message_handler
        
        # Mock queue get/empty behavior
        mock_instance = mock_queue.return_value
        mock_instance.get.side_effect = [
            PrioritisedItem(priority=MessagePriority.LOW.value, item="message1"),
            Empty(),  # To break the loop
        ]
        
        # Process queue
        self.queue.running = True
        self.queue._process_queue()
        
        # Check message was processed
        self.message_handler.assert_called_once_with("message1", MessagePriority.LOW)

class TestPerUserRateLimiter(unittest.TestCase):
    """Tests for PerUserRateLimiter class."""
    
    def setUp(self):
        """Set up for each test."""
        self.limiter = PerUserRateLimiter(rate=1.0, burst=3)
    
    @patch('time.time')
    def test_cleanup_inactive(self, mock_time):
        """Test cleanup of inactive users."""
        # Setup
        mock_time.return_value = 100.0
        self.limiter.last_cleanup = 0.0
        
        # Add some buckets
        bucket1 = TokenBucket(rate=1.0, max_tokens=3)
        bucket1.tokens = 3  # Full (inactive)
        
        bucket2 = TokenBucket(rate=1.0, max_tokens=3)
        bucket2.tokens = 1  # Not full (active)
        
        self.limiter.user_buckets = {
            "user1": bucket1,
            "user2": bucket2
        }
        
        # Run cleanup
        mock_time.return_value = 500.0  # After cleanup interval
        self.limiter._cleanup_inactive()
        
        # Check that inactive bucket was removed
        self.assertNotIn("user1", self.limiter.user_buckets)
        self.assertIn("user2", self.limiter.user_buckets)
        
        # Last cleanup time should be updated
        self.assertEqual(self.limiter.last_cleanup, 500.0)
    
    @patch('bot.utils.throttling.TokenBucket')
    def test_check_limit(self, mock_bucket):
        """Test per-user rate limit checking."""
        # Setup
        mock_instance = mock_bucket.return_value
        mock_instance.try_consume.return_value = True
        
        # First user (should create new bucket)
        self.limiter.check_limit("user1")
        self.assertIn("user1", self.limiter.user_buckets)
        
        # Rate limited
        mock_instance.try_consume.return_value = False
        mock_instance.get_wait_time.return_value = 2.0
        with self.assertRaises(ThrottlingError):
            self.limiter.check_limit("user2")
    
    @patch('bot.utils.throttling.TokenBucket')
    @patch('time.sleep')
    def test_wait_if_needed(self, mock_sleep, mock_bucket):
        """Test waiting for per-user rate limit."""
        # Setup
        mock_instance = mock_bucket.return_value
        
        # No wait needed
        mock_instance.get_wait_time.return_value = 0.0
        wait_time = self.limiter.wait_if_needed("user1")
        self.assertEqual(wait_time, 0.0)
        
        # Wait needed
        mock_instance.get_wait_time.return_value = 2.0
        wait_time = self.limiter.wait_if_needed("user2")
        self.assertEqual(wait_time, 2.0)
        mock_sleep.assert_called_with(2.0)

class TestCommandThrottler(unittest.TestCase):
    """Tests for CommandThrottler class."""
    
    def setUp(self):
        """Set up for each test."""
        self.throttler = CommandThrottler()
    
    @patch('time.time')
    def test_check_cooldown(self, mock_time):
        """Test command cooldown checking."""
        mock_time.return_value = 100.0
        
        # First use (no cooldown)
        self.assertTrue(self.throttler.check_cooldown("command", "user", 10.0))
        
        # Mark as used
        self.throttler.mark_use("command", "user")
        
        # Check cooldown (should be on cooldown)
        self.assertFalse(self.throttler.check_cooldown("command", "user", 10.0))
        
        # Wait for cooldown to expire
        mock_time.return_value = 111.0
        self.assertTrue(self.throttler.check_cooldown("command", "user", 10.0))
        
        # Different user (should not be on cooldown)
        mock_time.return_value = 100.0
        self.throttler.mark_use("command", "user1")
        self.assertFalse(self.throttler.check_cooldown("command", "user1", 10.0))
        self.assertTrue(self.throttler.check_cooldown("command", "user2", 10.0))
        
        # Different command (should not be on cooldown)
        self.throttler.mark_use("command1", "user")
        self.assertFalse(self.throttler.check_cooldown("command1", "user", 10.0))
        self.assertTrue(self.throttler.check_cooldown("command2", "user", 10.0))
    
    @patch('time.time')
    def test_get_remaining_cooldown(self, mock_time):
        """Test getting remaining cooldown time."""
        mock_time.return_value = 100.0
        
        # No previous use
        self.assertEqual(self.throttler.get_remaining_cooldown("command", "user", 10.0), 0.0)
        
        # Mark as used
        self.throttler.mark_use("command", "user")
        
        # Check remaining time
        self.assertEqual(self.throttler.get_remaining_cooldown("command", "user", 10.0), 10.0)
        
        # Partially elapsed
        mock_time.return_value = 105.0
        self.assertEqual(self.throttler.get_remaining_cooldown("command", "user", 10.0), 5.0)
        
        # Fully elapsed
        mock_time.return_value = 110.0
        self.assertEqual(self.throttler.get_remaining_cooldown("command", "user", 10.0), 0.0)
    
    @patch('time.time')
    def test_mark_use(self, mock_time):
        """Test marking command as used."""
        mock_time.return_value = 100.0
        
        # Mark command as used
        self.throttler.mark_use("command", "user")
        
        # Check command was marked
        self.assertIn("command", self.throttler.cooldowns)
        self.assertIn("user", self.throttler.cooldowns["command"])
        self.assertEqual(self.throttler.cooldowns["command"]["user"], 100.0)
    
    def test_reset_cooldown(self):
        """Test resetting cooldown for a command and user."""
        # Setup
        self.throttler.cooldowns = {
            "command": {
                "user1": 100.0,
                "user2": 100.0
            }
        }
        
        # Reset cooldown for user1
        self.throttler.reset_cooldown("command", "user1")
        
        # Check cooldown was reset
        self.assertNotIn("user1", self.throttler.cooldowns["command"])
        self.assertIn("user2", self.throttler.cooldowns["command"])
        
        # Reset non-existent cooldown (should not raise exception)
        self.throttler.reset_cooldown("command", "user3")

if __name__ == '__main__':
    unittest.main()