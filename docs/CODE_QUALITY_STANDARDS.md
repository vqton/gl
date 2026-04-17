# GL Accounting System - Code Quality Standards
*Author: Senior PM (20 years experience) | Updated: April 2026*

---

## Executive Summary

This document establishes code quality standards for the GL Accounting System. These standards ensure maintainability, reliability, and compliance with Vietnamese accounting regulations (TT99/2025).

**Principle**: Code is written once, read many times. Optimize for readability and maintainability.

---

## 1. Coding Standards

### 1.1 Language Conventions

| Rule | Standard | Rationale |
|------|----------|-----------|
| **Language** | C# 10+ with .NET 10 | Modern features, null safety |
| **Naming** | PascalCase for classes/methods, camelCase for variables | Industry standard |
| **Braces** | Allman style (newline for braces) | Better readability |
| **Indentation** | 4 spaces (no tabs) | Consistent across editors |
| **Line length** | Max 120 characters | Prevent horizontal scroll |

### 1.2 File Organization

```
src/
├── Application/
│   ├── DTOs/              # Data Transfer Objects
│   │   └── CommonDTOs.cs # Single file for common DTOs
│   └── Services/          # One class per file
│       └── [ServiceName]Service.cs
├── Domain/
│   ├── Entities/          # One entity per file
│   ├── Enums/             # One enum per file
│   └── Interfaces/        # Repository interfaces
└── Infrastructure/
    ├── Data/              # DbContext
    └── Repositories/      # Repository implementations
```

### 1.3 Class Structure

```csharp
// File: [ServiceName]Service.cs

namespace GL.Application.Services
{
    /// <summary>
    /// [Brief description of service purpose]
    /// </summary>
    public class [ServiceName]Service
    {
        // Private fields (only if needed)
        private readonly IRepository _repository;

        // Constructor with DI
        public [ServiceName]Service(IRepository repository)
        {
            _repository = repository;
        }

        // Public methods first
        /// <summary>
        /// [Verb] [Noun] - [Brief description]
        /// </summary>
        /// <param name="request">Request object</param>
        /// <returns>Result object</returns>
        public ReturnType MethodName(RequestType request)
        {
            // Guard clauses first
            if (request == null)
                throw new ArgumentNullException(nameof(request));

            // Business logic
            var result = DoSomething();

            return result;
        }

        // Private methods last
        private ReturnType DoSomething() { }
    }
}
```

---

## 2. Documentation Standards

### 2.1 Required XML Comments

**ALL public methods MUST have XML documentation:**

```csharp
/// <summary>
/// Creates a new journal entry for sales transactions
/// </summary>
/// <param name="request">Sales entry request containing customer and amount</param>
/// <returns>Created transaction with generated ID</returns>
/// <exception cref="ArgumentException">Thrown when amount is zero or negative</exception>
/// <remarks>
/// This method validates against TT99/2025 Article 15 requirements.
/// Must be called before COGS recognition.
/// </remarks>
public Transaction CreateSalesEntry(CreateSalesEntryRequest request)
```

### 2.2 Vietnamese Documentation

**For local team and Vietnamese compliance:**

```csharp
/// <summary>
/// Tạo bút toán kết chuyển doanh thu cuối kỳ
/// </summary>
/// <param name="request">Yêu cầu kết chuyển doanh thu</param>
/// <returns>Bút toán kết chuyển</returns>
/// <remarks>
/// Định khoản: Nợ 511 / Có 911 (doanh thu bán hàng)
/// Áp dụng Thông tư 99/2025/TT-BTC Điều 18
/// </remarks>
```

---

## 3. Error Handling

### 3.1 Exception Strategy

| Scenario | Approach |
|----------|-----------|
| Invalid input | `ArgumentException` / `ArgumentNullException` |
| Not found | `KeyNotFoundException` |
| Business rule violation | Custom exception with clear message |
| External system failure | Wrap in `InvalidOperationException` |

### 3.2 Error Message Format

```csharp
// WRONG ❌
throw new Exception("Error");

// CORRECT ✅
throw new ArgumentException(
    message: $"Account {accountCode} is not postable. Only level 3-4 accounts can be used for journaling. " +
             $"See TT99/2025 Article 17.",
    paramName: nameof(accountCode));
```

### 3.3 Never Swallow Exceptions

```csharp
// WRONG ❌
try { DoSomething(); }
catch { /* ignore */ }

// CORRECT ✅
try { DoSomething(); }
catch (Exception ex) 
{
    _logger.LogError(ex, "Failed to process transaction {TransactionId}", id);
    throw;
}
```

---

## 4. Testing Standards

### 4.1 Test Organization

```csharp
namespace GL.Domain.Tests
{
    /// <summary>
    /// Tests for [ServiceName]Service - [Module Code]
    /// </summary>
    public class [ServiceName]ServiceTests
    {
        private readonly [ServiceName]Service _service = new();
        
        // [Fact] or [Theory] for each use case
        [Fact]
        public void [UC-XXX]_[Scenario]_[ExpectedResult]()
        {
            // Arrange
            var request = new Request { ... };
            
            // Act
            var result = _service.Method(request);
            
            // Assert
            Assert.NotNull(result);
            Assert.True(result.IsValid);
        }
    }
}
```

### 4.2 Test Naming Convention

```
[UseCaseCode]_[Scenario]_[ExpectedResult]

Examples:
- S01_CreateCashSale_WithValidInput_ReturnsTransaction
- P02_CreatePurchase_WithVAT_CalculatesCorrectly
- AT01_LogTransaction_StoresUserAndTimestamp
- PL03_ValidatePeriod_ClosedPeriod_RejectsPosting
```

