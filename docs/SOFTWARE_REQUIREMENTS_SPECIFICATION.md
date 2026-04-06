# SOFTWARE REQUIREMENTS SPECIFICATION (SRS)
# Vietnamese Enterprise Accounting Software Platform
# Compliant with Circular 99/2025/TT-BTC & Latest Vietnamese Tax Laws

**Document Version:** 1.0
**Date:** April 2026
**Prepared by:** Lead Business Analyst Office
**Classification:** Confidential
**Status:** Approved for Development

**Source Documents:**
- BRD v1.0 (BUSINESS_REQUIREMENTS_DOCUMENT.md)
- URD v1.0 (USER_REQUIREMENTS_DOCUMENT.md)
- DATA_FLOW.md v1.0
- WORKFLOW.md v1.0
- USER_JOURNEY.md v1.0
- PROCESS_FLOWS.md v1.0

---

## TABLE OF CONTENTS

1.  Introduction
2.  Overall Description
3.  System Features — Functional Requirements
4.  External Interface Requirements
5.  Non-Functional Requirements
6.  Data Requirements
7.  Business Rules
8.  Regulatory Compliance Requirements
9.  System Constraints
10. Traceability Matrix
11. Glossary & Abbreviations
12. Appendix

---

## 1. INTRODUCTION

### 1.1 Purpose

This Software Requirements Specification (SRS) defines the complete functional and non-functional requirements for the Vietnamese Enterprise Accounting Software Platform. It serves as the single source of truth for:

- **Development Team:** What to build and how the system shall behave.
- **QA Team:** What to test and acceptance criteria.
- **Stakeholders:** What the system will deliver.

### 1.2 Scope

The system is a cloud-based, multi-tenant accounting platform designed for Vietnamese enterprises. It covers the complete accounting lifecycle — from transaction entry through financial reporting and tax declaration — fully compliant with **Circular 99/2025/TT-BTC** (effective 01/01/2026, replacing Circular 200/2014/TT-BTC) and all current Vietnamese tax laws.

**Target Users:** Enterprises of all sizes (micro to large), from 10 to 1,000+ employees.

### 1.3 Definitions, Acronyms & Abbreviations

| Term | Definition |
|------|-----------|
| TT99 | Circular 99/2025/TT-BTC — New Accounting Regime |
| TT200 | Circular 200/2014/TT-BTC — Old Accounting Regime (replaced) |
| TT133 | Circular 133/2016/TT-BTC — SME Accounting Regime |
| COA | Chart of Accounts (Hệ thống tài khoản kế toán) |
| GL | General Ledger (Sổ Cái Tổng Hợp) |
| AR | Accounts Receivable (Phải Thu) |
| AP | Accounts Payable (Phải Trả) |
| VAT/GTGT | Value Added Tax / Thuế Giá Trị Gia Tăng |
| CIT/TNDN | Corporate Income Tax / Thuế Thu Nhập Doanh Nghiệp |
| PIT/TNCN | Personal Income Tax / Thuế Thu Nhập Cá Nhân |
| BHXH | Social Insurance (Bảo Hiểm Xã Hội) |
| BHYT | Health Insurance (Bảo Hiểm Y Tế) |
| BHTN | Unemployment Insurance (Bảo Hiểm Thất Nghiệp) |
| BHTNLĐ-BNN | Occupational Accident & Disease Insurance |
| KPCD | Union Fee (Kinh Phí Công Đoàn) |
| CQT | Tax Authority (Cơ Quan Thuế) |
| GDT | General Department of Taxation |
| SBV | State Bank of Vietnam |
| e-invoice/HĐĐT | Electronic Invoice (Hóa Đơn Điện Tử) |
| BCTC | Financial Statements (Báo Cáo Tài Chính) |
| TSCD | Fixed Assets (Tài Sản Cố Định) |
| CCDC | Tools & Equipment (Công Cụ Dụng Cụ) |
| HTK | Inventory (Hàng Tồn Kho) |
| NRV | Net Realizable Value |
| FIFO | First In, First Out |
| SBV | State Bank of Vietnam |
| SoD | Segregation of Duties |
| RBAC | Role-Based Access Control |

### 1.4 References

| Ref ID | Document | Version |
|--------|----------|---------|
| REF-01 | Circular 99/2025/TT-BTC | Official |
| REF-02 | Law 67/2025/QH15 (CIT) | Official |
| REF-03 | Law 109/2025/QH15 (PIT) | Official |
| REF-04 | Law 149/2025/QH15 (VAT Amended) | Official |
| REF-05 | Law 108/2025/QH15 (Tax Admin) | Official |
| REF-06 | Decree 70/2025/ND-CP (E-Invoice) | Official |
| REF-07 | Circular 32/2025/TT-BTC (E-Invoice Guidance) | Official |
| REF-08 | Decree 320/2025/ND-CP (CIT Guidance) | Official |
| REF-09 | Decree 181/2025/ND-CP & 359/2025/ND-CP (VAT Guidance) | Official |
| REF-10 | Decree 310/2025/ND-CP (Tax Penalties) | Official |
| REF-11 | Decree 337/2025/ND-CP (E-Labor Contracts) | Official |
| REF-12 | Decree 52/2024/ND-CP (Cashless Payments) | Official |
| REF-13 | Decree 43/2025/ND-CP (Accounting Document Archiving) | Official |
| REF-14 | Resolution 204/2025/QH15 (8% VAT Reduction) | Official |
| REF-15 | NQ 107/2023/QH15 (Global Minimum Tax) | Official |
| REF-16 | NĐ 18/2024/ND-CP (Global Minimum Tax Guidance) | Official |
| REF-17 | Luật BHXH 2024 (Social Insurance Law) | Official |
| REF-18 | Luật ATVSLĐ (Occupational Safety Law) | Official |
| REF-19 | VAS 14 (Revenue Recognition) | Official |
| REF-20 | Luật Kế Toán (Accounting Law) | Official |

### 1.5 Document Conventions

| Convention | Meaning |
|-----------|---------|
| **SHALL** | Mandatory requirement (must be implemented) |
| **SHOULD** | Recommended requirement (strongly preferred) |
| **MAY** | Optional requirement |
| **P0** | Critical — Required for MVP launch |
| **P1** | High — Required within 3 months of launch |
| **P2** | Medium — Required within 6 months |
| **DK** | Debit (Nợ) |
| **Co** | Credit (Có) |

---

## 2. OVERALL DESCRIPTION

### 2.1 Product Perspective

The system is a standalone, cloud-native SaaS platform. It replaces or supplements existing accounting software (MISA, Fast, Bravo) and Excel-based processes. It integrates with external systems:

- **Tax Authority (GDT)** — E-filing, e-invoice code generation
- **Commercial Banks** — Statement import, payment initiation
- **E-Invoice Providers** — VNPT, Viettel, BKAV, Safe-CA
- **Social Insurance (BHXH)** — Monthly declarations
- **Time Tracking Systems** — Attendance data import

### 2.2 Product Functions (Module Overview)

| Module ID | Module Name | Description | Priority |
|-----------|------------|-------------|----------|
| MOD-01 | System Administration | User management, COA configuration, period management, backup | P0 |
| MOD-02 | General Ledger | Journal entries, account management, trial balance, TK 911 closing | P0 |
| MOD-03 | Accounts Receivable | Customer management, invoicing, payment matching, aging, bad debt | P0 |
| MOD-04 | Accounts Payable | Supplier management, invoice processing, 3-way match, payment | P0 |
| MOD-05 | Electronic Invoice | E-invoice creation, CQT code, replacement, adjustment, cancellation | P0 |
| MOD-06 | Tax Management | VAT, CIT, PIT, License Fee, Foreign Contractor Tax calculations | P0 |
| MOD-07 | Financial Reporting | B01-DN, B02-DN, B03-DN, B09-DN, trial balance, management reports | P0 |
| MOD-08 | Accounting Books | General journal, general ledger, subsidiary ledgers | P0 |
| MOD-09 | Bank & Cash | Cash management, bank reconciliation, payment processing | P0 |
| MOD-10 | Payroll | Salary calculation, insurance, PIT withholding, payslips | P0 |
| MOD-11 | Fixed Assets | Asset registration, depreciation, transfer, disposal, revaluation | P1 |
| MOD-12 | Inventory | Stock management, valuation (FIFO/weighted avg), provisions | P1 |
| MOD-13 | Data Migration | Circular 200/133 to Circular 99 balance transfer | P0 |
| MOD-14 | Digital Signature | Chữ ký số integration for e-invoice and tax filing | P0 |
| MOD-15 | Accounting Policy | Quy chế hạch toán management, custom account justification | P0 |

