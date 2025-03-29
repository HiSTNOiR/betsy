"""
Unit tests for the formatting utility module.

This module contains tests for the text formatting utilities in bot/utils/formatting.py.
"""

import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

from bot.utils.formatting import (
    format_number,
    format_currency,
    pluralise,
    truncate,
    format_list,
    clean_text,
    capitalise_first,
    capitalise_words,
    format_twitch_message,
    format_twitch_command,
    format_time_elapsed,
    format_timestamp_for_humans,
    format_bytes,
    strip_html_tags,
    escape_markdown,
    format_exception,
    format_json
)


class TestFormatNumber(unittest.TestCase):
    """Tests for the format_number function."""

    def test_integer_formatting(self):
        """Test formatting integers."""
        self.assertEqual(format_number(1000), "1,000")
        self.assertEqual(format_number(1000000), "1,000,000")
        self.assertEqual(format_number(0), "0")
        self.assertEqual(format_number(-1000), "-1,000")

    def test_float_formatting(self):
        """Test formatting floats."""
        self.assertEqual(format_number(1000.5, decimals=1), "1,000.5")
        self.assertEqual(format_number(1000.5, decimals=2), "1,000.50")
        self.assertEqual(format_number(1000.5, decimals=0), "1,001")

    def test_custom_separators(self):
        """Test custom separators."""
        self.assertEqual(format_number(1000, thousands_separator="."), "1.000")
        self.assertEqual(format_number(
            1000.5, decimals=1, thousands_separator=".", decimal_separator=","), "1.000,5")

    def test_non_numeric(self):
        """Test handling of non-numeric inputs."""
        self.assertEqual(format_number("abc"), "abc")
        self.assertEqual(format_number(None), "None")


class TestFormatCurrency(unittest.TestCase):
    """Tests for the format_currency function."""

    def test_default_formatting(self):
        """Test default currency formatting."""
        self.assertEqual(format_currency(1000), "£1,000.00")

    def test_different_currency(self):
        """Test different currency symbols."""
        self.assertEqual(format_currency(1000, currency="$"), "$1,000.00")
        self.assertEqual(format_currency(1000, currency="€"), "€1,000.00")

    def test_different_decimals(self):
        """Test different decimal places."""
        self.assertEqual(format_currency(1000, decimals=0), "£1,000")
        self.assertEqual(format_currency(1000.5, decimals=1), "£1,000.5")

    def test_suffix_position(self):
        """Test currency as suffix."""
        self.assertEqual(format_currency(
            1000, currency="£", position="suffix"), "1,000.00£")


class TestPluralise(unittest.TestCase):
    """Tests for the pluralise function."""

    def test_singular(self):
        """Test singular case."""
        self.assertEqual(pluralise(1, "apple"), "1 apple")
        self.assertEqual(pluralise(1, "apple", include_count=False), "apple")

    def test_plural(self):
        """Test plural case."""
        self.assertEqual(pluralise(2, "apple"), "2 apples")
        self.assertEqual(pluralise(0, "apple"), "0 apples")

    def test_custom_plural(self):
        """Test custom plural form."""
        self.assertEqual(pluralise(2, "child", "children"), "2 children")
        self.assertEqual(pluralise(1, "child", "children"), "1 child")

    def test_special_plurals(self):
        """Test special plural cases."""
        self.assertEqual(pluralise(2, "kiss"), "2 kisses")
        self.assertEqual(pluralise(2, "box"), "2 boxes")
        self.assertEqual(pluralise(2, "party"), "2 parties")


class TestTruncate(unittest.TestCase):
    """Tests for the truncate function."""

    def test_no_truncation_needed(self):
        """Test when no truncation is needed."""
        self.assertEqual(truncate("Hello", 10), "Hello")
        self.assertEqual(truncate("", 10), "")

    def test_truncation(self):
        """Test truncation."""
        self.assertEqual(truncate("Hello world", 8), "Hello...")
        self.assertEqual(truncate("Hello world", 5), "He...")

    def test_custom_suffix(self):
        """Test custom suffix."""
        self.assertEqual(truncate("Hello world", 8, suffix="!"), "Hello wo!")
        self.assertEqual(truncate("Hello world", 8, suffix=""), "Hello wo")

    def test_break_on_word(self):
        """Test breaking on word boundaries."""
        self.assertEqual(
            truncate("Hello world", 8, break_on_word=True), "Hello...")
        self.assertEqual(truncate("Hello beautiful world", 15,
                         break_on_word=True), "Hello beautiful...")

    def test_short_max_length(self):
        """Test very short max length."""
        self.assertEqual(truncate("Hello", 3, suffix="..."), "...")
        self.assertEqual(truncate("Hello", 0, suffix="..."), "...")


