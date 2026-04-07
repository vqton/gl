from app.extensions import db


class CasbinRule(db.Model):
    """SQLAlchemy model for Casbin policy storage."""
    __tablename__ = "casbin_rule"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ptype = db.Column(db.String(255), nullable=False, default="p")
    v0 = db.Column(db.String(255), nullable=True)
    v1 = db.Column(db.String(255), nullable=True)
    v2 = db.Column(db.String(255), nullable=True)
    v3 = db.Column(db.String(255), nullable=True)
    v4 = db.Column(db.String(255), nullable=True)
    v5 = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<CasbinRule {self.ptype}: {self.v0}, {self.v1}, {self.v2}>"

    def to_dict(self):
        return {
            "id": self.id,
            "ptype": self.ptype,
            "subject": self.v0,
            "resource": self.v1,
            "action": self.v2,
        }
