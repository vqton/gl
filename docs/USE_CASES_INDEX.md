# GL ACCOUNTING SYSTEM - USE CASE DOCUMENTS INDEX
*Consolidated: April 2026*

---

## MASTER DOCUMENTS

| File | Description | Priority |
|------|------------|----------|
| `GL_USE_CASES_MASTER.md` | **Main master document** | Primary |
| `GL_USE_CASES_CONSOLIDATED.md` | Phase-based overview | Reference |

---

## MODULE USE CASES

| File | Module | Codes |
|------|--------|-------|
| `use_cases/coa_use_cases.md` | Chart of Accounts | COA |
| `use_cases/sales_use_cases.md` | Sales | S01-S06 |
| `use_cases/purchase_use_cases.md` | Purchase | P01-P05 |
| `use_cases/cash_use_cases.md` | Cash | T01-T22 |
| `use_cases/bank_use_cases.md` | Bank | B01-B08 |
| `use_cases/inventory_use_cases.md` | Inventory | I01-I07 |
| `use_cases/fixed_asset_use_cases.md` | Fixed Assets | A01-A06 |
| `use_cases/payroll_use_cases.md` | Payroll | L01-L07 |
| `use_cases/einvoice_use_cases.md` | E-Invoice | EI01-EI07 |
| `use_cases/audit_period_use_cases.md` | Period Closing + Audit | G01-G04 |
| `use_cases/usecases_inventory_costing_20260417.md` | Inventory Costing | I05a-I05f |
| `use_cases/usecases_general_journal_20260417.md` | General Journal (NKC) | NKC-01 to NKC-06 |

---

## TAX

| File | Module |
|------|--------|
| `TAX_USE_CASES.md` | Tax (X01-X05) |

---

## REFERENCE DOCUMENTS

| File | Description |
|------|-------------|
| `ROADMAP.md` | System roadmap |
| `PRODUCTION_READINESS.md` | Production assessment |
| `CODE_QUALITY_STANDARDS.md` | Quality standards |
| `design/SYSTEM_DESIGN.md` | Architecture design |
| `GAP_ANALYSIS.md` | Gap analysis & missing flows |

---

## IMPLEMENTATION STATUS

| Module | Tests | Status |
|--------|-------|--------|
| SalesService | 18 | ✅ |
| PurchaseService | 15 | ✅ |
| CashService | 25 | ✅ |
| BankService | 11 | ✅ |
| InventoryService | 11 | ✅ |
| FixedAssetService | 22 | ✅ |
| PayrollCalculationService | 35 | ✅ |
| TaxService | 12 | ✅ |
| TransactionService | 8 | ✅ |
| GLCentralPostingService | 6 | ✅ |
| CostAccountingService | 6 | ✅ |
| SubsidiaryLedgerService | 9 | ✅ |
| InventoryCostingService | 7 | ✅ |
| **Total** | **338** | ✅ |

---

*Last Updated: April 2026*