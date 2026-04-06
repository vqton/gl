"""Tests for tien_ich/connection_registry.py - Dynamic DB connection registry."""

import threading
from unittest.mock import MagicMock, patch


class TestConnectionRegistry:
    """Test dynamic database connection registration."""

    def setup_method(self):
        """Clean up registry before each test."""
        from apps.tien_ich.connection_registry import ConnectionRegistry

        with ConnectionRegistry._lock:
            ConnectionRegistry._registered = set()

    def test_register_client_db_adds_alias(self):
        """Test that register_client_db adds a new database alias."""
        from apps.tien_ich import connection_registry

        mock_databases = {}

        with patch.object(connection_registry, "connections") as mock_conn:
            mock_conn.databases = mock_databases
            connection_registry.ConnectionRegistry.register(
                "company_abc", "/path/to/company_abc.sqlite3"
            )

            assert "company_abc" in mock_databases
            assert (
                mock_databases["company_abc"]["ENGINE"] == "django.db.backends.sqlite3"
            )
            assert (
                mock_databases["company_abc"]["NAME"] == "/path/to/company_abc.sqlite3"
            )

    def test_register_client_db_does_not_mutate_settings(self):
        """Test that registration does NOT mutate settings.DATABASES."""
        from django.conf import settings

        from apps.tien_ich import connection_registry

        original_databases = dict(settings.DATABASES)
        mock_databases = {}

        with patch.object(connection_registry, "connections") as mock_conn:
            mock_conn.databases = mock_databases
            connection_registry.ConnectionRegistry.register(
                "company_xyz", "/path/to/company_xyz.sqlite3"
            )

            assert settings.DATABASES == original_databases

    def test_unregister_client_db_removes_alias(self):
        """Test that unregister_client_db removes the alias."""
        from apps.tien_ich import connection_registry

        mock_databases = {
            "company_test": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": "/path/to/test.sqlite3",
            }
        }

        with patch.object(connection_registry, "connections") as mock_conn:
            mock_conn.databases = mock_databases
            mock_conn.__contains__ = lambda self, x: x in mock_databases
            connection_registry.ConnectionRegistry.register(
                "company_test", "/path/to/test.sqlite3"
            )
            assert "company_test" in mock_databases

            connection_registry.ConnectionRegistry.unregister("company_test")
            assert "company_test" not in mock_databases

    def test_unregister_closes_connections(self):
        """Test that unregister closes existing connections to the alias."""
        from apps.tien_ich import connection_registry

        mock_databases = {
            "company_close": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": "/path/to/close.sqlite3",
            }
        }
        mock_conn_obj = MagicMock()

        with patch.object(connection_registry, "connections") as mock_conn:
            mock_conn.databases = mock_databases
            mock_conn.__contains__ = lambda self, x: x in ["company_close"]
            mock_conn.__getitem__ = lambda self, x: mock_conn_obj

            connection_registry.ConnectionRegistry.register(
                "company_close", "/path/to/close.sqlite3"
            )
            connection_registry.ConnectionRegistry.unregister("company_close")

            assert "company_close" not in mock_databases

    def test_register_thread_safety(self):
        """Test that registration is thread-safe."""
        from apps.tien_ich import connection_registry

        errors = []
        mock_databases = {}

        def register_in_thread(client_id):
            try:
                with patch.object(connection_registry, "connections") as mock_conn:
                    mock_conn.databases = mock_databases
                    connection_registry.ConnectionRegistry.register(
                        client_id, f"/path/to/{client_id}.sqlite3"
                    )
            except Exception as e:
                errors.append(e)

        threads = []
        for i in range(10):
            t = threading.Thread(target=register_in_thread, args=(f"company_{i}",))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        assert len(errors) == 0

    def test_register_idempotent(self):
        """Test that registering the same alias twice doesn't duplicate."""
        from apps.tien_ich import connection_registry

        mock_databases = {}

        with patch.object(connection_registry, "connections") as mock_conn:
            mock_conn.databases = mock_databases
            connection_registry.ConnectionRegistry.register(
                "company_dup", "/path/to/dup.sqlite3"
            )
            connection_registry.ConnectionRegistry.register(
                "company_dup", "/path/to/dup.sqlite3"
            )

            assert "company_dup" in mock_databases

    def test_unregister_nonexistent_does_not_raise(self):
        """Test that unregistering a non-existent alias doesn't raise."""
        from apps.tien_ich import connection_registry

        mock_databases = {}

        with patch.object(connection_registry, "connections") as mock_conn:
            mock_conn.databases = mock_databases
            connection_registry.ConnectionRegistry.unregister("company_nonexistent")

    def test_register_with_mysql_config(self):
        """Test registering a MySQL client database."""
        from apps.tien_ich import connection_registry

        mock_databases = {}

        with patch.object(connection_registry, "connections") as mock_conn:
            mock_conn.databases = mock_databases
            connection_registry.ConnectionRegistry.register(
                "company_mysql",
                "/path/to/mysql",
                engine="mysql",
                user="admin",
                password="secret",
                host="db.local",
                port=3306,
            )

            assert (
                mock_databases["company_mysql"]["ENGINE"] == "django.db.backends.mysql"
            )
            assert mock_databases["company_mysql"]["USER"] == "admin"
            assert mock_databases["company_mysql"]["HOST"] == "db.local"
