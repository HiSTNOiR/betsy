"""
Tests for the security utility module.
"""
import unittest
import re
import os
from unittest.mock import patch
import base64
import secrets
import hashlib

from bot.utils.security import (
    generate_secure_token, hash_password, verify_password,
    is_valid_oauth_token, mask_sensitive_data,
    is_safe_string, rate_limit_key
)

class TestSecurity(unittest.TestCase):
    """Tests for security utility functions."""
    
    @patch('secrets.token_bytes')
    def test_generate_secure_token(self, mock_token_bytes):
        """Test secure token generation."""
        # Mock token bytes
        mock_token_bytes.return_value = b'test_token_bytes'
        
        # Generate token
        token = generate_secure_token()
        
        # Default length is 32
        mock_token_bytes.assert_called_with(32)
        
        # Should be base64 encoded
        self.assertEqual(token, base64.urlsafe_b64encode(b'test_token_bytes').decode('utf-8').rstrip('='))
        
        # Custom length
        token = generate_secure_token(16)
        mock_token_bytes.assert_called_with(16)
    
    @patch('secrets.token_hex')
    def test_hash_password(self, mock_token_hex):
        """Test password hashing."""
        # Mock salt generation
        mock_token_hex.return_value = "testsalt"
        
        # Hash with generated salt
        hash_val, salt = hash_password("testpassword")
        mock_token_hex.assert_called_with(16)
        self.assertEqual(salt, "testsalt")
        
        # Verify hash is correct
        hash_obj = hashlib.sha256()
        hash_obj.update("testsalt".encode('utf-8'))
        hash_obj.update("testpassword".encode('utf-8'))
        expected_hash = hash_obj.hexdigest()
        self.assertEqual(hash_val, expected_hash)
        
        # Hash with provided salt
        hash_val, salt = hash_password("testpassword", "providedsalt")
        self.assertEqual(salt, "providedsalt")
        
        # Verify hash is correct
        hash_obj = hashlib.sha256()
        hash_obj.update("providedsalt".encode('utf-8'))
        hash_obj.update("testpassword".encode('utf-8'))
        expected_hash = hash_obj.hexdigest()
        self.assertEqual(hash_val, expected_hash)
    
    def test_verify_password(self):
        """Test password verification."""
        # Hash a password
        hash_val, salt = hash_password("testpassword")
        
        # Verify correct password
        self.assertTrue(verify_password("testpassword", hash_val, salt))
        
        # Verify incorrect password
        self.assertFalse(verify_password("wrongpassword", hash_val, salt))
    

    
    def test_is_valid_oauth_token(self):
        """Test OAuth token validation."""
        # Valid token format
        self.assertTrue(is_valid_oauth_token("oauth:1234567890abcdefghijklmnopqrstuvwxyz"))
        self.assertTrue(is_valid_oauth_token("1234567890abcdefghijklmnopqrstuvwxyz"))
        
        # Valid complex token
        self.assertTrue(is_valid_oauth_token("oauth:1234567890ABCDEF_-abcdefghijklmnopqrstuvwxyz"))
        
        # Invalid tokens
        self.assertFalse(is_valid_oauth_token("oauth:"))
        self.assertFalse(is_valid_oauth_token("oauth:abc"))  # Too short
        self.assertFalse(is_valid_oauth_token("1234$%^&*()"))  # Invalid characters
    
    def test_mask_sensitive_data(self):
        """Test sensitive data masking."""
        # OAuth token
        self.assertEqual(mask_sensitive_data("oauth:1234567890abcdef"), "oauth:***********")
        
        # Other token (show first few characters)
        self.assertEqual(mask_sensitive_data("1234567890abcdef"), "123*************")
        
        # Short token (should mask most)
        self.assertEqual(mask_sensitive_data("12345678"), "12******")
        
        # Empty string
        self.assertEqual(mask_sensitive_data(""), "")
    
    def test_is_safe_string(self):
        """Test safe string validation."""
        # Safe strings
        self.assertTrue(is_safe_string("Hello, world!"))
        self.assertTrue(is_safe_string("123 ABC"))
        self.assertTrue(is_safe_string("Test with @#$%^&*()_+-=[]{};:\"'<>,.?/\\|"))
        
        # Empty string
        self.assertTrue(is_safe_string(""))
        
        # Unsafe strings (if any)
        # Note: The current implementation considers most characters safe
    
    def test_rate_limit_key(self):
        """Test rate limit key generation."""
        # Basic key
        self.assertEqual(rate_limit_key("user123", "command"), "user123:command")
        
        # Complex key
        self.assertEqual(rate_limit_key("user with spaces", "complex!command"), "user with spaces:complex!command")
        
        # Empty values
        self.assertEqual(rate_limit_key("", ""), ":")

if __name__ == '__main__':
    unittest.main()