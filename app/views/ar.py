from flask import Blueprint, render_template
from flask_login import login_required

from app.middleware.authorization import require_permission

ar_bp = Blueprint("ar", __name__)


@ar_bp.route("/")
@login_required
@require_permission()
def index():
    return render_template("ar/index.html")


@ar_bp.route("/invoices")
@login_required
@require_permission()
def invoices():
    return render_template("ar/invoices.html")


@ar_bp.route("/customers")
@login_required
@require_permission()
def customers():
    return render_template("ar/customers.html")
