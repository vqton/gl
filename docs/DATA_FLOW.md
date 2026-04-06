# DATA FLOW DOCUMENT
# Vietnamese Enterprise Accounting Software
# Compliant with Circular 99/2025/TT-BTC

**Document Version:** 1.0
**Date:** April 2026
**Prepared by:** CFO Office

---

## TABLE OF CONTENTS

1. Data Flow Overview
2. Data Flow Diagrams (DFD) - Level 0
3. Data Flow Diagrams (DFD) - Level 1
4. Data Flow Diagrams (DFD) - Level 2
5. Data Store Definitions
6. Data Entity Definitions
7. Data Flow Specifications
8. External Entity Specifications
9. Process Specifications
10. Data Dictionary
11. Data Validation Rules
12. Data Security & Privacy
13. Data Retention & Archival
14. Data Integration Points

---

## 1. DATA FLOW OVERVIEW

### 1.1 Purpose

This document defines the movement, transformation, storage, and retrieval of data within the Vietnamese Enterprise Accounting Software. It maps how data flows between external entities, processes, and data stores, ensuring complete traceability from source to report.

### 1.2 Scope

The data flows cover all modules:
- General Ledger & Chart of Accounts
- Accounts Receivable & Payable
- Tax Management (VAT, CIT, PIT)
- Electronic Invoice Management
- Payroll & Insurance
- Fixed Assets
- Inventory
- Bank & Cash
- Financial Reporting
- System Administration

### 1.3 Notation

```
External Entity: [Rectangle]
Process: (Circle/Oval)
Data Store: =Database=
Data Flow: --> (arrow with label)
```

---

## 2. DATA FLOW DIAGRAMS - LEVEL 0 (Context Diagram)

### 2.1 System Context

```
                    ┌─────────────────────────────────────────────────┐
                    │        VIETNAMESE ACCOUNTING SOFTWARE           │
                    │         (Circular 99/2025 Compliant)            │
                    │                                                 │
  [Customer] ──────>│                                                 │
                    │  (1.0)                                          │
  [Supplier] ──────>│  ACCOUNTING                                     │<───── [Tax Authority]
                    │  PROCESSING                                     │─────> (Tax Declarations)
  [Employee] ──────>│  ENGINE                                         │
                    │                                                 │<───── [Bank]
  [Bank] ──────────>│                                                 │─────> (Payment Instructions)
                    │  (2.0)                                          │
  [Tax Authority] <-│  REPORTING                                      │<───── [Social Insurance]
                    │  & COMPLIANCE                                   │─────> (Insurance Reports)
  [Social Ins.] <───│                                                 │
                    │                                                 │<───── [Auditor]
  [Auditor] ───────>│                                                 │─────> (Audit Reports)
                    │                                                 │
  [Management] <───>│                                                 │
                    └─────────────────────────────────────────────────┘
```

### 2.2 Level 0 Data Flows

| Flow ID | From | To | Data | Frequency |
|---------|------|-----|------|-----------|
| DF-001 | Customer | System | Sales orders, payment remittances | Continuous |
| DF-002 | System | Customer | E-invoices, statements, receipts | Per transaction |
| DF-003 | Supplier | System | Invoices, credit notes | Continuous |
| DF-004 | System | Supplier | Payment advices, remittances | Per payment |
| DF-005 | Employee | System | Timesheets, expense claims, dependent info | Monthly |
| DF-006 | System | Employee | Payslips, tax certificates | Monthly/Annual |
| DF-007 | Bank | System | Bank statements, transaction confirmations | Daily |
| DF-008 | System | Bank | Payment instructions, transfer requests | Per payment |
| DF-009 | System | Tax Authority | VAT declarations, CIT, PIT, license fee | Monthly/Quarterly/Annual |
| DF-010 | Tax Authority | System | Tax codes, validation responses, notices | Per submission |
| DF-011 | System | Social Insurance | Insurance declarations, contribution reports | Monthly |
| DF-012 | Social Insurance | System | Insurance rates, contribution confirmations | Monthly/When changed |
| DF-013 | System | Auditor | Financial data, audit trails, evidence | Annual/As needed |
| DF-014 | Auditor | System | Audit requests, findings | Annual |
| DF-015 | Management | System | Approval decisions, configuration | As needed |
| DF-016 | System | Management | Dashboards, reports, alerts | Daily/Weekly/Monthly |

---

## 3. DATA FLOW DIAGRAMS - LEVEL 1

### 3.1 General Ledger Data Flow

```
                    ┌──────────────────────────────────────────────┐
                    │           GENERAL LEDGER MODULE              │
                    │                                              │
  [Chief Accountant]│                                              │
         ──────────>│  (1.1)          ┌─────────────────┐          │
  Chart of Accounts │  Manage         │                 │          │
                    │  Chart of       │  =Chart of      │          │
  [System Admin]    │  Accounts       │  Accounts=      │          │
         ──────────>│                 │  (DF-1.1-DS1)   │          │
  Account Config    │       │         └─────────────────┘          │
                    │       v                                       │
                    │  (1.2)          ┌─────────────────┐          │
  [Accountant]      │  Create         │                 │          │
         ──────────>│  Journal        │  =Journal       │          │
  Journal Entry     │  Entries        │  Entries=       │          │
                    │       │         │  (DF-1.1-DS2)   │          │
                    │       v         └─────────────────┘          │
                    │  (1.3)                                       │
                    │  Post &         ┌─────────────────┐          │
                    │  Update         │                 │          │
                    │  Balances ─────>│  =Account       │          │
                    │                 │  Balances=      │          │
                    │                 │  (DF-1.1-DS3)   │          │
                    │                 └─────────────────┘          │
                    │                       │                       │
                    │                       v                       │
                    │  (1.4)          ┌─────────────────┐          │
                    │  Generate       │                 │          │
                    │  Trial          │  =Trial Balance │          │
                    │  Balance ──────>│  (DF-1.1-DS4)   │          │
                    │                 └─────────────────┘          │
                    └──────────────────────────────────────────────┘
```

