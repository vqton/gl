import pytest
from flask import url_for


class TestFARRoutes:
    def test_fa_index_requires_login(self, client):
        response = client.get("/fa/", follow_redirects=True)
        assert response.status_code == 200

    def test_fa_assets_requires_login(self, client):
        response = client.get("/fa/assets", follow_redirects=True)
        assert response.status_code == 200

    def test_fa_new_asset_requires_login(self, client):
        response = client.get("/fa/assets/new", follow_redirects=True)
        assert response.status_code == 200

    def test_fa_depreciation_requires_login(self, client):
        response = client.get("/fa/depreciation", follow_redirects=True)
        assert response.status_code == 200


class TestFAAuthenticatedRoutes:
    def test_fa_index_authenticated(self, client, admin_user):
        login_resp = client.post(
            "/auth/login",
            data={"username": "admin", "password": "adminpass"},
            follow_redirects=True,
        )
        assert login_resp.status_code == 200

        response = client.get("/fa/")
        assert response.status_code == 200

    def test_fa_assets_authenticated(self, client, admin_user):
        login_resp = client.post(
            "/auth/login",
            data={"username": "admin", "password": "adminpass"},
            follow_redirects=True,
        )
        assert login_resp.status_code == 200

        response = client.get("/fa/assets")
        assert response.status_code == 200


class TestInventoryRoutes:
    def test_inventory_index_requires_login(self, client):
        response = client.get("/inventory/", follow_redirects=True)
        assert response.status_code == 200

    def test_inventory_items_requires_login(self, client):
        response = client.get("/inventory/items", follow_redirects=True)
        assert response.status_code == 200

    def test_inventory_new_item_requires_login(self, client):
        response = client.get("/inventory/items/new", follow_redirects=True)
        assert response.status_code == 200


class TestInventoryAuthenticatedRoutes:
    def test_inventory_index_authenticated(self, client, admin_user):
        login_resp = client.post(
            "/auth/login",
            data={"username": "admin", "password": "adminpass"},
            follow_redirects=True,
        )
        assert login_resp.status_code == 200

        response = client.get("/inventory/")
        assert response.status_code == 200

    def test_inventory_items_authenticated(self, client, admin_user):
        login_resp = client.post(
            "/auth/login",
            data={"username": "admin", "password": "adminpass"},
            follow_redirects=True,
        )
        assert login_resp.status_code == 200

        response = client.get("/inventory/items")
        assert response.status_code == 200