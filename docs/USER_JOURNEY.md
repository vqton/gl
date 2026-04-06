# USER JOURNEY DOCUMENT
# Vietnamese Enterprise Accounting Software
# Compliant with Circular 99/2025/TT-BTC

**Document Version:** 1.0
**Date:** April 2026
**Prepared by:** CFO Office

---

## TABLE OF CONTENTS

1. User Journey Overview
2. Journey Map: Chief Accountant - Monthly Close
3. Journey Map: Tax Accountant - VAT Declaration
4. Journey Map: AR Accountant - Invoice to Cash
5. Journey Map: AP Accountant - Procure to Pay
6. Journey Map: Payroll Accountant - Monthly Payroll
7. Journey Map: Cashier - Daily Cash Operations
8. Journey Map: Fixed Asset Accountant - Asset Lifecycle
9. Journey Map: CFO - Financial Dashboard & Reporting
10. Journey Map: New Enterprise Onboarding (Circular 200 Migration)
11. Journey Map: Auditor - Compliance Review
12. Pain Points & Opportunities
13. Journey Metrics

---

## 1. USER JOURNEY OVERVIEW

### 1.1 Journey Scope

This document maps the end-to-end user journeys for all key personas interacting with the Vietnamese Enterprise Accounting Software. Each journey covers:

- **Trigger**: What initiates the journey
- **Phases**: Sequential steps the user takes
- **Touchpoints**: System interactions
- **Emotions**: User satisfaction/frustration points
- **Opportunities**: Areas for improvement

### 1.2 Personas Covered

| Persona | Primary Journeys |
|---------|-----------------|
| Chief Accountant (Chi) | Monthly close, financial review, team management |
| Tax Accountant (Minh) | VAT declaration, CIT filing, PIT filing |
| AR Accountant | Invoice creation, payment collection, aging management |
| AP Accountant | Invoice processing, payment execution, vendor reconciliation |
| Payroll Accountant (Lan) | Monthly payroll, insurance reporting, PIT withholding |
| Cashier | Daily receipts/payments, bank reconciliation |
| Fixed Asset Accountant | Asset registration, depreciation, disposal |
| CFO/Finance Director | Dashboard review, strategic reporting, approvals |
| Auditor | Compliance review, audit trail examination |
| New Customer | System onboarding, data migration, initial setup |

---

## 2. JOURNEY MAP: CHIEF ACCOUNTANT - MONTHLY CLOSE

### 2.1 Journey Overview

**Persona:** Chi, Chief Accountant (35 years, 10 years experience)
**Trigger:** Month-end approaching (25th of each month)
**Goal:** Complete monthly accounting close within 3 days
**Success Criteria:** All accounts reconciled, trial balance balanced, reports generated

### 2.2 Journey Phases

```
Phase 1: Preparation          Phase 2: Reconciliation        Phase 3: Review & Close
┌─────────────────────┐      ┌─────────────────────┐      ┌─────────────────────┐
│ - Review open items  │      │ - Bank reconciliation│      │ - Review trial balance│
│ - Check pending docs │      │ - AR/AP reconciliation│      │ - Verify adjustments  │
│ - Notify team members│      │ - Inventory count    │      │ - Approve entries     │
│ - Set period status  │      │ - Fixed asset check  │      │ - Generate reports    │
│                      │      │ - Tax reconciliation │      │ - Close period        │
└─────────────────────┘      └─────────────────────┘      └─────────────────────┘
     Day -5 to -3                  Day -3 to -1                  Day 0 to +1
```

### 2.3 Detailed Journey Steps