### 3.2 Accounts Receivable Data Flow

```
                    ┌──────────────────────────────────────────────┐
                    │         ACCOUNTS RECEIVABLE MODULE           │
                    │                                              │
  [AR Accountant]   │  (2.1)          ┌─────────────────┐          │
         ──────────>│  Create         │                 │          │
  Sales Data        │  Invoice ──────>│  =Sales Invoices│          │
                    │                 │  (DF-2.1-DS1)   │          │
                    │                 └────────┬────────┘          │
                    │                          │                   │
                    │                          v                   │
                    │  (2.2)          ┌─────────────────┐          │
                    │  Generate       │                 │          │
                    │  E-Invoice ────>│  =E-Invoice     │          │
                    │                 │  Register=      │          │
                    │                 │  (DF-2.1-DS2)   │          │
                    │                 └────────┬────────┘          │
                    │                          │                   │
                    │                          v                   │
                    │  (2.3)          ┌─────────────────┐          │
  [Customer]        │  Record         │                 │          │
  Payment ─────────>│  Payment ──────>│  =Payment       │          │
  Remittance        │                 │  Records=       │          │
                    │                 │  (DF-2.1-DS3)   │          │
                    │                 └────────┬────────┘          │
                    │                          │                   │
                    │                          v                   │
                    │  (2.4)          ┌─────────────────┐          │
                    │  Update         │                 │          │
                    │  AR Balance ───>│  =AR Customer   │          │
                    │                 │  Balances=      │          │
                    │                 │  (DF-2.1-DS4)   │          │
                    │                 └────────┬────────┘          │
                    │                          │                   │
                    │                          v                   │
                    │  (2.5)          ┌─────────────────┐          │
                    │  Generate       │                 │          │
                    │  Aging Report ─>│  =Aging Reports │          │
                    │                 │  (DF-2.1-DS5)   │          │
                    └──────────────────────────────────────────────┘
```

### 3.3 Tax Management Data Flow

```
                    ┌──────────────────────────────────────────────┐
                    │           TAX MANAGEMENT MODULE              │
                    │                                              │
  [GL Module]       │  (3.1)          ┌─────────────────┐          │
  VAT Transactions ──────────────────>│                 │          │
                    │  Collect VAT    │  =VAT           │          │
  [AR Module]       │  Data           │  Transactions=  │          │
  Output VAT ──────>│                 │  (DF-3.1-DS1)   │          │
                    │                 └────────┬────────┘          │
  [AP Module]       │                          │                   │
  Input VAT ───────>│                          v                   │
                    │  (3.2)          ┌─────────────────┐          │
                    │  Calculate      │                 │          │
                    │  VAT Payable    │  =VAT           │          │
                    │                 │  Calculations=  │          │
                    │                 │  (DF-3.1-DS2)   │          │
                    │                 └────────┬────────┘          │
                    │                          │                   │
                    │                          v                   │
                    │  (3.3)          ┌─────────────────┐          │
                    │  Generate       │                 │          │
                    │  Declaration    │  =Tax           │          │
                    │  Form           │  Declarations=  │          │
                    │                 │  (DF-3.1-DS3)   │          │
                    │                 └────────┬────────┘          │
                    │                          │                   │
                    │                          v                   │
                    │                          │                   │
                    └──────────────────────────┼───────────────────┘
                                               │
                                               v
                                        [Tax Authority]
                                        (GDT Portal)
```

### 3.4 Payroll Data Flow

```
                    ┌──────────────────────────────────────────────┐
                    │            PAYROLL MODULE                    │
                    │                                              │
  [Time Tracking]   │  (4.1)          ┌─────────────────┐          │
  Attendance ──────>│  Import         │                 │          │
                    │  Attendance     │  =Attendance    │          │
                    │                 │  Data=          │          │
                    │                 │  (DF-4.1-DS1)   │          │
                    │                 └────────┬────────┘          │
                    │                          │                   │
                    │                          v                   │
                    │  (4.2)          ┌─────────────────┐          │
  [HR Data]         │  Calculate      │                 │          │
  Employee Info ───>│  Payroll        │  =Payroll       │          │
                    │                 │  Calculations=  │          │
  [Tax Module]      │                 │  (DF-4.1-DS2)   │          │
  Tax Tables ──────>│                 └────────┬────────┘          │
                    │                          │                   │
  [Insurance]       │                          v                   │
  Rates ───────────>│  (4.3)          ┌─────────────────┐          │
                    │  Generate       │                 │          │
                    │  Payslips ─────>│  =Payslips=     │          │
                    │                 │  (DF-4.1-DS3)   │          │
                    │                 └────────┬────────┘          │
                    │                          │                   │
                    │                          v                   │
                    │  (4.4)          ┌─────────────────┐          │
                    │  Post to GL     │  =GL Journal    │          │
                    │                 │  Entries=       │          │
                    │                 │  (DF-4.1-DS4)   │          │
                    └──────────────────────────────────────────────┘
```

