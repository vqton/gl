"""User-Role many-to-many association table for multi-role support."""
from flask_login import UserMixin

from app.extensions import bcrypt, db

user_roles = db.Table(
    "user_roles",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    db.Column("role_name", db.String(32), db.ForeignKey("roles.name", ondelete="CASCADE"), primary_key=True),
)


class Role(db.Model):
    """Role definition stored in DB, synced with Casbin policies."""
    __tablename__ = "roles"

    name = db.Column(db.String(32), primary_key=True)
    display_name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(255), default="")
    is_system = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    users = db.relationship("User", secondary=user_roles, back_populates="assigned_roles")

    def to_dict(self):
        return {
            "name": self.name,
            "display_name": self.display_name,
            "description": self.description,
            "is_system": self.is_system,
            "user_count": len(self.users),
        }


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(128), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(32), nullable=False, default="accountant")
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    last_login = db.Column(db.DateTime)

    assigned_roles = db.relationship("Role", secondary=user_roles, back_populates="users")

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def get_all_roles(self):
        """Return primary role + additional assigned roles."""
        roles = {self.role}
        roles.update(r.name for r in self.assigned_roles)
        return roles

    def has_role(self, role_name):
        """Check if user has a specific role (primary or assigned)."""
        if self.role == "admin":
            return True
        return role_name in self.get_all_roles()

    def is_admin(self):
        return self.role == "admin" or "admin" in {r.name for r in self.assigned_roles}

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)

    def __repr__(self):
        return f"<User {self.username}>"