| Step | Action | System Interaction | Emotion | Time |
|------|--------|-------------------|---------|------|
| 1 | Receive month-end notification | Dashboard alert | 😊 Prepared | 1 min |
| 2 | Review pending journal entries | GL > Pending Entries list | 😐 Focused | 15 min |
| 3 | Check unposted vouchers | Voucher Management > Unposted | 😐 Focused | 10 min |
| 4 | Review bank reconciliation status | Bank > Reconciliation Dashboard | 😊 Satisfied (85% auto-matched) | 20 min |
| 5 | Manually reconcile unmatched items | Bank > Match Transactions | 😤 Frustrated (edge cases) | 45 min |
| 6 | Review AR aging report | AR > Aging Report | 😐 Focused | 15 min |
| 7 | Follow up on overdue receivables | AR > Overdue List > Send Reminder | 😤 Concerned | 30 min |
| 8 | Review AP aging report | AP > Aging Report | 😐 Focused | 15 min |
| 9 | Verify inventory valuation | Inventory > Valuation Report | 😊 Satisfied | 20 min |
| 10 | Check fixed asset depreciation | FA > Depreciation Schedule | 😊 Satisfied (auto-calculated) | 10 min |
| 11 | Review tax reconciliation | Tax > Tax Reconciliation | 😐 Focused | 30 min |
| 12 | Generate trial balance | Reports > Trial Balance | 😊 Satisfied (balanced) | 5 min |
| 13 | Review and approve adjustment entries | GL > Adjustment Entries > Approve | 😐 Focused | 30 min |
| 14 | Generate financial statements | Reports > Financial Statements | 😊 Satisfied | 10 min |
| 15 | Close accounting period | Settings > Period Management > Close | 😊 Relieved | 5 min |

**Total Time:** ~4 hours (vs. 2-3 days previously)

### 2.4 Pain Points & Opportunities

| Pain Point | Impact | Opportunity |
|-----------|--------|-------------|
| Manual bank reconciliation for edge cases | 45 min | AI-powered matching with learning |
| Overdue receivables follow-up | 30 min | Automated reminder workflow |
| Tax reconciliation complexity | 30 min | Automated tax reconciliation engine |

---

## 3. JOURNEY MAP: TAX ACCOUNTANT - VAT DECLARATION

### 3.1 Journey Overview

**Persona:** Minh, Tax Accountant (28 years, 4 years experience)
**Trigger:** VAT filing deadline approaching (Monthly: 20th of following month; Quarterly: last day of first month of next quarter)
**Goal:** Accurately file VAT declaration (Form 01/GTGT or 04/GTGT)
**Success Criteria:** Zero errors, on-time submission, matching with e-invoice data

### 3.2 Journey Phases

```
Phase 1: Data Collection        Phase 2: Calculation & Review    Phase 3: Submission
┌─────────────────────┐      ┌─────────────────────┐      ┌─────────────────────┐
│ - Gather input VAT   │      │ - Run VAT calculation│      │ - Generate form    │
│ - Gather output VAT  │      │ - Review calculations│      │ - Validate data    │
│ - Verify e-invoices  │      │ - Cross-check with   │      │ - Submit to tax    │
│ - Import HTKK data   │      │   e-invoice portal   │      │ - Confirm receipt  │
│                      │      │ - Prepare supplement │      │ - Archive records  │
└─────────────────────┘      └─────────────────────┘      └─────────────────────┘
     Day -10 to -5                  Day -5 to -2                  Day -2 to 0
```

### 3.3 Detailed Journey Steps

| Step | Action | System Interaction | Emotion | Time |
|------|--------|-------------------|---------|------|
| 1 | Receive VAT deadline notification | Dashboard alert + Calendar | 😊 Prepared | 1 min |
| 2 | Review input VAT (TK 1331, 1332) | Tax > Input VAT Report | 😐 Focused | 20 min |
| 3 | Verify input VAT against e-invoices | Tax > E-Invoice Verification | 😊 Confident | 15 min |
| 4 | Review output VAT by tax rate | Tax > Output VAT Report (10%, 8%, 5%, 0%, NonTaxable) | 😐 Focused | 20 min |
| 5 | Check for non-deductible VAT | Tax > Non-Deductible VAT | 😐 Focused | 10 min |
| 6 | Run VAT calculation | Tax > Calculate VAT | 😊 Satisfied (auto-calculated) | 2 min |
| 7 | Review VAT declaration form 01/GTGT | Tax > Declaration Form 01/GTGT | 😐 Focused | 15 min |
| 8 | Cross-check with tax authority portal | External > Tax Portal > Compare | 😊 Confident (matches) | 10 min |
| 9 | Prepare supplementary schedules | Tax > Supplementary Schedules | 😐 Focused | 15 min |
| 10 | Generate final declaration | Tax > Generate Declaration | 😊 Satisfied | 5 min |
| 11 | Submit to tax authority | Tax > Submit to GDT | 😊 Confident | 5 min |
| 12 | Receive submission confirmation | System notification | 😊 Relieved | 1 min |
| 13 | Archive declaration records | Tax > Archive Declaration | 😊 Organized | 5 min |

