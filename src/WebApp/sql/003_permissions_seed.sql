-- =====================================================
-- SME Role Permissions Matrix
-- Sử dụng cho doanh nghiệp vừa và nhỏ
-- Generated: 2026-04-17
-- =====================================================

USE gl_accounting;

-- =====================================================
-- ADMIN: Full access (chủ DN / IT)
-- =====================================================
INSERT INTO AspNetRoleClaims (RoleId, ClaimType, ClaimValue) VALUES
('role_admin', 'permission', 'full_access')
ON DUPLICATE KEY UPDATE ClaimType = VALUES(ClaimType);

-- =====================================================
-- ACCOUNTANT: Full accounting (kế toán)
-- =====================================================
INSERT INTO AspNetRoleClaims (RoleId, ClaimType, ClaimValue) VALUES
('role_accountant', 'permission', 'coa_view'),
('role_accountant', 'permission', 'transaction_view'),
('role_accountant', 'permission', 'transaction_create'),
('role_accountant', 'permission', 'transaction_edit'),
('role_accountant', 'permission', 'transaction_delete'),
('role_accountant', 'permission', 'transaction_approve'),
('role_accountant', 'permission', 'customer_view'),
('role_accountant', 'permission', 'customer_create'),
('role_accountant', 'permission', 'supplier_view'),
('role_accountant', 'permission', 'supplier_create'),
('role_accountant', 'permission', 'bank_view'),
('role_accountant', 'permission', 'bank_create'),
('role_accountant', 'permission', 'report_view'),
('role_accountant', 'permission', 'report_export'),
('role_accountant', 'permission', 'period_close'),
('role_accountant', 'permission', 'period_lock'),
('role_accountant', 'permission', 'asset_view'),
('role_accountant', 'permission', 'asset_create'),
('role_accountant', 'permission', 'payroll_view'),
('role_accountant', 'permission', 'payroll_create')
ON DUPLICATE KEY UPDATE ClaimType = VALUES(ClaimType);

-- =====================================================
-- BOOKKEEPER: Data entry (kế toán máy)
-- =====================================================
INSERT INTO AspNetRoleClaims (RoleId, ClaimType, ClaimValue) VALUES
('role_bookkeeper', 'permission', 'coa_view'),
('role_bookkeeper', 'permission', 'transaction_view'),
('role_bookkeeper', 'permission', 'transaction_create'),
('role_bookkeeper', 'permission', 'transaction_edit'),
('role_bookkeeper', 'permission', 'customer_view'),
('role_bookkeeper', 'permission', 'customer_create'),
('role_bookkeeper', 'permission', 'supplier_view'),
('role_bookkeeper', 'permission', 'supplier_create'),
('role_bookkeeper', 'permission', 'bank_view'),
('role_bookkeeper', 'permission', 'bank_create'),
('role_bookkeeper', 'permission', 'report_view')
ON DUPLICATE KEY UPDATE ClaimType = VALUES(ClaimType);

-- =====================================================
-- SALES: Sales (kinh doanh)
-- =====================================================
INSERT INTO AspNetRoleClaims (RoleId, ClaimType, ClaimValue) VALUES
('role_sales', 'permission', 'customer_view'),
('role_sales', 'permission', 'customer_create'),
('role_sales', 'permission', 'customer_edit'),
('role_sales', 'permission', 'sales_view'),
('role_sales', 'permission', 'sales_create'),
('role_sales', 'permission', 'sales_edit'),
('role_sales', 'permission', 'sales_approve'),
('role_sales', 'permission', 'inventory_view'),
('role_sales', 'permission', 'price_list_view'),
('role_sales', 'permission', 'report_sales_view')
ON DUPLICATE KEY UPDATE ClaimType = VALUES(ClaimType);

-- =====================================================
-- WAREHOUSE: Stock (kho)
-- =====================================================
INSERT INTO AspNetRoleClaims (RoleId, ClaimType, ClaimValue) VALUES
('role_warehouse', 'permission', 'inventory_view'),
('role_warehouse', 'permission', 'inventory_edit'),
('role_warehouse', 'permission', 'product_view'),
('role_warehouse', 'permission', 'product_create'),
('role_warehouse', 'permission', 'stock_in_view'),
('role_warehouse', 'permission', 'stock_in_create'),
('role_warehouse', 'permission', 'stock_out_view'),
('role_warehouse', 'permission', 'stock_out_create'),
('role_warehouse', 'permission', 'report_inventory_view')
ON DUPLICATE KEY UPDATE ClaimType = VALUES(ClaimType);

-- =====================================================
-- VIEWER: Read only (xem báo cáo)
-- =====================================================
INSERT INTO AspNetRoleClaims (RoleId, ClaimType, ClaimValue) VALUES
('role_viewer', 'permission', 'report_view'),
('role_viewer', 'permission', 'report_sales_view'),
('role_viewer', 'permission', 'report_purchase_view'),
('role_viewer', 'permission', 'report_inventory_view')
ON DUPLICATE KEY UPDATE ClaimType = VALUES(ClaimType);