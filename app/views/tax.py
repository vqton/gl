from flask import Blueprint, render_template
from flask_login import login_required

from app.middleware.authorization import require_permission

tax_bp = Blueprint("tax", __name__)


@tax_bp.route("/")
@login_required
@require_permission()
def index():
    return render_template("tax/index.html")


@tax_bp.route("/vat")
@login_required
@require_permission()
def vat():
    return render_template("tax/vat.html")


@tax_bp.route("/cit")
@login_required
@require_permission()
def cit():
    return render_template("tax/cit.html")


@tax_bp.route("/pit")
@login_required
@require_permission()
def pit():
    return render_template("tax/pit.html")
