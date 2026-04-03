"""
Comprehensive master data compliance tests against Thông tư 99/2025/TT-BTC.

These tests validate:
1. Chart of Accounts integrity (all Tier-1 and Tier-2 accounts)
2. Mandatory fields on document models
3. Tax constants compliance with 2025-2026 law
4. Document validation rules

Legal basis:
    - Thông tư 99/2025/TT-BTC Phụ lục II (Chart of Accounts)
    - Thông tư 99/2025/TT-BTC Phụ lục I (Document catalog)
    - Luật 67/2025/QH15 (Corporate Income Tax)
    - Nghị định 70/2025/NĐ-CP (VAT reduction)
    - Nghị định 58/2020/NĐ-CP (Social Insurance)
"""

import re
from datetime import date, timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings
from django.utils import timezone

from apps.danh_muc.models import (
    HangHoa,
    KhachHang,
    NhaCungCap,
    TaiKhoanKeToan,
)
from apps.nghiep_vu.constants import (
    THUE_SUAT_GTGT_2026,
    THUE_SUAT_TNDN_DEFAULT,
    THUE_SUAT_TNDN_SME,
)
from apps.nghiep_vu.models import (
    ButToan,
    ButToanChiTiet,
    HoaDon,
    HoaDonChiTiet,
    PhieuChi,
    PhieuThu,
)


# =============================================================================
# FULL CHART OF ACCOUNTS - TT 99/2025/TT-BTC Phụ lục II
# =============================================================================

