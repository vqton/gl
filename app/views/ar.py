from datetime import date

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.middleware.authorization import require_permission
from app.services.invoice_service import InvoiceService
from app.services.customer_service import CustomerService

ar_bp = Blueprint("ar", __name__)


@ar_bp.route("/")
@login_required
@require_permission()
def index():
    aging = InvoiceService.get_aging()
    total_outstanding = sum(aging.values())
    return render_template("ar/index.html", aging=aging, total_outstanding=total_outstanding)


@ar_bp.route("/invoices")
@login_required
@require_permission()
def invoices():
    page = request.args.get("page", 1, type=int)
    status = request.args.get("status")
    customer_id = request.args.get("customer_id", type=int)
    pagination = InvoiceService.get_all(page=page, status=status, customer_id=customer_id)
    customers = CustomerService.get_all()
    return render_template(
        "ar/invoices.html",
        pagination=pagination,
        customers=customers,
        current_status=status,
        current_customer=customer_id,
    )


@ar_bp.route("/invoices/new", methods=["GET", "POST"])
@login_required
@require_permission()
def new_invoice():
    if request.method == "POST":
        try:
            lines = []
            i = 1
            while f"line_desc_{i}" in request.form:
                lines.append({
                    "description": request.form[f"line_desc_{i}"],
                    "quantity": request.form.get(f"line_qty_{i}", 1),
                    "unit_price": request.form.get(f"line_price_{i}", 0),
                })
                i += 1
            due_str = request.form.get("due_date")
            due_date = date.fromisoformat(due_str) if due_str else None
            invoice = InvoiceService.create(
                invoice_date=date.today(),
                customer_id=int(request.form["customer_id"]),
                description=request.form.get("description", ""),
                lines=lines,
                vat_rate=float(request.form.get("vat_rate", 10.0)),
                due_date=due_date,
            )
            flash(f"Hóa đơn {invoice.invoice_number} đã được tạo.", "success")
            return redirect(url_for("ar.invoices"))
        except ValueError as e:
            flash(str(e), "danger")
    customers = CustomerService.get_all()
    return render_template("ar/invoice_form.html", customers=customers)


@ar_bp.route("/invoices/<int:invoice_id>/submit", methods=["POST"])
@login_required
@require_permission()
def submit_invoice(invoice_id):
    try:
        InvoiceService.submit(invoice_id)
        flash("Đã gửi hóa đơn.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("ar.invoices"))


@ar_bp.route("/invoices/<int:invoice_id>/approve", methods=["POST"])
@login_required
@require_permission()
def approve_invoice(invoice_id):
    try:
        InvoiceService.approve(invoice_id, current_user.id)
        flash("Đã duyệt hóa đơn.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    except PermissionError:
        flash("Bạn không có quyền phê duyệt hóa đơn này.", "danger")
    return redirect(url_for("ar.invoices"))


@ar_bp.route("/invoices/<int:invoice_id>/pay", methods=["POST"])
@login_required
@require_permission()
def pay_invoice(invoice_id):
    try:
        amount = float(request.form.get("amount", 0))
        InvoiceService.record_payment(invoice_id, amount)
        flash("Đã ghi nhận thanh toán.", "success")
    except (ValueError, TypeError) as e:
        flash(str(e), "danger")
    return redirect(url_for("ar.invoices"))


@ar_bp.route("/customers")
@login_required
@require_permission()
def customers():
    customers = CustomerService.get_all()
    return render_template("ar/customers.html", customers=customers)


@ar_bp.route("/customers/new", methods=["GET", "POST"])
@login_required
@require_permission()
def new_customer():
    if request.method == "POST":
        try:
            CustomerService.create(
                code=request.form["code"],
                name=request.form["name"],
                tax_code=request.form.get("tax_code", ""),
                address=request.form.get("address", ""),
                phone=request.form.get("phone", ""),
                email=request.form.get("email", ""),
            )
            flash("Đã tạo khách hàng.", "success")
            return redirect(url_for("ar.customers"))
        except ValueError as e:
            flash(str(e), "danger")
    return render_template("ar/customer_form.html")
