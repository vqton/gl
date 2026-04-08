import pytest
from flask import url_for


class TestARRoutes:
    def test_ar_index_requires_login(self, client):
        response = client.get("/ar/", follow_redirects=True)
        assert response.status_code == 200
        # Should redirect to login page
        assert b"Sign In" in response.data or b"login" in response.data.lower()

    def test_ar_index_authenticated(self, client, accountant_user):
        # Login first
        login_resp = client.post(
            "/auth/login",
            data={"username": "accountant", "password": "accountantpass"},
            follow_redirects=True,
        )
        assert login_resp.status_code == 200

        # Now access AR index
        response = client.get("/ar/")
        assert response.status_code == 200
        # Check for common AR page elements
        assert b"index" in response.data.lower() or b"ar" in response.data.lower()

    def test_ar_invoices_authenticated(self, client, accountant_user):
        # Login first
        login_resp = client.post(
            "/auth/login",
            data={"username": "accountant", "password": "accountantpass"},
            follow_redirects=True,
        )
        assert login_resp.status_code == 200

        # Now access AR invoices
        response = client.get("/ar/invoices")
        assert response.status_code == 200
        # Check for common invoices page elements
        assert b"invoices" in response.data.lower() or b"invoice" in response.data.lower()

    def test_ar_customers_authenticated(self, client, accountant_user):
        # Login first
        login_resp = client.post(
            "/auth/login",
            data={"username": "accountant", "password": "accountantpass"},
            follow_redirects=True,
        )
        assert login_resp.status_code == 200

        # Now access AR customers
        response = client.get("/ar/customers")
        assert response.status_code == 200
        # Check for common customers page elements
        assert b"customers" in response.data.lower() or b"customer" in response.data.lower()

    def test_ar_new_invoice_requires_login(self, client):
        response = client.get("/ar/invoices/new", follow_redirects=True)
        assert response.status_code == 200
        # Should redirect to login page
        assert b"Sign In" in response.data or b"login" in response.data.lower()

    def test_ar_new_customer_requires_login(self, client):
        response = client.get("/ar/customers/new", follow_redirects=True)
        assert response.status_code == 200
        # Should redirect to login page
        assert b"Sign In" in response.data or b"login" in response.data.lower()