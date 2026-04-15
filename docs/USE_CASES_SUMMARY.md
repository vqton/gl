# 📋 TT99 USE CASES SUMMARY
*Consolidated - Last Updated: April 2026*
*See also: MASTER_USE_CASES.md for complete reference*

---

## 📁 DOCUMENT STRUCTURE

| File | Content |
|------|---------|
| [MASTER_USE_CASES.md](MASTER_USE_CASES.md) | Consolidated master document |
| [use_cases/sales_use_cases.md](use_cases/sales_use_cases.md) | Sales (S01-S06) detail |
| [use_cases/laodong_tienluong.md](use_cases/laodong_tienluong.md) | Payroll detail |
| [use_cases/coa_use_cases.md](use_cases/coa_use_cases.md) | COA detail |
| [docs/core_use_cases_TT99_2025_updated.md](core_use_cases_TT99_2025_updated.md) | TT99 Full specs |  
*See also: MASTER_USE_CASES.md for complete reference*

---

## 📁 DOCUMENT STRUCTURE

| File | Content |
|------|---------|
| [MASTER_USE_CASES.md](MASTER_USE_CASES.md) | Consolidated master document |
| [docs/use_cases/sales_use_cases.md](docs/use_cases/sales_use_cases.md) | Sales (S01-S06) detail |
| [docs/use_cases/laodong_tienluong.md](docs/use_cases/laodong_tienluong.md) | Payroll detail |
| [docs/use_cases/coa_use_cases.md](docs/use_cases/coa_use_cases.md) | COA detail |
| [docs/core_use_cases_TT99_2025_updated.md](docs/core_use_cases_TT99_2025_updated.md) | TT99 Full specs |

---

## 📊 OVERVIEW

| Module | Use Cases | Status | Priority |
|--------|----------|--------|----------|
| **COA** (Chart of Accounts) | C01-C09 | ⚠️ Partial | P1 |
| **Sales & Revenue** (S01-S06) | S01-S06 | 📝 Documented | P0 |
| **Purchase & Inventory** (P01-P05) | P01-P05 | ⚠️ Partial | P0 |
| **Cash & Bank** (T01-T05) | T01-T05 | ⚠️ Partial | P0 |
| **Tax** (X01-X05) | X01-X05 | ⚠️ Partial | P1 |
| **Fixed Assets** (A01-A06) | A01-A06 | ✅ Complete | P2 |
| **Payroll** (L01-L07) | L01-L07 | ✅ Complete | P2 |
| **Period Closing** (G01-G08) | G01-G08 | ✅ G01-G04 | P2 |

---

## 🔴 P0: CORE ACCOUNTING USE CASES

### 1. COA — Chart of Accounts (9 use cases)
| ID | Name | Status | Notes |
|----|------|--------|-------|
| C01 | Create Account | ✅ Entity exists | Code, Name, Type, Parent |
| C02 | Update Account | ⚠️ Partial | Cannot if has transactions |
| C03 | Delete Account | ⚠️ Partial | Check children/journals |
| C04 | Validate Hierarchy | ⚠️ Partial | Circular reference check |
| C05 | Set Posting Flag | ✅ Auto | Parent = false |
| C06 | Get Account Tree | ⚠️ Partial | Need UI/API |
| C07 | Validate Before Journal | ⚠️ Partial | Need service |
| C08 | Import COA (CSV) | ❌ Not implemented | Optional |
| C09 | Export COA | ❌ Not implemented | Optional |

### 2. Sales & Revenue (S01-S06)
| ID | Name | Status | Notes |
|----|------|--------|-------|
| S01 | Cash Sales + VAT | ✅ Implemented | 111 → 511, 33311 |
| S02 | Credit Sales (131) | ✅ Implemented | 131 → 511, 33311 |
| S03 | Record COGS (632) | ✅ Implemented | 632 → 156/155 |
| S04 | Sales Returns | ✅ Implemented | 5212 |
| S05 | Sales Discount | ✅ Implemented | 5211 |
| S06 | Payment Discount | ✅ Implemented | 5213 |

**Status: ✅ Implemented (6/6) - 9 new tests**

### 3. Purchase & Inventory (P01-P05)
| ID | Name | Status | Notes |
|----|------|--------|-------|
| P01a | Purchase + Invoice together | 📝 Documented | 156, 1331, 331 |
| P01b | Invoice before goods | 📝 Documented | 151 tracking |
| P01c | Goods before invoice | 📝 Documented | Temp pricing |
| P02 | Direct to cost (no inventory) | 📝 Documented | 621/627/641 |
| P03 | Purchase with freight | 📝 Documented | 1562 cost |
| P04 | Trade discount | 📝 Documented | 521 |
| P05 | Purchase returns | 📝 Documented | 156, 1331, 331 |
| P06 | Installment purchase | 📝 Documented | 242 interest |

**Status: 📝 Documented (Implementation pending)**