### 4.3 Test Coverage Requirements

| Module Type | Minimum Coverage |
|-------------|------------------|
| Core Services | 80% |
| Calculation Services | 90% |
| Compliance (Audit, Period) | 100% |
| Integration Points | 70% |

---

## 5. Security Standards

### 5.1 Sensitive Data

| Data Type | Handling |
|-----------|----------|
| Passwords | Never log, hash before storage |
| API Keys | Use secrets management |
| Financial amounts | Use `decimal` (never `double`) |
| Personal data (PII) | Encrypt at rest, mask in logs |

### 5.2 Input Validation

**Always validate at service boundary:**

```csharp
public Transaction CreateEntry(CreateEntryRequest request)
{
    // 1. Validate request object
    if (request == null)
        throw new ArgumentNullException(nameof(request));
    
    // 2. Validate business rules
    if (request.Amount <= 0)
        throw new ArgumentException("Amount must be positive", nameof(request.Amount));
    
    // 3. Validate against COA
    if (!_coaService.ValidateAccount(request.AccountCode).IsValid)
        throw new ArgumentException($"Invalid account: {request.AccountCode}");
    
    // Proceed with business logic
}
```

---

## 6. Performance Standards

### 6.1 Database Operations

| Rule | Standard |
|------|----------|
| Use async/await | Always for I/O operations |
| Connection pooling | Use default EF Core pooling |
| No N+1 queries | Use `.Include()` for navigation properties |
| Pagination | Always for lists > 100 items |

### 6.2 Memory Management

```csharp
// WRONG ❌ - Creates many allocations
var list = new List<string>();
foreach (var item in items) { list.Add(item); }

// CORRECT ✅ - Use collection expression
var list = items.ToList(); // or items.Select(...)
```

---

## 7. Code Review Checklist

### 7.1 Reviewer Must Verify

- [ ] Code follows naming conventions
- [ ] XML comments on all public methods
- [ ] Unit tests cover the changes
- [ ] Error handling is appropriate
- [ ] No secrets in code
- [ ] Business logic matches TT99/2025 requirements
- [ ] Changes don't break existing tests

### 7.2 Author Must Verify Before PR

- [ ] All tests pass locally
- [ ] Code builds without warnings
- [ ] No TODO comments remaining
- [ ] Self-review completed
- [ ] Branch is up-to-date with main

---

## 8. Version Control Standards

### 8.1 Commit Message Format

```
[type]: [short description]

[Long description if needed]

[Issue reference]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance

**Examples:**
```
feat: implement sales module S01-S06 with TDD

- Add SalesService with CreateCashSale, CreateCreditSale
- Add COGS calculation with FIFO method
- Add 18 unit tests

fix: correct VAT calculation for export sales

docs: update COA for TT99/2025 compliance
```

### 8.2 Branch Strategy

```
main (production-ready)
├── develop (integration)
│   ├── feature/S01-sales-module
│   ├── feature/P01-purchase-module
│   └── bugfix/fix-vat-calculation
└── hotfix/critical-security-patch
```

---

## 9. Deployment Standards

### 9.1 Environment Configuration

| Environment | Configuration |
|-------------|---------------|
| Development | Local MariaDB, debug logging |
| Staging | Local HA MariaDB, structured logging |
| Production | On-premises MariaDB, minimal logging, monitoring enabled |

### 9.2 Release Checklist

- [ ] All tests pass in CI
- [ ] Code review approved
- [ ] Integration tests pass
- [ ] Performance benchmarks met
- [ ] Security scan passed
- [ ] Database migrations tested
- [ ] Rollback plan documented

---

## 10. Metrics & KPIs

### 10.1 Quality Metrics

| Metric | Target | Critical |
|--------|--------|----------|
| Test Coverage | ≥ 80% | < 60% |
| Code Review Time | < 24 hours | > 48 hours |
| Bug Escape Rate | < 5% | > 15% |
| Technical Debt | < 10% of codebase | > 20% |

### 10.2 Delivery Metrics

| Metric | Target |
|--------|--------|
| Feature Delivery | 2-3 per sprint |
| Bug Fix Time | < 24 hours (critical) |
| Build Success Rate | > 95% |
| Deployment Frequency | Weekly |

---

## 11. Compliance Requirements

### 11.1 Accounting Standards

All code affecting financial calculations MUST:

1. Use `decimal` type (not `double` or `float`)
2. Implement proper rounding (2 decimal places for VND)
3. Support audit trail
4. Maintain transaction integrity
5. Comply with TT99/2025 article references in comments

### 11.2 Regulatory Compliance

| Requirement | Implementation |
|-------------|----------------|
| TT99/2025 | COA validation, journal entries |
| Data Retention | Audit logs, transaction history |
| Access Control | User/role management planned |
| Audit Trail | Phase 4 implemented |

---

## Quick Reference Card

| Category | Do | Don't |
|----------|-----|-------|
| Naming | `CreateSalesEntry` | `createSales`, `SalesEntry_Create` |
| Comments | XML docs for public APIs | Inline comments for obvious code |
| Errors | Meaningful messages | Generic "Error occurred" |
| Tests | One assert per test aspect | Multiple unrelated asserts |
| Commits | Atomic, descriptive | Mixed changes, "WIP" |

---

*Document Version: 1.0*
*Last Updated: April 2026*
*Next Review: Quarterly*