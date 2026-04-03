"""Tests for tien_ich crypto module."""

import os

import pytest
from cryptography.fernet import Fernet


@pytest.fixture(autouse=True)
def setup_encryption_key():
    """Set up encryption key for all crypto tests."""
    key = Fernet.generate_key().decode()
    os.environ["ENCRYPTION_KEY"] = key
    yield
    del os.environ["ENCRYPTION_KEY"]


class TestCrypto:
    """Test encryption/decryption functions."""

    def test_encrypt_decrypt_roundtrip(self):
        """Test that encrypt then decrypt returns original value."""
        from apps.tien_ich import crypto

        crypto._fernet = None
        key = os.environ.get("ENCRYPTION_KEY")
        if key and len(key) == 44:
            crypto._fernet = Fernet(key.encode())

        original = "sensitive_data_123"
        encrypted = crypto.encrypt(original)
        assert encrypted != original
        decrypted = crypto.decrypt(encrypted)
        assert decrypted == original

    def test_encrypt_returns_different_ciphertext(self):
        """Test that same plaintext produces different ciphertext (IV)."""
        from apps.tien_ich import crypto

        crypto._fernet = None
        key = os.environ.get("ENCRYPTION_KEY")
        if key and len(key) == 44:
            crypto._fernet = Fernet(key.encode())

        enc1 = crypto.encrypt("same_text")
        enc2 = crypto.encrypt("same_text")
        assert enc1 != enc2

    def test_decrypt_invalid_data_raises(self):
        """Test that decrypting invalid data raises exception."""
        from apps.tien_ich import crypto

        crypto._fernet = None
        key = os.environ.get("ENCRYPTION_KEY")
        if key and len(key) == 44:
            crypto._fernet = Fernet(key.encode())

        with pytest.raises(Exception):
            crypto.decrypt("not_valid_encrypted_data")

    def test_missing_key_fallback_encrypt(self):
        """Test encrypt falls back to plaintext when key is missing."""
        from apps.tien_ich import crypto

        original_fernet = crypto._fernet
        crypto._fernet = None
        try:
            result = crypto.encrypt("plaintext")
            assert result == "plaintext"
        finally:
            crypto._fernet = original_fernet

    def test_missing_key_fallback_decrypt(self):
        """Test decrypt falls back to plaintext when key is missing."""
        from apps.tien_ich import crypto

        original_fernet = crypto._fernet
        crypto._fernet = None
        try:
            result = crypto.decrypt("plaintext")
            assert result == "plaintext"
        finally:
            crypto._fernet = original_fernet

    def test_empty_string_encrypt(self):
        """Test encrypting empty string."""
        from apps.tien_ich import crypto

        crypto._fernet = None
        key = os.environ.get("ENCRYPTION_KEY")
        if key and len(key) == 44:
            crypto._fernet = Fernet(key.encode())

        encrypted = crypto.encrypt("")
        assert encrypted != ""
        assert crypto.decrypt(encrypted) == ""

    def test_unicode_encrypt(self):
        """Test encrypting unicode (Vietnamese) strings."""
        from apps.tien_ich import crypto

        crypto._fernet = None
        key = os.environ.get("ENCRYPTION_KEY")
        if key and len(key) == 44:
            crypto._fernet = Fernet(key.encode())

        original = "Công ty TNHH Một Thành Viên"
        encrypted = crypto.encrypt(original)
        assert crypto.decrypt(encrypted) == original