**Total Time:** ~2 hours (vs. 4-6 hours previously)

### 3.4 Pain Points & Opportunities

| Pain Point | Impact | Opportunity |
|-----------|--------|-------------|
| Cross-checking with tax authority portal | 10 min | Direct API integration |
| Non-deductible VAT identification | 10 min | Automated rule-based classification |
| Supplementary schedule preparation | 15 min | Auto-generation from transaction data |

---

## 4. JOURNEY MAP: AR ACCOUNTANT - INVOICE TO CASH

### 4.1 Journey Overview

**Persona:** AR Accountant
**Trigger:** Goods/services delivered, payment due
**Goal:** Issue invoice, collect payment, reconcile
**Success Criteria:** Invoice issued correctly, payment received on time, accounts reconciled

### 4.2 Journey Phases

```
Phase 1: Invoice Creation       Phase 2: Invoice Delivery        Phase 3: Payment Collection
┌─────────────────────┐      ┌─────────────────────┐      ┌─────────────────────┐
│ - Create sales order │      │ - Generate e-invoice │      │ - Monitor due dates  │
│ - Verify pricing     │      │ - Send to customer   │      │ - Send reminders     │
│ - Apply discounts    │      │ - Track delivery     │      │ - Receive payment    │
│ - Generate e-invoice │      │ - Confirm receipt    │      │ - Match to invoice   │
│                      │      │                      │      │ - Reconcile account  │
└─────────────────────┘      └─────────────────────┘      └─────────────────────┘
     Day 0                        Day 0-1                       Day 1-30+
```

### 4.3 Detailed Journey Steps

| Step | Action | System Interaction | Emotion | Time |
|------|--------|-------------------|---------|------|
| 1 | Create sales invoice | AR > New Invoice | 😐 Focused | 5 min |
| 2 | Select customer & verify details | AR > Customer Lookup | 😊 Quick | 1 min |
| 3 | Add line items, verify pricing | AR > Line Items | 😐 Focused | 3 min |
| 4 | Apply commercial discount (if any) | AR > Discount > Chiet Khau | 😐 Focused | 2 min |
| 5 | Select VAT rate (10%, 8%, 0%) | AR > Tax Rate Selection | 😊 Auto-suggested | 1 min |
| 6 | Generate e-invoice | AR > Generate E-Invoice | 😊 Satisfied | 1 min |
| 7 | Send invoice to customer | AR > Send (Email/Portal) | 😊 Efficient | 1 min |
| 8 | Track invoice status | AR > Invoice Dashboard | 😊 Informed | 2 min |
| 9 | Monitor payment due dates | AR > Aging Report | 😐 Monitoring | 10 min/day |
| 10 | Send payment reminder (if overdue) | AR > Overdue > Send Reminder | 😤 Uncomfortable | 5 min |
| 11 | Receive payment notification | System notification | 😊 Happy | 1 min |
| 12 | Match payment to invoice | AR > Payment Matching | 😊 Auto-matched | 2 min |
| 13 | Reconcile customer account | AR > Account Reconciliation | 😊 Balanced | 5 min |

**Total Time per Invoice:** ~15 min creation, ~5 min collection

### 4.4 Pain Points & Opportunities

| Pain Point | Impact | Opportunity |
|-----------|--------|-------------|
| Manual payment reminders | 5 min per customer | Automated escalation workflow |
| Complex discount calculations | 2 min | Pre-configured discount rules |
| Partial payment handling | 5 min | Automated partial payment allocation |

---

## 5. JOURNEY MAP: AP ACCOUNTANT - PROCURE TO PAY

### 5.1 Journey Overview

**Persona:** AP Accountant
**Trigger:** Supplier invoice received
**Goal:** Verify, approve, and pay supplier invoices
**Success Criteria:** Invoice verified, approved, paid on time, account reconciled

### 5.2 Journey Phases

```
Phase 1: Invoice Receipt        Phase 2: Verification & Approval   Phase 3: Payment
┌─────────────────────┐      ┌─────────────────────┐      ┌─────────────────────┐
│ - Receive invoice    │      │ - 3-way match        │      │ - Schedule payment  │
│ - Scan/upload        │      │ - Verify VAT         │      │ - Execute payment   │
│ - Data entry         │      │ - Check approval     │      │ - Record payment    │
│ - Match to PO        │      │ - Resolve disputes   │      │ - Reconcile account │
│                      │      │ - Approve for payment│      │                     │
└─────────────────────┘      └─────────────────────┘      └─────────────────────┘
     Day 0                        Day 0-3                       Day 3-30
```

