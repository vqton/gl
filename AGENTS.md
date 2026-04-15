# GL Accounting System - Agent Guidance

## Solution Structure (Clean Architecture)
```
src/
├── Domain/           # Entities, Enums, Interfaces
│   ├── Entities/     # Account, Transaction
│   ├── Enums/        # AccountType
│   └── Interfaces/   # IAccountRepository, ITransactionRepository
├── Application/      # Business logic services, DTOs
├── Infrastructure/   # Data access (MySqlConnector)
└── WebApp/           # ASP.NET Core MVC (Bootstrap, jQuery, FastReport)

tests/
└── Domain.Tests/    # xUnit tests (TDD)
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
- **Always write docstring/XML comments in Vietnamese when possible**
- Standard ASP.NET Core MVC structure

## Development Workflow
1. Write failing tests first (TDD)
2. Implement to pass tests
3. Run `dotnet build` then `dotnet test`
4. Commit changes with descriptive message
5. Push to GitHub when possible

## MariaDB Setup
- Uses MySqlConnector package for MariaDB connectivity
- Update connection string in `src/WebApp/appsettings.json` before running

## Current Status (COA Module Complete)
- Core entities: Account, AccountType, Transaction, TransactionLine
- Modules implemented:
  - **Payroll** (L01-L07) ✅ Complete
  - **Fixed Assets** (A01-A06) ✅ Complete
  - **Period Closing** (G01-G04) ✅ Complete
  - **Cash & Bank** (T01-T22) ✅ Complete
  - **Tax** (X01-X05) ✅ Complete
  - **COA Validation** ✅ Complete
- Tests: 255 passing (all modules)