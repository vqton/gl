# WORKFLOW DOCUMENT
# Vietnamese Enterprise Accounting Software
# Compliant with Circular 99/2025/TT-BTC

**Document Version:** 1.0
**Date:** April 2026
**Prepared by:** CFO Office

---

## TABLE OF CONTENTS

1. Workflow Overview
2. General Ledger Workflows
3. Accounts Receivable Workflows
4. Accounts Payable Workflows
5. Tax Management Workflows
6. Electronic Invoice Workflows
7. Payroll Workflows
8. Fixed Asset Workflows
9. Inventory Workflows
10. Bank & Cash Workflows
11. Financial Reporting Workflows
12. Period Close Workflows
13. System Administration Workflows
14. Exception & Error Handling Workflows

---

## 1. WORKFLOW OVERVIEW

### 1.1 Workflow Notation

```
[Start] --> (Process) --> <Decision?> --> [End]
                |
                +-- Yes --> (Next Process)
                +-- No  --> (Alternative Process)
```

### 1.2 Workflow Categories

| Category | Workflows | Priority |
|----------|-----------|----------|
| General Ledger | Journal Entry, Account Management, Period Management | P0 |
| Accounts Receivable | Invoice Creation, Payment Collection, Bad Debt | P0 |
| Accounts Payable | Invoice Processing, Payment Execution, Dispute | P0 |
| Tax Management | VAT Declaration, CIT Filing, PIT Filing | P0 |
| Electronic Invoice | Create, Replace, Adjust, Cancel | P0 |
| Payroll | Monthly Payroll, Insurance Reporting | P0 |
| Fixed Assets | Registration, Depreciation, Disposal | P1 |
| Inventory | Receipt, Issue, Valuation, Provision | P1 |
| Bank & Cash | Receipt, Payment, Reconciliation | P0 |
| Financial Reporting | Statement Generation, Review, Submission | P0 |
| Period Close | Reconciliation, Adjustment, Closing | P0 |
| Administration | User Management, Configuration, Backup | P0 |

---

## 2. GENERAL LEDGER WORKFLOWS

### 2.1 Journal Entry Workflow

```
[Start: New Transaction]
        |
        v
[Create Journal Entry]
        |
        v
(Select Accounting Period)
        |
        v
<Is Period Open?>
        |
        +-- No --> [Error: Period Closed] --> [End]
        |
        +-- Yes
        |
        v
(Enter Debit Account)
        |
        v
(Enter Credit Account)
        |
        v
(Enter Amount & Description)
        |
        v
<Is Debit = Credit?>
        |
        +-- No --> [Error: Unbalanced Entry] --> [Return to Entry]
        |
        +-- Yes
        |
        v
<Requires Approval?>
        |
        +-- No --> [Auto-Post] --> [Update GL Balances] --> [End]
        |
        +-- Yes
        |
        v
[Send to Approver]
        |
        v
<Approved?>
        |
        +-- No --> [Return to Creator with Comments] --> [Revise & Resubmit]
        |
        +-- Yes
        |
        v
[Post to General Ledger]
        |
        v
[Update Account Balances]
        |
        v
[Generate Audit Log Entry]
        |
        v
[End: Entry Posted]
```

### 2.2 Account Management Workflow

```
[Start: Need New Account]
        |
        v
[Propose New Account]
        |
        v
<Is Standard Circular 99 Account?>
        |
        +-- Yes --> [Activate Account] --> [End]
        |
        +-- No (Custom Sub-Account)
        |
        v
[Define Account Code, Name, Parent]
        |
        v
[Document Justification per Article 11]
        |
        v
<Does Not Overlap Existing Accounts?>
        |
        +-- No --> [Error: Code Conflict] --> [Revise]
        |
        +-- Yes
        |
        v
<Does Not Alter Financial Statement Items?>
        |
        +-- No --> [Error: FS Impact] --> [Revise]
        |
        +-- Yes
        |
        v
[Chief Accountant Approval]
        |
        v
[Create Account in System]
        |
        v
[Update Accounting Policy Document]
        |
        v
[End: Account Active]
```

### 2.3 Period Management Workflow

