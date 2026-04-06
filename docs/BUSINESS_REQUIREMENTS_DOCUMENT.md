# BUSINESS REQUIREMENTS DOCUMENT (BRD)
# Vietnamese Enterprise Accounting Software Platform
# Compliant with Circular 99/2025/TT-BTC & Latest Vietnamese Tax Laws

**Document Version:** 1.0
**Date:** April 2026
**Prepared by:** CFO Office (20 Years Experience)
**Classification:** Confidential
**Status:** Draft for Stakeholder Review

---

## TABLE OF CONTENTS

1. Executive Summary
2. Business Objectives
3. Problem Statement
4. Business Scope
5. Stakeholder Analysis
6. Business Process Overview
7. Functional Business Requirements
8. Financial & Economic Justification
9. Risk Assessment & Mitigation
10. Regulatory & Compliance Framework
11. Implementation Strategy
12. Success Metrics & KPIs
13. Budget & Resource Estimation
14. Timeline & Milestones
15. Assumptions & Constraints
16. Approval & Sign-Off

---

## 1. EXECUTIVE SUMMARY

### 1.1 Business Context

Vietnam's Ministry of Finance has issued **Circular 99/2025/TT-BTC**, a comprehensive new accounting regime that **replaces Circular 200/2014/TT-BTC** effective **01/01/2026**, applicable to fiscal years beginning on or after this date. Enterprises currently using **Circular 133/2016/TT-BTC** (small and medium enterprises) may continue using TT133 or voluntarily migrate to TT99. Simultaneously, Vietnam has enacted significant tax law reforms:

- **New Corporate Income Tax Law** (Law 67/2025/QH15)
- **New Personal Income Tax Law** (Law 109/2025/QH15)
- **Amended VAT Law** (Law 149/2025/QH15)
- **New Tax Administration Law** (Law 108/2025/QH15)
- **Updated Electronic Invoice Regulations** (Decree 70/2025/ND-CP, Circular 32/2025/TT-BTC)

This creates an urgent business need for an accounting software platform that is fully compliant with all current Vietnamese regulations, supports seamless transition from old regimes, and provides comprehensive financial management capabilities.

### 1.2 Business Vision

To build a modern, cloud-based Vietnamese enterprise accounting software that:
- Ensures 100% compliance with Circular 99/2025/TT-BTC and all current tax laws
- Reduces accounting processing time by 60%
- Eliminates tax filing errors and associated penalties
- Provides real-time financial visibility for management decision-making
- Supports enterprises of all sizes (micro to large)

### 1.3 Investment Rationale

The regulatory transition deadline of 01/01/2026 creates a time-critical market opportunity. Enterprises currently using Circular 200-based systems must migrate, creating immediate demand. The Vietnamese accounting software market (dominated by MISA, Fast, Bravo) requires a modern, compliant alternative with superior user experience.

---

## 2. BUSINESS OBJECTIVES

### 2.1 Primary Objectives

| ID | Objective | Target | Timeline |
|----|-----------|--------|----------|
| BO-01 | Achieve full Circular 99/2025 compliance | 100% compliance | Q3 2026 |
| BO-02 | Support all current tax laws (CIT, PIT, VAT, Tax Admin) | 100% coverage | Q3 2026 |
| BO-03 | Reduce monthly closing time | From 10 days to 3 days | Q4 2026 |
| BO-04 | Reduce tax filing errors | From 5% to <0.5% | Q4 2026 |
| BO-05 | Achieve automated bank reconciliation | 85% auto-match rate | Q4 2026 |

### 2.2 Strategic Objectives

| ID | Objective | Target |
|----|-----------|--------|
| SO-01 | Market share in Vietnamese accounting software | 15% within 3 years |
| SO-02 | Customer retention rate | >90% annually |
| SO-03 | Support multi-branch, multi-currency operations | Full support |
| SO-04 | Integration ecosystem (banks, tax authority, e-invoice providers) | 50+ integrations |
| SO-05 | Mobile accessibility | Full mobile app support |

---

## 3. PROBLEM STATEMENT

### 3.1 Current Pain Points

