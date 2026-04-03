"""Tests for audit queue."""

import json
import os
import sqlite3
import tempfile

import pytest


@pytest.mark.django_db
class TestAuditQueue:
    """Test audit queue functionality."""

    def test_queue_push_and_flush(self):
        """Test pushing items to queue and flushing."""
        from core.audit_queue import AuditQueue

        with tempfile.NamedTemporaryFile(suffix=".sqlite3", delete=False) as f:
            db_path = f.name

        try:
            queue = AuditQueue(db_path=db_path)
            queue.push(
                {
                    "user": "admin",
                    "action": "CREATE",
                    "url": "/test/",
                    "ip_address": "127.0.0.1",
                    "model_name": "TestModel",
                    "object_id": "1",
                    "old_value": None,
                    "new_value": json.dumps({"name": "Test"}),
                }
            )
            assert len(queue._buffer) == 1

            queue.flush()
            assert len(queue._buffer) == 0
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)

    def test_flush_writes_to_database(self):
        """Test that flush writes entries to SQLite."""
        from core.audit_queue import AuditQueue

        with tempfile.NamedTemporaryFile(suffix=".sqlite3", delete=False) as f:
            db_path = f.name

        try:
            queue = AuditQueue(db_path=db_path)
            queue.push(
                {
                    "user": "admin",
                    "action": "UPDATE",
                    "url": "/test/",
                    "ip_address": "192.168.1.1",
                    "model_name": "TestModel",
                    "object_id": "42",
                    "old_value": json.dumps({"name": "Old"}),
                    "new_value": json.dumps({"name": "New"}),
                }
            )
            queue.flush()

            conn = sqlite3.connect(db_path)
            cursor = conn.execute("SELECT COUNT(*) FROM audit_log")
            count = cursor.fetchone()[0]
            conn.close()
            assert count == 1
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)

    def test_auto_flush_on_threshold(self):
        """Test auto-flush when buffer reaches threshold."""
        from core.audit_queue import AuditQueue

        with tempfile.NamedTemporaryFile(suffix=".sqlite3", delete=False) as f:
            db_path = f.name

        try:
            queue = AuditQueue(db_path=db_path, flush_threshold=3)
            for i in range(3):
                queue.push(
                    {
                        "user": "admin",
                        "action": "CREATE",
                        "url": f"/test/{i}/",
                        "ip_address": "127.0.0.1",
                        "model_name": "TestModel",
                        "object_id": str(i),
                        "old_value": None,
                        "new_value": None,
                    }
                )
            assert len(queue._buffer) == 0
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)

    def test_separate_db_file(self):
        """Test that audit log uses separate database file."""
        from core.audit_queue import get_audit_db_path

        db_path = get_audit_db_path()
        assert "audit" in db_path.name.lower() or "audit" in str(db_path)

    def test_batch_flush_multiple_items(self):
        """Test flushing multiple items at once."""
        from core.audit_queue import AuditQueue

        with tempfile.NamedTemporaryFile(suffix=".sqlite3", delete=False) as f:
            db_path = f.name

        try:
            queue = AuditQueue(db_path=db_path)
            for i in range(10):
                queue.push(
                    {
                        "user": f"user_{i}",
                        "action": "CREATE",
                        "url": f"/test/{i}/",
                        "ip_address": "127.0.0.1",
                        "model_name": "TestModel",
                        "object_id": str(i),
                        "old_value": None,
                        "new_value": None,
                    }
                )
            queue.flush()

            conn = sqlite3.connect(db_path)
            cursor = conn.execute("SELECT COUNT(*) FROM audit_log")
            count = cursor.fetchone()[0]
            conn.close()
            assert count == 10
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)
