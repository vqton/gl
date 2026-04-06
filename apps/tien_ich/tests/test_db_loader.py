"""Tests for core/db_loader.py - Database configuration loader."""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

from cryptography.fernet import Fernet


class TestDbConfigLoader:
    """Test database configuration loading."""

    def test_load_valid_sqlite_config(self):
        """Test loading a valid SQLite configuration."""
        from core.db_loader import load_db_config

        config = {
            "default": {
                "engine": "sqlite",
                "name": "/path/to/db.sqlite3",
            }
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config, f)
            temp_path = f.name

        try:
            with patch("core.db_loader.DB_CONFIG_PATH", Path(temp_path)):
                result = load_db_config()

                assert result["default"]["ENGINE"] == "django.db.backends.sqlite3"
                assert result["default"]["NAME"] == "/path/to/db.sqlite3"
        finally:
            os.unlink(temp_path)

    def test_load_mysql_config(self):
        """Test loading MySQL configuration with encrypted password."""
        from core.db_loader import load_db_config

        key = Fernet.generate_key()
        fernet = Fernet(key)
        encrypted_pwd = fernet.encrypt(b"my_secret_password").decode()

        config = {
            "default": {
                "engine": "mysql",
                "name": "mydb",
                "user": "admin",
                "password": encrypted_pwd,
                "host": "localhost",
                "port": 3306,
                "_encryption_key": key.decode(),
            }
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config, f)
            temp_path = f.name

        try:
            with patch("core.db_loader.DB_CONFIG_PATH", Path(temp_path)):
                result = load_db_config()

                assert result["default"]["ENGINE"] == "django.db.backends.mysql"
                assert result["default"]["NAME"] == "mydb"
                assert result["default"]["USER"] == "admin"
                assert result["default"]["PASSWORD"] == "my_secret_password"
                assert result["default"]["HOST"] == "localhost"
                assert result["default"]["PORT"] == 3306
        finally:
            os.unlink(temp_path)

    def test_load_postgresql_config(self):
        """Test loading PostgreSQL configuration."""
        from core.db_loader import load_db_config

        config = {
            "default": {
                "engine": "postgresql",
                "name": "mydb",
                "user": "postgres",
                "password": "secret",
                "host": "db.example.com",
                "port": 5432,
            }
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config, f)
            temp_path = f.name

        try:
            with patch("core.db_loader.DB_CONFIG_PATH", Path(temp_path)):
                result = load_db_config()

                assert result["default"]["ENGINE"] == "django.db.backends.postgresql"
                assert result["default"]["PORT"] == 5432
        finally:
            os.unlink(temp_path)

    def test_load_sqlserver_config(self):
        """Test loading SQL Server configuration."""
        from core.db_loader import load_db_config

        config = {
            "default": {
                "engine": "sqlserver",
                "name": "MyDB",
                "user": "sa",
                "password": "Secret123!",
                "host": "sqlserver.local",
                "port": 1433,
            }
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config, f)
            temp_path = f.name

        try:
            with patch("core.db_loader.DB_CONFIG_PATH", Path(temp_path)):
                result = load_db_config()

                assert result["default"]["ENGINE"] == "mssql"
                assert result["default"]["PORT"] == 1433
        finally:
            os.unlink(temp_path)

    def test_fallback_to_sqlite_when_file_missing(self):
        """Test fallback to SQLite when config file is missing."""
        from core.db_loader import load_db_config

        with patch("core.db_loader.DB_CONFIG_PATH", Path("/nonexistent/path.json")):
            result = load_db_config()

            assert "default" in result
            assert result["default"]["ENGINE"] == "django.db.backends.sqlite3"

    def test_fallback_to_sqlite_when_file_empty(self):
        """Test fallback to SQLite when config file is empty."""
        from core.db_loader import load_db_config

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("")
            temp_path = f.name

        try:
            with patch("core.db_loader.DB_CONFIG_PATH", Path(temp_path)):
                result = load_db_config()

                assert "default" in result
                assert result["default"]["ENGINE"] == "django.db.backends.sqlite3"
        finally:
            os.unlink(temp_path)

    def test_fallback_to_sqlite_when_invalid_json(self):
        """Test fallback to SQLite when config file has invalid JSON."""
        from core.db_loader import load_db_config

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("not valid json")
            temp_path = f.name

        try:
            with patch("core.db_loader.DB_CONFIG_PATH", Path(temp_path)):
                result = load_db_config()

                assert "default" in result
                assert result["default"]["ENGINE"] == "django.db.backends.sqlite3"
        finally:
            os.unlink(temp_path)

    def test_decrypts_password_correctly(self):
        """Test that encrypted passwords are decrypted on load."""
        from core.db_loader import load_db_config

        key = Fernet.generate_key()
        fernet = Fernet(key)
        original_password = "SuperSecret123!"
        encrypted = fernet.encrypt(original_password.encode()).decode()

        config = {
            "default": {
                "engine": "mysql",
                "name": "testdb",
                "user": "root",
                "password": encrypted,
                "host": "localhost",
                "port": 3306,
                "_encryption_key": key.decode(),
            }
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config, f)
            temp_path = f.name

        try:
            with patch("core.db_loader.DB_CONFIG_PATH", Path(temp_path)):
                result = load_db_config()

                assert result["default"]["PASSWORD"] == original_password
        finally:
            os.unlink(temp_path)

    def test_engine_mapping_unknown_defaults_to_sqlite(self):
        """Test that unknown engine defaults to SQLite."""
        from core.db_loader import load_db_config

        config = {
            "default": {
                "engine": "oracle",
                "name": "/path/to/db.sqlite3",
            }
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config, f)
            temp_path = f.name

        try:
            with patch("core.db_loader.DB_CONFIG_PATH", Path(temp_path)):
                result = load_db_config()

                assert result["default"]["ENGINE"] == "django.db.backends.sqlite3"
        finally:
            os.unlink(temp_path)

    def test_sqlite_options_included(self):
        """Test that SQLite config includes timeout option."""
        from core.db_loader import load_db_config

        config = {
            "default": {
                "engine": "sqlite",
                "name": "/path/to/db.sqlite3",
            }
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config, f)
            temp_path = f.name

        try:
            with patch("core.db_loader.DB_CONFIG_PATH", Path(temp_path)):
                result = load_db_config()

                assert "OPTIONS" in result["default"]
                assert result["default"]["OPTIONS"]["timeout"] == 30
        finally:
            os.unlink(temp_path)

    def test_multiple_database_aliases(self):
        """Test loading multiple database aliases."""
        from core.db_loader import load_db_config

        config = {
            "default": {
                "engine": "sqlite",
                "name": "/path/to/system.sqlite3",
            },
            "company_abc": {
                "engine": "sqlite",
                "name": "/path/to/company_abc.sqlite3",
            },
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config, f)
            temp_path = f.name

        try:
            with patch("core.db_loader.DB_CONFIG_PATH", Path(temp_path)):
                result = load_db_config()

                assert "default" in result
                assert "company_abc" in result
                assert result["default"]["ENGINE"] == "django.db.backends.sqlite3"
                assert result["company_abc"]["ENGINE"] == "django.db.backends.sqlite3"
        finally:
            os.unlink(temp_path)
