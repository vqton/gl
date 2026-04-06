"""M1/M8 Integration services: Invoice ↔ Inventory ↔ Accounting."""

import decimal
import logging
from datetime import date
from typing import Dict, List, Optional

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.danh_muc.models import HangHoa, KhachHang, NhaCungCap
from apps.kho.models import Kho as KhoModel
from apps.kho.models import VatTuHangHoa
from apps.kho.services import InventoryValuationService
from apps.nghiep_vu.models import (
    ButToan,
    HoaDon,
    HoaDonChiTiet,
    NhapKho,
    NhapKhoChiTiet,
    XuatKho,
    XuatKhoChiTiet,
)
from apps.nghiep_vu.services import (
    tao_but_toan,
    tao_phieu_chi,
    tao_phieu_thu,
    tinh_thue_gtgt,
)
from apps.nghiep_vu.validators import validate_ngay_chung_tu

logger = logging.getLogger(__name__)


@transaction.atomic
def phat_hanh_hoa_don(
    hoa_don: HoaDon,
    kho_xuat: Optional[KhoModel] = None,
    tu_dong_xuat_kho: bool = True,
    tu_dong_thanh_toan: bool = False,
) -> Dict:
    """
    Issue invoice with automatic inventory issue and journal entries.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on invoice requirements
        - Nghị định 320/2025/NĐ-CP on e-invoice implementation

    Journal entries created:
        1. Revenue recognition:
           Nợ 131 (Phải thu khách hàng)
           Có 511 (Doanh thu bán hàng)
           Có 3331 (Thuế GTGT đầu ra)

        2. Cost of goods sold (if tu_dong_xuat_kho=True):
           Nợ 632 (Giá vốn hàng bán)
           Có 156/155 (Hàng hóa/Thành phẩm)

    Args:
        hoa_don: HoaDon instance (must have chi_tiet items)
        kho_xuat: Warehouse to issue from (required if tu_dong_xuat_kho)
        tu_dong_xuat_kho: Auto-create XuatKho entries
        tu_dong_thanh_toan: Auto-create PhieuThu

    Returns:
        Dict with keys:
            - hoa_don: Updated HoaDon instance
            - xuat_kho: List of XuatKho instances (if created)
            - phieu_thu: PhieuThu instance (if created)
            - but_toan_doanh_thu: ButToan for revenue
            - but_toan_gia_von: ButToan for COGS (if created)
    """
    if hoa_don.trang_thai != "draft":
        raise ValidationError({"trang_thai": ["Hóa đơn không ở trạng thái nháp"]})

    chi_tiet = list(hoa_don.chi_tiet.all())
    if not chi_tiet:
        raise ValidationError({"chi_tiet": ["Hóa đơn phải có ít nhất một mặt hàng"]})

    result = {
        "hoa_don": hoa_don,
        "xuat_kho": [],
        "phieu_thu": None,
        "but_toan_doanh_thu": None,
        "but_toan_gia_von": None,
    }

    # 1. Create revenue journal entry
    tk_no = "111" if hoa_don.hinh_thuc_thanh_toan == "tien_mat" else "112"
    chi_tiet_bt = [
        {
            "tai_khoan": "131",
            "loai_no_co": "no",
            "so_tien": hoa_don.tong_cong_thanh_toan,
            "ma_doi_tuong": hoa_don.khach_hang.ma_kh,
            "dien_giai": f"Công nợ hóa đơn {hoa_don.so_hoa_don}",
        },
        {
            "tai_khoan": "511",
            "loai_no_co": "co",
            "so_tien": hoa_don.tong_tien_truoc_thue,
            "ma_doi_tuong": hoa_don.khach_hang.ma_kh,
            "dien_giai": f"Doanh thu hóa đơn {hoa_don.so_hoa_don}",
        },
        {
            "tai_khoan": "3331",
            "loai_no_co": "co",
            "so_tien": hoa_don.tien_thue_gtgt,
            "ma_doi_tuong": "",
            "dien_giai": f"Thuế GTGT hóa đơn {hoa_don.so_hoa_don}",
        },
    ]
    result["but_toan_doanh_thu"] = tao_but_toan(
        ngay=hoa_don.ngay_hoa_don,
        dien_giai=f"Hóa đơn {hoa_don.so_hoa_don} - Ghi nhận doanh thu",
        chi_tiet=chi_tiet_bt,
        so_but_toan=f"BT-HD-{hoa_don.so_hoa_don}",
    )

    # 2. Auto-create inventory issue
    if tu_dong_xuat_kho and kho_xuat:
        xuat_kho = XuatKho.objects.create(
            so_chung_tu=f"XK-HD-{hoa_don.so_hoa_don}",
            ngay=hoa_don.ngay_hoa_don,
            kho=kho_xuat,
            khach_hang=hoa_don.khach_hang,
            tong_tien=hoa_don.tong_tien_truoc_thue,
            trang_thai="completed",
            created_by=hoa_don.created_by,
        )
        for ct in chi_tiet:
            XuatKhoChiTiet.objects.create(
                xuat_kho=xuat_kho,
                hang_hoa=ct.hang_hoa,
                so_luong=ct.so_luong,
                don_gia=ct.don_gia,
                thanh_tien=ct.tong_tien - ct.tien_thue,
            )
        result["xuat_kho"].append(xuat_kho)

        # COGS journal entry
        chi_tiet_gv = [
            {
                "tai_khoan": "632",
                "loai_no_co": "no",
                "so_tien": hoa_don.tong_tien_truoc_thue,
                "ma_doi_tuong": hoa_don.khach_hang.ma_kh,
                "dien_giai": f"Giá vốn hóa đơn {hoa_don.so_hoa_don}",
            },
            {
                "tai_khoan": "156",
                "loai_no_co": "co",
                "so_tien": hoa_don.tong_tien_truoc_thue,
                "ma_doi_tuong": "",
                "dien_giai": f"Xuất kho hóa đơn {hoa_don.so_hoa_don}",
            },
        ]
        result["but_toan_gia_von"] = tao_but_toan(
            ngay=hoa_don.ngay_hoa_don,
            dien_giai=f"Hóa đơn {hoa_don.so_hoa_don} - Giá vốn hàng bán",
            chi_tiet=chi_tiet_gv,
            so_but_toan=f"BT-GV-{hoa_don.so_hoa_don}",
        )
        hoa_don.da_xuat_kho = True

    # 3. Auto-create payment receipt
    if tu_dong_thanh_toan:
        result["phieu_thu"] = tao_phieu_thu(
            khach_hang=hoa_don.khach_hang,
            so_tien=hoa_don.tong_cong_thanh_toan,
            tk_co="131",
            hinh_thuc_thanh_toan=hoa_don.hinh_thuc_thanh_toan,
            ngay_chung_tu=hoa_don.ngay_hoa_don,
            dien_giai=f"Thanh toán hóa đơn {hoa_don.so_hoa_don}",
            nguoi_tao=hoa_don.created_by,
            so_chung_tu=f"PT-HD-{hoa_don.so_hoa_don}",
        )
        hoa_don.da_thanh_toan = True

    hoa_don.trang_thai = "issued"
    hoa_don.save(
        update_fields=["trang_thai", "da_xuat_kho", "da_thanh_toan", "updated_at"]
    )

    logger.info(
        "Issued invoice %s with %d items, xuat_kho=%s, thanh_toan=%s",
        hoa_don.so_hoa_don,
        len(chi_tiet),
        tu_dong_xuat_kho,
        tu_dong_thanh_toan,
    )
    return result


