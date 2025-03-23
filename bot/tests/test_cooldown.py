"""
Tests for the cooldown utility module.
"""
import unittest
from unittest.mock import patch
import time

from bot.utils.cooldown import Cooldown, CooldownManager, BucketType
from bot.core.errors import CooldownError

class TestCooldown(unittest.TestCase):
    """Tests for Cooldown class."""
    
    def setUp(self):
        """Set up for each test."""
        self.cooldown = Cooldown(rate=2, per=10.0)
    
    def test_init(self):
        """Test initialisation."""
        self.assertEqual(self.cooldown.rate, 2)
        self.assertEqual(self.cooldown.per, 10.0)
        self.assertEqual(self.cooldown._tokens, 2)
        self.assertEqual(self.cooldown._last, 0.0)
    
    def test_reset(self):
        """Test cooldown reset."""
        # Use up some tokens
        self.cooldown._tokens = 0
        self.cooldown._last = 123.0
        
        # Reset
        self.cooldown.reset()
        
        # Should be back to initial state
        self.assertEqual(self.cooldown._tokens, 2)
        self.assertEqual(self.cooldown._last, 0.0)
    
    def test_get_tokens(self):
        """Test getting token count."""
        self.cooldown._tokens = 1
        self.assertEqual(self.cooldown.get_tokens(), 1)
    
    @patch('bot.utils.time_utils.get_current_timestamp')
    def test_update_rate_limit(self, mock_timestamp):
        """Test rate limit updating."""
        # Initial state (2 tokens available)
        mock_timestamp.return_value = 100.0
        self.cooldown._tokens = 2
        self.cooldown._last = 100.0
        
        # Use 1 token (should succeed, 1 token remains)
        result = self.cooldown.update_rate_limit()
        self.assertIsNone(result)
        self.assertEqual(self.cooldown._tokens, 1)
        self.assertEqual(self.cooldown._last, 100.0)
        
        # Use 1 more token (should succeed, 0 tokens remain)
        result = self.cooldown.update_rate_limit()
        self.assertIsNone(result)
        self.assertEqual(self.cooldown._tokens, 0)
        self.assertEqual(self.cooldown._last, 100.0)
        
        # Try to use another token (should fail, need to wait)
        result = self.cooldown.update_rate_limit()
        self.assertEqual(result, 10.0)  # Need to wait 10 seconds for next token
        
        # Time passes (5 seconds), tokens refill
        mock_timestamp.return_value = 105.0
        result = self.cooldown.update_rate_limit()
        self.assertEqual(result, 5.0)  # Still need to wait 5 more seconds
        
        # Time passes (more 5 seconds), 1 token available
        mock_timestamp.return_value = 110.0
        result = self.cooldown.update_rate_limit()
        self.assertIsNone(result)  # Can use 1 token now
        self.assertEqual(self.cooldown._tokens, 0)
        
        # Time passes (more 10 seconds), 1 token available
        mock_timestamp.return_value = 120.0
        result = self.cooldown.update_rate_limit()
        self.assertIsNone(result)  # Can use 1 token now
        self.assertEqual(self.cooldown._tokens, 0)
    
    @patch('bot.utils.time_utils.get_current_timestamp')
    def test_get_retry_after(self, mock_timestamp):
        """Test retry after calculation."""
        # Initial state (2 tokens available)
        mock_timestamp.return_value = 100.0
        self.cooldown._tokens = 2
        self.cooldown._last = 100.0
        
        # With tokens available, retry after is 0
        self.assertEqual(self.cooldown.get_retry_after(), 0.0)
        
        # Use both tokens
        self.cooldown._tokens = 0
        
        # Now retry after is 10 seconds
        self.assertEqual(self.cooldown.get_retry_after(), 10.0)
        
        # Time passes (5 seconds)
        mock_timestamp.return_value = 105.0
        self.assertEqual(self.cooldown.get_retry_after(), 5.0)
        
        # Time passes (more 5 seconds)
        mock_timestamp.return_value = 110.0
        self.assertEqual(self.cooldown.get_retry_after(), 0.0)

