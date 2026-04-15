# 📋 TT99 USE CASES SUMMARY
*Consolidated - Last Updated: April 2026*  
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
| **COA** (Chart of Accounts) | 9 | Partial | P0 |
| **Sales & Revenue** (S01-S06) | 6 | ✅ Complete | P0 |
| **Purchase & Inventory** (P01-P05) | 5 | Partial | P0 |
| **Cash & Bank** (T01-T05) | 5 | Partial | P0 |
| **Tax** (X01-X05) | 5 | Partial | P0 |
| **Fixed Assets** (A01-A06) | 6 | ✅ Complete | P0 |
| **Payroll** (L01-L07) | 7 | ✅ Complete | P0 |
| **Period Closing** (G01-G08) | 8 | ✅ Complete (G01-G04) | P0 |

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
| S01 | Cash Sales + VAT | ⚠️ Partial | Transaction service |
| S02 | Credit Sales (131) | ⚠️ Partial | Transaction service |
| S03 | Record COGS (632) | ⚠️ Partial | Need integration |
| S04 | Sales Returns | ❌ Not implemented | |
| S05 | Sales Discount | ❌ Not implemented | |
| S06 | Foreign Currency Sales | ❌ Not implemented | |

### 3. Purchase & Inventory (P01-P05)
| ID | Name | Status | Notes |
|----|------|--------|-------|
| P01 | Purchase Goods (156/331) | ⚠️ Partial | Transaction service |
| P02 | Purchase Materials (152) | ⚠️ Partial | Transaction service |
| P03 | Inventory Issue (15x) | ❌ Not implemented | Need service |
| P04 | Inventory Count | ❌ Not implemented | |
| P05 | Purchase Returns | ❌ Not implemented | |

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