1. **Regulatory Transition Risk**: Enterprises using Circular 200/2014 must transition to Circular 99/2025 for fiscal years beginning on or after 01/01/2026. Enterprises using Circular 133/2016 may continue or voluntarily migrate. Existing software may not be updated in time.

2. **Fragmented Tax Compliance**: Multiple tax laws with frequent updates require manual tracking and calculation, leading to errors and penalties.

3. **Manual Processes**: Many enterprises still use Excel-based accounting, which is error-prone, time-consuming, and lacks audit trails.

4. **Invoice Management Complexity**: Decree 70/2025 introduces new e-invoice rules (replacement, adjustment, discount invoices) that require sophisticated handling.

5. **Financial Reporting Delays**: Manual financial statement preparation takes 7-15 days, delaying management decisions.

6. **Data Silos**: Accounting, tax, payroll, and inventory data often reside in separate systems, causing reconciliation challenges.

7. **Audit Readiness**: Lack of proper audit trails and document management creates compliance risks.

### 3.2 Business Impact

| Issue | Annual Cost Impact | Risk Level |
|-------|-------------------|------------|
| Tax filing errors & penalties | 50-500 million VND | High |
| Delayed financial reporting | Lost decision-making value | High |
| Manual data entry errors | 20-100 million VND | Medium |
| Staff time on repetitive tasks | 200-500 hours/month | High |
| Non-compliance with Circular 99 | Regulatory sanctions | Critical |

---

## 4. BUSINESS SCOPE

### 4.1 In-Scope

| Module | Description |
|--------|-------------|
| **General Ledger** | Chart of accounts (Circular 99), journal entries, general ledger, trial balance |
| **Accounts Receivable** | Customer management, invoicing, payment tracking, aging, bad debt provisions |
| **Accounts Payable** | Supplier management, invoice processing, payment scheduling, aging |
| **Inventory** | Stock management, valuation (FIFO, weighted average), provisions, allocation |
| **Fixed Assets** | Asset registry, depreciation, transfers, disposals, revaluation |
| **Payroll** | Salary calculation, insurance (BHXH, BHYT, BHTN), union fees, PIT withholding |
| **Tax Management** | VAT, CIT, PIT, License Fee, Foreign Contractor Tax calculations and declarations |
| **E-Invoice** | Creation, management, correction, replacement per Decree 70/2025 |
| **Bank & Cash** | Cash management, bank reconciliation, payment processing |
| **Financial Reporting** | B01, B02, B03, B09 statements per Circular 99, management reports |
| **Accounting Books** | General journal, general ledger, subsidiary ledgers, fixed asset register |
| **Data Migration** | Circular 200 to Circular 99 balance transfer |

### 4.2 Out-of-Scope (Phase 1)

| Item | Reason | Future Phase |
|------|--------|-------------|
| Manufacturing ERP (MRP, BOM) | Complexity | Phase 3 |
| Customer Relationship Management (CRM) | Separate domain | Phase 3 |
| Human Resources Management (HRM) | Separate domain | Phase 2 |
| Business Intelligence & Advanced Analytics | Requires data maturity | Phase 2 |
| Multi-entity consolidation | Complex requirement | Phase 2 |
| Mobile application | Requires separate development | Phase 2 |

---

## 5. STAKEHOLDER ANALYSIS

### 5.1 Stakeholder Matrix

| Stakeholder | Interest | Influence | Engagement Strategy |
|-------------|----------|-----------|-------------------|
| **CFO / Finance Director** | Financial control, compliance, reporting | High | Weekly demos, UAT participation |
| **Chief Accountant** | Daily operations, accuracy, efficiency | High | Design workshops, pilot testing |
| **Tax Accountant** | Tax compliance, declaration accuracy | Medium | Feature validation, tax rule testing |
| **External Auditor** | Audit trail, compliance evidence | Medium | Compliance review sessions |
| **IT Department** | Integration, security, infrastructure | High | Technical architecture review |
| **CEO / Board** | Strategic oversight, ROI | High | Quarterly steering committee |
| **Tax Authority** | Compliance, data accuracy | High (regulatory) | Compliance certification |
| **End Users (Accountants)** | Usability, efficiency | Medium | User testing, feedback sessions |

