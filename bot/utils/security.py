"""
Security-related utility functions for the bot.

This module provides utility functions for security operations such as
hashing, validation, and sanitisation.
"""

import base64
import hashlib
import hmac
import os
import re
import secrets
import string
from typing import Any, Dict, List, Optional, Union

import logging

# Set up logger for this module
logger = logging.getLogger(__name__)


def generate_random_string(length: int = 32, include_special: bool = False) -> str:
    """
    Generate a cryptographically secure random string.

    Args:
        length (int): Length of the random string.
        include_special (bool): Whether to include special characters.

    Returns:
        str: Random string.
    """
    alphabet = string.ascii_letters + string.digits
    if include_special:
        alphabet += string.punctuation

    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_token(length: int = 64) -> str:
    """
    Generate a cryptographically secure token.

    Args:
        length (int): Length of the token in bytes.

    Returns:
        str: Base64-encoded token.
    """
    token_bytes = secrets.token_bytes(length)
    return base64.urlsafe_b64encode(token_bytes).decode('utf-8').rstrip('=')


def hash_password(password: str, salt: Optional[str] = None) -> Dict[str, str]:
    """
    Hash a password using a secure algorithm (PBKDF2-HMAC-SHA256).

    Args:
        password (str): Password to hash.
        salt (Optional[str]): Salt to use. If None, a random salt is generated.

    Returns:
        Dict[str, str]: Dictionary containing the hashed password and salt.
    """
    if salt is None:
        salt = os.urandom(32)  # 32 bytes = 256 bits
    elif isinstance(salt, str):
        salt = salt.encode('utf-8')

    # Use PBKDF2-HMAC-SHA256 with 100,000 iterations
    password_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000
    )

    # Convert to hex for storage
    return {
        'hash': password_hash.hex(),
        'salt': salt.hex() if isinstance(salt, bytes) else salt
    }


def verify_password(password: str, password_hash: str, salt: str) -> bool:
    """
    Verify a password against a hash.

    Args:
        password (str): Password to verify.
        password_hash (str): Stored password hash (hex-encoded).
        salt (str): Salt used to hash the password (hex-encoded).

    Returns:
        bool: True if the password matches, False otherwise.
    """
    # Convert hex to bytes
    if isinstance(salt, str):
        salt = bytes.fromhex(salt)

    # Hash the password with the same salt
    new_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000
    ).hex()

    # Compare the hashes
    return new_hash == password_hash


def generate_hmac(data: str, key: str) -> str:
    """
    Generate an HMAC for data.

    Args:
        data (str): Data to generate HMAC for.
        key (str): Secret key.

    Returns:
        str: Hex-encoded HMAC.
    """
    h = hmac.new(
        key.encode('utf-8'),
        data.encode('utf-8'),
        hashlib.sha256
    )
    return h.hexdigest()


def verify_hmac(data: str, key: str, expected_hmac: str) -> bool:
    """
    Verify an HMAC for data.

    Args:
        data (str): Data to verify HMAC for.
        key (str): Secret key.
        expected_hmac (str): Expected HMAC.

    Returns:
        bool: True if the HMAC matches, False otherwise.
    """
    calculated_hmac = generate_hmac(data, key)
    return hmac.compare_digest(calculated_hmac, expected_hmac)


def sanitise_input(input_str: str, allowed_chars: str = None) -> str:
    """
    Sanitise input by removing potentially dangerous characters.

    Args:
        input_str (str): Input string to sanitise.
        allowed_chars (str): Optional string of allowed characters.
            If None, allows alphanumeric characters and basic punctuation.

    Returns:
        str: Sanitised input string.
    """
    if not input_str:
        return ""

    if allowed_chars:
        # Keep only allowed characters
        return ''.join(c for c in input_str if c in allowed_chars)

    # Remove potentially dangerous characters
    # Allow alphanumeric, spaces, and basic punctuation
    return re.sub(r'[^\w\s.,;\-_!?@#£$%&*()[\]{}:"\']', '', input_str)


def sanitise_filename(filename: str) -> str:
    """
    Sanitise a filename by removing potentially dangerous characters.

    Args:
        filename (str): Filename to sanitise.

    Returns:
        str: Sanitised filename.
    """
    if not filename:
        return ""

    # Remove path separators and other potentially dangerous characters
    sanitised = re.sub(r'[/\\:*?"<>|]', '', filename)

    # Ensure the filename is not empty or just periods
    if not sanitised or all(c == '.' for c in sanitised):
        return "unnamed_file"

    return sanitised


