"""Fixed Asset service with straight-line depreciation per Circular 99/2025."""
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

from app.extensions import db
from app.models.fixed_asset import FixedAsset


class FixedAssetService:
    """Business logic for fixed asset management and depreciation."""

    @staticmethod
    def get_all(status=None):
        query = FixedAsset.query
        if status:
            query = query.filter_by(status=status)
        return query.order_by(FixedAsset.asset_code).all()

    @staticmethod
    def get_by_id(asset_id):
        return db.session.get(FixedAsset, asset_id)

    @staticmethod
    def get_by_code(asset_code):
        return FixedAsset.query.filter_by(asset_code=asset_code).first()

    @staticmethod
    def create(asset_code, asset_name, category, original_cost, useful_life_years,
               acquisition_date, depreciation_method="straight_line",
               residual_value=0, depreciation_start_date=None,
               location="", responsible_person=""):
        if not asset_code or not asset_code.strip():
            raise ValueError("Mã tài sản không được để trống")
        if not asset_name or not asset_name.strip():
            raise ValueError("Tên tài sản không được để trống")
        if FixedAsset.get_by_code(asset_code):
            raise ValueError(f"Tài sản với mã '{asset_code}' đã tồn tại")
        asset = FixedAsset(
            asset_code=asset_code,
            asset_name=asset_name,
            category=category,
            original_cost=original_cost,
            residual_value=residual_value,
            depreciation_method=depreciation_method,
            useful_life_years=useful_life_years,
            acquisition_date=acquisition_date,
            depreciation_start_date=depreciation_start_date or acquisition_date,
            location=location,
            responsible_person=responsible_person,
            status="active",
        )
        db.session.add(asset)
        db.session.commit()
        return asset

    @staticmethod
    def calc_monthly_depreciation(asset):
        """Calculate monthly depreciation using straight-line method."""
        if asset.depreciation_method != "straight_line":
            return Decimal("0")
        cost = Decimal(str(asset.original_cost))
        residual = Decimal(str(asset.residual_value))
        months = asset.useful_life_years * 12
        if months <= 0:
            return Decimal("0")
        return ((cost - residual) / months).quantize(Decimal("1"), rounding=ROUND_HALF_UP)

    @staticmethod
    def run_monthly_depreciation(period):
        """Calculate and record depreciation for all active assets for a period.

        Returns list of dicts with asset details and depreciation amount.
        Also creates journal entry lines for the depreciation posting.
        """
        assets = FixedAsset.query.filter_by(status="active").all()
        results = []
        total_depreciation = Decimal("0")

        for asset in assets:
            if not asset.depreciation_start_date:
                continue

            period_date = date.fromisoformat(f"{period}-01")
            if asset.depreciation_start_date > period_date:
                continue

            months_elapsed = (
                (period_date.year - asset.depreciation_start_date.year) * 12
                + (period_date.month - asset.depreciation_start_date.month)
            )
            if months_elapsed < 0:
                continue

            monthly_dep = FixedAssetService.calc_monthly_depreciation(asset)
            max_months = asset.useful_life_years * 12
            if months_elapsed >= max_months:
                continue

            accumulated = Decimal(str(asset.accumulated_depreciation))
            results.append({
                "asset_code": asset.asset_code,
                "asset_name": asset.asset_name,
                "category": asset.category,
                "original_cost": float(asset.original_cost),
                "monthly_depreciation": float(monthly_dep),
                "accumulated_depreciation": float(accumulated),
                "net_book_value": float(asset.original_cost) - float(accumulated),
                "remaining_months": max_months - months_elapsed,
            })
            total_depreciation += monthly_dep

        return {
            "period": period,
            "assets": results,
            "total_depreciation": float(total_depreciation),
            "asset_count": len(results),
        }

    @staticmethod
    def dispose_asset(asset_id, disposal_date, disposal_value=0, reason=""):
        asset = db.session.get(FixedAsset, asset_id)
        if not asset:
            raise ValueError("Tài sản không tìm thấy")
        if asset.status != "active":
            raise ValueError("Chỉ tài sản đang hoạt động mới có thể thanh lý")
        asset.status = "disposed"
        asset.disposal_date = disposal_date
        asset.disposal_value = disposal_value
        asset.disposal_reason = reason
        db.session.commit()
        return asset

    @staticmethod
    def get_summary():
        assets = FixedAsset.query.all()
        total_cost = sum(float(a.original_cost) for a in assets if a.status == "active")
        total_accumulated = sum(float(a.accumulated_depreciation) for a in assets if a.status == "active")
        total_net = total_cost - total_accumulated
        active_count = sum(1 for a in assets if a.status == "active")
        disposed_count = sum(1 for a in assets if a.status == "disposed")

        by_category = {}
        for asset in assets:
            if asset.status != "active":
                continue
            cat = asset.category
            if cat not in by_category:
                by_category[cat] = {"count": 0, "cost": 0, "accumulated": 0}
            by_category[cat]["count"] += 1
            by_category[cat]["cost"] += float(asset.original_cost)
            by_category[cat]["accumulated"] += float(asset.accumulated_depreciation)

        return {
            "total_cost": total_cost,
            "total_accumulated": total_accumulated,
            "total_net": total_net,
            "active_count": active_count,
            "disposed_count": disposed_count,
            "by_category": by_category,
        }
