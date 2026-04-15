# 📋 IMPLEMENTATION ROADMAP & EXECUTION PLAN
*Updated: April 2026 | Based on MASTER_USE_CASES.md & Gap Analysis*

---

## 🎯 IMPLEMENTATION STRATEGY

### TDD Methodology
```
1. Write failing tests first (TDD)
2. Implement to pass tests
3. Run: dotnet build && dotnet test
4. Commit with descriptive message
```

---

## 📊 PHASE IMPLEMENTATION PLAN

### PHASE 1: Critical Core (COMPLETED ✅)
| Week | Module | Use Cases | Deliverables | Tests |
|------|--------|-----------|-------------|-------|
| 1 | **Fixed Assets (A01-A06)** | A01-A06 | FixedAsset, FixedAssetService | 9 |
| 2 | **Period Closing (G01-G04)** | G01-G04 | PeriodClosingService | 8 |
| **Total** | | | **17 tests** | ✅ Pass |

---

### PHASE 2: Sales (CURRENT - Week 3)
| Week | Module | Use Cases | Deliverables | Tests | Status |
|------|--------|-----------|-------------|-------|--------|
| 3 | **Sales Documentation** | S01-S06 | sales_use_cases.md | ✅ Done |
| 3a | **S01: Bán tiền mặt** | S01 | SalesService.CreateCashSale | 3 | 🔄 Implementing |
| 3b | **S02: Bán chịu** | S02 | SalesService.CreateCreditSale | 3 | ⏳ Pending |
| 3c | **S03: Giá vốn** | S03 | SalesService.RecordCOGS | 3 | ⏳ Pending |
| 3d | **S04: Trả hàng** | S04 | SalesService.ProcessReturn | 3 | ⏳ Pending |
| 3e | **S05: Giảm giá** | S05 | SalesService.ApplyDiscount | 2 | ⏳ Pending |
| 3f | **S06: Chiết khấu TT** | S06 | SalesService.ApplyPaymentDiscount | 2 | ⏳ Pending |

**Target: 16 tests for Sales**

---

### PHASE 2b: Purchase Documentation (Week 4)
| Week | Module | Use Cases | Deliverables | Tests | Status |
|------|--------|-----------|-------------|-------|--------|
| 4 | **Purchase Documentation** | P01-P06 | purchase_use_cases.md | ✅ Done |

---

### PHASE 3: Purchase Implementation (Week 5)
| Week | Module | Use Cases | Deliverables | Tests |
|------|--------|-----------|-------------|-------|
| 5 | **P01-P05** | Purchase Orders, Inventory, Returns | PurchaseService | 16 |

---

### PHASE 4: Cash & Bank (Week 6)
| Week | Module | Use Cases | Deliverables |
|------|--------|-----------|--------------|
| 6 | **T01-T05** | Payments, Receipts, Transfers | CashService |

---

### PHASE 5: Tax & Reporting (Week 7-8)
| Week | Module | Use Cases | Deliverables |
|------|--------|-----------|--------------|
| 7 | **Tax (X01-X05)** | VAT, PIT, FCT | TaxService |
| 8 | **Reports (R01-R03)** | Trial Balance, Income Statement | ReportService |
| 8 | **Reports** | B01-B03 | ReportService |

---

## 📅 GANTT CHART

```
Week:    1   2   3   4   5   6   7   8
        |---|---|---|---|---|---|---|---|
Phase1   ████████                    DONE ✅
Phase2           ████████              IN PROGRESS
Phase3                       ████████
Phase4                       ████████
Phase5                               ██████████
```

---

## 🔧 SALES (S01-S06) IMPLEMENTATION DETAILS

### Entity: SalesTransaction.cs
```csharp
public class SalesTransaction
{
    public string Id { get; set; }
    public string TransactionNo { get; set; }
    public DateTime TransactionDate { get; set; }
    public SalesType Type { get; set; }  // Cash, Credit
    public string CustomerId { get; set; }
    public string CustomerName { get; set; }
    
    // Items
    public List<SalesLine> Lines { get; set; }
    
    // Totals
    public decimal SubTotal { get; set; }
    public decimal VATAmount { get; set; }
    public decimal TotalAmount { get; set; }
    public decimal COGS { get; set; }  // Giá vốn
    
    // Status
    public SalesStatus Status { get; set; }
    public PaymentStatus PaymentStatus { get; set; }
}

public class SalesLine
{
    public string ProductId { get; set; }
    public string ProductName { get; set; }
    public decimal Quantity { get; set; }
    public decimal UnitPrice { get; set; }
    public decimal DiscountPercent { get; set; }
    public decimal DiscountAmount { get; set; }
    public decimal LineTotal { get; set; }
}

public enum SalesType
{
    Cash,           // Bán tiền mặt
    Credit,         // Bán chịu
    Installment,    // Bán trả góp
    Consignment     // Bán đại lý
}

public enum SalesStatus
{
    Draft,
    PendingPayment,
    Paid,
    PartiallyPaid,
    Overdue,
    Returned,
    Cancelled
}
```

