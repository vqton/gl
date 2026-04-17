-- =====================================================
-- GL Accounting System - SQL Server Schema Script
-- Generated: 2026-04-16
-- Compatible: SQL Server 2019+
-- =====================================================

USE gl_accounting;
GO

-- =====================================================
-- ASP.NET Core Identity Tables
-- =====================================================
IF OBJECT_ID('AspNetUsers', 'U') IS NULL
CREATE TABLE AspNetUsers (
    Id VARCHAR(50) PRIMARY KEY,
    UserName NVARCHAR(256),
    NormalizedUserName NVARCHAR(256),
    Email NVARCHAR(256),
    NormalizedEmail NVARCHAR(256),
    EmailConfirmed BIT NOT NULL DEFAULT 0,
    PasswordHash NVARCHAR(255),
    SecurityStamp NVARCHAR(255),
    ConcurrencyStamp NVARCHAR(255),
    PhoneNumber NVARCHAR(20),
    PhoneNumberConfirmed BIT NOT NULL DEFAULT 0,
    TwoFactorEnabled BIT NOT NULL DEFAULT 0,
    LockoutEnd DATETIME2,
    LockoutEnabled BIT NOT NULL DEFAULT 1,
    AccessFailedCount INT NOT NULL DEFAULT 0,
    FullName NVARCHAR(100),
    IsActive BIT NOT NULL DEFAULT 1,
    LastLoginAt DATETIME2,
    Department NVARCHAR(100)
);
GO

IF OBJECT_ID('AspNetRoles', 'U') IS NULL
CREATE TABLE AspNetRoles (
    Id VARCHAR(50) PRIMARY KEY,
    Name NVARCHAR(256) NOT NULL UNIQUE,
    NormalizedName NVARCHAR(256) NOT NULL UNIQUE,
    ConcurrencyStamp NVARCHAR(255),
    Description NVARCHAR(200)
);
GO

IF OBJECT_ID('AspNetUserRoles', 'U') IS NULL
CREATE TABLE AspNetUserRoles (
    UserId VARCHAR(50) NOT NULL,
    RoleId VARCHAR(50) NOT NULL,
    PRIMARY KEY (UserId, RoleId),
    FOREIGN KEY (UserId) REFERENCES AspNetUsers(Id) ON DELETE CASCADE,
    FOREIGN KEY (RoleId) REFERENCES AspNetRoles(Id) ON DELETE CASCADE
);
GO

IF OBJECT_ID('AspNetUserClaims', 'U') IS NULL
CREATE TABLE AspNetUserClaims (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    UserId VARCHAR(50) NOT NULL,
    ClaimType NVARCHAR(MAX),
    ClaimValue NVARCHAR(MAX),
    FOREIGN KEY (UserId) REFERENCES AspNetUsers(Id) ON DELETE CASCADE
);
GO

IF OBJECT_ID('AspNetRoleClaims', 'U') IS NULL
CREATE TABLE AspNetRoleClaims (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    RoleId VARCHAR(50) NOT NULL,
    ClaimType NVARCHAR(MAX),
    ClaimValue NVARCHAR(MAX),
    FOREIGN KEY (RoleId) REFERENCES AspNetRoles(Id) ON DELETE CASCADE
);
GO

IF OBJECT_ID('AspNetUserLogins', 'U') IS NULL
CREATE TABLE AspNetUserLogins (
    LoginProvider NVARCHAR(50) NOT NULL,
    ProviderKey NVARCHAR(50) NOT NULL,
    ProviderDisplayName NVARCHAR(100),
    UserId VARCHAR(50) NOT NULL,
    PRIMARY KEY (LoginProvider, ProviderKey),
    FOREIGN KEY (UserId) REFERENCES AspNetUsers(Id) ON DELETE CASCADE
);
GO

IF OBJECT_ID('AspNetUserTokens', 'U') IS NULL
CREATE TABLE AspNetUserTokens (
    UserId VARCHAR(50) NOT NULL,
    LoginProvider NVARCHAR(50) NOT NULL,
    Name NVARCHAR(50) NOT NULL,
    Value NVARCHAR(MAX),
    PRIMARY KEY (UserId, LoginProvider, Name),
    FOREIGN KEY (UserId) REFERENCES AspNetUsers(Id) ON DELETE CASCADE
);
GO

-- =====================================================
-- Table: Accounts (COA - Chart of Accounts)
-- =====================================================
IF OBJECT_ID('Accounts', 'U') IS NULL
CREATE TABLE Accounts (
    Code VARCHAR(20) PRIMARY KEY,
    Name NVARCHAR(200) NOT NULL,
    Level INT NOT NULL DEFAULT 0,
    Type VARCHAR(20) NOT NULL,
    NormalBalance VARCHAR(10) NOT NULL DEFAULT 'Debit',
    ParentCode VARCHAR(20) NOT NULL DEFAULT '',
    IsPostable BIT NOT NULL DEFAULT 1
);

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_Accounts_Code')
CREATE INDEX IX_Accounts_Code ON Accounts(Code);

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_Accounts_Parent')
CREATE INDEX IX_Accounts_Parent ON Accounts(ParentCode);
GO

