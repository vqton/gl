"""Dynamic database connection registry.

Manages client database aliases at runtime WITHOUT mutating settings.DATABASES.
Uses django.db.connections.databases directly for thread-safe registration.
"""

import logging
import threading

from django.db import connections

logger = logging.getLogger(__name__)

ENGINE_MAP = {
    "sqlite": "django.db.backends.sqlite3",
    "mysql": "django.db.backends.mysql",
    "postgresql": "django.db.backends.postgresql",
    "sqlserver": "mssql",
}


class ConnectionRegistry:
    """Thread-safe registry for dynamic database connections.

    Manages client database aliases without mutating settings.DATABASES.
    Uses django.db.connections.databases directly.
    """

    _lock = threading.Lock()
    _registered: set = set()

    @classmethod
    def register(
        cls,
        alias: str,
        db_path: str,
        engine: str = "sqlite",
        user: str = "",
        password: str = "",
        host: str = "localhost",
        port: int = 0,
    ) -> None:
        """Register a new database alias.

        Args:
            alias: Database alias name (e.g., 'company_abc').
            db_path: Path to SQLite file or database name.
            engine: Database engine type.
            user: Database username (non-SQLite).
            password: Database password (non-SQLite).
            host: Database host (non-SQLite).
            port: Database port (non-SQLite).
        """
        engine_backend = ENGINE_MAP.get(engine, ENGINE_MAP["sqlite"])

        if engine_backend == ENGINE_MAP["sqlite"]:
            db_config = {
                "ENGINE": engine_backend,
                "NAME": db_path,
                "OPTIONS": {"timeout": 30},
            }
        else:
            db_config: dict = {
                "ENGINE": engine_backend,
                "NAME": db_path,
                "USER": user,
                "PASSWORD": password,
                "HOST": host,
                "PORT": port,
            }

        with cls._lock:
            connections.databases[alias] = db_config
            cls._registered.add(alias)

        logger.info("Registered database alias: %s", alias)

    @classmethod
    def unregister(cls, alias: str) -> None:
        """Unregister a database alias and close connections.

        Args:
            alias: Database alias name to remove.
        """
        with cls._lock:
            if alias in connections.databases:
                del connections.databases[alias]
                cls._registered.discard(alias)

            if alias in connections:
                try:
                    connections[alias].close()
                except Exception as e:
                    logger.warning("Error closing connection for %s: %s", alias, e)

        logger.info("Unregistered database alias: %s", alias)

    @classmethod
    def is_registered(cls, alias: str) -> bool:
        """Check if a database alias is registered.

        Args:
            alias: Database alias name.

        Returns:
            True if alias is registered.
        """
        return alias in cls._registered


def register_client_db(
    alias: str,
    db_path: str,
    engine: str = "sqlite",
    user: str = "",
    password: str = "",
    host: str = "localhost",
    port: int = 0,
) -> None:
    """Register a client database alias.

    Convenience function for ConnectionRegistry.register.

    Args:
        alias: Database alias name (e.g., 'company_abc').
        db_path: Path to SQLite file or database name.
        engine: Database engine type.
        user: Database username.
        password: Database password.
        host: Database host.
        port: Database port.
    """
    ConnectionRegistry.register(alias, db_path, engine, user, password, host, port)


def unregister_client_db(alias: str) -> None:
    """Unregister a client database alias.

    Convenience function for ConnectionRegistry.unregister.

    Args:
        alias: Database alias name to remove.
    """
    ConnectionRegistry.unregister(alias)
