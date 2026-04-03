"""Encryption helper using Fernet symmetric encryption."""

import logging
import os

from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)

_ENCRYPTION_KEY = os.environ.get("ENCRYPTION_KEY")
_fernet = None

if _ENCRYPTION_KEY:
    try:
        if len(_ENCRYPTION_KEY) == 32:
            import base64

            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b"static_salt_for_django",
                iterations=480000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(_ENCRYPTION_KEY.encode()))
            _fernet = Fernet(key)
        else:
            _fernet = Fernet(_ENCRYPTION_KEY.encode())
    except Exception as e:
        logger.warning("Failed to initialize Fernet: %s", e)
        _fernet = None
else:
    logger.warning("ENCRYPTION_KEY not set. Encryption will fall back to plaintext.")


def encrypt(plaintext: str) -> str:
    """
    Encrypt a string using Fernet symmetric encryption.

    Args:
        plaintext: String to encrypt.

    Returns:
        Encrypted string, or plaintext if encryption is unavailable.
    """
    if _fernet is None:
        logger.warning("Encryption unavailable, returning plaintext")
        return plaintext
    return _fernet.encrypt(plaintext.encode()).decode()


def decrypt(ciphertext: str) -> str:
    """
    Decrypt a Fernet-encrypted string.

    Args:
        ciphertext: Encrypted string to decrypt.

    Returns:
        Decrypted string, or ciphertext if decryption is unavailable.

    Raises:
        InvalidToken: If ciphertext is not valid Fernet token.
    """
    if _fernet is None:
        logger.warning("Decryption unavailable, returning ciphertext")
        return ciphertext
    return _fernet.decrypt(ciphertext.encode()).decode()
