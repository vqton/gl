import os

from flask import Flask

from config import config
from app.extensions import db, migrate, login_manager, bcrypt


def create_app(config_name=None, test_db_uri=None):
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "default")

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Override DB URI for testing
    if test_db_uri:
        app.config["SQLALCHEMY_DATABASE_URI"] = test_db_uri

    init_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)
    register_shell_context(app)

    return app


def init_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return db.session.get(User, int(user_id))


def register_blueprints(app):
    from app.views.auth import auth_bp
    from app.views.gl import gl_bp
    from app.views.ar import ar_bp
    from app.views.ap import ap_bp
    from app.views.tax import tax_bp
    from app.views.payroll import payroll_bp
    from app.views.fa import fa_bp
    from app.views.inventory import inventory_bp
    from app.views.reports import reports_bp
    from app.views.admin import admin_bp
    from app.views.main import main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(gl_bp, url_prefix="/gl")
    app.register_blueprint(ar_bp, url_prefix="/ar")
    app.register_blueprint(ap_bp, url_prefix="/ap")
    app.register_blueprint(tax_bp, url_prefix="/tax")
    app.register_blueprint(payroll_bp, url_prefix="/payroll")
    app.register_blueprint(fa_bp, url_prefix="/fa")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")
    app.register_blueprint(reports_bp, url_prefix="/reports")
    app.register_blueprint(admin_bp, url_prefix="/admin")


def register_error_handlers(app):
    from flask import render_template

    @app.errorhandler(400)
    def bad_request(e):
        return render_template("errors/400.html"), 400

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(e):
        db.session.rollback()
        return render_template("errors/500.html"), 500


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        from app.models.user import User
        from app.models.account import Account
        from app.models.journal_entry import JournalEntry, JournalEntryLine

        return dict(
            db=db,
            User=User,
            Account=Account,
            JournalEntry=JournalEntry,
            JournalEntryLine=JournalEntryLine,
        )
