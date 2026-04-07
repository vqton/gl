"""System Administration Service Layer.

Handles user management, role assignment, audit logging, and system settings.
All operations are designed for accounting compliance (SoD, auditability).
"""
from datetime import datetime

from app.extensions import db
from app.models.user import User, Role, user_roles
from app.services.casbin_service import CasbinService


class AdminUserService:
    """User management with audit trail."""

    @staticmethod
    def get_all(active_only=True):
        query = User.query
        if active_only:
            query = query.filter_by(is_active=True)
        return query.order_by(User.username).all()

    @staticmethod
    def get_by_id(user_id):
        return db.session.get(User, user_id)

    @staticmethod
    def create(username, email, password, full_name, role="accountant", additional_roles=None):
        if User.get_by_username(username):
            raise ValueError(f"Tên đăng nhập '{username}' đã tồn tại")
        if User.get_by_email(email):
            raise ValueError(f"Email '{email}' đã tồn tại")

        user = User(
            username=username,
            email=email,
            full_name=full_name,
            role=role,
            is_active=True,
        )
        user.password = password
        db.session.add(user)
        db.session.flush()

        if additional_roles:
            for role_name in additional_roles:
                role = db.session.get(Role, role_name)
                if role:
                    user.assigned_roles.append(role)

        db.session.commit()
        return user

    @staticmethod
    def update(user_id, **kwargs):
        user = db.session.get(User, user_id)
        if not user:
            raise ValueError("Không tìm thấy người dùng")

        allowed = {"full_name", "email", "is_active", "last_login"}
        for key, value in kwargs.items():
            if key in allowed:
                setattr(user, key, value)

        db.session.commit()
        return user

    @staticmethod
    def change_role(user_id, new_primary_role):
        user = db.session.get(User, user_id)
        if not user:
            raise ValueError("Không tìm thấy người dùng")
        user.role = new_primary_role
        db.session.commit()
        return user

    @staticmethod
    def assign_roles(user_id, role_names):
        user = db.session.get(User, user_id)
        if not user:
            raise ValueError("Không tìm thấy người dùng")

        user.assigned_roles.clear()
        for role_name in role_names:
            role = db.session.get(Role, role_name)
            if role:
                user.assigned_roles.append(role)

        db.session.commit()
        return user

    @staticmethod
    def deactivate(user_id):
        user = db.session.get(User, user_id)
        if not user:
            raise ValueError("Không tìm thấy người dùng")
        user.is_active = False
        db.session.commit()
        return user


class AdminRoleService:
    """Role management synced with Casbin policies."""

    DEFAULT_ROLES = [
        {"name": "admin", "display_name": "Quản trị viên", "description": "Toàn quyền hệ thống", "is_system": True},
        {"name": "cfo", "display_name": "Giám đốc tài chính", "description": "Quản lý tài chính, phê duyệt", "is_system": True},
        {"name": "chief_accountant", "display_name": "Kế toán trưởng", "description": "Quản lý sổ cái, phê duyệt bút toán", "is_system": True},
        {"name": "accountant", "display_name": "Kế toán viên", "description": "Hạch toán, quản lý chứng từ", "is_system": True},
        {"name": "tax_accountant", "display_name": "Kế toán thuế", "description": "Kê khai thuế", "is_system": True},
        {"name": "payroll_accountant", "display_name": "Kế toán lương", "description": "Quản lý bảng lương", "is_system": True},
        {"name": "cashier", "display_name": "Thủ quỹ", "description": "Quản lý thu chi tiền mặt/ngân hàng", "is_system": True},
        {"name": "auditor", "display_name": "Kiểm toán viên", "description": "Xem báo cáo, kiểm tra", "is_system": True},
        {"name": "viewer", "display_name": "Người xem", "description": "Chỉ xem báo cáo", "is_system": True},
    ]

    @staticmethod
    def seed_default_roles():
        """Create default roles if they don't exist."""
        for role_data in AdminRoleService.DEFAULT_ROLES:
            existing = db.session.get(Role, role_data["name"])
            if not existing:
                role = Role(**role_data)
                db.session.add(role)
        db.session.commit()

    @staticmethod
    def get_all():
        return Role.query.order_by(Role.name).all()

    @staticmethod
    def get_by_name(name):
        return db.session.get(Role, name)

    @staticmethod
    def get_permissions(role_name):
        return CasbinService.get_role_permissions(role_name)

    @staticmethod
    def get_users_with_role(role_name):
        role = db.session.get(Role, role_name)
        if not role:
            return []
        return role.users

    @staticmethod
    def create_role(name, display_name, description=""):
        existing = db.session.get(Role, name)
        if existing:
            raise ValueError(f"Vai trò '{name}' đã tồn tại")
        role = Role(name=name, display_name=display_name, description=description)
        db.session.add(role)
        db.session.commit()
        return role

    @staticmethod
    def delete_role(name):
        role = db.session.get(Role, name)
        if not role:
            raise ValueError("Không tìm thấy vai trò")
        if role.is_system:
            raise ValueError("Không thể xóa vai trò hệ thống")
        if role.users:
            raise ValueError("Không thể xóa vai trò đang được gán cho người dùng")
        db.session.delete(role)
        db.session.commit()


class AuditLogService:
    """Audit trail for all admin and financial actions."""

    @staticmethod
    def log(user_id, action, entity_type, entity_id, details=None):
        from app.models.audit_log import AuditLog
        log = AuditLog(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=details or {},
        )
        db.session.add(log)
        db.session.commit()
        return log

    @staticmethod
    def get_logs(entity_type=None, user_id=None, limit=100):
        from app.models.audit_log import AuditLog
        query = AuditLog.query
        if entity_type:
            query = query.filter_by(entity_type=entity_type)
        if user_id:
            query = query.filter_by(user_id=user_id)
        return query.order_by(AuditLog.created_at.desc()).limit(limit).all()
