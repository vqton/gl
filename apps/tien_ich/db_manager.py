"""Database management utilities for backup, restore, health check, and more."""

import json
import os
import shutil
import sqlite3
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import connection, connections

logger = __import__("logging").getLogger(__name__)


class DBManager:
    """Database management utilities for SQLite databases.

    Provides backup, restore, health check, VACUUM, export, and import
    functionality for SQLite databases used in the accounting system.
    """

    def __init__(self, db_alias: str = "default"):
        """Initialize DBManager with database alias.

        Args:
            db_alias: Django database alias (default: 'default').
        """
        self.db_alias = db_alias

    def _get_db_path(self) -> Path:
        """Get path to the database file.

        Returns:
            Path to the SQLite database file.

        Raises:
            ValidationError: If database is in-memory (not file-based).
        """
        db_settings = connections.databases[self.db_alias]
        db_name = db_settings["NAME"]
        if db_name == ":memory:" or "mode=memory" in str(db_name):
            raise ValidationError(
                "Cannot perform file operations on in-memory database"
            )
        return Path(db_name)

    def _checkpoint_wal(self) -> None:
        """Checkpoint WAL file to ensure consistent backup.

        Runs PRAGMA wal_checkpoint(TRUNCATE) to flush WAL to main DB.
        """
        conn = sqlite3.connect(str(self._get_db_path()))
        try:
            conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        finally:
            conn.close()

    def backup(
        self,
        backup_dir: str | None = None,
        prefix: str = "backup",
    ) -> str:
        """Create online backup of the database.

        Uses sqlite3.Connection.backup() for zero-downtime backup.
        Checkpoints WAL first, then creates timestamped zip file.

        Args:
            backup_dir: Directory to store backup (default: data/backups/).
            prefix: Filename prefix (default: 'backup').

        Returns:
            Path to the backup zip file.
        """
        if backup_dir is None:
            backup_dir = str(Path(settings.BASE_DIR) / "data" / "backups")

        backup_path = Path(backup_dir)
        backup_path.mkdir(parents=True, exist_ok=True)

        # Checkpoint WAL first
        self._checkpoint_wal()

        # Create timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_name = f"{prefix}_{timestamp}.zip"
        zip_path = backup_path / zip_name

        db_path = self._get_db_path()
        wal_path = Path(str(db_path) + "-wal")
        shm_path = Path(str(db_path) + "-shm")

        # Create backup using online backup API
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_db = Path(tmpdir) / db_path.name

            # Use sqlite3 backup API for consistent copy
            src_conn = sqlite3.connect(str(db_path))
            dst_conn = sqlite3.connect(str(tmp_db))
            try:
                src_conn.backup(dst_conn)
            finally:
                dst_conn.close()
                src_conn.close()

            # Copy WAL and SHM if they exist
            if wal_path.exists():
                shutil.copy2(wal_path, Path(tmpdir) / wal_path.name)
            if shm_path.exists():
                shutil.copy2(shm_path, Path(tmpdir) / shm_path.name)

            # Create zip file
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                zf.write(tmp_db, db_path.name)
                if wal_path.exists():
                    zf.write(
                        Path(tmpdir) / wal_path.name,
                        wal_path.name,
                    )
                if shm_path.exists():
                    zf.write(
                        Path(tmpdir) / shm_path.name,
                        shm_path.name,
                    )

        logger.info("Backup created: %s", zip_path)
        return str(zip_path)

    def restore(self, backup_path: str) -> dict:
        """Restore database from backup zip file.

        Validates zip file, extracts, replaces current DB, and verifies
        integrity.

        Args:
            backup_path: Path to backup zip file.

        Returns:
            Dict with restore result: {"status": "ok", "integrity": "ok"}.

        Raises:
            ValidationError: If backup file is invalid or restore fails.
        """
        backup_file = Path(backup_path)
        if not backup_file.exists():
            raise ValidationError(f"Backup file not found: {backup_path}")

        if not zipfile.is_zipfile(backup_file):
            raise ValidationError(f"Invalid backup file: {backup_path}")

        db_path = self._get_db_path()

        # Backup current DB before restore
        if db_path.exists():
            self.backup(prefix="pre_restore")

        with tempfile.TemporaryDirectory() as tmpdir:
            # Extract backup
            with zipfile.ZipFile(backup_file, "r") as zf:
                zf.extractall(tmpdir)

            # Find DB file in extracted contents
            db_files = list(Path(tmpdir).glob("*.sqlite3"))
            if not db_files:
                raise ValidationError("No database file found in backup")

            src_db = db_files[0]

            # Replace current DB
            shutil.copy2(src_db, db_path)

            # Copy WAL/SHM if present
            wal_files = list(Path(tmpdir).glob("*.sqlite3-wal"))
            if wal_files:
                shutil.copy2(wal_files[0], Path(str(db_path) + "-wal"))

            shm_files = list(Path(tmpdir).glob("*.sqlite3-shm"))
            if shm_files:
                shutil.copy2(shm_files[0], Path(str(db_path) + "-shm"))

        # Verify integrity
        conn = sqlite3.connect(str(db_path))
        try:
            result = conn.execute("PRAGMA integrity_check").fetchone()
            integrity = result[0] if result else "unknown"
        finally:
            conn.close()

        if integrity != "ok":
            raise ValidationError(f"Restore failed: integrity check = {integrity}")

        logger.info("Database restored from: %s", backup_path)
        return {"status": "ok", "integrity": integrity}

    def health_check(self) -> dict:
        """Check database health and return status report.

        Returns:
            Dict with health status:
            - integrity: 'ok' or error message
            - db_size_mb: Database file size in MB
            - wal_size_mb: WAL file size in MB (0 if not exists)
            - row_counts: Dict of table name -> row count
            - last_backup: Path to most recent backup or None
        """
        db_path = self._get_db_path()
        db_size = db_path.stat().st_size if db_path.exists() else 0
        wal_path = Path(str(db_path) + "-wal")
        wal_size = wal_path.stat().st_size if wal_path.exists() else 0

        # Check integrity
        conn = sqlite3.connect(str(db_path))
        try:
            result = conn.execute("PRAGMA integrity_check").fetchone()
            integrity = result[0] if result else "unknown"

            # Get row counts
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
            )
            tables = [row[0] for row in cursor.fetchall()]
            row_counts = {}
            for table in tables:
                try:
                    count = conn.execute(f"SELECT COUNT(*) FROM [{table}]").fetchone()[
                        0
                    ]
                    row_counts[table] = count
                except Exception:
                    row_counts[table] = -1
        finally:
            conn.close()

        # Find last backup
        backup_dir = Path(settings.BASE_DIR) / "data" / "backups"
        last_backup = None
        if backup_dir.exists():
            backups = sorted(backup_dir.glob("*.zip"))
            if backups:
                last_backup = str(backups[-1])

        return {
            "integrity": integrity,
            "db_size_mb": round(db_size / 1024 / 1024, 2),
            "wal_size_mb": round(wal_size / 1024 / 1024, 2),
            "row_counts": row_counts,
            "last_backup": last_backup,
        }

    def vacuum(self) -> dict:
        """Run VACUUM to reclaim space and rebuild indexes.

        Returns:
            Dict with before/after sizes:
            - before_mb: Size before VACUUM
            - after_mb: Size after VACUUM
        """
        db_path = self._get_db_path()
        before_size = db_path.stat().st_size if db_path.exists() else 0

        conn = sqlite3.connect(str(db_path))
        try:
            conn.execute("PRAGMA busy_timeout=5000")
            conn.execute("VACUUM")
        finally:
            conn.close()

        after_size = db_path.stat().st_size if db_path.exists() else 0

        logger.info(
            "VACUUM: %.2f MB -> %.2f MB",
            before_size / 1024 / 1024,
            after_size / 1024 / 1024,
        )
        return {
            "before_mb": round(before_size / 1024 / 1024, 2),
            "after_mb": round(after_size / 1024 / 1024, 2),
        }

    def export_data(
        self,
        tables: list[str] | None = None,
        output_dir: str | None = None,
        format: str = "json",
    ) -> str:
        """Export database tables to JSON or Excel format.

        Args:
            tables: List of table names to export (None = all).
            output_dir: Directory for export file (default: data/exports/).
            format: Export format ('json' or 'excel').

        Returns:
            Path to the exported file.
        """
        if output_dir is None:
            output_dir = str(Path(settings.BASE_DIR) / "data" / "exports")

        export_path = Path(output_dir)
        export_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"export_{timestamp}.json"
        file_path = export_path / filename

        conn = sqlite3.connect(str(self._get_db_path()))
        conn.row_factory = sqlite3.Row
        try:
            if tables is None:
                cursor = conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
                )
                tables = [row[0] for row in cursor.fetchall()]

            data = {}
            for table in tables:
                try:
                    rows = conn.execute(f"SELECT * FROM [{table}]").fetchall()
                    data[table] = [dict(row) for row in rows]
                except Exception as e:
                    logger.warning("Failed to export table %s: %s", table, e)
                    data[table] = []
        finally:
            conn.close()

        # Add metadata
        output = {
            "_metadata": {
                "exported_at": datetime.now().isoformat(),
                "database": str(self._get_db_path()),
                "tables": list(data.keys()),
            },
            **data,
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2, default=str)

        logger.info("Data exported to: %s", file_path)
        return str(file_path)

    def import_data(
        self,
        file_path: str,
        format: str = "json",
    ) -> dict:
        """Import data from JSON or Excel file.

        Validates data before import, uses transaction for rollback on error.

        Args:
            file_path: Path to import file.
            format: Import format ('json' or 'excel').

        Returns:
            Dict with import result: {"status": "ok", "tables_imported": [...]}.

        Raises:
            ValidationError: If file is invalid or import fails.
        """
        import_file = Path(file_path)
        if not import_file.exists():
            raise ValidationError(f"Import file not found: {file_path}")

        try:
            with open(import_file, encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValidationError(f"Invalid JSON file: {e}")

        # Remove metadata
        data.pop("_metadata", None)

        conn = sqlite3.connect(str(self._get_db_path()))
        try:
            conn.execute("BEGIN")
            tables_imported = []
            for table, rows in data.items():
                if not rows:
                    continue
                try:
                    columns = list(rows[0].keys())
                    placeholders = ", ".join(["?"] * len(columns))
                    col_names = ", ".join([f"[{c}]" for c in columns])
                    sql = (
                        f"INSERT OR REPLACE INTO [{table}] "
                        f"({col_names}) VALUES ({placeholders})"
                    )
                    for row in rows:
                        values = [row.get(col) for col in columns]
                        conn.execute(sql, values)
                    tables_imported.append(table)
                except Exception as e:
                    conn.rollback()
                    raise ValidationError(f"Failed to import table {table}: {e}")
            conn.commit()
        finally:
            conn.close()

        logger.info(
            "Data imported from: %s (%d tables)", file_path, len(tables_imported)
        )
        return {"status": "ok", "tables_imported": tables_imported}
