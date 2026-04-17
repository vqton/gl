-- =====================================================
-- GL Accounting System - Chart of Accounts Seed Data
-- TT99/2025 Vietnamese Accounting Standards
-- =====================================================

USE gl_accounting;

-- =====================================================
-- ASSETS (1xxx)
-- =====================================================
INSERT INTO Accounts (Code, Name, Level, Type, NormalBalance, ParentCode, IsPostable) VALUES
-- Cash and Cash Equivalents (11x)
('111', 'Tiền mặt', 1, 'Asset', 'Debit', '', TRUE),
('1111', 'Tiền mặt tại quỹ', 2, 'Asset', 'Debit', '111', TRUE),
('112', 'Tiền gửi ngân hàng', 1, 'Asset', 'Debit', '', TRUE),
('1121', 'Tiền gửi ngân hàng', 2, 'Asset', 'Debit', '112', TRUE),
('121', 'Tiền đang chuyển', 1, 'Asset', 'Debit', '', TRUE),

-- Accounts Receivable (131)
('131', 'Phải thu của khách hàng', 1, 'Asset', 'Debit', '', TRUE),
('1311', 'Phải thu của khách hàng', 2, 'Asset', 'Debit', '131', TRUE),
('1312', 'Phải thu nội bộ', 2, 'Asset', 'Debit', '131', FALSE),

-- Advances to Suppliers (141)
('141', 'Tạm ứng', 1, 'Asset', 'Debit', '', TRUE),
('1411', 'Tạm ứng cho CNV', 2, 'Asset', 'Debit', '141', TRUE),
('1412', 'Tạm ứng cho khách', 2, 'Asset', 'Debit', '141', TRUE),

-- Other Receivables (136, 138)
('136', 'Phải thu nội bộ', 1, 'Asset', 'Debit', '', TRUE),
('138', 'Phải thu khác', 1, 'Asset', 'Debit', '', TRUE),
('1381', 'Phải thu khác', 2, 'Asset', 'Debit', '138', TRUE),
('1388', 'Phải thu khác - TM', 2, 'Asset', 'Debit', '138', TRUE),

-- Inventory (15x)
('151', 'Hàng mua đang đi đường', 1, 'Asset', 'Debit', '', TRUE),
('152', 'Nguyên vật liệu', 1, 'Asset', 'Debit', '', TRUE),
('1521', 'Nguyên vật liệu chính', 2, 'Asset', 'Debit', '152', TRUE),
('1522', 'Nguyên vật liệu phụ', 2, 'Asset', 'Debit', '152', TRUE),
('153', 'Công cụ dụng cụ', 1, 'Asset', 'Debit', '', TRUE),
('154', 'Chi phí sản xuất kinh doanh dở dang', 1, 'Asset', 'Debit', '', TRUE),
('1541', 'Chi phí NVL trực tiếp', 2, 'Asset', 'Debit', '154', TRUE),
('1542', 'Chi phí nhân công trực tiếp', 2, 'Asset', 'Debit', '154', TRUE),
('1543', 'Chi phí sản xuất chung', 2, 'Asset', 'Debit', '154', TRUE),
('155', 'Thành phẩm', 1, 'Asset', 'Debit', '', TRUE),
('156', 'Hàng hóa', 1, 'Asset', 'Debit', '', TRUE),
('1561', 'Hàng hóa tại kho', 2, 'Asset', 'Debit', '156', TRUE),
('1562', 'Hàng hóa đi đường', 2, 'Asset', 'Debit', '156', TRUE),

-- Fixed Assets (21x)
('211', 'Tài sản cố định hữu hình', 1, 'Asset', 'Debit', '', TRUE),
('2111', 'Nguyên giá TSCĐ', 2, 'Asset', 'Debit', '211', TRUE),
('2112', 'Hao mòn lũy kế', 2, 'Asset', 'Credit', '211', TRUE),
('212', 'Tài sản cố định vô hình', 1, 'Asset', 'Debit', '', TRUE),
('213', 'Tài sản cố định thuê tài chính', 1, 'Asset', 'Debit', '', TRUE),
('214', 'Hao mòn TSCĐ', 1, 'Asset', 'Credit', '', TRUE),

-- Construction in Progress (24x)
('241', 'Xây dựng cơ bản dở dang', 1, 'Asset', 'Debit', '', TRUE),

-- Long-term Investments (22x)
('221', 'Đầu tư vào công ty con', 1, 'Asset', 'Debit', '', TRUE),
('222', 'Đầu tư vào cty liên kết', 1, 'Asset', 'Debit', '', TRUE),
('228', 'Đầu tư khác', 1, 'Asset', 'Debit', '', TRUE),

