from flask import Blueprint, render_template

fa_bp = Blueprint("fa", __name__)


@fa_bp.route("/")
def index():
    return render_template("fa/index.html")


@fa_bp.route("/assets")
def assets():
    return render_template("fa/assets.html")


@fa_bp.route("/depreciation")
def depreciation():
    return render_template("fa/depreciation.html")
