from flask import Blueprint, render_template

ap_bp = Blueprint("ap", __name__)


@ap_bp.route("/")
def index():
    return render_template("ap/index.html")


@ap_bp.route("/bills")
def bills():
    return render_template("ap/bills.html")


@ap_bp.route("/suppliers")
def suppliers():
    return render_template("ap/suppliers.html")
