"""Mua hàng services - PO processing, cost allocation."""

import logging
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.danh_muc.models import HangHoa, NhaCungCap
from apps.mua_hang.models import DonDatHang, DonDatHangChiTiet, TraHangNCC
from apps.nghiep_vu.models import NhapKho, NhapKhoChiTiet

logger = logging.getLogger(__name__)


@transaction.atomic
def tao_don_dat_hang(
    nha_cung_cap: NhaCungCap,
    items: list[dict],
    ngay=None,
    ngay_giao_du_kien=None,
    nguoi_tao: str = "",
) -> DonDatHang:
    """
    Create purchase order with line items.

    Args:
        nha_cung_cap: Supplier
        items: List of dicts with keys: hang_hoa, so_luong, don_gia
        ngay: Order date
        ngay_giao_du_kien: Expected delivery date
        nguoi_tao: Creator username
    """
    from datetime import date as date_cls

    if ngay is None:
        ngay = date_cls.today()

    count = DonDatHang.objects.filter(ngay__year=ngay.year).count() + 1
    so_don = f"DH{ngay.strftime('%Y%m%d')}{count:04d}"

    don_hang = DonDatHang.objects.create(
        so_don_hang=so_don,
        ngay=ngay,
        nha_cung_cap=nha_cung_cap,
        ngay_giao_du_kien=ngay_giao_du_kien,
        created_by=nguoi_tao,
    )

    tong_tien = Decimal("0")
    for item in items:
        hh = item["hang_hoa"]
        if isinstance(hh, str):
            hh = HangHoa.objects.get(ma_hang_hoa=hh)

        so_luong = item["so_luong"]
        don_gia = item["don_gia"]
        thanh_tien = (so_luong * don_gia).quantize(Decimal("0.01"))
        tong_tien += thanh_tien

        DonDatHangChiTiet.objects.create(
            don_hang=don_hang,
            hang_hoa=hh,
            so_luong=so_luong,
            don_gia=don_gia,
            thanh_tien=thanh_tien,
        )

    don_hang.tong_tien = tong_tien
    don_hang.save()

    return don_hang


@transaction.atomic
def xac_nhan_don_hang(don_hang: DonDatHang) -> DonDatHang:
    """
    Confirm a purchase order (draft → confirmed).
    """
    if don_hang.trang_thai != "draft":
        raise ValidationError(
            {"trang_thai": ["Chỉ có thể xác nhận đơn hàng ở trạng thái nháp"]}
        )
    if not don_hang.chi_tiet.exists():
        raise ValidationError({"chi_tiet": ["Đơn hàng phải có ít nhất một mặt hàng"]})

    don_hang.trang_thai = "confirmed"
    don_hang.save()
    return don_hang


