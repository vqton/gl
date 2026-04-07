from flask import Blueprint, render_template
from flask_login import login_required

from app.middleware.authorization import require_permission

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("main/index.html")


@main_bp.route("/dashboard")
@login_required
@require_permission()
def dashboard():
    return render_template("main/dashboard.html")
