"""Financial report services - TT 99/2025/TT-BTC compliant.

Reports implemented:
- B01-DN: Báo cáo tình hình tài chính (Balance Sheet)
- B02-DN: Báo cáo kết quả hoạt động kinh doanh (P&L)
- B03-DN: Báo cáo lưu chuyển tiền tệ (Cash Flow Statement)
- B09-DN: Thuyết minh Báo cáo tài chính (Notes to Financial Statements)
- BCĐSPS: Bảng cân đối số phát sinh (Trial Balance)
"""

import logging
from datetime import date
from decimal import Decimal
from typing import Dict, List

from django.db.models import Sum

from apps.danh_muc.models import TaiKhoanKeToan
from apps.nghiep_vu.models import ButToan, ButToanChiTiet

logger = logging.getLogger(__name__)


def _get_period_totals(ma_tai_khoan: str, tu_ngay: date, den_ngay: date) -> Dict[str, Decimal]:
    """Get total debit/credit for an account in a period (posted entries only)."""
    chi_tiet = ButToanChiTiet.objects.filter(
        but_toan__ngay_hach_toan__gte=tu_ngay,
        but_toan__ngay_hach_toan__lte=den_ngay,
        but_toan__trang_thai="posted",
        tai_khoan__ma_tai_khoan=ma_tai_khoan,
    )
    no_tong = chi_tiet.filter(loai_no_co="no").aggregate(total=Sum("so_tien"))["total"] or Decimal("0")
    co_tong = chi_tiet.filter(loai_no_co="co").aggregate(total=Sum("so_tien"))["total"] or Decimal("0")
    return {"no_tong": no_tong, "co_tong": co_tong, "so_du": no_tong - co_tong}


def get_so_du_tai_khoan(
    ma_tai_khoan: str,
    ngay_bat_dau: date,
    ngay_ket_thuc: date,
) -> Dict[str, Decimal]:
    """Get account balance for a period (posted entries only)."""
    return _get_period_totals(ma_tai_khoan, ngay_bat_dau, ngay_ket_thuc)


def _line(ma_so: str, ten_chi_tieu: str, so_tien) -> Dict:
    """Create a report line item."""
    return {
        "ma_so": ma_so,
        "ten_chi_tieu": ten_chi_tieu,
        "so_tien": Decimal(str(so_tien)),
    }


