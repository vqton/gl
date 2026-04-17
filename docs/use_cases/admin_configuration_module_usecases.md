# Use Cases - Admin & Configuration Module

## Mô tả Module

Module quản trị và cấu hình hệ thống ERP, dựa trên Thông tư 99/2025/TT-BTC và best practices từ NetSuite, ERPNext, SAP, Oracle Fusion.

**Mã module**: CONFIG  
**Phiên bản**: 1.0  
**Ngày**: 2026-04-17

---

## 1. Company Setup (C01-C08)

### C01: Tạo/Cập nhật thông tin công ty

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | C01 |
| Actor | Admin |
| Mục tiêu | Thiết lập thông tin công ty |
| Pre-condition | User có quyền ADMIN |
| Post-condition | Lưu thông tin vào database |

**业务流程**:
1. Admin truy cập trang Company Settings
2. Nhập thông tin: Tên công ty, Địa chỉ, MST, Điện thoại, Email
3. Upload logo công ty
4. Nhấn Save
5. Hệ thống lưu và xác nhận

**Validation**:
- Tên công ty: Bắt buộc, tối đa 200 ký tự
- MST: Định dạng 10 số
- Email: Định dạng hợp lệ

---

### C02: Cấu hình năm tài chính

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | C02 |
| Actor | Admin, Accountant |
| Mục tiêu | Thiết lập kỳ kế toán |
| Pre-condition | User có quyền ACCOUNTANT |
| Post-condition | Tạo 12 kỳ kế toán |

**业务流程**:
1. Truy cập Fiscal Year Settings
2. Chọn ngày bắt đầu (01/01 hoặc 01/04)
3. Chọn số kỳ (12 tháng hoặc 13 kỳ 4-4-4-1)
4. Hệ thống tự động tạo các period
5. Lưu cấu hình

**Validation**:
- Ngày bắt đầu phải là ngày đầu tháng
- Kỳ phải khớp với năm dương lịch

---

### C03: Cấu hình tiền tệ

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | C03 |
| Actor | Admin |
| Mục tiêu | Thiết lập tiền tệ |
| Pre-condition | User có quyền ADMIN |
| Post-condition | Lưu cấu hình tiền tệ |

**业务流程**:
1. Truy cập Currency Settings
2. Chọn tiền tệ cơ sở (VND)
3. Thêm tiền tệ phụ (USD, EUR,...)
4. Cập nhật tỷ giá
5. Lưu cấu hình

---

### C04: Cấu hình định dạng

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | C04 |
| Actor | Admin |
| Mục tiêu | Thiết lập định dạng |
| Pre-condition | User có quyền ADMIN |
| Post-condition | Lưu định dạng |

