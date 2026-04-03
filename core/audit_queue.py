"""Audit queue for batch writing to separate audit database."""

import logging
import sqlite3
import threading
import time
from pathlib import Path

from django.conf import settings

logger = logging.getLogger(__name__)

_AUDIT_DB_DIR = settings.BASE_DIR / "data"
_AUDIT_DB_PATH = _AUDIT_DB_DIR / "audit.sqlite3"


def get_audit_db_path() -> Path:
    """Get the path to the audit database file."""
    _AUDIT_DB_DIR.mkdir(parents=True, exist_ok=True)
    return _AUDIT_DB_PATH


def _init_audit_db(db_path: str) -> None:
    """Initialize the audit database schema."""
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            action TEXT NOT NULL,
            url TEXT DEFAULT '',
            ip_address TEXT DEFAULT '',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            model_name TEXT DEFAULT '',
            object_id TEXT DEFAULT '',
            old_value TEXT,
            new_value TEXT
        )
    """)
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_log(timestamp)"
    )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_log(user)")
    conn.commit()
    conn.close()


class AuditQueue:
    """
    Batch audit log writer.

    Buffers audit entries and flushes them to a separate SQLite database
    every 10 seconds or when the buffer reaches the threshold.
    """

    def __init__(
        self,
        db_path: str | None = None,
        flush_interval: int = 10,
        flush_threshold: int = 50,
    ):
        """
        Initialize audit queue.

        Args:
            db_path: Path to audit SQLite database.
            flush_interval: Seconds between automatic flushes.
            flush_threshold: Number of items to trigger auto-flush.
        """
        self._db_path = db_path or str(get_audit_db_path())
        self._flush_interval = flush_interval
        self._flush_threshold = flush_threshold
        self._buffer: list[dict] = []
        self._lock = threading.Lock()
        self._last_flush = time.time()

        _init_audit_db(self._db_path)

    def push(self, entry: dict) -> None:
        """
        Push an audit entry to the queue.

        Args:
            entry: Dict with user, action, url, ip_address, model_name,
                   object_id, old_value, new_value.
        """
        with self._lock:
            self._buffer.append(entry)
            if len(self._buffer) >= self._flush_threshold:
                self._flush_locked()

    def flush(self) -> None:
        """Flush all buffered entries to the audit database."""
        with self._lock:
            self._flush_locked()

    def _flush_locked(self) -> None:
        """Internal flush method (must be called with lock held)."""
        if not self._buffer:
            return

        try:
            conn = sqlite3.connect(self._db_path)
            conn.execute("PRAGMA journal_mode=WAL")
            _init_audit_db(self._db_path)
            conn.executemany(
                """
                INSERT INTO audit_log
                    (user, action, url, ip_address, model_name, object_id,
                     old_value, new_value)
                VALUES
                    (:user, :action, :url, :ip_address, :model_name,
                     :object_id, :old_value, :new_value)
            """,
                self._buffer,
            )
            conn.commit()
            conn.close()
            self._buffer.clear()
            self._last_flush = time.time()
        except Exception as e:
            logger.error("Failed to flush audit queue: %s", e, exc_info=True)

    def should_flush(self) -> bool:
        """Check if auto-flush should be triggered."""
        if len(self._buffer) >= self._flush_threshold:
            return True
        if self._buffer and (time.time() - self._last_flush) >= self._flush_interval:
            return True
        return False

    def auto_flush(self) -> None:
        """Check and flush if needed."""
        if self.should_flush():
            self.flush()


_global_queue: AuditQueue | None = None


def get_audit_queue() -> AuditQueue:
    """Get or create the global audit queue singleton."""
    global _global_queue
    if _global_queue is None:
        _global_queue = AuditQueue()
    return _global_queue
