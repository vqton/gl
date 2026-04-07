"""System Administration Blueprint.

Handles user management, role management, accounting periods, audit logs, and system settings.
All routes are protected by Casbin RBAC authorization.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.middleware.authorization import require_permission
from app.services.admin_service import AdminUserService, AdminRoleService, AuditLogService
from app.services.casbin_service import CasbinService
from app.services.period_service import PeriodService

admin_bp = Blueprint("admin", __name__)


# ──────────────────────────────────────────────
# Dashboard
# ──────────────────────────────────────────────

@admin_bp.route("/")
@login_required
@require_permission()
def index():
    users = AdminUserService.get_all()
    roles = AdminRoleService.get_all()
    return render_template(
        "admin/index.html",
        users=users,
        roles=roles,
    )


# ──────────────────────────────────────────────
# User Management
# ──────────────────────────────────────────────

@admin_bp.route("/users")
@login_required
@require_permission()
def users():
    users = AdminUserService.get_all(active_only=False)
    all_roles = AdminRoleService.get_all()
    return render_template(
        "admin/users.html",
        users=users,
        all_roles=all_roles,
    )


@admin_bp.route("/users/new", methods=["GET", "POST"])
@login_required
@require_permission()
def new_user():
    if request.method == "POST":
        try:
            additional_roles = request.form.getlist("additional_roles")
            AdminUserService.create(
                username=request.form["username"],
                email=request.form["email"],
                password=request.form["password"],
                full_name=request.form["full_name"],
                role=request.form.get("role", "accountant"),
                additional_roles=additional_roles if additional_roles else None,
            )
            flash("Đã tạo người dùng thành công.", "success")
            return redirect(url_for("admin.users"))
        except ValueError as e:
            flash(str(e), "danger")

    all_roles = AdminRoleService.get_all()
    return render_template("admin/user_form.html", all_roles=all_roles)


@admin_bp.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
@require_permission()
def edit_user(user_id):
    user = AdminUserService.get_by_id(user_id)
    if not user:
        flash("Không tìm thấy người dùng.", "danger")
        return redirect(url_for("admin.users"))

    if request.method == "POST":
        try:
            AdminUserService.update(
                user_id,
                full_name=request.form.get("full_name"),
                email=request.form.get("email"),
                is_active=request.form.get("is_active") == "on",
            )
            AdminUserService.change_role(user_id, request.form.get("role", user.role))
            AdminUserService.assign_roles(user_id, request.form.getlist("additional_roles"))
            flash("Đã cập nhật người dùng.", "success")
            return redirect(url_for("admin.users"))
        except ValueError as e:
            flash(str(e), "danger")

    all_roles = AdminRoleService.get_all()
    return render_template(
        "admin/user_form.html",
        user=user,
        all_roles=all_roles,
    )


@admin_bp.route("/users/<int:user_id>/deactivate", methods=["POST"])
@login_required
@require_permission()
def deactivate_user(user_id):
    try:
        AdminUserService.deactivate(user_id)
        flash("Đã vô hiệu hóa người dùng.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("admin.users"))


# ──────────────────────────────────────────────
# Role Management
# ──────────────────────────────────────────────

@admin_bp.route("/roles")
@login_required
@require_permission()
def roles():
    roles = AdminRoleService.get_all()
    role_permissions = {}
    for role in roles:
        role_permissions[role.name] = CasbinService.get_role_permissions(role.name)
    hierarchy = CasbinService.get_role_hierarchy()
    return render_template(
        "admin/roles.html",
        roles=roles,
        role_permissions=role_permissions,
        hierarchy=hierarchy,
    )


@admin_bp.route("/roles/<role_name>")
@login_required
@require_permission()
def view_role(role_name):
    role = AdminRoleService.get_by_name(role_name)
    if not role:
        flash("Không tìm thấy vai trò.", "danger")
        return redirect(url_for("admin.roles"))

    permissions = CasbinService.get_role_permissions(role_name)
    users = AdminRoleService.get_users_with_role(role_name)
    return render_template(
        "admin/role_detail.html",
        role=role,
        permissions=permissions,
        users=users,
    )


# ──────────────────────────────────────────────
# Accounting Period Management
# ──────────────────────────────────────────────

@admin_bp.route("/periods")
@login_required
@require_permission()
def periods():
    all_periods = PeriodService.get_all()
    current = PeriodService.get_current()
    return render_template(
        "admin/periods.html",
        periods=all_periods,
        current=current,
    )


@admin_bp.route("/periods/open", methods=["POST"])
@login_required
@require_permission()
def open_period():
    period_str = request.form.get("period")
    try:
        PeriodService.open_period(period_str, current_user.id)
        flash(f"Đã mở kỳ {period_str}.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("admin.periods"))


@admin_bp.route("/periods/<period_str>/lock", methods=["POST"])
@login_required
@require_permission()
def lock_period(period_str):
    try:
        PeriodService.lock_period(period_str, current_user.id)
        flash(f"Đã khóa tạm thời kỳ {period_str}.", "warning")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("admin.periods"))


@admin_bp.route("/periods/<period_str>/close", methods=["POST"])
@login_required
@require_permission()
def close_period(period_str):
    try:
        PeriodService.close_period(period_str, current_user.id)
        flash(f"Đã khóa cứng kỳ {period_str}.", "danger")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("admin.periods"))


@admin_bp.route("/periods/auto-create", methods=["POST"])
@login_required
@require_permission()
def auto_create_periods():
    months = request.form.get("months", 12, type=int)
    created = PeriodService.auto_create_periods(months)
    flash(f"Đã tạo {created} kỳ kế toán.", "success")
    return redirect(url_for("admin.periods"))


# ──────────────────────────────────────────────
# Audit Log
# ──────────────────────────────────────────────

@admin_bp.route("/audit-log")
@login_required
@require_permission()
def audit_log():
    entity_type = request.args.get("entity_type")
    limit = request.args.get("limit", 200, type=int)
    logs = AuditLogService.get_logs(entity_type=entity_type, limit=limit)
    return render_template("admin/audit_log.html", logs=logs)


# ──────────────────────────────────────────────
# Settings
# ──────────────────────────────────────────────

@admin_bp.route("/settings")
@login_required
@require_permission()
def settings():
    return render_template("admin/settings.html")
