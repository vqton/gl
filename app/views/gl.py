from datetime import date

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.services.account_service import AccountService
from app.services.journal_entry_service import JournalEntryService
from app.middleware.authorization import require_permission

gl_bp = Blueprint("gl", __name__)


@gl_bp.route("/")
@login_required
@require_permission()
def index():
    return render_template("gl/index.html")


@gl_bp.route("/accounts")
@login_required
@require_permission()
def accounts():
    accounts = AccountService.get_all()
    return render_template("gl/accounts.html", accounts=accounts)


@gl_bp.route("/accounts/new", methods=["GET", "POST"])
@login_required
@require_permission()
def new_account():
    if request.method == "POST":
        try:
            AccountService.create(
                code=request.form["code"],
                name=request.form["name"],
                account_type=request.form["account_type"],
                level=int(request.form.get("level", 1)),
                parent_code=request.form.get("parent_code") or None,
                description=request.form.get("description", ""),
                is_system=False,
            )
            flash("Account created successfully", "success")
            return redirect(url_for("gl.accounts"))
        except ValueError as e:
            flash(str(e), "danger")
    return render_template("gl/account_form.html")


@gl_bp.route("/journal-entries")
@login_required
@require_permission()
def journal_entries():
    page = request.args.get("page", 1, type=int)
    period = request.args.get("period")
    status = request.args.get("status")
    pagination = JournalEntryService.get_all(page=page, period=period, status=status)
    return render_template("gl/journal_entries.html", pagination=pagination)


@gl_bp.route("/journal-entries/new", methods=["GET", "POST"])
@login_required
@require_permission()
def new_journal_entry():
    if request.method == "POST":
        try:
            lines = []
            i = 1
            while f"account_code_{i}" in request.form:
                lines.append({
                    "account_code": request.form[f"account_code_{i}"],
                    "debit_amount": request.form.get(f"debit_amount_{i}", 0),
                    "credit_amount": request.form.get(f"credit_amount_{i}", 0),
                    "description": request.form.get(f"line_desc_{i}", ""),
                })
                i += 1
            entry = JournalEntryService.create(
                entry_date=date.today(),
                description=request.form["description"],
                lines=lines,
                created_by=current_user.id,
            )
            flash(f"Journal entry {entry.entry_number} created", "success")
            return redirect(url_for("gl.journal_entries"))
        except ValueError as e:
            flash(str(e), "danger")
    accounts = AccountService.get_all()
    return render_template("gl/journal_entry_form.html", accounts=accounts)


@gl_bp.route("/journal-entries/<int:entry_id>")
@login_required
@require_permission()
def view_journal_entry(entry_id):
    entry = JournalEntryService.get_by_id(entry_id)
    if not entry:
        flash("Journal entry not found", "danger")
        return redirect(url_for("gl.journal_entries"))
    return render_template("gl/journal_entry_view.html", entry=entry)


@gl_bp.route("/journal-entries/<int:entry_id>/approve", methods=["POST"])
@login_required
@require_permission()
def approve_journal_entry(entry_id):
    try:
        JournalEntryService.approve(entry_id, current_user.id)
        flash("Journal entry approved", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("gl.view_journal_entry", entry_id=entry_id))


@gl_bp.route("/trial-balance")
@login_required
@require_permission()
def trial_balance():
    period = request.args.get("period", date.today().strftime("%Y-%m"))
    data = JournalEntryService.get_trial_balance(period)
    return render_template("gl/trial_balance.html", data=data, period=period)