### 5.2 User Personas

**Persona 1: Chi - Chief Accountant (35 years old)**
- 10 years experience
- Manages team of 5 accountants
- Needs: Quick overview, approval workflow, compliance assurance
- Pain points: Month-end closing takes too long, manual reconciliation

**Persona 2: Minh - Tax Accountant (28 years old)**
- 4 years experience
- Handles all tax declarations
- Needs: Automated tax calculations, up-to-date tax rates, declaration forms
- Pain points: Frequent tax law changes, manual HTKK data entry

**Persona 3: Lan - Payroll Accountant (32 years old)**
- 6 years experience
- Manages payroll for 200 employees
- Needs: Automated salary calculation, insurance tracking, PIT withholding
- Pain points: Complex insurance rate changes, dependent management

---

## 6. BUSINESS PROCESS OVERVIEW

### 6.1 Core Business Processes

```
┌─────────────────────────────────────────────────────────────────────┐
│                     ACCOUNTING BUSINESS PROCESSES                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐           │
│  │  PROCUREMENT │───>│  INVENTORY   │───>│    SALES     │           │
│  │  TO PAY      │    │  MANAGEMENT  │    │  TO CASH     │           │
│  └──────────────┘    └──────────────┘    └──────────────┘           │
│         │                    │                    │                  │
│         v                    v                    v                  │
│  ┌──────────────────────────────────────────────────────┐           │
│  │              GENERAL LEDGER & JOURNAL                │           │
│  └──────────────────────────────────────────────────────┘           │
│                              │                                       │
│              ┌───────────────┼───────────────┐                      │
│              v               v               v                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │  TAX MGMT    │  │  PAYROLL     │  │  FIXED ASSET │              │
│  │  & DECLARATION│  │  MANAGEMENT  │  │  MANAGEMENT  │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
│              │               │               │                      │
│              v               v               v                      │
│  ┌──────────────────────────────────────────────────────┐           │
│  │          FINANCIAL REPORTING & COMPLIANCE            │           │
│  │  (B01, B02, B03, B09 per Circular 99/2025)          │           │
│  └──────────────────────────────────────────────────────┘           │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 6.2 Process Hierarchy

| Level 1 | Level 2 | Level 3 |
|---------|---------|---------|
| Procure-to-Pay | Purchase Order | PO creation, approval, receipt |
| Procure-to-Pay | Invoice Processing | Invoice receipt, verification, matching |
| Procure-to-Pay | Payment Processing | Payment scheduling, execution, reconciliation |
| Sales-to-Cash | Order Management | Order entry, pricing, confirmation |
| Sales-to-Cash | Invoicing | E-invoice creation, delivery, tracking |
| Sales-to-Cash | Collection | Payment receipt, matching, aging |
| Record-to-Report | Journal Entry | Entry creation, approval, posting |
| Record-to-Report | Period Close | Reconciliation, accruals, closing |
| Record-to-Report | Financial Reporting | Statement generation, review, submission |
| Hire-to-Retire | Payroll Processing | Time tracking, calculation, payment |
| Hire-to-Retire | Tax Withholding | PIT calculation, declaration, payment |
| Hire-to-Retire | Insurance Management | BHXH, BHYT, BHTN calculation, reporting |

---

## 7. FUNCTIONAL BUSINESS REQUIREMENTS

### 7.1 Business Requirement Prioritization

| Priority | Definition | Criteria |
|----------|------------|----------|
| **P0 - Critical** | Must have for launch | Legal compliance, core accounting |
| **P1 - High** | Required within 3 months | Tax management, reporting |
| **P2 - Medium** | Required within 6 months | Advanced features, integrations |
| **P3 - Low** | Future enhancement | Nice-to-have features |

### 7.2 Business Requirements by Module

#### 7.2.1 General Ledger (P0)

| BR-ID | Requirement | Priority | Business Value |
|-------|-------------|----------|----------------|
| BR-GL-01 | Full Circular 99 chart of accounts (71 L1, 101 L2 accounts) | P0 | Legal compliance |
| BR-GL-02 | Double-entry bookkeeping with balance enforcement | P0 | Accounting integrity |
| BR-GL-03 | Multi-currency support with exchange rate management | P0 | International operations |
| BR-GL-04 | Period management (open/close) with audit trail | P0 | Data integrity |
| BR-GL-05 | Reversing entries and adjustment entries | P0 | Correction capability |
| BR-GL-06 | Automatic balance transfer from Circular 200 | P0 | Migration support |

#### 7.2.2 Tax Management (P0)

| BR-ID | Requirement | Priority | Business Value |
|-------|-------------|----------|----------------|
| BR-TAX-01 | VAT calculation with multiple rates (10%, 8%, 0%, non-taxable) | P0 | Tax compliance |
| BR-TAX-02 | VAT declaration forms (01/GTGT, 04/GTGT) | P0 | Legal filing |
| BR-TAX-03 | CIT quarterly provisional + annual finalization | P0 | Tax compliance |
| BR-TAX-04 | PIT monthly/quarterly + annual finalization | P0 | Tax compliance |
| BR-TAX-05 | License fee calculation and declaration | P0 | Tax compliance |
| BR-TAX-06 | Foreign contractor tax management | P1 | Compliance |
| BR-TAX-07 | Global minimum tax support (per NQ 107/2023/QH15, NĐ 18/2024/ND-CP, NĐ 320/2025/ND-CP) | P1 | Compliance |
| BR-TAX-08 | Tax calendar with deadline alerts | P1 | Penalty prevention |

#### 7.2.3 Electronic Invoices (P0)

| BR-ID | Requirement | Priority | Business Value |
|-------|-------------|----------|----------------|
| BR-EINV-01 | E-invoice creation with tax authority code | P0 | Legal compliance |
| BR-EINV-02 | Invoice replacement workflow (Decree 70/2025) | P0 | Error correction |
| BR-EINV-03 | Invoice adjustment (increase/decrease) | P0 | Error correction |
| BR-EINV-04 | Commercial discount invoice handling | P0 | Business operations |
| BR-EINV-05 | Returned goods invoice processing | P0 | Business operations |
| BR-EINV-06 | Internal consumption invoice | P0 | Compliance |
| BR-EINV-07 | Invoice verification with tax authority | P1 | Fraud prevention |

#### 7.2.4 Financial Reporting (P0)

| BR-ID | Requirement | Priority | Business Value |
|-------|-------------|----------|----------------|
| BR-RPT-01 | B01-DN: Statement of Financial Position | P0 | Legal requirement |
| BR-RPT-02 | B02-DN: Statement of Business Results | P0 | Legal requirement |
| BR-RPT-03 | B03-DN: Cash Flow Statement | P0 | Legal requirement |
| BR-RPT-04 | B09-DN: Notes to Financial Statements | P0 | Legal requirement |
| BR-RPT-05 | Interim financial reports | P1 | Management needs |
| BR-RPT-06 | Trial balance and account detail reports | P0 | Audit support |
| BR-RPT-07 | Management dashboard with KPIs | P2 | Decision support |

#### 7.2.5 Payroll & Insurance (P0)

| BR-ID | Requirement | Priority | Business Value |
|-------|-------------|----------|----------------|
| BR-PAY-01 | Salary calculation with allowances and deductions | P0 | Core payroll |
| BR-PAY-02 | Insurance calculation with correct 2026 rates: Employee (BHXH 8%, BHYT 1.5%, BHTN 1% = 10.5% total); Employer (BHXH 14%, BHYT 3%, BHTN 1%, BHTNLĐ-BNN 0.5% = 18.5% total) | P0 | Legal compliance |
| BR-PAY-02a | KPCD (Union Fee) calculation: 2% on social insurance wage base (quỹ lương đóng BHXH), not actual salary | P0 | Legal compliance |
| BR-PAY-03 | ~~Union fees (KPCD 2%)~~ *(merged into BR-PAY-02a)* | P0 | Legal compliance |
| BR-PAY-04 | PIT withholding with dependent deductions | P0 | Tax compliance |
| BR-PAY-05 | Overtime calculation per Labor Law | P0 | Legal compliance |
| BR-PAY-06 | Electronic labor contracts (Decree 337/2025) | P1 | Compliance |
| BR-PAY-07 | Occupational accident & disease insurance (BHTNLĐ-BNN): Employer 0.5% | P0 | Legal compliance (Luật ATVSLĐ) |

#### 7.2.6 Inventory (P1)

| BR-ID | Requirement | Priority | Business Value |
|-------|-------------|----------|----------------|
| BR-INV-01 | Multiple valuation methods (FIFO, weighted average) | P1 | Accurate costing |
| BR-INV-02 | Stock movement tracking (receipt, issue, transfer) | P1 | Inventory control |
| BR-INV-03 | Inventory provision calculation | P1 | Accurate reporting |
| BR-INV-04 | Material allocation to cost centers | P1 | Cost accuracy |

#### 7.2.7 Fixed Assets (P1)

| BR-ID | Requirement | Priority | Business Value |
|-------|-------------|----------|----------------|
| BR-FA-01 | Asset registration with full documentation | P1 | Asset tracking |
| BR-FA-02 | Depreciation calculation (straight-line, declining balance) | P1 | Accurate costing |
| BR-FA-03 | Asset transfer, disposal, revaluation | P1 | Asset lifecycle |
| BR-FA-04 | Depreciation schedule generation | P1 | Reporting |

#### 7.2.8 Digital Signature & Security (P0)

| BR-ID | Requirement | Priority | Business Value |
|-------|-------------|----------|----------------|
| BR-DS-01 | Digital signature (chữ ký số) integration for e-invoice signing | P0 | Legal compliance (NĐ 70/2025, Luật GDĐT) |
| BR-DS-02 | Digital signature for electronic tax declaration submission | P0 | Legal compliance (Luật QL Thuế) |
| BR-DS-03 | Support multiple digital signature providers (VNPT, Viettel, BKAV, Safe-CA) | P0 | Vendor flexibility |

#### 7.2.9 Accounting Policy & System Configuration (P0)

| BR-ID | Requirement | Priority | Business Value |
|-------|-------------|----------|----------------|
| BR-AP-01 | Accounting Policy Document (Quy chế hạch toán) management | P0 | Required per TT99 Article 11 when customizing accounts |
| BR-AP-02 | TK 911 year-end closing automation (transfer all revenue/cost to 911, net to 421) | P0 | Year-end compliance |
| BR-AP-03 | Exchange rate revaluation (TK 413) at period-end for all foreign currency monetary items | P0 | Accurate FX reporting |
| BR-AP-04 | CCDC allocation (TK 242 → 642/641/627) with configurable allocation periods | P0 | Accurate cost allocation |
| BR-AP-05 | Construction progress accounting (TK 337) for construction enterprises | P1 | Industry-specific compliance |

---

## 8. FINANCIAL & ECONOMIC JUSTIFICATION

### 8.1 Cost-Benefit Analysis

| Category | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 |
|----------|--------|--------|--------|--------|--------|
| **Costs** | | | | | |
| Development | 5,000M VND | 1,500M | 1,000M | 800M | 600M |
| Infrastructure | 500M | 600M | 700M | 800M | 900M |
| Operations | 300M | 400M | 500M | 600M | 700M |
| Marketing | 200M | 300M | 400M | 400M | 400M |
| **Total Costs** | **6,000M** | **2,800M** | **2,600M** | **2,600M** | **2,600M** |
| **Revenue** | | | | | |
| Subscription | 1,000M | 4,000M | 8,000M | 12,000M | 15,000M |
| Implementation | 500M | 1,500M | 2,500M | 3,000M | 3,500M |
| Support | 100M | 500M | 1,000M | 1,500M | 2,000M |
| **Total Revenue** | **1,600M** | **6,000M** | **11,500M** | **16,500M** | **20,500M** |
| **Net Cash Flow** | **-4,400M** | **3,200M** | **8,900M** | **13,900M** | **17,900M** |

### 8.2 ROI Analysis

- **Total 5-Year Investment**: 16,600M VND
- **Total 5-Year Revenue**: 56,100M VND
- **Net Present Value (NPV)**: 25,800M VND (at 12% discount rate)
- **Internal Rate of Return (IRR)**: 47%
- **Payback Period**: 18 months
- **ROI (5-year)**: 238%

### 8.3 Customer Value Proposition

| Benefit | Value per Customer (Annual) |
|---------|---------------------------|
| Reduced accounting staff time | 120-200 million VND |
| Eliminated tax penalties | 50-200 million VND |
| Faster financial closing | 30-80 million VND (decision value) |
| Reduced audit preparation time | 20-50 million VND |
| **Total Annual Savings** | **220-530 million VND** |

---

## 9. RISK ASSESSMENT & MITIGATION

### 9.1 Risk Register

| Risk ID | Risk Description | Probability | Impact | Risk Level | Mitigation Strategy |
|---------|-----------------|-------------|--------|------------|-------------------|
| R-01 | Circular 99 interpretation errors | Medium | Critical | High | Engage Ministry of Finance certified accounting expert for monthly review; legal review |
| R-02 | Tax law changes during development | High | High | High | Modular tax rule engine; frequent regulatory monitoring |
| R-03 | Data migration failures from Circular 200 | Medium | High | High | Comprehensive testing; parallel run validation |
| R-04 | Integration with tax authority systems fails | Medium | Critical | High | Early API testing; fallback manual submission |
| R-05 | Security breach / data leak | Low | Critical | High | Enterprise-grade security; penetration testing |
| R-06 | Performance issues with large datasets | Medium | Medium | Medium | Load testing; scalable architecture |
| R-07 | User adoption resistance | Medium | Medium | Medium | Comprehensive training; intuitive UI design |
| R-08 | Competitive pressure from MISA/Fast | High | Medium | Medium | Differentiate on compliance and UX |
| R-09 | Regulatory non-compliance penalties | Low | Critical | High | Continuous compliance audit; certification |
| R-10 | Key personnel loss | Medium | High | High | Knowledge documentation; cross-training |

### 9.2 Risk Response Matrix

```
Impact
  ^
  |  R-05    R-01    R-09
