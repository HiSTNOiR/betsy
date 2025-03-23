"""
Tests for the time utility module.
"""
import unittest
import time
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, MagicMock

from bot.utils.time_utils import (
    get_current_timestamp, get_current_datetime, get_formatted_datetime,
    parse_datetime, datetime_to_timestamp, timestamp_to_datetime,
    get_time_difference, get_time_difference_seconds, is_expired,
    get_random_delay, sleep, with_timeout, get_time_until,
    format_timedelta, get_cooldown_end_time, format_cooldown_remaining
)

class TestTimeUtils(unittest.TestCase):
    """Tests for time utility functions."""
    
    def test_get_current_timestamp(self):
        """Test current timestamp."""
        # Just ensure it returns a float
        timestamp = get_current_timestamp()
        self.assertIsInstance(timestamp, float)
        
        # Ensure it's current (within a small margin)
        self.assertAlmostEqual(timestamp, time.time(), delta=1.0)
    
    def test_get_current_datetime(self):
        """Test current datetime."""
        # Ensure it returns a datetime with timezone
        dt = get_current_datetime()
        self.assertIsInstance(dt, datetime)
        self.assertIsNotNone(dt.tzinfo)
        
        # Ensure it's UTC
        self.assertEqual(dt.tzinfo, timezone.utc)
        
        # Ensure it's current (within a small margin)
        self.assertAlmostEqual(dt.timestamp(), time.time(), delta=1.0)
    
    def test_get_formatted_datetime(self):
        """Test datetime formatting."""
        # Test with specific datetime
        dt = datetime(2023, 1, 1, 12, 30, 45, tzinfo=timezone.utc)
        self.assertEqual(
            get_formatted_datetime(dt),
            "2023-01-01 12:30:45"
        )
        
        # Custom format
        self.assertEqual(
            get_formatted_datetime(dt, format_str="%Y/%m/%d %H:%M"),
            "2023/01/01 12:30"
        )
        
        # Current time (just ensure it doesn't raise an exception)
        formatted = get_formatted_datetime()
        self.assertIsInstance(formatted, str)
    
    def test_parse_datetime(self):
        """Test datetime parsing."""
        # Normal format
        dt = parse_datetime("2023-01-01 12:30:45")
        self.assertEqual(dt.year, 2023)
        self.assertEqual(dt.month, 1)
        self.assertEqual(dt.day, 1)
        self.assertEqual(dt.hour, 12)
        self.assertEqual(dt.minute, 30)
        self.assertEqual(dt.second, 45)
        
        # Custom format
        dt = parse_datetime("2023/01/01 12:30", format_str="%Y/%m/%d %H:%M")
        self.assertEqual(dt.year, 2023)
        self.assertEqual(dt.month, 1)
        self.assertEqual(dt.day, 1)
        self.assertEqual(dt.hour, 12)
        self.assertEqual(dt.minute, 30)
        
        # Invalid format
        self.assertIsNone(parse_datetime("invalid"))
    
    def test_datetime_to_timestamp(self):
        """Test datetime to timestamp conversion."""
        dt = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        timestamp = datetime_to_timestamp(dt)
        self.assertEqual(timestamp, dt.timestamp())
    
    def test_timestamp_to_datetime(self):
        """Test timestamp to datetime conversion."""
        timestamp = 1672574400.0  # 2023-01-01 12:00:00 UTC
        dt = timestamp_to_datetime(timestamp)
        
        self.assertEqual(dt.year, 2023)
        self.assertEqual(dt.month, 1)
        self.assertEqual(dt.day, 1)
        self.assertEqual(dt.hour, 12)
        self.assertEqual(dt.minute, 0)
        self.assertEqual(dt.second, 0)
        self.assertEqual(dt.tzinfo, timezone.utc)
    
    def test_get_time_difference(self):
        """Test time difference calculation."""
        dt1 = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        dt2 = datetime(2023, 1, 1, 12, 30, 0, tzinfo=timezone.utc)
        
        # Positive difference
        diff = get_time_difference(dt1, dt2)
        self.assertEqual(diff, timedelta(minutes=30))
        
        # Negative difference (absolute value)
        diff = get_time_difference(dt2, dt1)
        self.assertEqual(diff, timedelta(minutes=30))
    
    def test_get_time_difference_seconds(self):
        """Test time difference calculation in seconds."""
        dt1 = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        dt2 = datetime(2023, 1, 1, 12, 30, 0, tzinfo=timezone.utc)
        
        # Positive difference
        diff = get_time_difference_seconds(dt1, dt2)
        self.assertEqual(diff, 1800.0)
        
        # Negative difference (absolute value)
        diff = get_time_difference_seconds(dt2, dt1)
        self.assertEqual(diff, 1800.0)
    
    def test_is_expired(self):
        """Test expiration check."""
        current_time = time.time()
        
        # Expired (in the past)
        self.assertTrue(is_expired(current_time - 60, 30))
        
        # Not expired (in the future)
        self.assertFalse(is_expired(current_time, 30))
        self.assertFalse(is_expired(current_time + 60, 30))
    
    @patch('random.uniform')
    def test_get_random_delay(self, mock_uniform):
        """Test random delay generation."""
        mock_uniform.return_value = 2.0
        
        # Default range
        delay = get_random_delay()
        mock_uniform.assert_called_with(0.5, 3.0)
        self.assertEqual(delay, 2.0)
        
        # Custom range
        delay = get_random_delay(1.0, 5.0)
        mock_uniform.assert_called_with(1.0, 5.0)
        self.assertEqual(delay, 2.0)
    
    @patch('time.sleep')
    def test_sleep(self, mock_sleep):
        """Test sleep function."""
        # Simple sleep
        sleep(2.0)
        mock_sleep.assert_called_with(2.0)
    
    def test_with_timeout(self):
        """Test function execution with timeout."""
        # Function completes within timeout
        def fast_function():
            return "success"
        
        result = with_timeout(fast_function, 1.0)
        self.assertEqual(result, "success")
        
        # Function exceeds timeout
        def slow_function():
            time.sleep(2.0)
            return "success"
        
        with self.assertRaises(TimeoutError):
            with_timeout(slow_function, 0.5)
    
    def test_get_time_until(self):
        """Test time until calculation."""
        now = get_current_datetime()
        future = now + timedelta(minutes=30)
        
        # Future time
        delta = get_time_until(future)
        self.assertAlmostEqual(delta.total_seconds(), 1800, delta=1)
        
        # Past time (should be zero)
        past = now - timedelta(minutes=30)
        delta = get_time_until(past)
        self.assertEqual(delta.total_seconds(), 0)
    
    def test_format_timedelta(self):
        """Test timedelta formatting."""
        # Days, hours, minutes, seconds
        delta = timedelta(days=2, hours=3, minutes=45, seconds=30)
        self.assertEqual(format_timedelta(delta), "2d 3h 45m 30s")
        
        # Without seconds
        self.assertEqual(format_timedelta(delta, include_seconds=False), "2d 3h 45m")
        
        # Only hours and minutes
        delta = timedelta(hours=3, minutes=45)
        self.assertEqual(format_timedelta(delta), "3h 45m")
        
        # Only minutes and seconds
        delta = timedelta(minutes=5, seconds=30)
        self.assertEqual(format_timedelta(delta), "5m 30s")
        
        # Only seconds
        delta = timedelta(seconds=30)
        self.assertEqual(format_timedelta(delta), "30s")
        
        # Zero
        delta = timedelta(seconds=0)
        self.assertEqual(format_timedelta(delta), "0s")
    
    def test_get_cooldown_end_time(self):
        """Test cooldown end time calculation."""
        now = get_current_datetime()
        
        # 60-second cooldown
        end_time = get_cooldown_end_time(60)
        self.assertAlmostEqual(
            get_time_difference_seconds(now, end_time),
            60,
            delta=1
        )
    
    def test_format_cooldown_remaining(self):
        """Test cooldown remaining time formatting."""
        now = get_current_datetime()
        
        # Future time
        end_time = now + timedelta(minutes=5, seconds=30)
        self.assertEqual(format_cooldown_remaining(end_time), "5m 30s")
        
        # Past time (cooldown expired)
        end_time = now - timedelta(minutes=5)
        self.assertEqual(format_cooldown_remaining(end_time), "0s")

if __name__ == '__main__':
    unittest.main()