---

## 4. DATA FLOW DIAGRAMS - LEVEL 2

### 4.1 E-Invoice Data Flow (Detailed)

```
                    ┌──────────────────────────────────────────────┐
                    │        E-INVOICE DATA FLOW (DETAILED)        │
                    │                                              │
  [Sales Invoice]   │  (5.1)          ┌─────────────────┐          │
  Data ────────────>│  Validate       │                 │          │
                    │  Invoice Data   │  =Validation    │          │
                    │                 │  Results=       │          │
                    │                 │  (DF-5.1-DS1)   │          │
                    │                 └────────┬────────┘          │
                    │                          │                   │
                    │                     <Valid?>                  │
                    │                    /        \                 │
                    │                  Yes        No                │
                    │                  /            \               │
                    │                 v              v              │
                    │  (5.2)                    (5.3)               │
                    │  Request CQT              Log Error           │
                    │  Code                       │                 │
                    │     │                       v                 │
                    │     v              ┌─────────────────┐       │
                    │     │              │  =Error Log=    │       │
                    │     v              │  (DF-5.1-DS2)   │       │
                    │  ┌─────────────────┐                  │       │
                    │  │                 │<─────────────────┘       │
                    │  =E-Invoice       │                          │
                    │  Registry=        │                          │
                    │  (DF-5.1-DS3)     │                          │
                    │  └────────┬───────┘                          │
                    │           │                                   │
                    │           v                                   │
                    │  (5.4)                                        │
                    │  Apply Digital                                │
                    │  Signature                                    │
                    │     │                                         │
                    │     v                                         │
                    │  (5.5)          ┌─────────────────┐          │
                    │  Send to ──────>│  =Sent Invoices │          │
                    │  Customer       │  (DF-5.1-DS4)   │          │
                    │                 └─────────────────┘          │
                    └──────────────────────────────────────────────┘
```

### 4.2 Financial Statement Data Flow (Detailed)

```
                    ┌──────────────────────────────────────────────┐
                    │    FINANCIAL STATEMENT DATA FLOW (DETAILED)  │
                    │                                              │
  =Account          │  (6.1)          ┌─────────────────┐          │
  Balances= ───────>│  Extract        │                 │          │
  (DF-1.1-DS3)      │  Account        │  =Extracted     │          │
                    │  Balances       │  Balances=      │          │
                    │                 │  (DF-6.1-DS1)   │          │
                    │                 └────────┬────────┘          │
                    │                          │                   │
                    │                          v                   │
                    │  (6.2)          ┌─────────────────┐          │
  =Chart of         │  Map to         │                 │          │
  Accounts= ───────>│  B01-DN         │  =B01-DN Data=  │          │
  (DF-1.1-DS1)      │  Line Items     │  (DF-6.1-DS2)   │          │
                    │                 └─────────────────┘          │
                    │                                              │
                    │  (6.3)          ┌─────────────────┐          │
  =Revenue/         │  Map to         │                 │          │
  Expense= ────────>│  B02-DN         │  =B02-DN Data=  │          │
  Accounts          │  Line Items     │  (DF-6.1-DS3)   │          │
                    │                 └─────────────────┘          │
                    │                                              │
                    │  (6.4)          ┌─────────────────┐          │
  =Cash/Bank        │  Map to         │                 │          │
  Transactions= ───>│  B03-DN         │  =B03-DN Data=  │          │
                    │  Line Items     │  (DF-6.1-DS4)   │          │
                    │                 └─────────────────┘          │
                    │                                              │
                    │  (6.5)          ┌─────────────────┐          │
  =All Modules=     │  Compile        │                 │          │
                    │  Notes          │  =B09-DN Data=  │          │
                    │                 │  (DF-6.1-DS5)   │          │
                    │                 └─────────────────┘          │
                    └──────────────────────────────────────────────┘
```

---

## 5. DATA STORE DEFINITIONS

### 5.1 Core Data Stores

