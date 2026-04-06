"""Client management utilities for accounting firms."""

import logging
import shutil
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import connections

from apps.tien_ich.connection_registry import ConnectionRegistry

logger = logging.getLogger(__name__)


class ClientManager:
    """
    Client lifecycle management for accounting firms.

    Handles onboarding, suspension, activation, archiving, and batch operations
    for client databases.
    """

    def __init__(self):
        """Initialize ClientManager."""
        self.registry = ConnectionRegistry()

    def onboard(self, client_data: dict) -> "Client":  # noqa: F821
        """
        Onboard a new client.

        Creates client record, copies template DB, registers connection,
        and assigns users.

        Args:
            client_data: Dict with keys:
                - ten_cong_ty: Company name
                - ma_so_thue: Tax code
                - nganh_nghe: Industry (optional)
                - nam: Fiscal year
                - admin_user: Admin user instance (optional)
                - assigned_users: List of (user, vai_tro) tuples (optional)

        Returns:
            Created Client instance.

        Raises:
            ValidationError: If template DB not found or creation fails.
        """
        from apps.he_thong.models import Client

        # Find template DB
        template_path = Path(settings.BASE_DIR) / "data" / "template_2026.sqlite3"
        if not template_path.exists():
            raise ValidationError(
                "Không tìm thấy CSDL mẫu. Vui lòng chạy "
                "'python manage.py create_template_db' trước."
            )

        # Generate client DB path
        clients_dir = Path(settings.BASE_DIR) / "data" / "clients"
        clients_dir.mkdir(parents=True, exist_ok=True)

        # Get next client number
        last_client = Client.objects.order_by("-pk").first()
        client_num = (last_client.pk + 1) if last_client else 1
        db_filename = f"client_{client_num:03d}_{client_data.get('nam', 2026)}.sqlite3"
        db_path = clients_dir / db_filename

        # Copy template DB
        shutil.copy2(template_path, db_path)
        logger.info("Template copied to: %s", db_path)

        # Create client record
        client = Client.objects.create(
            ten_cong_ty=client_data["ten_cong_ty"],
            ma_so_thue=client_data["ma_so_thue"],
            nganh_nghe=client_data.get("nganh_nghe", ""),
            db_path=str(db_path),
            trang_thai="active",
        )

        # Register client DB in connection registry
        alias = f"client_{client.pk}"
        self.registry.register_client_db(
            client_id=client.pk,
            db_path=str(db_path),
            alias=alias,
        )

        # Assign users if provided
        assigned_users = client_data.get("assigned_users", [])
        for user, vai_tro in assigned_users:
            from apps.he_thong.models import ClientUserMapping

            ClientUserMapping.objects.create(
                client=client,
                user=user,
                vai_tro=vai_tro,
            )

        logger.info(
            "Client onboarded: %s (%s)", client.ma_khach_hang, client.ten_cong_ty
        )
        return client

    def suspend(self, client_id: int) -> "Client":  # noqa: F821
        """
        Suspend client access.

        Args:
            client_id: Client primary key.

        Returns:
            Updated Client instance.

        Raises:
            ValidationError: If client not found.
        """
        from apps.he_thong.models import Client

        try:
            client = Client.objects.get(pk=client_id)
        except Client.DoesNotExist:
            raise ValidationError(f"Không tìm thấy khách hàng ID {client_id}")

        client.suspend()

        # Unregister from connection registry
        alias = f"client_{client_id}"
        self.registry.unregister_client_db(alias)

        logger.info("Client suspended: %s", client.ma_khach_hang)
        return client

    def activate(self, client_id: int) -> "Client":  # noqa: F821
        """
        Reactivate suspended client.

        Args:
            client_id: Client primary key.

        Returns:
            Updated Client instance.

        Raises:
            ValidationError: If client not found.
        """
        from apps.he_thong.models import Client

        try:
            client = Client.objects.get(pk=client_id)
        except Client.DoesNotExist:
            raise ValidationError(f"Không tìm thấy khách hàng ID {client_id}")

        client.activate()

        # Re-register in connection registry
        db_path = Path(client.db_path)
        if db_path.exists():
            alias = f"client_{client_id}"
            self.registry.register_client_db(
                client_id=client_id,
                db_path=str(db_path),
                alias=alias,
            )

        logger.info("Client activated: %s", client.ma_khach_hang)
        return client

    def archive(self, client_id: int) -> str:
        """
        Archive client: backup, compress, move to archive folder.

        Args:
            client_id: Client primary key.

        Returns:
            Path to archived file.

        Raises:
            ValidationError: If client not found or archive fails.
        """
        import zipfile
        from datetime import datetime

        from apps.he_thong.models import Client

        try:
            client = Client.objects.get(pk=client_id)
        except Client.DoesNotExist:
            raise ValidationError(f"Không tìm thấy khách hàng ID {client_id}")

        db_path = Path(client.db_path)
        if not db_path.exists():
            raise ValidationError(f"CSDL không tồn tại: {db_path}")

        # Create archive directory
        archive_dir = Path(settings.BASE_DIR) / "data" / "archives"
        archive_dir.mkdir(parents=True, exist_ok=True)

        # Create zip archive
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = f"{client.ma_khach_hang}_{timestamp}.zip"
        archive_path = archive_dir / archive_name

        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.write(db_path, db_path.name)

        # Remove original DB
        db_path.unlink()

        # Unregister from connection registry
        alias = f"client_{client_id}"
        self.registry.unregister_client_db(alias)

        # Update client status
        client.archive()
        client.db_path = str(archive_path)
        client.save(update_fields=["db_path", "trang_thai", "updated_at"])

        logger.info("Client archived: %s → %s", client.ma_khach_hang, archive_path)
        return str(archive_path)

    def batch_backup(self) -> dict:
        """
        Backup all active client databases.

        Returns:
            Dict with results:
            - success: List of successfully backed up clients
            - failed: List of failed clients with error messages
        """
        import zipfile
        from datetime import datetime

        from apps.he_thong.models import Client
        from apps.tien_ich.db_manager import DBManager

        clients = Client.get_active_clients()
        backup_dir = Path(settings.BASE_DIR) / "data" / "backups" / "clients"
        backup_dir.mkdir(parents=True, exist_ok=True)

        results = {"success": [], "failed": []}

        for client in clients:
            try:
                db_path = Path(client.db_path)
                if not db_path.exists():
                    results["failed"].append(
                        {
                            "client": client.ma_khach_hang,
                            "error": "CSDL không tồn tại",
                        }
                    )
                    continue

                # Create backup
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"{client.ma_khach_hang}_{timestamp}.zip"
                backup_path = backup_dir / backup_name

                with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as zf:
                    zf.write(db_path, db_path.name)

                results["success"].append(client.ma_khach_hang)
                logger.info("Backup created: %s", backup_path)

            except Exception as e:
                results["failed"].append(
                    {
                        "client": client.ma_khach_hang,
                        "error": str(e),
                    }
                )
                logger.error("Backup failed for %s: %s", client.ma_khach_hang, e)

        return results
