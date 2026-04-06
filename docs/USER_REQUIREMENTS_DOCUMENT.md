# USER REQUIREMENTS DOCUMENT (URD)
# Vietnamese Enterprise Accounting Software
# Compliant with Circular 99/2025/TT-BTC & Latest Tax Laws

**Document Version:** 1.0
**Date:** April 2026
**Prepared by:** CFO Office
**Status:** Draft for Review

---

## TABLE OF CONTENTS

1. Executive Summary
2. Stakeholders & User Roles
3. Functional Requirements
4. Non-Functional Requirements
5. Regulatory Compliance Requirements
6. Integration Requirements
7. Reporting Requirements
8. Data & Document Management Requirements
9. Security & Access Requirements
10. Acceptance Criteria

---

## 1. EXECUTIVE SUMMARY

### 1.1 Purpose

This document defines the user requirements for a comprehensive Vietnamese enterprise accounting software system that complies with:

- **Circular 99/2025/TT-BTC** - New Accounting Regime (effective 01/01/2026, replacing Circular 200/2014/TT-BTC)
- **Law on Corporate Income Tax No. 67/2025/QH15** (effective 01/10/2025)
- **Law on Personal Income Tax No. 109/2025/QH15** (effective 01/07/2026)
- **Amended VAT Law No. 149/2025/QH15** (effective 01/01/2026)
- **Law on Tax Administration No. 108/2025/QH15** (effective 01/07/2026)
- **Decree 70/2025/ND-CP** - Electronic Invoices (amending Decree 123/2020/ND-CP)
- **Circular 32/2025/TT-BTC** - Guidance on Electronic Invoices
- **Decree 320/2025/ND-CP** - Guidance on CIT Law
- **Decree 181/2025/ND-CP** & **Decree 359/2025/ND-CP** - Guidance on VAT Law
- **Resolution 204/2025/QH15** - 8% VAT reduction (01/07/2025 to 31/12/2026)
- **Decree 310/2025/ND-CP** - Tax & Invoice Penalties
- **Decree 337/2025/ND-CP** - Electronic Labor Contracts
- **Decree 52/2024/ND-CP** - Cashless Payments

### 1.2 Scope

The system shall cover the complete accounting lifecycle for Vietnamese enterprises, from transaction entry through financial reporting and tax declaration, fully compliant with the new Circular 99/2025/TT-BTC regime.

### 1.3 Key Transition

Enterprises currently using Circular 200/2014/TT-BTC MUST transition to Circular 99/2025/TT-BTC for fiscal years beginning on or after 01/01/2026. Enterprises using Circular 133/2016/TT-BTC may continue.

---

## 2. STAKEHOLDERS & USER ROLES

### 2.1 User Role Matrix

| Role | Description | Key Responsibilities |
|------|-------------|---------------------|
| **Chief Accountant (Ke Toan Truong)** | Head of accounting department | Approve entries, manage chart of accounts, review reports, tax compliance |
| **General Accountant (Ke Toan Tong Hop)** | Senior accountant | Journal entries, account reconciliation, financial statement preparation |
| **Tax Accountant (Ke Toan Thue)** | Tax specialist | Tax declarations (VAT, CIT, PIT), tax invoice management, tax reconciliation |
| **AR Accountant (Ke Toan Cong No Phai Thu)** | Receivables specialist | Customer invoices, payment tracking, debt collection, aging reports |
| **AP Accountant (Ke Toan Cong No Phai Tra)** | Payables specialist | Supplier invoices, payment processing, vendor reconciliation |
| **Inventory Accountant (Ke Toan Kho)** | Inventory specialist | Stock movements, inventory valuation, stock reports |
| **Payroll Accountant (Ke Toan Luong)** | Payroll specialist | Salary calculation, social insurance (BHXH, BHYT, BHTN), union fees (KPCD) |
| **Fixed Asset Accountant (Ke Toan TSCD)** | Fixed asset specialist | Asset registration, depreciation, asset disposal |
| **Cashier (Thu Quy)** | Cash handler | Cash receipts/payments, bank transactions, daily cash reports |
| **CFO / Finance Director** | Financial leadership | Financial oversight, strategic decisions, board reporting |
| **CEO / Director** | Executive management | Dashboard viewing, approval workflows, strategic reports |
| **Auditor (Internal/External)** | Audit function | Read-only access, audit trails, compliance verification |
| **System Administrator** | IT administration | User management, system configuration, backup, security |