| DS-ID | Data Store | Description | Retention | Volume Estimate |
|-------|-----------|-------------|-----------|----------------|
| DS-01 | Chart of Accounts | Circular 99 account structure (71 L1, 101 L2, custom L3/L4) | Permanent | ~500 records |
| DS-02 | Journal Entries | All accounting journal entries with debit/credit | 10+ years | 1M+/year |
| DS-03 | Account Balances | Current and historical account balances | 10+ years | ~500 accounts x periods |
| DS-04 | Trial Balance | Period-end trial balances | 10+ years | 12/year |
| DS-05 | Customer Master | Customer information, credit terms, tax codes | Permanent + 5 years | ~10,000 |
| DS-06 | Sales Invoices | All sales invoices with line items | 10+ years | 100K+/year |
| DS-07 | E-Invoice Register | E-invoice records with CQT codes, status | 10+ years | 100K+/year |
| DS-08 | Payment Records | Customer payment receipts and matching | 10+ years | 50K+/year |
| DS-09 | AR Customer Balances | Current customer balances and aging | Current | ~10,000 |
| DS-10 | Supplier Master | Supplier information, payment terms | Permanent + 5 years | ~5,000 |
| DS-11 | Purchase Invoices | All supplier invoices | 10+ years | 50K+/year |
| DS-12 | Payment Records (AP) | Supplier payments and matching | 10+ years | 30K+/year |
| DS-13 | AP Supplier Balances | Current supplier balances and aging | Current | ~5,000 |
| DS-14 | VAT Transactions | Input and output VAT transaction details | 10+ years | 200K+/year |
| DS-15 | VAT Calculations | Period-end VAT calculations | 10+ years | 12-48/year |
| DS-16 | Tax Declarations | Filed tax declarations and confirmations | 10+ years | 50+/year |
| DS-17 | Employee Master | Employee information, contracts, dependents | Permanent + 5 years | ~5,000 |
| DS-18 | Attendance Data | Employee attendance records | 5 years | 1.2M+/year |
| DS-19 | Payroll Calculations | Monthly payroll calculations per employee | 10+ years | 60K+/year |
| DS-20 | Payslips | Generated payslips | 10+ years | 60K+/year |
| DS-21 | Insurance Records | BHXH, BHYT, BHTN contribution records | 10+ years | 60K+/year |
| DS-22 | Fixed Asset Register | All fixed assets with details | Permanent | ~10,000 |
| DS-23 | Depreciation Schedule | Monthly depreciation per asset | 10+ years | 120K+/year |
| DS-24 | Biological Assets Register | Livestock, crops, biological assets | Permanent | ~5,000 |
| DS-25 | Inventory Master | Item master data, categories, units | Permanent | ~50,000 |
| DS-26 | Inventory Transactions | Stock movements (receipts, issues, transfers) | 10+ years | 500K+/year |
| DS-27 | Inventory Balances | Current stock quantities and values | Current | ~50,000 |
| DS-28 | Bank Accounts | Bank account information | Permanent | ~50 |
| DS-29 | Bank Transactions | Bank statement transactions | 10+ years | 200K+/year |
| DS-30 | Cash Transactions | Cash receipts and payments | 10+ years | 100K+/year |
| DS-31 | Financial Statements | Generated B01, B02, B03, B09 reports | 10+ years | 12+/year |
| DS-32 | Audit Log | All system actions and modifications | 10+ years | 5M+/year |
| DS-33 | User Accounts | User credentials, roles, permissions | Permanent | ~500 |
| DS-34 | Error Log | System errors and validation failures | 5 years | 100K+/year |
| DS-35 | Construction Progress | TK 337 progress payment records | 10+ years | ~5,000 |
| DS-36 | Price Stabilization Fund | TK 357 fund records | Permanent | ~100 |
| DS-37 | Government Bond Repo | TK 171 bond transaction records | 10+ years | ~10,000 |

---

## 6. DATA ENTITY DEFINITIONS

### 6.1 Key Data Entities

#### 6.1.1 Journal Entry Entity

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| entry_id | UUID | Yes | Unique identifier |
| entry_number | String(20) | Yes | Sequential number |
| entry_date | Date | Yes | Transaction date |
| accounting_period | String(7) | Yes | YYYY-MM format |
| description | Text | Yes | Entry description |
| entry_type | Enum | Yes | Daily/Adjustment/Closing/Reversing |
| created_by | UUID | Yes | Creator user ID |
| created_at | Timestamp | Yes | Creation timestamp |
| approved_by | UUID | No | Approver user ID |
| approved_at | Timestamp | No | Approval timestamp |
| status | Enum | Yes | Draft/Pending/Posted/Reversed |
| currency | String(3) | Yes | VND or foreign currency |
| exchange_rate | Decimal | No | Rate if foreign currency |
| total_debit | Decimal(18,2) | Yes | Total debit amount |
| total_credit | Decimal(18,2) | Yes | Total credit amount |

#### 6.1.2 Journal Entry Line Entity

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| line_id | UUID | Yes | Unique identifier |
| entry_id | UUID | Yes | Parent journal entry |
| line_number | Integer | Yes | Line sequence |
| account_code | String(10) | Yes | Circular 99 account code |
| debit_amount | Decimal(18,2) | No | Debit amount (mutually exclusive with credit) |
| credit_amount | Decimal(18,2) | No | Credit amount (mutually exclusive with debit) |
| description | Text | No | Line description |
| cost_center | String(20) | No | Cost center code |
| project | String(20) | No | Project code |
| customer_id | UUID | No | Related customer (for AR) |
| supplier_id | UUID | No | Related supplier (for AP) |
| invoice_ref | String(50) | No | Related invoice number |
| tax_rate | Decimal(5,2) | No | Applicable tax rate |
| tax_amount | Decimal(18,2) | No | Tax amount |

#### 6.1.3 E-Invoice Entity

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| invoice_id | UUID | Yes | Unique identifier |
| invoice_number | String(20) | Yes | Sequential number |
| invoice_symbol | String(10) | Yes | Per Decree 70/2025 |
| invoice_date | Date | Yes | Invoice date |
| invoice_time | Time | Yes | Invoice time |
| seller_tax_code | String(20) | Yes | Seller tax code |
| seller_name | String(255) | Yes | Seller name |
| seller_address | Text | Yes | Seller address |
| buyer_tax_code | String(20) | Yes | Buyer tax code |
| buyer_name | String(255) | Yes | Buyer name |
| buyer_address | Text | Yes | Buyer address |
| cqt_code | String(50) | No | Tax authority code (if applicable) |
| invoice_type | Enum | Yes | With CQT/Without CQT |
| invoice_status | Enum | Yes | Draft/Sent/Confirmed/Replaced/Cancelled |
| total_amount | Decimal(18,2) | Yes | Total before tax |
| total_vat | Decimal(18,2) | Yes | Total VAT |
| total_with_vat | Decimal(18,2) | Yes | Total including VAT |
| digital_signature | Text | Yes | Digital signature hash |
| sent_at | Timestamp | No | When sent to customer |
| confirmed_at | Timestamp | No | When confirmed by CQT |

