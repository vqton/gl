# 📋 IMPLEMENTATION ROADMAP
*Based on: USE_CASES_SUMMARY.md*
*Execution Plan for GL Accounting System*

---

## 🎯 IMPLEMENTATION STRATEGY

### Phased Approach (TDD Methodology)
1. **Write failing tests first** (TDD)
2. **Implement to pass tests**
3. **Run:** `dotnet build && dotnet test`
4. **Commit** with descriptive message

---

## 📊 PHASE IMPLEMENTATION PLAN

### PHASE 1: Critical Core (Week 1-2)
**Priority: 🔴 P0 - Must Have**

| Week | Module | Use Cases | Deliverables | Files to Create |
|------|--------|-----------|--------------|-----------------|
| 1 | **A01-A06: Fixed Assets** | A01, A02, A03, A04 | Asset entity, Depreciation service | `FixedAsset.cs`, `FixedAssetService.cs` |
| 1 | Tests | A01-A06 (7 tests) | Unit tests | `FixedAssetTests.cs` |
| 2 | **G01-G04: Period Closing** | G01, G02, G03, G04 | Closing service | `PeriodClosingService.cs` |
| 2 | Tests | G01-G04 (8 tests) | Unit tests | `PeriodClosingTests.cs` |

**Success Criteria:** 
- Assets can be added with depreciation calculated monthly
- Period closing entries (911) are generated correctly

---

### PHASE 2: Accounting Foundation (Week 3-4)
**Priority: 🟠 P1 - Important**

| Week | Module | Use Cases | Deliverables |
|------|--------|-----------|--------------|
| 3 | **Tax (X01-X05)** | X01, X02, X03, X04 | VAT service, Tax declaration |
| 3 | Tests | X01-X05 (5 tests) | `TaxTests.cs` |
| 4 | **Sales (S01-S06)** | S01, S02, S03, S04, S05 | Sales service, Returns |
| 4 | Tests | S01-S06 (6 tests) | `SalesTests.cs` |

---

### PHASE 3: Inventory & Payments (Week 5-6)
**Priority: 🟠 P1 - Important**

| Week | Module | Use Cases | Deliverables |
|------|--------|-----------|--------------|
| 5 | **Purchase (P01-P05)** | P01, P02, P03, P04, P05 | Purchase service |
| 5 | Tests | P01-P05 (5 tests) | `PurchaseTests.cs` |
| 6 | **Cash (T01-T05)** | T01, T02, T03, T04, T05 | Cash service |
| 6 | Tests | T01-T05 (5 tests) | `CashTests.cs` |

---

### PHASE 4: Reporting (Week 7-8)
**Priority: 🟡 P2 - Standard**

| Week | Module | Use Cases | Deliverables |
|------|--------|-----------|--------------|
| 7 | **Reports (R01-R05)** | R01, R02, R03 | Trial balance, Income statement, Cash flow |
| 7 | Tests | R01-R03 (3 tests) | `ReportTests.cs` |
| 8 | **Audit Trail (AT01-AT03)** | AT01, AT02, AT03 | Complete audit trail |
| 8 | Tests | AT01-AT03 (3 tests) | `AuditTrailTests.cs` |

---

### PHASE 5: Integration & Polish (Week 9-10)
**Priority: 🟢 P3 - Enhancement**

| Week | Module | Deliverables |
|------|--------|-------------|
| 9 | COA Validation Service | Complete account validation |
| 9 | Import/Export COA | `ImportExportCOAService.cs` |
| 10 | Integration Testing | Full workflow tests |
| 10 | Performance Optimization | Caching, indexes |

---

## 📅 GANTT CHART

```
Week:    1   2   3   4   5   6   7   8   9   10
        |---|---|---|---|---|---|---|---|---|
P0:     ████████
P1:             ████████████████
P2:                             ████████
P3:                                     ████
```

---

## 🔧 IMPLEMENTATION DETAILS

### Phase 1: Fixed Assets (A01-A06)

#### Entity: FixedAsset.cs
```csharp
public class FixedAsset
{
    public string Id { get; set; }
    public string AssetCode { get; set; }
    public string AssetName { get; set; }
    public string AssetType { get; set; }  // 211=TSCĐ, 213=BTHD, 217=CCDC
    public decimal OriginalCost { get; set; }
    public decimal AccumulatedDepreciation { get; set; }
    public decimal NetBookValue { get; set; }
    public DateTime PurchaseDate { get; set; }
    public int UsefulLifeYears { get; set; }
    public decimal DepreciationRate { get; set; }
    public DepreciationMethod Method { get; set; }  // Straight-line, Declining
    public FixedAssetStatus Status { get; set; }
}
```

#### Service: FixedAssetService.cs
```csharp
public class FixedAssetService
{
    // A01: Add new asset
    public (bool, FixedAsset) AddAsset(AddAssetInput input);
    
    // A02: Calculate monthly depreciation
    public (bool, decimal) CalculateMonthlyDepreciation(string assetId);
    
    // A03: Transfer asset between departments
    public (bool, string) TransferAsset(string assetId, string newDepartment);
    
    // A04: Dispose asset
    public (bool, string) DisposeAsset(string assetId, decimal proceeds);
}
```