@transaction.atomic
def nhan_hang_don_hang(
    don_hang: DonDatHang,
    kho,
    so_luong_nhan: dict,
    nguoi_tao: str = "",
) -> NhapKho:
    """
    Receive goods from a purchase order (partial or full).

    Args:
        don_hang: Purchase order
        kho: Warehouse
        so_luong_nhan: Dict mapping chi_tiet.id to quantity received
        nguoi_tao: Creator username
    """
    if don_hang.trang_thai not in ("confirmed", "received"):
        raise ValidationError(
            {"trang_thai": ["Đơn hàng phải ở trạng thái đã xác nhận hoặc đã nhận hàng"]}
        )

    tong_tien = Decimal("0")
    items = []
    for ct_id, so_luong in so_luong_nhan.items():
        ct = DonDatHangChiTiet.objects.get(id=ct_id, don_hang=don_hang)
        if ct.so_luong_da_nhan + so_luong > ct.so_luong:
            raise ValidationError(
                {f"chi_tiet_{ct_id}": [
                    f"Số lượng nhận ({so_luong}) vượt quá số lượng còn lại "
                    f"({ct.so_luong - ct.so_luong_da_nhan})"
                ]}
            )
        thanh_tien = (so_luong * ct.don_gia).quantize(Decimal("0.01"))
        tong_tien += thanh_tien
        items.append({
            "hang_hoa": ct.hang_hoa,
            "so_luong": so_luong,
            "don_gia": ct.don_gia,
            "thanh_tien": thanh_tien,
        })

    from datetime import date as date_cls

    count = NhapKho.objects.filter(ngay__year=date_cls.today().year).count() + 1
    so_chung_tu = f"NK-DH{date_cls.today().strftime('%Y%m%d')}{count:04d}"

    nhap_kho = NhapKho.objects.create(
        so_chung_tu=so_chung_tu,
        ngay=date_cls.today(),
        kho=kho,
        nha_cung_cap=don_hang.nha_cung_cap,
        tong_tien=tong_tien,
        trang_thai="completed",
        created_by=nguoi_tao,
    )

    for item in items:
        NhapKhoChiTiet.objects.create(
            nhap_kho=nhap_kho,
            hang_hoa=item["hang_hoa"],
            so_luong=item["so_luong"],
            don_gia=item["don_gia"],
            thanh_tien=item["thanh_tien"],
        )

    for ct_id, so_luong in so_luong_nhan.items():
        ct = DonDatHangChiTiet.objects.get(id=ct_id)
        ct.so_luong_da_nhan += so_luong
        ct.save()

    all_received = all(
        ct.so_luong_da_nhan >= ct.so_luong
        for ct in don_hang.chi_tiet.all()
    )
    if all_received:
        don_hang.trang_thai = "completed"
    else:
        don_hang.trang_thai = "received"
    don_hang.save()

    return nhap_kho


@transaction.atomic
def tao_tra_hang_ncc(
    nha_cung_cap: NhaCungCap,
    nhap_kho_goc: NhapKho,
    ly_do: str,
    items: list[dict],
    ngay=None,
) -> TraHangNCC:
    """
    Create purchase return referencing original receipt.
    """
    from datetime import date as date_cls

    if ngay is None:
        ngay = date_cls.today()

    count = TraHangNCC.objects.filter(ngay__year=ngay.year).count() + 1
    so_chung_tu = f"THN{ngay.strftime('%Y%m%d')}{count:04d}"

    tong_tien = Decimal("0")
    for item in items:
        tong_tien += item.get("thanh_tien", Decimal("0"))
        if nhap_kho_goc and tong_tien > nhap_kho_goc.tong_tien:
            raise ValidationError(
                {"items": ["Tổng tiền trả không được vượt quá tổng tiền nhập"]}
            )

    tra_hang = TraHangNCC.objects.create(
        so_chung_tu=so_chung_tu,
        ngay=ngay,
        nha_cung_cap=nha_cung_cap,
        ly_do_tra=ly_do,
        tong_tien=tong_tien,
    )

    return tra_hang


def phan_bo_chi_phi(theo: str, tong_chi_phi: Decimal, doi_tuong: list) -> dict:
    """
    Allocate costs to goods by value or quantity.

    Args:
        theo: 'gia_tri' or 'so_luong'
        tong_chi_phi: Total cost to allocate
        doi_tuong: List of dicts with 'thanh_tien' or 'so_luong' keys
    """
    if theo == "gia_tri":
        tong = sum(d.get("thanh_tien", 0) for d in doi_tuong)
    elif theo == "so_luong":
        tong = sum(d.get("so_luong", 0) for d in doi_tuong)
    else:
        raise ValidationError({"theo": ["Phải là 'gia_tri' hoặc 'so_luong'"]})

    if tong == 0:
        raise ValidationError({"doi_tuong": ["Tổng giá trị/số lượng không được bằng 0"]})

    result = {}
    for i, d in enumerate(doi_tuong):
        if theo == "gia_tri":
            ti_le = d.get("thanh_tien", 0) / tong
        else:
            ti_le = d.get("so_luong", 0) / tong
        result[i] = (tong_chi_phi * ti_le).quantize(Decimal("0.01"))

    return result