---

## 3. FUNCTIONAL REQUIREMENTS

### 3.1 Chart of Accounts Management (TKKT)

**FR-001:** System shall support the complete Circular 99/2025/TT-BTC chart of accounts:
- 71 Level-1 accounts
- 101 Level-2 accounts
- 10 Level-3 accounts
- 2 Level-4 accounts

**FR-002:** System shall support 8 account groups (Loại 1-9):
- Group 1: Assets (Tai San) - TK 111 to 244
- Group 2: Liabilities (No Phai Tra) - TK 331 to 357
- Group 3: Equity (Von Chu So Huu) - TK 411 to 421
- Group 4: Revenue (Doanh Thu) - TK 511 to 521
- Group 5: Production/Business Costs (Chi Phi SXKD) - TK 621 to 642
- Group 6: Other Income (Thu Nhap Khac) - TK 711
- Group 7: Other Expenses (Chi Phi Khac) - TK 811 to 821
- Group 8: Business Results (Xac Dinh Ket Qua) - TK 911

**FR-003:** Users shall be able to add custom sub-accounts (Level 3, 4) per Article 11 of Circular 99, provided:
- No overlap with existing accounts
- Does not alter financial statement line items
- Documented in internal accounting policy

**FR-004:** System shall support account name, code, structure, and content customization with mandatory justification documentation.

### 3.2 Voucher & Document Management (Chung Tu)

**FR-005:** System shall support all Circular 99 voucher templates:
- 01-VT: Goods Receipt Note (Phieu Nhap Kho)
- 02-VT: Goods Issue Note (Phieu Xuat Kho)
- 03-TT: Advance Request Form (Giay De Nghi Tam Ung)
- 01-TT: Cash Receipt Voucher (Phieu Thu)
- 02-TT: Cash Payment Voucher (Phieu Chi)
- 06-VT: Purchase List (Bang Ke Mua Hang)
- TSCD forms: Asset handover, liquidation, revaluation, inventory
- Salary payment forms, allocation tables
- Contract forms (giao khoan)

**FR-006:** System shall support electronic voucher generation, approval workflow, and digital signatures.

**FR-007:** System shall maintain sequential voucher numbering with no gaps.

### 3.3 Journal Entry & General Ledger

**FR-008:** System shall support double-entry bookkeeping with mandatory debit/credit balance.

**FR-009:** System shall support journal entry types:
- Daily entries (Nhat Ky Chung)
- Special journals (Nhat Ky Dac Biet)
- Recurring entries (But Toan Tu Dong)
- Opening entries (So Du Dau Ky)
- Closing entries (But Toan Cuoi Ky)
- Adjustment entries (But Toan Dieu Chinh)

**FR-010:** System shall enforce the accounting equation: Assets = Liabilities + Equity.

**FR-011:** System shall support multi-currency entries with automatic exchange rate application (TK 413).

**FR-012:** System shall support VAT calculation at multiple rates:
- Standard rate: 10%
- Reduced rate: 8% (per Resolution 204/2025/QH15)
- Zero rate: 0% (exports)
- Non-taxable: Khong chiu thue

### 3.4 Accounts Receivable (Phai Thu)

**FR-013:** System shall manage customer accounts (TK 131) with:
- Invoice generation and tracking
- Payment receipt matching
- Aging analysis (30/60/90/180+ days)
- Bad debt provision (Du Phong Phai Thu Kho Doi - TK 2293)
- Debt collection workflow

