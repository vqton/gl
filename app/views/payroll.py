from flask import Blueprint, render_template
from flask_login import login_required

from app.middleware.authorization import require_permission

payroll_bp = Blueprint("payroll", __name__)


@payroll_bp.route("/")
@login_required
@require_permission()
def index():
    return render_template("payroll/index.html")


@payroll_bp.route("/employees")
@login_required
@require_permission()
def employees():
    return render_template("payroll/employees.html")


@payroll_bp.route("/payslips")
@login_required
@require_permission()
def payslips():
    return render_template("payroll/payslips.html")
