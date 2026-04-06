from flask import Blueprint, render_template

payroll_bp = Blueprint("payroll", __name__)


@payroll_bp.route("/")
def index():
    return render_template("payroll/index.html")


@payroll_bp.route("/employees")
def employees():
    return render_template("payroll/employees.html")


@payroll_bp.route("/payslips")
def payslips():
    return render_template("payroll/payslips.html")
