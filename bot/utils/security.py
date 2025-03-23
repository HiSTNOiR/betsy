"""
Security utility functions for the Twitch bot.
"""
import os
import re
import logging
import hashlib
import secrets
import base64
from typing import Optional, Dict, Any, Tuple

# Set up logger
logger = logging.getLogger(__name__)

def generate_secure_token(length: int = 32) -> str:
    """
    Generate a cryptographically secure random token.
    
    Args:
        length: Length of token in bytes (default: 32)
    
    Returns:
        Secure token string (base64-encoded)
    """
    token_bytes = secrets.token_bytes(length)
    return base64.urlsafe_b64encode(token_bytes).decode('utf-8').rstrip('=')

def hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
    """
    Hash a password using a secure algorithm (SHA-256).
    
    Args:
        password: Password to hash
        salt: Optional salt (if None, a random salt will be generated)
    
    Returns:
        Tuple of (password_hash, salt)
    """
    if not salt:
        salt = secrets.token_hex(16)
    
    # Create hash
    hash_obj = hashlib.sha256()
    hash_obj.update(salt.encode('utf-8'))
    hash_obj.update(password.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    
    return password_hash, salt

def verify_password(password: str, password_hash: str, salt: str) -> bool:
    """
    Verify a password against a stored hash.
    
    Args:
        password: Password to verify
        password_hash: Stored password hash
        salt: Salt used for hashing
    
    Returns:
        True if password matches, False otherwise
    """
    calculated_hash, _ = hash_password(password, salt)
    return secrets.compare_digest(calculated_hash, password_hash)

def is_valid_oauth_token(token: str) -> bool:
    """
    Check if a token appears to be a valid OAuth token.
    
    Args:
        token: Token to validate
    
    Returns:
        True if token appears valid, False otherwise
    """
    # Check if token starts with "oauth:" (Twitch format)
    if token.startswith('oauth:'):
        token = token[6:]
    
    # Simple validation: at least 30 chars, only alphanumeric or certain special chars
    return bool(re.match(r'^[a-zA-Z0-9_\-]{30,}$', token))

def mask_sensitive_data(data: str) -> str:
    """
    Mask sensitive data for logging.
    
    Args:
        data: Data to mask
    
    Returns:
        Masked data
    """
    if not data:
        return ""
    
    # Mask OAuth tokens
    if data.startswith('oauth:'):
        return 'oauth:***********'
    
    # Mask other types of tokens or sensitive data
    if len(data) > 8:
        visible_chars = min(4, len(data) // 4)
        return data[:visible_chars] + '*' * (len(data) - visible_chars)
    
    return '********'

def is_safe_string(text: str) -> bool:
    """
    Check if a string contains only safe characters.
    
    Args:
        text: String to check
    
    Returns:
        True if string is safe, False otherwise
    """
    # Allow alphanumeric, space, and common punctuation
    return bool(re.match(r'^[a-zA-Z0-9\s.,!?@#$%^&*()_+\-=\[\]{}|;:"\'<>\/\\]+$', text))

def rate_limit_key(user_id: str, command: str) -> str:
    """
    Generate a key for rate limiting.
    
    Args:
        user_id: User ID
        command: Command name
    
    Returns:
        Rate limit key
    """
    return f"{user_id}:{command}"