### 4. Cash & Bank (T01-T05)
| ID | Name | Status | Notes |
|----|------|--------|-------|
| T01 | Pay Supplier (331→111/112) | ⚠️ Partial | Transaction service |
| T02 | Receive Customer (131→111/112) | ⚠️ Partial | Transaction service |
| T03 | Bank Transfer (111→112) | ⚠️ Partial | Transaction service |
| T04 | Petty Cash | ❌ Not implemented | Need service |
| T05 | Reconcile Bank Statement | ❌ Not implemented | |

### 5. Tax (X01-X05)
| ID | Name | Status | Notes |
|----|------|--------|-------|
| X01 | VAT Input (1331) | ⚠️ Partial | Transaction service |
| X02 | VAT Output (33311) | ⚠️ Partial | Transaction service |
| X03 | PIT Withholding | ⚠️ Partial | Need service |
| X04 | Annual Tax Declaration | ❌ Not implemented | |
| X05 | FCT Invoice | ❌ Not implemented | |

### 6. Payroll & Social Insurance (L01-L07)
| ID | Name | Status | Notes |
|----|------|--------|-------|
| L01 | Labor Contract Management | ✅ Complete | Entity + Service |
| L02 | Monthly Payroll | ✅ Complete | With BH, PIT |
| L03 | Overtime Calculation | ✅ Complete | 150/200/300% |
| L04 | Leave Management | ✅ Complete | 12-19 days |
| L05 | Severance Pay | ✅ Complete | 0.5 month/year |
| L06 | Social Insurance Declaration | ✅ Complete | 17.5% |
| L07 | Salary Scale | ✅ Complete | Grade/Coefficient |

**Status: ✅ COMPLETE (7/7)**

### 7. Fixed Assets (A01-A06)
| ID | Name | Status | Notes |
|----|------|--------|-------|
| A01 | Add Asset (211) | ✅ Complete | FixedAsset entity |
| A02 | Depreciation (214/627) | ✅ Complete | StraightLine + Declining |
| A03 | Asset Transfer (211) | ✅ Complete | Department transfer |
| A04 | Asset Disposal (811) | ✅ Complete | With journal entry |
| A05 | Asset Revaluation (412) | ✅ Complete | Optional |
| A06 | Asset Inventory | ⚠️ Partial | Need count service |

**Status: ✅ COMPLETE (6/6)**

### 8. Period Closing (G01-G08)
| ID | Name | Status | Notes |
|----|------|--------|-------|
| G01 | Transfer Revenue to 911 | ✅ Complete | 511,515,711→911 |
| G02 | Transfer Expenses to 911 | ✅ Complete | 632,641,642→911 |
| G03 | Transfer Profit to 4212 | ✅ Complete | 911→4212 |
| G04 | Allocate Prepaid (242) | ✅ Complete | Prepaid allocation |
| G05 | Provision for Receivables | ❌ Not implemented | 2293 |
| G06 | FX Difference (413) | ❌ Not implemented | |
| G07 | Adjust Prepaid Income | ❌ Not implemented | |
| G08 | Final Period Closing | ❌ Not implemented | |

**Status: ✅ COMPLETE (G01-G04), 4 remaining**

**Status: ❌ NOT IMPLEMENTED (G01-G04 critical)**

---

## 🟠 P1: SUPPORTING USE CASES

### 9. Reporting (R01-R05)
| ID | Name | Status | Notes |
|----|------|--------|-------|
| R01 | Trial Balance (B01) | ❌ Not implemented | Need GL aggregates |
| R02 | Income Statement (B02) | ❌ Not implemented | Need G01/G02 |
| R03 | Cash Flow (B03) | ❌ Not implemented | |
| R04 | Aging Receivables | ⚠️ Partial | Need service |
| R05 | Aging Payables | ❌ Not implemented | |

### 10. Audit Trail (AT01-AT03)
| ID | Name | Status | Notes |
|----|------|--------|-------|
| AT01 | Log All Journal Entries | ⚠️ Partial | Entity exists |
| AT02 | Audit Report | ⚠️ Partial | Service exists |
| AT03 | User Activity | ❌ Not implemented | Need service |

---

## 📌 IMPLEMENTATION PRIORITY (Chief Accountant Recommended)

| Priority | Use Cases | Reason |
|----------|----------|--------|
| 🔴 **P0.1** | A01-A06 (Fixed Assets) | Required by law, monthly depreciation |
| 🔴 **P0.2** | G01-G04 (Period Closing) | Required for BCTC |
| 🟠 **P1.1** | X01-X05 (Tax) | Monthly VAT declaration |
| 🟠 **P1.2** | S01-S06 (Sales) | Revenue recognition |
| 🟡 **P2.1** | P01-P05 (Purchase) | Inventory costing |
| 🟡 **P2.2** | R01-R05 (Reports) | Financial statements |

---

## 📁 FILES REFERENCE

| Document | Location |
|----------|----------|
| Full Use Cases (TT99) | `docs/core_use_cases_TT99_2025_updated.md` |
| COA Use Cases | `docs/use_cases/coa_use_cases.md` |
| Payroll Use Cases | `docs/use_cases/laodong_tienluong.md` |
| Payroll Roadmap | `docs/roadmaps/laodong_tienluong_roadmap.md` |

---

*Consolidated from: core_use_cases_TT99_2025_updated.md, coa_use_cases.md, laodong_tienluong.md*