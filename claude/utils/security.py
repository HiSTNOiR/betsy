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
logger = logging.getLogger(__name__)
VALID_SCHEMES = frozenset(['http', 'https', 'ws', 'wss'])


def generate_random_string(length: int = 32, include_special: bool = False) -> str:
    if length <= 0:
        return ""
    alphabet = string.ascii_letters + string.digits
    if include_special:
        alphabet += string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_token(length: int = 64) -> str:
    if length <= 0:
        return ""
    token_bytes = secrets.token_bytes(length)
    return base64.urlsafe_b64encode(token_bytes).decode('utf-8').rstrip('=')


def hash_password(password: str, salt: Optional[Union[str, bytes]] = None) -> Dict[str, str]:
    if not password:
        raise ValueError("Password cannot be empty")
    if salt is None:
        salt = os.urandom(32)
    elif isinstance(salt, str):
        try:
            salt = bytes.fromhex(salt)
        except ValueError:
            salt = salt.encode('utf-8')
    password_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000
    )
    return {
        'hash': password_hash.hex(),
        'salt': salt.hex() if isinstance(salt, bytes) else salt
    }


def verify_password(password: str, password_hash: str, salt: Union[str, bytes]) -> bool:
    if not password or not password_hash or not salt:
        return False
    if isinstance(salt, str):
        try:
            salt = bytes.fromhex(salt)
        except ValueError:
            salt = salt.encode('utf-8')
    try:
        new_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        ).hex()
        return hmac.compare_digest(new_hash, password_hash)
    except Exception as e:
        logger.error(f"Error verifying password: {str(e)}")
        return False


def generate_hmac(data: str, key: str) -> str:
    if not data or not key:
        return ""
    h = hmac.new(
        key.encode('utf-8'),
        data.encode('utf-8'),
        hashlib.sha256
    )
    return h.hexdigest()


def verify_hmac(data: str, key: str, expected_hmac: str) -> bool:
    if not data or not key or not expected_hmac:
        return False
    calculated_hmac = generate_hmac(data, key)
    return hmac.compare_digest(calculated_hmac, expected_hmac)


def sanitise_input(input_str: Optional[str], allowed_chars: Optional[str] = None) -> str:
    if not input_str:
        return ""
    if allowed_chars:
        return ''.join(c for c in input_str if c in allowed_chars)
    return re.sub(r'[^\w\s.,;\-_!?@#£$%&*()[\]{}:"\']', '', input_str)


def sanitise_filename(filename: Optional[str]) -> str:
    if not filename:
        return "unnamed_file"
    sanitised = re.sub(r'[/\\:*?"<>|]', '', filename)
    if not sanitised or all(c == '.' for c in sanitised):
        return "unnamed_file"
    return sanitised


def sanitise_path(path: Optional[str]) -> str:
    if not path:
        return ""
    try:
        from pathlib import Path
        clean_path = Path(path).resolve()
        return str(clean_path)
    except Exception as e:
        logger.error(f"Error sanitising path: {str(e)}")
        return ""


def is_safe_url(url: Optional[str]) -> bool:
    if not url:
        return False
    try:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme.lower() not in VALID_SCHEMES:
            return False
        if not parsed.netloc or parsed.netloc.startswith(":") or "@" in parsed.netloc:
            return False
        if "//" in parsed.path:
            return False
        dangerous_patterns = ['javascript:', 'data:', 'vbscript:']
        for part in [parsed.path, parsed.query, parsed.fragment]:
            for pattern in dangerous_patterns:
                if pattern in part.lower():
                    return False
        if any(ord(c) > 127 for c in parsed.netloc):
            try:
                parsed.netloc.encode('idna').decode('ascii')
            except UnicodeError:
                return False
        return True
    except Exception as e:
        logger.error(f"Error checking URL safety: {str(e)}")
        return False


def is_valid_twitch_username(username: Optional[str]) -> bool:
    if not username:
        return False
    return bool(re.match(r'^[a-zA-Z0-9_]{4,25}$', username))


def is_safe_command(command: Optional[str]) -> bool:
    if not command:
        return False
    dangerous_chars = ('|', '&', ';', '`', '$', '(', ')', '<', '>', '\n')
    return not any(char in command for char in dangerous_chars)


def validate_twitch_token(token: Optional[str]) -> bool:
    if not token:
        return False
    if not token.startswith('oauth:'):
        return False
    token_part = token[6:]
    return bool(re.match(r'^[a-zA-Z0-9_]{30,}$', token_part))


def encrypt_string(text: Optional[str], key: Optional[str]) -> str:
    if not text or not key:
        return ""
    try:
        hash_key = hashlib.sha256(key.encode('utf-8')).digest()
        result = bytearray()
        for i, char in enumerate(text.encode('utf-8')):
            result.append(char ^ hash_key[i % len(hash_key)])
        return base64.b64encode(result).decode('utf-8')
    except Exception as e:
        logger.error(f"Error encrypting string: {str(e)}")
        return ""


def decrypt_string(encrypted_text: Optional[str], key: Optional[str]) -> str:
    if not encrypted_text or not key:
        return ""
    try:
        encrypted_bytes = base64.b64decode(encrypted_text)
        hash_key = hashlib.sha256(key.encode('utf-8')).digest()
        result = bytearray()
        for i, char in enumerate(encrypted_bytes):
            result.append(char ^ hash_key[i % len(hash_key)])
        return result.decode('utf-8')
    except Exception as e:
        logger.error(f"Error decrypting string: {str(e)}")
        return ""


try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

    def _derive_key(password: str, salt: Optional[bytes] = None) -> Tuple[bytes, bytes]:
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
        if not text or not password:
            raise ValueError("Text and password cannot be empty")
        key, salt = _derive_key(password)
        f = Fernet(key)
        ciphertext = f.encrypt(text.encode('utf-8'))
        return {
            'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
            'salt': base64.b64encode(salt).decode('utf-8')
        }

    def secure_decrypt(encrypted_data: Dict[str, str], password: str) -> str:
        if not encrypted_data or not password:
            raise ValueError("Encrypted data and password cannot be empty")
        if 'ciphertext' not in encrypted_data or 'salt' not in encrypted_data:
            raise ValueError(
                "Encrypted data must contain 'ciphertext' and 'salt' keys")
        ciphertext = base64.b64decode(encrypted_data['ciphertext'])
        salt = base64.b64decode(encrypted_data['salt'])
        key, _ = _derive_key(password, salt)
        f = Fernet(key)
        plaintext = f.decrypt(ciphertext)
        return plaintext.decode('utf-8')
    ADVANCED_ENCRYPTION_AVAILABLE = True
    logger.info("Advanced encryption using cryptography package is available")

except ImportError:
    def secure_encrypt(text: str, password: str) -> Dict[str, str]:
        raise RuntimeError(
            "Advanced encryption requires the 'cryptography' package. "
            "Install it with 'pip install cryptography'."
        )

    def secure_decrypt(encrypted_data: Dict[str, str], password: str) -> str:
        raise RuntimeError(
            "Advanced encryption requires the 'cryptography' package. "
            "Install it with 'pip install cryptography'."
        )
    ADVANCED_ENCRYPTION_AVAILABLE = False
    logger.warning(
        "Advanced encryption not available. Install 'cryptography' package to enable.")