### 2.3 User Classes & Characteristics

| User Class | Role | Technical Skill | Accounting Knowledge | Frequency |
|-----------|------|----------------|---------------------|-----------|
| UC-01 | Chief Accountant | Medium | Expert (10+ years) | Daily |
| UC-02 | General Accountant | Medium | Advanced (5+ years) | Daily |
| UC-03 | Tax Accountant | Medium | Advanced (tax specialist) | Monthly/Quarterly peaks |
| UC-04 | AR Accountant | Basic | Intermediate | Daily |
| UC-05 | AP Accountant | Basic | Intermediate | Daily |
| UC-06 | Payroll Accountant | Medium | Intermediate (payroll specialist) | Monthly |
| UC-07 | Inventory Accountant | Basic | Intermediate | Daily |
| UC-08 | Fixed Asset Accountant | Basic | Intermediate | Monthly |
| UC-09 | Cashier | Basic | Basic (cash handling) | Daily |
| UC-10 | CFO/Finance Director | Medium | Expert (strategic) | Daily/Weekly |
| UC-11 | CEO/Director | Low | Basic (overview only) | Weekly/Monthly |
| UC-12 | Auditor (Internal/External) | Medium | Expert (audit standards) | Annual |
| UC-13 | System Administrator | Expert | Basic (IT only) | Daily |

### 2.4 Operating Environment

| Aspect | Requirement |
|--------|------------|
| Platform | Web-based (Chrome, Firefox, Edge, Safari — latest 2 versions) |
| Server | Cloud-native, hosted in Vietnam (data sovereignty) |
| Database | PostgreSQL with row-level security |
| Backend | Python (Django/FastAPI) or Node.js |
| Frontend | React/Next.js with Vietnamese i18n |
| Mobile | Responsive web (Phase 1); Native app (Phase 2) |

### 2.5 Design & Implementation Constraints

| Constraint ID | Constraint | Impact |
|--------------|-----------|--------|
| CON-01 | Data must be stored in Vietnam | Hosting limited to VN-region cloud |
| CON-02 | Must support Vietnamese language & number formatting | UI/UX localization required |
| CON-03 | Must comply with Vietnamese Accounting Standards (VAS) | Development complexity |
| CON-04 | Double-entry bookkeeping is mandatory | All transactions must balance |
| CON-05 | Period lock is irreversible without CA override | Audit trail integrity |
| CON-06 | Sequential voucher numbering with no gaps | Concurrency control required |
| CON-07 | Digital signature mandatory for e-invoice & tax filing | Integration with VNPT/Viettel/BKAV |

### 2.6 Assumptions & Dependencies

| Assumption ID | Assumption | Risk if False |
|--------------|-----------|---------------|
| ASM-01 | Circular 99 will not be significantly amended before launch | High — rework required |
| ASM-02 | Tax authority e-filing APIs will be available and documented | High — fallback to manual |
| ASM-03 | Target enterprises have internet connectivity for cloud access | Medium — offline mode needed |
| ASM-04 | E-invoice providers offer stable APIs | Medium — manual fallback |
| ASM-05 | SBV publishes daily exchange rates in machine-readable format | Low — manual entry fallback |

---

## 3. SYSTEM FEATURES — FUNCTIONAL REQUIREMENTS

### 3.1 MOD-01: System Administration

#### 3.1.1 User Management

**SRS-ADM-001:** The system SHALL implement Role-Based Access Control (RBAC) with predefined roles matching user classes UC-01 through UC-13.

**SRS-ADM-002:** The system SHALL support the following operations for user accounts:
- Create, activate, deactivate, delete
- Assign one or more roles per user
- Set password with policy: minimum 8 characters, complexity (uppercase, lowercase, number, special character)
- Force password change on first login
- Support Two-Factor Authentication (2FA) via TOTP

**SRS-ADM-003:** The system SHALL prevent concurrent login from multiple devices for the same user account.

**SRS-ADM-004:** The system SHALL implement session timeout after 30 minutes of inactivity.

**SRS-ADM-005:** The system SHALL log all login attempts (successful and failed) with timestamp, IP address, and device ID.

**SRS-ADM-006:** The system SHALL support IP-based access restrictions configurable per enterprise.

#### 3.1.2 Chart of Accounts Management

**SRS-ADM-007:** The system SHALL pre-load the complete Circular 99/2025/TT-BTC Chart of Accounts:
- 71 Level-1 accounts (3 digits: e.g., 111, 333, 421)
- 101 Level-2 accounts (4 digits: e.g., 1331, 3331, 4211)
- 10 Level-3 accounts (5 digits: e.g., 33311, 33312)
- 2 Level-4 accounts (6 digits: e.g., 333111, 333112)

**SRS-ADM-008:** The system SHALL organize accounts into 8 groups:
- Group 1: Assets (TK 111–244)
- Group 2: Liabilities (TK 331–357)
- Group 3: Equity (TK 411–421)
- Group 4: Revenue (TK 511–521)
- Group 5: Production/Business Costs (TK 621–642)
- Group 6: Other Income (TK 711)
- Group 7: Other Expenses (TK 811–821)
- Group 8: Business Results (TK 911)

**SRS-ADM-009:** The system SHALL allow users to add custom sub-accounts (Level 3, 4) per Article 11 of Circular 99, subject to:
- No overlap with existing account codes
- No alteration of financial statement line items
- Mandatory justification documentation stored in Accounting Policy

**SRS-ADM-010:** The system SHALL validate custom account creation against the above rules before allowing activation.

#### 3.1.3 Accounting Period Management

**SRS-ADM-011:** The system SHALL support accounting periods in YYYY-MM format.

**SRS-ADM-012:** The system SHALL enforce period states:
- **Open:** New entries can be posted
- **Locked:** No new entries; adjustments require CA override
- **Closed:** No modifications allowed; permanent archive

**SRS-ADM-013:** The system SHALL prevent posting to a closed period. Reopening a closed period SHALL require Chief Accountant authentication and SHALL generate an audit log entry.

**SRS-ADM-014:** The system SHALL automatically open the next period when the current period is closed.

#### 3.1.4 Exchange Rate Management

**SRS-ADM-015:** The system SHALL support daily exchange rate import from State Bank of Vietnam (SBV).

**SRS-ADM-016:** The system SHALL allow manual exchange rate entry as fallback.

**SRS-ADM-017:** The system SHALL maintain a historical exchange rate table with effective dates.

#### 3.1.5 Backup & Restore

**SRS-ADM-018:** The system SHALL perform daily incremental backups and weekly full backups.

**SRS-ADM-019:** The system SHALL encrypt backup data before storage.

**SRS-ADM-020:** The system SHALL verify backup integrity after each backup operation.

**SRS-ADM-021:** The system SHALL store backups in a secondary geographic location within Vietnam.

### 3.2 MOD-02: General Ledger

#### 3.2.1 Journal Entry Management

**SRS-GL-001:** The system SHALL support double-entry bookkeeping with mandatory debit/credit balance enforcement.

**SRS-GL-002:** The system SHALL support the following journal entry types:
- Daily entries (Nhat Ky Chung)
- Special journals (Nhat Ky Dac Biet)
- Recurring entries (But Toan Tu Dong)
- Opening entries (So Du Dau Ky)
- Closing entries (But Toan Cuoi Ky)
- Adjustment entries (But Toan Dieu Chinh)
- Reversing entries

**SRS-GL-003:** The system SHALL enforce the following validation rules on journal entry submission:

| Rule ID | Validation | Error Message |
|---------|-----------|--------------|
| VR-GL-01 | Total debit = Total credit | "Entry unbalanced: Debit {X} != Credit {Y}" |
| VR-GL-02 | Accounting period is Open | "Period {period} is closed" |
| VR-GL-03 | All account codes exist in COA | "Account {code} does not exist" |
| VR-GL-04 | At least one debit and one credit line | "Entry must have at least one debit and one credit" |
| VR-GL-05 | All amounts > 0 | "Amount must be greater than zero" |
| VR-GL-06 | Entry date within selected period | "Entry date {date} is outside period {period}" |
| VR-GL-07 | Description is not empty | "Entry description is required" |

**SRS-GL-004:** The system SHALL support multi-currency journal entries:
- Base currency: VND
- Foreign currency entries SHALL record both foreign amount and VND equivalent
- VND equivalent SHALL be calculated using the exchange rate effective on the entry date
- Exchange rate differences SHALL be recorded in TK 413

