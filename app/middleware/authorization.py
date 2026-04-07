"""Authorization middleware for Flask using Casbin RBAC and Rule Engine."""

from functools import wraps

from flask import abort, flash, redirect, request, url_for
from flask_login import current_user


def require_permission(resource=None, action=None):
    """
    Decorator to enforce authorization on a route using RBAC + RuleEngine.

    Checks ALL user roles (primary + assigned) — if ANY role grants
    access, the request is allowed. Then applies RuleEngine checks
    (SoD, period lock, amount threshold) via AuthorizationService.

    Usage:
        @require_permission()  # Auto-detect from request path and method
        @require_permission(resource="/gl/*", action="GET")
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("auth.login"))

            target_resource = resource or request.path
            target_action = action or request.method

            from app.services.authorization import AuthorizationService

            context = {
                "resource": target_resource,
                "action": target_action,
                "request_path": request.path,
                "request_method": request.method,
            }

            allowed = AuthorizationService.check_permission(
                current_user,
                target_action,
                resource=target_resource,
                context=context,
            )

            if not allowed:
                flash("Bạn không có quyền truy cập chức năng này.", "danger")
                abort(403)

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def has_permission(user, resource, action):
    """Helper function to check permission for a user object."""
    from app.services.authorization import AuthorizationService

    return AuthorizationService.check_permission(user, action, resource=resource)