#### 6.1.4 Tax Declaration Entity

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| declaration_id | UUID | Yes | Unique identifier |
| tax_type | Enum | Yes | VAT/CIT/PIT/License Fee |
| declaration_form | String(20) | Yes | Form code (01/GTGT, 03/TNDN, etc.) |
| period_type | Enum | Yes | Monthly/Quarterly/Annual |
| period_start | Date | Yes | Period start date |
| period_end | Date | Yes | Period end date |
| filing_date | Date | Yes | Actual filing date |
| deadline | Date | Yes | Filing deadline |
| status | Enum | Yes | Draft/Submitted/Accepted/Rejected |
| submission_ref | String(50) | No | Tax authority submission reference |
| total_tax_payable | Decimal(18,2) | Yes | Total tax amount |
| payment_status | Enum | Yes | Unpaid/Partial/Paid |
| payment_date | Date | No | Payment date |
| created_by | UUID | Yes | Creator user ID |
| created_at | Timestamp | Yes | Creation timestamp |

---

## 7. DATA FLOW SPECIFICATIONS

### 7.1 Detailed Data Flow Specifications

| Flow ID | Name | Source | Destination | Data Elements | Volume | Frequency |
|---------|------|--------|-------------|--------------|--------|-----------|
| DF-101 | Journal Entry Data | User Input | Journal Entry Process | entry_date, accounts, amounts, description | 500/day | Continuous |
| DF-102 | Posted Entry Data | Journal Entry Process | Account Balances | account_code, debit, credit, period | 500/day | Continuous |
| DF-103 | Balance Update | Account Balances | Trial Balance | account_code, debit_balance, credit_balance | 500/period | Period-end |
| DF-104 | Invoice Data | User Input | Invoice Process | customer, items, prices, tax rate | 200/day | Continuous |
| DF-105 | E-Invoice Data | Invoice Process | E-Invoice Registry | invoice_number, cqt_code, amounts, signature | 200/day | Continuous |
| DF-106 | E-Invoice to Customer | E-Invoice Registry | Customer | PDF/XML invoice, delivery confirmation | 200/day | Continuous |
| DF-107 | Payment Data | Customer | Payment Process | amount, date, reference, matched invoice | 100/day | Continuous |
| DF-108 | VAT Input Data | AP Module | VAT Process | supplier, invoice, input_vat, tax_code | 100/day | Continuous |
| DF-109 | VAT Output Data | AR Module | VAT Process | customer, invoice, output_vat, tax_rate | 200/day | Continuous |
| DF-110 | VAT Calculation | VAT Process | VAT Calculations | period, input_vat, output_vat, payable | 1/month | Monthly |
| DF-111 | VAT Declaration | VAT Calculations | Tax Authority | Form 01/GTGT data, supplementary schedules | 1/month | Monthly |
| DF-112 | Payroll Data | Attendance + HR | Payroll Process | employee, gross, deductions, net | 5,000/month | Monthly |
| DF-113 | Payslip Data | Payroll Process | Employee | payslip details, YTD totals | 5,000/month | Monthly |
| DF-114 | Bank Statement | Bank | Bank Process | date, reference, amount, description | 500/day | Daily |
| DF-115 | Reconciliation Data | Bank Process | Account Balances | matched transactions, differences | 500/day | Daily |
| DF-116 | GL Posting Data | All Modules | General Ledger | account, debit, credit, description, reference | 1,000/day | Continuous |
| DF-117 | Financial Statement Data | Account Balances | Reporting Process | mapped line items, comparative data | 12/year | Monthly/Annual |
| DF-118 | Audit Trail Data | All Processes | Audit Log | user, action, timestamp, old_value, new_value | 10,000/day | Continuous |

---

## 8. EXTERNAL ENTITY SPECIFICATIONS

### 8.1 External Entities

| Entity ID | Entity Name | Type | Description | Data Provided | Data Received |
|-----------|------------|------|-------------|--------------|---------------|
| EE-01 | Customer | External | Buyers of goods/services | Orders, payments, remittances | Invoices, statements, receipts |
| EE-02 | Supplier | External | Sellers of goods/services | Invoices, credit notes | Payments, remittances |
| EE-03 | Employee | External | Company employees | Timesheets, expense claims, dependent info | Payslips, tax certificates (02/TNCN) |
| EE-04 | Tax Authority (GDT) | External | General Department of Taxation | Tax codes, validation, notices | Tax declarations (VAT, CIT, PIT) |
| EE-05 | Bank | External | Commercial banks | Bank statements, confirmations | Payment instructions, transfers |
| EE-06 | Social Insurance | External | BHXH Vietnam | Insurance rates, confirmations | Insurance declarations, contributions |
| EE-07 | Auditor | External | Internal/External auditors | Audit requests, findings | Financial data, audit trails |
| EE-08 | Management | External | CFO, CEO, Board | Approvals, configurations | Dashboards, reports, alerts |
| EE-09 | E-Invoice Provider | External | VNPT, Viettel, MISA, etc. | Invoice codes, confirmations | Invoice data for code generation |
| EE-10 | Time Tracking System | External | Attendance/biometric systems | Attendance records | - |
| EE-11 | HTKK Software | External | Tax support software | - | Export files for HTKK import |

