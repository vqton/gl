import pytest
from sqlalchemy import StaticPool
from app import create_app
from app.extensions import db as _db
from app.models.user import User


@pytest.fixture
def app():
    """Fresh app with in-memory SQLite DB per test using StaticPool."""
    app = create_app("testing", test_db_uri="sqlite:///:memory:")
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "poolclass": StaticPool,
        "connect_args": {"check_same_thread": False},
    }

    with app.app_context():
        _db.create_all()
        yield app
        _db.session.rollback()
        _db.session.close()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def db(app):
    return _db


@pytest.fixture
def admin_user(db):
    user = User(
        username="admin",
        email="admin@example.com",
        full_name="Admin User",
        role="admin",
    )
    user.password = "adminpass"
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def accountant_user(db):
    user = User(
        username="accountant",
        email="accountant@example.com",
        full_name="Test Accountant",
        role="accountant",
    )
    user.password = "accountantpass"
    db.session.add(user)
    db.session.commit()
    return user
