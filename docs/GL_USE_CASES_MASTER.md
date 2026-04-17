# GL ACCOUNTING SYSTEM - MASTER USE CASE DOCUMENT
*Thông tư 99/2025/TT-BTC | Consolidated: April 2026*

---

## TABLE OF CONTENTS

1. [Overview](#1-overview)
2. [Core Modules (S01-S06, P01-P05)](#2-core-modules)
3. [Cash & Bank (T01-T22, B01-B08)](#3-cash--bank)
4. [Inventory (I01-I07)](#4-inventory)
5. [Fixed Assets (A01-A06)](#5-fixed-assets)
6. [Payroll (L01-L07)](#6-payroll)
7. [Tax (X01-X05)](#7-tax)
8. [Period Closing (G01-G05)](#8-period-closing)
9. [Books & Registers](#9-books--registers)
10. [Financial Reports](#10-financial-reports)
11. [E-Invoice (EI01-EI07)](#11-e-invoice)

---

## 1. OVERVIEW

| Metric | Value |
|--------|-------|
| Total Use Cases | 100+ |
| Total Services | 28 |
| Total Tests | 331 |
| Compliance | TT99/2025 |

### Document Index

| Module | File | Status |
|--------|------|--------|
| Sales | `use_cases/sales_use_cases.md` | ✅ |
| Purchase | `use_cases/purchase_use_cases.md` | ✅ |
| Cash | `use_cases/cash_use_cases.md` | ✅ |
| Bank | `use_cases/bank_use_cases.md` | ✅ |
| Inventory | `use_cases/inventory_use_cases.md` | ✅ |
| Fixed Assets | `use_cases/fixed_asset_use_cases.md` | ✅ |
| Payroll | `use_cases/payroll_use_cases.md` | ✅ |
| Tax | `TAX_USE_CASES.md` | ✅ |
| COA | `use_cases/coa_use_cases.md` | ✅ |

---

## 2. CORE MODULES

### S01-S06: Sales & Revenue

| Code | Use Case | Định khoản |
|------|---------|------------|
| S01 | Doanh thu bán hàng | Nợ 111,112 / Có 511 + 333 |
| S02 | Giảm giá hàng bán | Nợ 521 / Có 111,112 |
| S03 | Trả lại hàng bán | Nợ 531 / Có 111,112 |
| S04 | Chiết khấu thanh toán | Nợ 521 / Có 111,112 |
| S05 | Doanh thu dịch vụ | Nợ 111,112 / Có 511 |
| S06 | Kết chuyển doanh thu | Nợ 511 / C� 911 |

**Service:** `SalesService.cs` (18 tests)

### P01-P05: Purchase & Inventory

| Code | Use Case | Định khoản |
|------|---------|------------|
| P01 | Mua hàng nhập kho | Nợ 156,133 / Có 111,112,331 |
| P02 | Giảm giá mua hàng | Nợ 111,112,331 / Có 156 |
| P03 | Trả lại hàng mua | Nợ 111,112,331 / Có 156 |
| P04 | Chi phí mua hàng | Nợ 156 / Có 111,112 |
| P05 | Kết chuyển giá vốn | Nợ 632 / Có 156 |

**Service:** `PurchaseService.cs` (15 tests)

---

## 3. CASH & BANK

### T01-T22: Cash (Quỹ Tiền Mặt)

| Code | Use Case | Định khoản |
|------|---------|------------|
| T01 | Rút tiền NH về quỹ | Nợ 111 / Có 112 |
| T02 | Thu bán hàng nhập quỹ | Nợ 111 / Có 511 + 333 |
| T03 | Chi mua hàng | Nợ 156,133 / Có 111 |
| T04 | Nộp tiền vào NH | Nợ 112 / Có 111 |
| T05 | Chi lương TM | Nợ 334 / Có 111 |
| T06 | Chi tạm ứng | Nợ 141 / Có 111 |
| T07 | Thu hồi nợ | Nợ 111 / Có 131 |
| T08 | Thừa tiền (KK) | Nợ 111 / Có 338 |
| T09 | Thiếu tiền (KK) | Nợ 138 / Có 111 |
| T10 | Nhận vốn góp | Nợ 111 / Có 411 |
| T11 | Nhận ký quỹ | Nợ 111 / Có 344 |
| T12 | Hoàn trả ký quỹ | Nợ 344 / Có 111 |
| T13 | Chi phí KD | Nợ 6xx,133 / Có 111 |
| T14 | Đi vay | Nợ 111 / Có 341,311 |
| T15 | Bán đầu tư | Nợ 111 / Có 121 + 515 |
| T16 | Mua đầu tư | Nợ 121 / Có 111 |
| T17 | Thu ngoại tệ | Nợ 1112 / Có 511 |
| T18 | Thu nợ ngoại tệ | Nợ 1112 / Có 131 |
| T19 | Xuất ngoại tệ | Nợ 156 / Có 1112 |
| T20 | Bán ngoại tệ | Nợ 1111 / Có 1112 |
| T21 | Ủng trước NCC | Nợ 331 / Có 1112 |
| T22 | Thu đặt trước | Nợ 1112 / Có 131 |

**Service:** `CashService.cs` (22 methods, 25 tests)

### B01-B08: Bank (Ngân Hàng)

| Code | Use Case | Định khoản |
|------|---------|------------|
| B01 | Chuyển tiền thanh toán | Nợ 331 / Có 112 |
| B02 | Nhận tiền vào NH | Nợ 112 / Có 511,131 |
| B03 | Thanh toán L/C | Nợ 331 / Có 112 |
| B04 | Chiết khấu | Nợ 112 / Có 131 |
| B05 | Vay ngắn hạn | Nợ 112 / Có 341 |
| B06 | Đáo hạn vay | Nợ 341 / Có 112 |
| B07 | Thế chấp TSBĐ | Nợ 112 / Có 341 |
| B08 | Kết chuyển NH | Nợ 112 / Có 111 |

**Service:** `BankService.cs` (11 tests)

---

## 4. INVENTORY

### I01-I07: Inventory Management

| Code | Use Case | Định khoản |
|------|---------|------------|
| I01 | Nhập kho hàng mua | Nợ 156 / Có 331 |
| I02 | Xuất kho hàng bán | Nợ 632 / Có 156 |
| I03 | Chuyển kho nội bộ | Nợ 156(Đ) / Có 156(N) |
| I04 | Kiểm kê kho | Điều chỉnh 156 |
| I05 | Đánh giá HTK | Chênh lệch 156 |
| I06 | Bảng tổng hợp NX | Báo cáo |
| I07 | Kết chuyển GV | Nợ 632 / Có 156 |

**Service:** `InventoryService.cs` (11 tests)

---

## 5. FIXED ASSETS

### A01-A06: Fixed Assets

| Code | Use Case | Định khoản |
|------|---------|------------|
| A01 | Mua TSCĐ | Nợ 211 / Có 111,112,331 |
| A02 | Khấu hao TSCĐ | Nợ 642 / Có 214 |
| A03 | Thanh lý TSCĐ | Điều chỉnh 211,214 |
| A04 | Đánh giá lại TSCĐ | Chênh lệch 411 |
| A05 | Kiểm kê TSCĐ | Điều chỉnh |
| A06 | Chuyển nhượng TSCĐ | Giao dịch 211 |

**Service:** `FixedAssetService.cs` (22 tests)

---

## 6. PAYROLL

### L01-L07: Payroll & Labor

| Code | Use Case | Calculation |
|------|---------|------------|
| L01 | Quản lý HĐ lao động | Entity: LaborContract |
| L02 | Tính lương tháng | Base + Phụ cấp |
| L03 | Tính tăng ca | 150%/200%/300% |
| L04 | Quản lý nghỉ phép | 12-19 days/year |
| L05 | Tính BHXH | 17.5% (17+1%) |
| L06 | Tính thuế TNCN | 5%-35% lũy tiến |
| L07 | Trợ cấp thôi việc | 0.5 tháng/năm |

**Service:** `PayrollCalculationService.cs` (35 tests)

---

## 7. TAX

### X01-X05: Tax Management

| Code | Use Case | Account |
|------|---------|---------|
| X01 | Kê khai VAT đầu vào | 1331 |
| X02 | Kê khai VAT đầu ra | 33311 |
| X03 | Khấu trừ thuế TNCN | 3335 |
| X04 | Quyết toán TNDN | 8211 |
| X05 | Hóa đơn điện tử | EI01-EI07 |

**Service:** `TaxService.cs` (12 tests)

---

## 8. PERIOD CLOSING

### G01-G05: Period Closing

| Code | Use Case | Định khoản |
|------|---------|------------|
| G01 | Kết chuyển DT | Nợ 511 / Có 911 |
| G02 | Kết chuyển CP | Nợ 911 / Có 632,641,642 |
| G03 | Xác định KQKD | Nợ 911 / Có 421 |
| G04 | Kết chuyển LN | Nợ 421 / Có 4212 |
| G05 | Central Posting | GL Entries |

**Service:** `TransactionService.cs` + `GLCentralPostingService.cs`

---

## 9. BOOKS & REGISTERS

### General Journal (Sổ Nhật Ký Chung)

| Code | Use Case |
|------|---------|
| NKC-01 | Ghi sổ NKC |
| NKC-02 | Ghi chênh lệch tỷ giá |
| NKC-03 | Đối chiếu Sổ Cái |

### General Ledger (Sổ Cái)

| Code | Use Case |
|------|---------|
| GL-01 | Lập Sổ Cái theo TK |
| GL-02 | Ghi Số dư đầu kỳ |
| GL-03 | Tính PS và Số dư cuối |
| GL-04 | In Sổ Cái |

### Trial Balance (Bảng CĐPS)

| Code | Use Case |
|------|---------|
| TB-01 | Lập Bảng CĐPS |
| TB-02 | Kiểm tra đối chiếu |
| TB-03 | In Bảng CĐPS |

### Subsidiary Ledgers (Sổ Chi Tiết)

| Code | Use Case | Account |
|------|---------|---------|
| SL-01 | Sổ chi tiết 131 | 131 |
| SL-02 | Sổ chi tiết 331 | 331 |
| SL-03 | Sổ chi tiết 156 | 156 |

---

## 10. FINANCIAL REPORTS

### B01-B09: Financial Statements

| Report | Code | Description |
|--------|------|-------------|
| Bảng CĐKT | B01-DN | Balance Sheet |
| BCKQHĐKD | B02-DN | Income Statement |
| Lưu chuyển TM | B03-DN | Cash Flow |
| Tìn hình HTK | B05-DN | Inventory |
| TSCĐ | B06-DN | Fixed Assets |
| Thuế | B07-DN | Tax |
| BHXH | B08-DN | Social Insurance |
| Thuyết minh | B09-DN | Notes |

---

## 11. E-INVOICE

### EI01-EI07: Electronic Invoice

| Code | Use Case |
|------|---------|
| EI01 | Tạo hóa đơn điện tử |
| EI02 | Ký số hóa đơn |
| EI03 | Gửi hóa đơn qua mạng |
| EI04 | Nhận phản hồi từ TCT |
| EI05 | Hiển thị hóa đơn |
| EI06 | Hủy hóa đơn điện tử |
| EI07 | Báo cáo tổng hợp HĐĐT |

---

## IMPLEMENTATION STATUS

| Module | Tests | Status |
|--------|-------|--------|
| SalesService | 18 | ✅ Pass |
| PurchaseService | 15 | ✅ Pass |
| CashService | 25 | ✅ Pass |
| BankService | 11 | ✅ Pass |
| InventoryService | 11 | ✅ Pass |
| FixedAssetService | 22 | ✅ Pass |
| PayrollCalculationService | 35 | ✅ Pass |
| TaxService | 12 | ✅ Pass |
| TransactionService | 8 | ✅ Pass |
| GLCentralPostingService | 6 | ✅ Pass |
| CostAccountingService | 6 | ✅ Pass |
| SubsidiaryLedgerService | 9 | ✅ Pass |

**Total: 331 tests passing**

---

## REFERENCE FILES

| Document | Path |
|----------|------|
| Master Use Cases | `docs/GL_USE_CASES_MASTER.md` |
| Consolidated | `docs/GL_USE_CASES_CONSOLIDATED.md` |
| Use Cases Index | `docs/USE_CASES_INDEX.md` |
| Gap Analysis | `docs/GAP_ANALYSIS.md` |
| Implementation Roadmap | `docs/roadmaps/implementation_roadmap.md` |
| Production Readiness | `docs/PRODUCTION_READINESS.md` |

### Inventory Costing (I05a-I05f)
- Source: `docs/use_cases/usecases_inventory_costing_20260417.md`
- Tests: `tests/Domain.Tests/InventoryCostingMethodTests.cs`

---

*Last Updated: April 2026*
*Based on Thông tư 99/2025/TT-BTC*