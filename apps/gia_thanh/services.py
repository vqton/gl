"""Giá Thành (Product Costing) services."""

import logging
from datetime import date
from decimal import Decimal
from typing import Dict, List, Optional

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Sum

from apps.nghiep_vu.models import ButToan, ButToanChiTiet

from .models import (
    BangPhanBoChiPhi,
    BangTinhGiaThanh,
    ChiTietPhanBoChiPhi,
    DoiTuongTapHopChiPhi,
    KhoanMucChiPhi,
    PhieuTapHopChiPhi,
)

logger = logging.getLogger(__name__)


class TinhGiaThanhService:
    """
    Service for product cost calculation.

    Legal basis:
        - Thông tư 99/2025/TT-BTC, Phụ lục III - Cost accounting
        - VAS 02 - Hàng tồn kho

    Cost flow:
        1. Tập hợp chi phí → TK 154
        2. Cuối kỳ: Kết chuyển TK 154 → TK 631
        3. Tính giá thành sản phẩm hoàn thành
        4. Kết chuyển TK 631 → TK 155 (thành phẩm)
    """

    def __init__(self, thang: int, nam: int):
        self.thang = thang
        self.nam = nam

    def get_tong_chi_phi_theo_doi_tuong(
        self, doi_tuong: DoiTuongTapHopChiPhi
    ) -> Decimal:
        """
        Get total cost for a cost object in the period.

        Sums all posted PhieuTapHopChiPhi for the given object
        within the service's month/year.

        Args:
            doi_tuong: Cost collection object

        Returns:
            Total cost as Decimal
        """
        from datetime import date as date_cls

        if self.thang == 12:
            ngay_dau = date_cls(self.nam, self.thang, 1)
            ngay_cuoi = date_cls(self.nam + 1, 1, 1)
        else:
            ngay_dau = date_cls(self.nam, self.thang, 1)
            ngay_cuoi = date_cls(self.nam, self.thang + 1, 1)

        tong = PhieuTapHopChiPhi.objects.filter(
            doi_tuong=doi_tuong,
            ngay_chung_tu__gte=ngay_dau,
            ngay_chung_tu__lt=ngay_cuoi,
            trang_thai="posted",
        ).aggregate(total=Sum("so_tien"))["total"]

        return tong or Decimal("0")

    def get_cp_theo_khoan_muc(
        self, doi_tuong: DoiTuongTapHopChiPhi
    ) -> Dict[str, Decimal]:
        """
        Get cost breakdown by cost item for a cost object.

        Args:
            doi_tuong: Cost collection object

        Returns:
            Dict mapping cost item type to total amount
        """
        from datetime import date as date_cls

        if self.thang == 12:
            ngay_dau = date_cls(self.nam, self.thang, 1)
            ngay_cuoi = date_cls(self.nam + 1, 1, 1)
        else:
            ngay_dau = date_cls(self.nam, self.thang, 1)
            ngay_cuoi = date_cls(self.nam, self.thang + 1, 1)

        phieu_list = PhieuTapHopChiPhi.objects.filter(
            doi_tuong=doi_tuong,
            ngay_chung_tu__gte=ngay_dau,
            ngay_chung_tu__lt=ngay_cuoi,
            trang_thai="posted",
        ).select_related("khoan_muc")

        result = {
            "nguyen_vat_lieu": Decimal("0"),
            "nhan_cong": Decimal("0"),
            "san_xuat_chung": Decimal("0"),
        }
        for p in phieu_list:
            loai = p.khoan_muc.loai
            if loai in result:
                result[loai] += p.so_tien

        return result

    @transaction.atomic
    def tao_bang_tinh_gia_thanh(
        self,
        doi_tuong: DoiTuongTapHopChiPhi,
        cp_dở_dang_dau_ky: Decimal,
        cp_dở_dang_cuoi_ky: Decimal,
        so_luong_sp: Decimal,
        dien_giai: str = "",
    ) -> BangTinhGiaThanh:
        """
        Create cost calculation table for a cost object.

        Auto-calculates:
            - cp_phat_sinh: from posted PhieuTapHopChiPhi
            - gia_thanh_sp_hoan_thanh: = DD đầu kỳ + PS - DD cuối kỳ
            - gia_thanh_don_vi: = GT hoàn thành / SL

        Args:
            doi_tuong: Cost collection object
            cp_dở_dang_dau_ky: Opening WIP cost
            cp_dở_dang_cuoi_ky: Closing WIP cost
            so_luong_sp: Quantity of finished products
            dien_giai: Description

        Returns:
            Created BangTinhGiaThanh instance
        """
        cp_phat_sinh = self.get_tong_chi_phi_theo_doi_tuong(doi_tuong)

        bang = BangTinhGiaThanh(
            thang=self.thang,
            nam=self.nam,
            doi_tuong=doi_tuong,
            cp_dở_dang_dau_ky=cp_dở_dang_dau_ky,
            cp_phat_sinh=cp_phat_sinh,
            cp_dở_dang_cuoi_ky=cp_dở_dang_cuoi_ky,
            so_luong_sp=so_luong_sp,
            dien_giai=dien_giai,
        )
        bang.full_clean()
        bang.save()

        logger.info(
            "Created cost calc T%d/%d for %s: GT=%s, ĐV=%s",
            self.thang,
            self.nam,
            doi_tuong,
            bang.gia_thanh_sp_hoan_thanh,
            bang.gia_thanh_don_vi,
        )
        return bang

    @transaction.atomic
    def phan_bo_chi_phi(
        self,
        bang_phan_bo: BangPhanBoChiPhi,
        chi_tiet_data: List[Dict],
    ) -> BangPhanBoChiPhi:
        """
        Allocate costs to cost objects.

        Args:
            bang_phan_bo: Allocation table
            chi_tiet_data: List of dicts with keys:
                - doi_tuong: DoiTuongTapHopChiPhi
                - he_so: allocation coefficient
                - dien_giai: description (optional)

        Returns:
            Updated BangPhanBoChiPhi

        Raises:
            ValidationError: If total allocated != total cost
        """
        tong_chi_phi = bang_phan_bo.tong_chi_phi
        tong_he_so = sum(item["he_so"] for item in chi_tiet_data)

        if tong_he_so == Decimal("0"):
            raise ValidationError(
                {"chi_tiet": ["Tổng hệ số phải lớn hơn 0"]}
            )

        for item in chi_tiet_data:
            muc_phan_bo = (
                tong_chi_phi * item["he_so"] / tong_he_so
            ).quantize(Decimal("0.01"))

            ChiTietPhanBoChiPhi.objects.create(
                bang_phan_bo=bang_phan_bo,
                doi_tuong=item["doi_tuong"],
                he_so=item["he_so"],
                muc_phan_bo=muc_phan_bo,
                dien_giai=item.get("dien_giai", ""),
            )

        tong_da_phan_bo = bang_phan_bo.tong_da_phan_bo()
        chen_lech = abs(tong_da_phan_bo - tong_chi_phi)

        if chen_lech > Decimal("0.01"):
            diff = tong_chi_phi - tong_da_phan_bo
            last_ct = ChiTietPhanBoChiPhi.objects.filter(
                bang_phan_bo=bang_phan_bo
            ).order_by("-pk").first()
            if last_ct:
                last_ct.muc_phan_bo += diff
                last_ct.save(update_fields=["muc_phan_bo"])
        elif chen_lech > Decimal("0"):
            diff = tong_chi_phi - tong_da_phan_bo
            last_ct = ChiTietPhanBoChiPhi.objects.filter(
                bang_phan_bo=bang_phan_bo
            ).order_by("-pk").first()
            if last_ct:
                last_ct.muc_phan_bo += diff
                last_ct.save(update_fields=["muc_phan_bo"])

        logger.info(
            "Allocated %s across %d objects",
            tong_chi_phi,
            len(chi_tiet_data),
        )
        return bang_phan_bo

    @transaction.atomic
    def dang_bang_tinh_gia_thanh(
        self, bang: BangTinhGiaThanh
    ) -> ButToan:
        """
        Post cost calculation and create journal entry.

        Journal entry:
            Nợ 155 (Thành phẩm) / Có 631 (Giá thành SX)

        Args:
            bang: BangTinhGiaThanh to post

        Returns:
            Created ButToan instance
        """
        if bang.gia_thanh_sp_hoan_thanh <= Decimal("0"):
            raise ValidationError(
                {"gia_thanh": ["Giá thành phải lớn hơn 0 để ghi sổ"]}
            )

        bang.trang_thai = "posted"
        bang.save(update_fields=["trang_thai", "updated_at"])

        from apps.danh_muc.models import TaiKhoanKeToan
        from apps.nghiep_vu.services import tao_but_toan

        tk155 = TaiKhoanKeToan.objects.filter(ma_tai_khoan="155").first()
        tk631 = TaiKhoanKeToan.objects.filter(ma_tai_khoan="631").first()

        if not tk155 or not tk631:
            raise ValidationError(
                {"tai_khoan": ["Cần có TK 155 và 631 để kết chuyển"]}
            )

        chi_tiet = [
            {
                "tai_khoan": tk155,
                "loai_no_co": "no",
                "so_tien": bang.gia_thanh_sp_hoan_thanh,
                "ma_doi_tuong": bang.doi_tuong.ma_doi_tuong,
                "dien_giai": f"Kết chuyển giá thành T{bang.thang}/{bang.nam}",
            },
            {
                "tai_khoan": tk631,
                "loai_no_co": "co",
                "so_tien": bang.gia_thanh_sp_hoan_thanh,
                "ma_doi_tuong": bang.doi_tuong.ma_doi_tuong,
                "dien_giai": f"Kết chuyển giá thành T{bang.thang}/{bang.nam}",
            },
        ]

        but_toan = tao_but_toan(
            ngay=date(bang.nam, bang.thang, 28),
            dien_giai=f"Kết chuyển giá thành T{bang.thang}/{bang.nam} - {bang.doi_tuong}",
            chi_tiet=chi_tiet,
            so_but_toan=f"GT-{bang.nam}{bang.thang:02d}-{bang.doi_tuong.ma_doi_tuong}",
        )

        logger.info(
            "Posted cost calc %s: Nợ 155 / Có 631 = %s",
            bang,
            bang.gia_thanh_sp_hoan_thanh,
        )
        return but_toan


def tinh_gia_thanh_don_vi(
    cp_dau_ky: Decimal,
    cp_phat_sinh: Decimal,
    cp_cuoi_ky: Decimal,
    so_luong: Decimal,
) -> Decimal:
    """
    Calculate unit cost.

    Formula: (CP DD đầu kỳ + CP PS - CP DD cuối kỳ) / SL

    Args:
        cp_dau_ky: Opening WIP cost
        cp_phat_sinh: Cost incurred in period
        cp_cuoi_ky: Closing WIP cost
        so_luong: Quantity of finished products

    Returns:
        Unit cost as Decimal
    """
    gia_thanh = cp_dau_ky + cp_phat_sinh - cp_cuoi_ky
    if gia_thanh < Decimal("0"):
        gia_thanh = Decimal("0")
    if so_luong <= Decimal("0"):
        return Decimal("0")
    return (gia_thanh / so_luong).quantize(Decimal("0.0001"))