```
[Start: Period End]
        |
        v
[Initiate Period Close]
        |
        v
[Check All Sub-Ledgers Reconciled]
        |
        v
<All Reconciled?>
        |
        +-- No --> [List Unreconciled Items] --> [Resolve] --> [Recheck]
        |
        +-- Yes
        |
        v
[Run Automatic Accruals]
        |
        v
[Run Depreciation]
        |
        v
[Run Cost Allocation]
        |
        v
[Transfer to TK 911]
        |
        v
[Generate Trial Balance]
        |
        v
<Trial Balance Balanced?>
        |
        +-- No --> [Investigate Discrepancy] --> [Adjust] --> [Recheck]
        |
        +-- Yes
        |
        v
[Generate Financial Statements]
        |
        v
[Chief Accountant Review]
        |
        v
<Approved?>
        |
        +-- No --> [Make Adjustments] --> [Recheck]
        |
        +-- Yes
        |
        v
[Lock Accounting Period]
        |
        v
[Open Next Period]
        |
        v
[End: Period Closed]
```

---

## 3. ACCOUNTS RECEIVABLE WORKFLOWS

### 3.1 Sales Invoice Creation Workflow

```
[Start: Sale Confirmed]
        |
        v
[Create Sales Invoice]
        |
        v
(Select Customer)
        |
        v
<Customer Exists?>
        |
        +-- No --> [Create Customer Record] --> [Continue]
        |
        +-- Yes
        |
        v
(Add Line Items)
        |
        v
(Auto-Calculate Subtotal)
        |
        v
<Apply Commercial Discount?>
        |
        +-- Yes --> [Apply Discount per Decree 70/2025]
        |              |
        |              v
        |         [Generate Discount Invoice]
        |
        +-- No
        |
        v
(Select VAT Rate: 10%, 8%, 0%, Non-Taxable)
        |
        v
(Auto-Calculate VAT)
        |
        v
(Calculate Total)
        |
        v
[Generate E-Invoice per Decree 70/2025]
        |
        v
<Invoice with Tax Authority Code?>
        |
        +-- Yes --> [Request Code from CQT] --> [Receive Code]
        |
        +-- No --> [Generate Internal Number]
        |
        v
[Assign Invoice Number]
        |
        v
[Post to GL: DK 131/Co 511, 3331]
        |
        v
[Send Invoice to Customer]
        |
        v
[End: Invoice Created]
```

### 3.2 Payment Collection Workflow

```
[Start: Payment Received]
        |
        v
[Record Payment Receipt]
        |
        v
(Select Payment Method: Cash/Bank Transfer)
        |
        v
(Enter Amount)
        |
        v
<Auto-Match to Invoice?>
        |
        +-- Yes --> [Match to Open Invoice]
        |
        +-- No --> [Manual Match Selection]
        |
        v
<Full Payment?>
        |
        +-- Yes --> [Mark Invoice as Paid]
        |              |
        |              v
        |         [Post: DK 111,112/Co 131]
        |
        +-- No (Partial)
        |
        v
[Apply Partial Payment]
        |
        v
[Update Remaining Balance]
        |
        v
[Post Partial Payment Entry]
        |
        v
[End: Payment Recorded]
```

### 3.3 Bad Debt Provision Workflow

```
[Start: Overdue Receivable]
        |
        v
[Run AR Aging Report]
        |
        v
<Overdue > 180 Days?>
        |
        +-- No --> [Monitor] --> [End]
        |
        +-- Yes
        |
        v
[Assess Collectibility]
        |
        v
<Probable Non-Collection?>
        |
        +-- No --> [Continue Monitoring] --> [End]
        |
        +-- Yes
        |
        v
[Calculate Provision Amount]
        |
        v
[Create Provision Journal Entry]
        |
        v
[Post: DK 6426/Co 2293]
        |
        v
[Document Provision Justification]
        |
        v
  Required evidence per tax law:
  - Bien ban xac nhan no kho doi
  - Court documents / Police reports / Debt collection records
  - Correspondence with debtor
        |
        v
[Chief Accountant Approval]
        |
        v
[End: Provision Recorded]
```

---

## 4. ACCOUNTS PAYABLE WORKFLOWS

### 4.1 Supplier Invoice Processing Workflow

