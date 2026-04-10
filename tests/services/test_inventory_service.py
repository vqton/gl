import pytest
from decimal import Decimal
from datetime import date
from app.services.inventory_service import InventoryService
from app.models.inventory_item import InventoryItem


class TestInventoryService:
    def test_get_all_empty(self, db):
        items = InventoryService.get_all()
        assert items == []

    def test_get_all_with_items(self, db):
        item = InventoryItem(
            item_code="VT001",
            item_name="Sản phẩm A",
            category="nguyên vật liệu",
            unit="cái",
            quantity=100,
            unit_cost=Decimal("100000.00"),
            total_value=Decimal("10000000.00"),
            valuation_method="fifo",
        )
        db.session.add(item)
        db.session.commit()

        items = InventoryService.get_all()
        assert len(items) == 1

    def test_get_by_id(self, db):
        item = InventoryItem(
            item_code="VT002",
            item_name="Sản phẩm B",
            category="nguyên vật liệu",
            unit="cái",
            quantity=50,
            unit_cost=Decimal("200000.00"),
            total_value=Decimal("10000000.00"),
            valuation_method="fifo",
        )
        db.session.add(item)
        db.session.commit()

        found = InventoryService.get_by_id(item.id)
        assert found is not None
        assert found.item_code == "VT002"

    def test_get_by_id_not_found(self, db):
        found = InventoryService.get_by_id(99999)
        assert found is None

    def test_get_by_code(self, db):
        item = InventoryItem(
            item_code="VT003",
            item_name="Sản phẩm C",
            category="nguyên vật liệu",
            unit="cái",
            quantity=30,
            unit_cost=Decimal("150000.00"),
            total_value=Decimal("4500000.00"),
            valuation_method="fifo",
        )
        db.session.add(item)
        db.session.commit()

        found = InventoryService.get_by_code("VT003")
        assert found is not None
        assert found.item_code == "VT003"

    def test_get_by_code_not_found(self, db):
        found = InventoryService.get_by_code("NONEXISTENT")
        assert found is None

    def test_create_item(self, db):
        item = InventoryService.create(
            item_code="VT004",
            item_name="Vật tư mới",
            category="nguyên vật liệu",
            unit="kg",
            quantity=0,
            unit_cost=0,
            min_quantity=10,
        )
        db.session.commit()

        assert item.id is not None
        assert item.item_code == "VT004"
        assert item.item_name == "Vật tư mới"

    def test_create_duplicate_code_raises_error(self, db):
        InventoryService.create(
            item_code="VT005",
            item_name="Item 1",
            category="nguyên vật liệu",
            unit="cái",
        )
        db.session.commit()

        with pytest.raises(ValueError, match="đã tồn tại"):
            InventoryService.create(
                item_code="VT005",
                item_name="Item 2",
                category="nguyên vật liệu",
                unit="cái",
            )
        db.session.rollback()

    def test_create_missing_required_fields(self, db):
        with pytest.raises(ValueError, match="Mã vật tư không được để trống"):
            InventoryService.create(
                item_code="",
                item_name="Test Item",
                category="nguyên vật liệu",
                unit="cái",
            )
        db.session.rollback()

        with pytest.raises(ValueError, match="Tên vật tư không được để trống"):
            InventoryService.create(
                item_code="VT006",
                item_name="",
                category="nguyên vật liệu",
                unit="cái",
            )
        db.session.rollback()

    def test_receive_inventory(self, db):
        item = InventoryService.create(
            item_code="VT007",
            item_name="Vật tư nhập",
            category="nguyên vật liệu",
            unit="kg",
            quantity=100,
            unit_cost=Decimal("50000.00"),
        )
        db.session.commit()

        result = InventoryService.receive("VT007", 50, 60000)
        assert result.quantity == 150
        # Weighted average: (100*50000 + 50*60000) / 150 = 8000000/150 = 53333.33
        assert float(result.unit_cost) == pytest.approx(53333.33, rel=0.01)

    def test_receive_nonexistent_item_raises_error(self, db):
        with pytest.raises(ValueError, match="không tìm thấy"):
            InventoryService.receive("NONEXISTENT", 10, 10000)
        db.session.rollback()

    def test_issue_inventory(self, db):
        item = InventoryService.create(
            item_code="VT008",
            item_name="Vật tư xuất",
            category="nguyên vật liệu",
            unit="cái",
            quantity=100,
            unit_cost=Decimal("100000.00"),
        )
        db.session.commit()

        result, value = InventoryService.issue("VT008", 30)
        assert result.quantity == 70
        assert value == 3000000  # 30 * 100000

    def test_issue_insufficient_stock_raises_error(self, db):
        item = InventoryService.create(
            item_code="VT009",
            item_name="Vật tư",
            category="nguyên vật liệu",
            unit="cái",
            quantity=10,
            unit_cost=Decimal("100000.00"),
        )
        db.session.commit()

        with pytest.raises(ValueError, match="không đủ"):
            InventoryService.issue("VT009", 50)
        db.session.rollback()

    def test_issue_nonexistent_item_raises_error(self, db):
        with pytest.raises(ValueError, match="không tìm thấy"):
            InventoryService.issue("NONEXISTENT", 10)
        db.session.rollback()

    def test_adjust_inventory(self, db):
        item = InventoryService.create(
            item_code="VT010",
            item_name="Vật tư điều chỉnh",
            category="nguyên vật liệu",
            unit="cái",
            quantity=100,
            unit_cost=Decimal("100000.00"),
        )
        db.session.commit()

        result = InventoryService.adjust("VT010", 80, "Kiểm kê phát hiện thiếu")
        assert result.quantity == 80

    def test_adjust_nonexistent_item_raises_error(self, db):
        with pytest.raises(ValueError, match="không tìm thấy"):
            InventoryService.adjust("NONEXISTENT", 50)
        db.session.rollback()

    def test_get_summary(self, db):
        InventoryService.create(
            item_code="VT011",
            item_name="Vật tư 1",
            category="nguyên vật liệu",
            unit="cái",
            quantity=100,
            unit_cost=Decimal("100000.00"),
        )
        InventoryService.create(
            item_code="VT012",
            item_name="Vật tư 2",
            category="bán thành phẩm",
            unit="cái",
            quantity=50,
            unit_cost=Decimal("200000.00"),
        )
        db.session.commit()

        summary = InventoryService.get_summary()
        assert summary["total_items"] == 2

    def test_get_by_category(self, db):
        InventoryService.create(
            item_code="VT013",
            item_name="Item 1",
            category="nguyên vật liệu",
            unit="cái",
        )
        InventoryService.create(
            item_code="VT014",
            item_name="Item 2",
            category="bán thành phẩm",
            unit="cái",
        )
        db.session.commit()

        items = InventoryService.get_all(category="nguyên vật liệu")
        assert len(items) == 1

    def test_low_stock_detection(self, db):
        item = InventoryService.create(
            item_code="VT015",
            item_name="Item thấp",
            category="nguyên vật liệu",
            unit="cái",
            quantity=5,
            unit_cost=Decimal("10000.00"),
            min_quantity=20,
        )
        db.session.commit()

        items = InventoryService.get_all(low_stock_only=True)
        assert len(items) == 1
        assert items[0].is_low_stock is True