**SRS-GL-005:** The system SHALL implement a Maker-Checker approval workflow for journal entries:
- Entries below configurable threshold: Auto-post
- Entries above threshold: Require approval from Senior Accountant or Chief Accountant
- No user SHALL approve their own entries

**SRS-GL-006:** The system SHALL generate sequential entry numbers with no gaps per accounting period.

#### 3.2.2 Trial Balance

**SRS-GL-007:** The system SHALL generate trial balance reports for any open or closed period.

**SRS-GL-008:** The trial balance SHALL list all accounts with:
- Opening debit/credit balance
- Period debit/credit turnover
- Closing debit/credit balance
- Verification: Total debit = Total credit

#### 3.2.3 TK 911 Year-End Closing

**SRS-GL-009:** The system SHALL automate the year-end closing process per Circular 99:
1. Transfer all revenues to TK 911 (credit side): DK 511, 515, 711 / Co 911
2. Transfer all costs to TK 911 (debit side): DK 911 / Co 632, 635, 641, 642, 811, 821
3. Calculate net profit/loss
4. If profit: DK 911 / Co 4212
5. If loss: DK 4212 / Co 911
6. Transfer TK 4212 to TK 4211 (accumulated)
7. Zero out TK 911 and TK 4212

**SRS-GL-010:** The system SHALL generate a Year-End Closing Report showing all transfer entries.

### 3.3 MOD-03: Accounts Receivable

#### 3.3.1 Customer Management

**SRS-AR-001:** The system SHALL maintain a customer master database with:
- Customer name, tax code (10-13 digits), address
- Credit limit and payment terms
- Contact information
- Status (active/inactive)

**SRS-AR-002:** The system SHALL validate customer tax code format (10-13 numeric digits).

#### 3.3.2 Invoice & Revenue Management

**SRS-AR-003:** The system SHALL create sales invoices with:
- Customer selection (auto-fill tax code, address)
- Line items (product/service, quantity, unit price)
- Commercial discount application (per Decree 70/2025)
- VAT rate selection (0%, 5%, 8%, 10%, Non-Taxable)
- Auto-calculation: Subtotal, VAT, Total

**SRS-AR-004:** The system SHALL recognize revenue (TK 511) when control of goods/services transfers to the customer, not merely upon invoice issuance (per VAS 14).

**SRS-AR-005:** The system SHALL post the following entry upon revenue recognition:
- DK 131 / Co 511 (revenue), Co 3331 (VAT output)

#### 3.3.3 Payment Matching

**SRS-AR-006:** The system SHALL support payment receipt recording with:
- Payment method: Cash (TK 111), Bank transfer (TK 112)
- Auto-matching to open invoices by amount, date, reference
- Manual override for partial payments
- Post entry: DK 111,112 / Co 131

**SRS-AR-007:** The system SHALL handle partial payments by:
- Applying payment to oldest invoice first (FIFO)
- Updating remaining balance on the invoice
- Maintaining invoice status: Unpaid / Partial / Paid

#### 3.3.4 Aging & Bad Debt

**SRS-AR-008:** The system SHALL generate AR aging reports with buckets: 0-30, 31-60, 61-90, 91-180, 180+ days.

**SRS-AR-009:** The system SHALL support bad debt provision (TK 2293) with:
- Identification of receivables overdue > 180 days
- Collectibility assessment workflow
- Journal entry: DK 6426 / Co 2293
- Required evidence documentation:
  - Bien ban xac nhan no kho doi
  - Court documents / Police reports / Debt collection records
  - Correspondence with debtor
- Chief Accountant approval required

### 3.4 MOD-04: Accounts Payable

#### 3.4.1 Supplier Management

**SRS-AP-001:** The system SHALL maintain a supplier master database with:
- Supplier name, tax code, address
- Payment terms and bank account details
- Status (active/inactive)

#### 3.4.2 Invoice Processing

**SRS-AP-002:** The system SHALL support supplier invoice processing with:
- OCR data extraction from uploaded invoices
- Manual data entry fallback
- 3-way matching: Purchase Order vs. Goods Receipt vs. Invoice
- Input VAT verification (TK 1331) against e-invoice validity on GDT portal

**SRS-AP-003:** The system SHALL block 3-way match if PO ≠ Goods Receipt ≠ Invoice and SHALL flag the discrepancy for resolution.

**SRS-AP-004:** The system SHALL post the following entry upon invoice approval:
- DK 152, 153, 156, 211, 642... + 1331 (input VAT) / Co 331

#### 3.4.3 Payment Execution

**SRS-AP-005:** The system SHALL support payment request creation with:
- Selection of approved invoices for payment
- Early payment discount calculation
- Approval workflow routing

**SRS-AP-006:** The system SHALL execute payments via:
- Bank transfer: Post DK 331 / Co 112
- Cash payment: Post DK 331 / Co 111

### 3.5 MOD-05: Electronic Invoice

#### 3.5.1 E-Invoice Creation

**SRS-EINV-001:** The system SHALL create electronic invoices per Decree 70/2025 & Circular 32/2025 with:
- Invoices with tax authority code (Co Ma CQT)
- Invoices without tax authority code (Khong Co Ma CQT)
- Mandatory fields per prescribed templates
- Digital signature application

**SRS-EINV-002:** The system SHALL request invoice codes from the Tax Authority API for invoices requiring CQT codes.

**SRS-EINV-003:** The system SHALL support the following invoice types:
- Standard sales invoice
- Commercial discount invoice (Chiet Khau Thuong Mai)
- Returned goods invoice (Hang Ban Tra Lai)
- Internal consumption invoice (Tieu Dung Noi Bo)
- POS-generated invoice (May Tinh Tien)

#### 3.5.2 Invoice Correction

**SRS-EINV-004:** The system SHALL support invoice correction per Decree 70/2025:

| Error Type | Correction Method | Action |
|-----------|------------------|--------|
| Wrong buyer info (name, address, tax code) | Adjustment (Dieu Chinh) | Issue adjustment invoice; original remains valid |
| Wrong amount, tax rate, quantity | Replacement (Thay The) | Issue replacement invoice; original voided |
| Goods returned | Return invoice | Issue return invoice; reduce revenue |

**SRS-EINV-005:** The system SHALL generate required correction documents:
- Bien Ban Dieu Chinh (for adjustments)
- Bien Ban Thay The (for replacements)
- Form 04/SS-HDDT submission to Tax Authority

**SRS-EINV-006:** The system SHALL adjust GL entries when invoices are replaced or adjusted.

#### 3.5.3 VAT Timing

**SRS-EINV-007:** The system SHALL determine VAT timing (thời điểm xác định thuế GTGT) per VAT Law:
- Goods: Time of delivery/transfer of ownership
- Services: Time of service completion
- Construction: Time of payment collection or handover (whichever earlier)
- Export: Time of customs clearance

**SRS-EINV-008:** The system SHALL separate VAT liability date from invoice date — VAT liability may arise before or after invoice issuance.

### 3.6 MOD-06: Tax Management

#### 3.6.1 VAT Management

**SRS-TAX-001:** The system SHALL calculate VAT with the following rates:
- Standard: 10%
- Reduced: 8% (per Resolution 204/2025/QH15, valid 01/07/2025–31/12/2026)
- Reduced: 5% (legacy rate for transitional goods)
- Zero: 0% (exports)
- Non-Taxable: Khong chiu thue

**SRS-TAX-002:** The system SHALL track:
- Input VAT (TK 1331: goods/services, TK 1332: fixed assets)
- Output VAT (TK 33311: output, TK 33312: import)
- Non-deductible input VAT

**SRS-TAX-003:** The system SHALL generate VAT declaration forms:
- Form 01/GTGT (monthly/quarterly)
- Form 04/GTGT (for projects)

**SRS-TAX-004:** The system SHALL calculate VAT payable/refundable:
- If Output VAT > Input VAT: Generate payable entry DK 3331 / Co 112 (when paid)
- If Input VAT > Output VAT: Generate refund receivable DK 1388 / Co 3331

#### 3.6.2 Corporate Income Tax (CIT)

**SRS-TAX-005:** The system SHALL calculate quarterly provisional CIT:
- Quarterly Revenue – Quarterly Deductible Expenses = Quarterly Profit
- If Profit > 0: Apply CIT rate (20% standard or preferential)
- Generate Form 01A/TNDN for quarterly filing
- Post entry: DK 8211 / Co 3334