-- Long-term Receivables (23x)
('231', 'Phải thu dài hạn', 1, 'Asset', 'Debit', '', TRUE),
('242', 'Chi phí trả trước dài hạn', 1, 'Asset', 'Debit', '', TRUE),
('243', 'Tài sản thuế thu nhập hoãn lại', 1, 'Asset', 'Debit', '', TRUE)

ON DUPLICATE KEY UPDATE Name = VALUES(Name);

-- =====================================================
-- LIABILITIES (2xxx)
-- =====================================================
INSERT INTO Accounts (Code, Name, Level, Type, NormalBalance, ParentCode, IsPostable) VALUES
-- Accounts Payable (331)
('331', 'Phải trả cho người bán', 1, 'Liability', 'Credit', '', TRUE),
('3311', 'Phải trả người bán', 2, 'Liability', 'Credit', '331', TRUE),
('3312', 'Phải trả nội bộ', 2, 'Liability', 'Credit', '331', FALSE),

-- Advances from Customers (338)
('338', 'Phải trả nội bộ', 1, 'Liability', 'Credit', '', TRUE),
('3381', 'Nhận ký quỹ, ký cược', 2, 'Liability', 'Credit', '338', TRUE),
('3382', 'Nhận tạm ứng', 2, 'Liability', 'Credit', '338', TRUE),
('3383', 'Phải trả khác', 2, 'Liability', 'Credit', '338', TRUE),

-- Taxes (333)
('333', 'Thuế và các khoản phải nộp', 1, 'Liability', 'Credit', '', TRUE),
('3331', 'Thuế GTGT đầu ra', 2, 'Liability', 'Credit', '333', TRUE),
('3332', 'Thuế TNDN', 2, 'Liability', 'Credit', '333', TRUE),
('3333', 'Thuế TNCN', 2, 'Liability', 'Credit', '333', TRUE),
('3334', 'Thuế Tài nguyên', 2, 'Liability', 'Credit', '333', TRUE),
('3335', 'Thuế nhà thầu', 2, 'Liability', 'Credit', '333', TRUE),
('3338', 'Thuế khác', 2, 'Liability', 'Credit', '333', TRUE),
('33311', 'Thuế GTGT theo PP khấu trừ', 3, 'Liability', 'Credit', '3331', FALSE),
('33312', 'Thuế GTGT theo PP trực tiếp', 3, 'Liability', 'Credit', '3331', FALSE),

-- Salaries Payable (334)
('334', 'Phải trả người lao động', 1, 'Liability', 'Credit', '', TRUE),
('3341', 'Phải trả lương', 2, 'Liability', 'Credit', '334', TRUE),
('3342', 'Phải trả thưởng', 2, 'Liability', 'Credit', '334', TRUE),
('3343', 'Phải trả BHXH', 2, 'Liability', 'Credit', '334', TRUE),
('3344', 'Phải trả BHYT', 2, 'Liability', 'Credit', '334', TRUE),
('3345', 'Phải trả BHTN', 2, 'Liability', 'Credit', '334', TRUE),
('3346', 'Phải trả KPĐ', 2, 'Liability', 'Credit', '334', TRUE),
('3347', 'Phải trả thuế TNCN', 2, 'Liability', 'Credit', '334', TRUE),

-- Insurance (338)
('338', 'Phải trả khác', 1, 'Liability', 'Credit', '', TRUE),

-- Short-term Payables (32x)
('321', 'Vay ngắn hạn', 1, 'Liability', 'Credit', '', TRUE),
('322', 'Nợ dài hạn đến hạn trả', 1, 'Liability', 'Credit', '', TRUE),

-- Long-term Liabilities (34x)
('341', 'Vay dài hạn', 1, 'Liability', 'Credit', '', TRUE),
('342', 'Nợ phải trả', 1, 'Liability', 'Credit', '', TRUE),
('343', 'Thuế thu nhập hoãn lại phải trả', 1, 'Liability', 'Credit', '', TRUE),
('344', 'Quỹ khen thưởng phúc lợi', 1, 'Liability', 'Credit', '', TRUE)

ON DUPLICATE KEY UPDATE Name = VALUES(Name);

-- =====================================================
-- EQUITY (4xxx)
-- =====================================================
INSERT INTO Accounts (Code, Name, Level, Type, NormalBalance, ParentCode, IsPostable) VALUES
-- Owners Equity (41x)
('411', 'Vốn góp của chủ sở hữu', 1, 'Equity', 'Credit', '', TRUE),
('4111', 'Vốn góp', 2, 'Equity', 'Credit', '411', TRUE),
('4112', 'Thặng vốn cổ phần', 2, 'Equity', 'Credit', '411', TRUE),
('4113', 'Vốn khác', 2, 'Equity', 'Credit', '411', TRUE),

