"""Tests for core/routers.py - Company database router."""

from unittest.mock import MagicMock, patch


def _mock_connections_databases():
    """Create a mock connections.databases dict that can be patched."""
    from django.db import connections

    mock_db = dict(connections.databases)
    return mock_db


class TestCompanyRouter:
    """Test database routing between system and company databases."""

    def setup_method(self):
        """Reset thread-local client context before each test."""
        from core.routers import set_client_db

        set_client_db("client")

    def test_system_models_route_to_default(self):
        """Test that system models route to default database."""
        from core.routers import CompanyRouter

        router = CompanyRouter()

        assert (
            router.db_for_read(None, model_name="he_thong.ThongTinCongTy") == "default"
        )
        assert router.db_for_read(None, model_name="users.NguoiDung") == "default"
        assert router.db_for_read(None, model_name="tien_ich.AuditLog") == "default"

    def test_company_models_route_to_client_db(self):
        """Test that company models route to client database when it exists."""
        from core import routers
        from core.routers import CompanyRouter

        mock_databases = _mock_connections_databases()
        mock_databases["client"] = {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }

        with patch.object(routers, "connections") as mock_conn:
            mock_conn.databases = mock_databases
            router = CompanyRouter()

            assert router.db_for_read(None, model_name="nghiep_vu.PieuThu") == "client"
            assert router.db_for_read(None, model_name="kho.NhapKho") == "client"
            assert router.db_for_read(None, model_name="luong.BangLuong") == "client"
            assert (
                router.db_for_read(None, model_name="danh_muc.TaiKhoanKeToan")
                == "client"
            )
            assert (
                router.db_for_read(None, model_name="bao_cao.BaoCaoTaiChinh")
                == "client"
            )

    def test_db_for_write_routes_correctly(self):
        """Test that write operations route to correct databases."""
        from core import routers
        from core.routers import CompanyRouter

        mock_databases = _mock_connections_databases()
        mock_databases["client"] = {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }

        with patch.object(routers, "connections") as mock_conn:
            mock_conn.databases = mock_databases
            router = CompanyRouter()

            assert router.db_for_write(None, model_name="users.NguoiDung") == "default"
            assert router.db_for_write(None, model_name="nghiep_vu.PieuThu") == "client"

    def test_company_models_fallback_to_default(self):
        """Test that company models fallback to default when client DB doesn't exist."""
        from core import routers
        from core.routers import CompanyRouter

        mock_databases = _mock_connections_databases()
        mock_databases.pop("client", None)

        with patch.object(routers, "connections") as mock_conn:
            mock_conn.databases = mock_databases
            router = CompanyRouter()

            assert router.db_for_read(None, model_name="nghiep_vu.PieuThu") == "default"

    def test_allow_migrate_system_models_only_on_default(self):
        """Test that system models only migrate on default DB."""
        from core.routers import CompanyRouter

        router = CompanyRouter()

        assert router.allow_migrate("default", "users", model_name="NguoiDung") is True
        assert router.allow_migrate("client", "users", model_name="NguoiDung") is False

    def test_allow_migrate_company_models_only_on_client(self):
        """Test that company models only migrate on client DB."""
        from core import routers
        from core.routers import CompanyRouter

        mock_databases = _mock_connections_databases()
        mock_databases["client"] = {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }

        with patch.object(routers, "connections") as mock_conn:
            mock_conn.databases = mock_databases
            router = CompanyRouter()

            assert (
                router.allow_migrate("client", "nghiep_vu", model_name="PieuThu")
                is True
            )
            assert (
                router.allow_migrate("default", "nghiep_vu", model_name="PieuThu")
                is False
            )

    def test_allow_migrate_company_models_fallback_to_default(self):
        """Test that company models migrate on default when client doesn't exist."""
        from core import routers
        from core.routers import CompanyRouter

        mock_databases = _mock_connections_databases()
        mock_databases.pop("client", None)

        with patch.object(routers, "connections") as mock_conn:
            mock_conn.databases = mock_databases
            router = CompanyRouter()

            assert (
                router.allow_migrate("default", "nghiep_vu", model_name="PieuThu")
                is True
            )

    def test_allow_relation_cross_db(self):
        """Test that cross-database relations are not allowed."""
        from core.routers import CompanyRouter

        router = CompanyRouter()

        obj1 = MagicMock()
        obj1._meta.app_label = "users"
        obj2 = MagicMock()
        obj2._meta.app_label = "nghiep_vu"

        assert router.allow_relation(obj1, obj2) is False

    def test_same_app_relations_allowed(self):
        """Test that same-app relations are allowed."""
        from core.routers import CompanyRouter

        router = CompanyRouter()

        obj1 = MagicMock()
        obj1._meta.app_label = "nghiep_vu"
        obj2 = MagicMock()
        obj2._meta.app_label = "nghiep_vu"

        assert router.allow_relation(obj1, obj2) is True

    def test_dynamic_client_selection(self):
        """Test dynamic client database selection via context."""
        from core import routers
        from core.routers import CompanyRouter, get_client_db, set_client_db

        original_client = get_client_db()

        try:
            set_client_db("company_abc")
            assert get_client_db() == "company_abc"

            mock_databases = _mock_connections_databases()
            mock_databases["company_abc"] = {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }

            with patch.object(routers, "connections") as mock_conn:
                mock_conn.databases = mock_databases

                router = CompanyRouter()
                assert (
                    router.db_for_read(None, model_name="nghiep_vu.PieuThu")
                    == "company_abc"
                )
        finally:
            set_client_db(original_client)

    def test_default_client_is_client_alias(self):
        """Test that default client alias is 'client'."""
        from core.routers import get_client_db

        assert get_client_db() == "client"
