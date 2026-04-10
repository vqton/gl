# PROJECT ROADMAP — Vietnamese Enterprise Accounting Software

**Circular 99/2025/TT-BTC Compliant Platform**

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Date** | April 2026 |
| **Prepared by** | Project Management Office |
| **Classification** | Confidential |
| **Team Size** | 15 FTE |
| **Cadence** | 2-week sprints |
| **Total Duration** | 18 months (3 phases) |

---

## TABLE OF CONTENTS

1. Strategic Overview
2. Phase 1 — Foundation (Months 1-6): Sprints 1-12
3. Phase 2 — Enhancement (Months 7-12): Sprints 13-24
4. Phase 3 — Advanced (Months 13-18): Sprints 25-36
5. Epic Breakdown & Dependencies
6. Milestone Timeline & Critical Path
7. Resource Allocation Per Sprint
8. Risk-Based Prioritization
9. Go/No-Go Criteria Per Milestone
10. Release Strategy

---

## 1. STRATEGIC OVERVIEW

### 1.1 Vision Alignment

This roadmap delivers a cloud-based Vietnamese enterprise accounting platform achieving:
- **BO-01:** 100% Circular 99/2025 compliance by Q3 2026 (end of Phase 1)
- **BO-02:** Full tax law coverage (CIT, PIT, VAT, Tax Admin) by Q3 2026
- **BO-03:** Monthly closing reduced from 10 days to 3 days by Q4 2026
- **BO-04:** Tax filing errors reduced from 5% to <0.5% by Q4 2026
- **BO-05:** 85% automated bank reconciliation by Q4 2026

### 1.2 Compliance Deadlines (Hard Constraints)

| Deadline | Requirement | Legal Basis |
|----------|------------|-------------|
| **20th of each month** | VAT monthly filing, PIT monthly filing | Law 149/2025, Law 108/2025 |
| **Last day of 1st month of next quarter** | VAT quarterly, CIT quarterly, PIT quarterly | Law 67/2025, Law 149/2025 |
| **Within 90 days of fiscal year-end** | Annual BCTC (B01-B09) submission | Circular 99/2025 |
| **Within 30 days of quarter-end** | Quarterly BCTC submission | Circular 99/2025 |
| **01/07/2026** | New PIT Law effective (Law 109/2025) | Law 109/2025/QH15 |

### 1.3 Module Coverage (15 Modules per SRS)

| Module | SRS Section | Phase | Priority |
|--------|------------|-------|----------|
| MOD-01: System Administration | SRS §3.1 | Phase 1 | P0 |
| MOD-02: General Ledger | SRS §3.2 | Phase 1 | P0 |
| MOD-03: Accounts Receivable | SRS §3.3 | Phase 1 | P0 |
| MOD-04: Accounts Payable | SRS §3.4 | Phase 1 | P0 |
| MOD-05: Electronic Invoice | SRS §3.5 | Phase 1 | P0 |
| MOD-06: Tax Management | SRS §3.6 | Phase 1 | P0 |
| MOD-07: Financial Reporting | SRS §3.7 | Phase 1 | P0 |
| MOD-08: Accounting Books | SRS §3.8 | Phase 1 | P0 |
| MOD-09: Bank & Cash | SRS §3.9 | Phase 1 | P0 |
| MOD-10: Payroll | SRS §3.10 | Phase 2 | P0 |
| MOD-11: Fixed Assets | SRS §3.11 | Phase 2 | P1 |
| MOD-12: Inventory | SRS §3.12 | Phase 2 | P1 |
| MOD-13: Data Migration | SRS §3.13 | Phase 1 | P0 |
| MOD-14: Digital Signature | SRS §3.14 | Phase 1 | P0 |
| MOD-15: Accounting Policy | SRS §3.15 | Phase 1 | P0 |

### 1.4 Current Codebase State (Baseline)

| Component | Status | Notes |
|-----------|--------|-------|
| Models | Complete | User, Account, JournalEntry, Customer, Supplier, Bill, FixedAsset, InventoryItem exist |
| Services | Complete | AccountService, JournalEntryService, UserService, InvoiceService, CustomerService, BillService, SupplierService, FixedAssetService, InventoryService |
| Views | Complete | gl, ar, ap, tax, payroll, fa, inventory, reports, admin, auth, main all implemented |
| Tests | Complete | TDD methodology - comprehensive tests for GL (69), AR (41), AP (52), FA (16), Inventory (19) modules |
| Database | SQLite dev | Migrations folder exists, no migrations applied |
| CI/CD | Pre-commit hooks | GitHub Actions configured |

---

## 2. PHASE 1 — FOUNDATION (Months 1-6)

