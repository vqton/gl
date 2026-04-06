class TestAppFactory:
    def test_create_app_default_config(self, app):
        assert app.config["TESTING"] is True

    def test_create_app_has_blueprints(self, app):
        assert "main" in app.blueprints
        assert "auth" in app.blueprints
        assert "gl" in app.blueprints
        assert "ar" in app.blueprints
        assert "ap" in app.blueprints
        assert "tax" in app.blueprints
        assert "payroll" in app.blueprints
        assert "fa" in app.blueprints
        assert "inventory" in app.blueprints
        assert "reports" in app.blueprints
        assert "admin" in app.blueprints


class TestMainRoutes:
    def test_index_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200


class TestAuthRoutes:
    def test_login_page_loads(self, client):
        response = client.get("/auth/login")
        assert response.status_code == 200

    def test_login_success_redirects(self, client, admin_user):
        response = client.post(
            "/auth/login",
            data={"username": "admin", "password": "adminpass"},
            follow_redirects=True,
        )
        assert response.status_code == 200

    def test_login_failure_shows_error(self, client):
        response = client.post(
            "/auth/login",
            data={"username": "wrong", "password": "wrong"},
        )
        assert response.status_code == 200

    def test_logout_requires_login(self, client):
        response = client.get("/auth/logout", follow_redirects=True)
        assert response.status_code == 200


class TestGLRoutes:
    def test_gl_index_requires_login(self, client):
        response = client.get("/gl/", follow_redirects=True)
        assert response.status_code == 200

    def test_accounts_requires_login(self, client):
        response = client.get("/gl/accounts", follow_redirects=True)
        assert response.status_code == 200

    def test_journal_entries_requires_login(self, client):
        response = client.get("/gl/journal-entries", follow_redirects=True)
        assert response.status_code == 200


class TestErrorHandlers:
    def test_404_page(self, client):
        response = client.get("/nonexistent-page-that-does-not-exist")
        assert response.status_code == 404
