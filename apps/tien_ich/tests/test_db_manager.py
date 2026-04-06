"""Tests for DB management utilities."""

import json
import os
import sqlite3
import tempfile
import zipfile
from pathlib import Path
from unittest.mock import patch

import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings

from apps.tien_ich.db_manager import DBManager


class TestDBManagerBackup(TestCase):
    """Test database backup functionality."""

    def setUp(self):
        self.backup_dir = tempfile.mkdtemp()
        self.db_file = Path(tempfile.mkdtemp()) / "test_db.sqlite3"
        # Create a test database file
        conn = sqlite3.connect(str(self.db_file))
        conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)")
        conn.execute("INSERT INTO test (name) VALUES ('test1')")
        conn.commit()
        conn.close()

    @override_settings(DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": None,  # Will be set in test
        }
    })
    def test_backup_creates_zip_file(self):
        """Test that backup creates a valid zip file."""
        from django.db import connections
        connections.databases["default"]["NAME"] = str(self.db_file)
        manager = DBManager()
        backup_path = manager.backup(backup_dir=self.backup_dir)
        assert backup_path is not None
        assert Path(backup_path).exists()
        assert backup_path.endswith('.zip')

    @override_settings(DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": None,
        }
    })
    def test_backup_zip_contains_db_file(self):
        """Test that backup zip contains the database file."""
        from django.db import connections
        connections.databases["default"]["NAME"] = str(self.db_file)
        manager = DBManager()
        backup_path = manager.backup(backup_dir=self.backup_dir)
        with zipfile.ZipFile(backup_path, 'r') as zf:
            names = zf.namelist()
            assert any(name.endswith('.sqlite3') for name in names)

    @override_settings(DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": None,
        }
    })
    def test_backup_timestamped_filename(self):
        """Test that backup file has timestamp in name."""
        from django.db import connections
        connections.databases["default"]["NAME"] = str(self.db_file)
        manager = DBManager()
        backup_path = manager.backup(backup_dir=self.backup_dir)
        filename = Path(backup_path).name
        assert 'backup_' in filename
        assert filename.endswith('.zip')

    @override_settings(DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": None,
        }
    })
    def test_backup_custom_prefix(self):
        """Test backup with custom prefix."""
        from django.db import connections
        connections.databases["default"]["NAME"] = str(self.db_file)
        manager = DBManager()
        backup_path = manager.backup(
            backup_dir=self.backup_dir,
            prefix='client_001'
        )
        filename = Path(backup_path).name
        assert 'client_001' in filename


class TestDBManagerHealthCheck(TestCase):
    """Test database health check functionality."""

    def setUp(self):
        self.db_file = Path(tempfile.mkdtemp()) / "test_db.sqlite3"
        conn = sqlite3.connect(str(self.db_file))
        conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)")
        conn.execute("INSERT INTO test (name) VALUES ('test1')")
        conn.commit()
        conn.close()

    @override_settings(DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": None,
        }
    })
    def test_health_check_returns_dict(self):
        """Test that health check returns a dictionary."""
        from django.db import connections
        connections.databases["default"]["NAME"] = str(self.db_file)
        manager = DBManager()
        result = manager.health_check()
        assert isinstance(result, dict)

    @override_settings(DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": None,
        }
    })
    def test_health_check_has_integrity(self):
        """Test that health check includes integrity status."""
        from django.db import connections
        connections.databases["default"]["NAME"] = str(self.db_file)
        manager = DBManager()
        result = manager.health_check()
        assert 'integrity' in result
        assert result['integrity'] == 'ok'

    @override_settings(DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": None,
        }
    })
    def test_health_check_has_db_size(self):
        """Test that health check includes database size."""
        from django.db import connections
        connections.databases["default"]["NAME"] = str(self.db_file)
        manager = DBManager()
        result = manager.health_check()
        assert 'db_size_mb' in result
        assert isinstance(result['db_size_mb'], (int, float))

    @override_settings(DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": None,
        }
    })
    def test_health_check_has_row_counts(self):
        """Test that health check includes row counts."""
        from django.db import connections
        connections.databases["default"]["NAME"] = str(self.db_file)
        manager = DBManager()
        result = manager.health_check()
        assert 'row_counts' in result
        assert isinstance(result['row_counts'], dict)


class TestDBManagerVacuum(TestCase):
    """Test database VACUUM functionality."""

    def setUp(self):
        self.db_file = Path(tempfile.mkdtemp()) / "test_db.sqlite3"
        conn = sqlite3.connect(str(self.db_file))
        conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)")
        conn.execute("INSERT INTO test (name) VALUES ('test1')")
        conn.commit()
        conn.close()

    @override_settings(DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": None,
        }
    })
    def test_vacuum_returns_before_after_size(self):
        """Test that vacuum returns size comparison."""
        from django.db import connections
        connections.databases["default"]["NAME"] = str(self.db_file)
        manager = DBManager()
        result = manager.vacuum()
        assert isinstance(result, dict)
        assert 'before_mb' in result
        assert 'after_mb' in result

    @override_settings(DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": None,
        }
    })
    def test_vacuum_reduces_or_maintains_size(self):
        """Test that vacuum doesn't increase size significantly."""
        from django.db import connections
        connections.databases["default"]["NAME"] = str(self.db_file)
        manager = DBManager()
        result = manager.vacuum()
        # Vacuum should not increase size by more than 10%
        assert result['after_mb'] <= result['before_mb'] * 1.1


