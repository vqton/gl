"""Tests for health endpoint."""

import json

import pytest
from django.test import Client


@pytest.mark.django_db
class TestHealthEndpoint:
    """Test system health endpoint."""

    def test_health_returns_json(self):
        """Test health endpoint returns valid JSON with status ok."""
        client = Client()
        response = client.get("/he-thong/health/")
        assert response.status_code == 200
        assert response["Content-Type"] == "application/json"

        data = json.loads(response.content)
        assert data["status"] == "ok"
        assert "db_integrity" in data
        assert "disk_space_mb" in data

    def test_health_db_integrity(self):
        """Test health endpoint checks DB integrity."""
        client = Client()
        response = client.get("/he-thong/health/")
        data = json.loads(response.content)
        assert data["db_integrity"] == "ok"

    def test_health_disk_space(self):
        """Test health endpoint reports disk space."""
        client = Client()
        response = client.get("/he-thong/health/")
        data = json.loads(response.content)
        assert isinstance(data["disk_space_mb"], (int, float))
        assert data["disk_space_mb"] >= 0
