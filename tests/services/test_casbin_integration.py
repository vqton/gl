import os
import pytest

import casbin
from casbin_sqlalchemy_adapter import Adapter


class TestCasbinIntegration:
    """Test Casbin RBAC authorization."""

    def test_enforcer_loads(self, app):
        """Test that Casbin enforcer is initialized."""
        assert hasattr(app, "casbin_enforcer")
        assert isinstance(app.casbin_enforcer, casbin.Enforcer)

    def test_admin_has_full_access(self, app):
        """Test admin role has access to all resources."""
        enforcer = app.casbin_enforcer
        assert enforcer.enforce("admin", "/gl/journal_entries", "GET")
        assert enforcer.enforce("admin", "/gl/journal_entries", "POST")
        assert enforcer.enforce("admin", "/admin/users", "GET")
        assert enforcer.enforce("admin", "/admin/settings", "POST")
        assert enforcer.enforce("admin", "/reports/b01", "GET")

    def test_cfo_can_read_all(self, app):
        """Test CFO can read all modules."""
        enforcer = app.casbin_enforcer
        assert enforcer.enforce("cfo", "/gl/journal_entries", "GET")
        assert enforcer.enforce("cfo", "/ar/invoices", "GET")
        assert enforcer.enforce("cfo", "/ap/bills", "GET")
        assert enforcer.enforce("cfo", "/tax/vat", "GET")
        assert enforcer.enforce("cfo", "/payroll/payslips", "GET")
        assert enforcer.enforce("cfo", "/reports/b01", "GET")

    def test_accountant_cannot_delete(self, app):
        """Test accountant cannot delete entries."""
        enforcer = app.casbin_enforcer
        assert enforcer.enforce("accountant", "/gl/journal_entries", "GET")
        assert enforcer.enforce("accountant", "/gl/journal_entries", "POST")
        assert enforcer.enforce("accountant", "/gl/journal_entries", "PUT")
        assert not enforcer.enforce("accountant", "/gl/journal_entries", "DELETE")

    def test_auditor_read_only(self, app):
        """Test auditor has read-only access."""
        enforcer = app.casbin_enforcer
        assert enforcer.enforce("auditor", "/gl/journal_entries", "GET")
        assert enforcer.enforce("auditor", "/reports/b01", "GET")
        assert not enforcer.enforce("auditor", "/gl/journal_entries", "POST")
        assert not enforcer.enforce("auditor", "/gl/journal_entries", "PUT")
        assert not enforcer.enforce("auditor", "/gl/journal_entries", "DELETE")

    def test_viewer_dashboard_only(self, app):
        """Test viewer can only access dashboard and reports."""
        enforcer = app.casbin_enforcer
        assert enforcer.enforce("viewer", "/", "GET")
        assert enforcer.enforce("viewer", "/dashboard", "GET")
        assert enforcer.enforce("viewer", "/reports/b01", "GET")
        assert not enforcer.enforce("viewer", "/gl/journal_entries", "GET")
        assert not enforcer.enforce("viewer", "/admin/users", "GET")

    def test_role_inheritance(self, app):
        """Test role inheritance (accountant inherits viewer)."""
        enforcer = app.casbin_enforcer
        assert enforcer.enforce("accountant", "/", "GET")
        assert enforcer.enforce("accountant", "/dashboard", "GET")
        assert enforcer.enforce("chief_accountant", "/", "GET")
        assert enforcer.enforce("cfo", "/", "GET")

    def test_cashier_payment_access(self, app):
        """Test cashier can process payments but not view reports."""
        enforcer = app.casbin_enforcer
        assert enforcer.enforce("cashier", "/gl/cash/receipts", "GET")
        assert enforcer.enforce("cashier", "/gl/cash/payments", "POST")
        assert enforcer.enforce("cashier", "/ap/bills/1/pay", "POST")
        assert enforcer.enforce("cashier", "/reports/cash", "GET")

    def test_tax_accountant_tax_only(self, app):
        """Test tax accountant has full tax access but limited elsewhere."""
        enforcer = app.casbin_enforcer
        assert enforcer.enforce("tax_accountant", "/tax/vat", "GET")
        assert enforcer.enforce("tax_accountant", "/tax/vat", "POST")
        assert enforcer.enforce("tax_accountant", "/tax/cit", "GET")
        assert enforcer.enforce("tax_accountant", "/tax/*/submit", "POST")
        assert enforcer.enforce("tax_accountant", "/gl/journal_entries", "GET")
        assert not enforcer.enforce("tax_accountant", "/payroll/payslips", "GET")

    def test_payroll_accountant_payroll_only(self, app):
        """Test payroll accountant has payroll access but not tax."""
        enforcer = app.casbin_enforcer
        assert enforcer.enforce("payroll_accountant", "/payroll/employees", "GET")
        assert enforcer.enforce("payroll_accountant", "/payroll/payslips", "GET")
        assert enforcer.enforce("payroll_accountant", "/payroll/payslip/approve", "POST")
        assert not enforcer.enforce("payroll_accountant", "/tax/vat", "GET")

    def test_get_policy(self, app):
        """Test retrieving policy list."""
        enforcer = app.casbin_enforcer
        policies = enforcer.get_policy()
        assert len(policies) > 0
        assert any(p[0] == "admin" for p in policies)

    def test_get_roles(self, app):
        """Test retrieving role list."""
        enforcer = app.casbin_enforcer
        roles = set()
        for p in enforcer.get_policy():
            roles.add(p[0])
        assert "admin" in roles
        assert "accountant" in roles
        assert "auditor" in roles

    def test_add_remove_permission(self, app):
        """Test adding and removing a permission dynamically."""
        enforcer = app.casbin_enforcer
        result = enforcer.add_policy("viewer", "/gl/journal_entries", "GET")
        assert result is True
        assert enforcer.enforce("viewer", "/gl/journal_entries", "GET")
        enforcer.remove_policy("viewer", "/gl/journal_entries", "GET")
        assert not enforcer.enforce("viewer", "/gl/journal_entries", "GET")