### 5.3 Detailed Journey Steps

| Step | Action | System Interaction | Emotion | Time |
|------|--------|-------------------|---------|------|
| 1 | Receive supplier invoice | Email/Portal upload | 😐 Routine | 1 min |
| 2 | Scan and upload invoice | AP > Upload Invoice > OCR | 😊 OCR auto-extracts | 2 min |
| 3 | Verify invoice details | AP > Invoice Review | 😐 Focused | 3 min |
| 4 | 3-way match (PO-Receipt-Invoice) | AP > 3-Way Match | 😊 Auto-matched | 2 min |
| 5 | Verify input VAT (TK 1331) | AP > VAT Verification | 😐 Focused | 2 min |
| 6 | Check approval workflow | AP > Approval Status | 😐 Waiting | 1 min |
| 7 | Resolve discrepancies (if any) | AP > Dispute Resolution | 😤 Frustrated | 15 min |
| 8 | Approve for payment | AP > Approve Payment | 😊 Satisfied | 1 min |
| 9 | Schedule payment | AP > Payment Schedule | 😐 Planning | 3 min |
| 10 | Execute payment (bank transfer) | AP > Execute Payment | 😊 Efficient | 2 min |
| 11 | Record payment in GL | Auto-posted | 😊 Automated | 0 min |
| 12 | Reconcile supplier account | AP > Account Reconciliation | 😊 Balanced | 5 min |

**Total Time per Invoice:** ~20 min (with OCR), ~35 min (without OCR)

---

## 6. JOURNEY MAP: PAYROLL ACCOUNTANT - MONTHLY PAYROLL

### 6.1 Journey Overview

**Persona:** Lan, Payroll Accountant (32 years, 6 years experience)
**Trigger:** Monthly payroll cycle (25th of each month)
**Goal:** Calculate and process payroll for all employees
**Success Criteria:** Accurate salary, correct insurance deductions, PIT withholding, on-time payment

### 6.2 Journey Phases

```
Phase 1: Data Collection        Phase 2: Calculation             Phase 3: Processing
┌─────────────────────┐      ┌─────────────────────┐      ┌─────────────────────┐
│ - Import attendance  │      │ - Calculate gross    │      │ - Generate payslips  │
│ - Update allowances  │      │ - Calculate insurance│      │ - Process bank transfer│
│ - Update dependents  │      │ - Calculate PIT      │      │ - Submit insurance   │
│ - Review changes     │      │ - Calculate net      │      │ - File PIT           │
│                      │      │ - Review results     │      │ - Archive records    │
└─────────────────────┘      └─────────────────────┘      └─────────────────────┘
     Day -10 to -5                  Day -5 to -2                  Day -2 to 0
```

### 6.3 Detailed Journey Steps

| Step | Action | System Interaction | Emotion | Time |
|------|--------|-------------------|---------|------|
| 1 | Import attendance data | Payroll > Import Attendance | 😊 Automated import | 10 min |
| 2 | Review employee changes | Payroll > Employee Changes | 😐 Focused | 15 min |
| 3 | Update new allowances | Payroll > Allowances | 😐 Focused | 10 min |
| 4 | Verify dependent information | Payroll > Dependents | 😐 Focused | 10 min |
| 5 | Run payroll calculation | Payroll > Calculate Payroll | 😊 Satisfied (auto) | 5 min |
| 6 | Review gross salary | Payroll > Gross Salary Report | 😐 Focused | 15 min |
| 7 | Verify insurance deductions | Payroll > Insurance Report | 😐 Focused | 10 min |
| 8 | Verify PIT withholding | Payroll > PIT Report | 😐 Focused | 10 min |
| 9 | Review net salary | Payroll > Net Salary Report | 😊 Satisfied | 10 min |
| 10 | Generate payslips | Payroll > Generate Payslips | 😊 Satisfied | 5 min |
| 11 | Distribute payslips | Payroll > Send Payslips (Email/Portal) | 😊 Efficient | 5 min |
| 12 | Process bank transfer | Payroll > Bank Transfer File | 😊 Automated | 5 min |
| 13 | Generate insurance declaration | Payroll > Insurance Declaration | 😊 Auto-generated | 5 min |
| 14 | Submit PIT declaration | Tax > PIT Declaration > Submit | 😊 Efficient | 10 min |

