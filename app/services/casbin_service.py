import os

import casbin
from casbin_sqlalchemy_adapter import Adapter
from flask import current_app, g

from app.extensions import db
from app.models.casbin_rule import CasbinRule


def init_casbin(app):
    """Initialize Casbin enforcer with SQLAlchemy adapter."""
    with app.app_context():
        adapter = Adapter(db.engine)
        model_path = os.path.join(app.root_path, "..", "rbac_model.conf")
        enforcer = casbin.Enforcer(model_path, adapter)

        if not app.config.get("TESTING", False):
            if not enforcer.get_policy():
                policy_path = os.path.join(app.root_path, "..", "rbac_policy.csv")
                enforcer.load_policy()
                enforcer.save_policy()

        app.casbin_enforcer = enforcer


def get_enforcer():
    """Get Casbin enforcer from app context."""
    if "casbin_enforcer" not in g:
        g.casbin_enforcer = current_app.casbin_enforcer
    return g.casbin_enforcer


class CasbinService:
    """Service layer for Casbin policy management."""

    @staticmethod
    def check_permission(user_role, resource, action):
        """Check if a role has permission for a resource and action."""
        enforcer = get_enforcer()
        return enforcer.enforce(user_role, resource, action)

    @staticmethod
    def get_role_permissions(role):
        """Get all permissions for a specific role."""
        enforcer = get_enforcer()
        policies = enforcer.get_filtered_policy(0, role)
        return [{"resource": p[1], "action": p[2]} for p in policies if len(p) >= 3]

    @staticmethod
    def get_all_roles():
        """Get all roles defined in the policy."""
        enforcer = get_enforcer()
        roles = set()
        for policy in enforcer.get_policy():
            if policy[0] not in ["admin", "cfo", "chief_accountant", "accountant",
                                  "tax_accountant", "payroll_accountant", "cashier",
                                  "auditor", "viewer"]:
                continue
            roles.add(policy[0])
        return sorted(roles)

    @staticmethod
    def get_role_hierarchy():
        """Get role inheritance relationships."""
        enforcer = get_enforcer()
        return [{"child": g[0], "parent": g[1]} for g in enforcer.get_grouping_policy()]

    @staticmethod
    def add_permission(role, resource, action):
        """Add a permission to a role."""
        enforcer = get_enforcer()
        result = enforcer.add_policy(role, resource, action)
        if result:
            enforcer.save_policy()
        return result

    @staticmethod
    def remove_permission(role, resource, action):
        """Remove a permission from a role."""
        enforcer = get_enforcer()
        result = enforcer.remove_policy(role, resource, action)
        if result:
            enforcer.save_policy()
        return result

    @staticmethod
    def add_role_inheritance(child_role, parent_role):
        """Add role inheritance (child inherits parent's permissions)."""
        enforcer = get_enforcer()
        result = enforcer.add_grouping_policy(child_role, parent_role)
        if result:
            enforcer.save_policy()
        return result

    @staticmethod
    def remove_role_inheritance(child_role, parent_role):
        """Remove role inheritance."""
        enforcer = get_enforcer()
        result = enforcer.remove_grouping_policy(child_role, parent_role)
        if result:
            enforcer.save_policy()
        return result

    @staticmethod
    def get_all_permissions():
        """Get all permissions in the system."""
        enforcer = get_enforcer()
        policies = enforcer.get_policy()
        return [{"role": p[0], "resource": p[1], "action": p[2]} for p in policies if len(p) >= 3]
