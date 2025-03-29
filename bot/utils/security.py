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
import urllib.parse
from typing import Any, Dict, List, Optional, Tuple, Union

import logging

# Set up logger for this module
logger = logging.getLogger(__name__)

# Constants for URL validation
VALID_SCHEMES = frozenset(['http', 'https', 'ws', 'wss'])


def generate_random_string(length: int = 32, include_special: bool = False) -> str:
    """
    Generate a cryptographically secure random string.

    Args:
        length (int): Length of the random string.
        include_special (bool): Whether to include special characters.

    Returns:
        str: Random string.
    """
    if length <= 0:
        return ""

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
    if length <= 0:
        return ""

    token_bytes = secrets.token_bytes(length)
    return base64.urlsafe_b64encode(token_bytes).decode('utf-8').rstrip('=')


def hash_password(password: str, salt: Optional[Union[str, bytes]] = None) -> Dict[str, str]:
    """
    Hash a password using a secure algorithm (PBKDF2-HMAC-SHA256).

    Args:
        password (str): Password to hash.
        salt (Optional[Union[str, bytes]]): Salt to use. If None, a random salt is generated.

    Returns:
        Dict[str, str]: Dictionary containing the hashed password and salt.
    """
    if not password:
        raise ValueError("Password cannot be empty")

    if salt is None:
        salt = os.urandom(32)  # 32 bytes = 256 bits
    elif isinstance(salt, str):
        # Convert hex string to bytes
        try:
            salt = bytes.fromhex(salt)
        except ValueError:
            # If not valid hex, use as UTF-8
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


def verify_password(password: str, password_hash: str, salt: Union[str, bytes]) -> bool:
    """
    Verify a password against a hash.

    Args:
        password (str): Password to verify.
        password_hash (str): Stored password hash (hex-encoded).
        salt (Union[str, bytes]): Salt used to hash the password (hex-encoded or bytes).

    Returns:
        bool: True if the password matches, False otherwise.
    """
    if not password or not password_hash or not salt:
        return False

    # Convert hex to bytes if needed
    if isinstance(salt, str):
        try:
            salt = bytes.fromhex(salt)
        except ValueError:
            salt = salt.encode('utf-8')

    # Hash the password with the same salt
    try:
        new_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        ).hex()

        # Compare the hashes
        return hmac.compare_digest(new_hash, password_hash)
    except Exception as e:
        logger.error(f"Error verifying password: {str(e)}")
        return False


def generate_hmac(data: str, key: str) -> str:
    """
    Generate an HMAC for data.

    Args:
        data (str): Data to generate HMAC for.
        key (str): Secret key.

    Returns:
        str: Hex-encoded HMAC.
    """
    if not data or not key:
        return ""

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
    if not data or not key or not expected_hmac:
        return False

    calculated_hmac = generate_hmac(data, key)
    return hmac.compare_digest(calculated_hmac, expected_hmac)


