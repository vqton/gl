"""Business logic services for Vietnamese SME Accounting System."""

import decimal
import logging
from datetime import date
from typing import Optional

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction

from apps.danh_muc.models import (
    HangHoa,
    KhachHang,
    NhaCungCap,
    TaiKhoanKeToan,
)
from apps.nghiep_vu.models import Kho
from apps.nghiep_vu.constants import (
    THUE_SUAT_GTGT,
    THUE_SUAT_TNDN_DEFAULT,
    THUE_SUAT_TNDN_SME,
    NGUONG_DOANH_THU_SME,
)
from apps.nghiep_vu.models import (
    ButToan,
    ButToanChiTiet,
    HoaDon,
    HoaDonChiTiet,
    NhapKho,
    NhapKhoChiTiet,
    PhieuThu,
    PhieuChi,
    XuatKho,
    XuatKhoChiTiet,
    Kho,
)
from apps.nghiep_vu.validators import (
    validate_hoa_don,
    validate_ngay_chung_tu,
    validate_tai_khoan_no_co,
)

logger = logging.getLogger(__name__)


def tinh_thue_gtgt(
    so_tien: decimal.Decimal,
    thue_suat: str = "10",
) -> decimal.Decimal:
    """
    Calculate Value Added Tax (VAT/GTGT) amount.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on VAT calculation
        - Luật Thuế giá trị gia tăng

    Args:
        so_tien: Value of goods/services before VAT
        thue_suat: VAT rate as string ('0', '5', '8', '10')

    Returns:
        VAT amount as decimal
    """
    if so_tien < decimal.Decimal("0"):
        raise ValidationError({"so_tien": ["Số tiền không được âm"]})

    if thue_suat not in THUE_SUAT_GTGT:
        raise ValidationError(
            {
                "thue_suat": [
                    f"Thuế suất không hợp lệ. "
                    f'Chỉ chấp nhận: {", ".join(THUE_SUAT_GTGT.keys())}'
                ]
            }
        )

    rate = THUE_SUAT_GTGT[thue_suat]
    return (so_tien * rate).quantize(decimal.Decimal("0.01"))


def tinh_thue_tndn_sme(lai_nhuan: decimal.Decimal) -> decimal.Decimal:
    """
    Calculate Corporate Income Tax (TNDN) for SME.

    Legal basis:
        - Luật 67/2025/QH15 about Corporate Income Tax
        - Nghị định 320/2025/NĐ-CP implementation
        - Thông tư 99/2025/TT-BTC for SME provisions

    Tax rates:
        - 15% for SME (revenue < 3 billion VND)
        - 20% for standard enterprises

    Args:
        lai_nhuan: Pre-tax profit (decimal)

    Returns:
        Tax amount as decimal
    """
    if lai_nhuan < decimal.Decimal("0"):
        return decimal.Decimal("0")

    return (lai_nhuan * THUE_SUAT_TNDN_SME).quantize(decimal.Decimal("0.01"))


def tinh_thue_tndn(
    doanh_thu: decimal.Decimal,
    lai_nhuan: decimal.Decimal,
) -> decimal.Decimal:
    """
    Calculate Corporate Income Tax based on revenue threshold.

    Legal basis:
        - Luật 67/2025/QH15 about Corporate Income Tax
        - Nghị định 320/2025/NĐ-CP implementation

    Args:
        doanh_thu: Annual revenue
        lai_nhuan: Pre-tax profit

    Returns:
        Tax amount as decimal
    """
    if lai_nhuan < decimal.Decimal("0"):
        return decimal.Decimal("0")

    if doanh_thu < NGUONG_DOANH_THU_SME:
        rate = THUE_SUAT_TNDN_SME
    else:
        rate = THUE_SUAT_TNDN_DEFAULT

    return (lai_nhuan * rate).quantize(decimal.Decimal("0.01"))