**SRS-TAX-006:** The system SHALL support annual CIT finalization:
- Form 03/TNDN
- Deductible vs. non-deductible expense classification
- Loss carryforward tracking (Phu Luc 03-2/TNDN)
- TK 821 breakdown: 8211 (current), 8212 (deferred)

**SRS-TAX-007:** The system SHALL support global minimum tax:
- TK 82111: Standard CIT
- TK 82112: Supplementary global minimum tax
- Per NQ 107/2023/QH15, NĐ 18/2024/ND-CP, NĐ 320/2025/ND-CP

#### 3.6.3 Personal Income Tax (PIT)

**SRS-TAX-008:** The system SHALL calculate PIT withholding with:
- Personal deduction: 11,000,000 VND/month
- Dependent deduction: 4,400,000 VND/dependent/month
- Progressive tax rates per Law 109/2025/QH15
- Formula: (Gross – Insurance – Deductions) × Tax Rate

**SRS-TAX-009:** The system SHALL generate PIT declaration forms:
- Form 02/KK-TNCN (monthly/quarterly)
- Form 05/QTT-TNCN (annual finalization)
- Post entry: DK 334 / Co 3335

#### 3.6.4 License Fee & Foreign Contractor Tax

**SRS-TAX-010:** The system SHALL calculate License Fee (Le Phi Mon Bai) with tiered rates based on charter capital.

**SRS-TAX-011:** The system SHALL calculate Foreign Contractor Tax (Thue Nha Thau) with VAT and CIT components on foreign contractor payments.

#### 3.6.5 Tax Calendar

**SRS-TAX-012:** The system SHALL maintain a tax calendar with deadline alerts:
- VAT Monthly: 20th of following month
- VAT Quarterly: Last day of first month of next quarter
- CIT Quarterly: Last day of first month of next quarter
- PIT Monthly: 20th of following month
- PIT Quarterly: Last day of first month of next quarter
- Annual BCTC: Within 90 days of fiscal year-end
- Quarterly BCTC: Within 30 days of quarter-end

**SRS-TAX-013:** The system SHALL alert the Tax Accountant and Chief Accountant 7 days and 1 day before each deadline.

### 3.7 MOD-07: Financial Reporting

#### 3.7.1 Mandatory Financial Statements

**SRS-RPT-001:** The system SHALL generate the following Circular 99 financial statements:

| Form | Name | Vietnamese | Frequency |
|------|------|-----------|-----------|
| B01-DN | Statement of Financial Position | Bao Cao Tinh Hinh Tai Chinh | Annual/Quarterly |
| B02-DN | Statement of Business Results | Bao Cao Ket Qua HDKD | Annual/Quarterly |
| B03-DN | Cash Flow Statement | Bao Cao Luu Chuyen Tien Te | Annual/Quarterly |
| B09-DN | Notes to Financial Statements | Thuyet Minh BCTC | Annual/Quarterly |
| B01-DNKLT | For small & micro enterprises | — | Annual |
| B09-DNKLT | Notes for small & micro | — | Annual |

**SRS-RPT-002:** The system SHALL map account balances to BCTC line items per the official Circular 99 templates (see Appendix A for full mapping).

**SRS-RPT-003:** The system SHALL enforce presentation principles per Circular 99:
- Going concern assumption
- Consistency
- Accrual basis
- Materiality
- Offsetting prohibition
- Comparative information (current period vs. prior period)

**SRS-RPT-004:** The system SHALL support interim financial reports (Bao Cao Giua Nien Do).

**SRS-RPT-005:** The system SHALL support financial statement amendment/supplement workflow with version tracking.

#### 3.7.2 Management Reports

**SRS-RPT-006:** The system SHALL generate the following management reports:
- Trial Balance (Can Doi So Phat Sinh)
- Account Detail Reports (So Chi Tiet)
- AR/AP Aging Reports
- Inventory Valuation Report
- Fixed Asset Register & Depreciation Report
- Cash Flow Report
- Revenue & Expense Analysis
- Budget vs. Actual Report
- Tax Reconciliation Report

#### 3.7.3 B01-DN Account Mapping (Summary)

| B01-DN Section | Source Accounts |
|---------------|-----------------|
| A. Tai San Ngan Han | 111, 112, 113, 121, 128, 131, 133, 136, 138, 141, 151-158, 242 |
| I. Tien va tuong duong tien | 111, 112, 113 |
| II. Dau tu tai chinh ngan han | 121, 128 |
| III. Cac khoan phai thu ngan han | 131, 136, 138, 141 (less 2293) |
| IV. Hang ton kho | 151-158 (less 2294) |
| B. Tai San Dai Han | 211-217, 221, 222, 228, 229, 241, 243, 244 |
| A. No Phai Tra Ngan Han | 331-338, 341, 343, 344, 352 |
| B. No Phai Tra Dai Han | 341, 343, 347, 352 (long-term portion) |
| C. Von Chu So Huu | 411-421 |
| D. Quy Binh On Gia | 357 |

#### 3.7.4 B02-DN Account Mapping (Summary)

| B02-DN Line | Source | Calculation |
|------------|--------|-------------|
| 01. Doanh thu ban hang va CCDV | 511 | Credit turnover |
| 02. Cac khoan giam tru doanh thu | 521 | Debit turnover |
| 10. Doanh thu thuan | 01 - 02 | Net revenue |
| 11. Gia von hang ban | 632 | Debit turnover |
| 20. Loi nhuan gop | 10 - 11 | Gross profit |
| 21. Doanh thu HD tai chinh | 515 | Credit turnover |
| 22. Chi phi tai chinh | 635 | Debit turnover |
| 25. Chi phi ban hang | 641 | Debit turnover |
| 26. Chi phi QLDN | 642 | Debit turnover |
| 27. Trong do: Chi phi du phong | 6426 | Detail from 642 |
| 30. Loi nhuan thuan tu HDKD | 20+21-22-25-26 | Operating profit |
| 31. Thu nhap khac | 711 | Credit turnover |
| 32. Chi phi khac | 811 | Debit turnover |
| 50. Loi nhuan ke toan truoc thue | 30 + (31-32) | Profit before tax |
| 51. Chi phi thue TNDN hien hanh | 8211 | Debit turnover |
| 51.1. Chi phi thue TNDN thong thuong | 82111 | Detail from 8211 |
| 51.2. Chi phi thue TNDN bo sung (toithieu toan cau) | 82112 | Detail from 8211 |
| 52. Chi phi thue TNDN hoan lai | 8212 | Debit turnover |
| 60. LOI NHUAN SAU THUE | 50-51-52 | Net profit |

### 3.8 MOD-08: Accounting Books

**SRS-BOOK-001:** The system SHALL maintain all required accounting books per Circular 99:
- General Journal (So Nhat Ky Chung)
- General Ledger (So Cai Tai Khoan)
- Subsidiary Ledgers (So Chi Tiet) — per account
- Fixed Asset Register (So Theo Doi TSCD)
- Inventory Cards (The Kho)

**SRS-BOOK-002:** All accounting books SHALL be printable in official Circular 99 formats.

### 3.9 MOD-09: Bank & Cash

#### 3.9.1 Cash Management

**SRS-CASH-001:** The system SHALL manage cash accounts:
- TK 111: Cash on hand (Tien Mat)
- TK 112: Demand deposits (Tien Gui Khong Ky Han)
- TK 113: Cash in transit (Tien Dang Chuyen)
- TK 1281: Term deposits (Tien Gui Co Ky Han)

**SRS-CASH-002:** The system SHALL support cash receipt vouchers (01-TT) and cash payment vouchers (02-TT).

#### 3.9.2 Bank Reconciliation

**SRS-CASH-003:** The system SHALL support bank reconciliation with:
- Bank statement import (MT940, CSV, Excel)
- Auto-matching transactions by amount, date, reference
- Manual matching for unmatched items
- Reconciliation difference calculation
- Mark period as reconciled when difference = 0

**SRS-CASH-004:** The system SHALL target ≥85% auto-match rate for bank reconciliation.

#### 3.9.3 Cashless Payments

**SRS-CASH-005:** The system SHALL support cashless payments per Decree 52/2024/ND-CP, including bank transfer initiation via banking APIs.

### 3.10 MOD-10: Payroll

#### 3.10.1 Salary Calculation

**SRS-PAY-001:** The system SHALL calculate gross salary with:
- Basic salary, allowances, bonuses
- Overtime calculation per Labor Law
- Attendance-based adjustments