-- =====================================================
-- Table: AccountingPeriods
-- =====================================================
IF OBJECT_ID('AccountingPeriods', 'U') IS NULL
CREATE TABLE AccountingPeriods (
    Code VARCHAR(20) PRIMARY KEY,
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    Status VARCHAR(20) NOT NULL DEFAULT 'CLOSED'
);
GO

-- =====================================================
-- Table: Transactions
-- =====================================================
IF OBJECT_ID('Transactions', 'U') IS NULL
CREATE TABLE Transactions (
    Id VARCHAR(50) PRIMARY KEY,
    Date DATE NOT NULL,
    Description NVARCHAR(500),
    TotalAmount DECIMAL(18,2) NOT NULL DEFAULT 0,
    AccountingPeriodCode VARCHAR(20),
    Status VARCHAR(20) NOT NULL DEFAULT 'DRAFT',
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (AccountingPeriodCode) REFERENCES AccountingPeriods(Code)
);

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_Transactions_Date')
CREATE INDEX IX_Transactions_Date ON Transactions(Date);

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_Transactions_Period')
CREATE INDEX IX_Transactions_Period ON Transactions(AccountingPeriodCode);
GO

-- =====================================================
-- Table: TransactionLines
-- =====================================================
IF OBJECT_ID('TransactionLines', 'U') IS NULL
CREATE TABLE TransactionLines (
    Id BIGINT IDENTITY(1,1) PRIMARY KEY,
    TransactionId VARCHAR(50) NOT NULL,
    AccountCode VARCHAR(20) NOT NULL,
    Description NVARCHAR(200),
    DebitAmount DECIMAL(18,2) NOT NULL DEFAULT 0,
    CreditAmount DECIMAL(18,2) NOT NULL DEFAULT 0,
    FOREIGN KEY (TransactionId) REFERENCES Transactions(Id),
    FOREIGN KEY (AccountCode) REFERENCES Accounts(Code)
);

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_TransactionLines_Transaction')
CREATE INDEX IX_TransactionLines_Transaction ON TransactionLines(TransactionId);

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_TransactionLines_Account')
CREATE INDEX IX_TransactionLines_Account ON TransactionLines(AccountCode);
GO

-- =====================================================
-- Table: SalesTransactions
-- =====================================================
IF OBJECT_ID('SalesTransactions', 'U') IS NULL
CREATE TABLE SalesTransactions (
    Id VARCHAR(50) PRIMARY KEY,
    Date DATE NOT NULL,
    CustomerId VARCHAR(50) NOT NULL,
    CustomerName NVARCHAR(200),
    CustomerTaxCode VARCHAR(20),
    TotalAmount DECIMAL(18,2) NOT NULL DEFAULT 0,
    VatAmount DECIMAL(18,2) NOT NULL DEFAULT 0,
    NetAmount DECIMAL(18,2) NOT NULL DEFAULT 0,
    PaymentStatus VARCHAR(20) NOT NULL DEFAULT 'UNPAID',
    InvoiceId VARCHAR(50),
    AccountingPeriodCode VARCHAR(20),
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (AccountingPeriodCode) REFERENCES AccountingPeriods(Code)
);
GO

-- =====================================================
-- Table: PurchaseTransactions
-- =====================================================
IF OBJECT_ID('PurchaseTransactions', 'U') IS NULL
CREATE TABLE PurchaseTransactions (
    Id VARCHAR(50) PRIMARY KEY,
    Date DATE NOT NULL,
    SupplierId VARCHAR(50) NOT NULL,
    SupplierName NVARCHAR(200),
    SupplierTaxCode VARCHAR(20),
    TotalAmount DECIMAL(18,2) NOT NULL DEFAULT 0,
    VatAmount DECIMAL(18,2) NOT NULL DEFAULT 0,
    NetAmount DECIMAL(18,2) NOT NULL DEFAULT 0,
    PaymentStatus VARCHAR(20) NOT NULL DEFAULT 'UNPAID',
    InvoiceId VARCHAR(50),
    AccountingPeriodCode VARCHAR(20),
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (AccountingPeriodCode) REFERENCES AccountingPeriods(Code)
);
GO

