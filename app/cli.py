"""Flask CLI commands for system administration and data management."""
import csv
import os
from datetime import datetime

import click
from flask import current_app
from flask.cli import with_appcontext

from app.extensions import db
from app.models.user import User, Role
from app.models.account import Account


# ============================================================
# CLI GROUP: manage
# ============================================================

@click.group("manage")
def manage_cli():
    """System management commands."""
    pass


# ============================================================
# COA SEEDING
# ============================================================

@manage_cli.command("seed-coa")
@click.option("--force", is_flag=True, help="Delete existing COA and re-seed")
@click.option("--count", is_flag=True, help="Only show account count, do not seed")
@with_appcontext
def seed_coa(force, count):
    """Seed full Chart of Accounts compliant with Circular 99/2025/TT-BTC."""
    from app.services.coa_data import CIRCULAR99_COA

    if count:
        total = len(CIRCULAR99_COA)
        by_level = {}
        by_type = {}
        for acc in CIRCULAR99_COA:
            by_level[acc["level"]] = by_level.get(acc["level"], 0) + 1
            by_type[acc["type"]] = by_type.get(acc["type"], 0) + 1
        click.echo(f"\nCircular 99/2025/TT-BTC — Chart of Accounts Summary")
        click.echo(f"{'='*50}")
        click.echo(f"Total accounts: {total}")
        click.echo(f"By level: {dict(sorted(by_level.items()))}")
        click.echo(f"By type: {dict(sorted(by_type.items()))}")
        return

    existing = Account.query.count()
    if existing > 0 and not force:
        click.echo(f"\n⚠️  Database already has {existing} accounts.")
        click.echo("   Use --force to delete and re-seed, or run without --force to add missing only.")
        return

    if force:
        click.confirm(f"\n⚠️  This will DELETE all {existing} existing accounts. Continue?", abort=True)
        Account.query.delete()
        db.session.commit()
        click.echo("✅ Existing accounts deleted")

    click.echo(f"\n📋 Seeding Circular 99/2025/TT-BTC Chart of Accounts...")
    type_map = {
        "asset": "asset",
        "liability": "liability",
        "equity": "equity",
        "revenue": "revenue",
        "expense": "expense",
    }

    created = 0
    skipped = 0
    for acc in CIRCULAR99_COA:
        existing_acc = Account.query.filter_by(code=acc["code"]).first()
        if existing_acc:
            skipped += 1
            continue
        account = Account(
            code=acc["code"],
            name=acc["name"],
            name_en=acc.get("name_en", ""),
            account_type=type_map[acc["type"]],
            level=acc["level"],
            parent_code=acc.get("parent_code"),
            description=acc.get("description", ""),
            is_system=True,
        )
        db.session.add(account)
        created += 1

    db.session.commit()
    click.echo(f"✅ Created {created} accounts")
    if skipped:
        click.echo(f"⏭️  Skipped {skipped} existing accounts")
    click.echo(f"📊 Total in DB: {Account.query.count()}")


# ============================================================
# USER MANAGEMENT
# ============================================================

@manage_cli.command("create-user")
@click.argument("username")
@click.option("--email", prompt=True, help="User email address")
@click.option("--full-name", prompt=True, help="Full name (Vietnamese)")
@click.option("--role", default="accountant",
              type=click.Choice(["admin", "cfo", "chief_accountant", "accountant",
                                  "tax_accountant", "payroll_accountant", "cashier",
                                  "auditor", "viewer"]),
              help="User role")
@click.option("--password", prompt=True, hide_input=True,
              confirmation_prompt=True, help="User password")
