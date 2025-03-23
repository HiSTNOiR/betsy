"""
Tests for the validation utility module.
"""
import unittest
from bot.utils.validation import (
    validate_boolean, validate_port, validate_username,
    validate_command, validate_integer, validate_contains_emoji,
    validate_contains_only_numbers, validate_points, validate_item_name,
    validate_user_input
)
from bot.core.errors import ValidationError

class TestValidation(unittest.TestCase):
    """Tests for validation utility functions."""
    
    def test_validate_boolean(self):
        """Test boolean validation."""
        # True values
        self.assertTrue(validate_boolean(True))
        self.assertTrue(validate_boolean('True'))
        self.assertTrue(validate_boolean('true'))
        self.assertTrue(validate_boolean('t'))
        self.assertTrue(validate_boolean('yes'))
        self.assertTrue(validate_boolean('y'))
        self.assertTrue(validate_boolean('1'))
        self.assertTrue(validate_boolean('on'))
        
        # False values
        self.assertFalse(validate_boolean(False))
        self.assertFalse(validate_boolean('False'))
        self.assertFalse(validate_boolean('false'))
        self.assertFalse(validate_boolean('f'))
        self.assertFalse(validate_boolean('no'))
        self.assertFalse(validate_boolean('n'))
        self.assertFalse(validate_boolean('0'))
        self.assertFalse(validate_boolean('off'))
        
        # Invalid values
        with self.assertRaises(ValueError):
            validate_boolean('invalid')
        with self.assertRaises(ValueError):
            validate_boolean(None)
        with self.assertRaises(ValueError):
            validate_boolean(42)
    
    def test_validate_port(self):
        """Test port validation."""
        # Valid ports
        self.assertEqual(validate_port(1), 1)
        self.assertEqual(validate_port(80), 80)
        self.assertEqual(validate_port(8080), 8080)
        self.assertEqual(validate_port(65535), 65535)
        self.assertEqual(validate_port('1'), 1)
        self.assertEqual(validate_port('80'), 80)
        self.assertEqual(validate_port('8080'), 8080)
        self.assertEqual(validate_port('65535'), 65535)
        
        # Invalid ports
        with self.assertRaises(ValueError):
            validate_port(0)
        with self.assertRaises(ValueError):
            validate_port(65536)
        with self.assertRaises(ValueError):
            validate_port(-1)
        with self.assertRaises(ValueError):
            validate_port('0')
        with self.assertRaises(ValueError):
            validate_port('65536')
        with self.assertRaises(ValueError):
            validate_port('-1')
        with self.assertRaises(ValueError):
            validate_port('invalid')
        with self.assertRaises(ValueError):
            validate_port(None)
    
    def test_validate_username(self):
        """Test username validation."""
        # Valid usernames
        self.assertEqual(validate_username('test'), 'test')
        self.assertEqual(validate_username('user123'), 'user123')
        self.assertEqual(validate_username('test_user'), 'test_user')
        self.assertEqual(validate_username('a' * 25), 'a' * 25)  # Max length
        self.assertEqual(validate_username('abcd'), 'abcd')  # Min length
        
        # Invalid usernames
        with self.assertRaises(ValidationError):
            validate_username('')
        with self.assertRaises(ValidationError):
            validate_username('abc')  # Too short
        with self.assertRaises(ValidationError):
            validate_username('a' * 26)  # Too long
        with self.assertRaises(ValidationError):
            validate_username('user-123')  # Invalid character
        with self.assertRaises(ValidationError):
            validate_username('user 123')  # Space not allowed
        with self.assertRaises(ValidationError):
            validate_username('user@123')  # Special char not allowed
    
    def test_validate_command(self):
        """Test command validation."""
        # Valid commands
        self.assertEqual(validate_command('test'), 'test')
        self.assertEqual(validate_command('cmd123'), 'cmd123')
        self.assertEqual(validate_command('test_cmd'), 'test_cmd')
        
        # Commands with prefix
        self.assertEqual(validate_command('!test'), 'test')
        
        # Invalid commands
        with self.assertRaises(ValidationError):
            validate_command('')
        with self.assertRaises(ValidationError):
            validate_command('!')  # Just prefix
        with self.assertRaises(ValidationError):
            validate_command('test-cmd')  # Invalid character
        with self.assertRaises(ValidationError):
            validate_command('test cmd')  # Space not allowed
        with self.assertRaises(ValidationError):
            validate_command('test@cmd')  # Special char not allowed
    
    def test_validate_integer(self):
        """Test integer validation."""
        # Valid integers
        self.assertEqual(validate_integer(42), 42)
        self.assertEqual(validate_integer('42'), 42)
        self.assertEqual(validate_integer(-42), -42)
        self.assertEqual(validate_integer('-42'), -42)
        self.assertEqual(validate_integer(0), 0)
        self.assertEqual(validate_integer('0'), 0)
        
        # With range constraints
        self.assertEqual(validate_integer(5, min_value=0, max_value=10), 5)
        self.assertEqual(validate_integer(0, min_value=0, max_value=10), 0)
        self.assertEqual(validate_integer(10, min_value=0, max_value=10), 10)
        
        # Out of range
        with self.assertRaises(ValueError):
            validate_integer(-1, min_value=0)
        with self.assertRaises(ValueError):
            validate_integer(11, max_value=10)
        with self.assertRaises(ValueError):
            validate_integer(5, min_value=10, max_value=20)
        
        # Invalid integers
        with self.assertRaises(ValueError):
            validate_integer('invalid')
        with self.assertRaises(ValueError):
            validate_integer(None)
        with self.assertRaises(ValueError):
            validate_integer(3.14)
        with self.assertRaises(ValueError):
            validate_integer('3.14')
    
    def test_validate_contains_emoji(self):
        """Test emoji detection."""
        # Contains emoji
        self.assertTrue(validate_contains_emoji('Hello 😊'))
        self.assertTrue(validate_contains_emoji('🎮 Gaming'))
        self.assertTrue(validate_contains_emoji('🔥🔥🔥'))
        
        # No emoji
        self.assertFalse(validate_contains_emoji('Hello world'))
        self.assertFalse(validate_contains_emoji('Test 123'))
        self.assertFalse(validate_contains_emoji(''))
    
    def test_validate_contains_only_numbers(self):
        """Test numbers-only validation."""
        # Only numbers
        self.assertTrue(validate_contains_only_numbers('123'))
        self.assertTrue(validate_contains_only_numbers('0'))
        self.assertTrue(validate_contains_only_numbers('42'))
        
        # Not only numbers
        self.assertFalse(validate_contains_only_numbers('123a'))
        self.assertFalse(validate_contains_only_numbers('a123'))
        self.assertFalse(validate_contains_only_numbers('1.23'))
        self.assertFalse(validate_contains_only_numbers('-123'))
        self.assertFalse(validate_contains_only_numbers(''))
    
    def test_validate_points(self):
        """Test points validation."""
        # Valid points
        self.assertEqual(validate_points(0), 0)
        self.assertEqual(validate_points(42), 42)
        self.assertEqual(validate_points('0'), 0)
        self.assertEqual(validate_points('42'), 42)
        
        # Invalid points
        with self.assertRaises(ValueError):
            validate_points(-1)
        with self.assertRaises(ValueError):
            validate_points('-1')
        with self.assertRaises(ValueError):
            validate_points('invalid')
        with self.assertRaises(ValueError):
            validate_points(None)
        with self.assertRaises(ValueError):
            validate_points(3.14)
    
    def test_validate_item_name(self):
        """Test item name validation."""
        # Valid item names
        self.assertEqual(validate_item_name('Test Item'), 'Test Item')
        self.assertEqual(validate_item_name('item123'), 'item123')
        self.assertEqual(validate_item_name('Special Item!'), 'Special Item!')
        
        # Invalid item names
        with self.assertRaises(ValidationError):
            validate_item_name('')
    
    def test_validate_user_input(self):
        """Test user input validation."""
        # Valid input
        self.assertEqual(validate_user_input('Test input'), 'Test input')
        self.assertEqual(validate_user_input('abc123'), 'abc123')
        self.assertEqual(validate_user_input('test_input'), 'test_input')
        self.assertEqual(validate_user_input('test-input'), 'test-input')
        
        # Empty input
        self.assertEqual(validate_user_input(''), '')
        
        # Invalid input
        with self.assertRaises(ValidationError):
            validate_user_input('test@input')
        with self.assertRaises(ValidationError):
            validate_user_input('test$input')
        with self.assertRaises(ValidationError):
            validate_user_input('test!input')
        
        # Custom allowed chars
        self.assertEqual(validate_user_input('test@input', allowed_chars='a-zA-Z0-9_\\s\\-@'), 'test@input')
        self.assertEqual(validate_user_input('test!input', allowed_chars='a-zA-Z0-9_\\s\\-!'), 'test!input')

if __name__ == '__main__':
    unittest.main()