@transaction.atomic
def tao_but_toan(
    ngay: date,
    dien_giai: str,
    chi_tiet: list[dict],
    nguoi_tao: Optional[User] = None,
    so_but_toan: Optional[str] = None,
) -> ButToan:
    """
    Create journal entry with validation.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on journal entries
        - Chế độ kế toán doanh nghiệp nhỏ và vừa

    Args:
        ngay: Accounting date
        dien_giai: Description
        chi_tiet: List of dicts with keys:
            - tai_khoan: TaiKhoanKeToan instance or account code
            - loai_no_co: 'no' or 'co'
            - so_tien: Decimal amount
            - ma_doi_tuong: Optional object code
            - dien_giai: Optional line description
        nguoi_tao: User creating the entry
        so_but_toan: Optional voucher number (auto-generated if None)

    Returns:
        Created ButToan instance

    Raises:
        ValidationError: If validation fails
    """
    validate_ngay_chung_tu(ngay)

    if not chi_tiet:
        raise ValidationError({"chi_tiet": ["Bút toán phải có ít nhất một chi tiết"]})

    tong_no = decimal.Decimal("0")
    tong_co = decimal.Decimal("0")

    for line in chi_tiet:
        if line["so_tien"] <= decimal.Decimal("0"):
            raise ValidationError({"chi_tiet": ["Số tiền phải lớn hơn 0"]})
        if line["loai_no_co"] == "no":
            tong_no += line["so_tien"]
        else:
            tong_co += line["so_tien"]

    if abs(tong_no - tong_co) > decimal.Decimal("0.01"):
        raise ValidationError(
            {"chi_tiet": [f"Tổng Nợ ({tong_no}) không bằng tổng Có ({tong_co})"]}
        )

    if not so_but_toan:
        count = ButToan.objects.filter(ngay_hach_toan__year=ngay.year).count() + 1
        so_but_toan = f'BT{ngay.strftime("%Y%m%d")}{count:04d}'

    but_toan = ButToan.objects.create(
        so_but_toan=so_but_toan,
        ngay_hach_toan=ngay,
        dien_giai=dien_giai,
        nguoi_tao=nguoi_tao,
    )

    for line in chi_tiet:
        tk = line["tai_khoan"]
        if isinstance(tk, str):
            tk = TaiKhoanKeToan.objects.get(ma_tai_khoan=tk)

        ButToanChiTiet.objects.create(
            but_toan=but_toan,
            tai_khoan=tk,
            loai_no_co=line["loai_no_co"],
            so_tien=line["so_tien"],
            ma_doi_tuong=line.get("ma_doi_tuong", ""),
            dien_giai=line.get("dien_giai", ""),
        )

    logger.info(
        "Created journal entry %s with %d lines",
        so_but_toan,
        len(chi_tiet),
    )
    return but_toan


