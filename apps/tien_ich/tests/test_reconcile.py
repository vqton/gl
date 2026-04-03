"""Tests for reconcile_balances validator."""

from decimal import Decimal

import pytest

from apps.danh_muc.models import HangHoa, KhachHang, NhaCungCap, TaiKhoanKeToan
from apps.he_thong.models import SoDuDauKy
from apps.kho.models import Kho, VatTuHangHoa
from apps.tai_san.models import TaiSanCoDinh
from apps.tien_ich.validator import reconcile_balances


@pytest.fixture
def setup_gl_accounts(db):
    """Create all GL accounts needed for reconciliation tests."""
    accounts = {}
    for code, name, loai in [
        ("111", "Tiền mặt", "tai_san"),
        ("131", "Phải thu khách hàng", "tai_san"),
        ("331", "Phải trả người bán", "no_phai_tra"),
        ("156", "Hàng hóa", "tai_san"),
        ("211", "Tài sản cố định", "tai_san"),
        ("214", "Hao mòn TSCĐ", "tai_san"),
        ("411", "Vốn chủ sở hữu", "von_chu_so_huu"),
    ]:
        tk, _ = TaiKhoanKeToan.objects.get_or_create(
            ma_tai_khoan=code,
            defaults={
                "ten_tai_khoan": name,
                "cap_do": 1,
                "loai_tai_khoan": loai,
            },
        )
        accounts[code] = tk
    return accounts


@pytest.fixture
def kho_chn(db):
    return Kho.objects.create(ma_kho="KHN", ten_kho="Kho chính")


@pytest.fixture
def hang_hoa(db):
    hh = HangHoa.objects.create(
        ma_hang_hoa="HH001",
        ten_hang_hoa="Hàng mẫu",
        don_vi_tinh="cái",
    )
    return VatTuHangHoa.objects.create(hang_hoa=hh, phuong_phap_tinh_gia="FIFO")


@pytest.fixture
def tai_san(db):
    return TaiSanCoDinh.objects.create(
        ma_tai_san="TS001",
        ten_tai_san="Máy tính",
        nguyen_gia=Decimal("20000000"),
        thoi_gian_khau_hao_thang=36,
        ngay_dua_vao_su_dung="2026-01-01",
    )


class TestReconcileBalancesEmpty:
    """Test reconciliation with no data."""

    def test_empty_year_returns_success(self, db):
        """Test that empty year returns success with zero totals."""
        result = reconcile_balances(2026)
        assert result["valid"] is True
        assert result["errors"] == []


class TestReconcileBalancesNoCo:
    """Test Nợ = Có validation."""

    def test_balanced_gl_passes(self, setup_gl_accounts):
        """Test balanced GL passes reconciliation."""
        accounts = setup_gl_accounts
        SoDuDauKy.objects.create(
            tai_khoan=accounts["111"],
            so_du_no=Decimal("100000000"),
            so_du_co=Decimal("0"),
            nam=2026,
        )
        SoDuDauKy.objects.create(
            tai_khoan=accounts["411"],
            so_du_no=Decimal("0"),
            so_du_co=Decimal("100000000"),
            nam=2026,
        )
        result = reconcile_balances(2026)
        assert result["valid"] is True
        assert result["tong_no"] == Decimal("100000000")
        assert result["tong_co"] == Decimal("100000000")

    def test_unbalanced_gl_fails(self, setup_gl_accounts):
        """Test unbalanced GL fails reconciliation."""
        accounts = setup_gl_accounts
        SoDuDauKy.objects.create(
            tai_khoan=accounts["111"],
            so_du_no=Decimal("100000000"),
            so_du_co=Decimal("0"),
            nam=2026,
        )
        SoDuDauKy.objects.create(
            tai_khoan=accounts["411"],
            so_du_no=Decimal("0"),
            so_du_co=Decimal("80000000"),
            nam=2026,
        )
        result = reconcile_balances(2026)
        assert result["valid"] is False
        assert len(result["errors"]) > 0
        assert any("chênh lệch" in e.lower() for e in result["errors"])