```
[Start: Supplier Invoice Received]
        |
        v
[Upload/Scan Invoice]
        |
        v
[OCR Data Extraction]
        |
        v
<OCR Confidence > 90%?>
        |
        +-- No --> [Manual Data Entry]
        |
        +-- Yes --> [Auto-Populate Fields]
        |
        v
(Verify Supplier Details)
        |
        v
(Verify Invoice Amount)
        |
        v
<3-Way Match Required?>
        |
        +-- Yes --> [Match PO - Receipt - Invoice]
        |              |
        |              v
        |         <Match?>
        |              |
        |              +-- No --> [Flag Discrepancy] --> [Resolve] --> [Recheck]
        |              +-- Yes --> [Continue]
        |
        +-- No --> [Continue]
        |
        v
(Verify Input VAT - TK 1331)
        |
        v
<Valid Input VAT?>
        |
        +-- No --> [Mark as Non-Deductible] --> [Continue]
        |
        +-- Yes --> [Record as Deductible VAT]
        |
        v
[Route for Approval]
        |
        v
<Approved?>
        |
        +-- No --> [Return to Submitter] --> [Revise] --> [Resubmit]
        |
        +-- Yes
        |
        v
[Post to GL: DK 152,153,156,211,642... + 1331 / Co 331]
        |
        v
[Add to Payment Queue]
        |
        v
[End: Invoice Processed]
```

### 4.2 Payment Execution Workflow

```
[Start: Payment Due]
        |
        v
[Select Invoices for Payment]
        |
        v
[Verify Payment Terms]
        |
        v
<Early Payment Discount Available?>
        |
        +-- Yes --> [Calculate Discount] --> [Apply]
        |
        +-- No --> [Continue]
        |
        v
[Create Payment Request]
        |
        v
[Route for Approval]
        |
        v
<Approved?>
        |
        +-- No --> [Return] --> [Revise] --> [Resubmit]
        |
        +-- Yes
        |
        v
[Execute Payment (Bank Transfer)]
        |
        v
[Post: DK 331/Co 112]
        |
        v
[Update Supplier Balance]
        |
        v
[Send Payment Confirmation]
        |
        v
[End: Payment Complete]
```

---

## 5. TAX MANAGEMENT WORKFLOWS

### 5.1 VAT Declaration Workflow (Monthly/Quarterly)

```
[Start: VAT Filing Period]
        |
        v
[Collect Input VAT Data (TK 1331, 1332)]
        |
        v
[Collect Output VAT Data (TK 33311, 33312)]
        |
        v
[Verify E-Invoice Data]
        |
        v
<All Invoices Verified?>
        |
        +-- No --> [Identify Missing/Invalid] --> [Resolve] --> [Reverify]
        |
        +-- Yes
        |
        v
[Classify VAT by Rate: 10%, 8%, 0%, Non-Taxable]
        |
        v
[Identify Non-Deductible Input VAT]
        |
        v
[Calculate Deductible Input VAT]
        |
        v
[Calculate Output VAT]
        |
        v
[Calculate VAT Payable/Refundable]
        |
        v
<Output VAT > Input VAT?>
        |
        +-- Yes (Payable)
        |     |
        |     v
        |     [Generate Form 01/GTGT]
        |     |
        |     v
        |     [Record Payable: DK 3331/Co 112 (when paid)]
        |
        +-- No (Refundable)
              |
              v
              [Generate Form 01/GTGT + Refund Request]
              |
              v
              [Record Receivable: DK 1388/Co 3331]
        |
        v
[Chief Accountant Review]
        |
        v
<Approved?>
        |
        +-- No --> [Adjust] --> [Recalculate]
        |
        +-- Yes
        |
        v
[Submit to Tax Authority Portal]
        |
        v
[Receive Submission Confirmation]
        |
        v
[Archive Declaration]
        |
        v
[End: VAT Filed]
```

### 5.2 CIT Quarterly Provisional Workflow