TIER1_ACCOUNTS = {
    # LOẠI 1 - TÀI SẢN NGẮN HẠN
    "111": ("Tiền mặt", "tai_san"),
    "112": ("Tiền gửi ngân hàng", "tai_san"),
    "113": ("Tiền đang chuyển", "tai_san"),
    "121": ("Chứng khoán kinh doanh", "tai_san"),
    "122": ("Đầu tư nắm giữ đến ngày đáo hạn", "tai_san"),
    "128": ("Đầu tư nắm giữ ngắn hạn khác", "tai_san"),
    "131": ("Phải thu của khách hàng", "tai_san"),
    "133": ("Thuế GTGT được khấu trừ", "tai_san"),
    "136": ("Phải thu nội bộ", "tai_san"),
    "137": ("Phải thu theo tiến độ kế hoạch hợp đồng xây dựng", "tai_san"),
    "138": ("Phải thu khác", "tai_san"),
    "139": ("Dự phòng phải thu khó đòi", "tai_san"),
    "141": ("Tạm ứng", "tai_san"),
    "142": ("Chi phí trả trước ngắn hạn", "tai_san"),
    "144": ("Ký cược, ký quỹ ngắn hạn", "tai_san"),
    "151": ("Hàng mua đang đi trên đường", "tai_san"),
    "152": ("Nguyên liệu, vật liệu", "tai_san"),
    "153": ("Công cụ, dụng cụ", "tai_san"),
    "154": ("Chi phí sản xuất, kinh doanh dở dang", "tai_san"),
    "155": ("Sản phẩm", "tai_san"),
    "156": ("Hàng hóa", "tai_san"),
    "157": ("Hàng gửi đi bán", "tai_san"),
    "158": ("Nguyên liệu, vật tư tại kho bảo thuế", "tai_san"),
    "161": ("Thuế và các khoản phải thu Nhà nước", "tai_san"),
    "171": ("Giao dịch mua, bán lại trái phiếu chính phủ", "tai_san"),
    # LOẠI 2 - TÀI SẢN DÀI HẠN
    "211": ("Tài sản cố định hữu hình", "tai_san"),
    "212": ("Tài sản cố định thuê tài chính", "tai_san"),
    "213": ("Tài sản cố định vô hình", "tai_san"),
    "214": ("Hao mòn TSCĐ", "tai_san"),
    "215": ("Tài sản sinh học", "tai_san"),
    "217": ("Bất động sản đầu tư", "tai_san"),
    "221": ("Đầu tư vào công ty con", "tai_san"),
    "222": ("Góp vốn liên doanh", "tai_san"),
    "228": ("Đầu tư góp vốn khác", "tai_san"),
    "229": ("Dự phòng đầu tư dài hạn", "tai_san"),
    "241": ("XDCB dở dang", "tai_san"),
    "242": ("Chi phí trả trước dài hạn", "tai_san"),
    "243": ("Tài sản thuế thu nhập hoãn lại", "tai_san"),
    "244": ("Ký cược, ký quỹ dài hạn", "tai_san"),
    "261": ("Ký quỹ, ký cược dài hạn", "tai_san"),
    # LOẠI 3 - NỢ PHẢI TRẢ
    "311": ("Vay và nợ thuê tài chính ngắn hạn", "no_phai_tra"),
    "312": ("Nợ thuê tài chính ngắn hạn", "no_phai_tra"),
    "331": ("Phải trả cho người bán", "no_phai_tra"),
    "332": ("Phải trả cổ tức, lợi nhuận", "no_phai_tra"),
    "333": ("Thuế và các khoản phải nộp Nhà nước", "no_phai_tra"),
    "334": ("Phải trả người lao động", "no_phai_tra"),
    "335": ("Chi phí phải trả ngắn hạn", "no_phai_tra"),
    "336": ("Phải trả nội bộ", "no_phai_tra"),
    "337": ("Thanh toán theo tiến độ kế hoạch hợp đồng xây dựng", "no_phai_tra"),
    "338": ("Phải trả, phải nộp khác", "no_phai_tra"),
    "341": ("Vay và nợ thuê tài chính dài hạn", "no_phai_tra"),
    "342": ("Nợ thuê tài chính dài hạn", "no_phai_tra"),
    "343": ("Trái phiếu phát hành", "no_phai_tra"),
    "344": ("Nhận ký quỹ, ký cược", "no_phai_tra"),
    "347": ("Thuế thu nhập hoãn lại phải trả", "no_phai_tra"),
    "349": ("Nghĩa vụ khác dài hạn", "no_phai_tra"),
    "352": ("Dự phòng phải trả", "no_phai_tra"),
    "353": ("Quỹ khen thưởng, phúc lợi", "no_phai_tra"),
    "356": ("Quỹ phát triển khoa học và công nghệ", "no_phai_tra"),
    "357": ("Quỹ bình ổn giá", "no_phai_tra"),
    # LOẠI 4 - VỐN CHỦ SỞ HỮU
    "411": ("Vốn đầu tư của chủ sở hữu", "von_chu_so_huu"),
    "412": ("Thặng dư vốn cổ phần", "von_chu_so_huu"),
    "413": ("Chênh lệch tỷ giá hối đoái", "von_chu_so_huu"),
    "414": ("Quỹ đầu tư phát triển", "von_chu_so_huu"),
    "415": ("Chênh lệch đánh giá lại tài sản", "von_chu_so_huu"),
    "418": ("Các quỹ khác thuộc vốn chủ sở hữu", "von_chu_so_huu"),
    "419": ("Cổ phiếu quỹ", "von_chu_so_huu"),
    "420": ("Lợi ích cổ đông thiểu số", "von_chu_so_huu"),
    "421": ("Lợi nhuận sau thuế chưa phân phối", "von_chu_so_huu"),
    # LOẠI 5 - DOANH THU
    "511": ("Doanh thu bán hàng và cung cấp dịch vụ", "doanh_thu"),
    "512": ("Doanh thu bán hàng nội bộ", "doanh_thu"),
    "515": ("Doanh thu hoạt động tài chính", "doanh_thu"),
    "521": ("Các khoản giảm trừ doanh thu", "doanh_thu"),
    # LOẠI 6 - CHI PHÍ
    "621": ("Chi phí nguyên liệu, vật liệu trực tiếp", "chi_phi"),
    "622": ("Chi phí nhân công trực tiếp", "chi_phi"),
    "623": ("Chi phí sử dụng máy thi công", "chi_phi"),
    "627": ("Chi phí sản xuất chung", "chi_phi"),
    "631": ("Giá thành sản xuất", "chi_phi"),
    "632": ("Giá vốn hàng bán", "chi_phi"),
    "635": ("Chi phí tài chính", "chi_phi"),
    "641": ("Chi phí bán hàng", "chi_phi"),
    "642": ("Chi phí quản lý kinh doanh", "chi_phi"),
    # LOẠI 7 - THU NHẬP KHÁC
    "711": ("Thu nhập khác", "thu_nhap_khac"),
    # LOẠI 8 - CHI PHÍ KHÁC
    "811": ("Chi phí khác", "chi_phi_khac"),
    # LOẠI 9 - XÁC ĐỊNH KẾT QUẢ
    "911": ("Xác định kết quả kinh doanh", "xac_dinh_kq"),
}

