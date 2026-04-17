# GL Accounting System - System Design Document
*System Analyst: 20 Years Experience*
*Version: 1.0*
*Date: April 2026*

---

## 1. Executive Summary

This document outlines the comprehensive system design for GL Accounting System - a Vietnamese accounting software built on .NET Core 10, fully compliant with Thông tư 99/2025/TT-BTC. The system implements 22 core use cases covering the complete accounting cycle.

---

## 2. Architecture Overview

### 2.1 Technology Stack
- **Framework**: .NET 10 (LTS)
- **Database**: SQL Server 2022 (Primary) / MariaDB 10.x / PostgreSQL 16+ (Supported)
- **ORM**: Entity Framework Core 10 with provider switching
- **Frontend**: ASP.NET Core MVC + Bootstrap 5 + jQuery
- **Reporting**: FastReport.OpenSource 2026.2
- **Architecture**: Clean Architecture (3-layer)
- **Pattern**: Repository + Unit of Work
- **Testing**: xUnit with TDD methodology

### 2.2 Solution Structure (Clean Architecture)
```
src/
├── Domain/              # Domain Layer
│   ├── Entities/        # Account, Transaction
│   ├── Enums/           # AccountType
│   └── Interfaces/      # IAccountRepository, ITransactionRepository
├── Application/         # Business services, DTOs
├── Infrastructure/      # Data access (MySqlConnector)
└── WebApp/              # MVC + Bootstrap + FastReport

tests/
└── Domain.Tests/        # xUnit TDD tests
```

---

## 3. Domain Model Design

### 3.1 Core Entities

#### Account Entity
```csharp
public class Account {
    public string Code { get; set; }           // TT99: 111, 511, etc.
    public string Name { get; set; }           // Vietnamese name
    public AccountType Type { get; set; }      // Asset, Liability, Equity, Revenue, Expense
    public string NormalBalance { get; set; }  // Debit/Credit
    public string ParentCode { get; set; }     // Hierarchy
    public List<Account> Children { get; set; }
    public bool AllowPosting => Children.Count == 0;
}
```

#### AccountType Enum
```csharp
public enum AccountType {
    Asset = 1,      // Tài sản (1xxx)
    Liability = 2,  // Nợ phải trả (2xxx)
    Equity = 3,     // Vốn chủ sở hữu (3xxx)
    Revenue = 4,    // Doanh thu (5xxx)
    Expense = 5    // Chi phí (6xxx, 7xxx, 8xxx)
}
```

#### Transaction Entity (Sổ Chung/Journal Entry)
```csharp
public class Transaction {
    public string Id { get; set; }             // UUID
    public DateTime Date { get; set; }        // ngay_chung_tu_goc
    public string Description { get; set; }   // Diễn giải
    public List<TransactionLine> Lines { get; set; }
    
    // Double-entry validation
    public bool IsBalanced {
        get => Math.Abs(TotalDebit - TotalCredit) < 0.01m;
    }
}

public class TransactionLine {
    public string AccountCode { get; set; }   // TK cuối (TT99)
    public decimal DebitAmount { get; set; }  // Nợ
    public decimal CreditAmount { get; set; } // Có
    public string Description { get; set; }
}
```

---

## 4. TT99 Chart of Accounts Structure

### 4.1 71 Level-1 Accounts Summary

| Code | Name | Type | Normal |
|------|------|------|--------|
| 111 | Tiền mặt | Asset | Debit |
| 112 | Tiền gửi ngân hàng | Asset | Debit |
| 131 | Phải thu khách hàng | Asset | Debit |
| 133 | Thuế GTGT được khấu trừ | Asset | Debit |
| 151-157 | Hàng tồn kho | Asset | Debit |
| 211-214 | Tài sản cố định | Asset | Debit |
| 331 | Phải trả người bán | Liability | Credit |
| 333 | Thuế và các khoản phải nộp | Liability | Credit |
| 334 | Phải trả người lao động | Liability | Credit |
| 511-521 | Doanh thu | Revenue | Credit |
| 621-642 | Chi phí | Expense | Debit |
| 911 | Xác định kết quả | Expense/Revenue | Credit |

---

## 5. Use Case Implementation Map

### 5.1 22 Core Use Cases (TT99/2025)

| ID | Use Case | Domain | Priority |
|----|----------|--------|----------|
| S01 | Bán hàng thu tiền ngay | Sales | CORE |
| S02 | Bán hàng ghi công nợ | Sales | CORE |
| S03 | Ghi nhận giá vốn hàng bán | Sales | CORE |
| P01 | Mua hàng ghi công nợ | Purchase | CORE |
| P02 | Mua NVL ghi công nợ | Purchase | CORE |
| T01 | Thanh toán cho nhà cung cấp | Payment | CORE |
| T02 | Thu tiền từ khách hàng | Payment | CORE |
| X01 | Kê khai và nộp VAT | Tax | CORE |
| X02 | Ghi nhận CP thuế TNDN | Tax | CORE |
| X03 | Ghi nhận và nộp TNCN | Tax | CORE |
| A01 | Mua tài sản cố định | Asset | CORE |
| A02 | Khấu hao TSCĐ hàng tháng | Asset | CORE |
| L01 | Tính lương và phải trả | Payroll | CORE |
| L02 | Trích BHXH, BHYT, BHTN | Payroll | CORE |
| L03 | Thanh toán lương | Payroll | CORE |
| G01 | Kết chuyển doanh thu | Closing | CORE |
| G02 | Kết chuyển chi phí | Closing | CORE |
| G03 | Kết chuyển lợi nhuận | Closing | CORE |
| G04 | Phân bổ chi phí trả trước | Closing | CORE |

