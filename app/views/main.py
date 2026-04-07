from datetime import date

from flask import Blueprint, render_template
from flask_login import login_required

from app.middleware.authorization import require_permission
from app.services.report_service import ReportService

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("main/index.html")


@main_bp.route("/dashboard")
@login_required
@require_permission()
def dashboard():
    period = date.today().strftime("%Y-%m")
    try:
        dashboard_data = ReportService.get_dashboard_summary(period)
    except Exception:
        dashboard_data = {
            "period": period,
            "total_assets": 0,
            "total_liabilities": 0,
            "total_equity": 0,
            "net_profit": 0,
            "pending_invoices": 0,
            "pending_bills": 0,
            "pending_approvals": 0,
            "pending_bill_approvals": 0,
            "pending_payslips": 0,
        }
    return render_template("main/dashboard.html", dashboard=dashboard_data, period=period)