def sanitise_path(path: str) -> str:
    """
    Sanitise a file path by removing potentially dangerous components.

    Args:
        path (str): File path to sanitise.

    Returns:
        str: Sanitised file path.
    """
    if not path:
        return ""

    # Convert to Path object to handle normalization
    from pathlib import Path
    clean_path = Path(path).resolve()

    # Convert back to string
    return str(clean_path)


def is_safe_url(url: str) -> bool:
    """
    Check if a URL is safe (not a local file or potentially malicious protocol).

    Args:
        url (str): URL to check.

    Returns:
        bool: True if the URL is safe, False otherwise.
    """
    if not url:
        return False

    # Check for allowed protocols
    allowed_protocols = ('http://', 'https://', 'wss://', 'ws://')
    has_allowed_protocol = any(url.startswith(protocol)
                               for protocol in allowed_protocols)

    # Check for potential local file access
    has_file_protocol = url.startswith('file://')

    # Check for potential protocol smuggling
    has_protocol_smuggling = '//' in url.split(
        ':', 1)[1] if ':' in url else False

    return has_allowed_protocol and not has_file_protocol and not has_protocol_smuggling


def is_valid_twitch_username(username: str) -> bool:
    """
    Check if a string is a valid Twitch username.

    Args:
        username (str): Username to check.

    Returns:
        bool: True if the username is valid, False otherwise.
    """
    if not username:
        return False

    # Twitch usernames must be 4-25 characters and can only contain
    # alphanumeric characters and underscores
    return bool(re.match(r'^[a-zA-Z0-9_]{4,25}$', username))


def is_safe_command(command: str) -> bool:
    """
    Check if a command string is safe (not containing command injection).

    Args:
        command (str): Command to check.

    Returns:
        bool: True if the command is safe, False otherwise.
    """
    if not command:
        return False

    # Check for potential command injection
    dangerous_chars = ('|', '&', ';', '`', '$', '(', ')', '<', '>', '\n')
    return not any(char in command for char in dangerous_chars)


def validate_twitch_token(token: str) -> bool:
    """
    Validate a Twitch OAuth token format.

    Args:
        token (str): Token to validate.

    Returns:
        bool: True if the token has a valid format, False otherwise.
    """
    if not token:
        return False

    # Check if token starts with 'oauth:'
    if not token.startswith('oauth:'):
        return False

    # Check if the rest of the token is a valid format (alphanumeric)
    token_part = token[6:]
    return bool(re.match(r'^[a-zA-Z0-9_]{30,}$', token_part))


def encrypt_string(text: str, key: str) -> str:
    """
    Simple encryption for non-critical data.

    NOTE: This is NOT suitable for sensitive data. Use a proper cryptography
    library for sensitive data encryption.

    Args:
        text (str): Text to encrypt.
        key (str): Encryption key.

    Returns:
        str: Base64-encoded encrypted string.
    """
    if not text or not key:
        return ""

    # Create a deterministic but secure key from the input key
    hash_key = hashlib.sha256(key.encode('utf-8')).digest()

    # XOR each byte of the text with a byte from the key in a repeating pattern
    result = bytearray()
    for i, char in enumerate(text.encode('utf-8')):
        result.append(char ^ hash_key[i % len(hash_key)])

    # Return base64 encoded result
    return base64.b64encode(result).decode('utf-8')


def decrypt_string(encrypted_text: str, key: str) -> str:
    """
    Decrypt a string encrypted with encrypt_string.

    Args:
        encrypted_text (str): Base64-encoded encrypted string.
        key (str): Encryption key (must be the same as used for encryption).

    Returns:
        str: Decrypted string.
    """
    if not encrypted_text or not key:
        return ""

    try:
        # Decode base64
        encrypted_bytes = base64.b64decode(encrypted_text)

        # Create a deterministic but secure key from the input key
        hash_key = hashlib.sha256(key.encode('utf-8')).digest()

        # XOR each byte (XOR is its own inverse)
        result = bytearray()
        for i, char in enumerate(encrypted_bytes):
            result.append(char ^ hash_key[i % len(hash_key)])

        return result.decode('utf-8')
    except Exception as e:
        logger.error(f"Error decrypting string: {str(e)}")
        return ""