#### 3.10.2 Mandatory Contributions

**SRS-PAY-002:** The system SHALL calculate mandatory contributions per 2026 statutory rates:

| Contribution | Employer Rate | Employee Rate | Base |
|-------------|--------------|--------------|------|
| BHXH (Social Insurance) | 14% | 8% | Social insurance wage base |
| BHYT (Health Insurance) | 3% | 1.5% | Social insurance wage base |
| BHTN (Unemployment Insurance) | 1% | 1% | Social insurance wage base |
| BHTNLĐ-BNN (Occupational Accident) | 0.5% | 0% | Social insurance wage base |
| **Subtotal** | **18.5%** | **10.5%** | |
| KPCD (Union Fee) | 2% | 0% | Social insurance wage base |
| **Total Employer** | **20.5%** | | |

**SRS-PAY-003:** The system SHALL cap the insurance base at 20× the base salary (per BHXH regulations).

#### 3.10.3 PIT Withholding

**SRS-PAY-004:** The system SHALL calculate PIT withholding per SRS-TAX-008 and post entry: DK 334 / Co 3335.

#### 3.10.4 Payroll Posting

**SRS-PAY-005:** The system SHALL post the following payroll entries:
- DK 642, 622, 641... / Co 334 (net salary)
- DK 642, 622, 641... / Co 3383 (BHXH 14% employer)
- DK 642, 622, 641... / Co 3384 (BHYT 3% employer)
- DK 642, 622, 641... / Co 3386 (BHTN 1% employer)
- DK 642, 622, 641... / Co 3382 (KPCD 2%)
- DK 642, 622, 641... / Co 3335 (PIT withholding)

#### 3.10.5 Payslips & Declarations

**SRS-PAY-006:** The system SHALL generate:
- Individual payslips (digital distribution via email/portal)
- Bang Thanh Toan Tien Luong (salary payment table)
- Bang Phan Bo Tien Luong (salary allocation table)
- Insurance declaration files (e-BHXH format)
- PIT declaration (02/KK-TNCN)

### 3.11 MOD-11: Fixed Assets

**SRS-FA-001:** The system SHALL manage fixed assets:
- TK 211: Tangible fixed assets
- TK 212: Finance leased assets
- TK 213: Intangible fixed assets
- TK 214: Accumulated depreciation
- TK 215: Biological assets
- TK 217: Investment property

**SRS-FA-002:** The system SHALL calculate depreciation using:
- Straight-line method (Duong Thang)
- Declining balance method (So Du Giam Dan)
- Units of production method (Theo So Luong San Pham)

**SRS-FA-003:** The system SHALL start depreciation from the month **following** the month the asset is put into use (da dua vao su dung).

**SRS-FA-004:** The system SHALL post monthly depreciation:
- DK 6274, 6424, 6414... / Co 2141, 2142, 2143

**SRS-FA-005:** The system SHALL support asset lifecycle events:
- Registration (01-TSCD)
- Transfer/modification (03-TSCD)
- Liquidation (Bien Ban Thanh Ly)
- Revaluation (Bien Ban Danh Gia Lai)
- Inventory (05-TSCD)

**SRS-FA-006:** The system SHALL post asset disposal entries:
- DK 214 (accumulated depreciation)
- DK 811 (loss) / Co 711 (gain)
- DK 111, 112 (proceeds)
- Co 211, 212, 213 (original cost)

### 3.12 MOD-12: Inventory

**SRS-INV-001:** The system SHALL manage inventory accounts:
- TK 151: Goods in transit
- TK 152: Raw materials
- TK 153: Tools & supplies
- TK 154: Work in progress
- TK 155: Finished goods
- TK 156: Merchandise
- TK 157: Goods sent for sale
- TK 158: Materials in bonded warehouse

**SRS-INV-002:** The system SHALL support inventory valuation methods:
- FIFO (First In, First Out)
- Weighted average (Binh Quan Gia)
- Specific identification (Thuc Te Tung Lo)

**SRS-INV-003:** The system SHALL calculate inventory provisions (TK 2294) when Net Realizable Value < Cost:
- Annual assessment
- Provision = Cost – NRV – Previously provided amount
- Increase: DK 632 / Co 2294
- Decrease: DK 2294 / Co 632

**SRS-INV-004:** The system SHALL support material/supply allocation (Bang Phan Bo Nguyen Lieu, Vat Lieu, CCDC).

### 3.13 MOD-13: Data Migration

**SRS-MIG-001:** The system SHALL support balance transfer from Circular 200 to Circular 99 per Article 19 of Circular 99:

| Source (TT200) | Target (TT99) | Description |
|---------------|--------------|-------------|
| TK 111, 112, 113 (detail) | TK 111, 112, 113 (detail) | Direct transfer |
| TK 138 (BCC contribution) | TK 2281 | Investment in other entities |
| TK 2413 (upgrade portion) | TK 2414 | Asset upgrade costs |
| TK 338 (dividends detail) | TK 332 | Dividends payable |
| TK 441 + TK 466 | TK 4118 | Other capital |
| TK 421 | TK 421 | Retained earnings (direct) |
| TK 347 | TK 347 | Deferred tax liability (direct) |

**SRS-MIG-002:** The system SHALL support balance transfer from Circular 133 to Circular 99.

**SRS-MIG-003:** The system SHALL generate a migration verification report comparing pre- and post-migration balances.

**SRS-MIG-004:** The system SHALL support parallel run comparison (old system vs. new system) before cutover.

### 3.14 MOD-14: Digital Signature

**SRS-DS-001:** The system SHALL integrate with digital signature providers (chữ ký số) for:
- E-invoice signing (mandatory per Decree 70/2025)
- Electronic tax declaration submission (mandatory per Tax Admin Law)

**SRS-DS-002:** The system SHALL support multiple digital signature providers:
- VNPT-CA
- Viettel-CA
- BKAV-CA
- Safe-CA

### 3.15 MOD-15: Accounting Policy

**SRS-AP-001:** The system SHALL manage the Accounting Policy Document (Quy chế hạch toán) as required per Article 11 of Circular 99.

**SRS-AP-002:** The system SHALL store justification documentation for all custom account additions.

**SRS-AP-003:** The system SHALL link each custom account to its policy justification.

### 3.16 Exchange Rate Revaluation

**SRS-FX-001:** The system SHALL perform period-end exchange rate revaluation for all monetary items in foreign currency:
- Cash (TK 112 foreign currency)
- Receivables (TK 131, 136, 138 foreign currency)
- Payables (TK 331, 336, 338, 341 foreign currency)
- Loans (TK 341 foreign currency)

**SRS-FX-002:** The system SHALL record exchange rate differences to TK 413:
- Gain: DK 111, 112, 131... / Co 413
- Loss: DK 413 / Co 111, 112, 331...

**SRS-FX-003:** The system SHALL use State Bank of Vietnam (SBV) closing exchange rate for revaluation.

### 3.17 Revenue Recognition

**SRS-REV-001:** The system SHALL recognize revenue per VAS 14 when control of goods/services transfers to the customer, not when invoiced.

**SRS-REV-002:** The system SHALL support percentage-of-completion revenue recognition for construction contracts (TK 337).

**SRS-REV-003:** The system SHALL track unearned revenue (TK 3387) and recognize over time.

### 3.18 Lease Accounting

**SRS-LEASE-001:** The system SHALL support finance lease accounting:
- Lessee: Recognize leased asset (TK 212) and lease liability (TK 3412)
- Lessor: Track lease receivable and interest income

**SRS-LEASE-002:** The system SHALL calculate and post lease depreciation (DK 6274, 6424... / Co 2142) and interest expense (DK 635 / Co 3412).

### 3.19 CCDC Allocation

**SRS-CCDC-001:** The system SHALL perform period-end CCDC (Tools & Equipment) allocation from TK 242:
- Monthly allocation = Original Cost / Allocation Period (months)
- Production: DK 6273 / Co 242
- Sales: DK 6413 / Co 242
- Management: DK 6423 / Co 242

### 3.20 Construction Progress Accounting

**SRS-CONST-001:** The system SHALL support construction progress accounting (TK 337) for construction enterprises, tracking progress payments and revenue recognition by completion percentage.

---

## 4. EXTERNAL INTERFACE REQUIREMENTS

### 4.1 User Interfaces

**SRS-UI-001:** The system SHALL provide a web-based interface in Vietnamese language.

**SRS-UI-002:** The system SHALL support Vietnamese number formatting (1.234.567,89) and English number formatting (1,234,567.89).