**Objective:** Deliver MVP fully compliant with Circular 99/2025, covering core accounting, tax, e-invoice, and financial reporting.

**Sprints:** 1-12 (24 weeks)

**Modules Delivered:** MOD-01, MOD-02, MOD-03, MOD-04, MOD-05, MOD-06, MOD-07, MOD-08, MOD-09, MOD-13, MOD-14, MOD-15

### 2.1 Phase 1 Sprint Summary

| Sprint | Dates | Theme | Key Deliverables | SRS Coverage |
|--------|-------|-------|-----------------|--------------|
| **S1** | W1-2 | Platform Foundation | Auth, RBAC, DB schema, CI/CD, base models | SRS-ADM-001 to 006 |
| **S2** | W3-4 | Chart of Accounts | Full Circular 99 COA, custom accounts, period mgmt | SRS-ADM-007 to 014 |
| **S3** | W5-6 | GL Engine Core | Journal entry CRUD, balance enforcement, posting | SRS-GL-001 to 006 |
| **S4** | W7-8 | GL Advanced | Multi-currency, approval workflow, trial balance | SRS-GL-004 to 008 |
| **S5** | W9-10 | AR Module | Customer mgmt, invoicing, payment matching, aging | SRS-AR-001 to 009 |
| **S6** | W11-12 | AP Module | Supplier mgmt, invoice processing, 3-way match, payment | SRS-AP-001 to 006 |
| **S7** | W13-14 | E-Invoice Core | Invoice creation, CQT code, digital signature | SRS-EINV-001 to 003, SRS-DS-001 to 002 |
| **S8** | W15-16 | E-Invoice Advanced | Replacement, adjustment, VAT timing rules | SRS-EINV-004 to 008 |
| **S9** | W17-18 | Tax Engine (VAT/CIT/PIT) | VAT calculation, CIT quarterly, PIT withholding, tax calendar | SRS-TAX-001 to 013 |
| **S10** | W19-20 | Financial Reporting | B01-DN, B02-DN, B03-DN, B09-DN, accounting books | SRS-RPT-001 to 006, SRS-BOOK-001 to 002 |
| **S11** | W21-22 | Bank/Cash + Migration | Bank reconciliation, cash mgmt, Circular 200 migration | SRS-CASH-001 to 005, SRS-MIG-001 to 004 |
| **S12** | W23-24 | Compliance Audit + Hardening | Compliance review, performance testing, UAT, bug fixes | All P0 SRS |

### 2.2 Phase 1 Milestones

| Milestone | Sprint | Target Date | Go/No-Go Criteria |
|-----------|--------|------------|-------------------|
| **M1: Design Sign-Off** | S2 end | Month 1, Week 4 | Architecture approved, COA loaded, DB schema finalized |
| **M2: Core GL Functional** | S4 end | Month 3, Week 2 | Double-entry works, multi-currency, trial balance generates |
| **M3: AR/AP Complete** | S6 end | Month 4, Week 2 | Full procure-to-pay and order-to-cash flows operational |
| **M4: E-Invoice + Tax** | S9 end | Month 5, Week 4 | E-invoices issued, VAT/CIT/PIT calculated, declarations generated |
| **M5: Reporting Complete** | S10 end | Month 6, Week 2 | All B01-B09 statements generate correctly with Circular 99 mapping |
| **M6: MVP Launch Ready** | S12 end | Month 6, Week 4 | Compliance audit passed, UAT signed off, performance targets met |

---

## 3. PHASE 2 — ENHANCEMENT (Months 7-12)

**Objective:** Complete the full accounting suite with Payroll, Fixed Assets, Inventory, and management reporting.

**Sprints:** 13-24 (24 weeks)

**Modules Delivered:** MOD-10 (complete), MOD-11 (complete), MOD-12 (complete), MOD-07 (management reports), MOD-09 (bank API integration)

### 3.1 Phase 2 Sprint Summary

