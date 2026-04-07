from flask import Blueprint
from flask_login import login_required

from app.middleware.authorization import require_permission
from app.services.casbin_service import CasbinService

permissions_bp = Blueprint("permissions", __name__, url_prefix="/admin/permissions")


@permissions_bp.route("/")
@login_required
@require_permission()
def index():
    """Permission management dashboard."""
    roles = CasbinService.get_all_roles()
    hierarchy = CasbinService.get_role_hierarchy()
    all_permissions = CasbinService.get_all_permissions()

    permissions_by_role = {}
    for perm in all_permissions:
        role = perm["role"]
        if role not in permissions_by_role:
            permissions_by_role[role] = []
        permissions_by_role[role].append(perm)

    return render_template(
        "admin/permissions.html",
        roles=roles,
        hierarchy=hierarchy,
        permissions_by_role=permissions_by_role,
    )


@permissions_bp.route("/<role>")
@login_required
@require_permission()
def view_role(role):
    """View permissions for a specific role."""
    permissions = CasbinService.get_role_permissions(role)
    return render_template(
        "admin/permissions_detail.html",
        role=role,
        permissions=permissions,
    )


@permissions_bp.route("/add", methods=["POST"])
@login_required
@require_permission()
def add_permission():
    """Add a permission to a role."""
    role = request.form.get("role")
    resource = request.form.get("resource")
    action = request.form.get("action")

    if not all([role, resource, action]):
        flash("Vui lòng điền đầy đủ thông tin.", "danger")
        return redirect(url_for("permissions.index"))

    result = CasbinService.add_permission(role, resource, action)
    if result:
        flash(f"Đã thêm quyền: {role} → {resource} ({action})", "success")
    else:
        flash("Quyền đã tồn tại.", "warning")

    return redirect(url_for("permissions.index"))


@permissions_bp.route("/remove", methods=["POST"])
@login_required
@require_permission()
def remove_permission():
    """Remove a permission from a role."""
    role = request.form.get("role")
    resource = request.form.get("resource")
    action = request.form.get("action")

    result = CasbinService.remove_permission(role, resource, action)
    if result:
        flash(f"Đã xóa quyền: {role} → {resource} ({action})", "success")
    else:
        flash("Không tìm thấy quyền để xóa.", "warning")

    return redirect(url_for("permissions.index"))


@permissions_bp.route("/hierarchy/add", methods=["POST"])
@login_required
@require_permission()
def add_hierarchy():
    """Add role inheritance."""
    child = request.form.get("child_role")
    parent = request.form.get("parent_role")

    result = CasbinService.add_role_inheritance(child, parent)
    if result:
        flash(f"Đã phân quyền: {child} kế thừa {parent}", "success")
    else:
        flash("Phân quyền đã tồn tại.", "warning")

    return redirect(url_for("permissions.index"))
