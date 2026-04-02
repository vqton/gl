"""Constants for Payroll (M7)."""

from decimal import Decimal

# BHXH rates 2026 (per Nghị định 58/2020/NĐ-CP)
# Employee contribution
BHXT_NLD_BHXH = Decimal("0.08")  # 8% BHXH
BHXT_NLD_BHYT = Decimal("0.015")  # 1.5% BHYT
BHXT_NLD_BHTN = Decimal("0.01")  # 1% BHTN

# Employer contribution
BHXT_DN_BHXH = Decimal("0.175")  # 17.5% BHXH
BHXT_DN_BHYT = Decimal("0.03")  # 3% BHYT
BHXT_DN_BHTN = Decimal("0.01")  # 1% BHTN
BHXT_DN_BHTNLĐ_BNN = Decimal("0.005")  # 0.5% BHTNLĐ-BNN

# Total rates
BHXT_TONG_NLD = BHXT_NLD_BHXH + BHXT_NLD_BHYT + BHXT_NLD_BHTN  # 10.5%
BHXT_TONG_DN = BHXT_DN_BHXH + BHXT_DN_BHYT + BHXT_DN_BHTN + BHXT_DN_BHTNLĐ_BNN  # 22%

# Personal income tax brackets (Thuế TNCN - Biểu lũy tiến)
THUE_TNCN_BRACKETS = [
    (Decimal("0"), Decimal("5000000"), Decimal("0.05"), Decimal("0")),
    (Decimal("5000000"), Decimal("10000000"), Decimal("0.10"), Decimal("250000")),
    (Decimal("10000000"), Decimal("18000000"), Decimal("0.15"), Decimal("750000")),
    (Decimal("18000000"), Decimal("32000000"), Decimal("0.20"), Decimal("1650000")),
    (Decimal("32000000"), Decimal("52000000"), Decimal("0.25"), Decimal("3250000")),
    (Decimal("52000000"), Decimal("80000000"), Decimal("0.30"), Decimal("5850000")),
    (Decimal("80000000"), None, Decimal("0.35"), Decimal("9850000")),
]

# Personal deduction (Giảm trừ gia cảnh)
GIAM_TRU_BAN_THAN = Decimal("11000000")  # 11 million/month
GIAM_TRU_PHU_THUOC = Decimal("4400000")  # 4.4 million/dependent

# Salary cap for BHXH (20x base salary)
LUONG_CO_BAN = Decimal("2340000")  # Base salary 2026
MAX_LUONG_BHXH = LUONG_CO_BAN * Decimal("20")  # 46,800,000