**Total Time:** ~2 hours for 200 employees (vs. 1-2 days previously)

### 6.4 Pain Points & Opportunities

| Pain Point | Impact | Opportunity |
|-----------|--------|-------------|
| Attendance data import errors | 10 min | Direct integration with time tracking |
| Dependent information updates | 10 min | Self-service portal for employees |
| Insurance rate changes | Manual update | Auto-update from regulatory feed |

---

## 7. JOURNEY MAP: CASHIER - DAILY CASH OPERATIONS

### 7.1 Journey Overview

**Persona:** Cashier (Thu Quy)
**Trigger:** Daily business operations
**Goal:** Process all cash receipts and payments accurately
**Success Criteria:** All transactions recorded, cash balanced, bank reconciled

### 7.2 Journey Phases

```
Phase 1: Morning Setup          Phase 2: Transaction Processing    Phase 3: End of Day
┌─────────────────────┐      ┌─────────────────────┐      ┌─────────────────────┐
│ - Check opening cash │      │ - Process receipts   │      │ - Count physical cash│
│ - Review pending     │      │ - Process payments   │      │ - Compare to system  │
│ - Prepare vouchers   │      │ - Issue receipts     │      │ - Generate report    │
│                      │      │ - Update balances    │      │ - Handover (if shift)│
└─────────────────────┘      └─────────────────────┘      └─────────────────────┘
     8:00 AM                        8:00 AM - 5:00 PM              5:00 PM - 5:30 PM
```

### 7.3 Detailed Journey Steps

| Step | Action | System Interaction | Emotion | Time |
|------|--------|-------------------|---------|------|
| 1 | Check opening cash balance | Cash > Opening Balance | 😊 Prepared | 2 min |
| 2 | Review pending payment requests | Cash > Pending Payments | 😐 Focused | 5 min |
| 3 | Process cash receipt | Cash > New Receipt (01-TT) | 😊 Quick | 3 min |
| 4 | Process cash payment | Cash > New Payment (02-TT) | 😐 Focused | 5 min |
| 5 | Print receipt voucher | Cash > Print Voucher | 😊 Automated | 1 min |
| 6 | Process bank transfer | Cash > Bank Transfer | 😊 Efficient | 3 min |
| 7 | Record cash-in-transit | Cash > Cash in Transit (113) | 😐 Focused | 2 min |
| 8 | End-of-day cash count | Cash > Cash Count | 😐 Focused | 10 min |
| 9 | Compare physical vs. system | Cash > Reconciliation | 😊 Balanced | 5 min |
| 10 | Generate daily cash report | Cash > Daily Report | 😊 Satisfied | 3 min |

---

## 8. JOURNEY MAP: FIXED ASSET ACCOUNTANT - ASSET LIFECYCLE

### 8.1 Journey Overview

**Persona:** Fixed Asset Accountant
**Trigger:** New asset acquisition or asset lifecycle event
**Goal:** Manage asset registration, depreciation, and disposal
**Success Criteria:** All assets tracked, depreciation calculated correctly, proper documentation

### 8.2 Journey Phases

```
Phase 1: Asset Acquisition      Phase 2: Asset Management          Phase 3: Asset Disposal
┌─────────────────────┐      ┌─────────────────────┐      ┌─────────────────────┐
│ - Receive asset docs │      │ - Monthly depreciation│     │ - Initiate disposal  │
│ - Create asset record│      │ - Asset transfers    │      │ - Calculate gain/loss│
│ - Assign location    │      │ - Revaluation        │      │ - Generate documents │
│ - Set depreciation   │      │ - Physical inventory │      │ - Update records     │
│                      │      │ - Impairment testing │      │ - Archive records    │
└─────────────────────┘      └─────────────────────┘      └─────────────────────┘
     Day 0                        Monthly/Quarterly               As needed
```

### 8.3 Detailed Journey Steps