def sanitise_input(input_str: Optional[str], allowed_chars: Optional[str] = None) -> str:
    """
    Sanitise input by removing potentially dangerous characters.

    Args:
        input_str (Optional[str]): Input string to sanitise.
        allowed_chars (Optional[str]): Optional string of allowed characters.
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


def sanitise_filename(filename: Optional[str]) -> str:
    """
    Sanitise a filename by removing potentially dangerous characters.

    Args:
        filename (Optional[str]): Filename to sanitise.

    Returns:
        str: Sanitised filename.
    """
    if not filename:
        return "unnamed_file"

    # Remove path separators and other potentially dangerous characters
    sanitised = re.sub(r'[/\\:*?"<>|]', '', filename)

    # Ensure the filename is not empty or just periods
    if not sanitised or all(c == '.' for c in sanitised):
        return "unnamed_file"

    return sanitised


def sanitise_path(path: Optional[str]) -> str:
    """
    Sanitise a file path by removing potentially dangerous components.

    Args:
        path (Optional[str]): File path to sanitise.

    Returns:
        str: Sanitised file path.
    """
    if not path:
        return ""

    try:
        # Convert to Path object to handle normalization
        from pathlib import Path
        clean_path = Path(path).resolve()

        # Convert back to string
        return str(clean_path)
    except Exception as e:
        logger.error(f"Error sanitising path: {str(e)}")
        return ""


def is_safe_url(url: Optional[str]) -> bool:
    """
    Check if a URL is safe (not a local file or potentially malicious protocol).

    Args:
        url (Optional[str]): URL to check.

    Returns:
        bool: True if the URL is safe, False otherwise.
    """
    if not url:
        return False

    try:
        # Parse the URL
        parsed = urllib.parse.urlparse(url)

        # Check for allowed protocols
        if parsed.scheme.lower() not in VALID_SCHEMES:
            return False

        # Check if netloc is not empty and properly formatted
        if not parsed.netloc or parsed.netloc.startswith(":") or "@" in parsed.netloc:
            return False

        # Check for potential protocol smuggling
        if "//" in parsed.path:
            return False

        # Check for potentially dangerous fragments
        dangerous_patterns = ['javascript:', 'data:', 'vbscript:']
        for part in [parsed.path, parsed.query, parsed.fragment]:
            for pattern in dangerous_patterns:
                if pattern in part.lower():
                    return False

        # Check for Unicode homoglyphs or IDNA encoding attacks
        if any(ord(c) > 127 for c in parsed.netloc):
            # If domain contains non-ASCII, ensure it's properly IDNA encoded
            try:
                parsed.netloc.encode('idna').decode('ascii')
            except UnicodeError:
                return False

        return True
    except Exception as e:
        logger.error(f"Error checking URL safety: {str(e)}")
        return False


def is_valid_twitch_username(username: Optional[str]) -> bool:
    """
    Check if a string is a valid Twitch username.

    Args:
        username (Optional[str]): Username to check.

    Returns:
        bool: True if the username is valid, False otherwise.
    """
    if not username:
        return False

    # Twitch usernames must be 4-25 characters and can only contain
    # alphanumeric characters and underscores
    return bool(re.match(r'^[a-zA-Z0-9_]{4,25}$', username))


def is_safe_command(command: Optional[str]) -> bool:
    """
    Check if a command string is safe (not containing command injection).

    Args:
        command (Optional[str]): Command to check.

    Returns:
        bool: True if the command is safe, False otherwise.
    """
    if not command:
        return False

    # Check for potential command injection
    dangerous_chars = ('|', '&', ';', '`', '$', '(', ')', '<', '>', '\n')
    return not any(char in command for char in dangerous_chars)


def validate_twitch_token(token: Optional[str]) -> bool:
    """
    Validate a Twitch OAuth token format.

    Args:
        token (Optional[str]): Token to validate.

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


def encrypt_string(text: Optional[str], key: Optional[str]) -> str:
    """
    Simple encryption for non-critical data.

    NOTE: This is NOT suitable for sensitive data. Use a proper cryptography
    library for sensitive data encryption.

    Args:
        text (Optional[str]): Text to encrypt.
        key (Optional[str]): Encryption key.

    Returns:
        str: Base64-encoded encrypted string.
    """
    if not text or not key:
        return ""

    try:
        # Create a deterministic but secure key from the input key
        hash_key = hashlib.sha256(key.encode('utf-8')).digest()

        # XOR each byte of the text with a byte from the key in a repeating pattern
        result = bytearray()
        for i, char in enumerate(text.encode('utf-8')):
            result.append(char ^ hash_key[i % len(hash_key)])

        # Return base64 encoded result
        return base64.b64encode(result).decode('utf-8')
    except Exception as e:
        logger.error(f"Error encrypting string: {str(e)}")
        return ""