class TestFormatList(unittest.TestCase):
    """Tests for the format_list function."""

    def test_empty_list(self):
        """Test empty list."""
        self.assertEqual(format_list([]), "")

    def test_single_item(self):
        """Test single item list."""
        self.assertEqual(format_list(["apple"]), "apple")

    def test_two_items(self):
        """Test two item list."""
        self.assertEqual(format_list(["apple", "banana"]), "apple and banana")

    def test_multiple_items(self):
        """Test multiple item list."""
        self.assertEqual(format_list(
            ["apple", "banana", "orange"]), "apple, banana, and orange")

    def test_custom_conjunction(self):
        """Test custom conjunction."""
        self.assertEqual(format_list(
            ["apple", "banana", "orange"], conjunction="or"), "apple, banana, or orange")

    def test_without_oxford_comma(self):
        """Test without Oxford comma."""
        self.assertEqual(format_list(
            ["apple", "banana", "orange"], oxford_comma=False), "apple, banana and orange")


class TestCleanText(unittest.TestCase):
    """Tests for the clean_text function."""

    def test_whitespace_cleanup(self):
        """Test whitespace cleanup."""
        self.assertEqual(clean_text("  Hello  world  "), "Hello world")
        self.assertEqual(clean_text("\n\tHello\n\tworld\n"), "Hello world")

    def test_no_strip(self):
        """Test without stripping."""
        self.assertEqual(clean_text("  Hello  world  ",
                         strip=False), "  Hello world  ")

    def test_lowercase(self):
        """Test lowercase conversion."""
        self.assertEqual(clean_text("Hello World", lower=True), "hello world")
        self.assertEqual(clean_text(
            "Hello World", strip=False, lower=True), "hello world")

    def test_empty_input(self):
        """Test empty input."""
        self.assertEqual(clean_text(""), "")
        self.assertEqual(clean_text(None), "")


class TestCapitaliseFirst(unittest.TestCase):
    """Tests for the capitalise_first function."""

    def test_capitalise_first(self):
        """Test capitalising the first letter."""
        self.assertEqual(capitalise_first("hello"), "Hello")
        self.assertEqual(capitalise_first("hello world"), "Hello world")

    def test_already_capitalised(self):
        """Test already capitalised text."""
        self.assertEqual(capitalise_first("Hello"), "Hello")

    def test_empty_string(self):
        """Test empty string."""
        self.assertEqual(capitalise_first(""), "")
        self.assertEqual(capitalise_first(None), "")

    def test_single_character(self):
        """Test single character."""
        self.assertEqual(capitalise_first("a"), "A")


class TestCapitaliseWords(unittest.TestCase):
    """Tests for the capitalise_words function."""

    def test_capitalise_words(self):
        """Test capitalising all words."""
        self.assertEqual(capitalise_words("hello world"), "Hello World")

    def test_with_exceptions(self):
        """Test with exception words."""
        self.assertEqual(capitalise_words(
            "hello the world"), "Hello the World")
        # First word should be capitalised even if in exceptions
        self.assertEqual(capitalise_words(
            "the hello world"), "The Hello World")

    def test_custom_exceptions(self):
        """Test custom exceptions."""
        self.assertEqual(capitalise_words("hello the world",
                         exceptions=["world"]), "Hello The world")

    def test_empty_string(self):
        """Test empty string."""
        self.assertEqual(capitalise_words(""), "")
        self.assertEqual(capitalise_words(None), "")


class TestFormatTwitchMessage(unittest.TestCase):
    """Tests for the format_twitch_message function."""

    def test_basic_message(self):
        """Test basic message formatting."""
        self.assertEqual(format_twitch_message("Hello world"), "Hello world")

    def test_empty_message(self):
        """Test empty message."""
        self.assertEqual(format_twitch_message(""), "")
        self.assertEqual(format_twitch_message(None), "")

    def test_action_message(self):
        """Test action message."""
        self.assertEqual(format_twitch_message(
            "waves hello", is_action=True), "* waves hello")

    def test_with_badges(self):
        """Test message with badges."""
        badges = {"broadcaster": "1", "moderator": "1"}
        self.assertEqual(format_twitch_message(
            "Hello", badges=badges), "📹 🔧 Hello")

    def test_with_emotes(self):
        """Test message with emotes."""
        emotes = {"Kappa": ["0-5"]}
        # Emotes shouldn't affect the message text in this function
        self.assertEqual(format_twitch_message(
            "Hello", emotes=emotes), "Hello")

    def test_with_badges_and_action(self):
        """Test message with badges and action."""
        badges = {"subscriber": "1"}
        self.assertEqual(format_twitch_message(
            "waves", badges=badges, is_action=True), "✓ * waves")