**SRS-UI-003:** The system SHALL enable users to complete a standard journal entry within 3 clicks from the dashboard.

**SRS-UI-004:** The system SHALL provide role-specific dashboards for each user class (UC-01 through UC-13).

### 4.2 Hardware Interfaces

Not applicable (cloud-based SaaS).

### 4.3 Software Interfaces

#### 4.3.1 Tax Authority (GDT) API

**SRS-API-001:** The system SHALL communicate with the GDT e-filing portal via HTTPS REST API using XML format.

**SRS-API-002:** The system SHALL authenticate using digital certificates.

**SRS-API-003:** The system SHALL support:
- Tax declaration submission (VAT, CIT, PIT)
- Invoice data submission for CQT code generation
- Receipt of submission confirmations and validation responses

#### 4.3.2 E-Invoice Provider API

**SRS-API-004:** The system SHALL communicate with e-invoice providers (VNPT, Viettel, BKAV, Safe-CA) via HTTPS REST API using JSON/XML.

**SRS-API-005:** The system SHALL authenticate using API key + digital signature.

#### 4.3.3 Banking API

**SRS-API-006:** The system SHALL import bank statements via SFTP in MT940, CSV, or Excel format (daily).

**SRS-API-007:** The system SHALL initiate payments via HTTPS API using JSON/XML with OAuth 2.0 + digital signature authentication.

#### 4.3.4 Social Insurance (e-BHXH)

**SRS-API-008:** The system SHALL generate social insurance declaration files in e-BHXH XML format (monthly).

**SRS-API-009:** The system SHALL authenticate using digital certificates.

#### 4.3.5 Time Tracking System

**SRS-API-010:** The system SHALL import attendance data via HTTPS REST API in JSON format (daily).

#### 4.3.6 HTKK Export

**SRS-API-011:** The system SHALL export tax declaration data in HTKK-compatible XML format.

### 4.4 Communication Interfaces

**SRS-COM-001:** All external communications SHALL use TLS 1.3 encryption.

**SRS-COM-002:** All API responses SHALL be validated against defined schemas before processing.

---

## 5. NON-FUNCTIONAL REQUIREMENTS

### 5.1 Performance

**SRS-PERF-001:** The system SHALL process up to 50,000 journal entries per hour.

**SRS-PERF-002:** Financial statement generation SHALL complete within 30 seconds for enterprises with up to 1 million transactions per year.

**SRS-PERF-003:** The system SHALL support concurrent access by 100+ users.

**SRS-PERF-004:** Page load time SHALL not exceed 3 seconds for standard operations.

### 5.2 Availability

**SRS-AVAIL-001:** System availability SHALL be 99.9% during business hours (7:00–22:00, Monday–Saturday).

**SRS-AVAIL-002:** Scheduled maintenance SHALL NOT be performed during peak tax filing periods (last 5 days of monthly/quarterly filing deadlines).

### 5.3 Scalability

**SRS-SCALE-001:** The system SHALL support enterprises from micro (under 10 employees) to large (1,000+ employees).

**SRS-SCALE-002:** The database SHALL support up to 10 years of historical data without performance degradation.

### 5.4 Security

**SRS-SEC-001:** The system SHALL encrypt data at rest using AES-256.

**SRS-SEC-002:** The system SHALL encrypt data in transit using TLS 1.3.

**SRS-SEC-003:** User passwords SHALL be hashed using bcrypt.

**SRS-SEC-004:** Digital signatures SHALL use SHA-256 + RSA-2048.

**SRS-SEC-005:** The system SHALL classify data into four levels:
- Public: Company name, address, tax code
- Internal: Chart of accounts, policies
- Confidential: Journal entries, invoices, reports (encrypted at rest)
- Restricted: Employee salaries, bank accounts, passwords (encrypted at rest + in transit)

### 5.5 Auditability

**SRS-AUDIT-001:** The system SHALL log all data modifications with: user ID, timestamp, old value, new value.

**SRS-AUDIT-002:** The system SHALL maintain an immutable audit trail for all financial transactions.

**SRS-AUDIT-003:** Audit logs SHALL be retained for a minimum of 10 years per Accounting Law.

**SRS-AUDIT-004:** The system SHALL provide auditor read-only access with exportable audit trail reports.

### 5.6 Reliability

**SRS-REL-001:** The system SHALL implement automatic failover with Recovery Time Objective (RTO) < 1 hour.

**SRS-REL-002:** The system SHALL implement Recovery Point Objective (RPO) < 15 minutes.

### 5.7 Maintainability

**SRS-MAINT-001:** Tax rate changes SHALL be configurable without code deployment (via admin panel).

**SRS-MAINT-002:** The system SHALL support hot-swapping of e-invoice provider integrations.

---

## 6. DATA REQUIREMENTS

### 6.1 Data Retention

**SRS-DATA-001:** The system SHALL retain data per Nghị định 43/2025/ND-CP:

| Document Type | Retention | Classification |
|--------------|-----------|---------------|
| Accounting ledgers (So Cai, So Nhat Ky) | Permanent | Type A |
| Financial statements (B01-B09) | Permanent | Type A |
| Fixed asset records | Permanent | Type A |
| Tax declarations | 10 years | Type B |
| E-invoices | 10 years | Type B |
| Payroll records | 10 years | Type B |
| Bank statements | 10 years | Type B |
| Journal entry supporting docs | 10 years | Type B |
| Vouchers (Phieu thu/chi) | 10 years | Type B |
| Employee contracts | 5 years after termination | Type C |
| Attendance records | 5 years | Type C |
| Audit logs | 10 years | Type B |

**SRS-DATA-002:** The system SHALL implement tiered archival:
- Online storage: 0–5 years (immediate access)
- Cold storage: 5+ years (retrievable within 24 hours)

### 6.2 Data Validation

**SRS-DATA-003:** The system SHALL enforce all validation rules defined in Section 3 (VR-GL-01 through VR-GL-07) and the following:

| Rule ID | Validation | Error Message |
|---------|-----------|--------------|
| VR-INV-01 | Buyer tax code 10-13 digits | "Invalid tax code format" |
| VR-INV-02 | Invoice number sequential | "Invoice number gap detected" |
| VR-INV-03 | VAT rate valid (0/5/8/10/NonTaxable) | "Invalid VAT rate" |
| VR-INV-04 | Total = Sum(lines) + VAT | "Total calculation mismatch" |
| VR-INV-05 | Invoice date not in future | "Invoice date cannot be in the future" |
| VR-TAX-01 | Declaration filed before deadline | "Filing deadline has passed" |
| VR-TAX-02 | All required fields populated | "Required field {field} is empty" |
| VR-TAX-03 | VAT input matches verified invoices | "Input VAT mismatch with verified invoices" |
| VR-TAX-04 | CIT = (Revenue - Expenses) × Rate | "CIT calculation error" |
| VR-PAY-01 | Gross salary ≥ minimum wage | "Salary below minimum wage" |
| VR-PAY-02 | Insurance base ≤ 20× base salary | "Insurance base exceeds cap" |
| VR-PAY-03 | Dependent deduction = 4.4M × N | "Dependent deduction mismatch" |
| VR-PAY-04 | Net = Gross - Insurance - PIT | "Net salary calculation error" |

### 6.3 Data Export

**SRS-DATA-004:** The system SHALL support data export in Excel, PDF, and CSV formats.

---

## 7. BUSINESS RULES

### 7.1 Accounting Rules

**BR-001:** All journal entries SHALL balance (total debit = total credit).
**BR-002:** No posting to closed periods without Chief Accountant override.
**BR-003:** Voucher numbers SHALL be sequential with no gaps per period.
**BR-004:** Custom accounts SHALL NOT alter financial statement line items.
**BR-005:** Revenue recognition SHALL follow VAS 14 (control transfer, not invoicing).

### 7.2 Tax Rules

**BR-006:** VAT rates: 10% (standard), 8% (reduced per NQ 204/2025), 5% (transitional), 0% (export), Non-Taxable.
**BR-007:** Input VAT is deductible only if the e-invoice is valid on the GDT portal.
**BR-008:** CIT rate: 20% standard (or preferential per enterprise category).
**BR-009:** PIT personal deduction: 11M VND/month; dependent deduction: 4.4M VND/dependent/month.
**BR-010:** VAT filing deadlines: Monthly = 20th of following month; Quarterly = last day of first month of next quarter.

### 7.3 Payroll Rules