class TestCooldownManager(unittest.TestCase):
    """Tests for CooldownManager class."""
    
    def setUp(self):
        """Set up for each test."""
        self.manager = CooldownManager()
    
    def test_get_bucket_key(self):
        """Test bucket key generation."""
        # Default bucket
        key = self.manager._get_bucket_key("command")
        self.assertEqual(key, "global")
        
        # User bucket
        key = self.manager._get_bucket_key("command", user_id="user123", bucket_type=BucketType.USER)
        self.assertEqual(key, "user:user123")
        
        # Channel bucket
        key = self.manager._get_bucket_key("command", channel_id="channel123", bucket_type=BucketType.CHANNEL)
        self.assertEqual(key, "channel:channel123")
        
        # User-channel bucket
        key = self.manager._get_bucket_key(
            "command", 
            user_id="user123", 
            channel_id="channel123", 
            bucket_type=BucketType.USER_CHANNEL
        )
        self.assertEqual(key, "user:user123:channel:channel123")
        
        # Missing required user_id
        with self.assertRaises(ValueError):
            self.manager._get_bucket_key("command", bucket_type=BucketType.USER)
        
        # Missing required channel_id
        with self.assertRaises(ValueError):
            self.manager._get_bucket_key("command", bucket_type=BucketType.CHANNEL)
        
        # Missing required user_id and channel_id
        with self.assertRaises(ValueError):
            self.manager._get_bucket_key("command", bucket_type=BucketType.USER_CHANNEL)
        
        # Invalid bucket type
        with self.assertRaises(ValueError):
            self.manager._get_bucket_key("command", bucket_type="invalid")
    
    def test_get_bucket(self):
        """Test getting a bucket."""
        # Non-existent bucket
        bucket = self.manager.get_bucket("command", "key")
        self.assertIsNone(bucket)
        
        # Add a bucket
        self.manager.cooldowns = {"command": {"key": "bucket"}}
        bucket = self.manager.get_bucket("command", "key")
        self.assertEqual(bucket, "bucket")
    
    def test_add_bucket(self):
        """Test adding a bucket."""
        # Add a bucket
        bucket = self.manager.add_bucket("command", "key", 2, 10.0)
        
        # Check bucket was added
        self.assertIn("command", self.manager.cooldowns)
        self.assertIn("key", self.manager.cooldowns["command"])
        self.assertIs(self.manager.cooldowns["command"]["key"], bucket)
        
        # Check bucket properties
        self.assertEqual(bucket.rate, 2)
        self.assertEqual(bucket.per, 10.0)
    
    def test_get_or_create_bucket(self):
        """Test getting or creating a bucket."""
        # New bucket
        bucket1 = self.manager.get_or_create_bucket("command", "key", 2, 10.0)
        self.assertIn("command", self.manager.cooldowns)
        self.assertIn("key", self.manager.cooldowns["command"])
        
        # Existing bucket
        bucket2 = self.manager.get_or_create_bucket("command", "key", 3, 20.0)
        self.assertIs(bucket1, bucket2)  # Should be the same bucket instance
    
    def test_reset_bucket(self):
        """Test resetting a bucket."""
        # Add a bucket and use it
        bucket = self.manager.add_bucket("command", "key", 2, 10.0)
        bucket._tokens = 0
        bucket._last = 123.0
        
        # Reset the bucket
        result = self.manager.reset_bucket("command", "key")
        self.assertTrue(result)
        
        # Check bucket was reset
        self.assertEqual(bucket._tokens, 2)
        self.assertEqual(bucket._last, 0.0)
        
        # Reset non-existent bucket
        result = self.manager.reset_bucket("command", "nonexistent")
        self.assertFalse(result)
    
    def test_remove_bucket(self):
        """Test removing a bucket."""
        # Add buckets
        self.manager.add_bucket("command1", "key1", 2, 10.0)
        self.manager.add_bucket("command1", "key2", 2, 10.0)
        self.manager.add_bucket("command2", "key1", 2, 10.0)
        
        # Remove a bucket
        result = self.manager.remove_bucket("command1", "key1")
        self.assertTrue(result)
        
        # Check bucket was removed
        self.assertNotIn("key1", self.manager.cooldowns["command1"])
        self.assertIn("key2", self.manager.cooldowns["command1"])
        
        # Remove the last bucket for a command
        result = self.manager.remove_bucket("command1", "key2")
        self.assertTrue(result)
        
        # Command dict should be cleaned up
        self.assertNotIn("command1", self.manager.cooldowns)
        
        # Remove non-existent bucket
        result = self.manager.remove_bucket("command1", "key1")
        self.assertFalse(result)
    
    @patch('bot.utils.cooldown.Cooldown')
    def test_check_cooldown(self, mock_cooldown):
        """Test cooldown checking."""
        # Setup mock cooldown
        mock_instance = mock_cooldown.return_value
        
        # Not on cooldown
        mock_instance.update_rate_limit.return_value = None
        self.manager.check_cooldown("command", 2, 10.0)  # Should not raise an exception
        
        # On cooldown
        mock_instance.update_rate_limit.return_value = 5.0
        with self.assertRaises(CooldownError) as cm:
            self.manager.check_cooldown("command", 2, 10.0)
        self.assertAlmostEqual(cm.exception.remaining, 5.0)
    
    @patch('bot.utils.cooldown.Cooldown')
    def test_reset_cooldown(self, mock_cooldown):
        """Test resetting a cooldown via the manager."""
        # Setup mock
        mock_instance = mock_cooldown.return_value
        mock_instance.reset.return_value = None
        
        # Add a cooldown
        self.manager.cooldowns = {
            "command": {
                "user:user123": mock_instance
            }
        }
        
        # Reset cooldown
        result = self.manager.reset_cooldown("command", user_id="user123", bucket_type=BucketType.USER)
        self.assertTrue(result)
        mock_instance.reset.assert_called_once()
        
        # Reset non-existent cooldown
        result = self.manager.reset_cooldown("command", user_id="nonexistent", bucket_type=BucketType.USER)
        self.assertFalse(result)
    
    @patch('bot.utils.cooldown.Cooldown')
    def test_get_cooldown_remaining(self, mock_cooldown):
        """Test getting remaining cooldown time."""
        # Setup mock
        mock_instance = mock_cooldown.return_value
        mock_instance.get_retry_after.return_value = 5.0
        
        # Create a cooldown
        self.manager.cooldowns = {
            "command": {
                "user:user123": mock_instance
            }
        }
        
        # Get remaining time (existing cooldown)
        remaining = self.manager.get_cooldown_remaining(
            "command", 2, 10.0, user_id="user123", bucket_type=BucketType.USER
        )
        self.assertEqual(remaining, 5.0)
        
        # Get remaining time (non-existent cooldown)
        remaining = self.manager.get_cooldown_remaining(
            "command", 2, 10.0, user_id="nonexistent", bucket_type=BucketType.USER
        )
        self.assertEqual(remaining, 0.0)

if __name__ == '__main__':
    unittest.main()