**FR-014:** System shall support internal receivables (TK 136) with sub-accounts:
- 1361: Capital at subordinate units
- 1362: Internal exchange rate differences
- 1363: Internal capitalized borrowing costs
- 1368: Other internal receivables

**FR-015:** System shall support other receivables (TK 138):
- 1381: Missing assets pending resolution
- 1383: Special consumption tax on imports
- 1388: Other receivables

### 3.5 Accounts Payable (Phai Tra)

**FR-016:** System shall manage supplier accounts (TK 331) with:
- Invoice receipt and verification
- Payment scheduling and processing
- Aging analysis
- Supplier reconciliation

**FR-017:** System shall manage taxes payable (TK 333) with sub-accounts:
- 3331: VAT payable (33311: Output VAT, 33312: Import VAT)
- 3332: Special consumption tax
- 3333: Import/export tax
- 3334: Corporate income tax
- 3335: Personal income tax
- 3336: Natural resources tax
- 3337: Land tax, land rental
- 3338: Environmental protection tax & others
- 3339: Fees, charges & other payments

**FR-018:** System shall manage payroll payable (TK 334) and other payables (TK 338):
- 3381: Surplus assets pending resolution
- 3382: Union fees (Kinh phi cong doan)
- 3383: Social insurance (BHXH)
- 3384: Health insurance (BHYT)
- 3386: Unemployment insurance (BHTN)
- 3387: Unallocated revenue
- 3388: Other payables

### 3.6 Inventory Management (Hang Ton Kho)

**FR-019:** System shall manage inventory accounts:
- 151: Goods in transit
- 152: Raw materials
- 153: Tools & supplies
- 154: Work in progress
- 155: Finished goods
- 156: Merchandise
- 157: Goods sent for sale
- 158: Materials in bonded warehouse

**FR-020:** System shall support inventory valuation methods:
- FIFO (First In, First Out)
- Weighted average (Binh Quan Gia)
- Specific identification (Thuc Te Tung Lo)

**FR-021:** System shall calculate inventory provisions (TK 2294) when net realizable value < cost.

**FR-022:** System shall support material/supply allocation (Bang Phan Bo Nguyen Lieu, Vat Lieu, CCDC).

### 3.7 Fixed Assets & Depreciation (TSCD)

**FR-023:** System shall manage fixed assets:
- 211: Tangible fixed assets
- 212: Finance leased assets
- 213: Intangible fixed assets
- 214: Accumulated depreciation
- 215: Biological assets
- 217: Investment property

**FR-024:** System shall calculate depreciation using:
- Straight-line method (Duong Thang)
- Declining balance method (So Du Giam Dan)
- Units of production method (Theo So Luong San Pham)

**FR-025:** System shall support:
- Asset registration (Bien Ban Giao Nhan TSCD - 01-TSCD)
- Asset transfer/modification (03-TSCD)
- Asset liquidation (Bien Ban Thanh Ly TSCD)
- Asset revaluation (Bien Ban Danh Gia Lai TSCD)
- Asset inventory (05-TSCD)
- Depreciation schedule (Bang Tinh Khau Hao TSCD)

### 3.8 Payroll & Related Contributions (Luong & Bao Hiem)

**FR-026:** System shall calculate payroll with:
- Basic salary, allowances, bonuses
- Overtime calculation (per Labor Law)
- Personal income tax withholding (TK 3335)
- Salary allocation table (Bang Phan Bo Tien Luong)
- Salary payment table (Bang Thanh Toan Tien Luong)

**FR-027:** System shall calculate mandatory contributions per 2026 rates:
- Social Insurance (BHXH): Employer 14%, Employee 8%
- Health Insurance (BHYT): Employer 3%, Employee 1.5%
- Unemployment Insurance (BHTN): Employer 1%, Employee 1%
- Occupational Accident & Disease Insurance (BHTNLĐ-BNN): Employer 0.5%
- Union Fees (KPCD): Employer 2% on social insurance wage base (quỹ lương đóng BHXH)
- **Total Employer Rate: 18.5%** (BHXH 14% + BHYT 3% + BHTN 1% + BHTNLĐ-BNN 0.5%)
- **Total Employee Rate: 10.5%** (BHXH 8% + BHYT 1.5% + BHTN 1%)
- **KPCD: 2% on social insurance wage base** (not actual salary)