-- Share Premium (418)
('418', 'Chênh lệch đánh giá tài sản', 1, 'Equity', 'Credit', '', TRUE),

-- Funds (42x)
('421', 'Lợi nhuận sau thuế chưa phân phối', 1, 'Equity', 'Credit', '', TRUE),
('4211', 'LNST chưa phân phối', 2, 'Equity', 'Credit', '421', TRUE),
('4212', 'LNST đã phân phối', 2, 'Equity', 'Credit', '421', TRUE),

-- Reserve Fund (43x)
('431', 'Quỹ dự phòng tài chính', 1, 'Equity', 'Credit', '', TRUE),
('4311', 'Quỹ dự phòng bổ sung', 2, 'Equity', 'Credit', '431', TRUE),
('4312', 'Quỹ hỗ trợ SDHN', 2, 'Equity', 'Credit', '431', TRUE),
('4313', 'Quỹ phát triển', 2, 'Equity', 'Credit', '431', TRUE),

-- Revaluation Reserve (44x)
('441', 'Chênh lệch tỷ giá', 1, 'Equity', 'Credit', '', TRUE),
('444', 'Quỹ đ���u tư phát triển', 1, 'Equity', 'Credit', '', TRUE)

ON DUPLICATE KEY UPDATE Name = VALUES(Name);

-- =====================================================
-- REVENUE (5xxx)
-- =====================================================
INSERT INTO Accounts (Code, Name, Level, Type, NormalBalance, ParentCode, IsPostable) VALUES
-- Sales Revenue (511)
('511', 'Doanh thu bán hàng', 1, 'Revenue', 'Credit', '', TRUE),
('5111', 'Doanh thu bán hàng hóa', 2, 'Revenue', 'Credit', '511', TRUE),
('5112', 'Doanh thu bán thành phẩm', 2, 'Revenue', 'Credit', '511', TRUE),
('5113', 'Doanh thu cung cấp DV', 2, 'Revenue', 'Credit', '511', TRUE),
('5114', 'Doanh thu xây lắp', 2, 'Revenue', 'Credit', '511', TRUE),
('5117', 'Doanh thu nội bộ', 2, 'Revenue', 'Credit', '511', FALSE),

-- Sales Deductions (521)
('521', 'Giảm giá hàng bán', 1, 'Revenue', 'Debit', '', TRUE),
('5211', 'Giảm giá hàng bán', 2, 'Revenue', 'Debit', '521', TRUE),
('5212', 'Hàng bán bị trả lại', 2, 'Revenue', 'Debit', '521', TRUE),
('5213', 'Giảm giá hàng bán hóa đơn điều chỉnh', 2, 'Revenue', 'Debit', '521', TRUE),

-- Other Revenue (515, 711)
('515', 'Doanh thu hoạt động tài chính', 1, 'Revenue', 'Credit', '', TRUE),
('5151', 'Lãi tiền gửi', 2, 'Revenue', 'Credit', '515', TRUE),
('5152', 'Lãi bán hàng trả góp', 2, 'Revenue', 'Credit', '515', TRUE),
('5153', 'Lãi cho vay', 2, 'Revenue', 'Credit', '515', TRUE),
('5154', 'Chênh lệch lãi tỷ giá', 2, 'Revenue', 'Credit', '515', TRUE),
('5155', 'Lãi từ thanh lý TSCĐ', 2, 'Revenue', 'Credit', '515', TRUE),
('5156', 'Thu nhập từ đầu tư', 2, 'Revenue', 'Credit', '515', TRUE),
('711', 'Thu nhập khác', 1, 'Revenue', 'Credit', '', TRUE),
('7111', 'Thu nhập khác', 2, 'Revenue', 'Credit', '711', TRUE)

ON DUPLICATE KEY UPDATE Name = VALUES(Name);

-- =====================================================
-- COST OF GOODS SOLD (6xxx)
-- =====================================================
INSERT INTO Accounts (Code, Name, Level, Type, NormalBalance, ParentCode, IsPostable) VALUES
-- Cost of Goods Sold (632)
('632', 'Giá vốn hàng bán', 1, 'Expense', 'Debit', '', TRUE),
('6321', 'Giá vốn hàng hóa', 2, 'Expense', 'Debit', '632', TRUE),
('6322', 'Giá vốn thành phẩm', 2, 'Expense', 'Debit', '632', TRUE),
('6323', 'Giá vốn dịch vụ', 2, 'Expense', 'Debit', '632', TRUE),
('6324', 'Giá vốn xây lắp', 2, 'Expense', 'Debit', '632', TRUE),