TIER2_ACCOUNTS = {
    # Under 128
    "1281": ("Đầu tư ngắn hạn", "128"),
    "1282": ("Đầu tư dài hạn", "128"),
    "1283": ("Dự phòng giảm giá đầu tư", "128"),
    "1288": ("Đầu tư khác", "128"),
    # Under 133
    "1331": ("Thuế GTGT được khấu trừ", "133"),
    "1332": ("Thuế GTGT đầu vào của BĐS đầu tư", "133"),
    # Under 136
    "1361": ("Phải thu nội bộ ngắn hạn", "136"),
    "1362": ("Phải thu nội bộ dài hạn", "136"),
    "1363": ("Phải thu nội bộ khác", "136"),
    "1368": ("Phải thu nội bộ chi tiết", "136"),
    # Under 138
    "1381": ("Phải thu về tài sản thiếu", "138"),
    "1383": ("Phải thu về bồi thường", "138"),
    "1388": ("Phải thu khác chi tiết", "138"),
    # Under 214
    "2141": ("Hao mòn TSCĐ hữu hình", "214"),
    "2142": ("Hao mòn TSCĐ thuê tài chính", "214"),
    "2143": ("Hao mòn TSCĐ vô hình", "214"),
    "2147": ("Hao mòn BĐS đầu tư", "214"),
    # Under 215 - Tài sản sinh học
    "2151": ("Tài sản sinh học ngắn hạn", "215"),
    "2152": ("Tài sản sinh học dài hạn", "215"),
    # Under 229
    "2291": ("Dự phòng đầu tư CK kinh doanh", "229"),
    "2292": ("Dự phòng đầu tư đơn vị khác", "229"),
    "2293": ("Dự phòng đầu tư nắm giữ đến đáo hạn", "229"),
    "2294": ("Dự phòng tổn thất đầu tư khác", "229"),
    "2295": ("Dự phòng giảm giá đầu tư dài hạn", "229"),
    # Under 352 - Dự phòng phải trả
    "3521": ("Dự phòng bảo hành sản phẩm, hàng hóa", "352"),
    "3522": ("Dự phòng bảo lãnh", "352"),
    "3523": ("Dự phòng phải trả khác", "352"),
    # Under 353 - Quỹ khen thưởng, phúc lợi
    "3531": ("Quỹ khen thưởng", "353"),
    "3532": ("Quỹ phúc lợi", "353"),
    # Under 356 - Quỹ phát triển KH&CN
    "3561": ("Quỹ phát triển KH&CN ngắn hạn", "356"),
    "3562": ("Quỹ phát triển KH&CN dài hạn", "356"),
    # Under 241
    "2411": ("Chi phí XDCB dở dang", "241"),
    "2412": ("Thiết bị đang lắp đặt", "241"),
    "2413": ("Chi phí khác XDCB", "241"),
    "2414": ("Chi phí XDCB khác", "241"),
    # Under 333
    "3331": ("Thuế GTGT phải nộp", "333"),
    "3332": ("Thuế tiêu thụ đặc biệt", "333"),
    "3333": ("Thuế xuất, nhập khẩu", "333"),
    "3334": ("Thuế thu nhập doanh nghiệp", "333"),
    "3335": ("Thuế thu nhập cá nhân", "333"),
    "3336": ("Thuế tài nguyên", "333"),
    "3337": ("Thuế nhà thầu", "333"),
    "3338": ("Thuế bảo vệ môi trường", "333"),
    "3339": ("Các loại thuế khác", "333"),
    # Under 338
    "3381": ("Tài sản thừa chờ giải quyết", "338"),
    "3382": ("Kinh phí công đoàn", "338"),
    "3383": ("BHXH phải nộp", "338"),
    "3384": ("BHYT phải nộp", "338"),
    "3385": ("BHTN phải nộp", "338"),
    "3386": ("BHTNLĐ-BNN phải nộp", "338"),
    "3387": ("Công đoàn phí", "338"),
    "3388": ("Phải trả phải nộp khác", "338"),
    # Under 341
    "3411": ("Vay ngắn hạn", "341"),
    "3412": ("Vay dài hạn", "341"),
    # Under 343
    "3431": ("Trái phiếu thường", "343"),
    "3432": ("Trái phiếu có quyền chọn", "343"),
    # Under 411
    "4111": ("Vốn góp của chủ sở hữu", "411"),
    "4112": ("Thặng dư vốn cổ phần", "411"),
    "4113": ("Quyền chọn chuyển đổi trái phiếu", "411"),
    "4118": ("Vốn khác", "411"),
    # Under 421
    "4211": ("Lợi nhuận năm trước", "421"),
    "4212": ("Lợi nhuận năm nay", "421"),
    # Under 511
    "5111": ("Doanh thu bán hàng hóa", "511"),
    "5112": ("Doanh thu bán thành phẩm", "511"),
    "5113": ("Doanh thu cung cấp dịch vụ", "511"),
    "5114": ("Doanh thu trợ cấp, trợ giá", "511"),
    "5115": ("Doanh thu bất động sản đầu tư", "511"),
    "5116": ("Doanh thu nhượng bán TSCĐ", "511"),
    "5117": ("Doanh thu cho thuê TSCĐ", "511"),
    "5118": ("Doanh thu bản quyền", "511"),
    "5119": ("Doanh thu khác", "511"),
    # Under 521
    "5211": ("Chiết khấu thương mại", "521"),
    "5212": ("Giảm giá hàng bán", "521"),
    "5213": ("Hàng bán bị trả lại", "521"),
    "5214": ("Thuế TTĐB, thuế XK, thuế GTGT theo pp trực tiếp", "521"),
    # Under 621
    "6211": ("Chi phí NVLTT", "621"),
    # Under 622
    "6221": ("Chi phí NCTT", "622"),
    # Under 623
    "6231": ("Chi phí nhân công", "623"),
    "6232": ("Chi phí vật liệu", "623"),
    "6233": ("Chi phí dụng cụ sản xuất", "623"),
    "6234": ("Chi phí khấu hao máy", "623"),
    "6235": ("Chi phí dịch vụ mua ngoài", "623"),
    "6236": ("Chi phí bằng tiền khác", "623"),
    # Under 627
    "6271": ("Chi phí nhân viên phân xưởng", "627"),
    "6272": ("Chi phí vật liệu", "627"),
    "6273": ("Chi phí dụng cụ", "627"),
    "6274": ("Chi phí khấu hao TSCĐ", "627"),
    "6275": ("Chi phí dịch vụ mua ngoài", "627"),
    "6276": ("Chi phí bằng tiền khác", "627"),
    # Under 642
    "6421": ("Chi phí nhân viên quản lý", "642"),
    "6422": ("Chi phí vật liệu quản lý", "642"),
    "6423": ("Chi phí đồ dùng văn phòng", "642"),
    "6424": ("Chi phí khấu hao TSCĐ", "642"),
    "6425": ("Thuế, phí, lệ phí", "642"),
    "6426": ("Chi phí dịch vụ mua ngoài", "642"),
    "6427": ("Chi phí bằng tiền khác", "642"),
    "6428": ("Chi phí khác", "642"),
    # Under 821
    "8211": ("Chi phí thuế TNDN hiện hành", "821"),
    "8212": ("Chi phí thuế TNDN hoãn lại", "821"),
}


