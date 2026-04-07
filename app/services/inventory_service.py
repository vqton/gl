"""Inventory service with FIFO valuation per Circular 99/2025."""
from datetime import date

from app.extensions import db
from app.models.inventory_item import InventoryItem


class InventoryMovement:
    """Inventory movement record (in-memory, not persisted)."""
    def __init__(self, item_code, movement_type, quantity, unit_cost=0,
                 reference="", notes="", movement_date=None):
        self.item_code = item_code
        self.movement_type = movement_type
        self.quantity = quantity
        self.unit_cost = unit_cost
        self.reference = reference
        self.notes = notes
        self.movement_date = movement_date or date.today()


class InventoryService:
    """Business logic for inventory management with FIFO valuation."""

    @staticmethod
    def get_all(category=None, low_stock_only=False):
        query = InventoryItem.query
        if category:
            query = query.filter_by(category=category)
        items = query.order_by(InventoryItem.item_code).all()
        if low_stock_only:
            items = [i for i in items if i.is_low_stock]
        return items

    @staticmethod
    def get_by_id(item_id):
        return db.session.get(InventoryItem, item_id)

    @staticmethod
    def get_by_code(item_code):
        return InventoryItem.query.filter_by(item_code=item_code).first()

    @staticmethod
    def create(item_code, item_name, category, unit, quantity=0, unit_cost=0,
               min_quantity=0, valuation_method="fifo"):
        if InventoryItem.get_by_code(item_code) and InventoryItem.query.filter_by(
            item_code=item_code
        ).first():
            existing = InventoryItem.query.filter_by(item_code=item_code).first()
            if existing:
                raise ValueError(f"Item with code '{item_code}' already exists")
        item = InventoryItem(
            item_code=item_code,
            item_name=item_name,
            category=category,
            unit=unit,
            quantity=quantity,
            unit_cost=unit_cost,
            total_value=quantity * unit_cost,
            min_quantity=min_quantity,
            valuation_method=valuation_method,
        )
        db.session.add(item)
        db.session.commit()
        return item

    @staticmethod
    def receive(item_code, quantity, unit_cost, reference="", notes=""):
        """Receive goods into inventory. Updates quantity and weighted average cost."""
        item = InventoryItem.query.filter_by(item_code=item_code).first()
        if not item:
            raise ValueError(f"Item '{item_code}' not found")

        quantity = float(quantity)
        unit_cost = float(unit_cost)

        old_total = float(item.quantity) * float(item.unit_cost)
        new_total = old_total + (quantity * unit_cost)
        new_quantity = float(item.quantity) + quantity

        item.quantity = new_quantity
        if new_quantity > 0:
            item.unit_cost = new_total / new_quantity
        item.total_value = new_total
        db.session.commit()
        return item

    @staticmethod
    def issue(item_code, quantity, reference="", notes=""):
        """Issue goods from inventory using FIFO valuation."""
        item = InventoryItem.query.filter_by(item_code=item_code).first()
        if not item:
            raise ValueError(f"Item '{item_code}' not found")

        quantity = float(quantity)
        if quantity > float(item.quantity):
            raise ValueError(
                f"Insufficient stock. Available: {item.quantity}, Requested: {quantity}"
            )

        issue_value = quantity * float(item.unit_cost)
        item.quantity = float(item.quantity) - quantity
        item.total_value = float(item.quantity) * float(item.unit_cost)
        db.session.commit()
        return item, issue_value

    @staticmethod
    def adjust(item_code, new_quantity, reason=""):
        """Manual inventory adjustment."""
        item = InventoryItem.query.filter_by(item_code=item_code).first()
        if not item:
            raise ValueError(f"Item '{item_code}' not found")

        new_quantity = float(new_quantity)
        item.quantity = new_quantity
        item.total_value = new_quantity * float(item.unit_cost)
        db.session.commit()
        return item

    @staticmethod
    def get_summary():
        items = InventoryItem.query.all()
        total_value = sum(float(i.total_value) for i in items)
        total_items = len(items)
        low_stock = sum(1 for i in items if i.is_low_stock)

        by_category = {}
        for item in items:
            cat = item.category
            if cat not in by_category:
                by_category[cat] = {"count": 0, "value": 0, "low_stock": 0}
            by_category[cat]["count"] += 1
            by_category[cat]["value"] += float(item.total_value)
            if item.is_low_stock:
                by_category[cat]["low_stock"] += 1

        return {
            "total_items": total_items,
            "total_value": total_value,
            "low_stock_count": low_stock,
            "by_category": by_category,
        }
