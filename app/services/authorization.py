"""Centralized Authorization Service combining RBAC and rule-based checks.

Orchestrates Casbin RBAC policy evaluation with domain-specific RuleEngine
checks to enforce Segregation of Duties, period locks, and amount thresholds
in a single authorization decision point.
"""

from app.services.casbin_service import CasbinService
from app.services.rule_engine import RuleEngine


class AuthorizationService:
    """Unified authorization service for the accounting application.

    Combines role-based access control (Casbin) with attribute-based
    rules (RuleEngine) to produce comprehensive authorization decisions
    that satisfy Circular 99/2025/TT-BTC compliance requirements.
    """

    @staticmethod
    def check_permission(user, action, resource=None, context=None):
        """Evaluate whether a user is permitted to perform an action.

        Authorization is evaluated in two stages:
        1. RBAC check via Casbin — if the resource is a URL string (request-level
           context), Casbin policies are checked. If denied, the request is rejected.
        2. RuleEngine checks — domain-specific rules are evaluated based on the
           action type (approve, execute) and resource attributes.

        When called from the service layer with a domain object, the RBAC check
        is skipped because it was already enforced at the view/middleware layer.
        Only RuleEngine checks (SoD, period lock) are applied.

        Args:
            user: The authenticated user object. Must have a ``get_all_roles()``
                method returning a set of role names, and an ``id`` attribute.
            action: The action being attempted (e.g. 'approve', 'execute', 'create').
            resource: Optional domain object (e.g. JournalEntry) or URL string
                being acted upon. Used for SoD and period lock checks.
            context: Optional dict with additional request context (e.g. request
                path, HTTP method). Reserved for future ABAC extensions.

        Returns:
            bool: True if the user is authorized, False otherwise.
        """
        if context is None:
            context = {}

        user_roles = user.get_all_roles() if hasattr(user, "get_all_roles") else set()

        rbac_resource = context.get("resource", resource)

        if isinstance(rbac_resource, str):
            rbac_action = context.get("action", action)
            rbac_allowed = any(
                CasbinService.check_permission(role, rbac_resource, rbac_action)
                for role in user_roles
            )
            if not rbac_allowed:
                return False

        if action == "approve" and resource is not None:
            result = RuleEngine.check_sod_creator_approver(user, resource)
            if not result["allowed"]:
                return False

        if action == "execute" and resource is not None:
            result = RuleEngine.check_sod_approver_executor(user, resource)
            if not result["allowed"]:
                return False

        if resource is not None:
            result = RuleEngine.check_period_lock(resource)
            if not result["allowed"]:
                return False

        return True

    @staticmethod
    def enforce(user, action, resource, context=None):
        """Enforce authorization, raising PermissionError on denial.

        A convenience wrapper around ``check_permission`` that raises an
        exception rather than returning a boolean, suitable for use in
        service-layer methods where a failed authorization should halt
        execution.

        Args:
            user: The authenticated user object.
            action: The action being attempted.
            resource: The domain object being acted upon.
            context: Optional dict with additional request context.

        Raises:
            PermissionError: If the user is not authorized for the action.
        """
        allowed = AuthorizationService.check_permission(
            user, action, resource=resource, context=context
        )
        if not allowed:
            raise PermissionError(
                f"User {user.id} is not authorized to {action} " f"on {type(resource).__name__}."
            )
