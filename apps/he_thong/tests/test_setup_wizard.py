"""Tests for he_thong setup wizard views."""

import json
from pathlib import Path
from unittest.mock import patch

import pytest


@pytest.mark.django_db
class TestSetupWizard:
    """Test setup wizard views."""

    def test_setup_view_renders_first_run(self, client):
        """Test setup view renders when no config exists."""
        with patch("apps.he_thong.views.is_first_run", return_value=True):
            response = client.get("/setup/")
            assert response.status_code == 200
            assert b"setup" in response.content.lower()

    def test_setup_view_redirects_if_configured(self, client):
        """Test setup view redirects if already configured."""
        with patch("apps.he_thong.views.is_first_run", return_value=False):
            response = client.get("/setup/")
            assert response.status_code == 302

    def test_setup_save_sqlite_config(self, client):
        """Test saving SQLite configuration."""
        with patch("apps.he_thong.views.is_first_run", return_value=True):
            with patch("apps.he_thong.views.save_db_config") as mock_save:
                client.post(
                    "/setup/",
                    {
                        "action": "save",
                        "database_type": "sqlite",
                        "db_name": "/path/to/test.sqlite3",
                    },
                )
                assert mock_save.called

    def test_setup_save_mysql_config(self, client):
        """Test saving MySQL configuration."""
        with patch("apps.he_thong.views.is_first_run", return_value=True):
            with patch("apps.he_thong.views.save_db_config") as mock_save:
                client.post(
                    "/setup/",
                    {
                        "action": "save",
                        "database_type": "mysql",
                        "db_name": "mydb",
                        "db_host": "localhost",
                        "db_port": "3306",
                        "db_user": "admin",
                        "db_password": "secret",
                    },
                )
                assert mock_save.called

    def test_setup_save_postgresql_config(self, client):
        """Test saving PostgreSQL configuration."""
        with patch("apps.he_thong.views.is_first_run", return_value=True):
            with patch("apps.he_thong.views.save_db_config") as mock_save:
                client.post(
                    "/setup/",
                    {
                        "action": "save",
                        "database_type": "postgresql",
                        "db_name": "mydb",
                        "db_host": "db.example.com",
                        "db_port": "5432",
                        "db_user": "postgres",
                        "db_password": "secret",
                    },
                )
                assert mock_save.called

    def test_test_connection_success(self, client):
        """Test connection test returns success."""
        with patch("apps.he_thong.views.test_db_connection") as mock_test:
            mock_test.return_value = (True, "Kết nối thành công")
            response = client.post(
                "/setup/test-connection/",
                json.dumps(
                    {
                        "database_type": "sqlite",
                        "db_name": ":memory:",
                    }
                ),
                content_type="application/json",
            )
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True

    def test_test_connection_failure(self, client):
        """Test connection test returns failure."""
        with patch("apps.he_thong.views.test_db_connection") as mock_test:
            mock_test.return_value = (False, "Không thể kết nối")
            response = client.post(
                "/setup/test-connection/",
                json.dumps(
                    {
                        "database_type": "mysql",
                        "db_name": "nonexistent",
                        "db_host": "localhost",
                        "db_port": "3306",
                        "db_user": "root",
                        "db_password": "wrong",
                    }
                ),
                content_type="application/json",
            )
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is False

    def test_first_run_detection_no_config(self):
        """Test is_first_run returns True when no config file."""
        from apps.he_thong import views

        with patch.object(views, "DB_CONFIG_PATH", Path("/nonexistent/config.json")):
            assert views.is_first_run() is True

    def test_first_run_detection_empty_config(self):
        """Test is_first_run returns True when config is empty."""
        from apps.he_thong import views

        with patch.object(views, "DB_CONFIG_PATH", Path("/fake/config.json")):
            with patch.object(Path, "exists", return_value=True):
                with patch.object(Path, "read_text", return_value=""):
                    assert views.is_first_run() is True

    def test_first_run_detection_valid_config(self):
        """Test is_first_run returns False when config is valid."""
        from apps.he_thong import views

        config = {"default": {"engine": "sqlite", "name": "/path/to/db.sqlite3"}}

        with patch.object(views, "DB_CONFIG_PATH", Path("/fake/config.json")):
            with patch.object(Path, "exists", return_value=True):
                with patch.object(Path, "read_text", return_value=json.dumps(config)):
                    assert views.is_first_run() is False
