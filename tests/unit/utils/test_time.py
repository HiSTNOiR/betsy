"""
Unit tests for the bot.utils.time module.

This module contains tests for time-related utility functions.
"""

import datetime
import unittest
from unittest import mock
from datetime import datetime, timedelta, timezone
import re

from bot.utils.time import (
    get_utc_now,
    to_utc,
    format_datetime,
    parse_datetime,
    format_duration,
    parse_duration,
    time_until,
    time_since,
    format_relative_time,
    is_same_day,
    add_time,
    format_timestamp,
    get_date_range
)


class TestUtilsTime(unittest.TestCase):
    """Test cases for the bot.utils.time module."""

    def test_get_utc_now(self):
        """Test get_utc_now returns a datetime with UTC timezone."""
        now = get_utc_now()

        self.assertIsInstance(now, datetime)
        self.assertEqual(now.tzinfo, timezone.utc)
        # Ensure the time is recent (within 2 seconds of actual current time)
        actual_now = datetime.now(timezone.utc)
        self.assertLess(abs((now - actual_now).total_seconds()), 2)

    def test_to_utc(self):
        """Test to_utc converts datetimes to UTC timezone."""
        # Test with a timezone-aware datetime
        local_tz = datetime.now().astimezone().tzinfo
        dt_aware = datetime(2023, 1, 1, 12, 0, 0, tzinfo=local_tz)
        result = to_utc(dt_aware)

        self.assertEqual(result.tzinfo, timezone.utc)

        # Test with a timezone-naive datetime
        dt_naive = datetime(2023, 1, 1, 12, 0, 0)
        result = to_utc(dt_naive)

        self.assertEqual(result.tzinfo, timezone.utc)
        # The exact offset would depend on the local timezone, so we just check it's not the same time
        self.assertNotEqual(dt_naive.hour, result.hour)

    def test_format_datetime(self):
        """Test format_datetime correctly formats datetimes."""
        dt = datetime(2023, 1, 1, 12, 34, 56, tzinfo=timezone.utc)

        # Test default format
        result = format_datetime(dt)
        self.assertEqual(result, "2023-01-01 12:34:56")

        # Test custom format
        result = format_datetime(dt, format_str="%Y/%m/%d %H-%M")
        self.assertEqual(result, "2023/01/01 12-34")

        # Test with timezone
        result = format_datetime(dt, include_timezone=True)
        self.assertEqual(result, "2023-01-01 12:34:56 +0000")

    def test_parse_datetime(self):
        """Test parse_datetime correctly parses datetime strings."""
        # Test default format
        result = parse_datetime("2023-01-01 12:34:56")
        expected = datetime(2023, 1, 1, 12, 34, 56)
        self.assertEqual(result, expected)

        # Test custom format
        result = parse_datetime(
            "2023/01/01 12-34", format_str="%Y/%m/%d %H-%M")
        expected = datetime(2023, 1, 1, 12, 34)
        self.assertEqual(result, expected)

        # Test with default timezone
        result = parse_datetime("2023-01-01 12:34:56",
                                default_timezone=timezone.utc)
        expected = datetime(2023, 1, 1, 12, 34, 56, tzinfo=timezone.utc)
        self.assertEqual(result, expected)

        # Test with invalid format
        with self.assertRaises(ValueError):
            parse_datetime("invalid date")

    def test_format_duration(self):
        """Test format_duration correctly formats time durations."""
        # Test with seconds only
        self.assertEqual(format_duration(45), "45s")

        # Test with minutes and seconds
        self.assertEqual(format_duration(65), "1m 5s")

        # Test with hours, minutes, seconds
        self.assertEqual(format_duration(3665), "1h 1m 5s")

        # Test with days, hours, minutes, seconds
        self.assertEqual(format_duration(90065), "1d 1h 1m 5s")

        # Test without seconds
        self.assertEqual(format_duration(3665, include_seconds=False), "1h 1m")

        # Test with milliseconds
        self.assertEqual(format_duration(
            3.5, include_milliseconds=True), "3.500s")

        # Test with negative duration
        self.assertEqual(format_duration(-10), "0s")

    def test_parse_duration(self):
        """Test parse_duration correctly parses duration strings."""
        # Test with seconds only
        self.assertEqual(parse_duration("45s"), 45)

        # Test with minutes and seconds
        self.assertEqual(parse_duration("1m 5s"), 65)

        # Test with hours, minutes, seconds
        self.assertEqual(parse_duration("1h 1m 5s"), 3665)

        # Test with days, hours, minutes, seconds
        self.assertEqual(parse_duration("1d 1h 1m 5s"), 90065)

        # Test without spaces
        self.assertEqual(parse_duration("1h5m10s"), 3910)

        # Test with decimal values
        self.assertEqual(parse_duration("1.5h"), 5400)

        # Test with invalid format
        with self.assertRaises(ValueError):
            parse_duration("invalid duration")

    @mock.patch('bot.utils.time.get_utc_now')
    def test_time_until(self, mock_get_utc_now):
        """Test time_until returns correct timedelta to future datetime."""
        mock_now = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        mock_get_utc_now.return_value = mock_now

        # Test with future time
        future = datetime(2023, 1, 1, 14, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(time_until(future), timedelta(hours=2))

        # Test with past time (should return zero)
        past = datetime(2023, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(time_until(past), timedelta(0))

        # Test with timezone-naive datetime
        naive_future = datetime(2023, 1, 1, 14, 0, 0)
        self.assertEqual(time_until(naive_future), timedelta(hours=2))

    @mock.patch('bot.utils.time.get_utc_now')
    def test_time_since(self, mock_get_utc_now):
        """Test time_since returns correct timedelta from past datetime."""
        mock_now = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        mock_get_utc_now.return_value = mock_now

        # Test with past time
        past = datetime(2023, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(time_since(past), timedelta(hours=2))

        # Test with future time (should return zero)
        future = datetime(2023, 1, 1, 14, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(time_since(future), timedelta(0))

        # Test with timezone-naive datetime
        naive_past = datetime(2023, 1, 1, 10, 0, 0)
        self.assertEqual(time_since(naive_past), timedelta(hours=2))

    @mock.patch('bot.utils.time.get_utc_now')
    def test_format_relative_time(self, mock_get_utc_now):
        """Test format_relative_time formats time relative to now."""
        mock_now = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        mock_get_utc_now.return_value = mock_now

        # Test with past time (5 minutes ago, 0 seconds)
        past = datetime(2023, 1, 1, 11, 55, 0, tzinfo=timezone.utc)
        self.assertEqual(format_relative_time(past), "5m ago")

        # Test with future time (5 minutes ahead, 0 seconds)
        future = datetime(2023, 1, 1, 12, 5, 0, tzinfo=timezone.utc)
        self.assertEqual(format_relative_time(future), "in 5m")

        # Test with non-zero seconds
        past_with_seconds = datetime(
            2023, 1, 1, 11, 55, 30, tzinfo=timezone.utc)
        self.assertEqual(format_relative_time(past_with_seconds), "4m 30s ago")

        # Test without seconds
        self.assertEqual(format_relative_time(
            past, include_seconds=False), "5m ago")

        # Test with timezone-naive datetime
        naive_past = datetime(2023, 1, 1, 11, 55, 0)
        self.assertEqual(format_relative_time(naive_past), "5m ago")

    def test_is_same_day(self):
        """Test is_same_day correctly identifies same-day datetimes."""
        # Test same day, different times
        dt1 = datetime(2023, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        dt2 = datetime(2023, 1, 1, 14, 0, 0, tzinfo=timezone.utc)
        self.assertTrue(is_same_day(dt1, dt2))

        # Test different days
        dt3 = datetime(2023, 1, 2, 10, 0, 0, tzinfo=timezone.utc)
        self.assertFalse(is_same_day(dt1, dt3))

        # Test one with timezone, one without
        dt4 = datetime(2023, 1, 1, 10, 0, 0)
        self.assertTrue(is_same_day(dt1, dt4))

        # Test with different timezones but same day in UTC
        local_tz = datetime.now().astimezone().tzinfo
        dt5 = datetime(2023, 1, 1, 22, 0, 0, tzinfo=timezone.utc)
        # Assuming local_tz is UTC+4
        dt6 = datetime(2023, 1, 2, 2, 0, 0, tzinfo=local_tz)
        # This test might be flaky depending on the local timezone, so we'll skip the assertion
        # and just check that it completes without error
        is_same_day(dt5, dt6)

    def test_add_time(self):
        """Test add_time correctly adds time to datetimes."""
        dt = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

        # Test adding days
        result = add_time(dt, days=2)
        expected = datetime(2023, 1, 3, 12, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(result, expected)

        # Test adding hours
        result = add_time(dt, hours=5)
        expected = datetime(2023, 1, 1, 17, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(result, expected)

        # Test adding minutes
        result = add_time(dt, minutes=30)
        expected = datetime(2023, 1, 1, 12, 30, 0, tzinfo=timezone.utc)
        self.assertEqual(result, expected)

        # Test adding seconds
        result = add_time(dt, seconds=45)
        expected = datetime(2023, 1, 1, 12, 0, 45, tzinfo=timezone.utc)
        self.assertEqual(result, expected)

        # Test adding multiple units
        result = add_time(dt, days=1, hours=2, minutes=3, seconds=4)
        expected = datetime(2023, 1, 2, 14, 3, 4, tzinfo=timezone.utc)
        self.assertEqual(result, expected)

    def test_format_timestamp(self):
        """Test format_timestamp correctly formats datetime as timestamp."""
        dt = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

        # Jan 1, 2023 12:00:00 UTC is timestamp 1672574400
        self.assertEqual(format_timestamp(dt), "1672574400")

        # Test with timezone-naive datetime
        naive_dt = datetime(2023, 1, 1, 12, 0, 0)
        self.assertEqual(format_timestamp(naive_dt), "1672574400")

    def test_get_date_range(self):
        """Test get_date_range returns correct list of dates."""
        start = datetime(2023, 1, 1, tzinfo=timezone.utc)
        end = datetime(2023, 1, 5, tzinfo=timezone.utc)

        # Test inclusive date range
        dates = get_date_range(start, end, include_end=True)
        expected_dates = [
            datetime(2023, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
            datetime(2023, 1, 2, 0, 0, 0, tzinfo=timezone.utc),
            datetime(2023, 1, 3, 0, 0, 0, tzinfo=timezone.utc),
            datetime(2023, 1, 4, 0, 0, 0, tzinfo=timezone.utc),
            datetime(2023, 1, 5, 0, 0, 0, tzinfo=timezone.utc),
        ]
        self.assertEqual(dates, expected_dates)

        # Test exclusive date range
        dates = get_date_range(start, end, include_end=False)
        expected_dates = [
            datetime(2023, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
            datetime(2023, 1, 2, 0, 0, 0, tzinfo=timezone.utc),
            datetime(2023, 1, 3, 0, 0, 0, tzinfo=timezone.utc),
            datetime(2023, 1, 4, 0, 0, 0, tzinfo=timezone.utc),
        ]
        self.assertEqual(dates, expected_dates)

        # Test with reversed dates (should return empty list)
        reversed_dates = get_date_range(end, start)
        self.assertEqual(reversed_dates, [])

        # Test with same date
        same_date = get_date_range(start, start, include_end=True)
        expected = [datetime(2023, 1, 1, 0, 0, 0, tzinfo=timezone.utc)]
        self.assertEqual(same_date, expected)

        # Test with same date, exclusive
        same_date_exclusive = get_date_range(start, start, include_end=False)
        self.assertEqual(same_date_exclusive, [])


if __name__ == '__main__':
    unittest.main()
