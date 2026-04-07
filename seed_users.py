"""Seed script to create default users for development."""
from app import create_app
from app.extensions import db
from app.models.user import User, Role


def seed_users():
    """Create default users if they don't exist."""
    app = create_app()

    with app.app_context():
        users = [
            {
                "username": "admin",
                "email": "admin@ketoan.vn",
                "password": "Admin@123",
                "full_name": "Quản Trị Viên",
                "role": Role.ADMIN,
            },
            {
                "username": "cfo",
                "email": "cfo@ketoan.vn",
                "password": "Cfo@123",
                "full_name": "Giám Đốc Tài Chính",
                "role": Role.CFO,
            },
            {
                "username": "ketoantruong",
                "email": "kttruong@ketoan.vn",
                "password": "Ktt@123",
                "full_name": "Kế Toán Trưởng",
                "role": Role.CHIEF_ACCOUNTANT,
            },
            {
                "username": "ketoan",
                "email": "ketoan@ketoan.vn",
                "password": "Kt@123",
                "full_name": "Kế Toán Viên",
                "role": Role.ACCOUNTANT,
            },
            {
                "username": "thue",
                "email": "thue@ketoan.vn",
                "password": "Thue@123",
                "full_name": "Kế Toán Thuế",
                "role": Role.TAX_ACCOUNTANT,
            },
            {
                "username": "luong",
                "email": "luong@ketoan.vn",
                "password": "Luong@123",
                "full_name": "Kế Toán Lương",
                "role": Role.PAYROLL_ACCOUNTANT,
            },
            {
                "username": "thufund",
                "email": "thufund@ketoan.vn",
                "password": "Thu@123",
                "full_name": "Thủ Quỹ",
                "role": Role.CASHIER,
            },
            {
                "username": "kiemtoan",
                "email": "kiemtoan@ketoan.vn",
                "password": "Kt@123",
                "full_name": "Kiểm Toán Viên",
                "role": Role.AUDITOR,
            },
        ]

        created = 0
        for u in users:
            existing = User.get_by_username(u["username"])
            if existing:
                print(f"  ⏭  User '{u['username']}' already exists, skipping")
                continue
            user = User(
                username=u["username"],
                email=u["email"],
                full_name=u["full_name"],
                role=u["role"],
            )
            user.password = u["password"]
            db.session.add(user)
            created += 1
            print(f"  ✅ Created user: {u['username']} ({u['full_name']}) — Role: {u['role']}")

        if created > 0:
            db.session.commit()
            print(f"\n✅ {created} user(s) created successfully")
        else:
            print("\n⚠️  No new users created (all already exist)")

        print("\n" + "=" * 60)
        print("DEFAULT CREDENTIALS")
        print("=" * 60)
        print(f"{'Username':<20} {'Password':<15} {'Role':<25}")
        print("-" * 60)
        for u in users:
            print(f"{u['username']:<20} {u['password']:<15} {u['role']:<25}")
        print("=" * 60)


if __name__ == "__main__":
    seed_users()