def decrypt_string(encrypted_text: Optional[str], key: Optional[str]) -> str:
    """
    Decrypt a string encrypted with encrypt_string.

    Args:
        encrypted_text (Optional[str]): Base64-encoded encrypted string.
        key (Optional[str]): Encryption key (must be the same as used for encryption).

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


try:
    # Attempt to import cryptography for advanced encryption
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

    def _derive_key(password: str, salt: Optional[bytes] = None) -> Tuple[bytes, bytes]:
        """
        Derive a key from a password using PBKDF2.

        Args:
            password (str): Password to derive the key from.
            salt (Optional[bytes]): Salt for key derivation. If None, random salt is generated.

        Returns:
            Tuple[bytes, bytes]: (key, salt) where key is the derived key and salt is the salt used.
        """
        if salt is None:
            salt = os.urandom(16)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode('utf-8')))
        return key, salt

    def secure_encrypt(text: str, password: str) -> Dict[str, str]:
        """
        Encrypt text using Fernet symmetric encryption with a password-derived key.

        Args:
            text (str): Text to encrypt.
            password (str): Password for encryption.

        Returns:
            Dict[str, str]: Dictionary containing base64-encoded ciphertext and salt.
        """
        if not text or not password:
            raise ValueError("Text and password cannot be empty")

        # Derive key from password
        key, salt = _derive_key(password)

        # Encrypt
        f = Fernet(key)
        ciphertext = f.encrypt(text.encode('utf-8'))

        return {
            'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
            'salt': base64.b64encode(salt).decode('utf-8')
        }

    def secure_decrypt(encrypted_data: Dict[str, str], password: str) -> str:
        """
        Decrypt text that was encrypted with secure_encrypt.

        Args:
            encrypted_data (Dict[str, str]): Dictionary with 'ciphertext' and 'salt' keys.
            password (str): Password used for encryption.

        Returns:
            str: Decrypted text.
        """
        if not encrypted_data or not password:
            raise ValueError("Encrypted data and password cannot be empty")

        if 'ciphertext' not in encrypted_data or 'salt' not in encrypted_data:
            raise ValueError(
                "Encrypted data must contain 'ciphertext' and 'salt' keys")

        # Decode the base64 encodings
        ciphertext = base64.b64decode(encrypted_data['ciphertext'])
        salt = base64.b64decode(encrypted_data['salt'])

        # Derive key from password
        key, _ = _derive_key(password, salt)

        # Decrypt
        f = Fernet(key)
        plaintext = f.decrypt(ciphertext)

        return plaintext.decode('utf-8')

    ADVANCED_ENCRYPTION_AVAILABLE = True
    logger.info("Advanced encryption using cryptography package is available")

except ImportError:
    # If cryptography is not available, add placeholder functions that warn users
    def secure_encrypt(text: str, password: str) -> Dict[str, str]:
        """
        Placeholder for secure encryption (requires cryptography package).

        Args:
            text (str): Text to encrypt.
            password (str): Password for encryption.

        Returns:
            Dict[str, str]: Dictionary simulating encrypted data.

        Raises:
            RuntimeError: Always raised to indicate that cryptography is not available.
        """
        raise RuntimeError(
            "Advanced encryption requires the 'cryptography' package. "
            "Install it with 'pip install cryptography'."
        )

    def secure_decrypt(encrypted_data: Dict[str, str], password: str) -> str:
        """
        Placeholder for secure decryption (requires cryptography package).

        Args:
            encrypted_data (Dict[str, str]): Dictionary with encrypted data.
            password (str): Password used for encryption.

        Returns:
            str: Decrypted text.

        Raises:
            RuntimeError: Always raised to indicate that cryptography is not available.
        """
        raise RuntimeError(
            "Advanced encryption requires the 'cryptography' package. "
            "Install it with 'pip install cryptography'."
        )

    ADVANCED_ENCRYPTION_AVAILABLE = False
    logger.warning(
        "Advanced encryption not available. Install 'cryptography' package to enable.")
