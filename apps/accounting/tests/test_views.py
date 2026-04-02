"""Tests for accounting views (login, logout, dashboard)."""

import pytest
from django.urls import resolve, reverse
from django.contrib.auth import get_user_model


User = get_user_model()


class TestAuthUrls:
    """Test authentication URL routing."""

    def test_login_url_resolves(self):
        """Test login URL resolves to correct view."""
        match = resolve("/login/")
        assert match.url_name == "login"
        assert match.app_name == "accounting"

    def test_logout_url_resolves(self):
        """Test logout URL resolves to correct view."""
        match = resolve("/logout/")
        assert match.url_name == "logout"
        assert match.app_name == "accounting"

    def test_dashboard_url_resolves(self):
        """Test dashboard URL resolves to correct view."""
        match = resolve("/")
        assert match.url_name == "dashboard"
        assert match.app_name == "accounting"

    def test_reverse_login(self):
        """Test reverse URL for login."""
        url = reverse("accounting:login")
        assert url == "/login/"

    def test_reverse_logout(self):
        """Test reverse URL for logout."""
        url = reverse("accounting:logout")
        assert url == "/logout/"

    def test_reverse_dashboard(self):
        """Test reverse URL for dashboard."""
        url = reverse("accounting:dashboard")
        assert url == "/"


@pytest.mark.django_db
class TestLoginView:
    """Test login view behavior."""

    def test_login_page_get(self, client):
        """Test login page loads for anonymous users."""
        response = client.get("/login/")
        assert response.status_code == 200
        assert "Đăng nhập" in response.content.decode()

    def test_login_redirect_when_authenticated(self, client):
        """Test authenticated users are redirected from login page."""
        User.objects.create_user(username="testuser", password="testpass123")
        client.login(username="testuser", password="testpass123")
        response = client.get("/login/")
        assert response.status_code == 302
        assert response.url == "/"

    def test_login_success(self, client):
        """Test successful login redirects to dashboard."""
        User.objects.create_user(username="testuser", password="testpass123")
        response = client.post("/login/", {
            "username": "testuser",
            "password": "testpass123",
        })
        assert response.status_code == 302

    def test_login_failure(self, client):
        """Test failed login shows error."""
        response = client.post("/login/", {
            "username": "wronguser",
            "password": "wrongpass",
        })
        assert response.status_code == 200
        assert "không đúng" in response.content.decode()


@pytest.mark.django_db
class TestLogoutView:
    """Test logout view behavior."""

    def test_logout_redirects_to_login(self, client):
        """Test logout redirects to login page."""
        User.objects.create_user(username="testuser", password="testpass123")
        client.login(username="testuser", password="testpass123")
        response = client.get("/logout/")
        assert response.status_code == 302
        assert response.url == "/login/"

    def test_logout_logs_out_user(self, client):
        """Test logout actually logs out the user."""
        User.objects.create_user(username="testuser", password="testpass123")
        client.login(username="testuser", password="testpass123")
        client.get("/logout/")
        response = client.get("/login/")
        assert response.status_code == 200


@pytest.mark.django_db
class TestDashboardView:
    """Test dashboard view behavior."""

    def test_dashboard_requires_login(self, client):
        """Test dashboard redirects to login for anonymous users."""
        response = client.get("/")
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_dashboard_loads_for_authenticated(self, client):
        """Test dashboard loads for authenticated users."""
        User.objects.create_user(username="testuser", password="testpass123")
        client.login(username="testuser", password="testpass123")
        response = client.get("/")
        assert response.status_code == 200
        assert "Kế toán SME" in response.content.decode()