| Sprint | Dates | Theme | Key Deliverables | SRS Coverage |
|--------|-------|-------|-----------------|--------------|
| **S13** | W25-26 | Payroll Core | Employee mgmt, salary calculation, insurance (2026 rates) | SRS-PAY-001 to 003 |
| **S14** | W27-28 | Payroll Advanced | PIT withholding, payslips, insurance declarations, GL posting | SRS-PAY-004 to 006, SRS-TAX-008 to 009 |
| **S15** | W29-30 | Fixed Assets Core | Asset registration, depreciation (3 methods), schedules | SRS-FA-001 to 004 |
| **S16** | W31-32 | Fixed Assets Advanced | Transfer, disposal, revaluation, lifecycle events | SRS-FA-005 to 006 |
| **S17** | W33-34 | Inventory Core | Stock mgmt, valuation (FIFO/weighted avg), provisions | SRS-INV-001 to 003 |
| **S18** | W35-36 | Inventory Advanced | Material allocation, CCDC allocation, inventory reports | SRS-INV-004, SRS-CCDC-001 |
| **S19** | W37-38 | Bank API Integration | Direct bank statement import, payment initiation | SRS-API-006 to 007, SRS-CASH-005 |
| **S20** | W39-40 | Management Reporting | Dashboard, KPIs, budget vs actual, tax reconciliation | SRS-RPT-006, SRS-UI-004 |
| **S21** | W41-42 | Advanced Features | FX revaluation, revenue recognition, lease accounting | SRS-FX-001 to 003, SRS-REV-001 to 003, SRS-LEASE-001 to 002 |
| **S22** | W43-44 | Integration Testing | End-to-end testing, HTKK export, e-BHXH generation | SRS-API-008 to 011 |
| **S23** | W45-46 | Performance & Security | Load testing, penetration testing, security hardening | SRS-PERF-001 to 004, SRS-SEC-001 to 005 |
| **S24** | W47-48 | Phase 2 Release | UAT, compliance audit, documentation, release | All P1 SRS |

### 3.2 Phase 2 Milestones

| Milestone | Sprint | Target Date | Go/No-Go Criteria |
|-----------|--------|------------|-------------------|
| **M7: Payroll Live** | S14 end | Month 8, Week 2 | 2026 insurance rates correct, PIT matches HTKK, payslips generated |
| **M8: FA + Inventory Live** | S18 end | Month 10, Week 2 | Depreciation accurate, inventory valuation matches FIFO/WA |
| **M9: Full Suite Complete** | S21 end | Month 12, Week 2 | All 15 modules operational, management reports functional |
| **M10: Phase 2 Release** | S24 end | Month 12, Week 4 | Performance targets met, security audit passed, UAT signed off |

---

## 4. PHASE 3 — ADVANCED (Months 13-18)

**Objective:** Enterprise-grade features: multi-entity consolidation, mobile app, BI/analytics, advanced integrations.

**Sprints:** 25-36 (24 weeks)

**Modules Delivered:** Multi-entity, Mobile App, BI Dashboard, Advanced Integrations (50+), HRM foundation

### 4.1 Phase 3 Sprint Summary

| Sprint | Dates | Theme | Key Deliverables |
|--------|-------|-------|-----------------|
| **S25** | W49-50 | Multi-Entity Foundation | Entity hierarchy, inter-company transactions, consolidation rules |
| **S26** | W51-52 | Consolidation Engine | Elimination entries, consolidated BCTC, currency translation |
| **S27** | W53-54 | Mobile App Foundation | React Native setup, auth, dashboard, approval workflows |
| **S28** | W55-56 | Mobile Core Features | Invoice viewing, payment approval, expense capture, receipt scanning |
| **S29** | W57-58 | BI/Analytics Foundation | Data warehouse schema, ETL pipelines, KPI definitions |
| **S30** | W59-60 | BI Dashboards | Revenue analytics, cash flow forecasting, working capital analysis |
| **S31** | W61-62 | Advanced Integrations | Additional bank APIs, e-invoice provider expansion, ERP connectors |
| **S32** | W63-64 | HRM Foundation | Employee self-service, leave management, performance tracking |
| **S33** | W65-66 | Advanced Compliance | Global minimum tax full support, transfer pricing documentation |
| **S34** | W67-68 | AI/ML Features | AI bank reconciliation, anomaly detection, predictive cash flow |
| **S35** | W69-70 | Platform Hardening | Disaster recovery, multi-region deployment, SOC 2 preparation |
| **S36** | W71-72 | Phase 3 Release | Full platform release, customer onboarding, go-to-market |

### 4.2 Phase 3 Milestones

| Milestone | Sprint | Target Date | Go/No-Go Criteria |
|-----------|--------|------------|-------------------|
| **M11: Multi-Entity Live** | S26 end | Month 14, Week 2 | Consolidated BCTC generates correctly, inter-company eliminations work |
| **M12: Mobile App Beta** | S28 end | Month 15, Week 2 | Core mobile features functional, user acceptance >4.0/5 |
| **M13: BI Platform Live** | S30 end | Month 16, Week 2 | Dashboards operational, forecasting accuracy >80% |
| **M14: Enterprise Platform** | S36 end | Month 18, Week 4 | All Phase 3 features live, SOC 2 audit ready, 50+ integrations |

---

## 5. EPIC BREAKDOWN & DEPENDENCIES

### 5.1 Epic Inventory