**FR-028:** System shall manage:
- Labor contracts (Hop Dong Lao Dong) per Decree 337/2025
- Probation contracts (Hop Dong Thu Viec)
- Dependents registration for PIT deduction
- Form 08/CK-TNCN (Income commitment)

### 3.9 Cost Accounting (Ke Toan Chi Phi)

**FR-029:** System shall track production costs:
- 621: Direct materials
- 622: Direct labor
- 623: Construction equipment costs (with sub-accounts 6231-6238)
- 627: Manufacturing overhead (with sub-accounts 6271-6278)

**FR-030:** System shall track business costs:
- 632: Cost of goods sold
- 635: Financial costs
- 641: Selling expenses (with sub-accounts 6411-6418)
- 642: Management expenses (with sub-accounts 6421-6428)

**FR-031:** System shall support TK 911 for business result determination:
- Transfer all revenues to TK 911 (credit side)
- Transfer all costs to TK 911 (debit side)
- Calculate net profit/loss

### 3.10 Tax Management

**FR-032:** VAT Management (Thue GTGT):
- Input VAT tracking (TK 1331, 1332)
- Output VAT calculation
- VAT declaration forms (01/GTGT, 04/GTGT)
- Deductible vs. non-deductible VAT
- 8% reduced VAT rate support (Resolution 204/2025/QH15)
- VAT by period (monthly/quarterly)

**FR-033:** Corporate Income Tax (Thue TNDN):
- Quarterly provisional CIT calculation
- Annual CIT finalization (Form 03/TNDN)
- Deductible vs. non-deductible expenses
- Loss carryforward (Phu Luc 03-2/TNDN)
- TK 821: CIT expense (8211: Current, 8212: Deferred)
- Global minimum tax support (82111, 82112)

**FR-034:** Personal Income Tax (Thue TNCN):
- Monthly/quarterly PIT declaration (02/KK-TNCN)
- Annual PIT finalization (05/QTT-TNCN)
- Dependent deductions
- Contract worker PIT calculation
- Electronic PIT withholding certificates

**FR-035:** License Fee (Le Phi Mon Bai):
- Annual declaration and payment
- Tiered rates based on charter capital

**FR-036:** Foreign Contractor Tax (Thue Nha Thau):
- VAT and CIT on foreign contractor payments
- Declaration and payment tracking

### 3.11 Electronic Invoice Management (Hoa Don Dien Tu)

**FR-037:** System shall support electronic invoices per Decree 70/2025 & Circular 32/2025:
- Invoices with tax authority code (Co Ma CQT)
- Invoices without tax authority code (Khong Co Ma CQT)
- Invoice replacement (Thay The)
- Invoice adjustment (Dieu Chinh Tang/Giam)
- Commercial discount invoices (Chiet Khau Thuong Mai)
- Returned goods invoices (Hang Ban Tra Lai)
- Internal consumption invoices (Tieu Dung Noi Bo)
- POS-generated invoices (May Tinh Tien)

**FR-038:** System shall support:
- Invoice registration workflow
- Invoice number management
- Error handling (Form 04/SS-HDDT)
- Invoice verification with tax authority
- Invoice archiving per Decree 123

**FR-039:** System shall enforce correct invoice timing:
- Goods delivery time
- Service completion time
- Payment collection time

### 3.12 Bank & Cash Management

**FR-040:** System shall manage:
- 111: Cash on hand (Tien Mat)
- 112: Demand deposits (Tien Gui Khong Ky Han)
- 113: Cash in transit (Tien Dang Chuyen)
- 1281: Term deposits (Tien Gui Co Ky Han)