def lap_bang_can_doi_ke_toan(ngay_ket_thuc: date) -> Dict:
    """
    Generate Balance Sheet (Báo cáo tình hình tài chính - Mẫu B01-DN).

    Legal basis: Thông tư 99/2025/TT-BTC, Phụ lục I - Mẫu B01-DN
    """
    d = ngay_ket_thuc
    tu = date(d.year, 1, 1)

    # === TÀI SẢN ===
    # A. Tài sản ngắn hạn
    tien = _get_period_totals("111", tu, d)["so_du"] + _get_period_totals("112", tu, d)["so_du"] + _get_period_totals("113", tu, d)["so_du"]
    dau_tu_nh = sum(_get_period_totals(tk, tu, d)["so_du"] for tk in ["121", "128"])
    phai_thu_nh = sum(_get_period_totals(tk, tu, d)["so_du"] for tk in ["131", "133", "136", "138", "141"])
    hang_ton_kho = sum(_get_period_totals(tk, tu, d)["so_du"] for tk in ["151", "152", "153", "154", "155", "157", "158"])
    tai_san_nh_khac = sum(_get_period_totals(tk, tu, d)["so_du"] for tk in ["171", "242", "244"])

    tong_tai_san_ngan_han = tien + dau_tu_nh + phai_thu_nh + hang_ton_kho + tai_san_nh_khac

    # B. Tài sản dài hạn
    tscd = _get_period_totals("211", tu, d)["so_du"] + _get_period_totals("212", tu, d)["so_du"] + _get_period_totals("213", tu, d)["so_du"]
    hao_mon = _get_period_totals("214", tu, d)["so_du"]
    bat_dong_san = sum(_get_period_totals(tk, tu, d)["so_du"] for tk in ["215", "217"])
    dau_tu_dh = sum(_get_period_totals(tk, tu, d)["so_du"] for tk in ["221", "222", "228", "229"])
    phai_thu_dh = sum(_get_period_totals(tk, tu, d)["so_du"] for tk in ["136", "138", "243"])
    tai_san_dh_khac = sum(_get_period_totals(tk, tu, d)["so_du"] for tk in ["241", "242"])

    tong_tai_san_dai_han = (tscd + hao_mon) + bat_dong_san + dau_tu_dh + phai_thu_dh + tai_san_dh_khac

    tong_tai_san = tong_tai_san_ngan_han + tong_tai_san_dai_han

    # === NGUỒN VỐN ===
    # C. Nợ ngắn hạn (liability accounts: credit balance = negative so_du)
    phai_tra_nb = abs(_get_period_totals("331", tu, d)["so_du"])
    nguoi_mua_tra_truoc = Decimal("0")
    thue_phai_nop = abs(sum(_get_period_totals(tk, tu, d)["so_du"] for tk in ["332", "333"]))
    phai_tra_nld = abs(_get_period_totals("334", tu, d)["so_du"])
    chi_phi_phai_tra = abs(sum(_get_period_totals(tk, tu, d)["so_du"] for tk in ["335", "352"]))
    phai_tra_noi_bo = abs(_get_period_totals("336", tu, d)["so_du"])
    phai_tra_nh_khac = abs(sum(_get_period_totals(tk, tu, d)["so_du"] for tk in ["338", "341", "343", "344", "347", "353", "356"]))

    tong_no_ngan_han = phai_tra_nb + nguoi_mua_tra_truoc + thue_phai_nop + phai_tra_nld + chi_phi_phai_tra + phai_tra_noi_bo + phai_tra_nh_khac

    # D. Nợ dài hạn
    vay_dh = abs(_get_period_totals("341", tu, d)["so_du"])
    trai_phieu = abs(_get_period_totals("343", tu, d)["so_du"])
    no_dh_khac = abs(sum(_get_period_totals(tk, tu, d)["so_du"] for tk in ["347", "352"]))

    tong_no_dai_han = vay_dh + trai_phieu + no_dh_khac

    # E. Vốn chủ sở hữu (equity accounts: credit balance = negative so_du)
    von_dau_tu = abs(_get_period_totals("411", tu, d)["so_du"])
    thang_du_von = abs(_get_period_totals("412", tu, d)["so_du"])
    chen_lech_danh_gia = abs(_get_period_totals("413", tu, d)["so_du"])
    quy_dau_tu = abs(_get_period_totals("414", tu, d)["so_du"])
    quy_khac = abs(_get_period_totals("418", tu, d)["so_du"])
    co_phieu_quy = abs(_get_period_totals("419", tu, d)["so_du"])
    loi_nhuan_chua_pp = abs(_get_period_totals("421", tu, d)["so_du"])

    tong_von_chu_so_huu = von_dau_tu + thang_du_von + chen_lech_danh_gia + quy_dau_tu + quy_khac + co_phieu_quy + loi_nhuan_chua_pp

    tong_nguon_von = tong_no_ngan_han + tong_no_dai_han + tong_von_chu_so_huu

    return {
        "ngay_bao_cao": ngay_ket_thuc,
        "tai_san": {
            "A": {
                "ten": "TÀI SẢN NGẮN HẠN",
                "chi_tiet": {
                    "110": _line("110", "Tiền và các khoản tương đương tiền", tien),
                    "120": _line("120", "Đầu tư tài chính ngắn hạn", dau_tu_nh),
                    "130": _line("130", "Các khoản phải thu ngắn hạn", phai_thu_nh),
                    "140": _line("140", "Hàng tồn kho", hang_ton_kho),
                    "150": _line("150", "Tài sản ngắn hạn khác", tai_san_nh_khac),
                },
                "tong_cong": tong_tai_san_ngan_han,
            },
            "B": {
                "ten": "TÀI SẢN DÀI HẠN",
                "chi_tiet": {
                    "210": _line("210", "Tài sản cố định", tscd + hao_mon),
                    "220": _line("220", "Bất động sản đầu tư", bat_dong_san),
                    "230": _line("230", "Đầu tư tài chính dài hạn", dau_tu_dh),
                    "240": _line("240", "Các khoản phải thu dài hạn", phai_thu_dh),
                    "250": _line("250", "Tài sản dài hạn khác", tai_san_dh_khac),
                },
                "tong_cong": tong_tai_san_dai_han,
            },
        },
        "nguon_von": {
            "C": {
                "ten": "NỢ NGẮN HẠN",
                "chi_tiet": {
                    "310": _line("310", "Phải trả người bán ngắn hạn", phai_tra_nb),
                    "320": _line("320", "Người mua trả tiền trước ngắn hạn", nguoi_mua_tra_truoc),
                    "330": _line("330", "Thuế và các khoản phải nộp Nhà nước", thue_phai_nop),
                    "340": _line("340", "Phải trả người lao động", phai_tra_nld),
                    "350": _line("350", "Chi phí phải trả ngắn hạn", chi_phi_phai_tra),
                    "360": _line("360", "Phải trả nội bộ ngắn hạn", phai_tra_noi_bo),
                    "370": _line("370", "Phải trả, phải nộp ngắn hạn khác", phai_tra_nh_khac),
                },
                "tong_cong": tong_no_ngan_han,
            },
            "D": {
                "ten": "NỢ DÀI HẠN",
                "chi_tiet": {
                    "410": _line("410", "Vay và nợ thuê tài chính dài hạn", vay_dh),
                    "420": _line("420", "Trái phiếu phát hành", trai_phieu),
                    "430": _line("430", "Nợ dài hạn khác", no_dh_khac),
                },
                "tong_cong": tong_no_dai_han,
            },
            "E": {
                "ten": "VỐN CHỦ SỞ HỮU",
                "chi_tiet": {
                    "410": _line("410", "Vốn chủ sở hữu", tong_von_chu_so_huu),
                    "411": _line("411", "Vốn đầu tư của chủ sở hữu", von_dau_tu),
                    "412": _line("412", "Thặng dư vốn cổ phần", thang_du_von),
                    "413": _line("413", "Lợi nhuận sau thuế chưa phân phối", loi_nhuan_chua_pp),
                },
                "tong_cong": tong_von_chu_so_huu,
            },
        },
        "can_doi": tong_tai_san == tong_nguon_von,
        "tong_tai_san": tong_tai_san,
        "tong_nguon_von": tong_nguon_von,
    }