| Epic ID | Epic Name | SRS References | Phase | Sprints | Dependencies |
|---------|-----------|---------------|-------|---------|-------------|
| **EP-01** | Platform Foundation | SRS-ADM-001 to 021, SRS-SEC-001 to 005 | P1 | S1-S2 | None |
| **EP-02** | Chart of Accounts Engine | SRS-ADM-007 to 010, SRS-AP-001 to 003 | P1 | S2-S3 | EP-01 |
| **EP-03** | General Ledger Core | SRS-GL-001 to 010, SRS-CCDC-001 | P1 | S3-S4 | EP-02 |
| **EP-04** | Accounts Receivable | SRS-AR-001 to 009, SRS-REV-001 to 003 | P1 | S5-S6 | EP-03 |
| **EP-05** | Accounts Payable | SRS-AP-001 to 006 | P1 | S5-S6 | EP-03 |
| **EP-06** | Electronic Invoice | SRS-EINV-001 to 008, SRS-DS-001 to 002 | P1 | S7-S8 | EP-04, EP-05 |
| **EP-07** | Tax Management | SRS-TAX-001 to 013, SRS-FX-001 to 003 | P1 | S9-S10 | EP-03, EP-06 |
| **EP-08** | Financial Reporting | SRS-RPT-001 to 006, SRS-BOOK-001 to 002 | P1 | S10 | EP-03, EP-04, EP-05, EP-07 |
| **EP-09** | Bank & Cash | SRS-CASH-001 to 005, SRS-MIG-001 to 004 | P1 | S11 | EP-03, EP-04, EP-05 |
| **EP-10** | Compliance & UAT | All P0 SRS | P1 | S12 | EP-01 to EP-09 |
| **EP-11** | Payroll | SRS-PAY-001 to 006 | P2 | S13-S14 | EP-03, EP-07 |
| **EP-12** | Fixed Assets | SRS-FA-001 to 006, SRS-LEASE-001 to 002 | P2 | S15-S16 | EP-03 |
| **EP-13** | Inventory | SRS-INV-001 to 004 | P2 | S17-S18 | EP-03, EP-05 |
| **EP-14** | Bank API Integration | SRS-API-006 to 007 | P2 | S19 | EP-09 |
| **EP-15** | Management Reporting | SRS-RPT-006, SRS-UI-004 | P2 | S20 | EP-03 to EP-13 |
| **EP-16** | Advanced Features | SRS-FX-001 to 003, SRS-REV-001 to 003, SRS-LEASE-001 to 002, SRS-CONST-001 | P2 | S21 | EP-03, EP-11, EP-12 |
| **EP-17** | Phase 2 Release | All P1 SRS | P2 | S22-S24 | EP-11 to EP-16 |
| **EP-18** | Multi-Entity Consolidation | New requirements | P3 | S25-S26 | EP-08, EP-17 |
| **EP-19** | Mobile Application | SO-05 | P3 | S27-S28 | EP-17 |
| **EP-20** | BI/Analytics Platform | SO-04 | P3 | S29-S30 | EP-17 |
| **EP-21** | Advanced Integrations | SO-04 | P3 | S31 | EP-19, EP-20 |
| **EP-22** | HRM Module | Out-of-scope P1 | P3 | S32 | EP-11 |
| **EP-23** | Platform Hardening | SRS-AVAIL-001 to 002, SRS-REL-001 to 002 | P3 | S33-S35 | EP-18 to EP-22 |
| **EP-24** | Phase 3 Release | All P2/P3 SRS | P3 | S36 | EP-18 to EP-23 |

### 5.2 Dependency Graph (Phase 1)

```
EP-01 (Platform Foundation)
    |
    v
EP-02 (Chart of Accounts)
    |
    v
EP-03 (General Ledger Core) <──────────────────────────────────┐
    |                                                           |
    +------------------+------------------+---------------------+
    |                  |                  |                     |
    v                  v                  v                     v
EP-04 (AR)        EP-05 (AP)        EP-09 (Bank/Cash)    EP-11 (Payroll, P2)
    |                  |                  |
    +------------------+                  |
    |                                     |
    v                                     v
EP-06 (E-Invoice)                   EP-08 (Reporting)
    |                                     ^
    v                                     |
EP-07 (Tax) ──────────────────────────────+
    |
    v
EP-10 (Compliance & UAT)
```

### 5.3 Critical Path (Phase 1)

```
EP-01 (S1-S2) → EP-02 (S2-S3) → EP-03 (S3-S4) → EP-06 (S7-S8) → EP-07 (S9-S10) → EP-08 (S10) → EP-10 (S12)
                              ↘ EP-04 (S5-S6) ↗
                              ↘ EP-05 (S5-S6) ↗
                              ↘ EP-09 (S11)   ↗
```

