from flask import Blueprint, render_template

reports_bp = Blueprint("reports", __name__)


@reports_bp.route("/")
def index():
    return render_template("reports/index.html")


@reports_bp.route("/financial-statements")
def financial_statements():
    return render_template("reports/financial_statements.html")


@reports_bp.route("/b01")
def b01():
    return render_template("reports/b01.html")


@reports_bp.route("/b02")
def b02():
    return render_template("reports/b02.html")


@reports_bp.route("/b03")
def b03():
    return render_template("reports/b03.html")


@reports_bp.route("/b09")
def b09():
    return render_template("reports/b09.html")
