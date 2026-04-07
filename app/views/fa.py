from flask import Blueprint, render_template
from flask_login import login_required

from app.middleware.authorization import require_permission

fa_bp = Blueprint("fa", __name__)


@fa_bp.route("/")
@login_required
@require_permission()
def index():
    return render_template("fa/index.html")


@fa_bp.route("/assets")
@login_required
@require_permission()
def assets():
    return render_template("fa/assets.html")


@fa_bp.route("/depreciation")
@login_required
@require_permission()
def depreciation():
    return render_template("fa/depreciation.html")
