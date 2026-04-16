# 📋 GL ACCOUNTING SYSTEM — MASTER USE CASE DOCUMENT
*Consolidated: April 2026 | Based on TT99/2025*

---

## 📁 DOCUMENT STRUCTURE

| File | Module | Coverage |
|------|--------|----------|
| `MASTER_USE_CASES.md` | **This file** | Consolidated overview |
| `use_cases/sales_use_cases.md` | Sales & Revenue | S01-S06 |
| `use_cases/laodong_tienluong.md` | Payroll & Labor | L01-L07 |
| `use_cases/coa_use_cases.md` | Chart of Accounts | C01-C09 |
| `use_cases/purchase_use_cases.md` | Purchase & Inventory | P01-P05 |
| `use_cases/cash_use_cases.md` | Cash & Bank | T01-T22 ✅ Complete |

---

## 🗂️ PART 4: CASH & BANK (T01-T22) ✅ COMPLETE

| T# | Use Case | Định khoản |
|----|----------|------------|
| T01 | Rút tiền ngân hàng về quỹ | Nợ 111 / Có 112 |
| T02 | Thu tiền bán hàng nhập quỹ | Nợ 111 / Có 511 + Có 333 |
| T03 | Chi tiền mua hàng | Nợ 156,133 / Có 111 |
| T04 | Nộp tiền vào ngân hàng | Nợ 112 / Có 111 |
| T05 | Chi lương tiền mặt | Nợ 334 / Có 111 |
| T06 | Chi tạm ứng | Nợ 141 / Có 111 |
| T07 | Thu hồi nợ phải thu | Nợ 111 / Có 131 |
| T08 | Thừa tiền mặt (kiểm kê) | Nợ 111 / Có 338 |
| T09 | Thiếu tiền mặt (kiểm kê) | Nợ 138 / Có 111 |
| T10 | Nhận vốn góp | Nợ 111 / Có 411 |
| T11 | Nhận ký quỹ | Nợ 111 / Có 344 |
| T12 | Hoàn trả ký quỹ | Nợ 344 / Có 111 |
| T13 | Chi phí kinh doanh | Nợ 6xx,133 / Có 111 |
| T14 | Đi vay | Nợ 111 / Có 341/311 |
| T15 | Bán đầu tư | Nợ 111 / Có 121 + 515/635 |
| T16 | Mua đầu tư | Nợ 121 / Có 111 |
| T17 | Thu ngoại tệ (bán hàng) | Nợ 1112 / Có 511 |
| T18 | Thu hồi nợ ngoại tệ | Nợ 1112 / Có 131 |
| T19 | Xuất ngoại tệ mua hàng | Nợ 156 / Có 1112 |
| T20 | Bán ngoại tệ | Nợ 1111 / Có 1112 |
| T21 | Ứng trước NCC ngoại tệ | Nợ 331 / Có 1112 |
| T22 | Thu tiền đặt trước (ngoại tệ) | Nợ 1112 / Có 131 |

> **Implementation:** `CashService.cs` - 22 methods, 25 tests passing

---

## 🗂️ PART 5: TAX (X01-X05) ✅ COMPLETE

### 📌 X01 — KÊ KHAI VAT ĐẦU VÀO
- **Tác nhân:** Kế toán thuế
- **Luồng chính:** Kê khai 1331 hàng tháng

### 📌 X02 — KÊ KHAI VAT ĐẦU RA
- **Luồng chính:** Kê khai 33311 hàng tháng

### 📌 X03 — KHẤU TRỪ THUẾ TNCN
### 📌 X04 — QUYẾT TOÁN THUẾ TNDN
### 📌 X05 — HÓA ĐƠN ĐIỆN TỬ

> **Implementation:** `TaxService.cs` - 8 methods, 12 tests passing

---

## 🗂️ PART 6: FIXED ASSETS (A01-A06) ✅ COMPLETE

### 📌 A01 — THÊM TSCĐ MỚI
### 📌 A02 — TÍNH KHẤU HAO
### 📌 A03 — CHUYỂN GIAO TSCĐ
### 📌 A04 — THANH LÝ TSCĐ
### 📌 A05 — ĐÁNH GIÁ LẠI TSCĐ
### 📌 A06 — KIỂM KÊ TSCĐ