@transaction.atomic
def tao_hoa_don(
    khach_hang: KhachHang,
    items: list[dict],
    ngay_hoa_don: Optional[date] = None,
    hinh_thuc_thanh_toan: str = "tien_mat",
    nguoi_tao: Optional[str] = None,
) -> HoaDon:
    """
    Create sales invoice with auto journal entries.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on invoice requirements
        - Nghị định 320/2025/NĐ-CP on e-invoice implementation

    Args:
        khach_hang: Customer instance
        items: List of dicts with keys:
            - hang_hoa: HangHoa instance or product code
            - so_luong: Decimal quantity
            - don_gia: Decimal unit price
            - thue_suat: Tax rate string ('0', '5', '8', '10')
        ngay_hoa_don: Invoice date (default today)
        hinh_thuc_thanh_toan: Payment method
        nguoi_tao: Creator username

    Returns:
        Created HoaDon instance
    """
    from datetime import date as date_cls

    if ngay_hoa_don is None:
        ngay_hoa_don = date_cls.today()

    validate_ngay_chung_tu(ngay_hoa_don)

    if not items:
        raise ValidationError({"items": ["Hóa đơn phải có ít nhất một mặt hàng"]})

    tong_tien_truoc_thue = decimal.Decimal("0")
    tien_thue_gtgt = decimal.Decimal("0")

    hoa_don_count = (
        HoaDon.objects.filter(ngay_hoa_don__year=ngay_hoa_don.year).count() + 1
    )
    so_hoa_don = f'HD{ngay_hoa_don.strftime("%Y%m%d")}{hoa_don_count:04d}'

    hoa_don = HoaDon.objects.create(
        so_hoa_don=so_hoa_don,
        ngay_hoa_don=ngay_hoa_don,
        khach_hang=khach_hang,
        hinh_thuc_thanh_toan=hinh_thuc_thanh_toan,
        created_by=nguoi_tao or "",
    )

    for item in items:
        hh = item["hang_hoa"]
        if isinstance(hh, str):
            hh = HangHoa.objects.get(ma_hang_hoa=hh)

        so_luong = item["so_luong"]
        don_gia = item["don_gia"]
        thue_suat = item.get("thue_suat", hh.thue_suat_gtgt)

        thanh_tien = (so_luong * don_gia).quantize(decimal.Decimal("0.01"))
        tien_thue = tinh_thue_gtgt(thanh_tien, thue_suat)
        tong_tien = thanh_tien + tien_thue

        tong_tien_truoc_thue += thanh_tien
        tien_thue_gtgt += tien_thue

        HoaDonChiTiet.objects.create(
            hoa_don=hoa_don,
            hang_hoa=hh,
            so_luong=so_luong,
            don_gia=don_gia,
            thue_suat=thue_suat,
            tien_thue=tien_thue,
            tong_tien=tong_tien,
        )

    tong_cong = tong_tien_truoc_thue + tien_thue_gtgt

    validate_hoa_don(tong_tien_truoc_thue, tien_thue_gtgt, tong_cong)

    hoa_don.tong_tien_truoc_thue = tong_tien_truoc_thue
    hoa_don.tien_thue_gtgt = tien_thue_gtgt
    hoa_don.tong_cong_thanh_toan = tong_cong
    hoa_don.save()

    logger.info(
        "Created invoice %s for customer %s",
        so_hoa_don,
        khach_hang.ma_kh,
    )
    return hoa_don


@transaction.atomic
def tao_nhap_kho(
    nha_cung_cap: NhaCungCap,
    kho: Kho,
    items: list[dict],
    ngay: Optional[date] = None,
    nguoi_tao: Optional[str] = None,
) -> NhapKho:
    """
    Create goods receipt with inventory update.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on inventory accounting
        - Chế độ kế toán doanh nghiệp nhỏ và vừa

    Args:
        nha_cung_cap: Supplier instance
        kho: Warehouse instance
        items: List of dicts with keys:
            - hang_hoa: HangHoa instance or product code
            - so_luong: Decimal quantity
            - don_gia: Decimal unit price
        ngay: Receipt date (default today)
        nguoi_tao: Creator username

    Returns:
        Created NhapKho instance
    """
    from datetime import date as date_cls

    if ngay is None:
        ngay = date_cls.today()

    validate_ngay_chung_tu(ngay)

    if not items:
        raise ValidationError({"items": ["Phiếu nhập phải có ít nhất một mặt hàng"]})

    tong_tien = decimal.Decimal("0")

    count = NhapKho.objects.filter(ngay__year=ngay.year).count() + 1
    so_chung_tu = f'NK{ngay.strftime("%Y%m%d")}{count:04d}'

    nhap_kho = NhapKho.objects.create(
        so_chung_tu=so_chung_tu,
        ngay=ngay,
        kho=kho,
        nha_cung_cap=nha_cung_cap,
        created_by=nguoi_tao or "",
    )

    for item in items:
        hh = item["hang_hoa"]
        if isinstance(hh, str):
            hh = HangHoa.objects.get(ma_hang_hoa=hh)

        so_luong = item["so_luong"]
        don_gia = item["don_gia"]
        thanh_tien = (so_luong * don_gia).quantize(decimal.Decimal("0.01"))

        tong_tien += thanh_tien

        NhapKhoChiTiet.objects.create(
            nhap_kho=nhap_kho,
            hang_hoa=hh,
            so_luong=so_luong,
            don_gia=don_gia,
            thanh_tien=thanh_tien,
        )

    nhap_kho.tong_tien = tong_tien
    nhap_kho.save()

    logger.info(
        "Created goods receipt %s from supplier %s",
        so_chung_tu,
        nha_cung_cap.ma_ncc,
    )
    return nhap_kho