**Critical Path Duration:** 24 weeks (S1 through S12, no slack)

**Buffer Allocation:** 2-week compliance audit buffer embedded in S12, plus 10% contingency per sprint.

---

## 6. MILESTONE TIMELINE

### 6.1 18-Month Gantt View

```
Month:  1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18
        |---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
Phase 1:████████████████████████████████████████████████
M1      ▲
M2              ▲
M3                      ▲
M4                              ▲
M5                                      ▲
M6                                              ▲
Phase 2:                                            ████████████████████████████
M7                                                      ▲
M8                                                              ▲
M9                                                                      ▲
M10                                                                             ▲
Phase 3:                                                                                ████████████████████████████
M11                                                                                     ▲
M12                                                                                             ▲
M13                                                                                                     ▲
M14                                                                                                             ▲
```

### 6.2 Key Dates

| Milestone | Date | Sprint | Description |
|-----------|------|--------|-------------|
| M1: Design Sign-Off | 2026-05-30 | S2 end | Architecture, schema, COA approved |
| M2: Core GL Functional | 2026-07-25 | S4 end | Double-entry, multi-currency, TB working |
| M3: AR/AP Complete | 2026-08-22 | S6 end | Full P2P and O2C flows |
| M4: E-Invoice + Tax | 2026-10-17 | S9 end | E-invoices issued, tax declarations generated |
| M5: Reporting Complete | 2026-11-14 | S10 end | B01-B09 statements generate correctly |
| M6: MVP Launch | 2026-12-12 | S12 end | Compliance audit passed, UAT signed off |
| M7: Payroll Live | 2027-02-06 | S14 end | Full payroll with 2026 rates |
| M8: FA + Inventory Live | 2027-04-03 | S18 end | Complete FA and inventory modules |
| M9: Full Suite Complete | 2027-05-15 | S21 end | All 15 modules operational |
| M10: Phase 2 Release | 2027-06-12 | S24 end | Full accounting suite released |
| M11: Multi-Entity Live | 2027-08-07 | S26 end | Consolidation engine working |
| M12: Mobile App Beta | 2027-09-04 | S28 end | Core mobile features functional |
| M13: BI Platform Live | 2027-10-02 | S30 end | Analytics dashboards operational |
| M14: Enterprise Platform | 2027-12-11 | S36 end | Full enterprise platform released |

---

## 7. RESOURCE ALLOCATION PER SPRINT

### 7.1 Team Composition (15 FTE)

| Role | Count | Allocation |
|------|-------|-----------|
| Project Manager | 1 | 100% |
| Business Analyst (Accounting) | 2 | 100% |
| Certified Accountant (SME) | 1 | 100% |
| Tax Expert (SME) | 1 | 100% |
| Tech Lead | 1 | 100% |
| Backend Developers | 3 | 100% |
| Frontend Developers | 2 | 100% |
| QA Engineers | 2 | 100% |
| DevOps Engineer | 1 | 100% |
| UI/UX Designer | 1 | 100% |

### 7.2 Phase 1 Resource Allocation (Sprints 1-12)

| Sprint | PM | BA | Acct SME | Tax SME | TL | BE | FE | QA | DevOps | UX |
|--------|----|----|----------|---------|----|----|----|----|----|----|
| S1 | 1.0 | 1.0 | 0.5 | 0.5 | 1.0 | 3.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| S2 | 0.5 | 2.0 | 1.0 | 0.5 | 1.0 | 3.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| S3 | 0.5 | 1.0 | 1.0 | 0.5 | 1.0 | 3.0 | 1.0 | 2.0 | 0.5 | 0.5 |
| S4 | 0.5 | 1.0 | 1.0 | 0.5 | 1.0 | 3.0 | 1.0 | 2.0 | 0.5 | 0.5 |
| S5 | 0.5 | 1.5 | 0.5 | 0.5 | 1.0 | 3.0 | 2.0 | 2.0 | 0.5 | 1.0 |
| S6 | 0.5 | 1.5 | 0.5 | 0.5 | 1.0 | 3.0 | 2.0 | 2.0 | 0.5 | 1.0 |
| S7 | 0.5 | 1.0 | 0.5 | 1.0 | 1.0 | 3.0 | 2.0 | 2.0 | 1.0 | 1.0 |
| S8 | 0.5 | 1.0 | 0.5 | 1.0 | 1.0 | 3.0 | 2.0 | 2.0 | 1.0 | 1.0 |
| S9 | 0.5 | 0.5 | 0.5 | 2.0 | 1.0 | 3.0 | 1.0 | 2.0 | 0.5 | 0.5 |
| S10 | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 2.0 | 2.0 | 2.0 | 0.5 | 1.0 |
| S11 | 0.5 | 1.0 | 0.5 | 0.5 | 1.0 | 3.0 | 2.0 | 2.0 | 1.0 | 0.5 |
| S12 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 2.0 | 1.0 | 2.0 | 1.0 | 0.5 |

