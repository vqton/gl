"""Permission decorators for RBAC system."""

import functools
import logging

from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseForbidden

logger = logging.getLogger(__name__)


def require_role(role_ma):
    """
    Decorator that restricts access to users with a specific role.

    System admins implicitly have all roles.

    Args:
        role_ma: Role code (e.g., 'ke_toan_truong', 'thu_quy').

    Returns:
        Decorated view function that checks role before execution.
    """

    def decorator(view_func):
        @functools.wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if isinstance(user, AnonymousUser):
                logger.warning(
                    "Anonymous user blocked from %s",
                    request.path,
                )
                return HttpResponseForbidden("Bạn cần đăng nhập để truy cập trang này.")
            if not user.has_role(role_ma):
                logger.warning(
                    "User %s (role: %s) blocked from %s - requires role: %s",
                    user.username,
                    user.vai_tro.ma if user.vai_tro else "none",
                    request.path,
                    role_ma,
                )
                return HttpResponseForbidden(
                    f"Bạn không có quyền truy cập trang này. "
                    f"Yêu cầu vai trò: {role_ma}"
                )
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def can_delete_posted_voucher(view_func):
    """
    Decorator that blocks deletion of posted vouchers for non-chief users.

    Only ke_toan_truong (chief accountant) or system admins can delete
    vouchers with status 'posted'.

    Returns:
        Decorated view function that checks permission before deletion.
    """

    @functools.wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if isinstance(user, AnonymousUser):
            logger.warning(
                "Anonymous user blocked from deleting voucher at %s",
                request.path,
            )
            return HttpResponseForbidden("Bạn cần đăng nhập để thực hiện thao tác này.")
        if not user.is_ke_toan_truong:
            logger.warning(
                "User %s blocked from deleting posted voucher at %s",
                user.username,
                request.path,
            )
            return HttpResponseForbidden(
                "Bạn không được xóa chứng từ đã ghi sổ. "
                "Chỉ Kế toán trưởng mới có quyền này."
            )
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def salary_access(view_func):
    """
    Decorator that restricts access to payroll module.

    Only ke_toan_truong (chief accountant) or system admins can access
    payroll data.

    Returns:
        Decorated view function that checks salary access permission.
    """

    @functools.wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if isinstance(user, AnonymousUser):
            logger.warning(
                "Anonymous user blocked from payroll at %s",
                request.path,
            )
            return HttpResponseForbidden("Bạn cần đăng nhập để truy cập module lương.")
        if not user.is_ke_toan_truong:
            logger.warning(
                "User %s blocked from payroll at %s",
                user.username,
                request.path,
            )
            return HttpResponseForbidden(
                "Bạn không có quyền truy cập thông tin lương. "
                "Chỉ Kế toán trưởng mới có quyền này."
            )
        return view_func(request, *args, **kwargs)

    return _wrapped_view
