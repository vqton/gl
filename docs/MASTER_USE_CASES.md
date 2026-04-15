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
| `use_cases/cash_use_cases.md` | Cash & Bank | T01-T05 |
| `use_cases/tax_use_cases.md` | Tax | X01-X05 |
| `use_cases/fixed_asset_use_cases.md` | Fixed Assets | A01-A06 |
| `use_cases/period_closing_use_cases.md` | Period Closing | G01-G08 |

---

## 📊 GAP ANALYSIS & IMPLEMENTATION STATUS

| Module | Use Cases | Implemented | Missing | Priority |
|--------|-----------|-------------|---------|----------|
| **COA** | C01-C09 | 3 | C02-C04, C06, C08-C09 | P1 |
| **Sales** | S01-S06 | 0 | All 6 | P0 |
| **Purchase** | P01-P05 | 0 | All 5 | P0 |
| **Cash** | T01-T05 | 0 | All 5 | P0 |
| **Tax** | X01-X05 | 0 | All 5 | P1 |
| **Fixed Assets** | A01-A06 | 6 | A06 | P2 |
| **Payroll** | L01-L07 | 7 | - | ✅ Done |
| **Period Closing** | G01-G08 | 4 | G05-G08 | P2 |

---

## 🎯 IMPLEMENTATION PRIORITY (Stakeholder Aligned)

| Phase | Module | Week | Deliverables |
|-------|--------|------|--------------|
| **Phase 2** | Sales (S01-S06) | 3 | SalesService, Returns, Discounts |
| **Phase 2** | Purchase (P01-P05) | 4 | PurchaseService, Inventory costing |
| **Phase 3** | Cash & Bank (T01-T05) | 5 | CashService, Reconciliation |
| **Phase 3** | Tax (X01-X05) | 6 | VATService, Withholding |
| **Phase 4** | COA Services (C01-C09) | 7 | Validation, Import/Export |
| **Phase 4** | Period Closing (G05-G08) | 8 | Provisions, FX, Final closing |

---

## 🗂️ PART 1: CHART OF ACCOUNTS (COA)

### 📌 C01 — CREATE ACCOUNT
- **Tác nhân:** Kế toán trưởng
- **Mục tiêu:** Tạo tài khoản kế toán mới trong hệ thống TT99
- **Luồng chính:**
  1. Nhập mã tài khoản (111, 211, 511...)
  2. Nhập tên tài khoản
  3. Chọn loại (tài sản, nợ phải trả, vốn chủ, doanh thu, chi phí)
  4. Chọn số dư bình thường (Nợ/Có)
  5. Chọn tài khoản cha (nếu có)
- **Luồng thay thế:** Mã đã tồn tại → Báo lỗi, yêu cầu mã mới
- **Postconditions:** Tài khoản được lưu vào Database

### 📌 C02 — UPDATE ACCOUNT
- **Tác nhân:** Kế toán trưởng
- **Mục tiêu:** Cập nhật thông tin tài khoản
- **Luồng chính:** Chỉnh sửa tên, mô tả, cha
- **⚠️ QUAN TRỌNG:** Không được đổi mã nếu đã phát sinh số dư
- **Postconditions:** Thông tin cập nhật

### 📌 C03 — DELETE ACCOUNT
- **Tác nhân:** Kế toán trưởng
- **Mục tiêu:** Xóa tài khoản không sử dụng
- **Luồng chính:**
  1. Kiểm tra không có phát sinh
  2. Kiểm tra không có tài khoản con
  3. Xóa khỏi Database
- **Postconditions:** Tài khoản được xóa

### 📌 C04 — GET ACCOUNT TREE
- **Tác nhân:** All users
- **Mục tiêu:** Hiển thị cây tài khoản theo cấp
- **Postconditions:** Trả về cây phân cấp

### 📌 C05 — VALIDATE ACCOUNT (for journal)
- **Tác nhân:** System (auto)
- **Mục tiêu:** Kiểm tra tài khoản hợp lệ trước khi hạch toán
- **Luồng chính:**
  1. Tìm tài khoản theo mã
  2. Kiểm tra tồn tại
  3. Kiểm tra cho phép hạch toán (không phải cha)
- **Postconditions:** Trả về true/false

### 📌 C06 — IMPORT COA (CSV)
### 📌 C07 — EXPORT COA

---

## 🗂️ PART 2: SALES & REVENUE (S01-S06)

### 📌 S01 — BÁN HÀNG TIỀN MẶT
- **Tác nhân:** Kế toán, thu ngân
- **Mục tiêu:** Ghi nhận doanh thu khi thu tiền ngay
- **Luồng chính:**
  1. Nhận hóa đơn VAT
  2. Kiểm tra thông tin (mã số thuế, ngày, số tiền)
  3. Định khoản: Nợ 111/112 / Có 511 / Có 33311
  4. Cập nhật sổ cái
- **Luồng thay thế:**
  - Hóa đơn không hợp lệ → Yêu cầu xuất điều chỉnh
  - Sai tài khoản → Điều chỉnh trước khi ghi
- **Postconditions:** Tổng Nợ = Tổng Có; Sổ 511 tăng

