"""
Unit tests for the security utility module.

This module contains tests for the security utility functions provided by
bot.utils.security.
"""

import base64
import hashlib
import hmac
import os
import pytest
import re
from unittest import mock

from bot.utils.security import (
    generate_random_string,
    generate_token,
    hash_password,
    verify_password,
    generate_hmac,
    verify_hmac,
    sanitise_input,
    sanitise_filename,
    sanitise_path,
    is_safe_url,
    is_valid_twitch_username,
    is_safe_command,
    validate_twitch_token,
    encrypt_string,
    decrypt_string,
)


class TestRandomGenerators:
    """Tests for random string and token generators."""

    def test_generate_random_string_length(self):
        """Test that generate_random_string produces a string of the correct length."""
        for length in [1, 10, 32, 100]:
            result = generate_random_string(length)
            assert len(result) == length
            # Verify it's a string
            assert isinstance(result, str)

    def test_generate_random_string_character_sets(self):
        """Test that generate_random_string uses the correct character sets."""
        # Without special characters
        result = generate_random_string(1000)
        allowed_chars = set(
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        assert all(c in allowed_chars for c in result)

        # With special characters
        result = generate_random_string(1000, include_special=True)
        allowed_chars = set(
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
        assert all(c in allowed_chars for c in result)

    def test_generate_random_string_uniqueness(self):
        """Test that generate_random_string produces unique strings."""
        results = [generate_random_string(32) for _ in range(100)]
        assert len(set(results)) == 100  # All strings should be unique

    def test_generate_token_format(self):
        """Test that generate_token produces a base64 URL-safe string."""
        token = generate_token()
        # Check it's a string
        assert isinstance(token, str)
        # Check it only contains base64 URL-safe characters
        assert all(
            c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_" for c in token)

    def test_generate_token_length(self):
        """Test that generate_token produces a token of approximately the expected length."""
        # Base64 encoding: 4 characters per 3 bytes, but we strip padding
        for length in [16, 32, 64]:
            token = generate_token(length)
            # The length should be close to 4/3 of the input bytes but without padding
            # Ceiling division without padding
            expected_length = (length * 4 + 2) // 3
            # Allow for minor variations due to padding
            assert abs(len(token) - expected_length) <= 1

    def test_generate_token_uniqueness(self):
        """Test that generate_token produces unique tokens."""
        tokens = [generate_token() for _ in range(100)]
        assert len(set(tokens)) == 100  # All tokens should be unique


class TestPasswordHandling:
    """Tests for password hashing and verification."""

    def test_hash_password_with_auto_salt(self):
        """Test that hash_password generates a hash and salt when no salt is provided."""
        result = hash_password("mypassword")
        assert "hash" in result
        assert "salt" in result
        assert isinstance(result["hash"], str)
        assert isinstance(result["salt"], str)

    def test_hash_password_with_provided_salt(self):
        """Test that hash_password works correctly with a provided salt."""
        salt = os.urandom(32)
        salt_hex = salt.hex()

        # Test with bytes salt
        result1 = hash_password("mypassword", salt)
        assert result1["salt"] == salt_hex

        # Test with hex string salt
        result2 = hash_password("mypassword", salt_hex)
        assert result2["hash"] == result1["hash"]
        assert result2["salt"] == result1["salt"]

    def test_hash_password_consistency(self):
        """Test that hash_password produces consistent results with the same password and salt."""
        salt = os.urandom(32)
        result1 = hash_password("mypassword", salt)
        result2 = hash_password("mypassword", salt)
        assert result1["hash"] == result2["hash"]
        assert result1["salt"] == result2["salt"]

    def test_hash_password_different_passwords(self):
        """Test that hash_password produces different hashes for different passwords."""
        salt = os.urandom(32)
        result1 = hash_password("password1", salt)
        result2 = hash_password("password2", salt)
        assert result1["hash"] != result2["hash"]

    def test_verify_password_correct(self):
        """Test that verify_password returns True for correct passwords."""
        password = "mypassword"
        hashed = hash_password(password)
        assert verify_password(password, hashed["hash"], hashed["salt"])

    def test_verify_password_incorrect(self):
        """Test that verify_password returns False for incorrect passwords."""
        password = "mypassword"
        wrong_password = "wrongpassword"
        hashed = hash_password(password)
        assert not verify_password(
            wrong_password, hashed["hash"], hashed["salt"])


class TestHMAC:
    """Tests for HMAC generation and verification."""

    def test_generate_hmac(self):
        """Test that generate_hmac produces the expected result."""
        data = "my data"
        key = "my key"

        # Calculate expected HMAC manually
        expected_hmac = hmac.new(
            key.encode('utf-8'),
            data.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        assert generate_hmac(data, key) == expected_hmac

    def test_verify_hmac_correct(self):
        """Test that verify_hmac returns True for correct HMACs."""
        data = "my data"
        key = "my key"
        hmac_value = generate_hmac(data, key)
        assert verify_hmac(data, key, hmac_value)

    def test_verify_hmac_incorrect(self):
        """Test that verify_hmac returns False for incorrect HMACs."""
        data = "my data"
        wrong_data = "wrong data"
        key = "my key"
        hmac_value = generate_hmac(data, key)
        assert not verify_hmac(wrong_data, key, hmac_value)
        assert not verify_hmac(data, key, "wrong hmac")


class TestInputSanitisation:
    """Tests for input sanitisation functions."""

    def test_sanitise_input_default_chars(self):
        """Test that sanitise_input correctly filters input with default allowed characters."""
        # Safe input should not be modified
        safe_input = "This is a safe string with punctuation: 123!@#$%^&*()_+-=[]{}|;':\",./<>?"
        assert sanitise_input(safe_input) == safe_input

        # Unsafe characters should be removed
        unsafe_input = "Unsafe \u0000 characters \u2028 should \u2029 be \x01 removed"
        expected = "Unsafe  characters  should  be  removed"
        assert sanitise_input(unsafe_input) == expected

    def test_sanitise_input_custom_chars(self):
        """Test that sanitise_input correctly filters input with custom allowed characters."""
        allowed_chars = "abc123"
        input_str = "abcdef123456"
        expected = "abc123"
        assert sanitise_input(input_str, allowed_chars) == expected

    def test_sanitise_input_empty(self):
        """Test that sanitise_input handles empty input."""
        assert sanitise_input("") == ""
        assert sanitise_input(None) == ""

    def test_sanitise_filename(self):
        """Test that sanitise_filename correctly filters filenames."""
        # Safe filename should not be modified
        safe_filename = "safe_filename-123.txt"
        assert sanitise_filename(safe_filename) == safe_filename

        # Unsafe characters should be removed
        unsafe_filename = "unsafe/file:name*?.txt"
        expected = "unsafefilename.txt"
        assert sanitise_filename(unsafe_filename) == expected

        # Empty or dot-only filenames should be replaced
        assert sanitise_filename("") == "unnamed_file"
        assert sanitise_filename("...") == "unnamed_file"

    @mock.patch('pathlib.Path.resolve')
    def test_sanitise_path(self, mock_resolve):
        """Test that sanitise_path correctly sanitises paths."""
        # Setup mock
        mock_path = mock.MagicMock()
        mock_path.__str__.return_value = "/sanitised/path"
        mock_resolve.return_value = mock_path

        result = sanitise_path("/path/to/file")
        assert result == "/sanitised/path"

        # Test empty path
        assert sanitise_path("") == ""


class TestURLSafety:
    """Tests for URL safety checks."""

    def test_is_safe_url_valid(self):
        """Test that is_safe_url correctly identifies safe URLs."""
        safe_urls = [
            "http://example.com",
            "https://example.com/path",
            "https://example.com:8080/path?query=param",
            "wss://example.com/websocket",
            "ws://localhost:8080/socket",
        ]
        for url in safe_urls:
            assert is_safe_url(url)

    def test_is_safe_url_invalid(self):
        """Test that is_safe_url correctly identifies unsafe URLs."""
        unsafe_urls = [
            "file:///etc/passwd",
            "javascript:alert('xss')",
            "data:text/html;base64,PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4=",
            "http://example.com:/../etc/passwd",
            "http://example.com/javascript:alert('xss')",
            "http://:@example.com",
            "",
            None,
        ]
        for url in unsafe_urls:
            assert not is_safe_url(url)


class TestTwitchFunctions:
    """Tests for Twitch-related validation functions."""

    def test_is_valid_twitch_username_valid(self):
        """Test that is_valid_twitch_username correctly identifies valid usernames."""
        valid_usernames = [
            "user1234",
            "user_name",
            "a_very_long_username_123",
            "UPPERCASE_user_123",
        ]
        for username in valid_usernames:
            assert is_valid_twitch_username(username)

    def test_is_valid_twitch_username_invalid(self):
        """Test that is_valid_twitch_username correctly identifies invalid usernames."""
        invalid_usernames = [
            "",  # Empty
            "abc",  # Too short
            "a_very_long_username_that_exceeds_the_maximum_length",  # Too long
            "user-name",  # Contains invalid character
            "user name",  # Contains space
            "user@name",  # Contains invalid character
            None,  # None
        ]
        for username in invalid_usernames:
            assert not is_valid_twitch_username(username)

    def test_validate_twitch_token_valid(self):
        """Test that validate_twitch_token correctly identifies valid tokens."""
        valid_tokens = [
            "oauth:abcdefghijklmnopqrstuvwxyz123456789",
            "oauth:abcdefghijklmnopqrstuvwxyz_123456789",
        ]
        for token in valid_tokens:
            assert validate_twitch_token(token)

    def test_validate_twitch_token_invalid(self):
        """Test that validate_twitch_token correctly identifies invalid tokens."""
        invalid_tokens = [
            "",  # Empty
            "token",  # No oauth: prefix
            "oauth:token",  # Too short
            "oauth:token!@#",  # Invalid characters
            "oauth token",  # Contains space
            None,  # None
        ]
        for token in invalid_tokens:
            assert not validate_twitch_token(token)


class TestCommandSafety:
    """Tests for command safety checks."""

    def test_is_safe_command_valid(self):
        """Test that is_safe_command correctly identifies safe commands."""
        safe_commands = [
            "echo hello",
            "git status",
            "python script.py",
            "ls -la",
        ]
        for command in safe_commands:
            assert is_safe_command(command)

    def test_is_safe_command_invalid(self):
        """Test that is_safe_command correctly identifies unsafe commands."""
        unsafe_commands = [
            "",  # Empty
            "echo hello | grep world",  # Pipe
            "echo hello && rm -rf /",  # AND operator
            "echo hello; rm -rf /",  # Semicolon
            "echo `rm -rf /`",  # Backticks
            "echo $(rm -rf /)",  # Command substitution
            "echo $PATH",  # Variable expansion
            "echo 'hello' > file.txt",  # Redirection
            None,  # None
        ]
        for command in unsafe_commands:
            assert not is_safe_command(command)


class TestEncryption:
    """Tests for encryption and decryption functions."""

    def test_encrypt_decrypt_string(self):
        """Test that encrypt_string and decrypt_string work together correctly."""
        for text in ["hello world", "special chars: !@#$%^&*()", "unicode: ñáéíóú"]:
            for key in ["key1", "another key", "yet another key 123"]:
                encrypted = encrypt_string(text, key)
                decrypted = decrypt_string(encrypted, key)
                assert decrypted == text
                # Ensure encrypted is different from original
                assert encrypted != text
                # Ensure encrypted is base64
                try:
                    base64.b64decode(encrypted)
                except Exception:
                    pytest.fail("Encrypted string is not valid base64")

    def test_encrypt_string_wrong_key(self):
        """Test that decrypt_string with wrong key doesn't produce the original text."""
        text = "secret message"
        key = "correct key"
        wrong_key = "wrong key"

        encrypted = encrypt_string(text, key)
        decrypted = decrypt_string(encrypted, wrong_key)

        assert decrypted != text

    def test_encrypt_decrypt_empty(self):
        """Test encryption and decryption of empty strings."""
        key = "some key"
        assert decrypt_string(encrypt_string("", key), key) == ""
        assert encrypt_string("", key) == ""
        assert decrypt_string("", key) == ""
        assert encrypt_string(None, key) == ""
        assert decrypt_string(None, key) == ""

    def test_decrypt_invalid_base64(self):
        """Test that decrypt_string handles invalid base64 input."""
        with pytest.warns(None) as warnings:
            result = decrypt_string("not-base64", "key")
            assert result == ""

    def test_encrypt_decrypt_no_key(self):
        """Test encryption and decryption with empty key."""
        text = "some text"
        assert encrypt_string(text, "") == ""
        assert decrypt_string(encrypt_string(text, "key"), "") == ""
