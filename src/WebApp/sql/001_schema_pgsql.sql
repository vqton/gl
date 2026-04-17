-- =====================================================
-- GL Accounting System - PostgreSQL Schema Script
-- Generated: 2026-04-16
-- Compatible: PostgreSQL 14+
-- =====================================================

-- =====================================================
-- ASP.NET Core Identity Tables
-- =====================================================
CREATE TABLE IF NOT EXISTS AspNetUsers (
    Id VARCHAR(50) PRIMARY KEY,
    UserName VARCHAR(256),
    NormalizedUserName VARCHAR(256),
    Email VARCHAR(256),
    NormalizedEmail VARCHAR(256),
    EmailConfirmed BOOLEAN NOT NULL DEFAULT FALSE,
    PasswordHash VARCHAR(255),
    SecurityStamp VARCHAR(255),
    ConcurrencyStamp VARCHAR(255),
    PhoneNumber VARCHAR(20),
    PhoneNumberConfirmed BOOLEAN NOT NULL DEFAULT FALSE,
    TwoFactorEnabled BOOLEAN NOT NULL DEFAULT FALSE,
    LockoutEnd TIMESTAMP,
    LockoutEnabled BOOLEAN NOT NULL DEFAULT FALSE,
    AccessFailedCount INT NOT NULL DEFAULT 0,
    FullName VARCHAR(100),
    IsActive BOOLEAN NOT NULL DEFAULT TRUE,
    LastLoginAt TIMESTAMP,
    Department VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS AspNetRoles (
    Id VARCHAR(50) PRIMARY KEY,
    Name VARCHAR(256) NOT NULL UNIQUE,
    NormalizedName VARCHAR(256) NOT NULL UNIQUE,
    ConcurrencyStamp VARCHAR(255),
    Description VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS AspNetUserRoles (
    UserId VARCHAR(50) NOT NULL,
    RoleId VARCHAR(50) NOT NULL,
    PRIMARY KEY (UserId, RoleId),
    FOREIGN KEY (UserId) REFERENCES AspNetUsers(Id) ON DELETE CASCADE,
    FOREIGN KEY (RoleId) REFERENCES AspNetRoles(Id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS AspNetUserClaims (
    Id SERIAL PRIMARY KEY,
    UserId VARCHAR(50) NOT NULL,
    ClaimType TEXT,
    ClaimValue TEXT,
    FOREIGN KEY (UserId) REFERENCES AspNetUsers(Id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS AspNetRoleClaims (
    Id SERIAL PRIMARY KEY,
    RoleId VARCHAR(50) NOT NULL,
    ClaimType TEXT,
    ClaimValue TEXT,
    FOREIGN KEY (RoleId) REFERENCES AspNetRoles(Id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS AspNetUserLogins (
    LoginProvider VARCHAR(50) NOT NULL,
    ProviderKey VARCHAR(50) NOT NULL,
    ProviderDisplayName VARCHAR(100),
    UserId VARCHAR(50) NOT NULL,
    PRIMARY KEY (LoginProvider, ProviderKey),
    FOREIGN KEY (UserId) REFERENCES AspNetUsers(Id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS AspNetUserTokens (
    UserId VARCHAR(50) NOT NULL,
    LoginProvider VARCHAR(50) NOT NULL,
    Name VARCHAR(50) NOT NULL,
    Value TEXT,
    PRIMARY KEY (UserId, LoginProvider, Name),
    FOREIGN KEY (UserId) REFERENCES AspNetUsers(Id) ON DELETE CASCADE
);

-- =====================================================
-- Table: Accounts (COA - Chart of Accounts)
-- =====================================================
CREATE TABLE IF NOT EXISTS Accounts (
    Code VARCHAR(20) PRIMARY KEY,
    Name VARCHAR(200) NOT NULL,
    Level INT NOT NULL DEFAULT 0,
    Type VARCHAR(20) NOT NULL,
    NormalBalance VARCHAR(10) NOT NULL DEFAULT 'Debit',
    ParentCode VARCHAR(20) NOT NULL DEFAULT '',
    IsPostable BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE INDEX idx_accounts_code ON Accounts(Code);
CREATE INDEX idx_accounts_parent ON Accounts(ParentCode);

-- =====================================================
-- Seed roles - SME (6 roles)
-- =====================================================
INSERT INTO AspNetRoles (Id, Name, NormalizedName, Description) VALUES
('role_admin', 'ADMIN', 'ADMIN', 'Quản trị - Full system'),
('role_accountant', 'ACCOUNTANT', 'ACCOUNTANT', 'Kế toán - Full accounting'),
('role_bookkeeper', 'BOOKKEEPER', 'BOOKKEEPER', 'Kế toán máy - Nhập liệu'),
('role_sales', 'SALES', 'SALES', 'Kinh doanh - Bán hàng'),
('role_warehouse', 'WAREHOUSE', 'WAREHOUSE', 'Kho - Nhập xuất'),
('role_viewer', 'VIEWER', 'VIEWER', 'Xem báo cáo')
ON CONFLICT (Id) DO NOTHING;

-- =====================================================
-- Seed SME users (password: GL@2026!)
-- =====================================================
INSERT INTO AspNetUsers (Id, UserName, NormalizedUserName, Email, NormalizedEmail, PasswordHash, FullName, IsActive) VALUES
('USR001', 'admin', 'ADMIN', 'admin@gl.local', 'ADMIN@GL.LOCAL', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p93qXq8fFKhPBKlz7M4sWq', 'Chủ DN - Administrator', true),
('USR002', 'accountant', 'ACCOUNTANT', 'ketoan@gl.local', 'KETOAN@GL.LOCAL', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p93qXq8fFKhPBKlz7M4sWq', 'Nguyễn Văn A - Kế toán', true),
('USR003', 'bookkeeper', 'BOOKKEEPER', 'mayke@gl.local', 'MAYKE@GL.LOCAL', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p93qXq8fFKhPBKlz7M4sWq', 'Trần Thị B - Kế toán máy', true),
('USR004', 'sales', 'SALES', 'kinhdoanh@gl.local', 'KINHDOANH@GL.LOCAL', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p93qXq8fFKhPBKlz7M4sWq', 'Phạm Văn C - Kinh doanh', true),
('USR005', 'warehouse', 'WAREHOUSE', 'kho@gl.local', 'KHO@GL.LOCAL', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p93qXq8fFKhPBKlz7M4sWq', 'Lê Văn D - Thủ kho', true),
('USR006', 'viewer', 'VIEWER', 'viewer@gl.local', 'VIEWER@GL.LOCAL', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p93qXq8fFKhPBKlz7M4sWq', 'Đỗ Văn E - Xem báo cáo', true)
ON CONFLICT (Id) DO NOTHING;

-- User-role assignments
INSERT INTO AspNetUserRoles (UserId, RoleId) VALUES
('USR001', 'role_admin'),
('USR002', 'role_accountant'),
('USR003', 'role_bookkeeper'),
('USR004', 'role_sales'),
('USR005', 'role_warehouse'),
('USR006', 'role_viewer')
ON CONFLICT (UserId, RoleId) DO NOTHING;

-- =====================================================
-- Table: AccountingPeriods
-- =====================================================
CREATE TABLE IF NOT EXISTS AccountingPeriods (
    Code VARCHAR(20) PRIMARY KEY,
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    Status VARCHAR(20) NOT NULL DEFAULT 'CLOSED'
);

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
    CreatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (AccountingPeriodCode) REFERENCES AccountingPeriods(Code)
);

CREATE INDEX idx_transactions_date ON Transactions(Date);
CREATE INDEX idx_transactions_period ON Transactions(AccountingPeriodCode);

-- =====================================================
-- Table: TransactionLines
-- =====================================================
CREATE TABLE IF NOT EXISTS TransactionLines (
    Id BIGSERIAL PRIMARY KEY,
    TransactionId VARCHAR(50) NOT NULL,
    AccountCode VARCHAR(20) NOT NULL,
    Description VARCHAR(200),
    DebitAmount DECIMAL(18,2) NOT NULL DEFAULT 0,
    CreditAmount DECIMAL(18,2) NOT NULL DEFAULT 0,
    FOREIGN KEY (TransactionId) REFERENCES Transactions(Id),
    FOREIGN KEY (AccountCode) REFERENCES Accounts(Code)
);

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
    CreatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (AccountingPeriodCode) REFERENCES AccountingPeriods(Code)
);

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
    CreatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (AccountingPeriodCode) REFERENCES AccountingPeriods(Code)
);

-- =====================================================
-- Table: Roles
-- =====================================================
CREATE TABLE IF NOT EXISTS Roles (
    Id VARCHAR(50) PRIMARY KEY,
    Name VARCHAR(50) NOT NULL UNIQUE,
    Description VARCHAR(200),
    CreatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

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
    LastLoginAt TIMESTAMP,
    CreatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Table: UserRoles
-- =====================================================
CREATE TABLE IF NOT EXISTS UserRoles (
    UserId VARCHAR(50) NOT NULL,
    RoleId VARCHAR(50) NOT NULL,
    PRIMARY KEY (UserId, RoleId),
    FOREIGN KEY (UserId) REFERENCES Users(Id),
    FOREIGN KEY (RoleId) REFERENCES Roles(Id)
);

-- =====================================================
-- Seed Data: Default Roles
-- =====================================================
INSERT INTO Roles (Id, Name, Description) VALUES
('ADMIN', 'Administrator', 'Full system access'),
('ACCOUNTANT', 'Accountant', 'Accounting operations'),
('VIEWER', 'Viewer', 'Read-only access')
ON CONFLICT (Id) DO NOTHING;

-- =====================================================
-- Seed Data: Default Users (password: Admin123!)
-- NOTE: Change password in production
-- =====================================================
INSERT INTO Users (Id, Username, Password, Email, FullName) VALUES
('USR001', 'admin', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p93qXq8fFKhPBKlz7M4sWq', 'admin@gl.local', 'Administrator'),
('USR002', 'accountant', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p93qXq8fFKhPBKlz7M4sWq', 'accountant@gl.local', 'Kế toán trưởng')
ON CONFLICT (Username) DO NOTHING;

INSERT INTO UserRoles (UserId, RoleId) VALUES
('USR001', 'ADMIN'),
('USR002', 'ACCOUNTANT')
ON CONFLICT (UserId, RoleId) DO NOTHING;