---

## 9. PROCESS SPECIFICATIONS

### 9.1 Core Processes

| Process ID | Process Name | Input | Output | Logic |
|-----------|-------------|-------|--------|-------|
| P-01 | Journal Entry Processing | Entry data | Posted entries | Double-entry validation, period check, approval workflow |
| P-02 | Balance Calculation | Posted entries | Account balances | Sum debits and credits by account and period |
| P-03 | Trial Balance Generation | Account balances | Trial balance | List all accounts with debit/credit balances, verify equality |
| P-04 | Invoice Creation | Sales data, customer info | Invoice record | Apply pricing, discounts, VAT, generate invoice number |
| P-05 | E-Invoice Generation | Invoice record | E-invoice with CQT code | Apply template, request CQT code, sign digitally |
| P-06 | Payment Matching | Payment data, open invoices | Matched payments | Auto-match by amount, date, reference; manual override |
| P-07 | VAT Calculation | Input VAT, output VAT transactions | VAT payable/refundable | Sum input VAT, sum output VAT, calculate difference |
| P-08 | Tax Declaration Generation | VAT/CIT/PIT calculations | Declaration form | Map calculations to official form fields |
| P-09 | Payroll Calculation | Attendance, salary data, tax tables | Net salary, deductions | Gross - Insurance - PIT = Net |
| P-10 | Depreciation Calculation | Asset register, depreciation methods | Monthly depreciation | Apply method (straight-line, declining balance) per asset |
| P-11 | Inventory Valuation | Stock movements, valuation method | Inventory value | Apply FIFO/weighted average to calculate cost |
| P-12 | Bank Reconciliation | Bank statement, system transactions | Reconciled items | Match by amount, date, reference; flag unmatched |
| P-13 | Financial Statement Generation | Account balances, chart of accounts mapping | B01, B02, B03, B09 | Map accounts to statement line items per Circular 99 |
| P-14 | Period Close | All module data | Closed period, audit trail | Verify reconciliation, run accruals, lock period |
| P-15 | Audit Trail Recording | All system actions | Audit log entries | Record user, action, timestamp, before/after values |

---

## 10. DATA DICTIONARY

### 10.1 Common Data Types

| Type | Format | Example | Description |
|------|--------|---------|-------------|
| VND_CURRENCY | Decimal(18,2) | 1,234,567,890.00 | Vietnamese Dong amounts |
| DATE_VN | DD/MM/YYYY | 01/01/2026 | Vietnamese date format |
| TAX_CODE | String(10-13) | 0100123456 | Vietnamese tax code |
| ACCOUNT_CODE | String(4-10) | 33311 | Circular 99 account code |
| INVOICE_NUMBER | String(20) | AA/25E/0000001 | E-invoice number per Decree 70 |
| PERIOD | String(7) | 2026-01 | Accounting period (YYYY-MM) |

### 10.2 Enumerations

| Enum Name | Values |
|-----------|--------|
| ENTRY_TYPE | Daily, Adjustment, Closing, Reversing, Opening |
| ENTRY_STATUS | Draft, Pending, Posted, Reversed |
| INVOICE_TYPE | WithCQT, WithoutCQT |
| INVOICE_STATUS | Draft, Sent, Confirmed, Replaced, Cancelled, Adjusted |
| VAT_RATE | 0, 5, 8, 10, NonTaxable |
| TAX_TYPE | VAT, CIT, PIT, LicenseFee, ForeignContractorTax |
| DECLARATION_STATUS | Draft, Submitted, Accepted, Rejected |
| PAYMENT_STATUS | Unpaid, Partial, Paid, Overdue |
| DEPRECIATION_METHOD | StraightLine, DecliningBalance, UnitsOfProduction |
| INVENTORY_VALUATION | FIFO, WeightedAverage, SpecificIdentification |
| PERIOD_STATUS | Open, Locked, Closed |

### 10.3 Circular 99 Account Code Structure

| Level | Format | Example | Description |
|-------|--------|---------|-------------|
| Level 1 | 3 digits | 333 | Taxes payable |
| Level 2 | 4 digits | 3331 | VAT payable |
| Level 3 | 5 digits | 33311 | Output VAT |
| Level 4 | 6 digits | 333111 | Output VAT - 10% |

---

## 11. DATA VALIDATION RULES

### 11.1 Journal Entry Validation

| Rule ID | Rule | Error Message |
|---------|------|--------------|
| VR-01 | Total debit must equal total credit | "Entry unbalanced: Debit {X} != Credit {Y}" |
| VR-02 | Accounting period must be open | "Period {period} is closed" |
| VR-03 | Account code must exist in chart of accounts | "Account {code} does not exist" |
| VR-04 | At least one debit and one credit line required | "Entry must have at least one debit and one credit line" |
| VR-05 | Amount must be positive | "Amount must be greater than zero" |
| VR-06 | Entry date must be within period | "Entry date {date} is outside period {period}" |
| VR-07 | Description required | "Entry description is required" |

### 11.2 Invoice Validation

| Rule ID | Rule | Error Message |
|---------|------|--------------|
| VR-08 | Buyer tax code must be valid (10-13 digits) | "Invalid tax code format" |
| VR-09 | Invoice number must be sequential | "Invoice number gap detected" |
| VR-10 | VAT rate must be valid (0%, 5%, 8%, 10%, Non-Taxable) | "Invalid VAT rate" |
| VR-11 | Total = Sum(line amounts) + VAT | "Total calculation mismatch" |
| VR-12 | Invoice date cannot be in future | "Invoice date cannot be in the future" |