@transaction.atomic
def tao_xuat_kho(
    khach_hang: Optional[KhachHang],
    kho: Kho,
    items: list[dict],
    ngay: Optional[date] = None,
    nguoi_tao: Optional[str] = None,
) -> XuatKho:
    """
    Create goods issue with inventory reduction.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on inventory accounting
        - Chế độ kế toán doanh nghiệp nhỏ và vừa

    Args:
        khach_hang: Customer instance (optional for internal issues)
        kho: Warehouse instance
        items: List of dicts with keys:
            - hang_hoa: HangHoa instance or product code
            - so_luong: Decimal quantity
            - don_gia: Decimal unit price
        ngay: Issue date (default today)
        nguoi_tao: Creator username

    Returns:
        Created XuatKho instance
    """
    from datetime import date as date_cls

    if ngay is None:
        ngay = date_cls.today()

    validate_ngay_chung_tu(ngay)

    if not items:
        raise ValidationError({"items": ["Phiếu xuất phải có ít nhất một mặt hàng"]})

    tong_tien = decimal.Decimal("0")

    count = XuatKho.objects.filter(ngay__year=ngay.year).count() + 1
    so_chung_tu = f'XK{ngay.strftime("%Y%m%d")}{count:04d}'

    xuat_kho = XuatKho.objects.create(
        so_chung_tu=so_chung_tu,
        ngay=ngay,
        kho=kho,
        khach_hang=khach_hang,
        created_by=nguoi_tao or "",
    )

    for item in items:
        hh = item["hang_hoa"]
        if isinstance(hh, str):
            hh = HangHoa.objects.get(ma_hang_hoa=hh)

        so_luong = item["so_luong"]
        don_gia = item["don_gia"]
        thanh_tien = (so_luong * don_gia).quantize(decimal.Decimal("0.01"))

        tong_tien += thanh_tien

        XuatKhoChiTiet.objects.create(
            xuat_kho=xuat_kho,
            hang_hoa=hh,
            so_luong=so_luong,
            don_gia=don_gia,
            thanh_tien=thanh_tien,
        )

    xuat_kho.tong_tien = tong_tien
    xuat_kho.save()

    logger.info(
        "Created goods issue %s from warehouse %s",
        so_chung_tu,
        kho.ma_kho,
    )
    return xuat_kho


def doi_tu_nguyen_te(
    so_tien: decimal.Decimal,
    ty_gia: decimal.Decimal = decimal.Decimal("1"),
) -> decimal.Decimal:
    """
    Convert foreign currency amount to VND.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on foreign currency accounting
        - Ngân hàng Nhà nước exchange rate regulations

    Args:
        so_tien: Amount in foreign currency
        ty_gia: Exchange rate (default 1 for VND)

    Returns:
        Amount in VND as decimal
    """
    if so_tien < decimal.Decimal("0"):
        raise ValidationError({"so_tien": ["Số tiền không được âm"]})

    if ty_gia <= decimal.Decimal("0"):
        raise ValidationError({"ty_gia": ["Tỷ giá phải lớn hơn 0"]})

    return (so_tien * ty_gia).quantize(decimal.Decimal("0.01"))