C |  R-04    R-03
r |          R-07    R-02
i |  R-06    R-08
t |________________________>
  Low    Medium    High
         Probability
```

---

## 10. REGULATORY & COMPLIANCE FRAMEWORK

### 10.1 Applicable Regulations

| Regulation | Subject | Effective Date | Compliance Status |
|------------|---------|---------------|-------------------|
| Circular 99/2025/TT-BTC | Accounting Regime | 01/01/2026 | Mandatory |
| Law 67/2025/QH15 | Corporate Income Tax | 01/10/2025 | Mandatory |
| Law 109/2025/QH15 | Personal Income Tax | 01/07/2026 | Mandatory |
| Law 149/2025/QH15 | VAT (Amended) | 01/01/2026 | Mandatory |
| Law 108/2025/QH15 | Tax Administration | 01/07/2026 | Mandatory |
| Decree 70/2025/ND-CP | Electronic Invoices | 20/03/2025 | Mandatory |
| Circular 32/2025/TT-BTC | E-Invoice Guidance | 31/05/2025 | Mandatory |
| Decree 320/2025/ND-CP | CIT Guidance | 01/01/2026 | Mandatory |
| Decree 181/2025/ND-CP | VAT Guidance | 01/07/2025 | Mandatory |
| Decree 359/2025/ND-CP | VAT Guidance (Amended) | 31/12/2025 | Mandatory |
| Decree 310/2025/ND-CP | Tax Penalties | 02/12/2025 | Mandatory |
| Decree 337/2025/ND-CP | E-Labor Contracts | 01/01/2026 | Mandatory |
| Decree 52/2024/ND-CP | Cashless Payments | Active | Mandatory |
| Resolution 204/2025/QH15 | 8% VAT Reduction | 01/07/2025-31/12/2026 | Temporary |
| Decree 373/2025/ND-CP | Tax Administration (Amended) | 31/12/2025 | Mandatory |
| Circular 69/2025/TT-BTC | VAT Guidance | 01/07/2025 | Mandatory |
| Circular 20/2026/TT-BTC | CIT Guidance | 2026 | Mandatory |
| Decree 362/2025/ND-CP | Fees & Charges Law | 31/12/2025 | Mandatory |
| Decree 20/2026/ND-CP | Resolution 198/2025 Guidance | 15/01/2026 | Mandatory |
| Decree 43/2025/ND-CP | Accounting Document Archiving | Active | Mandatory |

### 10.2 Compliance Certification Strategy

1. **Internal Compliance Review**: Monthly review by certified Vietnamese accountant
2. **External Audit**: Annual audit by Big 4 or top-tier Vietnamese audit firm
3. **Tax Authority Validation**: Submit test declarations for validation
4. **Certification**: Obtain compliance certificate from Ministry of Finance

---

## 11. IMPLEMENTATION STRATEGY

### 11.1 Phased Approach

| Phase | Duration | Scope | Deliverables |
|-------|----------|-------|-------------|
| **Phase 1: Foundation** | Months 1-6 | Core GL, AR, AP, E-Invoice, Tax (VAT, CIT, PIT), B01-B09 reports | MVP compliant with Circular 99 |
| **Phase 2: Enhancement** | Months 7-12 | Payroll, Fixed Assets, Inventory, Bank Integration, Management Reports | Full accounting suite |
| **Phase 3: Advanced** | Months 13-18 | Multi-entity, Mobile App, BI/Analytics, Advanced Integrations | Enterprise platform |

### 11.2 Technology Strategy

| Aspect | Recommendation | Rationale |
|--------|---------------|-----------|
| Architecture | Cloud-native, microservices | Scalability, maintainability |
| Database | PostgreSQL with row-level security | ACID compliance, data isolation |
| Frontend | React/Next.js with Vietnamese i18n | Performance, localization |
| Backend | Python (Django/FastAPI) or Node.js | Rapid development, ecosystem |
| Hosting | AWS/GCP Vietnam region | Data sovereignty, performance |
| Integration | REST APIs + webhooks | Flexibility, extensibility |

### 11.3 Data Migration Strategy

1. **Assessment**: Analyze existing Circular 200 data structure
2. **Mapping**: Create account mapping (Circular 200 -> Circular 99)
3. **Extraction**: Export data from legacy system
4. **Transformation**: Apply balance transfer rules per Article 19 of Circular 99
5. **Validation**: Parallel run comparison (old system vs. new system)
6. **Cutover**: Final data migration with reconciliation sign-off

---

## 12. SUCCESS METRICS & KPIs

### 12.1 Business KPIs

| KPI | Baseline | Target | Measurement |
|-----|----------|--------|-------------|
| Monthly closing time | 10 days | 3 days | Days from period end |
| Tax filing accuracy | 95% | 99.5% | Error-free submissions / total |
| Bank reconciliation auto-match | 0% | 85% | Auto-matched / total transactions |
| Invoice processing time | 30 min | 5 min | Minutes per invoice |
| Financial report generation | 7 days | Real-time | Time from request to delivery |
| User adoption rate | N/A | >80% | Active users / licensed users |
| Customer satisfaction | N/A | >4.5/5 | Quarterly survey |
| System uptime | N/A | 99.9% | Monthly availability |

### 12.2 Financial KPIs

| KPI | Target | Timeline |
|-----|--------|----------|
| Customer Acquisition Cost (CAC) | <15M VND | Year 1 |
| Customer Lifetime Value (LTV) | >200M VND | Year 2 |
| LTV:CAC Ratio | >10:1 | Year 2 |
| Monthly Recurring Revenue (MRR) Growth | 15% MoM | Year 1 |
| Churn Rate | <5% annually | Year 2 |
| Gross Margin | >70% | Year 2 |

---

## 13. BUDGET & RESOURCE ESTIMATION

### 13.1 Phase 1 Budget (Months 1-6)

| Category | Amount (M VND) | Details |
|----------|---------------|---------|
| **Personnel** | 3,600 | 15 FTE x 6 months x 40M avg |
| **Infrastructure** | 300 | Cloud, development tools |
| **Legal & Compliance** | 200 | Expert consultants, legal review |
| **Testing & QA** | 300 | Test environments, automation tools |
| **Contingency (15%)** | 660 | Risk buffer |
| **Total Phase 1** | **5,060** | |

### 13.2 Team Composition

| Role | Count | Responsibility |
|------|-------|---------------|
| Project Manager | 1 | Overall delivery |
| Business Analyst (Accounting) | 2 | Requirements, compliance |
| Certified Accountant (SME) | 1 | Circular 99 expertise |
| Tax Expert (SME) | 1 | Tax law expertise |
| Tech Lead | 1 | Architecture, code quality |
| Backend Developers | 3 | Core development |
| Frontend Developers | 2 | UI/UX development |
| QA Engineers | 2 | Testing, compliance validation |
| DevOps Engineer | 1 | Infrastructure, CI/CD |
| UI/UX Designer | 1 | Interface design |

---

## 14. TIMELINE & MILESTONES

### 14.1 Phase 1 Timeline (6 Months)

```
Month 1: Discovery & Design
├── W1-2: Requirements finalization, regulatory analysis
├── W3-4: Architecture design, database schema, UI wireframes
└── Milestone: Design Sign-Off

