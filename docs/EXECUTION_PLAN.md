# EXECUTION PLAN — Vietnamese Enterprise Accounting Software

**Circular 99/2025/TT-BTC Compliant Platform — Phase 1 Detailed Plan**

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Date** | April 2026 |
| **Prepared by** | Project Management Office |
| **Classification** | Confidential |
| **Scope** | Phase 1 (Sprints 1-12, 24 weeks) |
| **Team Size** | 15 FTE |
| **Cadence** | 2-week sprints |

---

## TABLE OF CONTENTS

1. Sprint Backlog (Sprint 1 through Sprint 12)
2. User Story Breakdown with Acceptance Criteria
3. Definition of Ready (DoR)
4. Definition of Done (DoD)
5. QA Strategy
6. CI/CD Pipeline Specification
7. Communication Plan
8. Escalation Matrix
9. Change Management Process
10. Technical Debt Tracking Approach

---

## 1. SPRINT BACKLOG (SPRINT 1 THROUGH SPRINT 12)

### SPRINT 1 — Platform Foundation (Weeks 1-2)

**Theme:** Authentication, RBAC, database infrastructure, CI/CD pipeline

| Story ID | User Story | SRS Ref | Priority | Est. Points | Assignee |
|----------|-----------|---------|----------|-------------|----------|
| US-001 | As a System Admin, I want to create user accounts with roles so that access is controlled | SRS-ADM-001, SRS-ADM-002 | P0 | 8 | BE-1 |
| US-002 | As a user, I want to log in with email/password and 2FA so that my account is secure | SRS-ADM-002, SRS-ADM-005 | P0 | 8 | BE-2 |
| US-003 | As a System Admin, I want to configure IP-based access restrictions so that only authorized networks can access the system | SRS-ADM-006 | P0 | 5 | BE-3 |
| US-004 | As a System Admin, I want session timeout after 30 minutes so that inactive sessions are terminated | SRS-ADM-004 | P0 | 3 | BE-1 |
| US-005 | As a System Admin, I want all login attempts logged so that I can audit access | SRS-ADM-005 | P0 | 5 | BE-2 |
| US-006 | As a DevOps Engineer, I want CI/CD pipeline with lint, test, build so that code quality is enforced | SRS-MAINT-001 | P0 | 8 | DevOps |
| US-007 | As a DevOps Engineer, I want a PostgreSQL database with proper schema so that data is stored reliably | — | P0 | 5 | DevOps |
| US-008 | As a UI/UX Designer, I want base layout templates so that UI is consistent | SRS-UI-001, SRS-UI-002 | P0 | 5 | UX + FE-1 |

**Sprint 1 Total: 47 points**

### SPRINT 2 — Chart of Accounts (Weeks 3-4)

**Theme:** Circular 99 COA loading, custom accounts, period management

| Story ID | User Story | SRS Ref | Priority | Est. Points | Assignee |
|----------|-----------|---------|----------|-------------|----------|
| US-009 | As a Chief Accountant, I want the full Circular 99 COA pre-loaded (71 L1, 101 L2, 10 L3, 2 L4) so that I do not have to configure manually | SRS-ADM-007 | P0 | 8 | BE-1 + Acct SME |
| US-010 | As a Chief Accountant, I want accounts organized into 8 groups so that navigation is intuitive | SRS-ADM-008 | P0 | 5 | BE-1 |
| US-011 | As a Chief Accountant, I want to add custom sub-accounts (L3/L4) with justification docs so that I can tailor the COA per Article 11 | SRS-ADM-009, SRS-ADM-010 | P0 | 8 | BE-2 |
| US-012 | As a Chief Accountant, I want to manage accounting periods (Open/Locked/Closed) so that period integrity is maintained | SRS-ADM-011 to 014 | P0 | 8 | BE-3 |
| US-013 | As a System Admin, I want to import daily exchange rates from SBV so that multi-currency is accurate | SRS-ADM-015 to 017 | P0 | 5 | BE-2 |
| US-014 | As a System Admin, I want daily incremental and weekly full backups so that data is protected | SRS-ADM-018 to 021 | P0 | 5 | DevOps |
| US-015 | As a user, I want role-specific dashboards so that I see relevant information | SRS-UI-004 | P0 | 8 | FE-1 + FE-2 |

**Sprint 2 Total: 47 points**

### SPRINT 3 — GL Engine Core (Weeks 5-6)

**Theme:** Journal entry CRUD, balance enforcement, posting logic

| Story ID | User Story | SRS Ref | Priority | Est. Points | Assignee |
|----------|-----------|---------|----------|-------------|----------|
| US-016 | As an Accountant, I want to create journal entries with debit/credit lines so that I can record transactions | SRS-GL-001, SRS-GL-002 | P0 | 8 | BE-1 |
| US-017 | As the system, I want to enforce total debit = total credit so that entries are always balanced | SRS-GL-001, VR-GL-01 | P0 | 5 | BE-1 |
| US-018 | As the system, I want to validate entries (period open, account exists, amounts > 0, date in period, description required) so that data integrity is maintained | SRS-GL-003, VR-GL-02 to 07 | P0 | 8 | BE-2 |
| US-019 | As an Accountant, I want to post entries and update account balances so that the GL reflects current state | SRS-GL-001 | P0 | 8 | BE-3 |
| US-020 | As an Accountant, I want to create different entry types (daily, recurring, opening, closing, adjustment, reversing) so that all transaction types are supported | SRS-GL-002 | P0 | 5 | BE-2 |
| US-021 | As the system, I want sequential entry numbers with no gaps per period so that audit trail is complete | SRS-GL-006 | P0 | 5 | BE-3 |
| US-022 | As a UI/UX Designer, I want the journal entry screen with real-time balance check and keyboard shortcuts so that data entry is efficient | SRS-UI-003 | P0 | 8 | FE-1 + FE-2 |

**Sprint 3 Total: 47 points**

### SPRINT 4 — GL Advanced (Weeks 7-8)

