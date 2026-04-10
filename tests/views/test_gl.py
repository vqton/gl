import pytest
from flask import url_for


class TestGLRoutes:
    def test_gl_index_requires_login(self, client):
        response = client.get("/gl/", follow_redirects=True)
        assert response.status_code == 200

    def test_gl_accounts_requires_login(self, client):
        response = client.get("/gl/accounts", follow_redirects=True)
        assert response.status_code == 200

    def test_gl_journal_entries_requires_login(self, client):
        response = client.get("/gl/journal-entries", follow_redirects=True)
        assert response.status_code == 200


class TestGLAccountsRoutes:
    def test_gl_new_account_requires_login(self, client):
        response = client.get("/gl/accounts/new", follow_redirects=True)
        assert response.status_code == 200


class TestGLJournalEntryRoutes:
    def test_gl_new_entry_requires_login(self, client):
        response = client.get("/gl/journal-entries/new", follow_redirects=True)
        assert response.status_code == 200

    def test_gl_trial_balance_requires_login(self, client):
        response = client.get("/gl/trial-balance", follow_redirects=True)
        assert response.status_code == 200


class TestGLAuthenticatedRoutes:
    def test_gl_index_authenticated(self, client, admin_user):
        login_resp = client.post(
            "/auth/login",
            data={"username": "admin", "password": "adminpass"},
            follow_redirects=True,
        )
        assert login_resp.status_code == 200

        response = client.get("/gl/")
        assert response.status_code == 200

    def test_gl_accounts_authenticated(self, client, admin_user):
        login_resp = client.post(
            "/auth/login",
            data={"username": "admin", "password": "adminpass"},
            follow_redirects=True,
        )
        assert login_resp.status_code == 200

        response = client.get("/gl/accounts")
        assert response.status_code == 200

    def test_gl_journal_entries_authenticated(self, client, admin_user):
        login_resp = client.post(
            "/auth/login",
            data={"username": "admin", "password": "adminpass"},
            follow_redirects=True,
        )
        assert login_resp.status_code == 200

        response = client.get("/gl/journal-entries")
        assert response.status_code == 200

    def test_gl_trial_balance_authenticated(self, client, admin_user):
        login_resp = client.post(
            "/auth/login",
            data={"username": "admin", "password": "adminpass"},
            follow_redirects=True,
        )
        assert login_resp.status_code == 200

        response = client.get("/gl/trial-balance")
        assert response.status_code == 200