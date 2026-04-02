"""Tests for Mua hàng app."""

import pytest
from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError

from apps.danh_muc.models import HangHoa, NhaCungCap
from apps.mua_hang.models import DeXuatMuaHang, DonDatHang, DonDatHangChiTiet, TraHangNCC
from apps.mua_hang.services import (
    nhan_hang_don_hang,
    phan_bo_chi_phi,
    tao_don_dat_hang,
    tao_tra_hang_ncc,
    xac_nhan_don_hang,
)


@pytest.fixture
def ncc(db):
    return NhaCungCap.objects.create(
        ma_ncc="NCC-MH001",
        ten_ncc="Nhà cung cấp Mua hàng",
    )


@pytest.fixture
def hang_hoa(db):
    return HangHoa.objects.create(
        ma_hang_hoa="HH-MH001",
        ten_hang_hoa="Hàng hóa test",
        don_vi_tinh="cái",
        gia_mua=Decimal("100000"),
        gia_ban=Decimal("150000"),
    )


@pytest.fixture
def kho(db):
    from apps.nghiep_vu.models import Kho
    return Kho.objects.create(
        ma_kho="KHO-MH001",
        ten_kho="Kho Mua hàng",
    )


class TestDeXuatMuaHang:
    @pytest.mark.django_db
    def test_create_de_xuat(self):
        dx = DeXuatMuaHang.objects.create(
            so_de_xuat="DX-001",
            ngay=date(2026, 1, 15),
            nguoi_de_xuat="Nguyễn Văn A",
            ly_do="Hết hàng tồn kho",
        )
        assert dx.trang_thai == "draft"


class TestDonDatHang:
    @pytest.mark.django_db
    def test_create_don_dat_hang(self, ncc, hang_hoa):
        dh = tao_don_dat_hang(
            nha_cung_cap=ncc,
            items=[
                {"hang_hoa": hang_hoa, "so_luong": Decimal("10"), "don_gia": Decimal("100000")},
            ],
            ngay=date(2026, 1, 15),
            nguoi_tao="admin",
        )
        assert dh.tong_tien == Decimal("1000000")
        assert dh.trang_thai == "draft"
        assert dh.chi_tiet.count() == 1

    @pytest.mark.django_db
    def test_xac_nhan_don_hang(self, ncc, hang_hoa):
        dh = tao_don_dat_hang(
            nha_cung_cap=ncc,
            items=[
                {"hang_hoa": hang_hoa, "so_luong": Decimal("5"), "don_gia": Decimal("200000")},
            ],
            ngay=date(2026, 1, 15),
        )
        dh = xac_nhan_don_hang(dh)
        assert dh.trang_thai == "confirmed"

    @pytest.mark.django_db
    def test_xac_nhan_don_hang_already_confirmed(self, ncc, hang_hoa):
        dh = tao_don_dat_hang(
            nha_cung_cap=ncc,
            items=[
                {"hang_hoa": hang_hoa, "so_luong": Decimal("5"), "don_gia": Decimal("200000")},
            ],
            ngay=date(2026, 1, 15),
        )
        xac_nhan_don_hang(dh)
        with pytest.raises(ValidationError):
            xac_nhan_don_hang(dh)

    @pytest.mark.django_db
    def test_don_hang_str(self, ncc):
        dh = DonDatHang(
            so_don_hang="DH-TEST",
            ngay=date(2026, 1, 1),
            nha_cung_cap=ncc,
        )
        assert "DH-TEST" in str(dh)


