-- =====================================================
-- GL Accounting System - MariaDB Schema Script
-- Generated: 2026-04-16
-- Compatible: MariaDB 11.x
-- =====================================================

USE gl_accounting;

-- =====================================================
-- ASP.NET Core Identity Tables
-- =====================================================
CREATE TABLE IF NOT EXISTS AspNetUsers (
    Id VARCHAR(50) PRIMARY KEY,
    UserName VARCHAR(256),
    NormalizedUserName VARCHAR(256),
    Email VARCHAR(256),
    NormalizedEmail VARCHAR(256),
    EmailConfirmed TINYINT(1) NOT NULL DEFAULT 0,
    PasswordHash VARCHAR(255),
    SecurityStamp VARCHAR(255),
    ConcurrencyStamp VARCHAR(255),
    PhoneNumber VARCHAR(20),
    PhoneNumberConfirmed TINYINT(1) NOT NULL DEFAULT 0,
    TwoFactorEnabled TINYINT(1) NOT NULL DEFAULT 0,
    LockoutEnd DATETIME(6),
    LockoutEnabled TINYINT(1) NOT NULL DEFAULT 0,
    AccessFailedCount INT NOT NULL DEFAULT 0,
    FullName VARCHAR(100),
    IsActive TINYINT(1) NOT NULL DEFAULT 1,
    LastLoginAt DATETIME(6),
    Department VARCHAR(100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS AspNetRoles (
    Id VARCHAR(50) PRIMARY KEY,
    Name VARCHAR(256),
    NormalizedName VARCHAR(256),
    ConcurrencyStamp VARCHAR(255),
    Description VARCHAR(200)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS AspNetUserRoles (
    UserId VARCHAR(50) NOT NULL,
    RoleId VARCHAR(50) NOT NULL,
    PRIMARY KEY (UserId, RoleId),
    FOREIGN KEY (UserId) REFERENCES AspNetUsers(Id) ON DELETE CASCADE,
    FOREIGN KEY (RoleId) REFERENCES AspNetRoles(Id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS AspNetUserClaims (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    UserId VARCHAR(50) NOT NULL,
    ClaimType TEXT,
    ClaimValue TEXT,
    FOREIGN KEY (UserId) REFERENCES AspNetUsers(Id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS AspNetRoleClaims (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    RoleId VARCHAR(50) NOT NULL,
    ClaimType TEXT,
    ClaimValue TEXT,
    FOREIGN KEY (RoleId) REFERENCES AspNetRoles(Id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS AspNetUserLogins (
    LoginProvider VARCHAR(50) NOT NULL,
    ProviderKey VARCHAR(50) NOT NULL,
    ProviderDisplayName VARCHAR(100),
    UserId VARCHAR(50) NOT NULL,
    PRIMARY KEY (LoginProvider, ProviderKey),
    FOREIGN KEY (UserId) REFERENCES AspNetUsers(Id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS AspNetUserTokens (
    UserId VARCHAR(50) NOT NULL,
    LoginProvider VARCHAR(50) NOT NULL,
    Name VARCHAR(50) NOT NULL,
    Value TEXT,
    PRIMARY KEY (UserId, LoginProvider, Name),
    FOREIGN KEY (UserId) REFERENCES AspNetUsers(Id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Seed roles - SME Recommended (6 roles for small business)
INSERT INTO AspNetRoles (Id, Name, NormalizedName, Description) VALUES
('role_admin', 'ADMIN', 'ADMIN', 'Quản trị - Full system (chủ doanh nghiệp)'),
('role_accountant', 'ACCOUNTANT', 'ACCOUNTANT', 'Kế toán - Full accounting + reports'),
('role_bookkeeper', 'BOOKKEEPER', 'BOOKKEEPER', 'Kế toán máy - Nhập liệu'),
('role_sales', 'SALES', 'SALES', 'Kinh doanh - Bán hàng + KH'),
('role_warehouse', 'WAREHOUSE', 'WAREHOUSE', 'Kho - Nhập xuất kho'),
('role_viewer', 'VIEWER', 'VIEWER', 'Xem báo cáo - Read only')
ON DUPLICATE KEY UPDATE Description = VALUES(Description);

-- =====================================================
-- Table: Accounts (COA - Chart of Accounts)
-- =====================================================
CREATE TABLE IF NOT EXISTS Accounts (
    Code VARCHAR(20) PRIMARY KEY,
    Name VARCHAR(200) NOT NULL,
    Level INT NOT NULL DEFAULT 0,
    Type ENUM('Asset','Liability','Equity','Revenue','Expense') NOT NULL,
    NormalBalance VARCHAR(10) NOT NULL DEFAULT 'Debit',
    ParentCode VARCHAR(20) NOT NULL DEFAULT '',
    IsPostable BOOLEAN NOT NULL DEFAULT TRUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Table: AccountingPeriods
-- =====================================================
CREATE TABLE IF NOT EXISTS AccountingPeriods (
    Code VARCHAR(20) PRIMARY KEY,
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    Status VARCHAR(20) NOT NULL DEFAULT 'CLOSED'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Table: Transactions
-- =====================================================
CREATE TABLE IF NOT EXISTS Transactions (
    Id VARCHAR(50) PRIMARY KEY,
    Date DATE NOT NULL,
    Description VARCHAR(500),
    TotalAmount DECIMAL(18,2) NOT NULL DEFAULT 0,
    AccountingPeriodCode VARCHAR(20),
    Status VARCHAR(20) NOT NULL DEFAULT 'DRAFT',
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (AccountingPeriodCode) REFERENCES AccountingPeriods(Code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Table: TransactionLines
-- =====================================================
CREATE TABLE IF NOT EXISTS TransactionLines (
    Id BIGINT AUTO_INCREMENT PRIMARY KEY,
    TransactionId VARCHAR(50) NOT NULL,
    AccountCode VARCHAR(20) NOT NULL,
    Description VARCHAR(200),
    DebitAmount DECIMAL(18,2) NOT NULL DEFAULT 0,
    CreditAmount DECIMAL(18,2) NOT NULL DEFAULT 0,
    FOREIGN KEY (TransactionId) REFERENCES Transactions(Id),
    FOREIGN KEY (AccountCode) REFERENCES Accounts(Code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_transactionlines_transaction ON TransactionLines(TransactionId);
CREATE INDEX idx_transactionlines_account ON TransactionLines(AccountCode);

-- =====================================================
-- Table: SalesTransactions
-- =====================================================
CREATE TABLE IF NOT EXISTS SalesTransactions (
    Id VARCHAR(50) PRIMARY KEY,
    Date DATE NOT NULL,
    CustomerId VARCHAR(50) NOT NULL,
    CustomerName VARCHAR(200),
    CustomerTaxCode VARCHAR(20),
    TotalAmount DECIMAL(18,2) NOT NULL DEFAULT 0,
    VatAmount DECIMAL(18,2) NOT NULL DEFAULT 0,
    NetAmount DECIMAL(18,2) NOT NULL DEFAULT 0,
    PaymentStatus VARCHAR(20) NOT NULL DEFAULT 'UNPAID',
    InvoiceId VARCHAR(50),
    AccountingPeriodCode VARCHAR(20),
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (AccountingPeriodCode) REFERENCES AccountingPeriods(Code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Table: PurchaseTransactions
-- =====================================================
CREATE TABLE IF NOT EXISTS PurchaseTransactions (
    Id VARCHAR(50) PRIMARY KEY,
    Date DATE NOT NULL,
    SupplierId VARCHAR(50) NOT NULL,
    SupplierName VARCHAR(200),
    SupplierTaxCode VARCHAR(20),
    TotalAmount DECIMAL(18,2) NOT NULL DEFAULT 0,
    VatAmount DECIMAL(18,2) NOT NULL DEFAULT 0,
    NetAmount DECIMAL(18,2) NOT NULL DEFAULT 0,
    PaymentStatus VARCHAR(20) NOT NULL DEFAULT 'UNPAID',
    InvoiceId VARCHAR(50),
    AccountingPeriodCode VARCHAR(20),
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (AccountingPeriodCode) REFERENCES AccountingPeriods(Code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Table: Roles
-- =====================================================
CREATE TABLE IF NOT EXISTS Roles (
    Id VARCHAR(50) PRIMARY KEY,
    Name VARCHAR(50) NOT NULL UNIQUE,
    Description VARCHAR(200),
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Table: Users
-- =====================================================
CREATE TABLE IF NOT EXISTS Users (
    Id VARCHAR(50) PRIMARY KEY,
    Username VARCHAR(50) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    FullName VARCHAR(100),
    IsActive BOOLEAN NOT NULL DEFAULT TRUE,
    LastLoginAt DATETIME,
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Table: UserRoles
-- =====================================================
CREATE TABLE IF NOT EXISTS UserRoles (
    UserId VARCHAR(50) NOT NULL,
    RoleId VARCHAR(50) NOT NULL,
    PRIMARY KEY (UserId, RoleId),
    FOREIGN KEY (UserId) REFERENCES Users(Id),
    FOREIGN KEY (RoleId) REFERENCES Roles(Id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Seed Data: Default Roles
-- =====================================================
INSERT INTO Roles (Id, Name, Description) VALUES
('ADMIN', 'Administrator', 'Full system access'),
('ACCOUNTANT', 'Accountant', 'Accounting operations'),
('VIEWER', 'Viewer', 'Read-only access')
ON DUPLICATE KEY UPDATE Description = VALUES(Description);

-- =====================================================
-- Seed SME users with roles (password: GL@2026!)
-- =====================================================
INSERT INTO AspNetUsers (Id, UserName, NormalizedUserName, Email, NormalizedEmail, PasswordHash, FullName, IsActive) VALUES
('USR001', 'admin', 'ADMIN', 'admin@gl.local', 'ADMIN@GL.LOCAL', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p93qXq8fFKhPBKlz7M4sWq', 'Chủ DN - Administrator', 1),
('USR002', 'accountant', 'ACCOUNTANT', 'ketoan@gl.local', 'KETOAN@GL.LOCAL', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p93qXq8fFKhPBKlz7M4sWq', 'Nguyễn Văn A - Kế toán', 1),
('USR003', 'bookkeeper', 'BOOKKEEPER', 'mayke@gl.local', 'MAYKE@GL.LOCAL', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p93qXq8fFKhPBKlz7M4sWq', 'Trần Thị B - Kế toán máy', 1),
('USR004', 'sales', 'SALES', 'kinhdoanh@gl.local', 'KINHDOANH@GL.LOCAL', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p93qXq8fFKhPBKlz7M4sWq', 'Phạm Văn C - Kinh doanh', 1),
('USR005', 'warehouse', 'WAREHOUSE', 'kho@gl.local', 'KHO@GL.LOCAL', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p93qXq8fFKhPBKlz7M4sWq', 'Lê Văn D - Thủ kho', 1),
('USR006', 'viewer', 'VIEWER', 'viewer@gl.local', 'VIEWER@GL.LOCAL', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p93qXq8fFKhPBKlz7M4sWq', 'Đỗ Văn E - Xem báo cáo', 1)
ON DUPLICATE KEY UPDATE FullName = VALUES(FullName);

-- Seed user-role assignments
INSERT INTO AspNetUserRoles (UserId, RoleId) VALUES
('USR001', 'role_admin'),
('USR002', 'role_accountant'),
('USR003', 'role_bookkeeper'),
('USR004', 'role_sales'),
('USR005', 'role_warehouse'),
('USR006', 'role_viewer')
ON DUPLICATE KEY UPDATE RoleId = VALUES(RoleId);