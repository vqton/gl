# GL ACCOUNTING USE CASES - CONSOLIDATED DOCUMENT
*Based on TT99/2025 - Phụ lục 3 & 4*
*Consolidated: 2026-04-16*

---

## 📋 TABLE OF CONTENTS

1. [Overview](#1-overview)
2. [Phase 1: Core Accounting](#phase-1-core-accounting)
3. [Phase 2: Transaction Processing](#phase-2-transaction-processing)
4. [Phase 3: Books & Registers](#phase-3-books--registers)
5. [Phase 4: Compliance & Audit](#phase-4-compliance--audit)
6. [Gap Analysis](#gap-analysis)
7. [Stakeholder Matrix](#stakeholder-matrix)

---

## 1. OVERVIEW

### 1.1 Mapping to TT99/2025 Phụ lục 4

| # | Sổ sách theo TT99 | Use Cases File | Status |
|---|------------------|---------------|--------|
| 01 | Nhật ký - Sổ Cái | usecases_so_nhat_ky_chung | ✅ |
| 02 | Sổ Cái (NKC) | usecases_so_cai_tai_khoan | ✅ |
| 03 | Sổ Quỹ TM | usecases_so_quy_tien_mat | ✅ |
| 04 | Sổ Tiền gửi NH | usecases_so_tien_gui_ngan_hang | ✅ |
| 13 | Bảng CĐPS | usecases_bang_can_doi_so_phat_sinh | ✅ |
| - | Sổ Chi tiết TT | usecases_so_chi_tiet_thanh_toan | ✅ |

### 1.2 Coverage Analysis - ✅ COMPLETE ALL

| Domain | Documents | Coverage | Files |
|--------|-----------|----------|-------|
| **Core GL** | COA | ✅ Complete | coa_use_cases.md |
| **General Journal** | NKC, Sổ Cái | ✅ Complete | usecases_so_nhat_ky_chung, usecases_so_cai_tai_khoan |
| **Cash & Bank** | Quỹ, TGNH | ✅ Complete | usecases_so_quy_tien_mat, usecases_so_tien_gui_ngan_hang |
| **Trial Balance** | Bảng CĐPS | ✅ Complete | usecases_bang_can_doi_so_phat_sinh |
| **Subsidiary Ledger** | AR/AP 131/331 | ✅ Complete | usecases_so_chi_tiet_thanh_toan |
| **Inventory** | I01-I07 | ✅ Complete | inventory_use_cases.md + usecases_inventory_extended |
| **Fixed Assets** | A01-A06 | ✅ Complete | inventory_use_cases.md + usecases_fixed_assets_extended |
| **Payroll** | L01-L07 | ✅ Complete | laodong_tienluong.md + usecases_payroll |
| **Financial Reports** | B01-B09 | ✅ Complete | usecases_bao_cao_tai_chinh |
| **Period Closing** | G01-G04 | ✅ Complete | phase4_audit_period_use_cases.md |

---

## 2. PHASE 1: CORE ACCOUNTING

### 2.1 Chart of Accounts (COA)

| UC Code | Use Case | Actor | Status |
|--------|---------|-------|--------|
| COA-01 | Tạo tài khoản | Kế toán | ✅ |
| COA-02 | Cập nhật tài khoản | Kế toán | ✅ |
| COA-03 | Khóa/Mở khóa TK | Kế toán trưởng | ✅ |
| COA-04 | Xóa tài khoản | Kế toán trưởng | ✅ |
| COA-05 | Validate hạch toán | Hệ thống | ✅ |

**Source:** `coa_use_cases.md`

---

## 3. PHASE 2: TRANSACTION PROCESSING

### 3.1 General Journal (Nhật ký Chung)

| UC Code | Use Case | Actor | Status |
|--------|---------|-------|--------|
| NKC-01 | Ghi sổ Nhật ký chung | Kế toán viên | ✅ |
| NKC-02 | Ghi chênh lệch tỷ giá | Kế toán viên | ✅ |
| NKC-03 | Đối chiếu Sổ Cái | Kế toán trưởng | ✅ |

**Source:** `usecases_so_nhat_ky_chung_tt99_20260416.md`

### 3.2 Cash & Bank

| UC Code | Use Case | Actor | Status |
|--------|---------|-------|--------|
| T01-T22 | Full Cash Process | Kế toán | ✅ |
| B01-B08 | Full Bank Process | Kế toán | ✅ |

**Source:** `usecases_so_quy_tien_mat`, `usecases_so_tien_gui_ngan_hang`, `cash_use_cases.md`, `bank_use_cases.md`

### 3.3 Inventory (Kho) - ✅ COMPLETE

| UC Code | Use Case | Actor | Status | Source |
|--------|---------|-------|--------|--------|
| I01 | Nhập kho hàng mua | Thủ kho, KT | ✅ | inventory_use_cases.md |
| I02 | Xuất kho hàng bán | Thủ kho, KT | ✅ | inventory_use_cases.md |
| I03 | Chuyển kho nội bộ | Thủ kho | ✅ | inventory_use_cases.md |
| I04 | Kiểm kê kho | Thủ kho, KT | ✅ | usecases_inventory_extended |
| I05 | Đánh giá hàng tồn kho | Kế toán | ✅ | usecases_inventory_extended |
| I06 | Lập Bảng tổng hợp NX | Kế toán | ✅ | usecases_inventory_extended |
| I07 | Kết chuyển giá vốn | Kế toán | ✅ | usecases_inventory_extended |

### 3.4 Fixed Assets (TSCĐ) - ✅ COMPLETE

| UC Code | Use Case | Actor | Status | Source |
|--------|---------|-------|--------|--------|
| A01 | Mua TSCĐ | Kế toán | ✅ | inventory_use_cases.md |
| A02 | Khấu hao TSCĐ | Kế toán | ✅ | inventory_use_cases.md |
| A03 | Thanh lý TSCĐ | Kế toán | ✅ | inventory_use_cases.md |
| A04 | Đánh giá lại TSCĐ | KT trưởng | ✅ | usecases_fixed_assets_extended |
| A05 | Kiểm kê TSCĐ | KT, QTHT | ✅ | usecases_fixed_assets_extended |
| A06 | Chuyển nhượng TSCĐ | Kế toán | ✅ | usecases_fixed_assets_extended |

### 3.5 Payroll (Tiền lương) - ✅ COMPLETE

| UC Code | Use Case | Actor | Status | Source |
|--------|---------|-------|--------|--------|
| L01 | Quản lý HĐ lao động | HR | ✅ | laodong_tienluong.md |
| L02 | Tính lương hàng tháng | Kế toán | ✅ | usecases_payroll |
| L03 | Hạch toán tiền lương | Kế toán | ✅ | usecases_payroll |
| L04 | Tính thuế TNCN | Kế toán | ✅ | usecases_payroll |
| L05 | Nộp BHXH, BHYT, BHTN | Kế toán | ✅ | usecases_payroll |
| L06 | Lập Bảng lương | Kế toán | ✅ | usecases_payroll |
| L07 | Chi trả lương | Kế toán | ✅ | usecases_payroll |

---

## 4. PHASE 3: BOOKS & REGISTERS

### 4.1 General Ledger (Sổ Cái)

| UC Code | Use Case | Actor | Status |
|---------|---------|-------|--------|
| GL-01 | Lập Sổ Cái theo TK | Kế toán viên | ✅ |
| GL-02 | Ghi Số dư đầu kỳ | Kế toán viên | ✅ |
| GL-03 | Tính PS và Số dư cuối | Hệ thống | ✅ |
| GL-04 | In Sổ Cái | Kế toán viên | ✅ |

**Source:** `usecases_so_cai_tai_khoan_tt99_20260416.md`

### 4.2 Trial Balance (Bảng CĐPS)

| UC Code | Use Case | Actor | Status |
|---------|---------|-------|--------|
| TB-01 | Lập Bảng CĐPS | Kế toán viên | ✅ |
| TB-02 | Kiểm tra đối chiếu | Kế toán trưởng | ✅ |
| TB-03 | In Bảng CĐPS | Kế toán viên | ✅ |
| TB-04 | Lưu số liệu kỳ sau | Hệ thống | ✅ |

**Source:** `usecases_bang_can_doi_so_phat_sinh_tt99_20260416.md`

### 4.3 Subsidiary Ledger (AR/AP)

| UC Code | Use Case | Actor | Status |
|---------|---------|-------|--------|
| SL-01 | Mở Sổ Chi tiết TT | Kế toán viên | ✅ |
| SL-02 | Ghi Phát sinh trong kỳ | Kế toán viên | ✅ |
| SL-03 | Theo dõi kỳ hạn | Kế toán viên | ✅ |
| SL-04 | Đối chiếu công nợ | KT + KH/NCC | ✅ |
| SL-05 | In Sổ Chi tiết TT | Kế toán viên | ✅ |

**Source:** `usecases_so_chi_tiet_thanh_toan_tt99_20260416.md`

### 4.4 Financial Statements

| UC Code | Use Case | Actor | Status |
|---------|---------|-------|--------|
| B01-DN | Bảng Cân đối kế toán | Kế toán trưởng | ✅ |
| B02-DN | Báo cáo KQKD | Kế toán trưởng | ✅ |
| B03-DN | Báo cáo Lưu chuyển TM | Kế toán trưởng | ✅ |
| B09-DN | Bản thuyết minh | Kế toán trưởng | ✅ |

**Source:** `usecases_bao_cao_tai_chinh_tt99_20260416.md`

---

## 5. PHASE 4: COMPLIANCE & AUDIT

### 5.1 Audit Trail

| UC Code | Use Case | Actor | Status |
|---------|---------|-------|--------|
| AT01 | Log Transaction Entry | Hệ thống | ✅ |
| AT02 | Query Audit History | KT trưởng | ✅ |
| AT03 | Generate Audit Report | KT trưởng | ✅ |

### 5.2 Period Locking

| UC Code | Use Case | Actor | Status |
|---------|---------|-------|--------|
| PL01 | Open Accounting Period | KT trưởng | ✅ |
| PL02 | Close Accounting Period | KT trưởng | ✅ |
| PL03 | Validate Period Before Posting | Hệ thống | ✅ |

### 5.3 Period Closing (G01-G04)

| UC Code | Use Case | Actor | Status |
|---------|---------|-------|--------|
| G01 | Kết chuyển doanh thu | Kế toán | ✅ |
| G02 | Kết chuyển chi phí | Kế toán | ✅ |
| G03 | Xác định KQKD | Kế toán | ✅ |
| G04 | Kết chuyển LN | Kế toán | ✅ |

**Source:** `phase4_audit_period_use_cases.md`

---

## 6. GAP ANALYSIS

### 6.1 Missing Flows (Critical) - ✅ RESOLVED

| # | Domain | Use Case | Priority | Status | File |
|---|--------|---------|----------|--------|------|
| 1 | Inventory | I04 - Kiểm kê kho | HIGH | ✅ | usecases_inventory_extended |
| 2 | Inventory | I05 - Đánh giá HTK | HIGH | ✅ | usecases_inventory_extended |
| 3 | Inventory | I06 - Bảng tổng hợp NX | HIGH | ✅ | usecases_inventory_extended |
| 4 | Inventory | I07 - Kết chuyển GV | HIGH | ✅ | usecases_inventory_extended |
| 5 | FA | A04 - Đánh giá lại TSCĐ | MEDIUM | ✅ | usecases_fixed_assets_extended |
| 6 | FA | A05 - Kiểm kê TSCĐ | MEDIUM | ✅ | usecases_fixed_assets_extended |
| 7 | FA | A06 - Chuyển nhượng TSCĐ | MEDIUM | ✅ | usecases_fixed_assets_extended |

### 6.2 Partial Coverage - ✅ ALL RESOLVED

| # | Domain | Previous Gap | Resolution |
|---|---------|-------------|------------|
| 1 | Inventory | ✅ Now I01-I07 complete |
| 2 | Fixed Assets | ✅ Now A01-A06 complete |
| 3 | Payroll | ✅ Now L01-L07 complete |

### 6.3 Quality Issues

| # | Issue | File | Remediation |
|-------|------|------------|
| 1 | Inconsistent format | Standardize all to template |
| 2 | Mixed language | Use Vietnamese + English consistently |
| 3 | Missing stakeholder | Add Secondary Actor |
| 4 | Edge cases incomplete | Add error handling flows |

---

## 7. STAKEHOLDER MATRIX

| Actor | Role | Access Level | Use Cases |
|-------|------|------------|-----------|
| **Kế toán viên** | Primary | RW | All transaction UCs |
| **Kế toán trưởng** | Secondary | Approve | Period closing, Reports, Audit |
| **Thủ kho** | Primary | RW | Inventory (I01-I03) |
| **Giám đốc** | Secondary | Read | Financial statements |
| **Auditor** | Secondary | Read | Audit trail, Reports |
| **Hệ thống** | Secondary | Auto | Validation, Logging |

---

## 8. REFERENCE LINKS

| Document | File |
|----------|------|
| Consolidated UC | docs/GL_USE_CASES_COMPLETE.md |
| Production Readiness | docs/PRODUCTION_READINESS.md |
| Implementation Roadmap | docs/roadmaps/implementation_roadmap.md |

---

*Last Updated: 2026-04-16*
*Consolidated by: GL System*