**Theme:** Multi-currency, approval workflow, trial balance

| Story ID | User Story | SRS Ref | Priority | Est. Points | Assignee |
|----------|-----------|---------|----------|-------------|----------|
| US-023 | As an Accountant, I want to create multi-currency entries with VND equivalent so that foreign transactions are recorded | SRS-GL-004 | P0 | 8 | BE-1 |
| US-024 | As the system, I want to calculate exchange rate differences and record to TK 413 so that FX is accurate | SRS-GL-004, SRS-FX-001 | P0 | 5 | BE-2 |
| US-025 | As a Chief Accountant, I want a Maker-Checker approval workflow for journal entries above threshold so that large entries are reviewed | SRS-GL-005 | P0 | 8 | BE-3 |
| US-026 | As the system, I want to prevent users from approving their own entries so that internal controls are enforced | SRS-GL-005, BR-015 | P0 | 3 | BE-3 |
| US-027 | As a Chief Accountant, I want to generate trial balance for any period so that I can verify GL accuracy | SRS-GL-007, SRS-GL-008 | P0 | 8 | BE-1 |
| US-028 | As an Accountant, I want to view account detail reports (So Chi Tiet) so that I can drill into transactions | SRS-BOOK-001 | P0 | 5 | BE-2 |
| US-029 | As a QA Engineer, I want comprehensive GL test coverage so that posting logic is verified | — | P0 | 5 | QA-1 + QA-2 |

**Sprint 4 Total: 42 points**

### SPRINT 5 — AR Module (Weeks 9-10)

**Theme:** Customer management, invoicing, payment matching, aging

| Story ID | User Story | SRS Ref | Priority | Est. Points | Assignee |
|----------|-----------|---------|----------|-------------|----------|
| US-030 | As an AR Accountant, I want to manage customer master data (name, tax code, address, credit limit, payment terms) so that I can track receivables | SRS-AR-001, SRS-AR-002 | P0 | 5 | BE-1 |
| US-031 | As an AR Accountant, I want to create sales invoices with line items, discounts, and VAT so that I can bill customers | SRS-AR-003 | P0 | 8 | BE-2 |
| US-032 | As the system, I want to recognize revenue (TK 511) when control transfers, not on invoice issuance, per VAS 14 so that revenue is correctly timed | SRS-AR-004, SRS-AR-005 | P0 | 8 | BE-3 |
| US-033 | As an AR Accountant, I want to record payment receipts and auto-match to open invoices so that collections are tracked | SRS-AR-006 | P0 | 8 | BE-1 |
| US-034 | As the system, I want to handle partial payments with FIFO application so that oldest invoices are cleared first | SRS-AR-007 | P0 | 5 | BE-2 |
| US-035 | As an AR Accountant, I want to generate AR aging reports (0-30, 31-60, 61-90, 91-180, 180+ days) so that I can monitor overdue receivables | SRS-AR-008 | P0 | 5 | BE-3 |
| US-036 | As a Chief Accountant, I want to manage bad debt provisions (TK 2293) with evidence documentation so that provisions are compliant | SRS-AR-009 | P0 | 8 | BE-1 |

**Sprint 5 Total: 47 points**

### SPRINT 6 — AP Module (Weeks 11-12)

**Theme:** Supplier management, invoice processing, 3-way match, payment

| Story ID | User Story | SRS Ref | Priority | Est. Points | Assignee |
|----------|-----------|---------|----------|-------------|----------|
| US-037 | As an AP Accountant, I want to manage supplier master data (name, tax code, bank details, payment terms) so that I can track payables | SRS-AP-001 | P0 | 5 | BE-2 |
| US-038 | As an AP Accountant, I want to process supplier invoices with OCR extraction so that data entry is efficient | SRS-AP-002 | P0 | 8 | BE-3 |
| US-039 | As the system, I want to perform 3-way match (PO vs Goods Receipt vs Invoice) and block on discrepancy so that payment accuracy is ensured | SRS-AP-002, SRS-AP-003 | P0 | 8 | BE-1 |
| US-040 | As the system, I want to verify input VAT (TK 1331) against e-invoice validity on GDT portal so that only deductible VAT is recorded | SRS-AP-002 | P0 | 5 | BE-2 |
| US-041 | As an AP Accountant, I want to create payment requests with approval workflow so that payments are authorized | SRS-AP-005 | P0 | 5 | BE-3 |
| US-042 | As a Cashier, I want to execute payments via bank transfer or cash so that suppliers are paid | SRS-AP-006 | P0 | 5 | BE-1 |
| US-043 | As an AP Accountant, I want to generate AP aging reports so that I can monitor payment obligations | — | P0 | 3 | BE-2 |
| US-044 | As a UI/UX Designer, I want the AP invoice processing screen with OCR preview so that invoice review is efficient | — | P0 | 5 | FE-1 |

**Sprint 6 Total: 44 points**

### SPRINT 7 — E-Invoice Core (Weeks 13-14)

**Theme:** Invoice creation, CQT code request, digital signature

| Story ID | User Story | SRS Ref | Priority | Est. Points | Assignee |
|----------|-----------|---------|----------|-------------|----------|
| US-045 | As an AR Accountant, I want to create e-invoices per Decree 70/2025 with mandatory fields so that invoices are legally compliant | SRS-EINV-001 | P0 | 8 | BE-1 |
| US-046 | As the system, I want to request invoice codes from Tax Authority API for invoices requiring CQT codes so that invoices are registered | SRS-EINV-002 | P0 | 8 | BE-2 |
| US-047 | As the system, I want to support all invoice types (standard, discount, return, internal, POS) so that all business scenarios are covered | SRS-EINV-003 | P0 | 8 | BE-3 |
| US-048 | As the system, I want to apply digital signatures to e-invoices using VNPT/Viettel/BKAV providers so that invoices are legally valid | SRS-DS-001, SRS-DS-002 | P0 | 8 | BE-1 + DevOps |
| US-049 | As an AR Accountant, I want to send e-invoices to customers via email/portal so that delivery is tracked | — | P0 | 5 | FE-2 |
| US-050 | As a UI/UX Designer, I want the multi-step e-invoice creation screen (customer, lines, review, sign, send) so that the workflow is intuitive | — | P0 | 8 | FE-1 + FE-2 |

