"""Constants for Vietnamese SME Accounting System."""

from decimal import Decimal

# VAT rates per Thông tư 99/2025/TT-BTC
THUE_SUAT_GTGT = {
    "0": Decimal("0"),
    "5": Decimal("0.05"),
    "8": Decimal("0.08"),
    "10": Decimal("0.10"),
}

THUE_SUAT_GTGT_2026 = [
    ("0", "0% - Không chịu thuế"),
    ("5", "5% - Nông, thủy sản,.."),
    ("8", "8% - Giảm theo NĐ 70/2025"),
    ("10", "10% - Thuế suất tiêu chuẩn"),
]

# Corporate income tax rates per Luật 67/2025/QH15
THUE_SUAT_TNDN_SME = Decimal("0.15")
THUE_SUAT_TNDN_DEFAULT = Decimal("0.20")
NGUONG_DOANH_THU_SME = Decimal("3000000000")

# Document types
LOAI_CHUNG_TU = [
    ("PT", "Phiếu thu"),
    ("PC", "Phiếu chi"),
    ("HD", "Hóa đơn"),
    ("NK", "Nhập kho"),
    ("XK", "Xuất kho"),
    ("BT", "Bút toán"),
]

# Invoice status
TRANG_THAI_HOA_DON = [
    ("draft", "Nháp"),
    ("issued", "Đã xuất"),
    ("cancelled", "Đã hủy"),
]

# Journal entry status
TRANG_THAI_BUT_TOAN = [
    ("draft", "Nháp"),
    ("posted", "Đã ghi sổ"),
]

# Debit/Credit types
LOAI_NO_CO = [
    ("no", "Nợ"),
    ("co", "Có"),
]

# Inventory status
TRANG_THAI_KHO = [
    ("draft", "Nháp"),
    ("completed", "Hoàn thành"),
    ("cancelled", "Đã hủy"),
]

# Payment methods
HINH_THUC_THANH_TOAN = [
    ("tien_mat", "Tiền mặt"),
    ("chuyen_khoan", "Chuyển khoản"),
]

# Currency
VND = "VND"

# TNCN (Personal Income Tax) brackets per current law
THUE_TNCN_BRACKETS = [
    (Decimal("0"), Decimal("11000000"), Decimal("0.05")),
    (Decimal("11000000"), Decimal("22000000"), Decimal("0.10")),
    (Decimal("22000000"), Decimal("44000000"), Decimal("0.15")),
    (Decimal("44000000"), Decimal("88000000"), Decimal("0.20")),
    (Decimal("88000000"), Decimal("132000000"), Decimal("0.25")),
    (Decimal("132000000"), Decimal("198000000"), Decimal("0.30")),
    (Decimal("198000000"), None, Decimal("0.35")),
]
THUE_TNCN_GIAM_TRU_GIA_CANH = Decimal("11000000")
THUE_TNCN_GIAM_TRU_PHU_THUOC = Decimal("4400000")