**FR-041:** System shall support bank reconciliation with automatic matching.

**FR-042:** System shall support cashless payments per Decree 52/2024/ND-CP.

### 3.13 Financial Statements (Bao Cao Tai Chinh)

**FR-043:** System shall generate Circular 99 financial statements:
- **B01-DN:** Statement of Financial Position (Bao Cao Tinh Hinh Tai Chinh)
- **B02-DN:** Statement of Business Results (Bao Cao Ket Qua Hoat Dong Kinh Doanh)
- **B03-DN:** Cash Flow Statement (Bao Cao Luu Chuyen Tien Te)
- **B09-DN:** Notes to Financial Statements (Thuyet Minh Bao Cao Tai Chinh)
- **B01-DNKLT:** For small & micro enterprises
- **B09-DNKLT:** Notes for small & micro enterprises

**FR-044:** System shall support interim financial reports (Bao Cao Giua Nien Do).

**FR-045:** System shall enforce presentation principles per Circular 99:
- Going concern assumption
- Consistency
- Accrual basis
- Materiality
- Offsetting prohibition
- Comparative information

**FR-046:** System shall support financial statement amendment/supplement workflow.

### 3.14 Accounting Books (So Sach)

**FR-047:** System shall maintain all required accounting books per Circular 99:
- General Journal (So Nhat Ky Chung)
- General Ledger (So Cai Tai Khoan)
- Subsidiary Ledgers (So Chi Tiet)
- Fixed Asset Register (So Theo Doi TSCD)
- Inventory Cards (The Kho)

### 3.15 Data Migration from Circular 200

**FR-048:** System shall support balance transfer from Circular 200 to Circular 99 per Article 19 of Circular 99:
- TK 111, 112, 113, 121, 153, 154, 156, 211, 212, 213 detail transfer based on detailed balances
- TK 138 (BCC contribution) to TK 2281 (Đầu tư góp vốn vào đơn vị khác)
- TK 2413 (Sửa chữa lớn TSCĐ - upgrade/costs portion) to TK 2414 (Nâng cấp, cải tạo TSCĐ)
- TK 338 (dividends detail) to TK 332 (Phải trả cổ tức, lợi nhuận)
- TK 441 (Nguồn vốn đầu tư XDCB) + TK 466 (Nguồn kinh phí đã hình thành TSCĐ) to TK 4118 (Vốn khác)
- TK 421 (Lợi nhuận chưa phân phối) direct transfer
- TK 347 (Thuế TNDN hoãn lại) direct transfer
- TK 213 (TSCĐ vô hình) detail transfer

### 3.16 Exchange Rate Revaluation

**FR-049:** System shall perform period-end exchange rate revaluation for all monetary items in foreign currency:
- Cash in foreign currency (TK 112)
- Receivables in foreign currency (TK 131, 136, 138)
- Payables in foreign currency (TK 331, 336, 338, 341)
- Loans in foreign currency (TK 341)
**FR-050:** System shall record exchange rate differences to TK 413 (Chênh lệch tỷ giá hối đoái):
- Gain: DK 111,112,131... / Co 413
- Loss: DK 413 / Co 111,112,331...
**FR-051:** System shall use State Bank of Vietnam (SBV) closing exchange rate for revaluation.

### 3.17 Revenue Recognition

**FR-052:** System shall recognize revenue per VAS 14 when control of goods/services transfers to customer, not when invoiced.
**FR-053:** System shall support percentage-of-completion revenue recognition for construction contracts (TK 337).
**FR-054:** System shall track unearned revenue (TK 3387 - Doanh thu chờ phân bổ) and recognize over time.

### 3.18 Lease Accounting

**FR-055:** System shall support finance lease accounting:
- Lessee: Recognize leased asset (TK 212) and lease liability (TK 3412)
- Lessor: Track lease receivable and interest income
**FR-056:** System shall calculate and post lease depreciation (DK 6274,6424... / Co 2142) and interest expense (DK 635 / Co 3412).