-- =====================================================
-- Table: Roles
-- =====================================================
IF OBJECT_ID('Roles', 'U') IS NULL
CREATE TABLE Roles (
    Id VARCHAR(50) PRIMARY KEY,
    Name VARCHAR(50) NOT NULL UNIQUE,
    Description NVARCHAR(200),
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
GO

-- =====================================================
-- Table: Users
-- =====================================================
IF OBJECT_ID('Users', 'U') IS NULL
CREATE TABLE Users (
    Id VARCHAR(50) PRIMARY KEY,
    Username VARCHAR(50) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    FullName NVARCHAR(100),
    IsActive BIT NOT NULL DEFAULT 1,
    LastLoginAt DATETIME,
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
GO

-- =====================================================
-- Table: UserRoles
-- =====================================================
IF OBJECT_ID('UserRoles', 'U') IS NULL
CREATE TABLE UserRoles (
    UserId VARCHAR(50) NOT NULL,
    RoleId VARCHAR(50) NOT NULL,
    PRIMARY KEY (UserId, RoleId),
    FOREIGN KEY (UserId) REFERENCES Users(Id),
    FOREIGN KEY (RoleId) REFERENCES Roles(Id)
);
GO

-- =====================================================
-- Seed Data: Default Roles
-- =====================================================
IF NOT EXISTS (SELECT 1 FROM Roles WHERE Id = 'ADMIN')
INSERT INTO Roles (Id, Name, Description) VALUES
('ADMIN', 'Administrator', 'Full system access'),
('ACCOUNTANT', 'Accountant', 'Accounting operations'),
('VIEWER', 'Viewer', 'Read-only access');
GO

-- =====================================================
-- Seed Data: Default Users (password: Admin123!)
-- NOTE: Change password in production
-- =====================================================
IF NOT EXISTS (SELECT 1 FROM Users WHERE Username = 'admin')
INSERT INTO Users (Id, Username, Password, Email, FullName) VALUES
('USR001', 'admin', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p93qXq8fFKhPBKlz7M4sWq', 'admin@gl.local', 'Administrator'),
('USR002', 'accountant', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p93qXq8fFKhPBKlz7M4sWq', 'accountant@gl.local', N'Kế toán trưởng');
GO

IF NOT EXISTS (SELECT 1 FROM UserRoles)
INSERT INTO UserRoles (UserId, RoleId) VALUES
('USR001', 'ADMIN'),
('USR002', 'ACCOUNTANT');
GO

-- =====================================================
-- SME Roles (6 roles)
-- =====================================================
IF NOT EXISTS (SELECT 1 FROM AspNetRoles WHERE Id = 'role_admin')
INSERT INTO AspNetRoles (Id, Name, NormalizedName, Description) VALUES
('role_admin', 'ADMIN', 'ADMIN', 'Quản trị - Full system'),
('role_accountant', 'ACCOUNTANT', 'ACCOUNTANT', 'Kế toán - Full accounting'),
('role_bookkeeper', 'BOOKKEEPER', 'BOOKKEEPER', 'Kế toán máy - Nhập liệu'),
('role_sales', 'SALES', 'SALES', 'Kinh doanh - Bán hàng'),
('role_warehouse', 'WAREHOUSE', 'WAREHOUSE', 'Kho - Nhập xuất'),
('role_viewer', 'VIEWER', 'VIEWER', 'Xem báo cáo');
GO

-- Seed SME users (password: GL@2026!)
IF NOT EXISTS (SELECT 1 FROM AspNetUsers WHERE Id = 'USR001')
INSERT INTO AspNetUsers (Id, UserName, NormalizedUserName, Email, NormalizedEmail, PasswordHash, FullName, IsActive) VALUES
('USR001', 'admin', 'ADMIN', 'admin@gl.local', 'ADMIN@GL.LOCAL', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p93qXq8fFKhPBKlz7M4sWq', N'Chủ DN - Administrator', 1),
('USR002', 'accountant', 'ACCOUNTANT', 'ketoan@gl.local', 'KETOAN@GL.LOCAL', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p93qXq8fFKhPBKlz7M4sWq', N'Nguyễn Văn A - Kế toán', 1),
('USR003', 'bookkeeper', 'BOOKKEEPER', 'mayke@gl.local', 'MAYKE@GL.LOCAL', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p93qXq8fFKhPBKlz7M4sWq', N'Trần Thị B - Kế toán máy', 1),
('USR004', 'sales', 'SALES', 'kinhdoanh@gl.local', 'KINHDOANH@GL.LOCAL', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p93qXq8fFKhPBKlz7M4sWq', N'Phạm Văn C - Kinh doanh', 1),
('USR005', 'warehouse', 'WAREHOUSE', 'kho@gl.local', 'KHO@GL.LOCAL', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p93qXq8fFKhPBKlz7M4sWq', N'Lê Văn D - Thủ kho', 1),
('USR006', 'viewer', 'VIEWER', 'viewer@gl.local', 'VIEWER@GL.LOCAL', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p93qXq8fFKhPBKlz7M4sWq', N'Đỗ Văn E - Xem báo cáo', 1);
GO

-- User-role assignments
IF NOT EXISTS (SELECT 1 FROM AspNetUserRoles)
INSERT INTO AspNetUserRoles (UserId, RoleId) VALUES
('USR001', 'role_admin'),
('USR002', 'role_accountant'),
('USR003', 'role_bookkeeper'),
('USR004', 'role_sales'),
('USR005', 'role_warehouse'),
('USR006', 'role_viewer');
GO