**BR-011:** Employee insurance: BHXH 8% + BHYT 1.5% + BHTN 1% = 10.5%.
**BR-012:** Employer insurance: BHXH 14% + BHYT 3% + BHTN 1% + BHTNLĐ-BNN 0.5% = 18.5%.
**BR-013:** KPCD: 2% on social insurance wage base (not actual salary).
**BR-014:** Insurance base capped at 20× base salary.

### 7.4 Internal Control Rules

**BR-015:** No user SHALL approve their own transactions (Maker-Checker).
**BR-016:** Purchaser SHALL NOT approve PO; AP SHALL NOT execute payment (Segregation of Duties).
**BR-017:** Invoices > 5M VND SHALL have scanned attachments.
**BR-018:** All approvals SHALL be logged with timestamp, IP, and device ID.

---

## 8. REGULATORY COMPLIANCE REQUIREMENTS

### 8.1 Accounting Law

**SRS-RC-001:** The system SHALL comply with Vietnam Accounting Law (Luật Kế Toán).
**SRS-RC-002:** The system SHALL comply with Vietnamese Accounting Standards (VAS).
**SRS-RC-003:** The system SHALL comply with Circular 99/2025/TT-BTC effective 01/01/2026.

### 8.2 Tax Law

**SRS-RC-004:** VAT calculations SHALL comply with Law 149/2025/QH15, Decree 181/2025, Decree 359/2025, Circular 69/2025.
**SRS-RC-005:** CIT calculations SHALL comply with Law 67/2025/QH15, Decree 320/2025.
**SRS-RC-006:** PIT calculations SHALL comply with Law 109/2025/QH15 (effective 01/07/2026).
**SRS-RC-007:** Tax administration SHALL comply with Law 108/2025/QH15, Decree 373/2025.
**SRS-RC-008:** Tax penalties SHALL comply with Decree 310/2025.

### 8.3 E-Invoice Compliance

**SRS-RC-009:** Electronic invoices SHALL comply with Decree 70/2025, Circular 32/2025.
**SRS-RC-010:** Invoice format, content, and numbering SHALL follow prescribed templates.

### 8.4 Data Retention

**SRS-RC-011:** Accounting document retention SHALL comply with Nghị định 43/2025/ND-CP (Type A/B/C classification).
**SRS-RC-012:** Electronic storage SHALL meet legal validity requirements per Nghị định 43/2025/ND-CP.

---

## 9. SYSTEM CONSTRAINTS

| Constraint | Description |
|-----------|-------------|
| CON-01 | Data sovereignty: All data stored in Vietnam |
| CON-02 | Vietnamese language UI mandatory |
| CON-03 | VAS compliance mandatory |
| CON-04 | Double-entry bookkeeping mandatory |
| CON-05 | Period lock irreversible without CA override |
| CON-06 | Sequential voucher numbering, no gaps |
| CON-07 | Digital signature mandatory for e-invoice and tax filing |

---

## 10. TRACEABILITY MATRIX

| SRS ID | Source BR | Source FR | Source Workflow | Test Case Prefix |
|--------|-----------|-----------|----------------|-----------------|
| SRS-ADM-001 to 006 | BR-GL-04 | SR-001 to SR-009 | WORKFLOW §13.1 | TC-ADM-xxx |
| SRS-ADM-007 to 010 | BR-GL-01 | FR-001 to FR-004 | WORKFLOW §2.2 | TC-ADM-xxx |
| SRS-ADM-011 to 014 | BR-GL-04 | — | WORKFLOW §2.3 | TC-ADM-xxx |
| SRS-ADM-015 to 017 | BR-GL-03 | FR-011 | DATA_FLOW §14.1 | TC-ADM-xxx |
| SRS-ADM-018 to 021 | — | DR-005 | WORKFLOW §13.2 | TC-ADM-xxx |
| SRS-GL-001 to 006 | BR-GL-01, 02, 05 | FR-008 to FR-012 | WORKFLOW §2.1 | TC-GL-xxx |
| SRS-GL-007 to 008 | BR-RPT-06 | FR-047 | WORKFLOW §2.3 | TC-GL-xxx |
| SRS-GL-009 to 010 | BR-AP-02 | FR-031 | WORKFLOW §9B.4 | TC-GL-xxx |
| SRS-AR-001 to 002 | BR-AR (implicit) | FR-013 | PROCESS_FLOWS §3 | TC-AR-xxx |
| SRS-AR-003 to 005 | BR-EINV-01 | FR-037, FR-052 | WORKFLOW §3.1 | TC-AR-xxx |
| SRS-AR-006 to 007 | BR-AR (implicit) | FR-013 | WORKFLOW §3.2 | TC-AR-xxx |
| SRS-AR-008 to 009 | BR-AR (implicit) | FR-013 | WORKFLOW §3.3 | TC-AR-xxx |
| SRS-AP-001 to 004 | BR-AP (implicit) | FR-016 to FR-018 | WORKFLOW §4.1 | TC-AP-xxx |
| SRS-AP-005 to 006 | BR-AP (implicit) | FR-016 | WORKFLOW §4.2 | TC-AP-xxx |
| SRS-EINV-001 to 003 | BR-EINV-01 to 06 | FR-037 | WORKFLOW §6.1 | TC-EINV-xxx |
| SRS-EINV-004 to 006 | BR-EINV-02, 03 | FR-037 | WORKFLOW §6.2, 6.3 | TC-EINV-xxx |
| SRS-EINV-007 to 008 | BR-EINV (implicit) | FR-057, FR-058 | WORKFLOW §3.1 | TC-EINV-xxx |
| SRS-TAX-001 to 004 | BR-TAX-01, 02 | FR-032 | WORKFLOW §5.1 | TC-TAX-xxx |
| SRS-TAX-005 to 007 | BR-TAX-03, 07 | FR-033 | WORKFLOW §5.2 | TC-TAX-xxx |
| SRS-TAX-008 to 009 | BR-TAX-04 | FR-034 | WORKFLOW §5.3 | TC-TAX-xxx |
| SRS-TAX-010 to 011 | BR-TAX-05, 06 | FR-035, FR-036 | — | TC-TAX-xxx |
| SRS-TAX-012 to 013 | BR-TAX-08 | — | USER_JOURNEY §3 | TC-TAX-xxx |
| SRS-RPT-001 to 005 | BR-RPT-01 to 05 | FR-043 to FR-046 | WORKFLOW §11.1 | TC-RPT-xxx |
| SRS-RPT-006 | BR-RPT (implicit) | RR-009 to RR-017 | DATA_FLOW §14.2 | TC-RPT-xxx |
| SRS-BOOK-001 to 002 | BR-BOOK (implicit) | FR-047 | — | TC-BOOK-xxx |
| SRS-CASH-001 to 002 | BR-CASH (implicit) | FR-040 | WORKFLOW §10.2 | TC-CASH-xxx |
| SRS-CASH-003 to 004 | BR-CASH (implicit) | FR-041 | WORKFLOW §10.1 | TC-CASH-xxx |
| SRS-CASH-005 | BR-CASH (implicit) | FR-042 | — | TC-CASH-xxx |
| SRS-PAY-001 | BR-PAY-01 | FR-026 | WORKFLOW §7.1 | TC-PAY-xxx |
| SRS-PAY-002 to 003 | BR-PAY-02, 02a, 07 | FR-027 | WORKFLOW §7.1 | TC-PAY-xxx |
| SRS-PAY-004 | BR-PAY-04 | FR-026 | WORKFLOW §5.3 | TC-PAY-xxx |
| SRS-PAY-005 | BR-PAY (implicit) | FR-026 | WORKFLOW §7.1 | TC-PAY-xxx |
| SRS-PAY-006 | BR-PAY (implicit) | FR-028 | USER_JOURNEY §6 | TC-PAY-xxx |
| SRS-FA-001 to 006 | BR-FA-01 to 04 | FR-023 to FR-025 | WORKFLOW §8 | TC-FA-xxx |
| SRS-INV-001 to 004 | BR-INV-01 to 04 | FR-019 to FR-022 | WORKFLOW §9, 9B.3 | TC-INV-xxx |
| SRS-MIG-001 to 004 | BR-GL-06 | FR-048 | USER_JOURNEY §10 | TC-MIG-xxx |
| SRS-DS-001 to 002 | BR-DS-01 to 03 | — | WORKFLOW §6.1 | TC-DS-xxx |
| SRS-AP-001 to 003 | BR-AP-01 | FR-003 | WORKFLOW §2.2 | TC-AP-xxx |
| SRS-FX-001 to 003 | BR-AP-03 | FR-049 to FR-051 | WORKFLOW §9B.1 | TC-FX-xxx |
| SRS-REV-001 to 003 | — | FR-052 to FR-054 | — | TC-REV-xxx |
| SRS-LEASE-001 to 002 | — | FR-055, FR-056 | — | TC-LEASE-xxx |
| SRS-CCDC-001 | BR-AP-04 | FR-022 | WORKFLOW §9B.2 | TC-CCDC-xxx |
| SRS-CONST-001 | BR-AP-05 | — | — | TC-CONST-xxx |

