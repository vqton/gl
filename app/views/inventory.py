from flask import Blueprint, render_template

inventory_bp = Blueprint("inventory", __name__)


@inventory_bp.route("/")
def index():
    return render_template("inventory/index.html")


@inventory_bp.route("/items")
def items():
    return render_template("inventory/items.html")


@inventory_bp.route("/movements")
def movements():
    return render_template("inventory/movements.html")