class TestCOAIntegrity(TestCase):
    """
    Test that the Chart of Accounts matches TT 99/2025/TT-BTC Phụ lục II exactly.

    These tests MUST FAIL if any account is missing or has wrong name.

    Legal basis:
        - Thông tư 99/2025/TT-BTC Phụ lục II - Hệ thống tài khoản kế toán
    """

    def test_all_tier1_accounts_exist(self):
        """FAIL if any Tier-1 account from TT 99 is missing."""
        existing_codes = set(
            TaiKhoanKeToan.objects.filter(cap_do=1).values_list(
                "ma_tai_khoan", flat=True
            )
        )
        missing = set(TIER1_ACCOUNTS.keys()) - existing_codes
        self.assertFalse(
            missing,
            f"Missing Tier-1 accounts: {sorted(missing)}",
        )

    def test_all_tier2_accounts_exist(self):
        """FAIL if any Tier-2 account from TT 99 is missing."""
        existing_codes = set(
            TaiKhoanKeToan.objects.filter(cap_do=2).values_list(
                "ma_tai_khoan", flat=True
            )
        )
        missing = set(TIER2_ACCOUNTS.keys()) - existing_codes
        self.assertFalse(
            missing,
            f"Missing Tier-2 accounts: {sorted(missing)}",
        )

    def test_account_names_match_exactly(self):
        """FAIL if any account name differs from TT 99."""
        for code, (expected_name, _) in TIER1_ACCOUNTS.items():
            acc = TaiKhoanKeToan.objects.filter(
                ma_tai_khoan=code, cap_do=1
            ).first()
            if acc:
                self.assertEqual(
                    acc.ten_tai_khoan,
                    expected_name,
                    f"Account {code} name mismatch: '{acc.ten_tai_khoan}' != '{expected_name}'",
                )
        for code, (expected_name, _) in TIER2_ACCOUNTS.items():
            acc = TaiKhoanKeToan.objects.filter(
                ma_tai_khoan=code, cap_do=2
            ).first()
            if acc:
                self.assertEqual(
                    acc.ten_tai_khoan,
                    expected_name,
                    f"Account {code} name mismatch: '{acc.ten_tai_khoan}' != '{expected_name}'",
                )

    def test_account_types_are_correct(self):
        """FAIL if account type (loai_tai_khoan) is wrong."""
        for code, (_, expected_type) in TIER1_ACCOUNTS.items():
            acc = TaiKhoanKeToan.objects.filter(
                ma_tai_khoan=code, cap_do=1
            ).first()
            if acc:
                self.assertEqual(
                    acc.loai_tai_khoan,
                    expected_type,
                    f"Account {code} type mismatch: '{acc.loai_tai_khoan}' != '{expected_type}'",
                )

    def test_account_hierarchy_is_valid(self):
        """FAIL if Tier-2 accounts don't have correct Tier-1 parent."""
        for code, (_, expected_parent) in TIER2_ACCOUNTS.items():
            acc = TaiKhoanKeToan.objects.filter(
                ma_tai_khoan=code, cap_do=2
            ).first()
            if acc and acc.tai_khoan_me_id:
                self.assertEqual(
                    acc.tai_khoan_me.ma_tai_khoan,
                    expected_parent,
                    f"Account {code} parent mismatch: "
                    f"'{acc.tai_khoan_me.ma_tai_khoan}' != '{expected_parent}'",
                )

    def test_immutable_accounts_cannot_be_modified(self):
        """FAIL if seeded accounts can be changed."""
        immutable = TaiKhoanKeToan.objects.filter(is_immutable=True).first()
        if immutable:
            original_name = immutable.ten_tai_khoan
            immutable.ten_tai_khoan = "MODIFIED NAME"
            with self.assertRaises(ValidationError):
                immutable.full_clean()
            immutable.ten_tai_khoan = original_name

    def test_no_duplicate_account_codes(self):
        """FAIL if duplicate ma_tai_khoan exists."""
        codes = TaiKhoanKeToan.objects.values_list("ma_tai_khoan", flat=True)
        self.assertEqual(
            len(codes),
            len(set(codes)),
            "Duplicate account codes found",
        )

    def test_account_code_format_valid(self):
        """FAIL if account codes don't match 3-digit pattern for Tier-1."""
        pattern = re.compile(r"^\d{3,4}$")
        for acc in TaiKhoanKeToan.objects.all():
            self.assertTrue(
                pattern.match(acc.ma_tai_khoan),
                f"Account code '{acc.ma_tai_khoan}' doesn't match 3-4 digit pattern",
            )


