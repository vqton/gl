from flask import Blueprint, render_template
from flask_login import login_required

from app.middleware.authorization import require_permission

reports_bp = Blueprint("reports", __name__)


@reports_bp.route("/")
@login_required
@require_permission()
def index():
    return render_template("reports/index.html")


@reports_bp.route("/financial-statements")
@login_required
@require_permission()
def financial_statements():
    return render_template("reports/financial_statements.html")


@reports_bp.route("/b01")
@login_required
@require_permission()
def b01():
    return render_template("reports/b01.html")


@reports_bp.route("/b02")
@login_required
@require_permission()
def b02():
    return render_template("reports/b02.html")


@reports_bp.route("/b03")
@login_required
@require_permission()
def b03():
    return render_template("reports/b03.html")


@reports_bp.route("/b09")
@login_required
@require_permission()
def b09():
    return render_template("reports/b09.html")