---

## 6. Validation Rules (Global)

### 6.1 Journal Entry Constraints
1. **Balance Rule**: SUM(debits) == SUM(credits) ± 0.01 VND
2. **Account Validation**: All account_code MUST exist in TT99 COA
3. **Period Validation**: accounting_period.status == "OPEN"
4. **Source Document**: MUST include so_chung_tu_goc AND ngay_chung_tu_goc

### 6.2 Business Rules
- **Double Entry**: Every transaction MUST have at least one debit AND one credit line
- **No Direct 911**: Revenue/expense accounts (5xx, 6xx, 7xx, 8xx) - only for period closing
- **VAT Handling**: VAT input (1331) and output (33311) MUST be tracked separately
- **Inventory Valuation**: Costing method (FIFO/Weighted Average) MUST be consistent

---

## 7. Database Schema Design

### 7.1 Core Tables

```sql
-- accounts: Danh mục tài khoản (TT99)
CREATE TABLE accounts (
    code VARCHAR(10) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type INT NOT NULL,          -- 1=Asset, 2=Liability, etc.
    normal_balance VARCHAR(10) NOT NULL,
    parent_code VARCHAR(10),
    level INT NOT NULL DEFAULT 1,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_code) REFERENCES accounts(code)
);

-- accounting_periods: Kỳ kế toán
CREATE TABLE accounting_periods (
    id VARCHAR(36) PRIMARY KEY,
    code VARCHAR(10) NOT NULL,  -- "2026-01"
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(10) NOT NULL, -- OPEN, CLOSED, LOCKED
    is_fiscal_year_end BOOLEAN DEFAULT FALSE
);

-- transactions: Sổ chung
CREATE TABLE transactions (
    id VARCHAR(36) PRIMARY KEY,
    entry_type VARCHAR(10) NOT NULL, -- S01, P01, etc.
    date DATE NOT NULL,
    description VARCHAR(500),
    period_id VARCHAR(36) NOT NULL,
    is_closing_entry BOOLEAN DEFAULT FALSE,
    status VARCHAR(10) DEFAULT 'POSTED',
    created_by VARCHAR(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (period_id) REFERENCES accounting_periods(id)
);

-- transaction_lines: Dòng sổ chung
CREATE TABLE transaction_lines (
    id VARCHAR(36) PRIMARY KEY,
    transaction_id VARCHAR(36) NOT NULL,
    account_code VARCHAR(10) NOT NULL,
    debit DECIMAL(18,2) DEFAULT 0,
    credit DECIMAL(18,2) DEFAULT 0,
    description VARCHAR(255),
    auxiliary JSON,
    FOREIGN KEY (transaction_id) REFERENCES transactions(id),
    FOREIGN KEY (account_code) REFERENCES accounts(code)
);
```

---

## 8. API/Controller Design

### 8.1 Account Controller
- GET /Account - Index (list all)
- GET /Account/Details/{code}
- GET /Account/Create
- POST /Account/Create
- GET /Account/Edit/{code}
- POST /Account/Edit/{code}
- GET /Account/Delete/{code}
- POST /Account/Delete/{code}
- GET /Account/Tree - JSON tree structure

### 8.2 Transaction Controller
- GET /Transaction - Index
- GET /Transaction/Create
- POST /Transaction/Create
- GET /Transaction/Details/{id}
- POST /Transaction/Validate - Validate balance

---

## 9. Security & Compliance

### 9.1 Audit Trail Requirements
- Every entry MUST log: created_by, created_at
- All changes tracked with timestamp
- Period closing prevents retroactive edits

### 9.2 TT99 Compliance
- All 71 level-1 accounts implemented
- All 22 core use cases supported
- Financial statements: BCĐKT, BCKQHĐKD

---

## 10. Development Phases

### Phase 1: Foundation (Current)
- [x] Core entities (Account, Transaction)
- [x] Repository pattern
- [x] Basic MVC setup
- [x] Unit tests (10 passing)

### Phase 2: Core Functionality
- [ ] Implement all 22 use cases
- [ ] DB schema implementation
- [ ] Import COA (71 accounts)
- [ ] Transaction posting

### Phase 3: Integration
- [ ] Report generation (FastReport)
- [ ] Period closing automation
- [ ] Financial statements

### Phase 4: Advanced
- [ ] Multi-currency
- [ ] Role-based access
- [ ] API for integration

---

## 11. Key Design Decisions

1. **Repository Pattern**: Decouple data access from business logic
2. **TDD Methodology**: Write tests first, implementation second
3. **Vietnamese Documentation**: All comments/docs in Vietnamese
4. **Cross-Platform**: .NET 8 ensures Linux/Windows compatibility
5. **Open Source**: FastReport.OpenSource for reporting

---

*Document prepared by System Analyst*
*For: GL Accounting System Development Team*
*Based on: Thông tư 99/2025/TT-BTC*