@click.option("--active/--inactive", default=True, help="User active status")
@with_appcontext
def create_user(username, email, full_name, role, password, active):
    """Create a new user (like Django createsuperuser)."""
    # Check existing
    existing = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()
    if existing:
        if existing.username == username:
            click.echo(f"❌ Error: Username '{username}' already exists")
        else:
            click.echo(f"❌ Error: Email '{email}' already exists")
        return

    user = User(
        username=username,
        email=email,
        full_name=full_name,
        role=role,
        is_active=active,
    )
    user.password = password
    db.session.add(user)
    db.session.commit()

    click.echo(f"\n✅ User created successfully!")
    click.echo(f"{'='*40}")
    click.echo(f"  Username:    {username}")
    click.echo(f"  Email:       {email}")
    click.echo(f"  Full Name:   {full_name}")
    click.echo(f"  Role:        {role}")
    click.echo(f"  Active:      {active}")
    click.echo(f"{'='*40}")


@manage_cli.command("list-users")
@with_appcontext
def list_users():
    """List all users."""
    users = User.query.order_by(User.username).all()
    if not users:
        click.echo("No users found.")
        return

    click.echo(f"\n{'ID':<5} {'Username':<15} {'Email':<25} {'Full Name':<20} {'Role':<20} {'Active':<8}")
    click.echo("-" * 95)
    for u in users:
        click.echo(f"{u.id:<5} {u.username:<15} {u.email:<25} {u.full_name:<20} {u.role:<20} {'✅' if u.is_active else '❌':<8}")
    click.echo(f"\nTotal: {len(users)} users")


@manage_cli.command("set-role")
@click.argument("username")
@click.argument("new_role",
                type=click.Choice(["admin", "cfo", "chief_accountant", "accountant",
                                    "tax_accountant", "payroll_accountant", "cashier",
                                    "auditor", "viewer"]))
@with_appcontext
def set_role(username, new_role):
    """Change a user's role."""
    user = User.query.filter_by(username=username).first()
    if not user:
        click.echo(f"❌ User '{username}' not found")
        return

    old_role = user.role
    user.role = new_role
    db.session.commit()

    click.echo(f"✅ Role changed: {username} — {old_role} → {new_role}")


@manage_cli.command("deactivate-user")
@click.argument("username")
@with_appcontext
def deactivate_user(username):
    """Deactivate a user."""
    user = User.query.filter_by(username=username).first()
    if not user:
        click.echo(f"❌ User '{username}' not found")
        return

    user.is_active = False
    db.session.commit()
    click.echo(f"✅ User '{username}' deactivated")


@manage_cli.command("activate-user")
@click.argument("username")
@with_appcontext
def activate_user(username):
    """Activate a user."""
    user = User.query.filter_by(username=username).first()
    if not user:
        click.echo(f"❌ User '{username}' not found")
        return

    user.is_active = True
    db.session.commit()
    click.echo(f"✅ User '{username}' activated")


@manage_cli.command("reset-password")
@click.argument("username")
@click.option("--password", prompt=True, hide_input=True,
              confirmation_prompt=True, help="New password")
@with_appcontext
def reset_password(username, password):
    """Reset a user's password."""
    user = User.query.filter_by(username=username).first()
    if not user:
        click.echo(f"❌ User '{username}' not found")
        return

    user.password = password
    db.session.commit()
    click.echo(f"✅ Password reset for '{username}'")


# ============================================================
# ROLES
# ============================================================

@manage_cli.command("list-roles")
@with_appcontext
def list_roles():
    """List all roles and their users."""
    roles = Role.query.order_by(Role.name).all()
    if not roles:
        click.echo("No roles found. Run 'flask manage seed-roles' first.")
        return

    for role in roles:
        user_count = len(role.users)
        click.echo(f"  {role.name:<25} {role.display_name:<25} ({user_count} users)")


@manage_cli.command("seed-roles")
@with_appcontext
def seed_roles():
    """Seed default roles into the database."""
    from app.services.admin_service import AdminRoleService
    AdminRoleService.seed_default_roles()
    roles = Role.query.order_by(Role.name).all()
    click.echo(f"✅ {len(roles)} roles seeded")


# ============================================================
# DATABASE
# ============================================================

