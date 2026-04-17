# GL Accounting System

Hệ thống kế toán tài chính doanh nghiệp tuân thủ Thông tư 99/2025/TT-BTC.

## Mô tả

Hệ thống kế toán tổng hợp (General Ledger) cho doanh nghiệp Việt Nam, triển khai on-premises.

## Tính năng

- **Kế toán tổng hợp** - Hạch toán định khoản, sổ cái, báo cáo tài chính
- **Bán hàng** - Quản lý doanh thu, công nợ phải thu (TT99 loại 1)
- **Mua hàng** - Quản lý chi phí, công nợ phải trả (TT99 loại 2)
- **Tiền mặt & Ngân hàng** - Quản lý quỹ, ngân hàng (TT99 loại 1)
- **Tài sản cố định** - Tính khấu hao, quản lý TSCĐ (TT99 loại 2)
- **Kho hàng** - Quản lý tồn kho, giá xuất (TT99 loại 1)
- **Lao động - Tiền lương** - Tính lương, BHXH, thuế TNCN (TT99 loại 6)
- **Thuế** - GTGT, TNDN, hóa đơn điện tử (TT99 loại 4)
- **Đóng sổ kỳ kế toán** - Kết chuyển, lập báo cáo
- **Kiểm toán** - Audit trail, period locking
- **User Management** - ASP.NET Core Identity
- **Multi-Database** - MariaDB, PostgreSQL, SQL Server

## Chuẩn kế toán

- **TT99/2025/TT-BTC** - Chế độ kế toán doanh nghiệp
- **VAS** - Vietnam Accounting Standards

## Công nghệ

| Thành phần | Công nghệ |
|-----------|-----------|
| Runtime | .NET 10 LTS |
| Database | MariaDB / PostgreSQL / SQL Server |
| ORM | Entity Framework Core 10 |
| Authentication | ASP.NET Core Identity |
| Reports | FastReport.OpenSource |
| Testing | xUnit |

## Multi-Database Support

Hỗ trợ 3 database phổ biến cho on-premises:

- **MariaDB 11.x** - MySQL compatible, Linux/Windows
- **PostgreSQL 14+** - Enterprise grade, Linux/Windows
- **SQL Server 2019+** - Windows enterprise (phổ biến tại VN)

### Chuyển đổi Database

Edit `appsettings.json`:

```json
{
  "DatabaseProvider": "MariaDB",  // or "PostgreSQL" or "SqlServer"
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Port=3306;Database=gl_accounting;User=root;Password=;",
    "PostgreSQL": "Host=localhost;Port=5432;Database=gl_accounting;Username=postgres;Password=;",
    "SqlServer": "Server=localhost,1433;Database=GL_Accounting;User=sa;Password=;"
  }
}
```

## Cài đặt

### Yêu cầu

- .NET 10 SDK
- MariaDB 11.x / PostgreSQL 14+ / SQL Server 2019+
- Linux/macOS/Windows

### Các bước

```bash
# Clone và build
dotnet build

# Khởi tạo database (chọn 1 trong 3)
# MariaDB
mariadb -u root -p gl < src/WebApp/sql/001_schema.sql

# PostgreSQL
psql -U postgres -d gl_accounting -f src/WebApp/sql/001_schema_pgsql.sql

# SQL Server
sqlcmd -S localhost -U sa -i src/WebApp/sql/001_schema_sqlserver.sql

# Seed COA (chung cho tat ca)
mariadb -u root -p gl < src/WebApp/sql/002_coa_seed.sql

# Seed roles & users
mariadb -u root -p gl < src/WebApp/sql/003_permissions_seed.sql

# Chạy ứng dụng
dotnet run --project src/WebApp/GL.WebApp.csproj
```

## SME User Roles

| Role | Username | Description |
|------|----------|-------------|
| ADMIN | admin | Quản trị - Full system |
| ACCOUNTANT | ketoan | Kế toán - Full accounting |
| BOOKKEEPER | mayke | Kế toán máy - Data entry |
| SALES | kinhdoanh | Kinh doanh - Sales |
| WAREHOUSE | kho | Kho - Inventory |
| VIEWER | viewer | Xem báo cáo - Read only |

**Default password**: GL@2026!

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - Login

### User Management
- `GET /api/v1/usermanagement` - List users
- `POST /api/v1/usermanagement` - Create user
- `PUT /api/v1/usermanagement/{id}` - Update user
- `DELETE /api/v1/usermanagement/{id}` - Delete user
- `POST /api/v1/usermanagement/{id}/change-password` - Change password

### Database Configuration
- `GET /api/v1/databaseconfig` - List database configs
- `POST /api/v1/databaseconfig/switch` - Switch database

### Accounting
- `/api/v1/accounts` - Tài khoản kế toán
- `/api/v1/transactions` - Bút toán
- `/api/v1/payrolls` - Tính lương
- `/api/v1/assets` - Tài sản cố định
- `/api/v1/invoices` - Hóa đơn điện tử
- `/api/v1/reports` - Báo cáo tài chính

## Triển khai On-Premises

### Linux (Nginx + systemd)

```bash
# Build release
dotnet publish -c Release -o /var/www/gl-accounting
```

### Windows (IIS)

```bash
# Build release
dotnet publish -c Release -o C:\inetpub\gl-accounting
```

## Kiểm thử

```bash
dotnet test
# Result: 331 tests passing
```

## Cấu trúc dự án

```
src/
├── Domain/           # Entities, Enums, Interfaces
├── Application/     # Business logic services
├── Infrastructure/  # Data access (EF Core)
└── WebApp/           # ASP.NET Core MVC + SQL scripts

tests/
└── Domain.Tests/     # xUnit tests
```

## Giấy phép

MIT License