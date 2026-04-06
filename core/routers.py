"""Database router for multi-tenant setup.

Routes system models to 'default' DB and company models to client DB.
Supports dynamic client selection via thread-local context.
"""

import threading

from django.db import connections

logger = __import__("logging").getLogger(__name__)

SYSTEM_APPS = {
    "he_thong",
    "users",
    "tien_ich",
    "accounting",
    "admin",
    "auth",
    "contenttypes",
    "sessions",
    "messages",
    "staticfiles",
    "sites",
}
COMPANY_APPS = {
    "nghiep_vu",
    "kho",
    "luong",
    "danh_muc",
    "bao_cao",
    "tai_san",
    "ngan_hang",
    "cong_no",
    "so_sach",
    "ccdc",
    "thue",
    "mua_hang",
    "gia_thanh",
    "thu_quy",
    "phan_tich",
}

_thread_local = threading.local()
_thread_local.client_db = "client"


def get_client_db() -> str:
    """Get current client database alias from thread-local context.

    Returns:
        Current client database alias (default: 'client').
    """
    return getattr(_thread_local, "client_db", "client")


def set_client_db(alias: str) -> None:
    """Set client database alias for current thread.

    Args:
        alias: Database alias name (e.g., 'company_abc').
    """
    _thread_local.client_db = alias


class CompanyRouter:
    """Database router for multi-tenant architecture.

    Routes system models (he_thong, users, tien_ich) to 'default' DB.
    Routes company models (nghiep_vu, kho, luong, etc.) to client DB.
    """

    def _get_app_label(self, model_name: str | None) -> str | None:
        """Extract app label from model_name string.

        Args:
            model_name: Full model name like 'app_label.ModelName'.

        Returns:
            App label or None.
        """
        if model_name and "." in model_name:
            return model_name.split(".")[0]
        return None

    def db_for_read(self, model, **hints):
        """Route read operations to appropriate database.

        Args:
            model: Model class or None.
            **hints: Additional routing hints.

        Returns:
            Database alias name.
        """
        app_label = self._get_app_label(hints.get("model_name"))
        if not app_label and hasattr(model, "_meta"):
            app_label = model._meta.app_label

        if app_label in SYSTEM_APPS:
            return "default"
        if app_label in COMPANY_APPS:
            client_db = get_client_db()

            if client_db in connections.databases:
                return client_db
            return "default"
        return None

    def db_for_write(self, model, **hints):
        """Route write operations to appropriate database.

        Args:
            model: Model class or None.
            **hints: Additional routing hints.

        Returns:
            Database alias name.
        """
        return self.db_for_read(model, **hints)

    def allow_relation(self, obj1, obj2, **hints):
        """Allow relations only within same database.

        Args:
            obj1: First model instance or hint dict.
            obj2: Second model instance or hint dict.
            **hints: Additional routing hints.

        Returns:
            True if relation is allowed, False otherwise.
        """
        app1 = None
        app2 = None

        if hasattr(obj1, "_meta"):
            app1 = obj1._meta.app_label
        elif isinstance(obj1, dict):
            app1 = obj1.get("app_label")

        if hasattr(obj2, "_meta"):
            app2 = obj2._meta.app_label
        elif isinstance(obj2, dict):
            app2 = obj2.get("app_label")

        if app1 and app2:
            if app1 in SYSTEM_APPS and app2 in SYSTEM_APPS:
                return True
            if app1 in COMPANY_APPS and app2 in COMPANY_APPS:
                return True
            if app1 == app2:
                return True
            if app1 not in SYSTEM_APPS and app1 not in COMPANY_APPS:
                return True
            if app2 not in SYSTEM_APPS and app2 not in COMPANY_APPS:
                return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Control which database migrations run on.

        System models migrate on 'default'.
        Company models migrate on client DB, or default if client doesn't exist.

        Args:
            db: Target database alias.
            app_label: App label of model being migrated.
            model_name: Model name being migrated.
            **hints: Additional routing hints.

        Returns:
            True if migration should run, False if not.
        """
        if app_label in SYSTEM_APPS:
            return db == "default"
        if app_label in COMPANY_APPS:
            client_db = get_client_db()
            if client_db in connections.databases:
                return db == client_db
            return db == "default"
        return None