---

## 🗂️ PART 7: PAYROLL (L01-L07) ✅ COMPLETE

### 📌 L01 — QUẢN LÝ HỢP ĐỒNG LAO ĐỘNG
### 📌 L02 — TÍNH LƯƠNG THÁNG
### 📌 L03 — TÍNH TĂNG CA
### 📌 L04 — QUẢN LÝ NGHỈ PHÉP
### 📌 L05 — TRỢ CẤP THÔI VIỆC
### 📌 L06 — KÊ KHAI BHXH
### 📌 L07 — THANG BẢNG LƯƠNG

---

## 🗂️ PART 8: PERIOD CLOSING (G01-G04) ✅ COMPLETE

### 📌 G01 — KẾT CHUYỂN DOANH THU (511→911)
### 📌 G02 — KẾT CHUYỂN CHI PHÍ (632,641,642→911)
### 📌 G03 — KẾT CHUYỂN LỢI NHUẬN (911→4212)
### 📌 G04 — PHÂN BỔ CHI PHÍ TRẢ TRƯỚC (242)

---

## 📋 GAP ANALYSIS

| Module | Implemented | Status | Priority |
|--------|-----------|--------|----------|
| COA Validation | ✅ Full | Service + Tests | Done |
| **Sales S01-S06** | ✅ Full | - | Done |
| **Purchase P01-P05** | ✅ Full | - | Done |
| Cash T01-T22 | ✅ Full | - | Done |
| **Tax X01-X05** | ✅ Full | - | Done |
| **Bank B01-B08** | ✅ Full | - | Done |
| **Inventory I01-I07** | ✅ Full | - | Done |
| Fixed Assets | ✅ Full | - | Done |
| Payroll | ✅ Full | - | Done |
| Period Closing | ✅ G01-G04 | - | Done |
| **GL Central Posting** | ✅ G05 | New | Done |
| **Cost Accounting** | ✅ C01 | New | Done |
| **Subsidiary Ledgers** | ✅ S01-S03 | New | Done |

---

## 📋 IMPLEMENTATION ROADMAP

| Phase | Module | Timeline | Deliverables |
|-------|--------|----------|------------|
| Phase 2 | Sales S01-S06 | Week 3 | SalesService.cs |
| Phase 3 | Purchase P01-P05 | Week 5 | PurchaseService.cs |
| Phase 4 | Tax X01-X05 | Week 8 | TaxService.cs (12 tests) |
| Phase 5 | COA Validation | Week 11 | CoaValidationService.cs (19 tests) |
| Phase 6 | Period Closing G05-G08 | TBD | TBD |

---

## 📋 FILE REFERENCE

| Document | Location |
|----------|----------|
| Master Use Cases | This document |
| Complete Use Cases | docs/GL_USE_CASES_COMPLETE.md |
| Sales Detail | docs/use_cases/sales_use_cases.md |
| Payroll Detail | docs/use_cases/laodong_tienluong.md |
| COA Detail | docs/use_cases/coa_use_cases.md |
| Cash Detail | docs/use_cases/cash_use_cases.md |
| Bank Detail | docs/use_cases/bank_use_cases.md |
| Inventory Detail | docs/use_cases/inventory_use_cases.md |
| TT99 Full Specs | docs/core_use_cases_TT99_2025_updated.md |

---

## 📋 NEW SERVICES (April 2026)

| Service | File | Tests | Account Codes |
|---------|------|-------|--------------|
| GLCentralPostingService | src/Application/Services/GLCentralPostingService.cs | 6 | All |
| CostAccountingService | src/Application/Services/CostAccountingService.cs | 6 | 154, 631 |
| SubsidiaryLedgerService | src/Application/Services/SubsidiaryLedgerService.cs | 9 | 131, 331, 156 |

---

*Last Updated: April 2026*  
*Consolidated from: COA, Sales, Payroll, Cash, Period Closing docs*