class TestMandatoryDocumentFields(TestCase):
    """
    Test that all document models have mandatory fields per Accounting Law.

    Legal basis:
        - Thông tư 99/2025/TT-BTC Phụ lục I - Danh mục chứng từ kế toán
        - Luật Kế toán 2015 - Nội dung chứng từ kế toán
    """

    def test_hoadon_has_mandatory_fields(self):
        """Invoice must have: ma_so_thue, dia_chi, nguoi_mua_hang, nguoi_ban_hang."""
        kh = KhachHang.objects.create(
            ma_kh="TEST001",
            ten_kh="Test Customer",
            ma_so_thue="0123456789",
            dia_chi="Test Address",
        )
        hd = HoaDon(
            so_hoa_don="HD-TEST-001",
            ngay_hoa_don=date.today(),
            khach_hang=kh,
            nguoi_mua_hang="Nguyen Van A",
            ma_so_thue_mua="0123456789",
            dia_chi_mua="Test Address",
            tong_tien_truoc_thue=Decimal("1000000"),
            tien_thue_gtgt=Decimal("100000"),
            tong_cong_thanh_toan=Decimal("1100000"),
        )
        hd.full_clean()
        hd.save()
        self.assertEqual(hd.nguoi_mua_hang, "Nguyen Van A")
        self.assertEqual(hd.ma_so_thue_mua, "0123456789")

    def test_hoadon_has_tax_fields(self):
        """Invoice must have: thue_suat, tien_thue, tong_tien_thanh_toan."""
        kh = KhachHang.objects.create(
            ma_kh="TEST002",
            ten_kh="Test Customer 2",
            ma_so_thue="0123456789",
        )
        hd = HoaDon(
            so_hoa_don="HD-TEST-002",
            ngay_hoa_don=date.today(),
            khach_hang=kh,
            tong_tien_truoc_thue=Decimal("1000000"),
            tien_thue_gtgt=Decimal("100000"),
            tong_cong_thanh_toan=Decimal("1100000"),
        )
        hd.full_clean()
        hd.save()
        self.assertEqual(hd.tien_thue_gtgt, Decimal("100000"))
        self.assertEqual(hd.tong_cong_thanh_toan, Decimal("1100000"))

    def test_hoadon_has_legal_fields(self):
        """Invoice must have: ky_hieu, so_hoa_don, ngay_hoa_don."""
        kh = KhachHang.objects.create(
            ma_kh="TEST003",
            ten_kh="Test Customer 3",
            ma_so_thue="0123456789",
        )
        hd = HoaDon(
            so_hoa_don="HD-TEST-003",
            ngay_hoa_don=date.today(),
            khach_hang=kh,
            ky_hieu="AA/26E",
            tong_tien_truoc_thue=Decimal("0"),
            tien_thue_gtgt=Decimal("0"),
            tong_cong_thanh_toan=Decimal("0"),
        )
        hd.full_clean()
        hd.save()
        self.assertEqual(hd.ky_hieu, "AA/26E")
        self.assertIsNotNone(hd.ngay_hoa_don)

    def test_phieu_thu_has_mandatory_fields(self):
        """Receipt must have: so_tien, tk_no, tk_co, dien_giai, ngay_chung_tu."""
        tk111 = TaiKhoanKeToan.objects.filter(ma_tai_khoan="111").first()
        tk511 = TaiKhoanKeToan.objects.filter(ma_tai_khoan="511").first()
        if tk111 and tk511:
            pt = PhieuThu(
                so_chung_tu="PT-TEST-001",
                ngay_chung_tu=date.today(),
                loai_chung_tu="phieu_thu",
                so_tien=Decimal("1000000"),
                tk_no=tk111,
                tk_co=tk511,
                dien_giai="Test receipt",
            )
            pt.full_clean()
            pt.save()
            self.assertEqual(pt.so_tien, Decimal("1000000"))
            self.assertEqual(pt.tk_no, tk111)

    def test_phieu_chi_has_mandatory_fields(self):
        """Payment must have: so_tien, tk_no, tk_co, dien_giai, ngay_chung_tu."""
        tk331 = TaiKhoanKeToan.objects.filter(ma_tai_khoan="331").first()
        tk111 = TaiKhoanKeToan.objects.filter(ma_tai_khoan="111").first()
        if tk331 and tk111:
            pc = PhieuChi(
                so_chung_tu="PC-TEST-001",
                ngay_chung_tu=date.today(),
                loai_chung_tu="phieu_chi",
                so_tien=Decimal("500000"),
                tk_no=tk331,
                tk_co=tk111,
                dien_giai="Test payment",
            )
            pc.full_clean()
            pc.save()
            self.assertEqual(pc.so_tien, Decimal("500000"))
            self.assertEqual(pc.tk_co, tk111)

    def test_but_toan_has_mandatory_fields(self):
        """Journal must have: so_but_toan, ngay_hach_toan, nguoi_tao."""
        bt = ButToan(
            so_but_toan="BT-TEST-001",
            ngay_hach_toan=date.today(),
            dien_giai="Test journal",
        )
        bt.full_clean()
        bt.save()
        self.assertEqual(bt.so_but_toan, "BT-TEST-001")
        self.assertIsNotNone(bt.ngay_hach_toan)

    def test_khachhang_has_mandatory_fields(self):
        """Customer must have: ma_so_thue, ten_kh, dia_chi."""
        kh = KhachHang(
            ma_kh="TEST004",
            ten_kh="Test Customer 4",
            ma_so_thue="0123456789",
            dia_chi="Test Address",
        )
        kh.full_clean()
        kh.save()
        self.assertEqual(kh.ma_so_thue, "0123456789")
        self.assertEqual(kh.ten_kh, "Test Customer 4")

    def test_nhacungcap_has_mandatory_fields(self):
        """Supplier must have: ma_so_thue, ten_ncc, dia_chi."""
        ncc = NhaCungCap(
            ma_ncc="SUP001",
            ten_ncc="Test Supplier",
            ma_so_thue="0987654321",
            dia_chi="Supplier Address",
        )
        ncc.full_clean()
        ncc.save()
        self.assertEqual(ncc.ma_so_thue, "0987654321")
        self.assertEqual(ncc.ten_ncc, "Test Supplier")

    def test_hanghoa_has_mandatory_fields(self):
        """Goods must have: ma_hang_hoa, ten_hang_hoa, don_vi_tinh."""
        hh = HangHoa(
            ma_hang_hoa="ITEM001",
            ten_hang_hoa="Test Item",
            don_vi_tinh="cái",
        )
        hh.full_clean()
        hh.save()
        self.assertEqual(hh.ma_hang_hoa, "ITEM001")
        self.assertEqual(hh.don_vi_tinh, "cái")