def lap_bao_cao_kq_kinh_doanh(tu_ngay: date, den_ngay: date) -> Dict:
    """
    Generate P&L Report (Báo cáo kết quả hoạt động kinh doanh - Mẫu B02-DN).

    Legal basis: Thông tư 99/2025/TT-BTC, Phụ lục I - Mẫu B02-DN
    """
    dt_511 = _get_period_totals("511", tu_ngay, den_ngay)["co_tong"]
    giam_tru_521 = _get_period_totals("521", tu_ngay, den_ngay)["no_tong"]
    dt_thuan = dt_511 - giam_tru_521

    gia_von = _get_period_totals("632", tu_ngay, den_ngay)["no_tong"]
    loi_nhuan_gop = dt_thuan - gia_von

    dt_tc = _get_period_totals("515", tu_ngay, den_ngay)["co_tong"]
    cp_tc = _get_period_totals("635", tu_ngay, den_ngay)["no_tong"]
    cp_bh = _get_period_totals("641", tu_ngay, den_ngay)["no_tong"]
    cp_ql = _get_period_totals("642", tu_ngay, den_ngay)["no_tong"]

    loi_nhuan_thuan = loi_nhuan_gop + dt_tc - cp_tc - cp_bh - cp_ql

    tn_khac = _get_period_totals("711", tu_ngay, den_ngay)["co_tong"]
    cp_khac = _get_period_totals("811", tu_ngay, den_ngay)["no_tong"]
    loi_nhuan_khac = tn_khac - cp_khac

    cp_thue_hien_hanh = _get_period_totals("821", tu_ngay, den_ngay)["no_tong"]
    loi_nhuan_rong = loi_nhuan_thuan + loi_nhuan_khac - cp_thue_hien_hanh

    return {
        "tu_ngay": tu_ngay,
        "den_ngay": den_ngay,
        "chi_tiet": {
            "01": _line("01", "Doanh thu bán hàng và cung cấp dịch vụ", dt_511),
            "02": _line("02", "Các khoản giảm trừ doanh thu", giam_tru_521),
            "10": _line("10", "Doanh thu thuần về bán hàng và cung cấp dịch vụ", dt_thuan),
            "11": _line("11", "Giá vốn hàng bán", gia_von),
            "20": _line("20", "Lợi nhuận gộp về bán hàng và cung cấp dịch vụ", loi_nhuan_gop),
            "30": _line("30", "Doanh thu hoạt động tài chính", dt_tc),
            "31": _line("31", "Chi phí tài chính", cp_tc),
            "40": _line("40", "Chi phí bán hàng", cp_bh),
            "41": _line("41", "Chi phí quản lý doanh nghiệp", cp_ql),
            "50": _line("50", "Lợi nhuận thuần từ hoạt động kinh doanh", loi_nhuan_thuan),
            "51": _line("51", "Thu nhập khác", tn_khac),
            "52": _line("52", "Chi phí khác", cp_khac),
            "60": _line("60", "Lợi nhuận khác", loi_nhuan_khac),
            "70": _line("70", "Chi phí thuế TNDN hiện hành", cp_thue_hien_hanh),
            "80": _line("80", "LỢI NHUẬN RÒNG", loi_nhuan_rong),
        },
    }


