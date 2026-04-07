from flask import Blueprint, render_template
from flask_login import login_required

from app.middleware.authorization import require_permission

inventory_bp = Blueprint("inventory", __name__)


@inventory_bp.route("/")
@login_required
@require_permission()
def index():
    return render_template("inventory/index.html")


@inventory_bp.route("/items")
@login_required
@require_permission()
def items():
    return render_template("inventory/items.html")


@inventory_bp.route("/movements")
@login_required
@require_permission()
def movements():
    return render_template("inventory/movements.html")