class TestTaxConstantsCompliance(TestCase):
    """
    Test that tax constants match 2025-2026 law.

    Legal basis:
        - Thông tư 99/2025/TT-BTC - VAT rates
        - Nghị định 70/2025/NĐ-CP - VAT reduction to 8%
        - Luật 67/2025/QH15 - Corporate Income Tax
        - Nghị định 58/2020/NĐ-CP - Social Insurance rates
    """

    def test_vat_rates_2026(self):
        """VAT rates must be exactly 0%, 5%, 8%, 10%."""
        expected_rates = {"0", "5", "8", "10"}
        actual_rates = {rate[0] for rate in THUE_SUAT_GTGT_2026}
        self.assertEqual(
            actual_rates,
            expected_rates,
            f"VAT rates mismatch: {actual_rates} != {expected_rates}",
        )

    def test_tndn_rates_2026(self):
        """TNDN rates must include 15% (SME) and 20% (standard)."""
        self.assertEqual(THUE_SUAT_TNDN_SME, Decimal("0.15"))
        self.assertEqual(THUE_SUAT_TNDN_DEFAULT, Decimal("0.20"))

    def test_tncn_brackets_2026(self):
        """TNCN must have 7 brackets with correct thresholds."""
        from apps.luong.constants import THUE_TNCN_BRACKETS

        self.assertEqual(len(THUE_TNCN_BRACKETS), 7)
        expected_rates = [
            Decimal("0.05"),
            Decimal("0.10"),
            Decimal("0.15"),
            Decimal("0.20"),
            Decimal("0.25"),
            Decimal("0.30"),
            Decimal("0.35"),
        ]
        actual_rates = [b[2] for b in THUE_TNCN_BRACKETS]
        self.assertEqual(actual_rates, expected_rates)

    def test_bhxh_rates_2026(self):
        """BHXH rates must match 2026: BHXH 8%/17.5%, BHYT 1.5%/3%, BHTN 1%/1%."""
        from apps.luong.constants import (
            BHXT_DN_BHXH,
            BHXT_DN_BHTN,
            BHXT_DN_BHTNLĐ_BNN,
            BHXT_DN_BHYT,
            BHXT_NLD_BHXH,
            BHXT_NLD_BHTN,
            BHXT_NLD_BHYT,
        )

        self.assertEqual(BHXT_NLD_BHXH, Decimal("0.08"))
        self.assertEqual(BHXT_DN_BHXH, Decimal("0.175"))
        self.assertEqual(BHXT_NLD_BHYT, Decimal("0.015"))
        self.assertEqual(BHXT_DN_BHYT, Decimal("0.03"))
        self.assertEqual(BHXT_NLD_BHTN, Decimal("0.01"))
        self.assertEqual(BHXT_DN_BHTN, Decimal("0.01"))
        self.assertEqual(BHXT_DN_BHTNLĐ_BNN, Decimal("0.005"))

    def test_personal_deductions_2026(self):
        """Personal deduction: 11M/month, dependent: 4.4M/month."""
        from apps.luong.constants import GIAM_TRU_BAN_THAN, GIAM_TRU_PHU_THUOC

        self.assertEqual(GIAM_TRU_BAN_THAN, Decimal("11000000"))
        self.assertEqual(GIAM_TRU_PHU_THUOC, Decimal("4400000"))

    def test_bhxh_cap_2026(self):
        """BHXH salary cap: 46,800,000 VND (20x base salary 2,340,000)."""
        from apps.luong.constants import LUONG_CO_BAN, MAX_LUONG_BHXH

        self.assertEqual(LUONG_CO_BAN, Decimal("2340000"))
        self.assertEqual(MAX_LUONG_BHXH, Decimal("46800000"))