class TestDBManagerExport(TestCase):
    """Test data export functionality."""

    def setUp(self):
        self.export_dir = tempfile.mkdtemp()
        self.db_file = Path(tempfile.mkdtemp()) / "test_db.sqlite3"
        conn = sqlite3.connect(str(self.db_file))
        conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)")
        conn.execute("INSERT INTO test (name) VALUES ('test1')")
        conn.commit()
        conn.close()

    @override_settings(DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": None,
        }
    })
    def test_export_creates_json_file(self):
        """Test that export creates a valid JSON file."""
        from django.db import connections
        connections.databases["default"]["NAME"] = str(self.db_file)
        manager = DBManager()
        export_path = manager.export_data(
            output_dir=self.export_dir,
            format='json'
        )
        assert export_path is not None
        assert Path(export_path).exists()
        assert export_path.endswith('.json')

    @override_settings(DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": None,
        }
    })
    def test_export_json_is_valid(self):
        """Test that exported JSON is valid."""
        from django.db import connections
        connections.databases["default"]["NAME"] = str(self.db_file)
        manager = DBManager()
        export_path = manager.export_data(
            output_dir=self.export_dir,
            format='json'
        )
        with open(export_path) as f:
            data = json.load(f)
        assert isinstance(data, dict)

    @override_settings(DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": None,
        }
    })
    def test_export_includes_metadata(self):
        """Test that export includes metadata."""
        from django.db import connections
        connections.databases["default"]["NAME"] = str(self.db_file)
        manager = DBManager()
        export_path = manager.export_data(
            output_dir=self.export_dir,
            format='json'
        )
        with open(export_path) as f:
            data = json.load(f)
        assert '_metadata' in data or 'metadata' in data


class TestDBManagerImport(TestCase):
    """Test data import functionality."""

    def setUp(self):
        self.export_dir = tempfile.mkdtemp()
        self.db_file = Path(tempfile.mkdtemp()) / "test_db.sqlite3"
        conn = sqlite3.connect(str(self.db_file))
        conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)")
        conn.execute("INSERT INTO test (name) VALUES ('test1')")
        conn.commit()
        conn.close()

    @override_settings(DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": None,
        }
    })
    def test_import_valid_json(self):
        """Test importing valid JSON data."""
        from django.db import connections
        connections.databases["default"]["NAME"] = str(self.db_file)
        manager = DBManager()
        # Export first, then import
        export_path = manager.export_data(
            output_dir=self.export_dir,
            format='json'
        )
        # Create a new DB for import with the same table structure
        new_db = Path(tempfile.mkdtemp()) / "import_db.sqlite3"
        conn = sqlite3.connect(str(new_db))
        conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)")
        conn.commit()
        conn.close()
        connections.databases["default"]["NAME"] = str(new_db)
        manager2 = DBManager()
        # Import should not raise
        result = manager2.import_data(export_path, format='json')
        assert result is not None

    def test_import_invalid_file_raises_error(self):
        """Test that importing invalid file raises error."""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            f.write(b'not valid json{{{')
            f.flush()
            manager = DBManager()
            with pytest.raises((ValidationError, json.JSONDecodeError)):
                manager.import_data(f.name, format='json')


class TestDBManagerRestore(TestCase):
    """Test database restore functionality."""

    def setUp(self):
        self.backup_dir = tempfile.mkdtemp()
        self.db_file = Path(tempfile.mkdtemp()) / "test_db.sqlite3"
        conn = sqlite3.connect(str(self.db_file))
        conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)")
        conn.execute("INSERT INTO test (name) VALUES ('test1')")
        conn.commit()
        conn.close()

    @override_settings(DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": None,
        }
    })
    def test_restore_valid_backup(self):
        """Test restoring from a valid backup."""
        from django.db import connections
        connections.databases["default"]["NAME"] = str(self.db_file)
        manager = DBManager()
        backup_path = manager.backup(backup_dir=self.backup_dir)
        # Restore should not raise
        result = manager.restore(backup_path)
        assert result is not None

    def test_restore_invalid_file_raises_error(self):
        """Test that restoring invalid file raises error."""
        with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as f:
            f.write(b'not a zip file')
            f.flush()
            manager = DBManager()
            with pytest.raises((ValidationError, zipfile.BadZipFile)):
                manager.restore(f.name)


class TestDBManagerInMemoryDatabase(TestCase):
    """Test DBManager behavior with in-memory databases."""

    @override_settings(DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    })
    def test_backup_raises_error_for_in_memory(self):
        """Test that backup raises error for in-memory database."""
        from django.db import connections
        # Force the setting to take effect
        connections.databases["default"]["NAME"] = ":memory:"
        manager = DBManager()
        with pytest.raises(ValidationError):
            manager.backup()

    @override_settings(DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    })
    def test_health_check_raises_error_for_in_memory(self):
        """Test that health check raises error for in-memory database."""
        from django.db import connections
        connections.databases["default"]["NAME"] = ":memory:"
        manager = DBManager()
        with pytest.raises(ValidationError):
            manager.health_check()
