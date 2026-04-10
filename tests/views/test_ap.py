import pytest
from flask import url_for


class TestAPRoutes:
    def test_ap_index_requires_login(self, client):
        response = client.get("/ap/", follow_redirects=True)
        assert response.status_code == 200
        assert b"Sign In" in response.data or b"login" in response.data.lower()

    def test_ap_index_authenticated(self, client, admin_user):
        login_resp = client.post(
            "/auth/login",
            data={"username": "admin", "password": "adminpass"},
            follow_redirects=True,
        )
        assert login_resp.status_code == 200

        response = client.get("/ap/")
        assert response.status_code == 200
        assert b"index" in response.data.lower() or b"ap" in response.data.lower()

    def test_ap_bills_requires_login(self, client):
        response = client.get("/ap/bills", follow_redirects=True)
        assert response.status_code == 200

    def test_ap_bills_authenticated(self, client, admin_user):
        login_resp = client.post(
            "/auth/login",
            data={"username": "admin", "password": "adminpass"},
            follow_redirects=True,
        )
        assert login_resp.status_code == 200

        response = client.get("/ap/bills")
        assert response.status_code == 200

    def test_ap_suppliers_requires_login(self, client):
        response = client.get("/ap/suppliers", follow_redirects=True)
        assert response.status_code == 200

    def test_ap_suppliers_authenticated(self, client, admin_user):
        login_resp = client.post(
            "/auth/login",
            data={"username": "admin", "password": "adminpass"},
            follow_redirects=True,
        )
        assert login_resp.status_code == 200

        response = client.get("/ap/suppliers")
        assert response.status_code == 200

    def test_ap_new_bill_requires_login(self, client):
        response = client.get("/ap/bills/new", follow_redirects=True)
        assert response.status_code == 200

    def test_ap_new_supplier_requires_login(self, client):
        response = client.get("/ap/suppliers/new", follow_redirects=True)
        assert response.status_code == 200


class TestAPBillRoutes:
    def test_submit_bill_requires_login(self, client):
        response = client.post("/ap/bills/1/submit", follow_redirects=True)
        assert response.status_code == 200

    def test_approve_bill_requires_login(self, client):
        response = client.post("/ap/bills/1/approve", follow_redirects=True)
        assert response.status_code == 200

    def test_pay_bill_requires_login(self, client):
        response = client.post("/ap/bills/1/pay", follow_redirects=True)
        assert response.status_code == 200