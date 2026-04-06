"""Tests for Client management models and utilities."""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings

from apps.he_thong.models import Client, ClientUserMapping


class TestClientModel(TestCase):
    """Test Client model."""

    def test_create_client_auto_code(self):
        """Test that client auto-generates ma_khach_hang."""
        client = Client.objects.create(
            ten_cong_ty="Công ty TNHH ABC",
            ma_so_thue="0123456789",
            db_path="data/clients/test.sqlite3",
        )
        assert client.ma_khach_hang == "KH001"

    def test_create_client_second_auto_code(self):
        """Test that second client gets next code."""
        Client.objects.create(
            ten_cong_ty="Công ty A",
            ma_so_thue="0123456789",
            db_path="data/clients/a.sqlite3",
        )
        client2 = Client.objects.create(
            ten_cong_ty="Công ty B",
            ma_so_thue="9876543210",
            db_path="data/clients/b.sqlite3",
        )
        assert client2.ma_khach_hang == "KH002"

    def test_client_str(self):
        """Test client string representation."""
        client = Client.objects.create(
            ten_cong_ty="Công ty TNHH ABC",
            ma_so_thue="0123456789",
            db_path="data/clients/test.sqlite3",
        )
        assert str(client) == "KH001 - Công ty TNHH ABC"

    def test_client_status_transitions(self):
        """Test client status transitions."""
        client = Client.objects.create(
            ten_cong_ty="Test Corp",
            ma_so_thue="0123456789",
            db_path="data/clients/test.sqlite3",
            trang_thai="active",
        )
        assert client.trang_thai == "active"

        client.suspend()
        assert client.trang_thai == "suspended"

        client.activate()
        assert client.trang_thai == "active"

        client.archive()
        assert client.trang_thai == "expired"

    def test_get_active_clients(self):
        """Test filtering active clients."""
        Client.objects.create(
            ten_cong_ty="Active Corp",
            ma_so_thue="0123456789",
            db_path="data/clients/active.sqlite3",
            trang_thai="active",
        )
        Client.objects.create(
            ten_cong_ty="Suspended Corp",
            ma_so_thue="9876543210",
            db_path="data/clients/suspended.sqlite3",
            trang_thai="suspended",
        )
        active = Client.get_active_clients()
        assert active.count() == 1
        assert active.first().ten_cong_ty == "Active Corp"


class TestClientUserMapping(TestCase):
    """Test ClientUserMapping model."""

    def setUp(self):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.client = Client.objects.create(
            ten_cong_ty="Test Corp",
            ma_so_thue="0123456789",
            db_path="data/clients/test.sqlite3",
        )

    def test_create_mapping(self):
        """Test creating client-user mapping."""
        mapping = ClientUserMapping.objects.create(
            client=self.client,
            user=self.user,
        )
        assert mapping.client == self.client
        assert mapping.user == self.user
        assert mapping.vai_tro is None

    def test_unique_constraint(self):
        """Test that duplicate mappings are prevented."""
        ClientUserMapping.objects.create(
            client=self.client,
            user=self.user,
        )
        with pytest.raises(Exception):  # IntegrityError
            ClientUserMapping.objects.create(
                client=self.client,
                user=self.user,
            )


class TestClientManager(TestCase):
    """Test ClientManager utility class."""

    def setUp(self):
        # Create a temp template DB
        self.temp_dir = tempfile.mkdtemp()
        self.template_path = Path(self.temp_dir) / "template_2026.sqlite3"
        self.template_path.touch()

    @override_settings(BASE_DIR=Path(__file__).resolve().parent.parent.parent)
    def test_onboard_requires_template(self):
        """Test that onboard fails if template DB doesn't exist."""
        from apps.tien_ich.client_manager import ClientManager

        manager = ClientManager()
        with pytest.raises(ValidationError):
            manager.onboard(
                {
                    "ten_cong_ty": "Test Corp",
                    "ma_so_thue": "0123456789",
                    "nam": 2026,
                }
            )

    def test_suspend_not_found(self):
        """Test suspending non-existent client raises error."""
        from apps.tien_ich.client_manager import ClientManager

        manager = ClientManager()
        with pytest.raises(ValidationError):
            manager.suspend(99999)

    def test_activate_not_found(self):
        """Test activating non-existent client raises error."""
        from apps.tien_ich.client_manager import ClientManager

        manager = ClientManager()
        with pytest.raises(ValidationError):
            manager.activate(99999)

    def test_archive_not_found(self):
        """Test archiving non-existent client raises error."""
        from apps.tien_ich.client_manager import ClientManager

        manager = ClientManager()
        with pytest.raises(ValidationError):
            manager.archive(99999)

    def test_batch_backup_empty(self):
        """Test batch backup with no clients."""
        from apps.tien_ich.client_manager import ClientManager

        manager = ClientManager()
        results = manager.batch_backup()
        assert results["success"] == []
        assert results["failed"] == []