def lap_bang_can_doi_so_phat_sinh(tu_ngay: date, den_ngay: date) -> Dict:
    """
    Generate Trial Balance (Bảng cân đối số phát sinh).

    Shows all accounts with opening balance, period activity, and closing balance.
    """
    all_accounts = TaiKhoanKeToan.objects.filter(is_active=True).order_by("ma_tai_khoan")
    accounts = []
    tong_so_du_dau_no = Decimal("0")
    tong_so_du_dau_co = Decimal("0")
    tong_phat_sinh_no = Decimal("0")
    tong_phat_sinh_co = Decimal("0")
    tong_so_du_cuoi_no = Decimal("0")
    tong_so_du_cuoi_co = Decimal("0")

    for acc in all_accounts:
        ps = _get_period_totals(acc.ma_tai_khoan, tu_ngay, den_ngay)
        so_du_dau_no = Decimal("0")
        so_du_dau_co = Decimal("0")
        so_du_cuoi_no = Decimal("0")
        so_du_cuoi_co = Decimal("0")

        if ps["so_du"] >= 0:
            so_du_cuoi_no = ps["so_du"]
        else:
            so_du_cuoi_co = abs(ps["so_du"])

        has_activity = ps["no_tong"] > 0 or ps["co_tong"] > 0 or so_du_cuoi_no > 0 or so_du_cuoi_co > 0
        if has_activity:
            accounts.append({
                "ma_tai_khoan": acc.ma_tai_khoan,
                "ten_tai_khoan": acc.ten_tai_khoan,
                "so_du_dau_no": so_du_dau_no,
                "so_du_dau_co": so_du_dau_co,
                "phat_sinh_no": ps["no_tong"],
                "phat_sinh_co": ps["co_tong"],
                "so_du_cuoi_no": so_du_cuoi_no,
                "so_du_cuoi_co": so_du_cuoi_co,
            })
            tong_so_du_dau_no += so_du_dau_no
            tong_so_du_dau_co += so_du_dau_co
            tong_phat_sinh_no += ps["no_tong"]
            tong_phat_sinh_co += ps["co_tong"]
            tong_so_du_cuoi_no += so_du_cuoi_no
            tong_so_du_cuoi_co += so_du_cuoi_co

    return {
        "tu_ngay": tu_ngay,
        "den_ngay": den_ngay,
        "accounts": accounts,
        "tong_so_du_dau_no": tong_so_du_dau_no,
        "tong_so_du_dau_co": tong_so_du_dau_co,
        "tong_phat_sinh_no": tong_phat_sinh_no,
        "tong_phat_sinh_co": tong_phat_sinh_co,
        "tong_so_du_cuoi_no": tong_so_du_cuoi_no,
        "tong_so_du_cuoi_co": tong_so_du_cuoi_co,
    }


