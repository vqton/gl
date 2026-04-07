from datetime import date

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.middleware.authorization import require_permission
from app.services.bill_service import BillService, SupplierService

ap_bp = Blueprint("ap", __name__)


@ap_bp.route("/")
@login_required
@require_permission()
def index():
    aging = BillService.get_aging()
    total_outstanding = sum(aging.values())
    return render_template("ap/index.html", aging=aging, total_outstanding=total_outstanding)


@ap_bp.route("/bills")
@login_required
@require_permission()
def bills():
    page = request.args.get("page", 1, type=int)
    status = request.args.get("status")
    supplier_id = request.args.get("supplier_id", type=int)
    pagination = BillService.get_all(page=page, status=status, supplier_id=supplier_id)
    suppliers = SupplierService.get_all()
    return render_template(
        "ap/bills.html",
        pagination=pagination,
        suppliers=suppliers,
        current_status=status,
        current_supplier=supplier_id,
    )


@ap_bp.route("/bills/new", methods=["GET", "POST"])
@login_required
@require_permission()
def new_bill():
    if request.method == "POST":
        try:
            lines = []
            i = 1
            while f"line_desc_{i}" in request.form:
                lines.append({
                    "description": request.form[f"line_desc_{i}"],
                    "quantity": request.form.get(f"line_qty_{i}", 1),
                    "unit_price": request.form.get(f"line_price_{i}", 0),
                    "account_code": request.form.get(f"line_account_{i}"),
                })
                i += 1
            due_str = request.form.get("due_date")
            due_date = date.fromisoformat(due_str) if due_str else None
            bill = BillService.create(
                invoice_date=date.today(),
                supplier_id=int(request.form["supplier_id"]),
                description=request.form.get("description", ""),
                lines=lines,
                vat_rate=float(request.form.get("vat_rate", 10)),
                due_date=due_date,
                document_number=request.form.get("document_number"),
                supplier_invoice_number=request.form.get("supplier_invoice_number"),
            )
            flash(f"Phiếu mua {bill.bill_number} đã được tạo.", "success")
            return redirect(url_for("ap.bills"))
        except ValueError as e:
            flash(str(e), "danger")
    suppliers = SupplierService.get_all()
    return render_template("ap/bill_form.html", suppliers=suppliers)


@ap_bp.route("/bills/<int:bill_id>/submit", methods=["POST"])
@login_required
@require_permission()
def submit_bill(bill_id):
    try:
        BillService.submit(bill_id)
        flash("Đã gửi phiếu mua.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("ap.bills"))


@ap_bp.route("/bills/<int:bill_id>/approve", methods=["POST"])
@login_required
@require_permission()
def approve_bill(bill_id):
    try:
        BillService.approve(bill_id, current_user.id)
        flash("Đã duyệt phiếu mua.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    except PermissionError:
        flash("Bạn không có quyền phê duyệt phiếu mua này.", "danger")
    return redirect(url_for("ap.bills"))


@ap_bp.route("/bills/<int:bill_id>/pay", methods=["POST"])
@login_required
@require_permission()
def pay_bill(bill_id):
    try:
        amount = float(request.form.get("amount", 0))
        BillService.record_payment(
            bill_id,
            amount,
            payment_method=request.form.get("payment_method", "bank_transfer"),
            reference=request.form.get("reference", ""),
        )
        flash("Đã ghi nhận thanh toán.", "success")
    except (ValueError, TypeError) as e:
        flash(str(e), "danger")
    return redirect(url_for("ap.bills"))


@ap_bp.route("/suppliers")
@login_required
@require_permission()
def suppliers():
    suppliers = SupplierService.get_all()
    return render_template("ap/suppliers.html", suppliers=suppliers)


@ap_bp.route("/suppliers/new", methods=["GET", "POST"])
@login_required
@require_permission()
def new_supplier():
    if request.method == "POST":
        try:
            SupplierService.create(
                code=request.form["code"],
                name=request.form["name"],
                tax_code=request.form.get("tax_code", ""),
                address=request.form.get("address", ""),
                phone=request.form.get("phone", ""),
                email=request.form.get("email", ""),
                payment_terms=int(request.form.get("payment_terms", 30)),
            )
            flash("Đã tạo nhà cung cấp.", "success")
            return redirect(url_for("ap.suppliers"))
        except ValueError as e:
            flash(str(e), "danger")
    return render_template("ap/supplier_form.html")