**Sprint 7 Total: 45 points**

### SPRINT 8 — E-Invoice Advanced (Weeks 15-16)

**Theme:** Replacement, adjustment, VAT timing rules

| Story ID | User Story | SRS Ref | Priority | Est. Points | Assignee |
|----------|-----------|---------|----------|-------------|----------|
| US-051 | As an AR Accountant, I want to replace invoices (wrong amount/tax rate/quantity) with Bien Ban Thay The so that errors are corrected per Decree 70/2025 | SRS-EINV-004 | P0 | 8 | BE-2 |
| US-052 | As an AR Accountant, I want to adjust invoices (wrong buyer info) with Bien Ban Dieu Chinh so that minor errors are corrected | SRS-EINV-004 | P0 | 5 | BE-3 |
| US-053 | As the system, I want to generate Form 04/SS-HDDT for correction notifications so that tax authority is informed | SRS-EINV-005 | P0 | 5 | BE-1 |
| US-054 | As the system, I want to adjust GL entries when invoices are replaced or adjusted so that financial records are accurate | SRS-EINV-006 | P0 | 8 | BE-2 |
| US-055 | As the system, I want to determine VAT timing based on goods delivery, service completion, or payment collection so that VAT liability is correctly timed | SRS-EINV-007, SRS-EINV-008 | P0 | 8 | BE-3 + Tax SME |
| US-056 | As the system, I want to separate VAT liability date from invoice date so that VAT timing rules are enforced | SRS-EINV-008 | P0 | 5 | BE-1 |

**Sprint 8 Total: 39 points**

### SPRINT 9 — Tax Engine (Weeks 17-18)

**Theme:** VAT, CIT, PIT calculations, tax calendar, declaration forms

| Story ID | User Story | SRS Ref | Priority | Est. Points | Assignee |
|----------|-----------|---------|----------|-------------|----------|
| US-057 | As a Tax Accountant, I want to calculate VAT with rates 10%, 8%, 5%, 0%, Non-Taxable so that VAT is correct | SRS-TAX-001, SRS-TAX-002 | P0 | 8 | BE-1 + Tax SME |
| US-058 | As a Tax Accountant, I want to generate VAT declaration Form 01/GTGT (monthly/quarterly) so that I can file VAT | SRS-TAX-003 | P0 | 8 | BE-2 + Tax SME |
| US-059 | As the system, I want to calculate VAT payable/refundable and generate the correct GL entry so that VAT accounting is accurate | SRS-TAX-004 | P0 | 5 | BE-3 |
| US-060 | As a Tax Accountant, I want to calculate quarterly provisional CIT with Form 01A/TNDN so that CIT is filed on time | SRS-TAX-005 | P0 | 8 | BE-1 + Tax SME |
| US-061 | As a Tax Accountant, I want to calculate annual CIT finalization (Form 03/TNDN) with deductible/non-deductible classification so that CIT is accurate | SRS-TAX-006 | P0 | 8 | BE-2 + Tax SME |
| US-062 | As a Tax Accountant, I want to calculate PIT withholding with personal deduction (11M) and dependent deduction (4.4M) so that PIT is correct | SRS-TAX-008 | P0 | 8 | BE-3 + Tax SME |
| US-063 | As a Tax Accountant, I want to generate PIT declaration forms (02/KK-TNCN, 05/QTT-TNCN) so that I can file PIT | SRS-TAX-009 | P0 | 5 | BE-1 |
| US-064 | As the system, I want to maintain a tax calendar with deadline alerts (7 days and 1 day before) so that filings are on time | SRS-TAX-012, SRS-TAX-013 | P0 | 5 | BE-2 |
| US-065 | As a Tax Accountant, I want to calculate License Fee and Foreign Contractor Tax so that all tax types are covered | SRS-TAX-010, SRS-TAX-011 | P0 | 5 | BE-3 |

**Sprint 9 Total: 60 points**

### SPRINT 10 — Financial Reporting (Weeks 19-20)

**Theme:** B01-DN, B02-DN, B03-DN, B09-DN, accounting books

| Story ID | User Story | SRS Ref | Priority | Est. Points | Assignee |
|----------|-----------|---------|----------|-------------|----------|
| US-066 | As a Chief Accountant, I want to generate B01-DN (Statement of Financial Position) with correct Circular 99 account mapping so that the balance sheet is compliant | SRS-RPT-001, SRS-RPT-002 | P0 | 13 | BE-1 + Acct SME |
| US-067 | As a Chief Accountant, I want to generate B02-DN (Statement of Business Results) with correct account mapping so that the P&L is compliant | SRS-RPT-001, SRS-RPT-002 | P0 | 13 | BE-2 + Acct SME |
| US-068 | As a Chief Accountant, I want to generate B03-DN (Cash Flow Statement) so that cash flows are reported | SRS-RPT-001 | P0 | 8 | BE-3 |
| US-069 | As a Chief Accountant, I want to generate B09-DN (Notes to Financial Statements) so that disclosures are complete | SRS-RPT-001 | P0 | 8 | BE-1 |
| US-070 | As the system, I want to enforce presentation principles (going concern, consistency, accrual, materiality, no offsetting, comparative info) so that BCTC is compliant | SRS-RPT-003 | P0 | 5 | BE-2 |
| US-071 | As a Chief Accountant, I want to print all accounting books in official Circular 99 formats (General Journal, General Ledger, Subsidiary Ledgers, FA Register, Inventory Cards) so that books are audit-ready | SRS-BOOK-001, SRS-BOOK-002 | P0 | 8 | FE-1 + FE-2 |
| US-072 | As a Chief Accountant, I want to support financial statement amendment with version tracking so that corrections are traceable | SRS-RPT-005 | P0 | 5 | BE-3 |

