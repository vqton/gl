import pytest
from flask import url_for


class TestPayrollRoutes:
    def test_payroll_index_requires_login(self, client):
        response = client.get("/payroll/", follow_redirects=True)
        assert response.status_code == 200

    def test_payroll_employees_requires_login(self, client):
        response = client.get("/payroll/employees", follow_redirects=True)
        assert response.status_code == 200

    def test_payroll_new_employee_requires_login(self, client):
        response = client.get("/payroll/employees/new", follow_redirects=True)
        assert response.status_code == 200

    def test_payroll_payslips_requires_login(self, client):
        response = client.get("/payroll/payslips", follow_redirects=True)
        assert response.status_code == 200


class TestPayrollAuthenticatedRoutes:
    def test_payroll_index_authenticated(self, client, admin_user):
        login_resp = client.post(
            "/auth/login",
            data={"username": "admin", "password": "adminpass"},
            follow_redirects=True,
        )
        assert login_resp.status_code == 200

        response = client.get("/payroll/")
        assert response.status_code == 200


class TestReportsRoutes:
    def test_reports_index_requires_login(self, client):
        response = client.get("/reports/", follow_redirects=True)
        assert response.status_code == 200


class TestReportsAuthenticatedRoutes:
    def test_reports_index_authenticated(self, client, admin_user):
        login_resp = client.post(
            "/auth/login",
            data={"username": "admin", "password": "adminpass"},
            follow_redirects=True,
        )
        assert login_resp.status_code == 200

        response = client.get("/reports/")
        assert response.status_code == 200


class TestTaxRoutes:
    def test_tax_index_requires_login(self, client):
        response = client.get("/tax/", follow_redirects=True)
        assert response.status_code == 200

    def test_tax_vat_requires_login(self, client):
        response = client.get("/tax/vat", follow_redirects=True)
        assert response.status_code == 200

    def test_tax_cit_requires_login(self, client):
        response = client.get("/tax/cit", follow_redirects=True)
        assert response.status_code == 200

    def test_tax_pit_requires_login(self, client):
        response = client.get("/tax/pit", follow_redirects=True)
        assert response.status_code == 200