def lap_bao_cao_luu_chuyen_tien_te(tu_ngay: date, den_ngay: date) -> Dict:
    """
    Generate Cash Flow Statement (Báo cáo lưu chuyển tiền tệ - Mẫu B03-DN).

    Legal basis: Thông tư 99/2025/TT-BTC, Phụ lục I - Mẫu B03-DN
    Uses direct method for operating activities based on cash account movements.
    """
    tk_111 = _get_period_totals("111", tu_ngay, den_ngay)
    tk_112 = _get_period_totals("112", tu_ngay, den_ngay)
    tk_113 = _get_period_totals("113", tu_ngay, den_ngay)

    tong_tien_dau_ky = Decimal("0")
    tong_tien_cuoi_ky = tk_111["so_du"] + tk_112["so_du"] + tk_113["so_du"]

    # Cash inflows (111/112/113 debit side = cash received)
    tong_thu_tien = tk_111["no_tong"] + tk_112["no_tong"] + tk_113["no_tong"]
    # Cash outflows (111/112/113 credit side = cash paid)
    tong_chi_tien = tk_111["co_tong"] + tk_112["co_tong"] + tk_113["co_tong"]

    # I. Lưu chuyển tiền từ hoạt động kinh doanh
    tien_thu_khach_hang = _get_period_totals("131", tu_ngay, den_ngay)["co_tong"]
    tien_chi_tra_ncc = _get_period_totals("331", tu_ngay, den_ngay)["no_tong"]
    tien_chi_tra_nld = _get_period_totals("334", tu_ngay, den_ngay)["no_tong"]
    thue_tndn_da_nop = _get_period_totals("333", tu_ngay, den_ngay)["no_tong"]
    thue_gtgt_da_nop = _get_period_totals("332", tu_ngay, den_ngay)["no_tong"]
    lai_vay_da_nhan = _get_period_totals("515", tu_ngay, den_ngay)["co_tong"]
    lai_vay_da_tra = _get_period_totals("635", tu_ngay, den_ngay)["no_tong"]
    thu_khac_tu_hdkd = _get_period_totals("711", tu_ngay, den_ngay)["co_tong"]
    chi_khac_tu_hdkd = _get_period_totals("811", tu_ngay, den_ngay)["no_tong"]

    tong_thu_hdkd = tien_thu_khach_hang + lai_vay_da_nhan + thu_khac_tu_hdkd
    tong_chi_hdkd = tien_chi_tra_ncc + tien_chi_tra_nld + thue_tndn_da_nop + thue_gtgt_da_nop + lai_vay_da_tra + chi_khac_tu_hdkd
    luu_chuyen_thuan_hdkd = tong_thu_hdkd - tong_chi_hdkd

    # If no non-cash entries, use direct cash movements
    if tong_thu_hdkd == 0 and tong_chi_hdkd == 0:
        tong_thu_hdkd = tong_thu_tien
        tong_chi_hdkd = tong_chi_tien
        luu_chuyen_thuan_hdkd = tong_thu_tien - tong_chi_tien

    # II. Lưu chuyển tiền từ hoạt động đầu tư
    tien_mua_tscd = _get_period_totals("211", tu_ngay, den_ngay)["no_tong"]
    tien_thanh_ly_tscd = _get_period_totals("211", tu_ngay, den_ngay)["co_tong"]
    tien_cho_vay = Decimal("0")
    tien_thu_hoi_cho_vay = Decimal("0")
    tien_dau_tu_vao_don_vi_khac = sum(_get_period_totals(tk, tu_ngay, den_ngay)["no_tong"] for tk in ["221", "222", "228"])
    tien_thu_hoi_dau_tu = sum(_get_period_totals(tk, tu_ngay, den_ngay)["co_tong"] for tk in ["221", "222", "228"])

    tong_thu_hddt = tien_thanh_ly_tscd + tien_thu_hoi_cho_vay + tien_thu_hoi_dau_tu
    tong_chi_hddt = tien_mua_tscd + tien_cho_vay + tien_dau_tu_vao_don_vi_khac
    luu_chuyen_thuan_hddt = tong_thu_hddt - tong_chi_hddt

    # III. Lưu chuyển tiền từ hoạt động tài chính
    tien_vay_duoc_nhan = _get_period_totals("341", tu_ngay, den_ngay)["co_tong"]
    tien_tra_goc_vay = _get_period_totals("341", tu_ngay, den_ngay)["no_tong"]
    tien_nop_von_cho_chu_sh = _get_period_totals("411", tu_ngay, den_ngay)["no_tong"]
    tien_nhan_von_gop = _get_period_totals("411", tu_ngay, den_ngay)["co_tong"]
    co_tuc_da_tra = Decimal("0")

    tong_thu_hdtc = tien_vay_duoc_nhan + tien_nhan_von_gop
    tong_chi_hdtc = tien_tra_goc_vay + tien_nop_von_cho_chu_sh + co_tuc_da_tra
    luu_chuyen_thuan_hdtc = tong_thu_hdtc - tong_chi_hdtc

    # IV. Tổng lưu chuyển tiền thuần
    tong_luu_chuyen = luu_chuyen_thuan_hdkd + luu_chuyen_thuan_hddt + luu_chuyen_thuan_hdtc

    return {
        "tu_ngay": tu_ngay,
        "den_ngay": den_ngay,
        "I": {
            "ten": "Lưu chuyển tiền từ hoạt động kinh doanh",
            "chi_tiet": {
                "01": _line("01", "Tiền thu từ bán hàng, cung cấp dịch vụ", tien_thu_khach_hang if tien_thu_khach_hang > 0 else tong_thu_tien),
                "02": _line("02", "Tiền chi trả cho người cung cấp hàng hóa, dịch vụ", tien_chi_tra_ncc),
                "03": _line("03", "Tiền chi trả cho người lao động", tien_chi_tra_nld),
                "04": _line("04", "Tiền lãi vay đã nhận", lai_vay_da_nhan),
                "05": _line("05", "Thuế TNDN đã nộp", thue_tndn_da_nop),
                "06": _line("06", "Thuế GTGT đã nộp", thue_gtgt_da_nop),
                "07": _line("07", "Chi phí lãi vay đã trả", lai_vay_da_tra),
                "08": _line("08", "Thu nhập khác từ hoạt động kinh doanh", thu_khac_tu_hdkd),
                "09": _line("09", "Chi phí khác từ hoạt động kinh doanh", chi_khac_tu_hdkd),
                "10": _line("10", "Thu tiền từ hoạt động kinh doanh khác", Decimal("0")),
                "20": _line("20", "Lưu chuyển tiền thuần từ hoạt động kinh doanh", luu_chuyen_thuan_hdkd),
            },
            "tong_thu": tong_thu_hdkd,
            "tong_chi": tong_chi_hdkd,
            "luu_chuyen_thuan": luu_chuyen_thuan_hdkd,
        },
        "II": {
            "ten": "Lưu chuyển tiền từ hoạt động đầu tư",
            "chi_tiet": {
                "21": _line("21", "Tiền mua TSCĐ", tien_mua_tscd),
                "22": _line("22", "Tiền thanh lý TSCĐ", tien_thanh_ly_tscd),
                "23": _line("23", "Tiền cho vay", tien_cho_vay),
                "24": _line("24", "Tiền thu hồi cho vay", tien_thu_hoi_cho_vay),
                "25": _line("25", "Tiền đầu tư vào đơn vị khác", tien_dau_tu_vao_don_vi_khac),
                "26": _line("26", "Tiền thu hồi đầu tư vào đơn vị khác", tien_thu_hoi_dau_tu),
            },
            "tong_thu": tong_thu_hddt,
            "tong_chi": tong_chi_hddt,
            "luu_chuyen_thuan": luu_chuyen_thuan_hddt,
        },
        "III": {
            "ten": "Lưu chuyển tiền từ hoạt động tài chính",
            "chi_tiet": {
                "31": _line("31", "Tiền vay được nhận", tien_vay_duoc_nhan),
                "32": _line("32", "Tiền trả gốc vay", tien_tra_goc_vay),
                "33": _line("33", "Tiền nộp vốn cho chủ sở hữu", tien_nop_von_cho_chu_sh),
                "34": _line("34", "Tiền nhận vốn góp từ chủ sở hữu", tien_nhan_von_gop),
                "35": _line("35", "Cổ tức đã trả", co_tuc_da_tra),
            },
            "tong_thu": tong_thu_hdtc,
            "tong_chi": tong_chi_hdtc,
            "luu_chuyen_thuan": luu_chuyen_thuan_hdtc,
        },
        "IV": {
            "ten": "Lưu chuyển tiền thuần trong kỳ",
            "tong_luu_chuyen": tong_luu_chuyen,
            "tien_dau_ky": tong_tien_dau_ky,
            "tien_cuoi_ky": tong_tien_cuoi_ky,
        },
    }