class TestFormatTwitchCommand(unittest.TestCase):
    """Tests for the format_twitch_command function."""

    def test_basic_command(self):
        """Test basic command formatting."""
        self.assertEqual(format_twitch_command("help"), "!help")

    def test_command_with_args(self):
        """Test command with arguments."""
        self.assertEqual(format_twitch_command(
            "give", ["user", "100"]), "!give user 100")

    def test_empty_command(self):
        """Test empty command."""
        self.assertEqual(format_twitch_command(""), "!")

    def test_custom_prefix(self):
        """Test custom prefix."""
        self.assertEqual(format_twitch_command("help", prefix="?"), "?help")
        self.assertEqual(format_twitch_command(
            "give", ["user", "100"], prefix="?"), "?give user 100")


class TestFormatTimeElapsed(unittest.TestCase):
    """Tests for the format_time_elapsed function."""

    def test_seconds(self):
        """Test formatting seconds."""
        self.assertEqual(format_time_elapsed(30), "30 seconds")
        self.assertEqual(format_time_elapsed(1), "1 second")

    def test_minutes(self):
        """Test formatting minutes."""
        self.assertEqual(format_time_elapsed(90), "1 minute and 30 seconds")
        self.assertEqual(format_time_elapsed(60), "1 minute")

    def test_hours(self):
        """Test formatting hours."""
        self.assertEqual(format_time_elapsed(3600), "1 hour")
        self.assertEqual(format_time_elapsed(
            3661), "1 hour, 1 minute and 1 second")

    def test_days(self):
        """Test formatting days."""
        self.assertEqual(format_time_elapsed(86400), "1 day")
        self.assertEqual(format_time_elapsed(90061),
                         "1 day, 1 hour, 1 minute and 1 second")

    def test_without_seconds(self):
        """Test without seconds."""
        self.assertEqual(format_time_elapsed(
            90, include_seconds=False), "1 minute")
        self.assertEqual(format_time_elapsed(
            3661, include_seconds=False), "1 hour and 1 minute")

    def test_negative_time(self):
        """Test negative time."""
        self.assertEqual(format_time_elapsed(-10), "0 seconds")

    def test_timedelta_input(self):
        """Test timedelta input."""
        self.assertEqual(format_time_elapsed(
            timedelta(seconds=90)), "1 minute and 30 seconds")


class TestFormatTimestampForHumans(unittest.TestCase):
    """Tests for the format_timestamp_for_humans function."""

    def test_datetime_formatting(self):
        """Test datetime formatting."""
        dt = datetime(2023, 1, 1, 12, 30, 45)
        self.assertEqual(format_timestamp_for_humans(dt),
                         "2023-01-01 12:30:45")

    def test_timestamp_formatting(self):
        """Test timestamp formatting."""
        # 2023-01-01 12:30:45 UTC
        timestamp = 1672576245  # Correct UTC timestamp for 2023-01-01 12:30:45
        self.assertEqual(format_timestamp_for_humans(
            timestamp), "2023-01-01 12:30:45")

    def test_custom_format(self):
        """Test custom format."""
        dt = datetime(2023, 1, 1, 12, 30, 45)
        self.assertEqual(format_timestamp_for_humans(
            dt, format_str="%d/%m/%Y"), "01/01/2023")


class TestFormatBytes(unittest.TestCase):
    """Tests for the format_bytes function."""

    def test_bytes(self):
        """Test bytes formatting."""
        self.assertEqual(format_bytes(500), "500 bytes")
        self.assertEqual(format_bytes(1), "1 bytes")

    def test_kilobytes(self):
        """Test kilobytes formatting."""
        self.assertEqual(format_bytes(1024), "1.00 KB")
        self.assertEqual(format_bytes(1536), "1.50 KB")

    def test_megabytes(self):
        """Test megabytes formatting."""
        self.assertEqual(format_bytes(1048576), "1.00 MB")
        self.assertEqual(format_bytes(1572864), "1.50 MB")

    def test_gigabytes(self):
        """Test gigabytes formatting."""
        self.assertEqual(format_bytes(1073741824), "1.00 GB")

    def test_decimal_places(self):
        """Test custom decimal places."""
        self.assertEqual(format_bytes(1572864, decimal_places=1), "1.5 MB")
        self.assertEqual(format_bytes(1572864, decimal_places=3), "1.500 MB")

    def test_negative_value(self):
        """Test negative value."""
        self.assertEqual(format_bytes(-100), "0 bytes")