**Sprint 10 Total: 60 points**

### SPRINT 11 — Bank/Cash + Data Migration (Weeks 21-22)

**Theme:** Bank reconciliation, cash management, Circular 200 migration

| Story ID | User Story | SRS Ref | Priority | Est. Points | Assignee |
|----------|-----------|---------|----------|-------------|----------|
| US-073 | As a Cashier, I want to manage cash accounts (TK 111, 112, 113, 1281) with receipt/payment vouchers so that cash is tracked | SRS-CASH-001, SRS-CASH-002 | P0 | 5 | BE-1 |
| US-074 | As a Cashier, I want to import bank statements (MT940, CSV, Excel) and auto-match transactions so that reconciliation is efficient | SRS-CASH-003 | P0 | 8 | BE-2 |
| US-075 | As a Cashier, I want to manually match unmatched bank transactions so that all items are reconciled | SRS-CASH-003 | P0 | 5 | BE-3 |
| US-076 | As the system, I want to target >=85% auto-match rate for bank reconciliation so that manual effort is minimized | SRS-CASH-004 | P0 | 5 | BE-2 |
| US-077 | As a Chief Accountant, I want to transfer balances from Circular 200 to Circular 99 per Article 19 so that migration is accurate | SRS-MIG-001 | P0 | 8 | BE-1 + Acct SME |
| US-078 | As a Chief Accountant, I want to transfer balances from Circular 133 to Circular 99 so that SME migration is supported | SRS-MIG-002 | P0 | 5 | BE-3 |
| US-079 | As the system, I want to generate a migration verification report comparing pre/post balances so that migration is validated | SRS-MIG-003 | P0 | 5 | BE-2 |
| US-080 | As a Chief Accountant, I want to run parallel comparison (old system vs new system) before cutover so that migration is verified | SRS-MIG-004 | P0 | 5 | BA-1 + BA-2 |

**Sprint 11 Total: 46 points**

### SPRINT 12 — Compliance Audit + Hardening (Weeks 23-24)

**Theme:** Compliance review, performance testing, UAT, bug fixes

| Story ID | User Story | SRS Ref | Priority | Est. Points | Assignee |
|----------|-----------|---------|----------|-------------|----------|
| US-081 | As a Compliance Auditor, I want to verify all Circular 99 requirements are met so that the system is compliant | SRS-RC-001 to 012 | P0 | 13 | Acct SME + Tax SME + QA |
| US-082 | As a Tax Accountant, I want to submit test tax declarations to GDT portal so that e-filing is validated | SRS-API-001 to 003 | P0 | 8 | BE + Tax SME |
| US-083 | As a QA Engineer, I want to run load tests (50K entries/hr, 100 concurrent users, <3s page load) so that performance targets are verified | SRS-PERF-001 to 004 | P0 | 8 | QA-1 + QA-2 |
| US-084 | As a Security Engineer, I want to run penetration testing so that vulnerabilities are identified | SRS-SEC-001 to 005 | P0 | 8 | DevOps + TL |
| US-085 | As a CFO, I want to perform UAT on all Phase 1 features so that the system meets business needs | All P0 SRS | P0 | 13 | PM + BA + CFO |
| US-086 | As a Developer, I want to fix all critical and high-priority bugs so that the MVP is stable | — | P0 | 13 | All BE + FE |
| US-087 | As a Technical Writer, I want complete user guides, API docs, and admin guides so that users can operate the system | — | P0 | 5 | BA-1 |

**Sprint 12 Total: 68 points**

---

## 2. USER STORY BREAKDOWN WITH ACCEPTANCE CRITERIA

### 2.1 Detailed Acceptance Criteria (Selected Critical Stories)

#### US-009: Circular 99 COA Pre-load

**Given** the system is initialized for a new enterprise
**When** the COA seeding process runs
**Then**:
- 71 Level-1 accounts (3-digit) are created with correct codes, names (VN + EN), and group assignments per Phu Luc II, TT 99/2025
- 101 Level-2 accounts (4-digit) are created with correct parent-child relationships
- 10 Level-3 accounts (5-digit) are created
- 2 Level-4 accounts (6-digit) are created
- All 8 account groups (Assets, Liabilities, Equity, Revenue, Costs, Other Income, Other Expenses, Business Results) are correctly assigned
- **SRS-ADM-007, SRS-ADM-008** verified

#### US-017: Debit/Credit Balance Enforcement

**Given** a journal entry is being submitted
**When** the system validates the entry
**Then**:
- If total_debit != total_credit, the entry is rejected with error "Entry unbalanced: Debit {X} != Credit {Y}"
- If total_debit == total_credit, validation passes
- The constraint is enforced at both application and database levels (CHECK constraint)
- **SRS-GL-001, VR-GL-01** verified

#### US-025: Maker-Checker Approval Workflow

**Given** a journal entry exceeds the configurable approval threshold
**When** the entry is submitted
**Then**:
- Entry status is set to "pending" (not "posted")
- Entry is routed to users with approver role
- The entry creator cannot approve their own entry
- Upon approval, status changes to "posted" with approver ID and timestamp recorded
- Upon rejection, status returns to "draft" with rejection comments
- **SRS-GL-005, BR-015** verified

#### US-057: VAT Calculation

**Given** a reporting period
**When** the VAT calculation is triggered
**Then**:
- Input VAT is summed from TK 1331 (goods/services) and TK 1332 (fixed assets)
- Output VAT is summed from TK 33311 (output) and TK 33312 (import)
- Non-deductible input VAT is identified and excluded
- VAT payable = Output VAT - Deductible Input VAT (if positive)
- VAT refundable = Deductible Input VAT - Output VAT (if positive)
- Result matches HTKK software output within +/-1,000 VND tolerance
- **SRS-TAX-001, SRS-TAX-002, SRS-TAX-004** verified

#### US-066: B01-DN Generation