```
[Start: Quarter End]
        |
        v
[Calculate Quarterly Revenue]
        |
        v
[Calculate Quarterly Deductible Expenses]
        |
        v
[Calculate Quarterly Profit]
        |
        v
<Profit > 0?>
        |
        +-- No (Loss) --> [Record Loss for Carryforward] --> [End: No CIT]
        |
        +-- Yes
        |
        v
[Apply CIT Rate (20% or preferential)]
        |
        v
[Calculate Provisional CIT]
        |
        v
[Deduct Prior Quarter Payments]
        |
        v
[Calculate CIT Payable]
        |
        v
[Generate Form 01A/TNDN]
        |
        v
[Post: DK 8211/Co 3334]
        |
        v
[Submit to Tax Authority]
        |
        v
[End: CIT Provisional Filed]
```

### 5.3 PIT Monthly/Quarterly Workflow

```
[Start: PIT Filing Period]
        |
        v
[Collect Employee Salary Data]
        |
        v
[Calculate Gross Income per Employee]
        |
        v
[Apply Personal Deduction (11M VND/month)]
        |
        v
[Apply Dependent Deductions (4.4M VND/dependent)]
        |
        v
[Calculate Taxable Income]
        |
        v
[Apply Progressive Tax Rates]
        |
        v
[Calculate PIT Withholding]
        |
        v
[Generate Form 02/KK-TNCN]
        |
        v
[Post: DK 334/Co 3335]
        |
        v
[Submit to Tax Authority]
        |
        v
[End: PIT Filed]
```

---

## 6. ELECTRONIC INVOICE WORKFLOWS

### 6.1 E-Invoice Creation Workflow

```
[Start: Sale Transaction]
        |
        v
[Create Invoice Data]
        |
        v
<Invoice Type?>
        |
        +-- With CQT Code
        |     |
        |     v
        |     [Send to Tax Authority API]
        |     |
        |     v
        |     <Code Received?>
        |     |
        |     +-- No --> [Retry/Error Handling]
        |     +-- Yes --> [Attach Code]
        |
        +-- Without CQT Code
        |     |
        |     v
        |     [Generate Internal Number]
        |
        v
[Apply Invoice Template per Decree 70/2025]
        |
        v
[Include Mandatory Fields]
        |
        v
[Apply Digital Signature]
        |
        v
[Send to Customer]
        |
        v
[Record in Invoice Register]
        |
        v
[End: E-Invoice Created]
```

### 6.2 Invoice Replacement Workflow (per Decree 70/2025)

```
[Start: Invoice Error Detected]
        |
        v
[Identify Error Type]
        |
        v
<Error Type?>
        |
        +-- Wrong Information --> [Replacement Required]
        +-- Wrong Amount --> [Adjustment Required]
        +-- Wrong Period --> [Replacement Required]
        +-- Cancel Needed --> [Cancellation Workflow]
        |
        v (Replacement)
[Create Replacement Invoice]
        |
        v
[Reference Original Invoice]
        |
        v
[Generate Replacement Document (Bien Ban Thay The)]
        |
        v
[Both Parties Sign]
        |
        v
[Submit 04/SS-HDDT to Tax Authority]
        |
        v
[Issue Replacement Invoice]
        |
        v
[Adjust GL Entries]
        |
        v
[End: Invoice Replaced]
```

### 6.3 Invoice Adjustment Workflow (Increase/Decrease)

```
[Start: Invoice Adjustment Needed]
        |
        v
[Identify Adjustment Type]
        |
        v
<Increase or Decrease?>
        |
        +-- Increase
        |     |
        |     v
        |     [Create Adjustment Invoice (Increase)]
        |     |
        |     v
        |     [Generate Bien Ban Dieu Chinh]
        |     |
        |     v
        |     [Post Additional Revenue/VAT]
        |
        +-- Decrease
              |
              v
              [Create Adjustment Invoice (Decrease)]
              |
              v
              [Generate Bien Ban Dieu Chinh]
              |
              v
              [Reverse Revenue/VAT]
        |
        v
[Submit to Tax Authority]
        |
        v
[End: Invoice Adjusted]
```

---

## 7. PAYROLL WORKFLOWS

### 7.1 Monthly Payroll Processing Workflow

