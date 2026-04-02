"""Tests for Phân Tích Tài Chính services."""

import pytest
from datetime import date
from decimal import Decimal

from apps.phan_tich.services import PhanTichTaiChinhService, _safe_div


class TestSafeDiv:
    def test_normal_division(self):
        result = _safe_div(Decimal("100"), Decimal("4"))
        assert result == Decimal("25")

    def test_division_by_zero(self):
        result = _safe_div(Decimal("100"), Decimal("0"))
        assert result == Decimal("0")

    def test_division_by_zero_custom_default(self):
        result = _safe_div(
            Decimal("100"), Decimal("0"), default=Decimal("-1")
        )
        assert result == Decimal("-1")

    def test_decimal_precision(self):
        result = _safe_div(Decimal("100"), Decimal("3"))
        assert result == Decimal("33.3333")


class TestPhanTichTaiChinhService:
    @pytest.fixture
    def service(self):
        return PhanTichTaiChinhService(
            tu_ngay=date(2026, 1, 1),
            den_ngay=date(2026, 3, 31),
        )

    def test_init(self, service):
        assert service.tu_ngay == date(2026, 1, 1)
        assert service.den_ngay == date(2026, 3, 31)

    def test_get_bang_tong_hop_empty_data(self, db, service):
        result = service.get_bang_tong_hop()
        assert "period" in result
        assert "ratios" in result
        assert "health" in result
        assert result["period"]["tu_ngay"] == "2026-01-01"
        assert result["period"]["den_ngay"] == "2026-03-31"

    def test_health_score_empty_data(self, db, service):
        health = service.get_suc_khoe_doanh_nghiep()
        assert "score" in health
        assert "rating" in health
        assert "warnings" in health
        assert isinstance(health["score"], int)
        assert 0 <= health["score"] <= 100

    def test_health_rating_weak(self, db, service):
        health = service.get_suc_khoe_doanh_nghiep()
        assert health["rating"] == "Yếu"
        assert health["score"] == 30

    def test_get_trend_data(self, db, service):
        trend = service.get_trend_data(so_ky=2)
        assert "periods" in trend
        assert len(trend["periods"]) == 2

    def test_he_so_thanh_toan_empty(self, db, service):
        ratios = service.get_he_so_thanh_toan()
        assert ratios["hien_hanh"] == Decimal("0")
        assert ratios["nhanh"] == Decimal("0")
        assert ratios["tuc_thoi"] == Decimal("0")

    def test_he_so_no_empty(self, db, service):
        ratios = service.get_he_so_no()
        assert ratios["he_so_no"] == Decimal("0")
        assert ratios["tu_tai_tro"] == Decimal("0")
        assert ratios["cau_truc_von"] == Decimal("0")

    def test_hieu_qua_hoat_dong_empty(self, db, service):
        ratios = service.get_hieu_qua_hoat_dong()
        assert ratios["vong_quay_ton_kho"] == Decimal("0")
        assert ratios["ky_thu_tien"] == Decimal("0")
        assert ratios["vong_quay_tai_san"] == Decimal("0")

    def test_kha_nang_sinh_loi_empty(self, db, service):
        ratios = service.get_kha_nang_sinh_loi()
        assert ratios["bien_loi_nhuan_gop"] == Decimal("0")
        assert ratios["bien_loi_nhuan_rong"] == Decimal("0")
        assert ratios["roa"] == Decimal("0")
        assert ratios["roe"] == Decimal("0")

    def test_dong_tien_empty(self, db, service):
        ratios = service.get_dong_tien()
        assert ratios["cfo"] == Decimal("0")
        assert ratios["free_cash_flow"] == Decimal("0")
        assert ratios["ty_le_dong_tien"] == Decimal("0")