**Given** a closed accounting period
**When** the B01-DN report is generated
**Then**:
- All line items match the official Circular 99 template (B01-DN, Phu luc III)
- Account balances are correctly mapped to line items per DATA_FLOW section 14.2
- Current year and previous year comparative columns are populated
- Total Assets = Total Liabilities + Equity (balance check)
- Report is printable in official format
- Generation completes within 30 seconds
- **SRS-RPT-001, SRS-RPT-002, SRS-RPT-003** verified

#### US-077: Circular 200 to 99 Migration

**Given** a Circular 200 balance export file
**When** the migration process runs
**Then**:
- TK 111, 112, 113 detail balances transfer directly
- TK 138 (BCC contribution) maps to TK 2281
- TK 2413 (upgrade portion) maps to TK 2414
- TK 338 (dividends) maps to TK 332
- TK 441 + TK 466 map to TK 4118
- TK 421 transfers directly
- TK 347 transfers directly
- Migration verification report shows zero balance differences
- **SRS-MIG-001, SRS-MIG-003** verified

---

## 3. DEFINITION OF READY (DoR)

A user story is **Ready** for sprint planning when ALL criteria are met:

| # | Criterion | Verified By |
|---|-----------|-------------|
| 1 | User story follows format: "As a [role], I want [feature] so that [benefit]" | BA |
| 2 | Acceptance criteria are defined and testable (Given/When/Then) | BA + QA |
| 3 | SRS requirement reference is linked (e.g., SRS-GL-001) | BA |
| 4 | Story is estimated (story points) by the team | Team |
| 5 | Dependencies are identified and resolved or scheduled | TL |
| 6 | UI/UX wireframes or mockups are available (for frontend stories) | UX |
| 7 | Compliance requirements are documented (for tax/accounting stories) | Acct SME / Tax SME |
| 8 | Story fits within sprint capacity (no story > 13 points without splitting) | PM |
| 9 | Technical approach is understood by assigned developer | TL + Developer |
| 10 | Test data requirements are identified | QA |

**DoR Checklist** must be completed during backlog refinement (held 2 days before sprint planning).

---

## 4. DEFINITION OF DONE (DoD)

A user story is **Done** when ALL criteria are met:

| # | Criterion | Verified By |
|---|-----------|-------------|
| 1 | Code is written and follows project conventions (black, isort, flake8) | Developer |
| 2 | All acceptance criteria are met | QA |
| 3 | Unit tests written with >= 80% coverage for new code | Developer |
| 4 | Integration tests written for cross-module interactions | QA |
| 5 | Code is reviewed and approved by Tech Lead (merge request) | TL |
| 6 | CI/CD pipeline passes (lint, test, build) | DevOps |
| 7 | No new critical or high-severity bugs introduced | QA |
| 8 | Database migrations written and tested (if schema changes) | Developer |
| 9 | API documentation updated (if API changes) | Developer |
| 10 | Vietnamese labels verified for UI elements | BA |
| 11 | Compliance requirements verified by SME (for tax/accounting stories) | Acct SME / Tax SME |
| 12 | User documentation updated (if user-facing changes) | BA |
| 13 | Story is demonstrated in sprint review | Team |
| 14 | No open TODO/FIXME comments in production code | TL |

**DoD Checklist** must be completed before a story is moved to "Done" in the sprint board.

---

## 5. QA STRATEGY

### 5.1 Test Pyramid

```
                    /\
                   /  \
                  / E2E \         ~10% of tests
                 /--------\
                /          \
               / Integration \    ~25% of tests
              /----------------\
             /                  \
            /     Unit Tests      \  ~65% of tests
           /------------------------\
```

### 5.2 Unit Test Coverage Targets

| Module | Target Coverage | Minimum Coverage | Test Count (Est.) |
|--------|----------------|-----------------|-------------------|
| Models | >= 90% | 80% | 150+ |
| Services | >= 85% | 75% | 200+ |
| Views | >= 75% | 65% | 100+ |
| **Overall** | **>= 80%** | **70%** | **450+** |

### 5.3 Test Execution Commands

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run single test file
pytest tests/models/test_account.py --no-cov -v

# Run single test method
pytest tests/models/test_account.py::TestAccountModel::test_create_account --no-cov -v

# Run single test class
pytest tests/services/test_account_service.py::TestAccountService --no-cov -v