```
[Start: Payroll Cycle]
        |
        v
[Import Attendance Data]
        |
        v
[Validate Attendance]
        |
        v
<Errors?>
        |
        +-- Yes --> [Correct Attendance] --> [Revalidate]
        |
        +-- No
        |
        v
[Update Employee Changes]
        |
        v
[Calculate Gross Salary]
        |
        v
  Base + Allowances + Overtime + Bonuses
        |
        v
[Calculate Insurance Deductions]
        |
        v
  BHXH: 8% (employee) | BHYT: 1.5% (employee) | BHTN: 1% (employee)
  Employer: BHXH 14% | BHYT 3% | BHTN 1% | BHTNLĐ-BNN 0.5%
        |
        v
[Calculate PIT Withholding]
        |
        v
  (Gross - Insurance - Personal Deduction 11M - Dependent Deduction 4.4M x N) x Tax Rate
        |
        v
[Calculate Net Salary]
        |
        v
  Gross - Employee Insurance (10.5%) - PIT
        |
        v
[Generate Payroll Register]
        |
        v
[Chief Accountant Review]
        |
        v
<Approved?>
        |
        +-- No --> [Adjust] --> [Recalculate]
        |
        +-- Yes
        |
        v
[Generate Payslips]
        |
        v
[Create Bank Transfer File]
        |
        v
[Process Salary Payment]
        |
        v
[Post: DK 642,622,641... / Co 334, 3383 (BHXH 17.5%), 3384 (BHYT 3%), 3386 (BHTN 1%), 3382 (KPCD 2%), 3335 (PIT)]
        |
        v
[Generate Insurance Declaration]
        |
        v
[Submit to Social Insurance]
        |
        v
[End: Payroll Complete]
```

---

## 8. FIXED ASSET WORKFLOWS

### 8.1 Asset Registration Workflow

```
[Start: Asset Acquired]
        |
        v
[Receive Asset Documentation]
        |
        v
[Create Asset Record]
        |
        v
(Enter: Name, Code, Category, Original Cost)
        |
        v
(Select Depreciation Method)
        |
        v
  Straight-Line | Declining Balance | Units of Production
        |
        v
(Set Useful Life, Residual Value)
        |
        v
(Assign Location, Cost Center, Responsible Person)
        |
        v
[Generate Bien Ban Giao Nhan TSCD (01-TSCD)]
        |
        v
[Post: DK 211,212,213/Co 111,112,331,241...]
        |
        v
[End: Asset Registered]
```

### 8.2 Monthly Depreciation Workflow

```
[Start: Month End]
        |
        v
[Identify Assets for Depreciation]
        |
        v
<New Assets Put Into Use This Month?>
        |
        +-- Yes --> [Start Depreciation from Next Month]
        |
        +-- No --> [Continue]
        |
        v
<Disposed Assets This Month?>
        |
        +-- Yes --> [Stop Depreciation]
        |
        +-- No --> [Continue]
        |
        v
[Calculate Depreciation per Asset]
        |
        v
[Aggregate by Cost Center]
        |
        v
[Generate Depreciation Schedule]
        |
        v
[Post: DK 6274,6424,6414... / Co 2141,2142,2143]
        |
        v
[End: Depreciation Posted]
```

### 8.3 Asset Disposal Workflow

```
[Start: Asset Disposal Decision]
        |
        v
[Initiate Disposal Request]
        |
        v
[Calculate Net Book Value]
        |
        v
  NBV = Original Cost - Accumulated Depreciation
        |
        v
[Estimate Disposal Proceeds]
        |
        v
[Calculate Gain/Loss]
        |
        v
  Gain/Loss = Proceeds - NBV
        |
        v
[Generate Bien Ban Thanh Ly TSCD]
        |
        v
[Approval (per Company Policy)]
        |
        v
<Approved?>
        |
        +-- No --> [Cancel Disposal] --> [End]
        |
        +-- Yes
        |
        v
[Remove Asset from Register]
        |
        v
[Post Disposal Entries]
        |
        v
  DK 214 (Accum. Depr.)
  DK 811 (Loss) / Co 711 (Gain)
  DK 111,112 (Proceeds)
  Co 211,212,213 (Original Cost)
        |
        v
[End: Asset Disposed]
```

---

## 9. INVENTORY WORKFLOWS

### 9.1 Goods Receipt Workflow