**业务流程**:
1. Truy cập Format Settings
2. Chọn định dạng ngày (dd/MM/yyyy)
3. Chọn định dạng số (#,##0.00)
4. Chọn múi giờ (Asia/Ho_Chi_Minh)
5. Lưu cấu hình

---

### C05: Cấu hình số phiếu tự động

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | C05 |
| Actor | Admin |
| Mục tiêu | Thiết lập quy tắc đánh số |
| Pre-condition | User có quyền ADMIN |
| Post-condition | Lưu quy tắc |

**业务流程**:
1. Truy cập Numbering Settings
2. Tạo quy tắc: Prefix + Running Number
3. Ví dụ: BL-{YYYY}-{MM}-{0000} cho Bút toán
4. Gán cho loại chứng từ
5. Lưu cấu hình

---

### C06: Cấu hình nhiều công ty

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | C06 |
| Actor | Admin |
| Mục tiêu | Thiết lập đa công ty |
| Pre-condition | User có quyền ADMIN |
| Post-condition | Tạo công ty con |

---

### C07: Thiết lập lịch làm việc

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | C07 |
| Actor | Admin |
| Mục tiêu | Cấu hình ngày nghỉ |
| Pre-condition | User có quyền ADMIN |
| Post-condition | Lưu calendar |

---

### C08: Thiết lập khoảng thời gian

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | C08 |
| Actor | Admin |
| Mục tiêu | Cấu hình working hours |
| Pre-condition | User có quyền ADMIN |
| Post-condition | Lưu hours |

---

## 2. System Parameters (S01-S08)

### S01: Cấu hình Session

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | S01 |
| Actor | Admin |
| Mục tiêu | Bảo mật phiên làm việc |
| Pre-condition | User có quyền ADMIN |
| Post-condition | Lưu session settings |

**业务流程**:
1. Truy cập Security Settings
2. Đặt Session Timeout (phút)
3. Đặt số đăng nhập tối đa
4. Bật/Tắt Remember Me
5. Lưu cấu hình

---

### S02: Cấu hình Password Policy

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | S02 |
| Actor | Admin |
| Mục tiêu | Chính sách mật khẩu |
| Pre-condition | User có quyền ADMIN |

**业务流程**:
1. Truy cập Password Policy
2. Đặt độ dài tối thiểu (8 ký tự)
3. Yêu cầu: uppercase, lowercase, số, ký tự đặc biệt
4. Đặt ngày hết hạn (90 ngày)
5. Số mật khẩu gần nhất không được dùng lại (5)
6. Lưu chính sách

---

### S03: Cấu hình Email/SMTP

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | S03 |
| Actor | Admin |
| Mục tiêu | Thiết lập SMTP |

**业务流程**:
1. Truy cập Email Settings
2. Nhập SMTP Server, Port
3. Nhập Username, Password
4. Thiết lập From Email, From Name
5. Gửi email test
6. Lưu cấu hình

---

### S04: Bật/Tắt modules

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | S04 |
| Actor | Admin |
| Mục tiêu | Kích hoạt modules |
| Pre-condition | User có quyền ADMIN |

**业务流程**:
1. Truy cập Module Settings
2. Liệt kê các modules có sẵn
3. Bật/Tắt modules cần thiết:
   - Sales & Revenue (S01-S06)
   - Purchasing & Inventory (P01-P05)
   - Cash & Bank (T01-T05)
   - Fixed Assets (A01-A06)
   - Payroll (L01-L07)
   - Tax (X01-X05)
   - E-Invoice (EI01-EI07)
4. Lưu cấu hình

---

### S05: Cấu hình Audit Trail

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | S05 |
| Actor | Admin |
| Mục tiêu | Log hoạt động |

**业务流程**:
1. Truy cập Audit Settings
2. Bật Audit Trail
3. Chọn log levels: Errors, Warnings, All
4. Đặt số ngày lưu log
5. Export log
6. Lưu cấu hình

---

### S06: Cấu hình Backup

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | S06 |
| Actor | Admin |
| Mục tiêu | Thiết lập backup |

**业务流程**:
1. Truy cập Backup Settings
2. Đặt lịch auto-backup
3. Chọn thư mục backup
4. Test backup
5. Lưu cấu hình

---

### S07: Cấu hình Scheduler

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | S07 |
| Actor | Admin |
| Mục tiêu | Job tự động |

**业务流程**:
1. Truy cập Scheduler Settings
2. Đăng ký jobs:
   - Auto-post transactions
   - Calculate depreciation
   - Send reminders
3. Đặt cron schedule
4. Enable/Disable jobs
5. View job logs
6. Lưu cấu hình

---

### S08: Cấu hình Cache

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | S08 |
| Actor | Admin |
| Mục tiêu | Quản lý cache |

---

## 3. User & Access Management (U01-U12)

### U01: Tạo user mới

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | U01 |
| Actor | Admin |
| Mục tiêu | Tạo tài khoản user |

**业务流程**:
1. Truy cập User List
2. Nhấn Add User
3. Nhập: Username, Email, FullName
4. Nhập Password tạm
5. Assign Roles
6. Nhấn Create
7. Gửi email thông báo

---

### U02: Cập nhật thông tin user

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | U02 |
| Actor | Admin |
| Mục tiêu | Sửa thông tin user |

---

### U03: Kích hoạt/Vô hiệu user

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | U03 |
| Actor | Admin |
| Mục tiêu | Quản lý trạng thái |

---

### U04: Đổi mật khẩu user

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | U04 |
| Actor | Admin |
| Mục tiêu | Reset password |

---

### U05: Reset mật khẩu (admin)

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | U05 |
| Actor | Admin |
| Mục tiêu | Admin reset password |

---

### U06: Gán role cho user

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | U06 |
| Actor | Admin |
| Mục tiêu | Phân quyền |

---

### U07: Xóa role khỏi user

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | U07 |
| Actor | Admin |
| Mục tiêu | Thu hồi quyền |

---

### U08: Tạo role mới

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | U08 |
| Actor | Admin |
| Mục tiêu | Tạo role |

---

### U09: Cấu quyền cho role

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | U09 |
| Actor | Admin |
| Mục tiêu | Gán permissions |

---

### U10: Xem lịch sử đăng nhập

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | U10 |
| Actor | Admin |
| Mục tiêu | Xem login history |

---

### U11: Xem danh sách active sessions

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | U11 |
| Actor | Admin |
| Mục tiêu | Session management |

---

### U12: Force logout user

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | U12 |
| Actor | Admin |
| Mục tiêu | Terminate session |

---

## 4. Data Management (D01-D08)

### D01: Import data từ CSV/Excel

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | D01 |
| Actor | Admin, Accountant |
| Mục tiêu | Import dữ liệu |

**业务流程**:
1. Truy cập Data Import
2. Chọn loại data (Accounts, Customers, Suppliers,...)
3. Upload file CSV/Excel
4. Map fields
5. Preview data
6. Validate
7. Import
8. View report

---

### D02: Export data

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | D02 |
| Actor | Admin, Accountant, Viewer |
| Mục tiêu | Export dữ liệu |

---

### D03: Bulk update

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | D03 |
| Actor | Admin |
| Mục tiêu | Update nhiều records |

---

### D04: Merge duplicates

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | D04 |
| Actor | Admin |
| Mục tiêu | Gộp trùng lặp |

---

### D05: Archive data

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | D05 |
| Actor | Admin |
| Mục tiêu | Lưu trữ data cũ |

---

### D06: Purge old data

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | D06 |
| Actor | Admin |
| Mục tiêu | Xóa data hết hạn |

---

### D07: Manual backup

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | D07 |
| Actor | Admin |
| Mục tiêu | Manual backup |

---

### D08: Restore backup

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | D08 |
| Actor | Admin |
| Mục tiêu | Khôi phục backup |

---

## 5. Audit & Compliance (A01-A06)

### A01: Xem audit trail

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | A01 |
| Actor | Admin, Auditor |
| Mục tiêu | Xem log thay đổi |

---

### A02: Export audit log

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | A02 |
| Actor | Admin, Auditor |
| Mục tiêu | Export audit log |

---

### A03: Xem báo cáo hoạt động user

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | A03 |
| Actor | Admin |
| Mục tiêu | Activity report |

---

### A04: Security audit

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | A04 |
| Actor | Admin |
| Mục tiêu | Review quyền |

---

### A05: Review role assignments

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | A05 |
| Actor | Admin |
| Mục tiêu | Kiểm tra phân quyền |

---

### A06: Compliance report

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | A06 |
| Actor | Admin, Auditor |
| Mục tiêu | Báo cáo tuân thủ |

---

## 6. System Health (H01-H06)

### H01: Xem system status

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | H01 |
| Actor | Admin |
| Mục tiêu | Dashboard |

---

### H02: Xem job scheduler status

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | H02 |
| Actor | Admin |
| Mục tiêu | Monitoring |

---

### H03: Clear cache

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | H03 |
| Actor | Admin |
| Mục tiêu | Maintenance |

---

### H04: Re-index database

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | H04 |
| Actor | Admin |
| Mục tiêu | Performance |

---

### H05: Xem version info

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | H05 |
| Actor | Admin |
| Mục tiêu | System info |

---

### H06: About & Support

| Thuộc tính | Giá trị |
|-----------|--------|
| ID | H06 |
| Actor | Admin |
| Mục tiêu | Support info |

---

## Tổng kết Use Cases

| Nhóm | Số lượng |
|------|---------|
| Company Setup | 8 |
| System Parameters | 8 |
| User & Access | 12 |
| Data Management | 8 |
| Audit & Compliance | 6 |
| System Health | 6 |
| **Tổng** | **48** |

---

## Role Permissions Mapping

| Use Case | ADMIN | ACCOUNTANT | BOOKKEEPER | SALES | WAREHOUSE | VIEWER |
|---------|-------|-----------|------------|------|----------|--------|
| C01-C08 | ✓ | ✓ | - | - | - | - |
| S01-S08 | ✓ | - | - | - | - | - |
| U01-U12 | ✓ | - | - | - | - | - |
| D01-D08 | ✓ | ✓ | - | - | - | - |
| A01-A06 | ✓ | - | - | - | - | ✓ |
| H01-H06 | ✓ | - | - | - | - | - |

---

## References

- TT99/2025/TT-BTC - Chế độ kế toán doanh nghiệp
- ERPNext System Settings
- NetSuite Administration Guide
- Oracle Fusion Securing ERP
- SAP S/4HANA User Management