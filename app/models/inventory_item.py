from app.extensions import db
from app.models.base import BaseModel


class InventoryItem(BaseModel):
    __tablename__ = "inventory_items"

    item_code = db.Column(db.String(20), unique=True, nullable=False, index=True)
    item_name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Numeric(18, 4), default=0, nullable=False)
    unit_cost = db.Column(db.Numeric(18, 2), default=0, nullable=False)
    total_value = db.Column(db.Numeric(18, 2), default=0, nullable=False)
    min_quantity = db.Column(db.Numeric(18, 4), default=0)
    valuation_method = db.Column(db.String(20), default="fifo")

    @property
    def is_low_stock(self):
        return self.quantity < self.min_quantity

    def __repr__(self):
        return f"<InventoryItem {self.item_code} - {self.item_name}>"
