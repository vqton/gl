from flask import Blueprint, render_template

tax_bp = Blueprint("tax", __name__)


@tax_bp.route("/")
def index():
    return render_template("tax/index.html")


@tax_bp.route("/vat")
def vat():
    return render_template("tax/vat.html")


@tax_bp.route("/cit")
def cit():
    return render_template("tax/cit.html")


@tax_bp.route("/pit")
def pit():
    return render_template("tax/pit.html")
