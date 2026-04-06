from app.extensions import db
from app.models.base import BaseModel


class Supplier(BaseModel):
    __tablename__ = "suppliers"

    code = db.Column(db.String(20), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    tax_code = db.Column(db.String(20), nullable=True, index=True)
    address = db.Column(db.Text, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(128), nullable=True)
    payment_terms = db.Column(db.Integer, default=30)

    @classmethod
    def get_by_code(cls, code):
        return cls.query.filter_by(code=code).first()

    def __repr__(self):
        return f"<Supplier {self.code} - {self.name}>"
