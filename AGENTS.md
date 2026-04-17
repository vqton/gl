# GL Accounting System - Agent Guidance

## Solution Structure (Clean Architecture)
```
src/
├── Domain/           # Entities, Enums, Interfaces
│   ├── Entities/     # Account, Transaction
│   ├── Enums/        # AccountType
│   └── Interfaces/   # IAccountRepository, ITransactionRepository
├── Application/      # Business logic services, DTOs
│   ├── Services/      # 28+ services (Payroll, Bank, Tax, E-Invoice...)
│   └── DTOs/         # Record types with positional constructors
├── Infrastructure/   # Data access (MariaDB/SQL Server + EF Core)
│   ├── Data/          # GLDbContext
│   └── Repositories/  # Repository pattern
└── WebApp/           # ASP.NET Core MVC + SQL scripts
    ├── Controllers/  # API controllers
    └── sql/           # MariaDB schema + COA seed

tests/
└── Domain.Tests/    # xUnit tests (TDD) - 331 passing
```

## Essential Commands
**Build solution:**
```bash
dotnet build
```

**Run all tests:**
```bash
dotnet test
```

**Run specific test:**
```bash
dotnet test tests/Domain.Tests/GL.Domain.Tests.csproj
```

**Run web application:**
```bash
dotnet run --project src/WebApp/GL.WebApp.csproj
```

## Key Conventions
- Target framework: .NET 10 (LTS)
- Repository pattern used for data access
- **TDD approach: Always write tests before implementation**
- **DTOs use `record` types with positional constructors**
- **Always write docstring/XML comments in Vietnamese when possible**
- **Multi-database: MariaDB / PostgreSQL / SQL Server**
- Standard ASP.NET Core MVC structure

## Development Workflow
1. Write failing tests first (TDD)
2. Implement to pass tests
3. Run `dotnet build` then `dotnet test`
4. Commit changes with descriptive message

## Database Setup (Multi-Database)

### MariaDB:
```bash
systemctl start mariadb
mariadb -u root gl_accounting < src/WebApp/sql/001_schema.sql
mariadb -u root gl_accounting < src/WebApp/sql/002_coa_seed.sql
mariadb -u root gl_accounting -e "SHOW TABLES;"
```

### PostgreSQL:
```bash
psql -U postgres -c "CREATE DATABASE gl_accounting;"
psql -U postgres -d gl_accounting -f src/WebApp/sql/001_schema_pgsql.sql
psql -U postgres -d gl_accounting -f src/WebApp/sql/002_coa_seed.sql
```

### SQL Server:
```bash
sqlcmd -S localhost -U sa -i src/WebApp/sql/001_schema_sqlserver.sql
sqlcmd -S localhost -U sa -d gl_accounting -i src/WebApp/sql/002_coa_seed.sql
```

## Current Status (All Core Modules Complete)

### Implemented Modules
| Module | Code | Status |
|--------|------|--------|
| Payroll | L01-L07 | ✅ Complete |
| Fixed Assets | A01-A06 | ✅ Complete |
| Period Closing | G01-G04 | ✅ Complete |
| Cash & Bank | T01-T22, B01-B08 | ✅ Complete |
| Tax | X01-X05 | ✅ Complete |
| COA Validation | - | ✅ Complete |
| E-Invoice | EI01-EI07 | ✅ Complete |
| Inventory | I01-I07 | ✅ Complete |
| Cost Accounting | C01 | ✅ Complete |
| Subsidiary Ledgers | S01-S03 (131/331/156) | ✅ Complete |
| Audit Trail | AT01-AT03 | ✅ Complete |
| Period Locking | PL01-PL03 | ✅ Complete |
| GL Central Posting | G05 | ✅ Complete |

### Test Results
- **Total tests:** 331 passing
- **Failed:** 0
- **Build:** 0 errors

## Technology Stack
- .NET 10 (LTS)
- Entity Framework Core 10 (SQL Server provider)
- MariaDB 11.x / PostgreSQL 14+ / SQL Server 2019+
- FastReport.OpenSource 2026.2.0 (report generation)
- xUnit (testing)
- TT99/2025 Vietnamese Accounting Standards

## Key Files
```
src/Application/
├── Services/
│   ├── FastReportService.cs        # Report data layer
│   ├── EInvoiceService.cs        # E-Invoice integration
│   ├── PayrollCalculationService.cs
│   ├── BankService.cs
│   └── ... (28+ services)
└── DTOs/
    └── CommonDTOs.cs            # Record types

src/WebApp/sql/
├── 001_schema.sql             # Database tables
└── 002_coa_seed.sql         # Chart of Accounts (TT99/2025)
```

## Known Limitations
- EF Core migrations: Blocked by .NET 10 / Pomelo EF Core MySQL version mismatch
- Workaround: Use raw SQL scripts for MariaDB deployment

## Notes for AI Agent
- LSP errors are false positives - always verify with `dotnet build`
- Test failures indicate real issues - investigate with test output
- Use Vietnamese comments for domain-specific logic
- Follow TT99/2025 for accounting standards