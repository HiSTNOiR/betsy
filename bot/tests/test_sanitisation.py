"""
Tests for the sanitisation utility module.
"""
import unittest
from bot.utils.sanitisation import (
    sanitise_input, sanitise_path, sanitise_username,
    sanitise_command_args, sanitise_for_db, 
    strip_twitch_emotes, sanitise_html,
    remove_non_alphanumeric, clean_numeric_string
)

class TestSanitisation(unittest.TestCase):
    """Tests for sanitisation utility functions."""
    
    def test_sanitise_input(self):
        """Test input sanitisation."""
        # Normal text
        self.assertEqual(sanitise_input("Hello, world!"), "Hello, world!")
        
        # HTML/script injection
        self.assertEqual(
            sanitise_input("<script>alert('XSS')</script>"),
            "&lt;script&gt;alert(&#x27;XSS&#x27;)&lt;/script&gt;"
        )
        
        # HTML entities
        self.assertEqual(
            sanitise_input("<b>Bold</b> & <i>Italic</i>"),
            "&lt;b&gt;Bold&lt;/b&gt; &amp; &lt;i&gt;Italic&lt;/i&gt;"
        )
        
        # Empty string
        self.assertEqual(sanitise_input(""), "")
    
    def test_sanitise_path(self):
        """Test path sanitisation."""
        # Basic path
        self.assertEqual(sanitise_path("/path/to/file"), "/path/to/file")
        
        # Path with directory traversal
        self.assertEqual(sanitise_path("/path/../to/file"), "/path/to/file")
        self.assertEqual(sanitise_path("/path/../../to/file"), "/path/to/file")
        
        # Path with double dots in name
        self.assertEqual(sanitise_path("/path/to..file"), "/path/to..file")

    def test_sanitise_username(self):
        """Test username sanitisation."""
        # Normal username
        self.assertEqual(sanitise_username("user123"), "user123")
        
        # Username with @ symbol
        self.assertEqual(sanitise_username("@user123"), "user123")
        
        # Username with special characters
        self.assertEqual(sanitise_username("user-123"), "user123")
        self.assertEqual(sanitise_username("user@123"), "user123")
        self.assertEqual(sanitise_username("user 123"), "user123")
        
        # Mixed case
        self.assertEqual(sanitise_username("UsEr123"), "user123")
        
        # With whitespace
        self.assertEqual(sanitise_username(" user123 "), "user123")
        
        # Empty string
        self.assertEqual(sanitise_username(""), "")
    
    def test_sanitise_command_args(self):
        """Test command arguments sanitisation."""
        # Normal args
        self.assertEqual(sanitise_command_args("arg1 arg2"), "arg1 arg2")
        
        # With whitespace
        self.assertEqual(sanitise_command_args(" arg1  arg2 "), "arg1  arg2")
        
        # Special characters (not sanitised in this simple implementation)
        self.assertEqual(sanitise_command_args("arg1 @arg2!"), "arg1 @arg2!")
        
        # Empty string
        self.assertEqual(sanitise_command_args(""), "")
    
    def test_sanitise_for_db(self):
        """Test database sanitisation."""
        # Normal text
        self.assertEqual(sanitise_for_db("Hello, world!"), "Hello, world!")
        
        # SQL injection attempt
        self.assertEqual(
            sanitise_for_db("Robert'); DROP TABLE Students;--"),
            "Robert''); DROP TABLE Students--"
        )
        
        # Single quotes
        self.assertEqual(sanitise_for_db("It's a test"), "It''s a test")
        
        # Semicolons
        self.assertEqual(sanitise_for_db("cmd1;cmd2;cmd3"), "cmd1cmd2cmd3")
        
        # Empty string
        self.assertEqual(sanitise_for_db(""), "")
    
    def test_strip_twitch_emotes(self):
        """Test Twitch emote stripping."""
        # Text with emotes
        self.assertEqual(
            strip_twitch_emotes("Hello :kappa: world :pogchamp:"),
            "Hello world"
        )
        
        # Multiple consecutive emotes
        self.assertEqual(
            strip_twitch_emotes(":kappa::pogchamp::biblethump:"),
            "  "
        )
        
        # No emotes
        self.assertEqual(strip_twitch_emotes("Hello, world!"), "Hello, world!")
        
        # Empty string
        self.assertEqual(strip_twitch_emotes(""), "")
    
    def test_sanitise_html(self):
        """Test HTML sanitisation."""
        # Simple HTML
        self.assertEqual(
            sanitise_html("<p>Hello, world!</p>"),
            "Hello, world!"
        )
        
        # Allowed tags
        self.assertEqual(
            sanitise_html("Hello, <b>bold</b> and <i>italic</i> world!"),
            "Hello, <b>bold</b> and <i>italic</i> world!"
        )
        
        # Disallowed tags
        self.assertEqual(
            sanitise_html("<script>alert('XSS')</script>"),
            "alert('XSS')"
        )
        self.assertEqual(
            sanitise_html("<div><p>Content</p></div>"),
            "Content"
        )
        
        # Mixed allowed and disallowed
        self.assertEqual(
            sanitise_html("<div>Hello, <b>bold</b> and <script>alert()</script></div>"),
            "Hello, <b>bold</b> and alert()"
        )
        
        # Empty string
        self.assertEqual(sanitise_html(""), "")
    
    def test_remove_non_alphanumeric(self):
        """Test non-alphanumeric character removal."""
        # With special characters
        self.assertEqual(
            remove_non_alphanumeric("Hello, world! 123"),
            "Hello world 123"
        )
        
        # Without spaces
        self.assertEqual(
            remove_non_alphanumeric("Hello,world!123", allow_spaces=False),
            "Helloworld123"
        )
        
        # Only special characters
        self.assertEqual(remove_non_alphanumeric("!@#$%^&*()"), "")
        
        # Empty string
        self.assertEqual(remove_non_alphanumeric(""), "")
    
    def test_clean_numeric_string(self):
        """Test numeric string cleaning."""
        # Already numeric
        self.assertEqual(clean_numeric_string("12345"), "12345")
        
        # Mixed characters
        self.assertEqual(clean_numeric_string("a1b2c3d4e5"), "12345")
        
        # Special characters
        self.assertEqual(clean_numeric_string("$1,234.56"), "123456")
        
        # No numeric characters
        self.assertEqual(clean_numeric_string("abcde"), "")
        
        # Empty string
        self.assertEqual(clean_numeric_string(""), "")

if __name__ == '__main__':
    unittest.main()