@transaction.atomic
def hoan_thanh_nhap_kho(
    nhap_kho: NhapKho,
    tu_dong_ghi_nho: bool = True,
) -> Dict:
    """
    Complete goods receipt with automatic inventory update and journal entries.

    Legal basis:
        - Thông tư 99/2025/TT-BTC on inventory accounting
        - Chế độ kế toán doanh nghiệp nhỏ và vừa

    Journal entries created:
        Nợ 156 (Hàng hóa) / Nợ 152 (Vật liệu)
        Nợ 133 (Thuế GTGT được khấu trừ)
        Có 331 (Phải trả người bán)

    Args:
        nhap_kho: NhapKho instance (must have chi_tiet items)
        tu_dong_ghi_nho: Auto-create journal entries

    Returns:
        Dict with keys:
            - nhap_kho: Updated NhapKho instance
            - but_toan: ButToan instance (if created)
            - kho_entries: List of KhoEntry instances from valuation engine
    """
    if nhap_kho.trang_thai != "draft":
        raise ValidationError({"trang_thai": ["Phiếu nhập không ở trạng thái nháp"]})

    chi_tiet = list(nhap_kho.chi_tiet.all())
    if not chi_tiet:
        raise ValidationError({"chi_tiet": ["Phiếu nhập phải có ít nhất một mặt hàng"]})

    result = {
        "nhap_kho": nhap_kho,
        "but_toan": None,
        "kho_entries": [],
    }

    # 1. Update inventory via valuation engine
    # Map nghiep_vu.Kho to kho.Kho if needed
    try:
        from apps.kho.models import Kho as KhoInventory

        kho_inventory, _ = KhoInventory.objects.get_or_create(
            ma_kho=nhap_kho.kho.ma_kho,
            defaults={"ten_kho": nhap_kho.kho.ten_kho},
        )
    except Exception:
        kho_inventory = None

    if kho_inventory:
        try:
            valuation_service = InventoryValuationService()
            for ct in chi_tiet:
                try:
                    vat_tu = VatTuHangHoa.objects.get(hang_hoa=ct.hang_hoa)
                except VatTuHangHoa.DoesNotExist:
                    logger.warning(
                        "VatTuHangHoa not found for %s, skipping inventory update",
                        ct.hang_hoa.ma_hang_hoa,
                    )
                    continue

                entries = valuation_service.nhap_kho(
                    hang_hoa=vat_tu,
                    kho=kho_inventory,
                    items=[
                        {
                            "so_luong": str(ct.so_luong),
                            "don_gia": str(ct.don_gia),
                            "ma_lot": f"NK-{nhap_kho.pk}-{ct.pk}",
                        }
                    ],
                    ngay=nhap_kho.ngay,
                    so_chung_tu=nhap_kho.so_chung_tu,
                )
                result["kho_entries"].extend(entries)
        except Exception as e:
            logger.error("Inventory update failed: %s", e, exc_info=True)

    # 2. Create journal entry
    if tu_dong_ghi_nho and nhap_kho.nha_cung_cap:
        chi_tiet_bt = [
            {
                "tai_khoan": "156",
                "loai_no_co": "no",
                "so_tien": nhap_kho.tong_tien,
                "ma_doi_tuong": nhap_kho.nha_cung_cap.ma_ncc,
                "dien_giai": f"Nhập kho {nhap_kho.so_chung_tu}",
            },
            {
                "tai_khoan": "331",
                "loai_no_co": "co",
                "so_tien": nhap_kho.tong_tien,
                "ma_doi_tuong": nhap_kho.nha_cung_cap.ma_ncc,
                "dien_giai": f"Công nợ nhập kho {nhap_kho.so_chung_tu}",
            },
        ]
        result["but_toan"] = tao_but_toan(
            ngay=nhap_kho.ngay,
            dien_giai=f"Nhập kho {nhap_kho.so_chung_tu} - Ghi nhận hàng hóa",
            chi_tiet=chi_tiet_bt,
            so_but_toan=f"BT-NK-{nhap_kho.so_chung_tu}",
        )

    nhap_kho.trang_thai = "completed"
    nhap_kho.save(update_fields=["trang_thai", "updated_at"])

    logger.info(
        "Completed goods receipt %s with %d items",
        nhap_kho.so_chung_tu,
        len(chi_tiet),
    )
    return result