def get_so_cai_tai_khoan(
    ma_tai_khoan: str,
    tu_ngay: date,
    den_ngay: date,
) -> Dict:
    """
    Get detailed General Ledger (Sổ Cái) for a single account.

    Returns opening balance, all posted journal lines in period with running balance,
    and closing balance.

    Args:
        ma_tai_khoan: Account code (e.g. "111")
        tu_ngay: Start date of period
        den_ngay: End date of period

    Returns:
        Dict with so_du_dau_ky, lines (list), so_du_cuoi_ky
    """
    account = TaiKhoanKeToan.objects.filter(ma_tai_khoan=ma_tai_khoan).first()
    if not account:
        return {
            "account": None,
            "so_du_dau_ky": Decimal("0"),
            "lines": [],
            "so_du_cuoi_ky": Decimal("0"),
        }

    is_debit_account = account.loai_tai_khoan in (
        "tai_san", "chi_phi", "chi_phi_khac", "xac_dinh_kq",
    )

    opening_no = Decimal("0")
    opening_co = Decimal("0")
    prior_entries = ButToanChiTiet.objects.filter(
        but_toan__ngay_hach_toan__lt=tu_ngay,
        but_toan__trang_thai="posted",
        tai_khoan__ma_tai_khoan=ma_tai_khoan,
    )
    opening_no = prior_entries.filter(loai_no_co="no").aggregate(total=Sum("so_tien"))["total"] or Decimal("0")
    opening_co = prior_entries.filter(loai_no_co="co").aggregate(total=Sum("so_tien"))["total"] or Decimal("0")

    if is_debit_account:
        so_du_dau_ky = opening_no - opening_co
    else:
        so_du_dau_ky = opening_co - opening_no

    period_entries = ButToanChiTiet.objects.filter(
        but_toan__ngay_hach_toan__gte=tu_ngay,
        but_toan__ngay_hach_toan__lte=den_ngay,
        but_toan__trang_thai="posted",
        tai_khoan__ma_tai_khoan=ma_tai_khoan,
    ).select_related("but_toan", "tai_khoan").order_by("but_toan__ngay_hach_toan", "pk")

    lines = []
    running_balance = so_du_dau_ky
    for entry in period_entries:
        if is_debit_account:
            if entry.loai_no_co == "no":
                running_balance += entry.so_tien
            else:
                running_balance -= entry.so_tien
        else:
            if entry.loai_no_co == "co":
                running_balance += entry.so_tien
            else:
                running_balance -= entry.so_tien

        lines.append({
            "ngay_chung_tu": entry.but_toan.ngay_hach_toan,
            "so_chung_tu": entry.but_toan.so_but_toan,
            "dien_giai": entry.dien_giai or entry.but_toan.dien_giai,
            "loai_no_co": entry.loai_no_co,
            "so_tien": entry.so_tien,
            "so_du_tang_dan": running_balance,
            "ma_doi_tuong": entry.ma_doi_tuong,
            "so_chung_tu_goc": entry.so_chung_tu_goc,
        })

    return {
        "account": account,
        "so_du_dau_ky": so_du_dau_ky,
        "lines": lines,
        "so_du_cuoi_ky": running_balance,
    }