```
[Start: Goods Received]
        |
        v
[Verify Delivery against PO]
        |
        v
<Quantity/Quality Match?>
        |
        +-- No --> [Record Discrepancy] --> [Notify Purchasing] --> [Resolve]
        |
        +-- Yes
        |
        v
[Create Goods Receipt Note (01-VT)]
        |
        v
[Update Inventory Quantity]
        |
        v
[Calculate Unit Cost]
        |
        v
  (Per Valuation Method: FIFO, Weighted Average)
        |
        v
[Post: DK 152,153,156/Co 331,111,112]
        |
        v
[End: Goods Received]
```

### 9.2 Goods Issue Workflow

```
[Start: Goods Request]
        |
        v
[Check Stock Availability]
        |
        v
<Sufficient Stock?>
        |
        +-- No --> [Notify Requestor] --> [End]
        |
        +-- Yes
        |
        v
[Create Goods Issue Note (02-VT)]
        |
        v
[Calculate Issue Cost]
        |
        v
  (Per Valuation Method)
        |
        v
[Update Inventory Quantity]
        |
        v
[Post: DK 621,641,642... / Co 152,153,156]
        |
        v
[End: Goods Issued]
```

---

## 9B. ADDITIONAL PERIOD-END WORKFLOWS

### 9B.1 Exchange Rate Revaluation Workflow (TK 413)

```
[Start: Period End]
        |
        v
[Identify All Monetary Items in Foreign Currency]
        |
        v
  - Cash in foreign currency (TK 112)
  - Receivables in foreign currency (TK 131)
  - Payables in foreign currency (TK 331)
  - Loans in foreign currency (TK 341)
        |
        v
[Get Closing Exchange Rate from SBV]
        |
        v
[Revalue Each Monetary Item]
        |
        v
  Revalued Amount = Foreign Currency Amount x Closing Rate
        |
        v
[Calculate Exchange Rate Difference]
        |
        v
  Difference = Revalued Amount - Book Amount
        |
        v
<Difference Type?>
        |
        +-- Gain --> [Post: DK 111,112,131... / Co 413]
        |
        +-- Loss --> [Post: DK 413 / Co 111,112,331...]
        |
        v
[Record in Exchange Rate Difference Account (TK 413)]
        |
        v
[End: FX Revaluation Complete]
```

### 9B.2 CCDC Allocation Workflow (Phân bổ công cụ dụng cụ TK 242)

```
[Start: Period End]
        |
        v
[Identify CCDC Pending Allocation (TK 242)]
        |
        v
[Calculate Monthly Allocation per Item]
        |
        v
  Monthly Allocation = Original Cost / Allocation Period (months)
        |
        v
[Allocate by Cost Center/Department]
        |
        v
<Allocation Target?>
        |
        +-- Production --> [Post: DK 6273 / Co 242]
        +-- Sales --> [Post: DK 6413 / Co 242]
        +-- Management --> [Post: DK 6423 / Co 242]
        |
        v
[Generate CCDC Allocation Table (Bang Phan Bo CCDC)]
        |
        v
[End: CCDC Allocation Complete]
```

### 9B.3 Inventory Provision Workflow (Lập dự phòng giảm giá HTK TK 2294)

```
[Start: Period End (Annual)]
        |
        v
[Identify Inventory Items for Provision Assessment]
        |
        v
[Compare Cost vs. Net Realizable Value (NRV)]
        |
        v
<NRV < Cost?>
        |
        +-- No --> [No Provision Required] --> [End]
        |
        +-- Yes
        |
        v
[Calculate Provision Amount]
        |
        v
  Provision = Cost - NRV - Previously Provided Amount
        |
        v
<Provision > 0?>
        |
        +-- Yes (Increase) --> [Post: DK 632 / Co 2294]
        |
        +-- No (Decrease) --> [Reverse: DK 2294 / Co 632]
        |
        v
[Document Provision Justification]
        |
        v
  Required: Price comparison, market data, inventory condition report
        |
        v
[Chief Accountant Approval]
        |
        v
[End: Inventory Provision Complete]
```

### 9B.4 TK 911 Year-End Closing Workflow