#### Tests: FixedAssetTests.cs
```csharp
[Fact]
public void AddAsset_ValidAsset_ReturnsSuccess() { }

[Fact]
public void CalculateDepreciation_StraightLine_ReturnsCorrect()
{
    // Annual depreciation = Cost / Useful Life
    // Monthly = Annual / 12
}

[Fact]
public void CalculateDepreciation_DecliningBalance_ReturnsCorrect()
{
    // Rate = 1 / Useful Life * 2
    // Year N = Book Value * Rate
}

[Fact]
public void DisposeAsset_WriteOff_ReturnsCorrectJournalEntry()
{
    // Nợ 811: Giá trị còn lại
    // Nợ 214: Khấu hao lũy kế
    // Có 211: Nguyên giá
}
```

---

### Phase 1: Period Closing (G01-G04)

#### Service: PeriodClosingService.cs
```csharp
public class PeriodClosingService
{
    // G01: Kết chuyển doanh thu về 911
    public (bool, JournalEntry) CloseRevenue(int year, int month);
    
    // G02: Kết chuyển chi phí về 911
    public (bool, JournalEntry) CloseExpenses(int year, int month);
    
    // G03: Kết chuyển lợi nhuận sau thuế
    public (bool, JournalEntry) CloseProfit(int year);
    
    // G04: Phân bổ chi phí trả trước
    public (bool, JournalEntry) AllocatePrepaid(int year, int month);
    
    // Lock period (prevent further posting)
    public (bool, string) ClosePeriod(int year, int month);
}
```

#### Journal Entry Rules (G01)
```
Entry: Nợ 511 → Có 911 (tổng doanh thu)
      Nợ 515 → Có 911 (doanh thu tài chính)  
      Nợ 711 → Có 911 (thu nhập khác)
```

#### Journal Entry Rules (G02)
```
Entry: Nợ 911 → Có 632 (giá vốn)
      Nợ 911 → Có 641 (chi phí bán hàng)
      Nợ 911 → Có 642 (chi phí QLDN)
      Nợ 911 → Có 635 (chi phí tài chính)
      Nợ 911 → Có 811 (chi phí khác)
      Nợ 911 → Có 821 (thuế TNDN)
```

#### Tests: PeriodClosingTests.cs
```csharp
[Fact]
public void G01_CloseRevenue_Balances911()
{
    // Total 511 + 515 + 711 = 911 credit
}

[Fact]
public void G02_CloseExpenses_Balances911()
{
    // 911 debit = Total 632 + 641 + 642 + 635 + 811 + 821
}

[Fact]
public void G03_CloseProfit_ProfitTransferredTo4212()
{
    // If 911 credit > 0: Nợ 911 → Có 4212
    // If 911 debit > 0: Nợ 4212 → Có 911
}

[Fact]
public void ClosePeriod_PreventsFurtherPosting()
{
    // Period status = CLOSED
}
```

---

## 📋 EXECUTION CHECKLIST

### Before Starting Each Module

- [ ] Run `dotnet test` - verify all tests pass
- [ ] Review TT99 documentation  
- [ ] Check existing entities/services
- [ ] Write failing tests (TDD)
- [ ] Implement service
- [ ] Run `dotnet build && dotnet test`
- [ ] Fix any failing tests
- [ ] Review code coverage

### Naming Conventions

| Item | Convention | Example |
|------|-----------|---------|
| Entity | `EntityName.cs` | `FixedAsset.cs` |
| Service | `EntityNameService.cs` | `FixedAssetService.cs` |
| Tests | `EntityNameTests.cs` | `FixedAssetTests.cs` |
| Repository | `IEntityNameRepository` | `IFixedAssetRepository` |

---

## 📈 SUCCESS METRICS

| Metric | Target |
|--------|--------|
| Test Coverage | ≥ 80% |
| Modules Implemented | 10/10 |
| Use Cases Complete | 50+/50 |
| Build Warnings | < 50 |
| All Tests Pass | 200+ |

---

## 🗂️ FILE STRUCTURE TO CREATE

```
src/
├── Domain/
│   └── Entities/
│       ├── FixedAsset.cs          ← NEW
│       └── AccountingPeriod.cs   ← Existing
├── Application/
│   └── Services/
│       ├── FixedAssetService.cs  ← NEW
│       └── PeriodClosingService.cs ← NEW
└── tests/
    └── Domain.Tests/
        ├── FixedAssetTests.cs     ← NEW
        └── PeriodClosingTests.cs ← NEW
```

---

## 🚦 GETTING STARTED

Run these commands when implementing:

```bash
# Build solution
dotnet build

# Run all tests
dotnet test

# Run specific test file
dotnet test tests/Domain.Tests/GL.Domain.Tests.csproj --filter "FixedAsset"

# Run with coverage
dotnet test --collect:"XPlat Code Coverage"
```

---

*Roadmap created based on: USE_CASES_SUMMARY.md*  
*Last updated: April 2026*