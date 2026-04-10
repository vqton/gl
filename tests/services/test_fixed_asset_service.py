import pytest
from datetime import date
from decimal import Decimal
from app.services.fixed_asset_service import FixedAssetService
from app.models.fixed_asset import FixedAsset


class TestFixedAssetService:
    def test_get_all_empty(self, db):
        assets = FixedAssetService.get_all()
        assert assets == []

    def test_get_all_with_assets(self, db):
        asset = FixedAsset(
            asset_code="TS001",
            asset_name="Test Asset",
            category="máy móc",
            original_cost=Decimal("100000000.00"),
            useful_life_years=5,
            acquisition_date=date.today(),
            status="active",
        )
        db.session.add(asset)
        db.session.commit()

        assets = FixedAssetService.get_all()
        assert len(assets) == 1

    def test_get_by_id(self, db):
        asset = FixedAsset(
            asset_code="TS002",
            asset_name="Test Asset 2",
            category="máy móc",
            original_cost=Decimal("50000000.00"),
            useful_life_years=5,
            acquisition_date=date.today(),
            status="active",
        )
        db.session.add(asset)
        db.session.commit()

        found = FixedAssetService.get_by_id(asset.id)
        assert found is not None
        assert found.asset_code == "TS002"

    def test_get_by_id_not_found(self, db):
        found = FixedAssetService.get_by_id(99999)
        assert found is None

    def test_get_by_code(self, db):
        asset = FixedAsset(
            asset_code="TS003",
            asset_name="Test Asset 3",
            category="máy móc",
            original_cost=Decimal("30000000.00"),
            useful_life_years=5,
            acquisition_date=date.today(),
            status="active",
        )
        db.session.add(asset)
        db.session.commit()

        found = FixedAssetService.get_by_code("TS003")
        assert found is not None
        assert found.asset_code == "TS003"

    def test_get_by_code_not_found(self, db):
        found = FixedAssetService.get_by_code("NONEXISTENT")
        assert found is None

    def test_create_asset(self, db):
        asset = FixedAssetService.create(
            asset_code="TS004",
            asset_name="Máy tính",
            category="máy móc",
            original_cost=Decimal("20000000.00"),
            useful_life_years=3,
            acquisition_date=date(2026, 1, 1),
            location="Hà Nội",
            responsible_person="Nguyễn Văn A",
        )
        db.session.commit()

        assert asset.id is not None
        assert asset.asset_code == "TS004"
        assert asset.asset_name == "Máy tính"
        assert asset.status == "active"

    def test_create_duplicate_code_raises_error(self, db):
        FixedAssetService.create(
            asset_code="TS005",
            asset_name="Asset 1",
            category="máy móc",
            original_cost=Decimal("10000000.00"),
            useful_life_years=5,
            acquisition_date=date.today(),
        )
        db.session.commit()

        with pytest.raises(ValueError, match="đã tồn tại"):
            FixedAssetService.create(
                asset_code="TS005",
                asset_name="Asset 2",
                category="máy móc",
                original_cost=Decimal("20000000.00"),
                useful_life_years=5,
                acquisition_date=date.today(),
            )
        db.session.rollback()

    def test_create_missing_required_fields(self, db):
        with pytest.raises(ValueError, match="Mã tài sản không được để trống"):
            FixedAssetService.create(
                asset_code="",
                asset_name="Test Asset",
                category="máy móc",
                original_cost=Decimal("10000000.00"),
                useful_life_years=5,
                acquisition_date=date.today(),
            )
        db.session.rollback()

        with pytest.raises(ValueError, match="Tên tài sản không được để trống"):
            FixedAssetService.create(
                asset_code="TS006",
                asset_name="",
                category="máy móc",
                original_cost=Decimal("10000000.00"),
                useful_life_years=5,
                acquisition_date=date.today(),
            )
        db.session.rollback()

    def test_calc_monthly_depreciation(self, db):
        asset = FixedAsset(
            asset_code="TS007",
            asset_name="Test Asset",
            category="máy móc",
            original_cost=Decimal("12000000.00"),
            residual_value=Decimal("0"),
            useful_life_years=1,
            acquisition_date=date.today(),
            depreciation_start_date=date.today(),
            status="active",
        )
        db.session.add(asset)
        db.session.commit()

        monthly = FixedAssetService.calc_monthly_depreciation(asset)
        assert monthly == Decimal("1000000")  # 12M / 12 months

    def test_calc_monthly_depreciation_with_residual(self, db):
        asset = FixedAsset(
            asset_code="TS008",
            asset_name="Test Asset",
            category="máy móc",
            original_cost=Decimal("12000000.00"),
            residual_value=Decimal("1200000.00"),
            useful_life_years=1,
            acquisition_date=date.today(),
            depreciation_start_date=date.today(),
            status="active",
        )
        db.session.add(asset)
        db.session.commit()

        monthly = FixedAssetService.calc_monthly_depreciation(asset)
        assert monthly == Decimal("900000")  # (12M - 1.2M) / 12

    def test_dispose_asset(self, db):
        asset = FixedAssetService.create(
            asset_code="TS009",
            asset_name="Asset to Dispose",
            category="máy móc",
            original_cost=Decimal("10000000.00"),
            useful_life_years=5,
            acquisition_date=date(2025, 1, 1),
        )
        db.session.commit()

        result = FixedAssetService.dispose_asset(
            asset.id,
            disposal_date=date(2026, 4, 10),
            disposal_value=Decimal("5000000.00"),
            reason="Bán thanh lý",
        )
        assert result.status == "disposed"
        assert result.disposal_value == Decimal("5000000.00")

    def test_dispose_non_existent_raises_error(self, db):
        with pytest.raises(ValueError, match="không tìm thấy"):
            FixedAssetService.dispose_asset(99999, date.today())
        db.session.rollback()

    def test_dispose_already_disposed_raises_error(self, db):
        asset = FixedAssetService.create(
            asset_code="TS010",
            asset_name="Asset",
            category="máy móc",
            original_cost=Decimal("10000000.00"),
            useful_life_years=5,
            acquisition_date=date(2025, 1, 1),
        )
        db.session.commit()

        FixedAssetService.dispose_asset(asset.id, date.today())

        with pytest.raises(ValueError, match="đang hoạt động"):
            FixedAssetService.dispose_asset(asset.id, date.today())
        db.session.rollback()

    def test_get_summary(self, db):
        FixedAssetService.create(
            asset_code="TS011",
            asset_name="Asset 1",
            category="máy móc",
            original_cost=Decimal("10000000.00"),
            useful_life_years=5,
            acquisition_date=date(2025, 1, 1),
        )
        FixedAssetService.create(
            asset_code="TS012",
            asset_name="Asset 2",
            category="phương tiện",
            original_cost=Decimal("50000000.00"),
            useful_life_years=5,
            acquisition_date=date(2025, 1, 1),
        )
        db.session.commit()

        summary = FixedAssetService.get_summary()
        assert summary["total_cost"] == 60000000
        assert summary["active_count"] == 2

    def test_run_monthly_depreciation(self, db):
        asset = FixedAsset(
            asset_code="TS013",
            asset_name="Asset for Depreciation",
            category="máy móc",
            original_cost=Decimal("12000000.00"),
            residual_value=Decimal("0"),
            useful_life_years=1,
            acquisition_date=date(2026, 1, 1),
            depreciation_start_date=date(2026, 1, 1),
            status="active",
            accumulated_depreciation=Decimal("0"),
        )
        db.session.add(asset)
        db.session.commit()

        result = FixedAssetService.run_monthly_depreciation("2026-02")
        assert result["asset_count"] == 1
        assert result["total_depreciation"] > 0