class TestStripHtmlTags(unittest.TestCase):
    """Tests for the strip_html_tags function."""

    def test_strip_tags(self):
        """Test stripping HTML tags."""
        self.assertEqual(strip_html_tags("<p>Hello</p>"), "Hello")
        self.assertEqual(strip_html_tags("<a href='#'>Link</a>"), "Link")
        self.assertEqual(strip_html_tags(
            "<div><span>Nested</span></div>"), "Nested")

    def test_complex_html(self):
        """Test complex HTML."""
        html = "<div class='container'><h1>Title</h1><p>Paragraph with <b>bold</b> text.</p></div>"
        self.assertEqual(strip_html_tags(
            html), "TitleParagraph with bold text.")

    def test_empty_input(self):
        """Test empty input."""
        self.assertEqual(strip_html_tags(""), "")
        self.assertEqual(strip_html_tags(None), "")

    def test_no_tags(self):
        """Test input without tags."""
        self.assertEqual(strip_html_tags("Hello world"), "Hello world")


class TestEscapeMarkdown(unittest.TestCase):
    """Tests for the escape_markdown function."""

    def test_escape_characters(self):
        """Test escaping Markdown characters."""
        self.assertEqual(escape_markdown("*bold*"), "\\*bold\\*")
        self.assertEqual(escape_markdown("_italic_"), "\\_italic\\_")
        self.assertEqual(escape_markdown("`code`"), "\\`code\\`")
        self.assertEqual(escape_markdown("[link](url)"), "\\[link\\]\\(url\\)")

    def test_multiple_characters(self):
        """Test escaping multiple characters."""
        self.assertEqual(escape_markdown("*bold* and _italic_"),
                         "\\*bold\\* and \\_italic\\_")

    def test_empty_input(self):
        """Test empty input."""
        self.assertEqual(escape_markdown(""), "")
        self.assertEqual(escape_markdown(None), "")


class TestFormatException(unittest.TestCase):
    """Tests for the format_exception function."""

    def test_format_exception(self):
        """Test formatting exceptions."""
        try:
            raise ValueError("Test error")
        except Exception as e:
            self.assertEqual(format_exception(e), "ValueError: Test error")

    def test_custom_exception(self):
        """Test formatting custom exceptions."""
        class CustomError(Exception):
            pass

        try:
            raise CustomError("Custom error message")
        except Exception as e:
            self.assertEqual(format_exception(
                e), "CustomError: Custom error message")


class TestFormatJson(unittest.TestCase):
    """Tests for the format_json function."""

    def test_simple_dict(self):
        """Test formatting a simple dictionary."""
        obj = {"name": "Test", "value": 123}
        expected = '{\n  "name": "Test",\n  "value": 123\n}'
        self.assertEqual(format_json(obj), expected)

    def test_nested_dict(self):
        """Test formatting a nested dictionary."""
        obj = {"user": {"name": "Test", "id": 123}, "active": True}
        expected = '{\n  "active": true,\n  "user": {\n    "id": 123,\n    "name": "Test"\n  }\n}'
        self.assertEqual(format_json(obj), expected)

    def test_custom_indent(self):
        """Test custom indentation."""
        obj = {"name": "Test", "value": 123}
        expected = '{\n    "name": "Test",\n    "value": 123\n}'
        self.assertEqual(format_json(obj, indent=4), expected)

    def test_no_sort_keys(self):
        """Test without sorting keys."""
        obj = {"b": 2, "a": 1}
        expected = '{\n  "b": 2,\n  "a": 1\n}'
        self.assertEqual(format_json(obj, sort_keys=False), expected)

    def test_unicode_characters(self):
        """Test formatting with Unicode characters."""
        obj = {"name": "Café", "currency": "£"}
        expected = '{\n  "currency": "£",\n  "name": "Café"\n}'
        self.assertEqual(format_json(obj), expected)


if __name__ == "__main__":
    unittest.main()
