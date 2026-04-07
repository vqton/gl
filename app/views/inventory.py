from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from app.middleware.authorization import require_permission
from app.services.inventory_service import InventoryService

inventory_bp = Blueprint("inventory", __name__)


@inventory_bp.route("/")
@login_required
@require_permission()
def index():
    summary = InventoryService.get_summary()
    return render_template("inventory/index.html", summary=summary)


@inventory_bp.route("/items")
@login_required
@require_permission()
def items():
    category = request.args.get("category")
    low_stock = request.args.get("low_stock") == "1"
    items = InventoryService.get_all(category=category, low_stock_only=low_stock)
    return render_template(
        "inventory/items.html",
        items=items,
        current_category=category,
        low_stock_only=low_stock,
    )


@inventory_bp.route("/items/new", methods=["GET", "POST"])
@login_required
@require_permission()
def new_item():
    if request.method == "POST":
        try:
            InventoryService.create(
                item_code=request.form["item_code"],
                item_name=request.form["item_name"],
                category=request.form["category"],
                unit=request.form["unit"],
                quantity=float(request.form.get("quantity", 0)),
                unit_cost=float(request.form.get("unit_cost", 0)),
                min_quantity=float(request.form.get("min_quantity", 0)),
                valuation_method=request.form.get("valuation_method", "fifo"),
            )
            flash("Đã tạo vật tư.", "success")
            return redirect(url_for("inventory.items"))
        except ValueError as e:
            flash(str(e), "danger")
    return render_template("inventory/item_form.html")


@inventory_bp.route("/items/<item_code>/receive", methods=["GET", "POST"])
@login_required
@require_permission()
def receive_item(item_code):
    if request.method == "POST":
        try:
            InventoryService.receive(
                item_code=item_code,
                quantity=float(request.form["quantity"]),
                unit_cost=float(request.form["unit_cost"]),
                reference=request.form.get("reference", ""),
            )
            flash("Đã nhập kho.", "success")
            return redirect(url_for("inventory.items"))
        except ValueError as e:
            flash(str(e), "danger")
    item = InventoryService.get_by_code(item_code)
    if not item:
        flash("Vật tư không tồn tại.", "danger")
        return redirect(url_for("inventory.items"))
    return render_template("inventory/receive_form.html", item=item)


@inventory_bp.route("/items/<item_code>/issue", methods=["GET", "POST"])
@login_required
@require_permission()
def issue_item(item_code):
    if request.method == "POST":
        try:
            InventoryService.issue(
                item_code=item_code,
                quantity=float(request.form["quantity"]),
                reference=request.form.get("reference", ""),
            )
            flash("Đã xuất kho.", "success")
            return redirect(url_for("inventory.items"))
        except ValueError as e:
            flash(str(e), "danger")
    item = InventoryService.get_by_code(item_code)
    if not item:
        flash("Vật tư không tồn tại.", "danger")
        return redirect(url_for("inventory.items"))
    return render_template("inventory/issue_form.html", item=item)


@inventory_bp.route("/movements")
@login_required
@require_permission()
def movements():
    return render_template("inventory/movements.html")
