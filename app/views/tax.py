from datetime import date

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.middleware.authorization import require_permission
from app.services.tax_service import TaxService

tax_bp = Blueprint("tax", __name__)


@tax_bp.route("/")
@login_required
@require_permission()
def index():
    period = request.args.get("period", date.today().strftime("%Y-%m"))
    dashboard = TaxService.get_tax_dashboard(period)
    return render_template("tax/index.html", dashboard=dashboard, period=period)


@tax_bp.route("/vat")
@login_required
@require_permission()
def vat():
    period = request.args.get("period", date.today().strftime("%Y-%m"))
    vat_summary = TaxService.get_vat_summary(period)
    return render_template("tax/vat.html", vat=vat_summary, period=period)


@tax_bp.route("/cit")
@login_required
@require_permission()
def cit():
    year = request.args.get("year", date.today().year, type=int)
    cit_estimate = TaxService.get_cit_estimate(year)
    return render_template("tax/cit.html", cit=cit_estimate, year=year)


@tax_bp.route("/pit")
@login_required
@require_permission()
def pit():
    from app.services.payroll_service import PayrollService
    period = request.args.get("period", date.today().strftime("%Y-%m"))
    from app.models.employee import Payslip
    payslips = PayrollService.get_payslips(period=period, status="approved")
    total_pit = sum(float(p.pit) for p in payslips)
    return render_template(
        "tax/pit.html",
        payslips=payslips,
        period=period,
        total_pit=total_pit,
    )