# Run with debugger on failure
pytest tests/ --tb=long --no-cov -x
```

### 5.4 Integration Test Approach

| Test Type | Scope | Frequency | Tool |
|-----------|-------|-----------|------|
| API Integration | All REST endpoints | Every sprint | pytest + Flask test client |
| Cross-Module | AR to GL, AP to GL, Tax to GL, Payroll to GL | Every sprint | pytest with full app context |
| Database | Migrations, constraints, indexes | Every sprint | pytest with in-memory SQLite |
| External API | Tax authority, e-invoice, bank (mocked) | Every sprint | pytest + responses/vcr |
| End-to-End | Full business workflows (O2C, P2P, R2R) | Every 2 sprints | Playwright |

### 5.5 Integration Test Scenarios (Phase 1)

| Scenario ID | Workflow | Steps | Expected Result |
|-------------|----------|-------|-----------------|
| IT-001 | Order-to-Cash | Create customer, Create invoice, Post to GL, Record payment, Verify AR balance | AR balance = 0, GL entries correct |
| IT-002 | Procure-to-Pay | Create supplier, Create invoice, 3-way match, Post to GL, Execute payment, Verify AP balance | AP balance = 0, GL entries correct |
| IT-003 | VAT Declaration | Create sales invoices, Create purchase invoices, Calculate VAT, Generate Form 01/GTGT | VAT payable matches manual calculation |
| IT-004 | Month-End Close | Post all entries, Run depreciation, Run CCDC allocation, Generate trial balance, Close period | Trial balanced, period locked |
| IT-005 | BCTC Generation | Close all periods, Generate B01-DN, Generate B02-DN, Generate B03-DN, Generate B09-DN | All statements balanced and compliant |
| IT-006 | E-Invoice Lifecycle | Create invoice, Request CQT code, Apply digital signature, Send to customer, Verify on GDT | Invoice confirmed by tax authority |
| IT-007 | Data Migration | Import Circular 200 balances, Run migration, Verify report, Compare with source | Zero balance differences |
| IT-008 | Bank Reconciliation | Import bank statement, Auto-match, Manual match, Reconcile, Verify difference = 0 | All transactions reconciled |

### 5.6 UAT Plan

| Phase | Duration | Participants | Scope |
|-------|----------|-------------|-------|
| **UAT-1: Alpha** | S4 end (Week 8) | Chief Accountant, Tech Lead | GL, COA, Auth |
| **UAT-2: Beta 1** | S8 end (Week 16) | Chief Accountant, AR/AP Accountants | GL, AR, AP, E-Invoice |
| **UAT-3: Beta 2** | S10 end (Week 20) | Chief Accountant, Tax Accountant, CFO | Full Phase 1 + Tax + Reporting |
| **UAT-4: Pre-Launch** | S12 (Weeks 23-24) | All user classes, External Auditor | Complete Phase 1, compliance validation |

**UAT Sign-Off Requirements:**
- All critical test cases passed (100%)
- All high-priority test cases passed (>= 95%)
- Zero open critical/high bugs
- CFO and Chief Accountant formal sign-off

### 5.7 Compliance Testing

| Compliance Area | Test Method | Validator | Frequency |
|----------------|-------------|-----------|-----------|
| Circular 99 COA accuracy | Compare against Phu Luc II | Certified Accountant | S2, then monthly |
| Financial statement templates | Compare against official Circular 99 forms | External Auditor | S10, S12 |
| Tax calculation accuracy | Compare against HTKK software (+/-1,000 VND) | Tax Expert | S9, then monthly |
| E-invoice compliance | Submit to GDT test portal | Tax Expert + BA | S7, S8, S12 |
| Voucher format compliance | Visual inspection against Circular 99 templates | Certified Accountant | S5, S6, S10 |
| Insurance rate accuracy | Compare against 2026 statutory rates | Payroll SME | S13 (Phase 2) |

---

## 6. CI/CD PIPELINE SPECIFICATION

### 6.1 Pipeline Stages

```
Commit -> Lint -> Unit Test -> Integration Test -> Build -> Deploy (staging) -> Smoke Test -> Deploy (production)
```

### 6.2 GitHub Actions Workflow

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: make install
      - name: Run linting
        run: make lint

  test:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: make install
      - name: Run unit tests
        run: pytest tests/models/ tests/services/ --no-cov -v
      - name: Run integration tests
        run: pytest tests/views/ --no-cov -v
      - name: Run coverage
        run: make test-cov
      - name: Upload coverage
        uses: codecov/codecov-action@v4

  build:
    runs-on: ubuntu-latest
    needs: test
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - name: Build Docker image
        run: docker build -t gl-app:${{ github.sha }} .
      - name: Push to registry
        run: docker push gl-app:${{ github.sha }}

  deploy-staging:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/develop'
    steps:
      - name: Deploy to staging
        run: ./scripts/deploy.sh staging
      - name: Run smoke tests
        run: ./scripts/smoke-test.sh staging

  deploy-production:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    environment: production
    steps:
      - name: Deploy to production
        run: ./scripts/deploy.sh production
      - name: Run smoke tests
        run: ./scripts/smoke-test.sh production
      - name: Health check
        run: ./scripts/health-check.sh
```

### 6.3 Pipeline Gates

| Gate | Condition | Action on Failure |
|------|-----------|-------------------|
| Lint | flake8 + black + isort pass | Block merge |
| Unit Tests | 100% pass | Block merge |
| Integration Tests | 100% pass | Block merge |
| Coverage | >= 70% overall | Warning (block at 60%) |
| Build | Docker image builds | Block deploy |
| Smoke Tests | All endpoints respond 200 | Auto-rollback |
| Health Check | System healthy for 5 min | Auto-rollback |

### 6.4 Branch Strategy

| Branch | Purpose | Protection |
|--------|---------|-----------|
| `main` | Production-ready code | Require 2 approvals, CI pass, no force push |
| `develop` | Integration branch | Require 1 approval, CI pass |
| `feature/*` | Feature development | — |
| `hotfix/*` | Production bug fixes | Require 1 approval, CI pass |
| `release/*` | Release preparation | Require 2 approvals, CI pass |

---

## 7. COMMUNICATION PLAN

### 7.1 Meeting Cadence

| Meeting | Frequency | Duration | Participants | Purpose |
|---------|-----------|----------|-------------|---------|
| **Daily Standup** | Daily (Mon-Fri) | 15 min | Full team | Progress, blockers, daily plan |
| **Sprint Planning** | Every 2 weeks | 2 hours | Full team | Select stories, estimate, commit |
| **Backlog Refinement** | Weekly (Wednesday) | 1 hour | PM, BA, TL, QA | Review upcoming stories, DoR check |
| **Sprint Review/Demo** | Every 2 weeks | 1 hour | Full team + CFO + Chief Accountant | Demonstrate completed work |
| **Sprint Retrospective** | Every 2 weeks | 1 hour | Full team | Improve process |
| **Weekly Steering** | Weekly (Friday) | 30 min | PM, CFO, TL, IT Director | Status, risks, decisions |
| **Monthly Steering Committee** | Monthly | 2 hours | PM, CFO, CEO, IT Director, External stakeholders | Strategic review, budget, timeline |
| **Compliance Review** | Monthly | 1 hour | PM, Acct SME, Tax SME, TL | Verify compliance progress |

### 7.2 Daily Standup Format

Each team member answers:
1. What did I complete yesterday?
2. What will I work on today?
3. Are there any blockers?

PM tracks sprint burndown, blocker resolution, and resource adjustments.

### 7.3 Reporting