def get_tong_hop_so_cai(
    tu_ngay: date,
    den_ngay: date,
) -> Dict:
    """
    Get summary General Ledger (Tổng hợp Sổ Cái) for all accounts.

    Returns each account with opening balances, period activity, and closing balances,
    plus a totals row.

    Args:
        tu_ngay: Start date of period
        den_ngay: End date of period

    Returns:
        Dict with accounts (list), totals
    """
    period_entries = ButToanChiTiet.objects.filter(
        but_toan__ngay_hach_toan__gte=tu_ngay,
        but_toan__ngay_hach_toan__lte=den_ngay,
        but_toan__trang_thai="posted",
    ).select_related("tai_khoan")

    account_data: Dict[str, Dict] = {}
    for entry in period_entries:
        ma = entry.tai_khoan.ma_tai_khoan
        if ma not in account_data:
            account_data[ma] = {
                "ten_tai_khoan": entry.tai_khoan.ten_tai_khoan,
                "loai_tai_khoan": entry.tai_khoan.loai_tai_khoan,
                "ps_no": Decimal("0"),
                "ps_co": Decimal("0"),
            }
        if entry.loai_no_co == "no":
            account_data[ma]["ps_no"] += entry.so_tien
        else:
            account_data[ma]["ps_co"] += entry.so_tien

    accounts = []
    tong_so_du_dau_no = Decimal("0")
    tong_so_du_dau_co = Decimal("0")
    tong_phat_sinh_no = Decimal("0")
    tong_phat_sinh_co = Decimal("0")
    tong_so_du_cuoi_no = Decimal("0")
    tong_so_du_cuoi_co = Decimal("0")

    for ma in sorted(account_data.keys()):
        data = account_data[ma]
        ps_no = data["ps_no"]
        ps_co = data["ps_co"]

        prior_no = Decimal("0")
        prior_co = Decimal("0")
        prior = ButToanChiTiet.objects.filter(
            but_toan__ngay_hach_toan__lt=tu_ngay,
            but_toan__trang_thai="posted",
            tai_khoan__ma_tai_khoan=ma,
        )
        prior_no = prior.filter(loai_no_co="no").aggregate(total=Sum("so_tien"))["total"] or Decimal("0")
        prior_co = prior.filter(loai_no_co="co").aggregate(total=Sum("so_tien"))["total"] or Decimal("0")

        is_debit = data["loai_tai_khoan"] in (
            "tai_san", "chi_phi", "chi_phi_khac", "xac_dinh_kq",
        )

        if is_debit:
            so_du_dau = prior_no - prior_co
            so_du_cuoi = so_du_dau + ps_no - ps_co
            if so_du_dau >= 0:
                sd_dau_no = so_du_dau
                sd_dau_co = Decimal("0")
            else:
                sd_dau_no = Decimal("0")
                sd_dau_co = abs(so_du_dau)
            if so_du_cuoi >= 0:
                sd_cuoi_no = so_du_cuoi
                sd_cuoi_co = Decimal("0")
            else:
                sd_cuoi_no = Decimal("0")
                sd_cuoi_co = abs(so_du_cuoi)
        else:
            so_du_dau = prior_co - prior_no
            so_du_cuoi = so_du_dau + ps_co - ps_no
            if so_du_dau >= 0:
                sd_dau_co = so_du_dau
                sd_dau_no = Decimal("0")
            else:
                sd_dau_co = Decimal("0")
                sd_dau_no = abs(so_du_dau)
            if so_du_cuoi >= 0:
                sd_cuoi_co = so_du_cuoi
                sd_cuoi_no = Decimal("0")
            else:
                sd_cuoi_co = Decimal("0")
                sd_cuoi_no = abs(so_du_cuoi)

        accounts.append({
            "ma_tai_khoan": ma,
            "ten_tai_khoan": data["ten_tai_khoan"],
            "so_du_dau_no": sd_dau_no,
            "so_du_dau_co": sd_dau_co,
            "phat_sinh_no": ps_no,
            "phat_sinh_co": ps_co,
            "so_du_cuoi_no": sd_cuoi_no,
            "so_du_cuoi_co": sd_cuoi_co,
        })

        tong_so_du_dau_no += sd_dau_no
        tong_so_du_dau_co += sd_dau_co
        tong_phat_sinh_no += ps_no
        tong_phat_sinh_co += ps_co
        tong_so_du_cuoi_no += sd_cuoi_no
        tong_so_du_cuoi_co += sd_cuoi_co

    return {
        "tu_ngay": tu_ngay,
        "den_ngay": den_ngay,
        "accounts": accounts,
        "tong_so_du_dau_no": tong_so_du_dau_no,
        "tong_so_du_dau_co": tong_so_du_dau_co,
        "tong_phat_sinh_no": tong_phat_sinh_no,
        "tong_phat_sinh_co": tong_phat_sinh_co,
        "tong_so_du_cuoi_no": tong_so_du_cuoi_no,
        "tong_so_du_cuoi_co": tong_so_du_cuoi_co,
    }