| Step | Action | System Interaction | Emotion | Time |
|------|--------|-------------------|---------|------|
| 1 | Receive asset purchase docs | FA > New Asset | 😐 Focused | 5 min |
| 2 | Create asset record (01-TSCD) | FA > Register Asset | 😊 Guided form | 5 min |
| 3 | Set depreciation method & period | FA > Depreciation Settings | 😐 Focused | 3 min |
| 4 | Assign cost center/location | FA > Assignment | 😊 Quick | 2 min |
| 5 | Monthly depreciation run | FA > Run Depreciation | 😊 Automated | 2 min |
| 6 | Review depreciation schedule | FA > Depreciation Report | 😊 Satisfied | 5 min |
| 7 | Process asset transfer | FA > Transfer Asset | 😐 Focused | 5 min |
| 8 | Annual physical inventory | FA > Inventory Count (05-TSCD) | 😤 Time-consuming | 2 hours |
| 9 | Process asset disposal | FA > Dispose Asset | 😐 Focused | 10 min |
| 10 | Generate liquidation document | FA > Liquidation Document | 😊 Auto-generated | 3 min |

---

## 9. JOURNEY MAP: CFO - FINANCIAL DASHBOARD & REPORTING

### 9.1 Journey Overview

**Persona:** CFO / Finance Director
**Trigger:** Need for financial visibility (daily/weekly/monthly)
**Goal:** Monitor financial health, make informed decisions
**Success Criteria:** Real-time access to key metrics, actionable insights

### 9.2 Journey Phases

```
Phase 1: Dashboard Review       Phase 2: Deep Dive Analysis        Phase 3: Decision & Action
┌─────────────────────┐      ┌─────────────────────┐      ┌─────────────────────┐
│ - Login & view       │      │ - Drill into details │      │ - Make decisions     │
│   dashboard          │      │ - Compare periods    │      │ - Approve actions    │
│ - Review KPIs        │      │ - Analyze variances  │      │ - Communicate to     │
│ - Check alerts       │      │ - Review trends      │      │   stakeholders       │
│                      │      │ - Generate reports   │      │ - Monitor execution  │
└─────────────────────┘      └─────────────────────┘      └─────────────────────┘
     Daily (5 min)                  Weekly (30 min)               As needed
```

### 9.3 Detailed Journey Steps

| Step | Action | System Interaction | Emotion | Time |
|------|--------|-------------------|---------|------|
| 1 | Login and view dashboard | Dashboard > Overview | 😊 Informed | 1 min |
| 2 | Review cash position | Dashboard > Cash Widget | 😊 Aware | 1 min |
| 3 | Check AR/AP status | Dashboard > AR/AP Widget | 😐 Monitoring | 2 min |
| 4 | Review revenue vs. budget | Dashboard > Revenue Widget | 😊/😐 Varies | 2 min |
| 5 | Check tax obligations | Dashboard > Tax Widget | 😐 Aware | 1 min |
| 6 | Drill into variance | Dashboard > Click > Detail Report | 😊 Insightful | 5 min |
| 7 | Generate financial statement | Reports > Financial Statements | 😊 Satisfied | 3 min |
| 8 | Export report for board | Reports > Export PDF/Excel | 😊 Efficient | 1 min |
| 9 | Approve pending items | Dashboard > Approvals | 😊 In control | 3 min |

**Total Time:** 5-15 minutes daily

### 9.4 Expanded CFO Deep-Dive Journey

| Step | Action | System Interaction | Emotion | Time |
|------|--------|-------------------|---------|------|
| 1 | Review P&L vs Budget | Reports > Budget vs Actual | 😐/😊 Varies | 5 min |
| 2 | Analyze revenue variance by product line | Reports > Revenue Analysis > Drill Down | 😊 Insightful | 5 min |
| 3 | Review cash flow forecast | Dashboard > Cash Flow Forecast | 😐 Monitoring | 3 min |
| 4 | Check tax liability summary | Tax > Tax Liability Dashboard | 😐 Aware | 2 min |
| 5 | Review working capital metrics | Dashboard > Working Capital Widget | 😐 Monitoring | 2 min |
| 6 | Approve large payment requests | Dashboard > Approvals > Payment | 😊 In Control | 3 min |
| 7 | Review bad debt exposure | AR > Bad Debt Exposure Report | 😤 Concerned | 5 min |
| 8 | Export board report package | Reports > Export Board Package | 😊 Efficient | 3 min |

---

## 9B. JOURNEY MAP: SYSTEM ADMINISTRATOR - SYSTEM CONFIGURATION

### 9B.1 Journey Overview