class TestReconcileBalancesSubLedger:
    """Test sub-ledger reconciliation."""

    def test_customer_subledger_matches_gl(self, setup_gl_accounts):
        """Test customer sub-ledger total matches GL account 131."""
        accounts = setup_gl_accounts
        KhachHang.objects.create(
            ma_kh="KH001",
            ten_kh="Khách hàng mẫu",
        )
        SoDuDauKy.objects.create(
            tai_khoan=accounts["131"],
            doi_tuong_ma="KH001",
            so_du_no=Decimal("50000000"),
            so_du_co=Decimal("0"),
            nam=2026,
        )
        SoDuDauKy.objects.create(
            tai_khoan=accounts["411"],
            so_du_no=Decimal("0"),
            so_du_co=Decimal("50000000"),
            nam=2026,
        )
        result = reconcile_balances(2026)
        assert result["valid"] is True
        assert result["sub_ledger_131"] == Decimal("50000000")
        assert result["gl_131"] == Decimal("50000000")

    def test_customer_subledger_mismatch_fails(self, setup_gl_accounts):
        """Test customer sub-ledger mismatch fails reconciliation."""
        accounts = setup_gl_accounts
        SoDuDauKy.objects.create(
            tai_khoan=accounts["131"],
            so_du_no=Decimal("100000000"),
            so_du_co=Decimal("0"),
            nam=2026,
        )
        SoDuDauKy.objects.create(
            tai_khoan=accounts["131"],
            doi_tuong_ma="KH001",
            so_du_no=Decimal("50000000"),
            so_du_co=Decimal("0"),
            nam=2026,
        )
        SoDuDauKy.objects.create(
            tai_khoan=accounts["111"],
            so_du_no=Decimal("150000000"),
            so_du_co=Decimal("0"),
            nam=2026,
        )
        result = reconcile_balances(2026)
        assert result["valid"] is False
        assert any("131" in e for e in result["errors"])

    def test_supplier_subledger_matches_gl(self, setup_gl_accounts):
        """Test supplier sub-ledger total matches GL account 331."""
        accounts = setup_gl_accounts
        NhaCungCap.objects.create(
            ma_ncc="NCC001",
            ten_ncc="Nhà cung cấp mẫu",
        )
        SoDuDauKy.objects.create(
            tai_khoan=accounts["331"],
            doi_tuong_ma="NCC001",
            so_du_no=Decimal("0"),
            so_du_co=Decimal("30000000"),
            nam=2026,
        )
        SoDuDauKy.objects.create(
            tai_khoan=accounts["111"],
            so_du_no=Decimal("30000000"),
            so_du_co=Decimal("0"),
            nam=2026,
        )
        result = reconcile_balances(2026)
        assert result["valid"] is True
        assert result["sub_ledger_331"] == Decimal("30000000")
        assert result["gl_331"] == Decimal("30000000")


class TestReconcileBalancesInventory:
    """Test inventory sub-ledger reconciliation."""

    def test_inventory_subledger_matches_gl(self, setup_gl_accounts, kho_chn, hang_hoa):
        """Test inventory sub-ledger total matches GL account 156."""
        accounts = setup_gl_accounts
        SoDuDauKy.objects.create(
            tai_khoan=accounts["156"],
            kho=kho_chn,
            hang_hoa=hang_hoa,
            so_du_no=Decimal("20000000"),
            so_du_co=Decimal("0"),
            nam=2026,
        )
        SoDuDauKy.objects.create(
            tai_khoan=accounts["411"],
            so_du_no=Decimal("0"),
            so_du_co=Decimal("20000000"),
            nam=2026,
        )
        result = reconcile_balances(2026)
        assert result["valid"] is True
        assert result["sub_ledger_156"] == Decimal("20000000")
        assert result["gl_156"] == Decimal("20000000")


class TestReconcileBalancesFixedAssets:
    """Test fixed asset sub-ledger reconciliation."""

    def test_fixed_asset_subledger_matches_gl(self, setup_gl_accounts, tai_san):
        """Test fixed asset sub-ledger matches GL account 211."""
        accounts = setup_gl_accounts
        SoDuDauKy.objects.create(
            tai_khoan=accounts["211"],
            tai_san=tai_san,
            so_du_no=Decimal("20000000"),
            so_du_co=Decimal("0"),
            nam=2026,
        )
        SoDuDauKy.objects.create(
            tai_khoan=accounts["411"],
            so_du_no=Decimal("0"),
            so_du_co=Decimal("20000000"),
            nam=2026,
        )
        result = reconcile_balances(2026)
        assert result["valid"] is True
        assert result["sub_ledger_211"] == Decimal("20000000")
        assert result["gl_211"] == Decimal("20000000")