---

## 11. GLOSSARY & ABBREVIATIONS

| Term | Vietnamese | English |
|------|-----------|---------|
| TKKT | Tài Khoản Kế Toán | Chart of Accounts |
| BCTC | Báo Cáo Tài Chính | Financial Statements |
| CĐPS | Cân Đối Phát Sinh | Trial Balance |
| HĐĐT | Hóa Đơn Điện Tử | Electronic Invoice |
| TSCĐ | Tài Sản Cố Định | Fixed Assets |
| CCDC | Công Cụ Dụng Cụ | Tools & Equipment |
| HTK | Hàng Tồn Kho | Inventory |
| NCC | Nhà Cung Cấp | Supplier |
| KH | Khách Hàng | Customer |
| PNK | Phiếu Nhập Kho | Goods Receipt Note |
| PXK | Phiếu Xuất Kho | Goods Issue Note |
| PT | Phiếu Thu | Cash Receipt Voucher |
| PC | Phiếu Chi | Cash Payment Voucher |
| BHXH | Bảo Hiểm Xã Hội | Social Insurance |
| BHYT | Bảo Hiểm Y Tế | Health Insurance |
| BHTN | Bảo Hiểm Thất Nghiệp | Unemployment Insurance |
| KPCD | Kinh Phí Công Đoàn | Union Fee |
| GTGT | Giá Trị Gia Tăng | Value Added |
| TNDN | Thu Nhập Doanh Nghiệp | Corporate Income |
| TNCN | Thu Nhập Cá Nhân | Personal Income |
| CQT | Cơ Quan Thuế | Tax Authority |

---

## 12. APPENDIX

### Appendix A: Complete B01-DN Account Mapping

| Row Code | B01-DN Line Item | Account(s) | Calculation Method |
|----------|-----------------|------------|-------------------|
| A | TAI SAN NGAN HAN | 111,112,113,121,128,131,133,136,138,141,151-158,242 | Sum of debit balances |
| A.I | Tien va tuong duong tien | 111, 112, 113 | Sum |
| A.II | Dau tu tai chinh ngan han | 121, 128 | Sum |
| A.III | Cac khoan phai thu ngan han | 131, 136, 138, 141 | Sum minus 2293 |
| A.IV | Hang ton kho | 151, 152, 153, 154, 155, 156, 157, 158 | Sum minus 2294 |
| B | TAI SAN DAI HAN | 211-217,221,222,228,229,241,243,244 | Sum of debit balances |
| B.I | TSCD | 211, 212, 213, 214, 215, 217 | Net book value (cost - accum. depr.) |
| B.II | Dau tu tai chinh dai han | 221, 222, 228 | Sum minus 2291, 2292, 2295 |
| B.III | Tai san thue TNDN hoan lai | 243 | Balance |
| B.IV | Tai san dai han khac | 241, 242, 244 | Sum |
| A' | TONG CONG TAI SAN | A + B | Sum |
| C | NO PHAI TRA NGAN HAN | 331-338,341,343,344,352 | Sum of credit balances |
| D | NO PHAI TRA DAI HAN | 341, 343, 347, 352 | Long-term portion only |
| E | VON CHU SO HUU | 411, 412, 413, 414, 418, 419, 421 | Sum of credit balances |
| F | QUY BINH ON GIA | 357 | Balance |
| G | TONG CONG NGUON VON | C + D + E + F | Must equal A' |

### Appendix B: Complete B02-DN Account Mapping

| Row | B02-DN Line Item | Account(s) | Calculation |
|-----|-----------------|------------|-------------|
| 01 | Doanh thu ban hang va CCDV | 511 | Credit turnover |
| 02 | Cac khoan giam tru doanh thu | 521 | Debit turnover |
| 10 | Doanh thu thuan ve BH va CCDV | — | 01 - 02 |
| 11 | Gia von hang ban | 632 | Debit turnover |
| 20 | Loi nhuan gop ve BH va CCDV | — | 10 - 11 |
| 21 | Doanh thu hoat dong tai chinh | 515 | Credit turnover |
| 22 | Chi phi tai chinh | 635 | Debit turnover |
| 23 | Trong do: Chi phi lai vay | 635 (detail) | Detail from 635 |
| 25 | Chi phi ban hang | 641 | Debit turnover |
| 26 | Chi phi quan ly doanh nghiep | 642 | Debit turnover |
| 27 | Trong do: Chi phi du phong | 6426 | Detail from 642 |
| 30 | Loi nhuan thuan tu HDKD | — | 20 + 21 - 22 - 25 - 26 |
| 31 | Thu nhap khac | 711 | Credit turnover |
| 32 | Chi phi khac | 811 | Debit turnover |
| 33 | Trong do: Chi phi phat vi pham hanh chinh | 811 (detail) | Detail from 811 |
| 40 | Loi nhuan khac | — | 31 - 32 |
| 50 | Loi nhuan ke toan truoc thue | — | 30 + 40 |
| 51 | Chi phi thue TNDN hien hanh | 8211 | Debit turnover |
| 51.1 | Chi phi thue TNDN hien hanh thong thuong | 82111 | Detail from 8211 |
| 51.2 | Chi phi thue TNDN bo sung (toi thieu toan cau) | 82112 | Detail from 8211 |
| 52 | Chi phi thue TNDN hoan lai | 8212 | Debit turnover |
| 60 | LOI NHUAN SAU THUE | — | 50 - 51 - 52 |

### Appendix C: Approval Thresholds (Default)

| Transaction Type | Auto-Post Threshold | Requires CA Approval | Requires CFO Approval | Requires CEO Approval |
|-----------------|-------------------|---------------------|---------------------|---------------------|
| Journal Entry | < 100M VND | 100M – 500M VND | 500M – 1B VND | > 1B VND |
| Payment Request | < 50M VND | 50M – 500M VND | 500M – 1B VND | > 1B VND |
| Asset Disposal | Any value | Required | Required | > 500M VND NBV |
| Payroll | < 500M VND total | 500M – 2B VND | 2B – 5B VND | > 5B VND |
| Tax Filing | N/A (always requires review) | Required | Required | Legal Rep signature |
| E-Invoice | < 100M VND | 100M – 500M VND | > 500M VND | N/A |

### Appendix D: Insurance Rate Reference (2026)

| Contribution | Employer | Employee | Total | Legal Basis |
|-------------|----------|----------|-------|-------------|
| BHXH | 14% | 8% | 22% | Luật BHXH 2024 |
| BHYT | 3% | 1.5% | 4.5% | Luật BHYT |
| BHTN | 1% | 1% | 2% | Luật Viec Lam |
| BHTNLĐ-BNN | 0.5% | 0% | 0.5% | Luật ATVSLĐ |
| **Subtotal** | **18.5%** | **10.5%** | **29%** | |
| KPCD | 2% | 0% | 2% | Luật Công đoàn |
| **Total Employer** | **20.5%** | | | |

### Appendix E: VAT Rate Reference

| Rate | Applicability | Legal Basis |
|------|--------------|-------------|
| 10% | Standard rate for most goods/services | Law 149/2025/QH15 |
| 8% | Reduced rate (Resolution 204/2025/QH15, valid 01/07/2025–31/12/2026) | NQ 204/2025/QH15 |
| 5% | Transitional rate for specific goods | Law 149/2025/QH15 |
| 0% | Export goods/services, international transport | Law 149/2025/QH15 |
| Non-Taxable | Financial services, healthcare, education, etc. | Law 149/2025/QH15 |

---

**END OF SOFTWARE REQUIREMENTS SPECIFICATION**

**Document Control:**

| Version | Date | Author | Changes | Approved By |
|---------|------|--------|---------|-------------|
| 1.0 | April 2026 | Lead BA Office | Initial release | — |

**Sign-Off:**

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Lead BA | | | |
| Tech Lead | | | |
| CFO / Project Sponsor | | | |
| Chief Accountant | | | |
| QA Lead | | | |