**Persona:** IT Administrator (Nam, 30 years, 5 years experience)
**Trigger:** New system setup, periodic maintenance, user management
**Goal:** Maintain system stability, security, and configuration accuracy
**Success Criteria:** All users properly provisioned, backups successful, system uptime 99.9%

### 9B.2 Detailed Journey Steps

| Step | Action | System Interaction | Emotion | Time |
|------|--------|-------------------|---------|------|
| 1 | Review system health dashboard | Admin > System Health | 😊 All Green | 5 min |
| 2 | Check backup status | Admin > Backup Status | 😊 Verified | 3 min |
| 3 | Process new user requests | Admin > User Management > Create | 😐 Focused | 10 min |
| 4 | Review access logs for anomalies | Admin > Access Log > Review | 😐 Monitoring | 10 min |
| 5 | Update exchange rates (daily) | Admin > Exchange Rates > Update | 😊 Auto-imported | 2 min |
| 6 | Manage accounting periods | Admin > Period Management | 😐 Focused | 5 min |
| 7 | Review system error logs | Admin > Error Log > Review | 😤 If errors | 10 min |
| 8 | Apply system updates/patches | Admin > System Update | 😐 Cautious | 30 min |
| 9 | Run database integrity check | Admin > Database Check | 😊 Satisfied | 15 min |
| 10 | Generate audit access report | Admin > Audit Report > Export | 😊 Organized | 5 min |

---

## 10. JOURNEY MAP: NEW ENTERPRISE ONBOARDING (CIRCULAR 200/133 MIGRATION)

### 10.1 Journey Overview

**Persona:** Chief Accountant + IT Administrator
**Trigger:** Enterprise decides to migrate from Circular 200/2014 or Circular 133/2016 to Circular 99/2025
**Goal:** Complete migration with zero data loss and minimal disruption
**Success Criteria:** All balances transferred correctly, system operational, users trained

### 10.2 Journey Phases

```
Phase 1: Assessment & Planning  Phase 2: Data Migration           Phase 3: Validation & Go-Live
┌─────────────────────┐      ┌─────────────────────┐      ┌─────────────────────┐
│ - Assess current     │      │ - Export Circular 200│      │ - Validate balances  │
│   system & data      │      │ - Map accounts       │      │ - Parallel run       │
│ - Plan migration     │      │ - Transform data     │      │ - User training      │
│ - Define timeline    │      │ - Import to new      │      │ - Go-live decision   │
│                      │      │ - Verify integrity   │      │ - Cut over           │
└─────────────────────┘      └─────────────────────┘      └─────────────────────┘
     Week 1-2                     Week 3-4                    Week 5-6
```

### 10.3 Detailed Journey Steps

| Step | Action | System Interaction | Emotion | Time |
|------|--------|-------------------|---------|------|
| 1 | Register new enterprise account | Setup > Create Account | 😊 Excited | 10 min |
| 2 | Configure company information | Setup > Company Profile | 😐 Focused | 15 min |
| 3 | Select accounting regime (Circular 99) or continue Circular 133 | Setup > Accounting Regime | 😊 Guided | 5 min |
| 4 | Import chart of accounts (TT200→TT99 mapping or TT133→TT99 mapping) | Setup > Import COA | 😊 Auto-loaded | 5 min |
| 5 | Map legacy accounts to Circular 99 | Migration > Account Mapping | 😤 Complex | 2 hours |
| 6 | Export data from legacy system | Migration > Export | 😐 Technical | 30 min |
| 7 | Import opening balances | Migration > Import Balances | 😐 Focused | 30 min |
| 8 | Verify balance transfer | Migration > Verification Report | 😊/😤 Depends | 1 hour |
| 9 | Run parallel comparison | Migration > Parallel Run | 😊 Confident | 1 day |
| 10 | Train users | Training > User Sessions | 😊 Empowered | 2 days |
| 11 | Go-live decision | Setup > Go-Live | 😊 Excited | 30 min |
| 12 | Cut over to new system | Setup > Activate | 😊 Relieved | 15 min |

**Total Time:** 4-6 weeks for complete migration

---

## 11. JOURNEY MAP: AUDITOR - COMPLIANCE REVIEW

### 11.1 Journey Overview

**Persona:** External Auditor
**Trigger:** Annual audit engagement
**Goal:** Verify compliance with Circular 99/2025 and tax laws
**Success Criteria:** Complete audit trail, evidence of compliance, audit opinion