### 7.3 Phase 2 Resource Allocation (Sprints 13-24)

| Sprint | PM | BA | Acct SME | Tax SME | TL | BE | FE | QA | DevOps | UX |
|--------|----|----|----------|---------|----|----|----|----|----|----|
| S13 | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 3.0 | 1.0 | 2.0 | 0.5 | 0.5 |
| S14 | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 3.0 | 1.0 | 2.0 | 0.5 | 0.5 |
| S15 | 0.5 | 1.0 | 1.0 | 0.5 | 1.0 | 3.0 | 1.0 | 2.0 | 0.5 | 0.5 |
| S16 | 0.5 | 1.0 | 1.0 | 0.5 | 1.0 | 3.0 | 1.0 | 2.0 | 0.5 | 0.5 |
| S17 | 0.5 | 1.0 | 0.5 | 0.5 | 1.0 | 3.0 | 1.0 | 2.0 | 0.5 | 1.0 |
| S18 | 0.5 | 1.0 | 0.5 | 0.5 | 1.0 | 3.0 | 1.0 | 2.0 | 0.5 | 1.0 |
| S19 | 0.5 | 0.5 | 0.5 | 0.5 | 1.0 | 3.0 | 1.0 | 2.0 | 1.0 | 0.5 |
| S20 | 0.5 | 1.0 | 0.5 | 0.5 | 1.0 | 2.0 | 2.0 | 2.0 | 0.5 | 1.0 |
| S21 | 0.5 | 1.0 | 1.0 | 0.5 | 1.0 | 3.0 | 1.0 | 2.0 | 0.5 | 0.5 |
| S22 | 0.5 | 0.5 | 0.5 | 0.5 | 1.0 | 2.0 | 1.0 | 2.0 | 1.0 | 0.5 |
| S23 | 0.5 | 0.5 | 0.5 | 0.5 | 1.0 | 3.0 | 1.0 | 2.0 | 1.0 | 0.5 |
| S24 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 2.0 | 1.0 | 2.0 | 1.0 | 0.5 |

### 7.4 Phase 3 Resource Allocation (Sprints 25-36)

| Sprint | PM | BA | Acct SME | Tax SME | TL | BE | FE | QA | DevOps | UX |
|--------|----|----|----------|---------|----|----|----|----|----|----|
| S25-S26 | 0.5 | 1.0 | 1.0 | 0.5 | 1.0 | 3.0 | 1.0 | 2.0 | 0.5 | 0.5 |
| S27-S28 | 0.5 | 0.5 | 0.5 | 0.0 | 1.0 | 2.0 | 3.0 | 1.5 | 0.5 | 1.5 |
| S29-S30 | 0.5 | 1.0 | 0.5 | 0.5 | 1.0 | 2.0 | 2.0 | 2.0 | 1.0 | 1.0 |
| S31 | 0.5 | 0.5 | 0.5 | 0.5 | 1.0 | 3.0 | 1.0 | 2.0 | 1.0 | 0.5 |
| S32 | 0.5 | 1.0 | 0.5 | 0.5 | 1.0 | 2.0 | 2.0 | 2.0 | 0.5 | 1.0 |
| S33 | 0.5 | 0.5 | 1.0 | 1.0 | 1.0 | 3.0 | 1.0 | 2.0 | 0.5 | 0.5 |
| S34 | 0.5 | 0.5 | 0.5 | 0.5 | 1.0 | 3.0 | 1.0 | 2.0 | 1.0 | 0.5 |
| S35 | 0.5 | 0.5 | 0.5 | 0.5 | 1.0 | 2.0 | 1.0 | 2.0 | 1.5 | 0.5 |
| S36 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 2.0 | 1.0 | 2.0 | 1.0 | 0.5 |

---

## 8. RISK-BASED PRIORITIZATION

### 8.1 Risk-Adjusted Priority Matrix