| Report | Frequency | Audience | Content |
|--------|-----------|----------|---------|
| Sprint Burndown | Daily | Team | Remaining work vs. ideal |
| Sprint Status | Weekly | CFO, IT Director | Completed stories, velocity, risks |
| Release Status | Bi-weekly | Steering Committee | Milestone progress, Go/No-Go status |
| Compliance Status | Monthly | CFO, External Auditor | Compliance checklist, audit findings |
| Budget Report | Monthly | CFO, CEO | Actual vs. planned spend |
| Risk Register | Monthly | Steering Committee | Updated risks, mitigation status |

### 7.4 Communication Channels

| Channel | Purpose | Tools |
|---------|---------|-------|
| Real-time chat | Daily communication, quick questions | Slack/Teams |
| Sprint board | Task tracking, status | Jira/Linear |
| Document repository | Specifications, decisions | Google Docs/Confluence |
| Code repository | Source code, reviews | GitHub |
| CI/CD notifications | Build/test status | Slack integration |
| Email | Formal communications, sign-offs | Corporate email |
| Video conferencing | Meetings, demos | Zoom/Teams |

---

## 8. ESCALATION MATRIX

### 8.1 Escalation Levels

| Level | Trigger | Response Time | Escalated To | Action |
|-------|---------|--------------|-------------|--------|
| **L1** | Developer blocked > 4 hours | 1 hour | Tech Lead | TL provides guidance or pairs with developer |
| **L2** | Blocker unresolved > 8 hours | 2 hours | PM + TL | PM reassigns resources, TL escalates to architecture decision |
| **L3** | Sprint goal at risk, compliance issue | 4 hours | PM + CFO | Scope adjustment, resource reallocation, stakeholder notification |
| **L4** | Go/No-Go at risk, regulatory deadline | 24 hours | Steering Committee | Emergency meeting, decision on timeline/scope/budget |

### 8.2 Escalation Contacts

| Role | Name | Contact | Availability |
|------|------|---------|-------------|
| Project Manager | [TBD] | [TBD] | Business hours + on-call |
| Tech Lead | [TBD] | [TBD] | Business hours + on-call |
| CFO / Sponsor | [TBD] | [TBD] | Business hours |
| Certified Accountant (SME) | [TBD] | [TBD] | Business hours |
| Tax Expert (SME) | [TBD] | [TBD] | Business hours |
| External Auditor | [TBD] | [TBD] | By appointment |

### 8.3 Escalation Decision Log

All escalations L3 and above must be documented:

| Field | Description |
|-------|-------------|
| Escalation ID | ESC-YYYY-NNN |
| Date/Time | When escalation was raised |
| Level | L1-L4 |
| Description | What is the issue |
| Impact | Which sprint/milestone is affected |
| Decision | What action was taken |
| Owner | Who is responsible for resolution |
| Resolution Date | When issue was resolved |

---

## 9. CHANGE MANAGEMENT PROCESS

### 9.1 Change Request Flow

```
[Change Identified]
        |
        v
[Submit Change Request (CR)]
        |
        v
[PM logs CR in Change Register]
        |
        v
[Impact Analysis (TL + BA + QA)]
  - Technical impact
  - Schedule impact
  - Cost impact
  - Compliance impact
        |
        v
<Change Size?>
        |
        +-- Small (< 3 SP) --> [TL approves] --> [Add to sprint backlog]
        |
        +-- Medium (3-8 SP) --> [PM + TL approve] --> [Add to next sprint]
        |
        +-- Large (> 8 SP) --> [Steering Committee approves] --> [Replan if needed]
        |
        v
[Update backlog, schedule, budget]
        |
        v
[Communicate change to team]
        |
        v
[Implement change]
        |
        v
[Verify in sprint review]
```

### 9.2 Change Request Template

| Field | Description |
|-------|-------------|
| CR-ID | CR-YYYY-NNN |
| Title | Brief description |
| Requestor | Who requested |
| Date | When requested |
| Priority | P0/P1/P2/P3 |
| Description | Detailed description of the change |
| SRS Reference | Which SRS requirement is affected |
| Justification | Why is this change needed |
| Impact Analysis | Technical, schedule, cost, compliance impact |
| Approval | Who approved (TL/PM/Steering Committee) |
| Status | Draft/Under Review/Approved/Rejected/Implemented |

### 9.3 Change Control Rules

| Rule | Description |
|------|-------------|
| No mid-sprint scope changes | Changes are added to next sprint unless P0 emergency |
| P0 emergency changes | Require PM + TL + CFO approval, documented in CR |
| Compliance-driven changes | Always approved, expedited through process |
| SRS changes | Must update traceability matrix |
| Budget impact > 10% | Requires Steering Committee approval |
| Timeline impact > 1 sprint | Requires Steering Committee approval |

### 9.4 Configuration Management

| Item | Tool | Version Control |
|------|------|----------------|
| Source code | GitHub | Git branching strategy |
| Database schema | Alembic/Flask-Migrate | Migration files in repo |
| Infrastructure | Docker + docker-compose | Dockerfiles in repo |
| Documentation | Markdown in docs/ | Git versioned |
| Requirements | SRS/BRD/URD documents | Git versioned with version numbers |
| Test cases | pytest test files | Git versioned |

---

## 10. TECHNICAL DEBT TRACKING APPROACH

### 10.1 Technical Debt Categories

| Category | Description | Example |
|----------|-------------|---------|
| **Code Debt** | Quick fixes, missing refactoring | Duplicated validation logic |
| **Test Debt** | Missing tests, low coverage | Service without unit tests |
| **Design Debt** | Suboptimal architecture decisions | Tight coupling between modules |
| **Documentation Debt** | Outdated or missing docs | API not documented |
| **Infrastructure Debt** | Temporary infrastructure setup | SQLite for dev instead of PostgreSQL |
| **Compliance Debt** | Temporary compliance workarounds | Hardcoded tax rate instead of configurable |

### 10.2 Technical Debt Register