### Service: SalesService.cs (Required Methods)
```csharp
public class SalesService
{
    // S01: Bán tiền mặt
    (bool, SalesTransaction) CreateCashSale(CreateSaleInput input);
    
    // S02: Bán chịu
    (bool, SalesTransaction) CreateCreditSale(CreateSaleInput input);
    
    // S03: Ghi nhận giá vốn
    (bool, string) RecordCOGS(string transactionId, string productId, decimal quantity);
    
    // S04: Xử lý trả hàng
    (bool, SalesTransaction) ProcessReturn(string transactionId, ReturnInput input);
    
    // S05: Giảm giá hàng bán
    (bool, string) ApplyDiscount(string transactionId, decimal discountAmount);
    
    // S06: Chiết khấu thanh toán
    (bool, string) ApplyPaymentDiscount(string transactionId, decimal discountPercent);
    
    // Queries
    SalesTransaction GetById(string id);
    IEnumerable<SalesTransaction> GetByCustomer(string customerId);
    IEnumerable<SalesTransaction> GetOverdueSales();
}
```

### Journal Entry Mapping
| Use Case | Debit | Credit |
|----------|-------|--------|
| S01: Bán tiền mặt | 111/112 | 511, 33311 |
| S02: Bán chịu | 131 | 511, 33311 |
| S03: Giá vốn | 632 | 156/155 |
| S04a: Trả hàng | 5212, 3331 | 131/111 |
| S04b: Điều chỉnh giá vốn | 156/155 | 632 |
| S05: Giảm giá | 5211 | 131/111 |
| S06: Chiết khấu TT | 111, 5213 | 131 |

---

## 📋 TEST CASES (TDD)

```csharp
[Fact]
public void S01_CreateCashSale_BalancesCorrectly()
{
    // Test: Tổng Nợ = Tổng Có
}

[Fact]
public void S01_CreateCashSale_WithVAT_10Percent()
{
    // Test: VAT = 10% của doanh thu
}

[Fact]
public void S02_CreateCreditSale_SetsOverdueAfter30Days()
{
    // Test: PaymentStatus tự động overdue sau 30 ngày
}

[Fact]
public void S03_RecordCOGS_FIFO_CalculatesCorrectly()
{
    // Test: Tính giá xuất kho FIFO
}

[Fact]
public void S03_RecordCOGS_WeightedAverage_CalculatesCorrectly()
{
    // Test: Tính giá xuất kho bình quân
}

[Fact]
public void S04_ProcessReturn_ReducesRevenue()
{
    // Test: Doanh thu giảm qua 5212
}

[Fact]
public void S04_ProcessReturn_AdjustsCOGS()
{
    // Test: Giá vốn được điều chỉnh
}

[Fact]
public void S05_ApplyDiscount_ValidAmount()
{
    // Test: Giảm giá <= 20% giá trị
}

[Fact]
public void S06_ApplyPaymentDiscount_CalculatesCorrectly()
{
    // Test: Chiết khấu = số tiền × tỷ lệ
}
```

---

## 📈 SUCCESS METRICS

| Metric | Target | Current |
|--------|--------|---------|
| Test Coverage | ≥ 80% | 67% |
| Modules Implemented | 10/10 | 4/10 |
| Use Cases Complete | 50+ | 27 |
| Build Warnings | < 50 | 70 |
| All Tests Pass | 200+ | 169 |

---

## 🚦 GETTING STARTED

```bash
# Build solution
dotnet build

# Run all tests
dotnet test

# Run Sales tests only
dotnet test tests/Domain.Tests/GL.Domain.Tests.csproj --filter "Sales"

# Run with coverage
dotnet test --collect:"XPlat Code Coverage"
```

---

## 📁 FILES STRUCTURE

```
src/
├── Domain/
│   └── Entities/
│       ├── SalesTransaction.cs    ← NEW
│       ├── FixedAsset.cs        ← Existing
│       └── AccountingPeriod.cs  ← Existing
├── Application/
│   └── Services/
│       ├── SalesService.cs       ← NEW
│       ├── FixedAssetService.cs   ← Existing
│       └── PeriodClosingService.cs ← Existing
└── tests/
    └── Domain.Tests/
        ├── SalesTests.cs          ← NEW
        ├── FixedAssetTests.cs    ← Existing
        └── PeriodClosingTests.cs  ← Existing
```

---

*Roadmap updated based on: MASTER_USE_CASES.md*  
*Last updated: April 2026*