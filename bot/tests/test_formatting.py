"""
Tests for the formatting utility module.
"""
import unittest
from bot.utils.formatting import (
    format_points, format_username, format_command,
    format_item_name, pluralise, format_list,
    truncate, normalise_name, format_chat_message
)

class TestFormatting(unittest.TestCase):
    """Tests for formatting utility functions."""
    
    def test_format_points(self):
        """Test points formatting."""
        # Basic formatting
        self.assertEqual(format_points(0), '0')
        self.assertEqual(format_points(123), '123')
        self.assertEqual(format_points(1234), '1,234')
        self.assertEqual(format_points(1234567), '1,234,567')
        
        # String input
        self.assertEqual(format_points('0'), '0')
        self.assertEqual(format_points('123'), '123')
        self.assertEqual(format_points('1234'), '1,234')
        
        # Invalid input
        self.assertEqual(format_points('invalid'), 'invalid')
        
        # Abbreviation
        self.assertEqual(format_points(1234, abbreviate=True), '1.2K')
        self.assertEqual(format_points(1234567, abbreviate=True), '1.2M')
        self.assertEqual(format_points(1234567890, abbreviate=True), '1.2B')
        self.assertEqual(format_points(123, abbreviate=True), '123')
    
    def test_format_username(self):
        """Test username formatting."""
        # Normal username
        self.assertEqual(format_username('user'), 'user')
        
        # Uppercase
        self.assertEqual(format_username('USER'), 'user')
        
        # Mixed case
        self.assertEqual(format_username('UsEr'), 'user')
        
        # With @ symbol
        self.assertEqual(format_username('@user'), 'user')
        
        # With spaces
        self.assertEqual(format_username(' user '), 'user')
        
        # Empty input
        self.assertEqual(format_username(''), '')
    
    def test_format_command(self):
        """Test command formatting."""
        # Normal command
        self.assertEqual(format_command('command'), '!command')
        
        # Already has prefix
        self.assertEqual(format_command('!command'), '!command')
        
        # Uppercase
        self.assertEqual(format_command('COMMAND'), '!command')
        
        # Mixed case
        self.assertEqual(format_command('CoMmAnD'), '!command')
        
        # With spaces
        self.assertEqual(format_command(' command '), '!command')
        
        # Empty input
        self.assertEqual(format_command(''), '!')
        
        # Custom prefix
        self.assertEqual(format_command('command', prefix='?'), '?command')
    
    def test_format_item_name(self):
        """Test item name formatting."""
        # Single word
        self.assertEqual(format_item_name('sword'), 'Sword')
        
        # Multiple words
        self.assertEqual(format_item_name('rusty dagger'), 'Rusty Dagger')
        
        # Already capitalised
        self.assertEqual(format_item_name('Rusty Dagger'), 'Rusty Dagger')
        
        # Mixed case
        self.assertEqual(format_item_name('rUsTy DaGgEr'), 'Rusty Dagger')
        
        # With extra spaces
        self.assertEqual(format_item_name(' rusty  dagger '), 'Rusty Dagger')
        
        # Empty input
        self.assertEqual(format_item_name(''), '')
    
    def test_pluralise(self):
        """Test pluralisation."""
        # Regular noun, singular
        self.assertEqual(pluralise('apple', 1), 'apple')
        
        # Regular noun, plural
        self.assertEqual(pluralise('apple', 2), 'apples')
        self.assertEqual(pluralise('apple', 0), 'apples')
        
        # Noun ending in 's', singular
        self.assertEqual(pluralise('bus', 1), 'bus')
        
        # Noun ending in 's', plural
        self.assertEqual(pluralise('bus', 2), 'buses')
        
        # Noun ending in 'x', plural
        self.assertEqual(pluralise('box', 2), 'boxes')
        
        # Noun ending in 'ch', plural
        self.assertEqual(pluralise('witch', 2), 'witches')
        
        # Noun ending in 'y' (consonant + y), plural
        self.assertEqual(pluralise('berry', 2), 'berries')
        
        # Noun ending in 'y' (vowel + y), plural
        self.assertEqual(pluralise('toy', 2), 'toys')
    
    def test_format_list(self):
        """Test list formatting."""
        # Empty list
        self.assertEqual(format_list([]), '')
        
        # Single item
        self.assertEqual(format_list(['apple']), 'apple')
        
        # Two items
        self.assertEqual(format_list(['apple', 'banana']), 'apple and banana')
        
        # Three items
        self.assertEqual(format_list(['apple', 'banana', 'orange']), 'apple, banana, and orange')
        
        # Custom conjunction
        self.assertEqual(format_list(['apple', 'banana'], conjunction='or'), 'apple or banana')
        self.assertEqual(format_list(['apple', 'banana', 'orange'], conjunction='or'), 'apple, banana, or orange')
    
    def test_truncate(self):
        """Test text truncation."""
        # Short text (no truncation)
        self.assertEqual(truncate('Hello, world!', 20), 'Hello, world!')
        
        # Exact length (no truncation)
        self.assertEqual(truncate('Hello, world!', 13), 'Hello, world!')
        
        # Truncation needed
        self.assertEqual(truncate('Hello, world!', 10), 'Hello, ...')
        
        # Custom suffix
        self.assertEqual(truncate('Hello, world!', 10, suffix='---'), 'Hello, ---')
        
        # Very short max length
        self.assertEqual(truncate('Hello, world!', 3), '...')
        
        # Max length shorter than suffix
        self.assertEqual(truncate('Hello, world!', 2), '..')
        
        # Empty string
        self.assertEqual(truncate('', 10), '')
    
    def test_normalise_name(self):
        """Test name normalisation."""
        # Regular name
        self.assertEqual(normalise_name('Test Item'), 'testitem')
        
        # With special characters
        self.assertEqual(normalise_name('Test-Item!123'), 'testitem123')
        
        # Mixed case
        self.assertEqual(normalise_name('TeSt ItEm'), 'testitem')
        
        # Empty string
        self.assertEqual(normalise_name(''), '')
    
    def test_format_chat_message(self):
        """Test chat message formatting."""
        # Normal message
        self.assertEqual(format_chat_message('Hello, world!', 'user'), 'user: Hello, world!')
        
        # Action message
        self.assertEqual(format_chat_message('waves hello', 'user', is_action=True), '* user waves hello')
        
        # Empty message
        self.assertEqual(format_chat_message('', 'user'), 'user: ')

if __name__ == '__main__':
    unittest.main()