| Priority | Risk Level | Modules | Rationale |
|----------|-----------|---------|-----------|
| **P0-Critical** | R-01, R-09 (Compliance) | MOD-01, MOD-02, MOD-06, MOD-07, MOD-14, MOD-15 | Legal non-compliance = regulatory sanctions |
| **P0-High** | R-03 (Migration) | MOD-13, MOD-09 | Data migration failures block customer adoption |
| **P0-High** | R-04 (Integration) | MOD-05, MOD-06 | Tax authority/e-invoice integration failures block filing |
| **P1-High** | R-02 (Tax changes) | MOD-10, MOD-06 (advanced) | Tax law changes during development require rework |
| **P1-Medium** | R-06 (Performance) | MOD-07, MOD-08, MOD-09 | Performance issues affect user experience |
| **P2-Medium** | R-07 (Adoption) | MOD-11, MOD-12 | Nice-to-have for MVP, required for full suite |
| **P3-Low** | R-08 (Competition) | Phase 3 features | Market differentiation, not compliance-critical |

### 8.2 Risk Mitigation Schedule

| Risk | Mitigation Action | Sprint | Owner |
|------|------------------|--------|-------|
| R-01: Circular 99 interpretation errors | Monthly review by certified accountant | Every sprint | Acct SME |
| R-02: Tax law changes during development | Modular tax rule engine; configurable rates | S2, S9 | TL + Tax SME |
| R-03: Data migration failures | Parallel run validation tool; migration test suite | S11 | BA + BE |
| R-04: Tax authority API fails | HTKK XML export fallback; manual submission workflow | S9, S12 | BE + DevOps |
| R-05: Security breach | Penetration testing in S23; encryption at rest from S1 | S1, S23 | DevOps + TL |
| R-06: Performance issues | Load testing every sprint from S5; performance budget | S5-S12 | QA + TL |
| R-09: Regulatory non-compliance | External compliance audit at M5 and M10 | S12, S24 | PM + Acct SME |

---

## 9. GO/NO-GO CRITERIA PER MILESTONE

### 9.1 M1: Design Sign-Off (S2 end)

| Criterion | Target | Verification Method |
|-----------|--------|-------------------|
| Architecture document approved | Signed by TL + PM | Document review |
| Database schema finalized | All 15 module tables defined | Schema review |
| Circular 99 COA loaded | 71 L1 + 101 L2 accounts in DB | Data verification |
| UI wireframes approved | Signed by CFO + Chief Accountant | Design review |
| CI/CD pipeline operational | Build + test on every commit | Pipeline check |

### 9.2 M2: Core GL Functional (S4 end)

| Criterion | Target | Verification Method |
|-----------|--------|-------------------|
| Double-entry balance enforcement | 100% of entries balanced | Automated test suite |
| Multi-currency entries | VND + 3 foreign currencies tested | Manual + automated test |
| Trial balance generates | Matches manual calculation | Reconciliation test |
| Period management working | Open/Locked/Closed states enforced | Integration test |
| Test coverage (GL module) | >= 80% | Coverage report |

### 9.3 M3: AR/AP Complete (S6 end)

| Criterion | Target | Verification Method |
|-----------|--------|-------------------|
| Full O2C flow works | Order → Invoice → Payment → GL posting | End-to-end test |
| Full P2P flow works | PO → Receipt → Invoice → Payment → GL | End-to-end test |
| 3-way match blocks discrepancies | PO ≠ Receipt ≠ Invoice blocked | Integration test |
| AR/AP aging reports accurate | Matches manual calculation | Reconciliation test |
| Test coverage (AR/AP) | >= 75% | Coverage report |

### 9.4 M4: E-Invoice + Tax (S9 end)

| Criterion | Target | Verification Method |
|-----------|--------|-------------------|
| E-invoices issued with CQT code | Valid on GDT portal | External verification |
| VAT calculation matches HTKK | Tolerance ±1,000 VND | Comparison test |
| CIT quarterly calculation correct | Matches manual calculation | Reconciliation test |
| PIT withholding correct | Matches statutory formula | Automated test |
| Tax calendar alerts working | 7-day and 1-day alerts trigger | Integration test |
| Digital signature integration | VNPT/Viettel/BKAV tested | Provider integration test |

### 9.5 M5: Reporting Complete (S10 end)

| Criterion | Target | Verification Method |
|-----------|--------|-------------------|
| B01-DN generates correctly | Matches official Circular 99 template | Compliance review |
| B02-DN generates correctly | Account mapping verified | Compliance review |
| B03-DN generates correctly | Cash flow reconciliation | Compliance review |
| B09-DN generates correctly | Notes complete and accurate | Compliance review |
| Accounting books printable | All 5 book types in Circular 99 format | Visual inspection |
| Report generation time | < 30 seconds | Performance test |

### 9.6 M6: MVP Launch Ready (S12 end)