### 3.19 VAT Timing Rules

**FR-057:** System shall determine VAT timing (thời điểm xác định thuế GTGT) per VAT Law:
- Goods: Time of delivery/transfer of ownership
- Services: Time of service completion
- Construction: Time of payment collection or handover (whichever earlier)
- Export: Time of customs clearance
**FR-058:** System shall separate VAT timing from invoice timing — VAT liability may arise before or after invoice issuance.

---

## 4. NON-FUNCTIONAL REQUIREMENTS

### 4.1 Performance

**NFR-001:** System shall process up to 50,000 journal entries per hour.
**NFR-002:** Financial statement generation shall complete within 30 seconds for enterprises with up to 1 million transactions per year.
**NFR-003:** System shall support concurrent access by 100+ users.
**NFR-004:** Page load time shall not exceed 3 seconds for standard operations.

### 4.2 Availability

**NFR-005:** System availability shall be 99.9% during business hours (7:00-22:00, Monday-Saturday).
**NFR-006:** Scheduled maintenance shall be performed outside peak tax filing periods.

### 4.3 Scalability

**NFR-007:** System shall support enterprises from micro (under 10 employees) to large (1000+ employees).
**NFR-008:** Database shall support up to 10 years of historical data without performance degradation.

### 4.4 Usability

**NFR-009:** Interface shall be in Vietnamese language.
**NFR-010:** System shall support both Vietnamese and English number formatting.
**NFR-011:** Users shall be able to complete standard journal entry within 3 clicks.

### 4.5 Auditability

**NFR-012:** All data modifications shall be logged with user, timestamp, old value, new value.
**NFR-013:** System shall maintain immutable audit trail for all financial transactions.
**NFR-014:** Audit logs shall be retained for minimum 10 years per Accounting Law.

---

## 5. REGULATORY COMPLIANCE REQUIREMENTS

### 5.1 Accounting Law Compliance

**RC-001:** System shall comply with Vietnam Accounting Law.
**RC-002:** System shall comply with Vietnamese Accounting Standards (VAS).
**RC-003:** System shall comply with Circular 99/2025/TT-BTC effective 01/01/2026.

### 5.2 Tax Law Compliance

**RC-004:** VAT calculations shall comply with Law 149/2025/QH15 (Amended VAT Law), Decree 181/2025, Decree 359/2025, Circular 69/2025.
**RC-005:** CIT calculations shall comply with Law 67/2025/QH15, Decree 320/2025, Circular 20/2026.
**RC-006:** PIT calculations shall comply with Law 109/2025/QH15 (effective 01/07/2026).
**RC-007:** Tax administration shall comply with Law 108/2025/QH15, Decree 373/2025.
**RC-008:** Tax penalties shall comply with Decree 310/2025.

### 5.3 Electronic Invoice Compliance

**RC-009:** Electronic invoices shall comply with Decree 70/2025, Circular 32/2025.
**RC-010:** Invoice format, content, and numbering shall follow prescribed templates.

### 5.4 Data Retention

**RC-011:** Accounting documents shall be retained per legal requirements: Type A (permanent), Type B (10 years), Type C (5 years) per Nghị định 43/2025/ND-CP.
**RC-012:** Electronic storage shall meet legal validity requirements per Nghị định 43/2025/ND-CP.
**RC-013:** Accounting document archiving shall comply with Nghị định 43/2025/ND-CP on archival methods, retention periods, and document classification.

---

## 6. INTEGRATION REQUIREMENTS

### 6.1 Tax Authority Integration

**IR-001:** System shall support electronic tax declaration via General Department of Taxation portal.
**IR-002:** System shall support electronic tax payment via e-banking.
**IR-003:** System shall support invoice data submission to tax authority.

### 6.2 Banking Integration

**IR-004:** System shall support bank statement import (MT940, CSV, Excel formats).
**IR-005:** System shall support direct payment initiation via banking APIs.