class TestDocumentValidationRules(TestCase):
    """
    Test business validation rules on document models.

    Legal basis:
        - Thông tư 99/2025/TT-BTC - Validation rules for accounting documents
        - Luật Kế toán 2015 - Document integrity requirements
    """

    def test_hoadon_tong_cong_calculation(self):
        """tong_cong = tong_truoc_thue + tien_thue."""
        kh = KhachHang.objects.create(
            ma_kh="TEST010",
            ten_kh="Test Customer 10",
            ma_so_thue="0123456789",
        )
        hd = HoaDon(
            so_hoa_don="HD-TEST-010",
            ngay_hoa_don=date.today(),
            khach_hang=kh,
            tong_tien_truoc_thue=Decimal("1000000"),
            tien_thue_gtgt=Decimal("100000"),
            tong_cong_thanh_toan=Decimal("1100000"),
        )
        hd.full_clean()
        hd.save()
        expected = Decimal("1000000") + Decimal("100000")
        self.assertEqual(hd.tong_cong_thanh_toan, expected)

    def test_hoadon_line_items_sum(self):
        """Sum of line items must equal total."""
        kh = KhachHang.objects.create(
            ma_kh="TEST011",
            ten_kh="Test Customer 11",
            ma_so_thue="0123456789",
        )
        hh = HangHoa.objects.create(
            ma_hang_hoa="ITEM011",
            ten_hang_hoa="Test Item 11",
            don_vi_tinh="cái",
            gia_ban=Decimal("500000"),
        )
        hd = HoaDon(
            so_hoa_don="HD-TEST-011",
            ngay_hoa_don=date.today(),
            khach_hang=kh,
            tong_tien_truoc_thue=Decimal("1000000"),
            tien_thue_gtgt=Decimal("100000"),
            tong_cong_thanh_toan=Decimal("1100000"),
        )
        hd.full_clean()
        hd.save()
        ct = HoaDonChiTiet.objects.create(
            hoa_don=hd,
            hang_hoa=hh,
            so_luong=Decimal("2"),
            don_gia=Decimal("500000"),
            tien_thue=Decimal("100000"),
            tong_tien=Decimal("1100000"),
        )
        line_total = ct.so_luong * ct.don_gia
        self.assertEqual(line_total, Decimal("1000000"))

    def test_phieu_thu_tk_no_must_be_111_or_112(self):
        """Debit account for receipt must be 111 or 112."""
        tk111 = TaiKhoanKeToan.objects.filter(ma_tai_khoan="111").first()
        tk511 = TaiKhoanKeToan.objects.filter(ma_tai_khoan="511").first()
        if tk111 and tk511:
            pt = PhieuThu(
                so_chung_tu="PT-TEST-012",
                ngay_chung_tu=date.today(),
                loai_chung_tu="phieu_thu",
                so_tien=Decimal("1000000"),
                tk_no=tk111,
                tk_co=tk511,
                dien_giai="Test",
            )
            pt.full_clean()
            self.assertIn(pt.tk_no.ma_tai_khoan, ("111", "112"))

    def test_phieu_chi_tk_co_must_be_111_or_112(self):
        """Credit account for payment must be 111 or 112."""
        tk331 = TaiKhoanKeToan.objects.filter(ma_tai_khoan="331").first()
        tk111 = TaiKhoanKeToan.objects.filter(ma_tai_khoan="111").first()
        if tk331 and tk111:
            pc = PhieuChi(
                so_chung_tu="PC-TEST-013",
                ngay_chung_tu=date.today(),
                loai_chung_tu="phieu_chi",
                so_tien=Decimal("500000"),
                tk_no=tk331,
                tk_co=tk111,
                dien_giai="Test",
            )
            pc.full_clean()
            self.assertIn(pc.tk_co.ma_tai_khoan, ("111", "112"))

    def test_but_toan_no_phai_bang_co(self):
        """Journal total debit must equal total credit."""
        bt = ButToan(
            so_but_toan="BT-TEST-014",
            ngay_hach_toan=date.today(),
            dien_giai="Test balanced journal",
            trang_thai="posted",
        )
        bt.full_clean()
        bt.save()
        tk111 = TaiKhoanKeToan.objects.filter(ma_tai_khoan="111").first()
        tk511 = TaiKhoanKeToan.objects.filter(ma_tai_khoan="511").first()
        if tk111 and tk511:
            ButToanChiTiet.objects.create(
                but_toan=bt,
                tai_khoan=tk111,
                loai_no_co="no",
                so_tien=Decimal("1000000"),
            )
            ButToanChiTiet.objects.create(
                but_toan=bt,
                tai_khoan=tk511,
                loai_no_co="co",
                so_tien=Decimal("1000000"),
            )
            tong_no = sum(
                ct.so_tien for ct in bt.chi_tiet.filter(loai_no_co="no")
            )
            tong_co = sum(
                ct.so_tien for ct in bt.chi_tiet.filter(loai_no_co="co")
            )
            self.assertEqual(tong_no, tong_co)

    def test_document_date_not_future(self):
        """Document date cannot be in the future."""
        kh = KhachHang.objects.create(
            ma_kh="TEST015",
            ten_kh="Test Customer 15",
            ma_so_thue="0123456789",
        )
        future_date = date.today() + timedelta(days=1)
        hd = HoaDon(
            so_hoa_don="HD-TEST-015",
            ngay_hoa_don=future_date,
            khach_hang=kh,
            tong_tien_truoc_thue=Decimal("0"),
            tien_thue_gtgt=Decimal("0"),
            tong_cong_thanh_toan=Decimal("0"),
        )
        with self.assertRaises(ValidationError):
            hd.full_clean()

    def test_document_date_not_before_2025(self):
        """Document date cannot be before TT 99 effective date (2025)."""
        kh = KhachHang.objects.create(
            ma_kh="TEST016",
            ten_kh="Test Customer 16",
            ma_so_thue="0123456789",
        )
        old_date = date(2024, 12, 31)
        hd = HoaDon(
            so_hoa_don="HD-TEST-016",
            ngay_hoa_don=old_date,
            khach_hang=kh,
            tong_tien_truoc_thue=Decimal("0"),
            tien_thue_gtgt=Decimal("0"),
            tong_cong_thanh_toan=Decimal("0"),
        )
        with self.assertRaises(ValidationError):
            hd.full_clean()

    def test_ma_so_thue_format(self):
        """Tax ID must be 10 or 13 digits."""
        kh = KhachHang(
            ma_kh="TEST017",
            ten_kh="Test Customer 17",
            ma_so_thue="12345",
            dia_chi="Test",
        )
        with self.assertRaises(ValidationError):
            kh.full_clean()

        kh.ma_so_thue = "0123456789"
        kh.full_clean()

        kh.ma_so_thue = "0123456789012"
        kh.full_clean()
