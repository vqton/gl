from app.extensions import db
from app.models.user import User


class UserService:
    @staticmethod
    def get_all():
        return User.query.order_by(User.username).all()

    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_by_username(username):
        return User.get_by_username(username)

    @staticmethod
    def create(username, email, password, full_name, role="accountant"):
        if User.get_by_username(username):
            raise ValueError(f"Username '{username}' already exists")
        if User.get_by_email(email):
            raise ValueError(f"Email '{email}' already exists")
        user = User(
            username=username,
            email=email,
            full_name=full_name,
            role=role,
        )
        user.password = password
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update(user_id, **kwargs):
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        if "password" in kwargs:
            user.password = kwargs.pop("password")
        user.update(**kwargs)
        db.session.commit()
        return user

    @staticmethod
    def delete(user_id):
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        user.delete()
        db.session.commit()

    @staticmethod
    def authenticate(username, password):
        user = User.get_by_username(username)
        if user and user.verify_password(password):
            return user
        return None
