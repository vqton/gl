from flask_login import UserMixin

from app.extensions import bcrypt, db
from app.models.base import BaseModel


class User(UserMixin, BaseModel):
    __tablename__ = "users"

    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(128), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(32), nullable=False, default="accountant")

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def has_role(self, role):
        if self.role == "admin":
            return True
        return self.role == role

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def __repr__(self):
        return f"<User {self.username}>"


class Role:
    ADMIN = "admin"
    CFO = "cfo"
    CHIEF_ACCOUNTANT = "chief_accountant"
    ACCOUNTANT = "accountant"
    TAX_ACCOUNTANT = "tax_accountant"
    PAYROLL_ACCOUNTANT = "payroll_accountant"
    CASHIER = "cashier"
    AUDITOR = "auditor"
    VIEWER = "viewer"

    ROLES = [
        ADMIN,
        CFO,
        CHIEF_ACCOUNTANT,
        ACCOUNTANT,
        TAX_ACCOUNTANT,
        PAYROLL_ACCOUNTANT,
        CASHIER,
        AUDITOR,
        VIEWER,
    ]