@transaction.atomic
def tao_phieu_thu(
    khach_hang=None,
    so_tien: decimal.Decimal = decimal.Decimal("0"),
    tk_co: str = "131",
    hinh_thuc_thanh_toan: str = "tien_mat",
    ngay_chung_tu: Optional[date] = None,
    dien_giai: str = "",
    ty_gia: decimal.Decimal = decimal.Decimal("1"),
    nguoi_tao: Optional[str] = None,
    so_chung_tu: Optional[str] = None,
) -> PhieuThu:
    """
    Create receipt voucher (Phiếu thu) with auto journal entry.

    Legal basis:
        - Thông tư 99/2025/TT-BTC Appendix III - Cash receipt forms
        - Chế độ kế toán doanh nghiệp nhỏ và vừa

    Journal entry:
        Nợ 111 (Tiền mặt) / Nợ 112 (Chuyển khoản)
        Có 131 (Phải thu khách hàng) / Có 511 (Doanh thu) / ...

    Args:
        khach_hang: Customer instance (optional)
        so_tien: Receipt amount
        tk_co: Credit account code (default '131')
        hinh_thuc_thanh_toan: 'tien_mat' or 'chuyen_khoan'
        ngay_chung_tu: Voucher date (default today)
        dien_giai: Description
        ty_gia: Exchange rate (default 1 for VND)
        nguoi_tao: Creator username
        so_chung_tu: Optional voucher number (auto-generated if None)

    Returns:
        Created PhieuThu instance

    Raises:
        ValidationError: If validation fails
    """
    from datetime import date as date_cls

    if ngay_chung_tu is None:
        ngay_chung_tu = date_cls.today()

    validate_ngay_chung_tu(ngay_chung_tu)

    if so_tien <= decimal.Decimal("0"):
        raise ValidationError({"so_tien": ["Số tiền phải lớn hơn 0"]})

    tk_no_code = "111" if hinh_thuc_thanh_toan == "tien_mat" else "112"
    tk_no = TaiKhoanKeToan.objects.get(ma_tai_khoan=tk_no_code)
    tk_co_obj = TaiKhoanKeToan.objects.get(ma_tai_khoan=tk_co)

    validate_tai_khoan_no_co(tk_no_code, tk_co)

    if not so_chung_tu:
        count = (
            PhieuThu.objects.filter(ngay_chung_tu__year=ngay_chung_tu.year).count() + 1
        )
        so_chung_tu = f'PT{ngay_chung_tu.strftime("%Y%m%d")}{count:04d}'

    phieu = PhieuThu.objects.create(
        so_chung_tu=so_chung_tu,
        ngay_chung_tu=ngay_chung_tu,
        loai_chung_tu="phieu_thu",
        dien_giai=dien_giai,
        so_tien=so_tien,
        ty_gia=ty_gia,
        hinh_thuc_thanh_toan=hinh_thuc_thanh_toan,
        tk_no=tk_no,
        tk_co=tk_co_obj,
        khach_hang=khach_hang,
        created_by=nguoi_tao or "",
    )

    # Auto-create journal entry
    chi_tiet = [
        {
            "tai_khoan": tk_no_code,
            "loai_no_co": "no",
            "so_tien": phieu.so_tien_vnd,
            "ma_doi_tuong": khach_hang.ma_kh if khach_hang else "",
            "dien_giai": dien_giai or f"Thu tiền {so_chung_tu}",
        },
        {
            "tai_khoan": tk_co,
            "loai_no_co": "co",
            "so_tien": phieu.so_tien_vnd,
            "ma_doi_tuong": khach_hang.ma_kh if khach_hang else "",
            "dien_giai": dien_giai or f"Thu tiền {so_chung_tu}",
        },
    ]
    but_toan = tao_but_toan(
        ngay=ngay_chung_tu,
        dien_giai=dien_giai or f"Phiếu thu {so_chung_tu}",
        chi_tiet=chi_tiet,
        so_but_toan=f"BT-{so_chung_tu}",
    )

    logger.info(
        "Created receipt %s: Nợ %s / Có %s - %s VND",
        so_chung_tu,
        tk_no,
        tk_co,
        phieu.so_tien_vnd,
    )
    return phieu


