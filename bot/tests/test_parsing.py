"""
Tests for the parsing utility module.
"""
import unittest
from bot.utils.parsing import (
    parse_command, parse_args, extract_user_and_amount,
    parse_key_value_pairs, extract_targets, safe_int_conversion,
    safe_float_conversion, safe_bool_conversion, parse_duration,
    parse_item_name, parse_bits_amount, extract_command_with_targets,
    is_valid_target_for_self, fuzzy_match_item
)

class TestParsing(unittest.TestCase):
    """Tests for parsing utility functions."""
    
    def test_parse_command(self):
        """Test command parsing."""
        # Normal command
        self.assertEqual(parse_command('!command arg1 arg2'), ('command', 'arg1 arg2'))
        
        # Command without arguments
        self.assertEqual(parse_command('!command'), ('command', ''))
        
        # Not a command (no prefix)
        self.assertEqual(parse_command('command arg1 arg2'), (None, 'command arg1 arg2'))
        
        # Just prefix
        self.assertEqual(parse_command('!'), ('', ''))
        
        # Empty string
        self.assertEqual(parse_command(''), (None, ''))
        
        # Custom prefix
        self.assertEqual(parse_command('?command arg1 arg2', prefix='?'), ('command', 'arg1 arg2'))
    
    def test_parse_args(self):
        """Test argument parsing."""
        # Simple arguments
        self.assertEqual(parse_args('arg1 arg2 arg3'), ['arg1', 'arg2', 'arg3'])
        
        # Quoted arguments
        self.assertEqual(parse_args('arg1 "arg2 with spaces" arg3'), ['arg1', 'arg2 with spaces', 'arg3'])
        
        # Mixed quotes
        self.assertEqual(parse_args("arg1 'arg2' \"arg3\""), ['arg1', 'arg2', 'arg3'])
        
        # Empty string
        self.assertEqual(parse_args(''), [])
        
        # Unbalanced quotes (fallback to simple splitting)
        self.assertEqual(parse_args('arg1 "arg2 arg3'), ['arg1', '"arg2', 'arg3'])
    
    def test_extract_user_and_amount(self):
        """Test user and amount extraction."""
        # Normal case
        self.assertEqual(extract_user_and_amount('user 100'), ('user', 100))
        
        # User with @ symbol
        self.assertEqual(extract_user_and_amount('@user 100'), ('user', 100))
        
        # Not enough arguments
        self.assertEqual(extract_user_and_amount('user'), (None, None))
        
        # Non-integer amount
        self.assertEqual(extract_user_and_amount('user abc'), ('user', None))
        
        # Negative amount
        self.assertEqual(extract_user_and_amount('user -100'), ('user', None))
        
        # Empty string
        self.assertEqual(extract_user_and_amount(''), (None, None))
    
    def test_parse_key_value_pairs(self):
        """Test key-value pair parsing."""
        # Normal case
        self.assertEqual(
            parse_key_value_pairs('key1=value1,key2=value2'),
            {'key1': 'value1', 'key2': 'value2'}
        )
        
        # With spaces
        self.assertEqual(
            parse_key_value_pairs('key1 = value1 , key2 = value2'),
            {'key1': 'value1', 'key2': 'value2'}
        )
        
        # Custom separator and delimiter
        self.assertEqual(
            parse_key_value_pairs('key1:value1;key2:value2', separator=':', delimiter=';'),
            {'key1': 'value1', 'key2': 'value2'}
        )
        
        # Missing separator in some pairs
        self.assertEqual(
            parse_key_value_pairs('key1=value1,key2,key3=value3'),
            {'key1': 'value1', 'key3': 'value3'}
        )
        
        # Empty string
        self.assertEqual(parse_key_value_pairs(''), {})
    
    def test_extract_targets(self):
        """Test target extraction."""
        # Normal case
        self.assertEqual(extract_targets('user1 user2 user3'), ['user1', 'user2', 'user3'])
        
        # Users with @ symbol
        self.assertEqual(extract_targets('@user1 @user2 @user3'), ['user1', 'user2', 'user3'])
        
        # Mixed
        self.assertEqual(extract_targets('user1 @user2 user3'), ['user1', 'user2', 'user3'])
        
        # Empty string
        self.assertEqual(extract_targets(''), [])
    
    def test_safe_int_conversion(self):
        """Test safe integer conversion."""
        # Valid integers
        self.assertEqual(safe_int_conversion(42), 42)
        self.assertEqual(safe_int_conversion('42'), 42)
        self.assertEqual(safe_int_conversion(-42), -42)
        self.assertEqual(safe_int_conversion('-42'), -42)
        
        # Invalid integers
        self.assertEqual(safe_int_conversion('not an int'), 0)
        self.assertEqual(safe_int_conversion(None), 0)
        self.assertEqual(safe_int_conversion(3.14), 3)
        
        # Custom default
        self.assertEqual(safe_int_conversion('not an int', default=42), 42)
    
    def test_safe_float_conversion(self):
        """Test safe float conversion."""
        # Valid floats
        self.assertEqual(safe_float_conversion(3.14), 3.14)
        self.assertEqual(safe_float_conversion('3.14'), 3.14)
        self.assertEqual(safe_float_conversion(-3.14), -3.14)
        self.assertEqual(safe_float_conversion('-3.14'), -3.14)
        
        # Integers as floats
        self.assertEqual(safe_float_conversion(42), 42.0)
        self.assertEqual(safe_float_conversion('42'), 42.0)
        
        # Invalid floats
        self.assertEqual(safe_float_conversion('not a float'), 0.0)
        self.assertEqual(safe_float_conversion(None), 0.0)
        
        # Custom default
        self.assertEqual(safe_float_conversion('not a float', default=3.14), 3.14)
    
    def test_safe_bool_conversion(self):
        """Test safe boolean conversion."""
        # Valid booleans
        self.assertEqual(safe_bool_conversion(True), True)
        self.assertEqual(safe_bool_conversion(False), False)
        
        # String representations
        self.assertEqual(safe_bool_conversion('true'), True)
        self.assertEqual(safe_bool_conversion('True'), True)
        self.assertEqual(safe_bool_conversion('yes'), True)
        self.assertEqual(safe_bool_conversion('y'), True)
        self.assertEqual(safe_bool_conversion('1'), True)
        self.assertEqual(safe_bool_conversion('on'), True)
        
        self.assertEqual(safe_bool_conversion('false'), False)
        self.assertEqual(safe_bool_conversion('False'), False)
        self.assertEqual(safe_bool_conversion('no'), False)
        self.assertEqual(safe_bool_conversion('n'), False)
        self.assertEqual(safe_bool_conversion('0'), False)
        self.assertEqual(safe_bool_conversion('off'), False)
        
        # Other values (use bool() conversion)
        self.assertEqual(safe_bool_conversion(1), True)
        self.assertEqual(safe_bool_conversion(0), False)
        self.assertEqual(safe_bool_conversion([]), False)
        self.assertEqual(safe_bool_conversion([1, 2]), True)
        
        # Invalid booleans
        self.assertEqual(safe_bool_conversion('not a bool'), True)  # Non-empty string is True
        self.assertEqual(safe_bool_conversion(None), False)
        
        # Custom default
        self.assertEqual(safe_bool_conversion(None, default=True), True)
    
    def test_parse_duration(self):
        """Test duration parsing."""
        # Simple durations
        self.assertEqual(parse_duration('30s'), 30)
        self.assertEqual(parse_duration('5m'), 300)
        self.assertEqual(parse_duration('2h'), 7200)
        self.assertEqual(parse_duration('1d'), 86400)
        
        # Combined durations
        self.assertEqual(parse_duration('1h30m'), 5400)
        self.assertEqual(parse_duration('1d2h30m15s'), 95415)
        
        # Plain integer (seconds)
        self.assertEqual(parse_duration('60'), 60)
        
        # Invalid format
        self.assertIsNone(parse_duration('not a duration'))
        
        # Empty string
        self.assertIsNone(parse_duration(''))
    
    def test_parse_item_name(self):
        """Test item name parsing."""
        # Normal case
        self.assertEqual(parse_item_name('Rusty Dagger'), 'Rusty Dagger')
        
        # With special characters
        self.assertEqual(parse_item_name('Rusty Dagger!'), 'Rusty Dagger')
        
        # With extra spaces
        self.assertEqual(parse_item_name(' Rusty  Dagger '), 'Rusty Dagger')
        
        # Empty string
        self.assertEqual(parse_item_name(''), '')
    
    def test_parse_bits_amount(self):
        """Test bits amount parsing."""
        # Normal case
        self.assertEqual(parse_bits_amount('cheer100'), 100)
        self.assertEqual(parse_bits_amount('Cheer1000'), 1000)
        
        # With surrounding text
        self.assertEqual(parse_bits_amount('Hello cheer50 world'), 50)
        
        # Multiple cheers (returns first)
        self.assertEqual(parse_bits_amount('cheer100 cheer200'), 100)
        
        # No bits
        self.assertIsNone(parse_bits_amount('Hello world'))
        
        # Invalid format
        self.assertIsNone(parse_bits_amount('cheerabc'))
        
        # Empty string
        self.assertIsNone(parse_bits_amount(''))
    
    def test_extract_command_with_targets(self):
        """Test command with targets extraction."""
        # Normal case
        self.assertEqual(
            extract_command_with_targets('!command @user1 @user2 arg1 arg2'),
            ('command', ['user1', 'user2'], 'arg1 arg2')
        )
        
        # No targets
        self.assertEqual(
            extract_command_with_targets('!command arg1 arg2'),
            ('command', [], 'arg1 arg2')
        )
        
        # Targets only
        self.assertEqual(
            extract_command_with_targets('!command @user1 @user2'),
            ('command', ['user1', 'user2'], '')
        )
        
        # Not a command
        self.assertEqual(
            extract_command_with_targets('text @user1 @user2'),
            (None, [], 'text @user1 @user2')
        )
        
        # Empty string
        self.assertEqual(
            extract_command_with_targets(''),
            (None, [], '')
        )
    
    def test_is_valid_target_for_self(self):
        """Test self-targeting validation."""
        # Different target and sender
        self.assertTrue(is_valid_target_for_self('target', 'sender'))
        
        # Same target and sender
        self.assertFalse(is_valid_target_for_self('sender', 'sender'))
        
        # With @ symbol
        self.assertFalse(is_valid_target_for_self('@sender', 'sender'))
        
        # Case insensitive
        self.assertFalse(is_valid_target_for_self('SENDER', 'sender'))
    
    def test_fuzzy_match_item(self):
        """Test fuzzy item matching."""
        items = ['Rusty Dagger', 'Iron Sword', 'Steel Shield', 'Leather Armor']
        
        # Exact match
        self.assertEqual(fuzzy_match_item('Rusty Dagger', items), 'Rusty Dagger')
        
        # Case insensitive
        self.assertEqual(fuzzy_match_item('rusty dagger', items), 'Rusty Dagger')
        
        # Prefix match
        self.assertEqual(fuzzy_match_item('iron', items), 'Iron Sword')
        
        # No match
        self.assertIsNone(fuzzy_match_item('golden', items))
        
        # Empty input
        self.assertIsNone(fuzzy_match_item('', items))
        
        # Empty item list
        self.assertIsNone(fuzzy_match_item('rusty', []))

if __name__ == '__main__':
    unittest.main()