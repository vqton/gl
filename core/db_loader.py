"""Database configuration loader.

Reads db_config.json at startup and maps engine names to Django backends.
Falls back to SQLite if file is missing or invalid.
"""

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

DB_CONFIG_PATH = Path(__file__).resolve().parent.parent / "db_config.json"

ENGINE_MAP = {
    "sqlite": "django.db.backends.sqlite3",
    "mysql": "django.db.backends.mysql",
    "postgresql": "django.db.backends.postgresql",
    "sqlserver": "mssql",
}


def _decrypt_password(password: str, encryption_key: str | None) -> str:
    """Decrypt password if encryption key is provided.

    Args:
        password: Encrypted or plaintext password.
        encryption_key: Fernet key for decryption.

    Returns:
        Decrypted password, or original if decryption unavailable.
    """
    if not encryption_key:
        return password

    try:
        from cryptography.fernet import Fernet

        fernet = Fernet(encryption_key.encode())
        return fernet.decrypt(password.encode()).decode()
    except Exception as e:
        logger.warning("Password decryption failed: %s", e)
        return password


def _build_db_config(alias: str, db_cfg: dict) -> dict:
    """Build Django-compatible database config from JSON entry.

    Args:
        alias: Database alias name.
        db_cfg: Raw configuration dictionary from JSON.

    Returns:
        Django-compatible DATABASES entry.
    """
    engine_raw = db_cfg.get("engine", "sqlite").lower()
    engine = ENGINE_MAP.get(engine_raw, ENGINE_MAP["sqlite"])

    config: dict = {
        "ENGINE": engine,
        "NAME": db_cfg.get("name", ""),
    }

    if engine != ENGINE_MAP["sqlite"]:
        config["USER"] = db_cfg.get("user", "")
        config["PASSWORD"] = db_cfg.get("password", "")
        config["HOST"] = db_cfg.get("host", "localhost")
        config["PORT"] = db_cfg.get("port", 0)

        encryption_key = db_cfg.get("_encryption_key")
        if config["PASSWORD"] and encryption_key:
            config["PASSWORD"] = _decrypt_password(config["PASSWORD"], encryption_key)
    else:
        config["OPTIONS"] = {"timeout": 30}

    return config


def load_db_config() -> dict:
    """Load database configuration from JSON file.

    Reads core/db_config.json and converts to Django DATABASES format.
    Falls back to default SQLite if file is missing, empty, or invalid.

    Returns:
        Dictionary compatible with Django DATABASES setting.
    """
    try:
        if not DB_CONFIG_PATH.exists():
            logger.info("db_config.json not found, falling back to SQLite")
            return _default_sqlite_config()

        content = DB_CONFIG_PATH.read_text(encoding="utf-8")
        if not content.strip():
            logger.info("db_config.json is empty, falling back to SQLite")
            return _default_sqlite_config()

        raw_config = json.loads(content)

        if not raw_config or "default" not in raw_config:
            logger.info("db_config.json has no 'default' key, falling back to SQLite")
            return _default_sqlite_config()

        databases = {}
        for alias, db_cfg in raw_config.items():
            databases[alias] = _build_db_config(alias, db_cfg)

        return databases

    except json.JSONDecodeError as e:
        logger.warning("Invalid JSON in db_config.json: %s", e)
        return _default_sqlite_config()
    except Exception as e:
        logger.error("Error loading db_config.json: %s", e)
        return _default_sqlite_config()


def _default_sqlite_config() -> dict:
    """Return default SQLite configuration.

    Returns:
        Default SQLite DATABASES dict.
    """
    base_dir = Path(__file__).resolve().parent.parent.parent
    db_path = base_dir / "db" / "accounting_tt99.sqlite3"
    db_path.parent.mkdir(parents=True, exist_ok=True)

    return {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": str(db_path),
            "OPTIONS": {"timeout": 30},
        }
    }