@transaction.atomic
def tao_phieu_chi(
    nha_cung_cap=None,
    so_tien: decimal.Decimal = decimal.Decimal("0"),
    tk_no: str = "331",
    hinh_thuc_thanh_toan: str = "tien_mat",
    ngay_chung_tu: Optional[date] = None,
    dien_giai: str = "",
    ty_gia: decimal.Decimal = decimal.Decimal("1"),
    nguoi_tao: Optional[str] = None,
    so_chung_tu: Optional[str] = None,
) -> PhieuChi:
    """
    Create payment voucher (Phiếu chi) with auto journal entry.

    Legal basis:
        - Thông tư 99/2025/TT-BTC Appendix III - Cash payment forms
        - Chế độ kế toán doanh nghiệp nhỏ và vừa

    Journal entry:
        Nợ 331 (Phải trả người bán) / Nợ 642 (Chi phí QLDN) / ...
        Có 111 (Tiền mặt) / Có 112 (Chuyển khoản)

    Args:
        nha_cung_cap: Supplier instance (optional)
        so_tien: Payment amount
        tk_no: Debit account code (default '331')
        hinh_thuc_thanh_toan: 'tien_mat' or 'chuyen_khoan'
        ngay_chung_tu: Voucher date (default today)
        dien_giai: Description
        ty_gia: Exchange rate (default 1 for VND)
        nguoi_tao: Creator username
        so_chung_tu: Optional voucher number (auto-generated if None)

    Returns:
        Created PhieuChi instance

    Raises:
        ValidationError: If validation fails
    """
    from datetime import date as date_cls

    if ngay_chung_tu is None:
        ngay_chung_tu = date_cls.today()

    validate_ngay_chung_tu(ngay_chung_tu)

    if so_tien <= decimal.Decimal("0"):
        raise ValidationError({"so_tien": ["Số tiền phải lớn hơn 0"]})

    tk_co_code = "111" if hinh_thuc_thanh_toan == "tien_mat" else "112"
    tk_no_obj = TaiKhoanKeToan.objects.get(ma_tai_khoan=tk_no)
    tk_co = TaiKhoanKeToan.objects.get(ma_tai_khoan=tk_co_code)

    validate_tai_khoan_no_co(tk_no, tk_co_code)

    if not so_chung_tu:
        count = (
            PhieuChi.objects.filter(ngay_chung_tu__year=ngay_chung_tu.year).count() + 1
        )
        so_chung_tu = f'PC{ngay_chung_tu.strftime("%Y%m%d")}{count:04d}'

    phieu = PhieuChi.objects.create(
        so_chung_tu=so_chung_tu,
        ngay_chung_tu=ngay_chung_tu,
        loai_chung_tu="phieu_chi",
        dien_giai=dien_giai,
        so_tien=so_tien,
        ty_gia=ty_gia,
        hinh_thuc_thanh_toan=hinh_thuc_thanh_toan,
        tk_no=tk_no_obj,
        tk_co=tk_co,
        nha_cung_cap=nha_cung_cap,
        created_by=nguoi_tao or "",
    )

    # Auto-create journal entry
    chi_tiet = [
        {
            "tai_khoan": tk_no,
            "loai_no_co": "no",
            "so_tien": phieu.so_tien_vnd,
            "ma_doi_tuong": nha_cung_cap.ma_ncc if nha_cung_cap else "",
            "dien_giai": dien_giai or f"Chi tiền {so_chung_tu}",
        },
        {
            "tai_khoan": tk_co_code,
            "loai_no_co": "co",
            "so_tien": phieu.so_tien_vnd,
            "ma_doi_tuong": nha_cung_cap.ma_ncc if nha_cung_cap else "",
            "dien_giai": dien_giai or f"Chi tiền {so_chung_tu}",
        },
    ]
    but_toan = tao_but_toan(
        ngay=ngay_chung_tu,
        dien_giai=dien_giai or f"Phiếu chi {so_chung_tu}",
        chi_tiet=chi_tiet,
        so_but_toan=f"BT-{so_chung_tu}",
    )

    logger.info(
        "Created payment %s: Nợ %s / Có %s - %s VND",
        so_chung_tu,
        tk_no,
        tk_co,
        phieu.so_tien_vnd,
    )
    return phieu