| Criterion | Target | Verification Method |
|-----------|--------|-------------------|
| All P0 SRS requirements met | 100% traceability | Requirements traceability matrix |
| Compliance audit passed | Zero critical findings | External audit report |
| UAT signed off | CFO + Chief Accountant approval | UAT sign-off document |
| Performance targets met | 50K entries/hr, <3s page load | Load test report |
| Security scan passed | Zero high/critical vulnerabilities | Penetration test report |
| Data migration tool validated | Circular 200 → 99 balances match | Parallel run comparison |
| Documentation complete | User guides, API docs, admin guides | Document review |
| Tax declaration test submission | Accepted by GDT test portal | Submission confirmation |

### 9.7 M7: Payroll Live (S14 end)

| Criterion | Target | Verification Method |
|-----------|--------|-------------------|
| 2026 insurance rates correct | Employee 10.5%, Employer 18.5%, KPCD 2% | Automated test |
| PIT calculation matches HTKK | Tolerance ±1,000 VND | Comparison test |
| Payslips generated | All employees receive digital payslip | Manual verification |
| Insurance declaration files | e-BHXH XML format valid | External validation |
| GL posting from payroll | Correct DK/Co entries | Integration test |

### 9.8 M8: FA + Inventory Live (S18 end)

| Criterion | Target | Verification Method |
|-----------|--------|-------------------|
| Depreciation accurate | All 3 methods match manual calculation | Reconciliation test |
| Inventory valuation correct | FIFO and weighted avg match manual | Reconciliation test |
| Asset lifecycle events | Registration → Depreciation → Disposal | End-to-end test |
| Inventory provisions | TK 2294 calculation correct | Automated test |

### 9.9 M9: Full Suite Complete (S21 end)

| Criterion | Target | Verification Method |
|-----------|--------|-------------------|
| All 15 modules operational | Each module passes acceptance criteria | Module-by-module review |
| Management reports functional | Dashboard, KPIs, budget vs actual | User acceptance |
| FX revaluation correct | TK 413 entries match manual | Reconciliation test |
| Revenue recognition correct | VAS 14 compliance verified | Compliance review |

### 9.10 M10: Phase 2 Release (S24 end)

| Criterion | Target | Verification Method |
|-----------|--------|-------------------|
| All P1 SRS requirements met | 100% traceability | Requirements traceability matrix |
| Performance targets met | 100 concurrent users, <3s response | Load test report |
| Security audit passed | Zero high/critical vulnerabilities | Penetration test report |
| UAT signed off | All user classes approve | UAT sign-off document |
| Compliance audit passed | External auditor sign-off | Audit report |

---

## 10. RELEASE STRATEGY

### 10.1 Release Cadence

| Release | Date | Scope | Environment |
|---------|------|-------|------------|
| **R0: Alpha** | S4 end | GL + COA + Auth | Internal dev |
| **R1: Beta 1** | S8 end | GL + AR + AP + E-Invoice | Staging |
| **R2: Beta 2** | S10 end | + Tax + Reporting | Staging |
| **R3: MVP** | S12 end | All Phase 1 modules | Production (pilot) |
| **R4: GA Phase 1** | S12 + 4 weeks | Production hardening | Production |
| **R5: Phase 2 Beta** | S20 end | + Payroll + FA + Inventory | Staging |
| **R6: Phase 2 GA** | S24 end | Full accounting suite | Production |
| **R7: Phase 3 Beta** | S32 end | + Multi-entity + Mobile | Staging |
| **R8: Enterprise GA** | S36 end | Full platform | Production |

### 10.2 Deployment Strategy

| Phase | Strategy | Rollback Plan |
|-------|----------|--------------|
| Alpha/Beta | Blue-green deployment | Switch to previous environment |
| MVP | Canary release (10% → 50% → 100%) | Revert to Beta 2 |
| GA Releases | Rolling update | Automated rollback on health check failure |

### 10.3 Release Criteria

| Criterion | MVP (R3) | GA (R4+) |
|-----------|----------|----------|
| Test coverage | >= 70% | >= 80% |
| Critical bugs | 0 | 0 |
| High bugs | <= 3 | 0 |
| Performance | Meets baseline | Exceeds baseline by 20% |
| Compliance | Internal audit passed | External audit passed |
| Documentation | User guides complete | Full documentation suite |

### 10.4 Post-Release Support

| Activity | Timeline | Owner |
|----------|----------|-------|
| Hypercare (intensive support) | 2 weeks post-release | Full team |
| Bug fix window | 4 weeks post-release | Dev + QA |
| Feature stabilization | 8 weeks post-release | Dev |
| Compliance monitoring | Ongoing | Acct SME + Tax SME |
| Tax law update window | As needed | Tax SME + Dev |

---

**END OF PROJECT ROADMAP**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | April 2026 | Project Management Office | Initial release |
