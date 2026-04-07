from datetime import date

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from app.middleware.authorization import require_permission
from app.services.fixed_asset_service import FixedAssetService

fa_bp = Blueprint("fa", __name__)


@fa_bp.route("/")
@login_required
@require_permission()
def index():
    summary = FixedAssetService.get_summary()
    return render_template("fa/index.html", summary=summary)


@fa_bp.route("/assets")
@login_required
@require_permission()
def assets():
    status = request.args.get("status")
    assets = FixedAssetService.get_all(status=status)
    return render_template("fa/assets.html", assets=assets, current_status=status)


@fa_bp.route("/assets/new", methods=["GET", "POST"])
@login_required
@require_permission()
def new_asset():
    if request.method == "POST":
        try:
            acq_str = request.form.get("acquisition_date")
            acq_date = date.fromisoformat(acq_str) if acq_str else date.today()
            dep_str = request.form.get("depreciation_start_date")
            dep_date = date.fromisoformat(dep_str) if dep_str else None
            FixedAssetService.create(
                asset_code=request.form["asset_code"],
                asset_name=request.form["asset_name"],
                category=request.form["category"],
                original_cost=float(request.form["original_cost"]),
                useful_life_years=int(request.form["useful_life_years"]),
                acquisition_date=acq_date,
                depreciation_method=request.form.get("depreciation_method", "straight_line"),
                residual_value=float(request.form.get("residual_value", 0)),
                depreciation_start_date=dep_date,
                location=request.form.get("location", ""),
                responsible_person=request.form.get("responsible_person", ""),
            )
            flash("Đã tạo tài sản cố định.", "success")
            return redirect(url_for("fa.assets"))
        except ValueError as e:
            flash(str(e), "danger")
    return render_template("fa/asset_form.html")


@fa_bp.route("/depreciation")
@login_required
@require_permission()
def depreciation():
    period = request.args.get("period", date.today().strftime("%Y-%m"))
    dep_data = FixedAssetService.run_monthly_depreciation(period)
    return render_template("fa/depreciation.html", depreciation=dep_data, period=period)
