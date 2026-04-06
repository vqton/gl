from flask import Blueprint

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    from flask import render_template
    return render_template("main/index.html")


@main_bp.route("/dashboard")
def dashboard():
    from flask import render_template
    return render_template("main/dashboard.html")