### 11.3 Tax Declaration Validation

| Rule ID | Rule | Error Message |
|---------|------|--------------|
| VR-13 | Declaration must be filed before deadline | "Filing deadline has passed" |
| VR-14 | All required fields must be populated | "Required field {field} is empty" |
| VR-15 | VAT input must match verified invoices | "Input VAT mismatch with verified invoices" |
| VR-16 | CIT calculation must follow formula | "CIT calculation error: Revenue - Expenses x Rate" |

### 11.4 Payroll Validation

| Rule ID | Rule | Error Message |
|---------|------|--------------|
| VR-17 | Gross salary must be >= minimum wage | "Salary below minimum wage" |
| VR-18 | Insurance base capped at 20x base salary | "Insurance base exceeds cap" |
| VR-19 | Dependent deduction = 4.4M x number of dependents | "Dependent deduction mismatch" |
| VR-20 | Net = Gross - Insurance - PIT | "Net salary calculation error" |

---

## 12. DATA SECURITY & PRIVACY

### 12.1 Data Classification

| Classification | Data Types | Access Level | Encryption |
|---------------|-----------|--------------|------------|
| **Public** | Company name, address, tax code | All users | No |
| **Internal** | Chart of accounts, policies | Authenticated users | No |
| **Confidential** | Journal entries, invoices, reports | Role-based | At rest |
| **Restricted** | Employee salaries, bank accounts, passwords | Strict role-based | At rest + in transit |

### 12.2 Encryption Requirements

| Data Type | At Rest | In Transit | Algorithm |
|-----------|---------|------------|-----------|
| User passwords | Yes | Yes | bcrypt (at rest), TLS 1.3 (in transit) |
| Bank account numbers | Yes | Yes | AES-256 (at rest), TLS 1.3 (in transit) |
| Employee salary data | Yes | Yes | AES-256 (at rest), TLS 1.3 (in transit) |
| Tax codes | No | Yes | TLS 1.3 (in transit) |
| Journal entries | No | Yes | TLS 1.3 (in transit) |
| Digital signatures | Yes | Yes | SHA-256 + RSA-2048 |

### 12.3 Access Control Matrix

| Data Store | Chief Accountant | Tax Accountant | AR Accountant | AP Accountant | Payroll | Cashier | CFO | Auditor |
|-----------|-----------------|---------------|--------------|--------------|---------|---------|-----|---------|
| Chart of Accounts | RW | R | R | R | R | R | R | R |
| Journal Entries | RW | R | R (own) | R (own) | R (own) | R (own) | R | R |
| Customer Data | RW | R | RW | R | - | R | R | R |
| Supplier Data | RW | R | R | RW | - | R | R | R |
| Tax Data | RW | RW | R | R | R | - | R | R |
| Payroll Data | RW | R | - | - | RW | - | R | R |
| Bank Data | RW | - | R | R | - | RW | R | R |
| Financial Statements | RW | R | R | R | R | R | RW | R |
| Audit Log | R | R | R | R | R | R | R | RW |

**Legend:** RW = Read/Write, R = Read Only, - = No Access

---

## 13. DATA RETENTION & ARCHIVAL

### 13.1 Retention Schedule

| Data Type | Retention Period | Document Type | Legal Basis | Archival Method |
|-----------|-----------------|---------------|-------------|-----------------|
| Accounting ledgers (So Cai, So Nhat Ky) | Permanent | Type A | NĐ 43/2025/ND-CP | Online (5 years) + Cold storage (permanent) |
| Financial statements (B01, B02, B03, B09) | Permanent | Type A | NĐ 43/2025/ND-CP | Online (5 years) + Cold storage (permanent) |
| Fixed asset records | Permanent | Type A | NĐ 43/2025/ND-CP | Online (5 years) + Cold storage (permanent) |
| Investment documents | Permanent | Type A | NĐ 43/2025/ND-CP | Online (5 years) + Cold storage (permanent) |
| Tax declarations | 10 years | Type B | NĐ 43/2025/ND-CP, Luật QL Thuế | Online (5 years) + Cold storage (5 years) |
| E-invoices | 10 years | Type B | NĐ 43/2025/ND-CP, NĐ 70/2025 | Online (5 years) + Cold storage (5 years) |
| Payroll records | 10 years | Type B | NĐ 43/2025/ND-CP, Bộ luật Lao động | Online (5 years) + Cold storage (5 years) |
| Bank statements | 10 years | Type B | NĐ 43/2025/ND-CP | Online (5 years) + Cold storage (5 years) |
| Journal entries (supporting docs) | 10 years | Type B | NĐ 43/2025/ND-CP | Online (5 years) + Cold storage (5 years) |
| Vouchers (Phieu thu, Phieu chi) | 10 years | Type B | NĐ 43/2025/ND-CP | Online (5 years) + Cold storage (5 years) |
| Employee contracts | 5 years after termination | Type C | NĐ 43/2025/ND-CP, Bộ luật Lao động | Online (2 years) + Cold storage (3 years) |
| Attendance records | 5 years | Type C | NĐ 43/2025/ND-CP | Online (2 years) + Cold storage (3 years) |
| Audit logs | 10 years | Type B | NĐ 43/2025/ND-CP, Luật Kế toán | Online (2 years) + Cold storage (8 years) |
| System configuration | Permanent | Type A | Internal policy | Online |