```
[Start: Fiscal Year End]
        |
        v
[Ensure All Revenue/Cost Accounts Have Balances]
        |
        v
[Transfer All Revenues to TK 911 (Credit Side)]
        |
        v
  DK 511, 515, 711 / Co 911
        |
        v
[Transfer All Costs to TK 911 (Debit Side)]
        |
        v
  DK 911 / Co 632, 635, 641, 642, 811, 821
        |
        v
[Calculate Net Profit/Loss]
        |
        v
  Net Result = Total Revenue (credit 911) - Total Cost (debit 911)
        |
        v
<Result Type?>
        |
        +-- Profit --> [Transfer to Retained Earnings: DK 911 / Co 421]
        |
        +-- Loss --> [Transfer to Retained Earnings: DK 421 / Co 911]
        |
        v
[Close TK 911 (Zero Balance)]
        |
        v
[Close TK 421 Sub-Accounts]
        |
        v
  Transfer TK 4212 (current year) to TK 4211 (accumulated)
        |
        v
[Generate Year-End Closing Report]
        |
        v
[Chief Accountant Approval]
        |
        v
[End: Year-End Closing Complete]
```

---

## 10. BANK & CASH WORKFLOWS

### 10.1 Bank Reconciliation Workflow

```
[Start: Bank Statement Received]
        |
        v
[Import Bank Statement]
        |
        v
  (MT940, CSV, Excel)
        |
        v
[Auto-Match Transactions]
        |
        v
<Match Found?>
        |
        +-- Yes --> [Mark as Reconciled]
        |
        +-- No --> [Flag for Manual Review]
        |
        v
[Manual Review Unmatched Items]
        |
        v
<Identified?>
        |
        +-- Yes --> [Match Manually]
        |
        +-- No --> [Create Adjusting Entry]
        |
        v
[Calculate Reconciliation Difference]
        |
        v
<Difference = 0?>
        |
        +-- No --> [Investigate] --> [Adjust] --> [Recheck]
        |
        +-- Yes
        |
        v
[Mark Period as Reconciled]
        |
        v
[End: Bank Reconciled]
```

### 10.2 Cash Receipt Workflow

```
[Start: Cash Received]
        |
        v
[Verify Cash Amount]
        |
        v
[Create Cash Receipt Voucher (01-TT)]
        |
        v
[Select Source Account]
        |
        v
  (Customer, Other Income, etc.)
        |
        v
[Post: DK 111/Co 131,511,711...]
        |
        v
[Update Cash Balance]
        |
        v
[Print Receipt]
        |
        v
[End: Cash Recorded]
```

---

## 11. FINANCIAL REPORTING WORKFLOWS

### 11.1 Annual Financial Statement Workflow

```
[Start: Year End]
        |
        v
[Ensure All Periods Closed]
        |
        v
[Run Year-End Procedures]
        |
        v
  - Transfer TK 911 to TK 421
  - Close revenue/expense accounts
  - Calculate retained earnings
        |
        v
[Generate B01-DN: Statement of Financial Position]
        |
        v
[Generate B02-DN: Statement of Business Results]
        |
        v
[Generate B03-DN: Cash Flow Statement]
        |
        v
[Generate B09-DN: Notes to Financial Statements]
        |
        v
[Chief Accountant Review]
        |
        v
<Errors Found?>
        |
        +-- Yes --> [Adjust] --> [Regenerate]
        |
        +-- No
        |
        v
[CFO Approval]
        |
        v
<Approved?>
        |
        +-- No --> [Adjust] --> [Regenerate]
        |
        +-- Yes
        |
        v
[Legal Representative Signature]
        |
        v
[Submit to Authorities]
        |
        v
  - Tax Authority (within 90 days of fiscal year-end for annual BCTC)
  - Statistics Office (within 90 days)
  - Business Registration Office (within 90 days)
  - Quarterly BCTC: within 30 days of quarter-end
        |
        v
[Archive Financial Statements]
        |
        v
[End: Financial Statements Complete]
```

---

## 12. PERIOD CLOSE WORKFLOWS

### 12.1 Month-End Close Workflow

