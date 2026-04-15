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
| `use_cases/cash_use_cases.md` | Cash & Bank | T01-T22 | ✅ Complete |

---

## 🗂️ PART 4: CASH & BANK (T01-T22) ✅ COMPLETE

### 📌 T01 — THANH TOÁN CHO NHÀ CUNG CẤP
- **Luồng chính:** Nợ 331 / Có 111/112

### 📌 T02 — THU TIỀN TỪ KHÁCH HÀNG
- **Luồng chính:** Nợ 111/112 / Có 131

### 📌 T03 — CHUYỂN KHOẢN NGÂN HÀNG
- **Luồng chính:** Nợ 112 / Có 111

### 📌 T04 — QUỸ TIỀN MẶT (Thủ quỹ)
### 📌 T05 — ĐỐI CHIẾU NGÂN HÀNG

> ℹ️ **Detail:** Full T01-T22 use cases documented in `use_cases/cash_use_cases.md`

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
| Cash T01-T22 | ✅ Full | - | Done |
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