### 13.2 Archival Process

```
[Start: Data Age > Active Period]
        |
        v
[Identify Data for Archival]
        |
        v
[Compress Data]
        |
        v
[Encrypt Compressed Data]
        |
        v
[Transfer to Cold Storage]
        |
        v
[Verify Integrity]
        |
        v
<Verification Passed?>
        |
        +-- No --> [Retry Transfer]
        |
        +-- Yes
        |
        v
[Update Data Catalog]
        |
        v
[Remove from Active Database]
        |
        v
[End: Data Archived]
```

### 13.3 Data Destruction

| Data Type | Destruction Method | Verification |
|-----------|-------------------|--------------|
| Active database records | Soft delete (mark as deleted) | Audit log entry |
| Archived data | Cryptographic erasure (delete encryption key) | Key destruction log |
| Backup data | Overwrite with random data (3 passes) | Verification hash |
| Physical media | Physical destruction | Destruction certificate |

---

## 14. DATA INTEGRATION POINTS

### 14.1 Integration Specifications

| Integration | Direction | Protocol | Format | Frequency | Authentication |
|------------|-----------|----------|--------|-----------|---------------|
| Tax Authority (GDT) | Outbound | HTTPS REST | XML | Per filing | Digital certificate |
| Tax Authority (GDT) | Inbound | HTTPS REST | XML | Per response | Digital certificate |
| E-Invoice Provider | Bidirectional | HTTPS REST | JSON/XML | Real-time | API key + Digital signature |
| Bank (Statement Import) | Inbound | SFTP | MT940/CSV | Daily | SFTP credentials |
| Bank (Payment Initiation) | Outbound | HTTPS API | JSON/XML | Per payment | OAuth 2.0 + Digital signature |
| Social Insurance (e-BHXH) | Outbound | HTTPS | XML | Monthly | Digital certificate |
| Time Tracking System | Inbound | HTTPS REST | JSON | Daily | API key |
| HTKK Export | Outbound | File Download | XML | Per filing | User authentication |

### 14.2 Data Mapping: Circular 99 to Financial Statements

#### B01-DN (Statement of Financial Position) Mapping

| B01-DN Line Item | Source Accounts | Calculation |
|-----------------|-----------------|-------------|
| A. TAI SAN NGAN HAN (Current Assets) | 111, 112, 113, 121, 128, 131, 133, 136, 138, 141, 151-158, 242 | Sum of account balances |
| I. Tien va tuong duong tien | 111, 112, 113 | Sum |
| II. Dau tu tai chinh ngan han | 121, 128 | Sum |
| III. Cac khoan phai thu ngan han | 131, 136, 138, 141 | Sum - 2293 |
| IV. Hang ton kho | 151-158 | Sum - 2294 |
| B. TAI SAN DAI HAN (Non-Current Assets) | 211-217, 221, 222, 228, 229, 241, 243, 244 | Sum of account balances |
| A. NO PHAI TRA NGAN HAN (Current Liabilities) | 331-338, 341, 343, 344, 352 | Sum of credit balances |
| B. NO PHAI TRA DAI HAN (Non-Current Liabilities) | 341, 343, 347, 352 | Long-term portion |
| C. VON CHU SO HUU (Equity) | 411-421 | Sum of credit balances |
| D. QUY BINH ON GIA (Price Stabilization Fund) | 357 | Per TT99 |

#### B02-DN (Statement of Business Results) Mapping

| B02-DN Line Item | Source Accounts | Calculation |
|-----------------|-----------------|-------------|
| 01. Doanh thu ban hang va CCDV | 511 | Credit turnover |
| 02. Cac khoan giam tru doanh thu | 521 | Debit turnover |
| 10. Doanh thu thuan ve BH va CCDV | 01 - 02 | Net revenue |
| 11. Gia von hang ban | 632 | Debit turnover |
| 20. Loi nhuan gop ve BH va CCDV | 10 - 11 | Gross profit |
| 21. Doanh thu hoat dong tai chinh | 515 | Credit turnover |
| 22. Chi phi tai chinh | 635 | Debit turnover |
| 23. Trong do: Chi phi lai vay | 635 | Detail from 635 |
| 25. Chi phi ban hang | 641 | Debit turnover |
| 26. Chi phi quan ly doanh nghiep | 642 | Debit turnover |
| 27. Trong do: Chi phi du phong | 6426 | Detail from 642 |
| 30. Loi nhuan thuan tu HDKD | 20 + 21 - 22 - 25 - 26 | Operating profit |
| 31. Thu nhap khac | 711 | Credit turnover |
| 32. Chi phi khac | 811 | Debit turnover |
| 33. Trong do: Chi phi phat vi pham hanh chinh | 811 | Detail from 811 |
| 40. Loi nhuan khac | 31 - 32 | Other profit |
| 50. Loi nhuan ke toan truoc thue | 30 + 40 | Profit before tax |
| 51. Chi phi thue TNDN hien hanh | 8211 | Debit turnover |
| 51.1. Chi phi thue TNDN hien hanh thong thuong | 82111 | Detail from 8211 |
| 51.2. Chi phi thue TNDN bo sung (toi thieu toan cau) | 82112 | Detail from 8211 |
| 52. Chi phi thue TNDN hoan lai | 8212 | Debit turnover |
| 60. LOI NHUAN SAU THUE | 50 - 51 - 52 | Net profit |

---

**END OF DATA FLOW DOCUMENT**