| TD-ID | Category | Description | Sprint Created | Estimated Effort | Priority | Status | Target Sprint |
|-------|----------|-------------|---------------|-----------------|----------|--------|---------------|
| TD-001 | Infrastructure | SQLite dev DB instead of PostgreSQL | S1 | 3 SP | P1 | Open | S2 |
| TD-002 | Code | Temporary auth implementation | S1 | 5 SP | P1 | Open | S3 |
| TD-003 | Test | Missing integration tests for GL | S3 | 5 SP | P2 | Open | S5 |
| TD-004 | Code | Hardcoded COA data instead of seed script | S2 | 3 SP | P1 | Open | S4 |
| TD-005 | Documentation | API docs not updated | S4 | 2 SP | P2 | Open | S6 |

### 10.3 Technical Debt Management Rules

| Rule | Description |
|------|-------------|
| **10% Sprint Capacity** | Each sprint reserves 10% capacity for technical debt repayment |
| **Debt Interest Tracking** | Each TD item tracks "interest" (how much it slows development) |
| **No New Debt Without Approval** | New technical debt requires TL approval with TD register entry |
| **P0 Debt Must Be Resolved Before MVP** | All P0 technical debt must be cleared by S12 |
| **Quarterly Debt Review** | PM + TL review TD register every quarter and reprioritize |
| **Debt Linked to Stories** | TD items are linked to user stories that created them |

### 10.4 Technical Debt Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Total open TD items | < 10 at any time | TD register count |
| P0 TD items | 0 by S12 | TD register filter |
| TD repayment rate | >= 2 items per sprint | Sprint velocity on TD |
| Test coverage debt | 0 (coverage >= target) | Coverage report |
| Code quality debt | 0 flake8/black violations | Lint report |

### 10.5 Technical Debt in Sprint Planning

During each sprint planning:
1. Review TD register for items that can be addressed
2. Allocate 10% of sprint capacity (approx. 5 SP) to TD repayment
3. Prioritize TD items that block current sprint work
4. Link TD repayment to relevant user stories where possible
5. Update TD register with status changes

---

## APPENDIX A: SPRINT VELOCITY PLANNING

### A.1 Velocity Projections

| Sprint | Planned Points | Expected Velocity | Confidence |
|--------|---------------|-------------------|------------|
| S1 | 47 | 40-45 | Medium (team forming) |
| S2 | 47 | 45-50 | Medium |
| S3 | 47 | 50-55 | High |
| S4 | 42 | 50-55 | High |
| S5 | 47 | 50-55 | High |
| S6 | 44 | 50-55 | High |
| S7 | 45 | 50-55 | High |
| S8 | 39 | 50-55 | High |
| S9 | 60 | 50-55 | Medium (complex tax logic) |
| S10 | 60 | 50-55 | Medium (complex reporting) |
| S11 | 46 | 50-55 | High |
| S12 | 68 | 50-55 | Medium (audit + hardening) |

**Total Phase 1: 605 story points across 12 sprints**

### A.2 Risk Buffer

| Sprint | Buffer Allocation | Purpose |
|--------|------------------|---------|
| S1-S4 | 10% | Team ramp-up, unknown technical challenges |
| S5-S8 | 10% | Integration complexity, external API dependencies |
| S9-S10 | 15% | Tax calculation complexity, reporting accuracy |
| S11-S12 | 15% | Migration validation, compliance audit findings |

---

## APPENDIX B: REQUIREMENTS TRACEABILITY MATRIX (Phase 1)

| SRS Requirement | Sprint | Story IDs | Test Prefix | Status |
|----------------|--------|-----------|-------------|--------|
| SRS-ADM-001 to 006 | S1 | US-001 to US-005 | TC-ADM-xxx | Planned |
| SRS-ADM-007 to 010 | S2 | US-009 to US-011 | TC-ADM-xxx | Planned |
| SRS-ADM-011 to 014 | S2 | US-012 | TC-ADM-xxx | Planned |
| SRS-ADM-015 to 017 | S2 | US-013 | TC-ADM-xxx | Planned |
| SRS-ADM-018 to 021 | S2 | US-014 | TC-ADM-xxx | Planned |
| SRS-GL-001 to 006 | S3-S4 | US-016 to US-021, US-023 to US-026 | TC-GL-xxx | Planned |
| SRS-GL-007 to 008 | S4 | US-027 | TC-GL-xxx | Planned |
| SRS-GL-009 to 010 | S10 | US-066 to US-072 | TC-GL-xxx | Planned |
| SRS-AR-001 to 009 | S5 | US-030 to US-036 | TC-AR-xxx | Planned |
| SRS-AP-001 to 006 | S6 | US-037 to US-044 | TC-AP-xxx | Planned |
| SRS-EINV-001 to 008 | S7-S8 | US-045 to US-056 | TC-EINV-xxx | Planned |
| SRS-TAX-001 to 013 | S9 | US-057 to US-065 | TC-TAX-xxx | Planned |
| SRS-RPT-001 to 006 | S10 | US-066 to US-072 | TC-RPT-xxx | Planned |
| SRS-BOOK-001 to 002 | S10 | US-071 | TC-BOOK-xxx | Planned |
| SRS-CASH-001 to 005 | S11 | US-073 to US-076 | TC-CASH-xxx | Planned |
| SRS-MIG-001 to 004 | S11 | US-077 to US-080 | TC-MIG-xxx | Planned |
| SRS-DS-001 to 002 | S7 | US-048 | TC-DS-xxx | Planned |
| SRS-AP-001 to 003 | S2 | US-011 | TC-AP-xxx | Planned |
| SRS-FX-001 to 003 | S4 | US-024 | TC-FX-xxx | Planned |
| SRS-RC-001 to 012 | S12 | US-081 | TC-RC-xxx | Planned |
| SRS-PERF-001 to 004 | S12 | US-083 | TC-PERF-xxx | Planned |
| SRS-SEC-001 to 005 | S12 | US-084 | TC-SEC-xxx | Planned |
| SRS-API-001 to 011 | S7, S9, S12 | US-046, US-082 | TC-API-xxx | Planned |

---

**END OF EXECUTION PLAN**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | April 2026 | Project Management Office | Initial release |