### 📌 S02 — BÁN HÀNG CHỊU (CÔNG NỢ)
- **Tác nhân:** Kế toán, sales
- **Mục tiêu:** Ghi nhận doanh thu và công nợ phải thu
- **Luồng chính:** Nợ 131 / Có 511 / Có 33311
- **Postconditions:** Sổ 131 tăng; Cập nhật aging

### 📌 S03 — GHI NHẬN GIÁ VỐN HÀNG BÁN (COGS)
- **Tác nhân:** Kế toán, kho
- **Mục tiêu:** Ghi nhận chi phí giá vốn khi giao hàng
- **Luồng chính:** Nợ 632 / Có 156/155
- **⚠️ CASCADE:** Tự động cập nhật thẻ kho

### 📌 S04 — HÀNG BÁN BỊ TRẢ L���I
- **Tác nhân:** Kế toán, kinh doanh, kho
- **Mục tiêu:** Điều chỉnh doanh thu khi trả hàng
- **Luồng chính:**
  - Nợ 5212 / Có 131/111
  - Nợ 156/155 / Có 632 (điều chỉnh giá vốn)

### 📌 S05 — GIẢM GIÁ HÀNG BÁN
- **Tác nhân:** Kế toán, kinh doanh
- **Mục tiêu:** Giảm giá cho khách do hàng lỗi
- **Luồng chính:** Nợ 5211 / Có 131/111

### 📌 S06 — CHIẾT KHẤU THANH TOÁN
- **Tác nhân:** Kế toán
- **Mục tiêu:** Ghi nhận chiết khấu khi khách trả trước
- **Luồng chính:** Nợ 111 / Nợ 5213 / Có 131

---

## 🗂️ PART 3: PURCHASE & INVENTORY (P01-P05)

### 📌 P01 — MUA HÀNG CHỊU (CÔNG NỢ PHẢI TRẢ)
- **Tác nhân:** Kế toán, mua hàng
- **Luồng chính:** Nợ 156/152 / Nợ 1331 / Có 331

### 📌 P02 — MUA HÀNG TIỀN MẶT
- **Tác nhân:** Kế toán
- **Luồng chính:** Nợ 156/152 / Nợ 1331 / Có 111/112

### 📌 P03 — XUẤT KHO (Xuất NVL/Công cụ)
- **Tác nhân:** Thủ kho
- **Luồng chính:** Nợ 621/627/641/642 / Có 152/153

### 📌 P04 — KIỂM KÊ KHO
### 📌 P05 — HÀNG MUA TRẢ LẠI

---

## 🗂️ PART 4: CASH & BANK (T01-T05)

### 📌 T01 — THANH TOÁN CHO NHÀ CUNG CẤP
- **Luồng chính:** Nợ 331 / Có 111/112

### 📌 T02 — THU TIỀN TỪ KHÁCH HÀNG
- **Luồng chính:** Nợ 111/112 / Có 131

### 📌 T03 — CHUYỂN KHOẢN NGÂN HÀNG
- **Luồng chính:** Nợ 112 / Có 111

### 📌 T04 — QUỸ TIỀN MẶT (Thủ quỹ)
### 📌 T05 — ĐỐI CHIẾU NGÂN HÀNG

---

## 🗂️ PART 5: TAX (X01-X05)

### 📌 X01 — KÊ KHAI VAT ĐẦU VÀO
- **Tác nhân:** Kế toán thuế
- **Luồng chính:** Kê khai 1331 hàng tháng

### 📌 X02 — KÊ KHAI VAT ĐẦU RA
- **Luồng chính:** Kê khai 33311 hàng tháng

### 📌 X03 — KHẤU TRỪ THUẾ TNCN
### 📌 X04 — QUYẾT TOÁN THUẾ TNDN
### 📌 X05 — HÓA ĐƠN ĐIỆN TỬ

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

| Module | Implemented | Missing | Priority |
|--------|-----------|---------|----------|
| COA | Entity | Service (validate) | Medium |
| Sales S01-S06 | Entity | Service (S04-S06) | High |
| Purchase P01-P05 | Entity | Service (P03-P05) | High |
| Cash T01-T05 | Entity | Service (T04-T05) | Medium |
| Tax X01-X05 | Entity | All services | High |
| Fixed Assets | ✅ Full | - | Done |
| Payroll | ✅ Full | - | Done |
| Period Closing | ✅ G01-G04 | G05-G08 | Low |

---

## 📋 IMPLEMENTATION ROADMAP

| Phase | Module | Timeline | Deliverables |
|-------|--------|----------|------------|
| Phase 2 | Sales S01-S06 | Week 3 | SalesService.cs |
| Phase 3 | Purchase P01-P05 | Week 5 | PurchaseService.cs |
| Phase 3 | Cash T01-T05 | Week 6 | CashService.cs |
| Phase 4 | Tax X01-X05 | Week 8 | TaxService.cs |

---

## 📋 FILE REFERENCE

| Document | Location |
|----------|----------|
| Master Use Cases | This document |
| Sales Detail | docs/use_cases/sales_use_cases.md |
| Payroll Detail | docs/use_cases/laodong_tienluong.md |
| COA Detail | docs/use_cases/coa_use_cases.md |
| TT99 Full Specs | docs/core_use_cases_TT99_2025_updated.md |

---

*Last Updated: April 2026*  
*Consolidated from: COA, Sales, Payroll, Period Closing docs*