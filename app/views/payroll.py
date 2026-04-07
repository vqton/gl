from datetime import date

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.middleware.authorization import require_permission
from app.services.payroll_service import EmployeeService, PayrollService

payroll_bp = Blueprint("payroll", __name__)


@payroll_bp.route("/")
@login_required
@require_permission()
def index():
    period = request.args.get("period", date.today().strftime("%Y-%m"))
    summary = PayrollService.get_payroll_summary(period)
    return render_template("payroll/index.html", summary=summary, period=period)


@payroll_bp.route("/employees")
@login_required
@require_permission()
def employees():
    employees = EmployeeService.get_all()
    return render_template("payroll/employees.html", employees=employees)


@payroll_bp.route("/employees/new", methods=["GET", "POST"])
@login_required
@require_permission()
def new_employee():
    if request.method == "POST":
        try:
            hire_str = request.form.get("hire_date")
            hire_date = date.fromisoformat(hire_str) if hire_str else date.today()
            dob_str = request.form.get("date_of_birth")
            dob = date.fromisoformat(dob_str) if dob_str else None
            ins_salary = request.form.get("insurance_salary")
            EmployeeService.create(
                employee_code=request.form["employee_code"],
                full_name=request.form["full_name"],
                hire_date=hire_date,
                gross_salary=float(request.form["gross_salary"]),
                department=request.form.get("department", ""),
                position=request.form.get("position", ""),
                contract_type=request.form.get("contract_type", "indefinite"),
                date_of_birth=dob,
                id_number=request.form.get("id_number", ""),
                address=request.form.get("address", ""),
                phone=request.form.get("phone", ""),
                email=request.form.get("email", ""),
                tax_code=request.form.get("tax_code", ""),
                bank_account=request.form.get("bank_account", ""),
                bank_name=request.form.get("bank_name", ""),
                dependents=int(request.form.get("dependents", 0)),
                is_insured=request.form.get("is_insured") == "on",
                insurance_salary=float(ins_salary) if ins_salary else None,
                salary_allowance=float(request.form.get("salary_allowance", 0)),
            )
            flash("Đã tạo nhân viên.", "success")
            return redirect(url_for("payroll.employees"))
        except ValueError as e:
            flash(str(e), "danger")
    return render_template("payroll/employee_form.html")


@payroll_bp.route("/payslips")
@login_required
@require_permission()
def payslips():
    period = request.args.get("period", date.today().strftime("%Y-%m"))
    payslips = PayrollService.get_payslips(period=period)
    employees = EmployeeService.get_all()
    return render_template(
        "payroll/payslips.html",
        payslips=payslips,
        period=period,
        employees=employees,
    )


@payroll_bp.route("/payslips/new", methods=["GET", "POST"])
@login_required
@require_permission()
def new_payslip():
    if request.method == "POST":
        try:
            period = request.form["period"]
            employee_id = int(request.form["employee_id"])
            working_days = int(request.form.get("working_days", 26))
            actual_days = int(request.form.get("actual_days", 26))
            overtime_hours = float(request.form.get("overtime_hours", 0))
            allowance = float(request.form.get("allowance", 0))
            bonus = float(request.form.get("bonus", 0))
            notes = request.form.get("notes", "")
            payslip = PayrollService.create_payslip(
                employee_id=employee_id,
                period=period,
                working_days=working_days,
                actual_days=actual_days,
                overtime_hours=overtime_hours,
                allowance=allowance,
                bonus=bonus,
                notes=notes,
            )
            flash(f"Bảng lương cho kỳ {period} đã được tạo.", "success")
            return redirect(url_for("payroll.payslips"))
        except ValueError as e:
            flash(str(e), "danger")
    employees = EmployeeService.get_all()
    return render_template("payroll/payslip_form.html", employees=employees)


@payroll_bp.route("/payslips/<int:payslip_id>/approve", methods=["POST"])
@login_required
@require_permission()
def approve_payslip(payslip_id):
    try:
        PayrollService.approve_payslip(payslip_id)
        flash("Đã duyệt bảng lương.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("payroll.payslips"))