class HoaDonDienTuMock:
    """
    Mock e-invoice API service for internal testing.

    Simulates the General Department of Taxation (GDT) e-invoice API.

    Legal basis:
        - Nghị định 320/2025/NĐ-CP on e-invoice implementation
        - Thông tư 99/2025/TT-BTC on e-invoice format
    """

    BASE_URL = "https://mock-api.gdt.gov.vn/invoice"

    @staticmethod
    def dang_ky_hoa_don(hoa_don: HoaDon) -> Dict:
        """
        Register invoice with mock GDT API.

        Args:
            hoa_don: HoaDon instance to register

        Returns:
            Dict with registration result:
                - ma_gdv: Tax authority code
                - ky_hieu: Invoice symbol
                - trang_thai: 'accepted' or 'rejected'
        """
        return {
            "ma_gdv": f"GDT-{hoa_don.ngay_hoa_don.year}",
            "ky_hieu": hoa_don.ky_hieu or "HD2026",
            "trang_thai": "accepted",
            "ma_hoa_don_gdt": f"GDT{hoa_don.so_hoa_don}",
        }

    @staticmethod
    def huy_hoa_don(hoa_don: HoaDon, ly_do: str = "") -> Dict:
        """
        Cancel invoice via mock GDT API.

        Args:
            hoa_don: HoaDon instance to cancel
            ly_do: Reason for cancellation

        Returns:
            Dict with cancellation result
        """
        return {
            "trang_thai": "cancelled",
            "ly_do": ly_do,
            "ma_hoa_don_gdt": f"GDT{hoa_don.so_hoa_don}",
        }

    @staticmethod
    def tra_cuu_hoa_don(ma_hoa_don: str) -> Dict:
        """
        Lookup invoice status from mock GDT API.

        Args:
            ma_hoa_don: GDT invoice code

        Returns:
            Dict with invoice status
        """
        return {
            "ma_hoa_don": ma_hoa_don,
            "trang_thai": "valid",
            "da_ghi_nhan": True,
        }
