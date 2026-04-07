from flask import Blueprint, render_template
from flask_login import login_required

from app.middleware.authorization import require_permission

ap_bp = Blueprint("ap", __name__)


@ap_bp.route("/")
@login_required
@require_permission()
def index():
    return render_template("ap/index.html")


@ap_bp.route("/bills")
@login_required
@require_permission()
def bills():
    return render_template("ap/bills.html")


@ap_bp.route("/suppliers")
@login_required
@require_permission()
def suppliers():
    return render_template("ap/suppliers.html")
