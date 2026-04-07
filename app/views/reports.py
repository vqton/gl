from datetime import date

from flask import Blueprint, render_template, request
from flask_login import login_required

from app.middleware.authorization import require_permission
from app.services.report_service import ReportService

reports_bp = Blueprint("reports", __name__)


@reports_bp.route("/")
@login_required
@require_permission()
def index():
    period = request.args.get("period", date.today().strftime("%Y-%m"))
    return render_template("reports/index.html", period=period)


@reports_bp.route("/financial-statements")
@login_required
@require_permission()
def financial_statements():
    period = request.args.get("period", date.today().strftime("%Y-%m"))
    dashboard = ReportService.get_dashboard_summary(period)
    return render_template("reports/financial_statements.html", dashboard=dashboard, period=period)


@reports_bp.route("/b01")
@login_required
@require_permission()
def b01():
    period = request.args.get("period", date.today().strftime("%Y-%m"))
    report = ReportService.generate_b01(period)
    return render_template("reports/b01.html", report=report, period=period)


@reports_bp.route("/b02")
@login_required
@require_permission()
def b02():
    period = request.args.get("period", date.today().strftime("%Y-%m"))
    report = ReportService.generate_b02(period)
    return render_template("reports/b02.html", report=report, period=period)


@reports_bp.route("/b03")
@login_required
@require_permission()
def b03():
    period = request.args.get("period", date.today().strftime("%Y-%m"))
    report = ReportService.generate_b03(period)
    return render_template("reports/b03.html", report=report, period=period)


@reports_bp.route("/b09")
@login_required
@require_permission()
def b09():
    period = request.args.get("period", date.today().strftime("%Y-%m"))
    report = ReportService.generate_b09(period)
    return render_template("reports/b09.html", report=report, period=period)