def lap_thuyet_minh_bctc(ngay_ket_thuc: date) -> Dict:
    """
    Generate Notes to Financial Statements (Thuyết minh BCTC - Mẫu B09-DN).

    Legal basis: Thông tư 99/2025/TT-BTC, Phụ lục I - Mẫu B09-DN
    """
    return {
        "ngay_bao_cao": ngay_ket_thuc,
        "thong_tin_chung": {
            "ten_doanh_nghiep": "Công ty TNHH SME",
            "ma_so_thue": "",
            "dia_chi": "",
            "ngay_bao_cao": ngay_ket_thuc,
            "ky_bao_cao": f"Năm tài chính kết thúc ngày {ngay_ket_thuc.strftime('%d/%m/%Y')}",
        },
        "chinh_sach_ke_toan": {
            "co_so_lap": "BCTC được lập theo Thông tư 99/2025/TT-BTC",
            "nguyen_tac_gia_goc": "Tài sản và nợ được ghi nhận theo nguyên tắc giá gốc",
            "phuong_phap_khau_hao": "Khấu hao đường thẳng theo thời gian sử dụng hữu ích",
            "phuong_phap_ton_kho": "Phương pháp bình quân gia quyền liên hoàn",
            "nguyen_tac_ghi_nhan_doanh_thu": "Doanh thu được ghi nhận khi quyền sở hữu được chuyển giao",
        },
        "thuyet_minh_chi_tieu": {
            "tien_va_tuong_duong": "Gồm tiền mặt tại quỹ (111), tiền gửi ngân hàng (112), tiền đang chuyển (113)",
            "phai_thu": "Phải thu khách hàng (131), phải thu nội bộ (136), phải thu khác (138)",
            "hang_ton_kho": "Nguyên liệu (152), công cụ dụng cụ (153), thành phẩm (155), hàng hóa (157)",
            "tai_san_co_dinh": "TSCĐ hữu hình (211), TSCĐ vô hình (213), hao mòn lũy kế (214)",
            "no_phai_tra": "Phải trả người bán (331), thuế phải nộp (333), phải trả NLĐ (334)",
            "von_chu_so_huu": "Vốn đầu tư CSH (411), lợi nhuận chưa phân phối (421)",
        },
    }