```
[Start: Month End]
        |
        v
[Step 1: Complete All Sub-Ledger Entries]
        |
        v
  - AR: All invoices and receipts posted
  - AP: All invoices and payments posted
  - Inventory: All receipts and issues posted
  - Fixed Assets: Depreciation posted
  - Payroll: Salary entries posted
        |
        v
[Step 2: Reconcile All Accounts]
        |
        v
  - Bank reconciliation
  - AR/AP reconciliation
  - Inventory count reconciliation
  - Inter-company reconciliation
        |
        v
[Step 3: Run Automatic Entries]
        |
        v
  - Depreciation
  - Amortization
  - Accruals
  - Cost allocation
  - Exchange rate revaluation
        |
        v
[Step 4: Review Trial Balance]
        |
        v
<Trial Balance Balanced?>
        |
        +-- No --> [Investigate & Adjust] --> [Recheck]
        |
        +-- Yes
        |
        v
[Step 5: Generate Management Reports]
        |
        v
[Step 6: Close Period]
        |
        v
[Step 7: Open Next Period]
        |
        v
[End: Month Close Complete]
```

---

## 13. SYSTEM ADMINISTRATION WORKFLOWS

### 13.1 User Access Management Workflow

```
[Start: New User Required]
        |
        v
[Submit User Access Request]
        |
        v
(Define Role & Permissions)
        |
        v
<Role Matches Job Function?>
        |
        +-- No --> [Select Correct Role]
        |
        +-- Yes
        |
        v
[IT Manager Approval]
        |
        v
<Approved?>
        |
        +-- No --> [Reject] --> [End]
        |
        +-- Yes
        |
        v
[Create User Account]
        |
        v
[Assign Role & Permissions]
        |
        v
[Set Initial Password]
        |
        v
[Send Credentials to User]
        |
        v
[User Changes Password on First Login]
        |
        v
[End: User Access Granted]
```

### 13.2 Data Backup Workflow

```
[Start: Scheduled Backup]
        |
        v
[Daily: Incremental Backup]
        |
        v
[Weekly: Full Backup]
        |
        v
[Encrypt Backup Data]
        |
        v
[Store in Secondary Location]
        |
        v
[Verify Backup Integrity]
        |
        v
<Verification Passed?>
        |
        +-- No --> [Alert Admin] --> [Rerun Backup]
        |
        +-- Yes
        |
        v
[Log Backup Details]
        |
        v
[End: Backup Complete]
```

---

## 14. EXCEPTION & ERROR HANDLING WORKFLOWS

### 14.1 Unbalanced Journal Entry Handling

```
[Start: Entry Submission]
        |
        v
<Debit = Credit?>
        |
        +-- Yes --> [Proceed to Posting]
        |
        +-- No
        |
        v
[Block Submission]
        |
        v
[Display Error: "Entry unbalanced by X VND"]
        |
        v
[Highlight Imbalance]
        |
        v
[Suggest Correction]
        |
        v
[User Corrects Entry]
        |
        v
[Revalidate]
        |
        v
[End: Entry Balanced or Cancelled]
```

### 14.2 E-Invoice Error Handling

```
[Start: E-Invoice Error Detected]
        |
        v
<Error Type?>
        |
        +-- Wrong Buyer Info --> [Issue Adjustment Invoice]
        +-- Wrong Amount --> [Issue Replacement Invoice]
        +-- Wrong Tax Rate --> [Issue Replacement Invoice]
        +-- Duplicate Invoice --> [Cancel Duplicate]
        +-- System Error --> [Retry with Error Log]
        |
        v
[Generate Correction Document]
        |
        v
[Obtain Required Signatures]
        |
        v
[Submit 04/SS-HDDT to Tax Authority]
        |
        v
[Issue Corrected Invoice]
        |
        v
[Adjust GL Entries]
        |
        v
[End: Error Resolved]
```

### 14.3 Tax Filing Deadline Missed Handling

```
[Start: Deadline Missed Detected]
        |
        v
[System Alert: Overdue Filing]
        |
        v
[Calculate Late Filing Penalty]
        |
        v
[Generate Penalty Estimate]
        |
        v
[Notify Chief Accountant & CFO]
        |
        v
[Prepare Late Filing]
        |
        v
[Submit with Penalty Payment]
        |
        v
[Record Penalty: DK 8218 (tax penalty) or DK 811 (admin penalty) / Co 3339]
        |
        v
[Document Root Cause]
        |
        v
[Implement Preventive Measures]
        |
        v
[End: Late Filing Resolved]
```

---

**END OF WORKFLOW DOCUMENT**
