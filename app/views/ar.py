from flask import Blueprint, render_template

ar_bp = Blueprint("ar", __name__)


@ar_bp.route("/")
def index():
    return render_template("ar/index.html")


@ar_bp.route("/invoices")
def invoices():
    return render_template("ar/invoices.html")


@ar_bp.route("/customers")
def customers():
    return render_template("ar/customers.html")
