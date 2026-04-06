from flask import Blueprint, render_template
from flask_login import login_required

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/")
@login_required
def index():
    return render_template("admin/index.html")


@admin_bp.route("/users")
@login_required
def users():
    return render_template("admin/users.html")


@admin_bp.route("/settings")
@login_required
def settings():
    return render_template("admin/settings.html")