### 11.2 Journey Phases

```
Phase 1: Planning               Phase 2: Fieldwork                Phase 3: Reporting
┌─────────────────────┐      ┌─────────────────────┐      ┌─────────────────────┐
│ - Understand system  │      │ - Test transactions  │      │ - Document findings  │
│ - Request access     │      │ - Verify compliance  │      │ - Draft audit report │
│ - Define scope       │      │ - Review controls    │      │ - Management letter  │
│ - Risk assessment    │      │ - Sample testing     │      │ - Final opinion      │
└─────────────────────┘      └─────────────────────┘      └─────────────────────┘
     Week 1                     Week 2-4                    Week 5
```

### 11.3 Detailed Journey Steps

| Step | Action | System Interaction | Emotion | Time |
|------|--------|-------------------|---------|------|
| 1 | Request auditor access | Admin > Create Auditor Account | 😊 Read-only | 5 min |
| 2 | Review chart of accounts | GL > Chart of Accounts | 😐 Verifying | 30 min |
| 3 | Test journal entry controls | GL > Audit Trail | 😊 Comprehensive | 1 hour |
| 4 | Verify voucher completeness | Vouchers > Sample Review | 😐 Testing | 2 hours |
| 5 | Review financial statements | Reports > B01, B02, B03, B09 | 😐 Analyzing | 2 hours |
| 6 | Verify tax calculations | Tax > Tax Reports | 😐 Testing | 2 hours |
| 7 | Verify e-invoices on GDT portal | External > tracuuhoadon.gdt.gov.vn > Cross-check | 😊 Confident | 30 min |
| 8 | Review audit trail | System > Audit Log | 😊 Complete trail | 1 hour |
| 9 | Export evidence | System > Export Evidence | 😊 Efficient | 30 min |

---

## 12. PAIN POINTS & OPPORTUNITIES

### 12.1 Consolidated Pain Points

| Pain Point | Affected Personas | Frequency | Severity | Opportunity |
|-----------|------------------|-----------|----------|-------------|
| Manual bank reconciliation | Cashier, Chief Accountant | Daily | Medium | AI-powered matching |
| Tax law change tracking | Tax Accountant | Monthly | High | Auto-update engine |
| Complex discount calculations | AR Accountant | Weekly | Medium | Pre-configured rules |
| Attendance data import | Payroll Accountant | Monthly | Medium | Direct integration |
| Physical asset inventory | FA Accountant | Annual | Low | Barcode/RFID scanning |
| Circular 200 migration | Chief Accountant, IT | One-time | High | Automated migration tool |
| Cross-system reconciliation | All accountants | Monthly | High | Unified data model |

### 12.2 Opportunity Prioritization

| Opportunity | Impact | Effort | Priority |
|------------|--------|--------|----------|
| AI-powered bank reconciliation | High | Medium | P0 |
| Automated tax rule updates | High | High | P0 |
| Automated migration from Circular 200 | High | High | P0 |
| Self-service employee portal | Medium | Medium | P1 |
| Barcode/RFID asset tracking | Medium | High | P2 |
| Direct tax authority API integration | High | High | P1 |

---

## 13. JOURNEY METRICS

### 13.1 Key Journey Metrics

| Journey | Current Time | Target Time | Improvement | CSAT Target |
|---------|-------------|-------------|-------------|-------------|
| Monthly Close | 10 days | 3 days | 70% | 4.5/5 |
| VAT Declaration | 4-6 hours | 2 hours | 60% | 4.5/5 |
| Invoice Creation | 30 min | 5 min | 83% | 4.7/5 |
| Invoice Processing (AP) | 45 min | 15 min | 67% | 4.5/5 |
| Monthly Payroll (200 employees) | 1-2 days | 2 hours | 85% | 4.5/5 |
| Daily Cash Operations | 2 hours | 1 hour | 50% | 4.5/5 |
| Asset Registration | 30 min | 10 min | 67% | 4.5/5 |
| CFO Dashboard Review | 30 min | 5 min | 83% | 4.8/5 |
| Circular 200/133 Migration | 3 months | 4-6 weeks | 60% | 4.0/5 |
| Audit Preparation | 2 weeks | 3 days | 75% | 4.5/5 |

---

**END OF USER JOURNEY DOCUMENT**