@manage_cli.command("db-info")
@with_appcontext
def db_info():
    """Show database information."""
    from sqlalchemy import inspect, text
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()

    click.echo(f"\n📊 Database Information")
    click.echo(f"{'='*50}")
    click.echo(f"Engine: {db.engine.url}")
    click.echo(f"Tables: {len(tables)}")
    click.echo()

    for table in sorted(tables):
        count = db.session.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
        click.echo(f"  {table:<30} {count:>8} rows")


@manage_cli.command("db-reset")
@click.confirmation_option(prompt="⚠️  This will DROP ALL tables. Continue?")
@with_appcontext
def db_reset():
    """Drop all tables (development only)."""
    db.drop_all()
    click.echo("✅ All tables dropped")
    click.echo("   Run 'flask db upgrade' or 'flask manage seed-coa --force' to rebuild")


# ============================================================
# ACCOUNTING PERIOD
# ============================================================

@manage_cli.command("open-period")
@click.argument("period")  # YYYY-MM
@with_appcontext
def open_period(period):
    """Open an accounting period."""
    from app.models.period import AccountingPeriod
    try:
        datetime.strptime(period, "%Y-%m")
    except ValueError:
        click.echo("❌ Invalid period format. Use YYYY-MM (e.g., 2026-04)")
        return

    existing = AccountingPeriod.query.filter_by(period=period).first()
    if existing:
        existing.status = "open"
        db.session.commit()
        click.echo(f"✅ Period {period} reopened")
    else:
        p = AccountingPeriod(period=period, status="open")
        db.session.add(p)
        db.session.commit()
        click.echo(f"✅ Period {period} created and opened")


@manage_cli.command("close-period")
@click.argument("period")
@with_appcontext
def close_period(period):
    """Close an accounting period."""
    from app.models.period import AccountingPeriod
    p = AccountingPeriod.query.filter_by(period=period).first()
    if not p:
        click.echo(f"❌ Period {period} not found")
        return

    p.status = "closed"
    p.closed_at = datetime.utcnow()
    db.session.commit()
    click.echo(f"✅ Period {period} closed")


@manage_cli.command("list-periods")
@with_appcontext
def list_periods():
    """List all accounting periods."""
    from app.models.period import AccountingPeriod
    periods = AccountingPeriod.query.order_by(AccountingPeriod.period).all()
    if not periods:
        click.echo("No periods found.")
        return

    click.echo(f"\n{'Period':<12} {'Status':<12} {'Closed At':<25}")
    click.echo("-" * 50)
    for p in periods:
        closed = p.closed_at.strftime("%Y-%m-%d %H:%M") if p.closed_at else "—"
        click.echo(f"  {p.period:<12} {p.status:<12} {closed:<25}")


# ============================================================
# CASBIN POLICY
# ============================================================

@manage_cli.command("policy-check")
@click.argument("role")
@click.argument("resource")
@click.argument("action")
@with_appcontext
def policy_check(role, resource, action):
    """Check if a role has permission for a resource/action."""
    from app.services.casbin_service import CasbinService
    result = CasbinService.check_permission(role, resource, action)
    status = "✅ ALLOWED" if result else "❌ DENIED"
    click.echo(f"\n  Role:     {role}")
    click.echo(f"  Resource: {resource}")
    click.echo(f"  Action:   {action}")
    click.echo(f"  Result:   {status}")


@manage_cli.command("policy-list")
@click.option("--role", default=None, help="Filter by role")
@with_appcontext
def policy_list(role):
    """List all Casbin policies."""
    from app.services.casbin_service import CasbinService
    policies = CasbinService.get_all_permissions()
    if role:
        policies = [p for p in policies if p["role"] == role]

    click.echo(f"\n{'Role':<25} {'Resource':<30} {'Action':<30}")
    click.echo("-" * 85)
    for p in policies:
        click.echo(f"  {p['role']:<25} {p['resource']:<30} {p['action']:<30}")
    click.echo(f"\nTotal: {len(policies)} policies")


# ============================================================
# REGISTER CLI
# ============================================================

def init_cli(app):
    """Register CLI commands with Flask app."""
    app.cli.add_command(manage_cli)