### 6.3 Social Insurance Integration

**IR-006:** System shall generate social insurance declaration files (e-Social Insurance format).

### 6.4 External Systems

**IR-007:** System shall support data export to HTKK tax support software.
**IR-008:** System shall support integration with MISA, Fast accounting software for data migration.

---

## 7. REPORTING REQUIREMENTS

### 7.1 Mandatory Reports

**RR-001:** Monthly/Quarterly VAT Declaration
**RR-002:** Monthly/Quarterly PIT Declaration
**RR-003:** Quarterly CIT Provisional Declaration
**RR-004:** Annual CIT Finalization
**RR-005:** Annual PIT Finalization
**RR-006:** Annual Financial Statements (B01, B02, B03, B09)
**RR-007:** License Fee Declaration
**RR-008:** Social Insurance Reports

### 7.2 Management Reports

**RR-009:** Trial Balance (Can Doi So Phat Sinh)
**RR-010:** Account Detail Reports (So Chi Tiet)
**RR-011:** AR/AP Aging Reports
**RR-012:** Inventory Valuation Report
**RR-013:** Fixed Asset Register & Depreciation Report
**RR-014:** Cash Flow Report
**RR-015:** Revenue & Expense Analysis
**RR-016:** Budget vs. Actual Report
**RR-017:** Tax Reconciliation Report

---

## 8. DATA & DOCUMENT MANAGEMENT REQUIREMENTS

**DR-001:** System shall support document attachment to journal entries.
**DR-002:** System shall support scanned document storage (PDF, images).
**DR-003:** System shall support document search by date, number, type, content.
**DR-004:** System shall support document versioning.
**DR-005:** System shall support automatic backup with daily incremental and weekly full backups.
**DR-006:** System shall support data export in Excel, PDF, CSV formats.

---

## 9. SECURITY & ACCESS REQUIREMENTS

**SR-001:** System shall implement Role-Based Access Control (RBAC).
**SR-002:** System shall require strong password policy (min 8 chars, complexity).
**SR-003:** System shall support Two-Factor Authentication (2FA).
**SR-004:** System shall encrypt data at rest (AES-256) and in transit (TLS 1.3).
**SR-005:** System shall implement session timeout after 30 minutes of inactivity.
**SR-006:** System shall prevent concurrent login from multiple devices for same user.
**SR-007:** System shall log all login attempts (successful and failed).
**SR-008:** System shall support IP-based access restrictions.
**SR-009:** System shall implement maker-checker principle for critical transactions.

---

## 10. ACCEPTANCE CRITERIA

### 10.1 Functional Acceptance

- All 71 Level-1 accounts from Circular 99 are correctly configured (verified against Phụ lục II, TT 99/2025/TT-BTC)
- All 101 Level-2 accounts correctly mapped
- All voucher templates match official Circular 99 formats (Phụ lục I, TT 99/2025/TT-BTC)
- All financial statement templates (B01-DN, B02-DN, B03-DN, B09-DN) match official formats
- Tax calculations produce results matching HTKK software outputs (tolerance ±1,000 VND)
- Balance transfer from Circular 200 produces correct Circular 99 balances per Article 19
- Balance transfer from Circular 133 produces correct Circular 99 balances
- Insurance calculations match statutory rates: Employee 10.5%, Employer 18.5%, KPCD 2% on BHXH wage base
- VAT timing rules correctly separate VAT liability date from invoice date
- Exchange rate revaluation (TK 413) produces correct gains/losses using SBV closing rates

### 10.2 Compliance Acceptance

- System passes audit by certified Vietnamese auditor
- Tax declarations match General Department of Taxation requirements
- Electronic invoices are accepted by tax authority system
- Financial statements pass regulatory review

### 10.3 Performance Acceptance

- System handles 10,000 entries/hour without degradation
- Financial statements generate within 30 seconds
- 100 concurrent users experience <3 second response time

---

**END OF USER REQUIREMENTS DOCUMENT**