Month 2-3: Core Development
├── W1-4: Chart of accounts, GL engine, journal entries
├── W5-8: AR/AP modules, basic reporting
└── Milestone: Core GL Functional

Month 4: Tax & E-Invoice
├── W1-2: VAT, CIT, PIT calculation engines
├── W3-4: E-invoice integration, declaration forms
└── Milestone: Tax Module Complete

Month 5: Financial Reporting
├── W1-2: B01, B02, B03, B09 report templates
├── W3-4: Accounting books, trial balance
└── Milestone: Reporting Complete

Month 6: Testing & Compliance
├── W1-2: Integration testing, UAT
├── W3-4: Compliance audit, performance testing
└── Milestone: MVP Launch Ready
```

### 14.2 Key Milestones

| Milestone | Target Date | Dependencies |
|-----------|-------------|-------------|
| Design Sign-Off | Month 1, Week 4 | Requirements approved |
| Core GL Functional | Month 3, Week 4 | Design approved |
| Tax Module Complete | Month 4, Week 4 | GL functional |
| Reporting Complete | Month 5, Week 4 | All modules functional |
| Compliance Audit | Month 6, Week 2 | All features complete |
| MVP Launch | Month 6, Week 4 | Compliance passed |

---

## 15. ASSUMPTIONS & CONSTRAINTS

### 15.1 Assumptions

| ID | Assumption | Validation |
|----|-----------|------------|
| A-01 | Circular 99/2025 will not be significantly amended before launch | Monitor MOF announcements |
| A-02 | Tax authority e-filing APIs will be available and documented | Early engagement with GDT |
| A-03 | Target enterprises have internet connectivity for cloud access | Market research |
| A-04 | Sufficient qualified developers are available | Recruitment pipeline |
| A-05 | Enterprises are willing to migrate from existing systems | Market validation |

### 15.2 Constraints

| ID | Constraint | Impact |
|----|-----------|--------|
| C-01 | Data must be stored in Vietnam (data sovereignty) | Hosting location limited |
| C-02 | System must support Vietnamese language and number formatting | UI/UX complexity |
| C-03 | Must comply with Vietnamese Accounting Standards | Development complexity |
| C-04 | Budget ceiling of 5,060M VND for Phase 1 | Resource constraints |
| C-05 | 6-month timeline to MVP | Scope prioritization required |

---

## 16. APPROVAL & SIGN-OFF

| Role | Name | Signature | Date |
|------|------|-----------|------|
| CFO / Project Sponsor | | | |
| Chief Accountant | | | |
| IT Director | | | |
| Legal Counsel | | | |
| Project Manager | | | |

---

**END OF BUSINESS REQUIREMENTS DOCUMENT**