-- Financial Expenses (635)
('635', 'Chi phí tài chính', 1, 'Expense', 'Debit', '', TRUE),
('6351', 'Lãi vay', 2, 'Expense', 'Debit', '635', TRUE),
('6352', 'Chiết khấu thanh toán', 2, 'Expense', 'Debit', '635', TRUE),
('6353', 'Chênh lệch lỗ tỷ giá', 2, 'Expense', 'Debit', '635', TRUE),
('6354', 'Lỗ từ thanh lý TSCĐ', 2, 'Expense', 'Debit', '635', TRUE),
('6358', 'Chi phí tài chính khác', 2, 'Expense', 'Debit', '635', TRUE),

-- Sales Expenses (641)
('641', 'Chi phí bán hàng', 1, 'Expense', 'Debit', '', TRUE),
('6411', 'Chi phí nhân viên', 2, 'Expense', 'Debit', '641', TRUE),
('6412', 'Chi phí vật liệu', 2, 'Expense', 'Debit', '641', TRUE),
('6413', 'Chi phí công cụ', 2, 'Expense', 'Debit', '641', TRUE),
('6414', 'Chi phí khấu hao TSCĐ', 2, 'Expense', 'Debit', '641', TRUE),
('6415', 'Chi phí thuê hoạt động', 2, 'Expense', 'Debit', '641', TRUE),
('6416', 'Chi phí bảo hiểm', 2, 'Expense', 'Debit', '641', TRUE),
('6417', 'Chi phí dịch vụ mua ngoài', 2, 'Expense', 'Debit', '641', TRUE),
('6418', 'Chi phí khác', 2, 'Expense', 'Debit', '641', TRUE),

-- Administrative Expenses (642)
('642', 'Chi phí quản lý doanh nghiệp', 1, 'Expense', 'Debit', '', TRUE),
('6421', 'Chi phí nhân viên', 2, 'Expense', 'Debit', '642', TRUE),
('6422', 'Chi phí vật liệu', 2, 'Expense', 'Debit', '642', TRUE),
('6423', 'Chi phí công cụ', 2, 'Expense', 'Debit', '642', TRUE),
('6424', 'Chi phí khấu hao TSCĐ', 2, 'Expense', 'Debit', '642', TRUE),
('6425', 'Thuế, phí, lệ phí', 2, 'Expense', 'Debit', '642', TRUE),
('6426', 'Chi phí dự phòng', 2, 'Expense', 'Debit', '642', TRUE),
('6427', 'Chi phí dịch vụ mua ngoài', 2, 'Expense', 'Debit', '642', TRUE),
('6428', 'Chi phí khác', 2, 'Expense', 'Debit', '642', TRUE)

ON DUPLICATE KEY UPDATE Name = VALUES(Name);

-- =====================================================
-- OTHER INCOME/EXPENSE (7xxx, 8xxx)
-- =====================================================
INSERT INTO Accounts (Code, Name, Level, Type, NormalBalance, ParentCode, IsPostable) VALUES
-- Other Income (71x)
('711', 'Thu nhập khác', 1, 'Revenue', 'Credit', '', TRUE),

-- Other Expenses (81x)
('811', 'Chi phí khác', 1, 'Expense', 'Debit', '', TRUE),

-- Income Tax Expense (821)
('821', 'Chi phí thuế TNDN', 1, 'Expense', 'Debit', '', TRUE),
('8211', 'Chi phí thuế TNDN hiện hành', 2, 'Expense', 'Debit', '821', TRUE),
('8212', 'Chi phí thuế TNDN hoãn lại', 2, 'Expense', 'Debit', '821', TRUE),

-- Profit/Loss (91x, 99x)
('911', 'Xác định kết quả kinh doanh', 1, 'Expense', 'Debit', '', TRUE),
('9111', 'Kết quả hoạt động KD', 2, 'Expense', 'Debit', '911', TRUE),
('9112', 'Kết quả hoạt động tài chính', 2, 'Expense', 'Debit', '911', TRUE),
('9113', 'Kết quả hoạt động khác', 2, 'Expense', 'Debit', '911', TRUE),
('9114', 'Kết quả trước thuế', 2, 'Expense', 'Debit', '911', TRUE)

ON DUPLICATE KEY UPDATE Name = VALUES(Name);