class TestNhanHang:
    @pytest.mark.django_db
    def test_nhan_hang_full(self, ncc, hang_hoa, kho):
        dh = tao_don_dat_hang(
            nha_cung_cap=ncc,
            items=[
                {"hang_hoa": hang_hoa, "so_luong": Decimal("10"), "don_gia": Decimal("100000")},
            ],
            ngay=date(2026, 1, 15),
        )
        xac_nhan_don_hang(dh)
        ct = dh.chi_tiet.first()
        nhap_kho = nhan_hang_don_hang(
            don_hang=dh,
            kho=kho,
            so_luong_nhan={ct.id: Decimal("10")},
        )
        assert nhap_kho is not None
        assert nhap_kho.tong_tien == Decimal("1000000")
        dh.refresh_from_db()
        assert dh.trang_thai == "completed"

    @pytest.mark.django_db
    def test_nhan_hang_partial(self, ncc, hang_hoa, kho):
        dh = tao_don_dat_hang(
            nha_cung_cap=ncc,
            items=[
                {"hang_hoa": hang_hoa, "so_luong": Decimal("10"), "don_gia": Decimal("100000")},
            ],
            ngay=date(2026, 1, 15),
        )
        xac_nhan_don_hang(dh)
        ct = dh.chi_tiet.first()
        nhan_hang_don_hang(
            don_hang=dh,
            kho=kho,
            so_luong_nhan={ct.id: Decimal("5")},
        )
        dh.refresh_from_db()
        assert dh.trang_thai == "received"
        ct.refresh_from_db()
        assert ct.so_luong_da_nhan == Decimal("5")

    @pytest.mark.django_db
    def test_nhan_hang_exceeds_quantity(self, ncc, hang_hoa, kho):
        dh = tao_don_dat_hang(
            nha_cung_cap=ncc,
            items=[
                {"hang_hoa": hang_hoa, "so_luong": Decimal("5"), "don_gia": Decimal("100000")},
            ],
            ngay=date(2026, 1, 15),
        )
        xac_nhan_don_hang(dh)
        ct = dh.chi_tiet.first()
        with pytest.raises(ValidationError):
            nhan_hang_don_hang(
                don_hang=dh,
                kho=kho,
                so_luong_nhan={ct.id: Decimal("10")},
            )

    @pytest.mark.django_db
    def test_nhan_hang_invalid_status(self, ncc, hang_hoa, kho):
        dh = tao_don_dat_hang(
            nha_cung_cap=ncc,
            items=[
                {"hang_hoa": hang_hoa, "so_luong": Decimal("5"), "don_gia": Decimal("100000")},
            ],
            ngay=date(2026, 1, 15),
        )
        with pytest.raises(ValidationError):
            nhan_hang_don_hang(dh, kho, {1: Decimal("5")})


class TestTraHangNCC:
    @pytest.mark.django_db
    def test_create_tra_hang(self, ncc):
        th = tao_tra_hang_ncc(
            nha_cung_cap=ncc,
            nhap_kho_goc=None,
            ly_do="Hàng lỗi",
            items=[{"thanh_tien": Decimal("1000000")}],
            ngay=date(2026, 1, 20),
        )
        assert th.tong_tien == Decimal("1000000")
        assert th.trang_thai == "draft"


class TestPhanBoChiPhi:
    def test_phan_bo_theo_gia_tri(self):
        doi_tuong = [
            {"thanh_tien": Decimal("600000")},
            {"thanh_tien": Decimal("400000")},
        ]
        result = phan_bo_chi_phi("gia_tri", Decimal("100000"), doi_tuong)
        assert result[0] == Decimal("60000")
        assert result[1] == Decimal("40000")

    def test_phan_bo_theo_so_luong(self):
        doi_tuong = [
            {"so_luong": Decimal("3")},
            {"so_luong": Decimal("2")},
        ]
        result = phan_bo_chi_phi("so_luong", Decimal("50000"), doi_tuong)
        assert result[0] == Decimal("30000")
        assert result[1] == Decimal("20000")

    def test_phan_bo_invalid_method(self):
        with pytest.raises(ValidationError):
            phan_bo_chi_phi("invalid", Decimal("100000"), [])

    def test_phan_bo_zero_total(self):
        with pytest.raises(ValidationError):
            phan_bo_chi_phi("gia_tri", Decimal("100000"), [])
