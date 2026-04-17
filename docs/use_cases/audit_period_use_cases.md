# Phase 4: Compliance & Audit - Use Cases
*Based on TT99/2025 Article 18 - Audit Trail & Period Locking*

---

## Overview

Phase 4 implements two critical components required for production:
1. **Audit Trail Service** - Log all accounting changes per TT99/2025
2. **Period Locking Service** - Control posting to accounting periods

---

## AUDIT TRAIL (AT01-AT03)

### AT01 - Log Transaction Entry
**Mục tiêu**: Ghi lại mọi thay đổi kế toán theo quy định TT99/2025 Điều 18

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán viên / `Secondary:` Hệ thống |
| **Mục tiêu** | Tạo audit log khi có bút toán mới |
| **Tiên quyết** | User đã đăng nhập, transaction hợp lệ |
| **Kích hoạt** | Bút toán được tạo hoặc cập nhật |

#### Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Tạo bút toán | |
| 2 | | Kiểm tra transaction hợp lệ |
| 3 | | Tạo AuditLog với: UserId, Timestamp, OldValues, NewValues |
| 4 | | Lưu vào database |
| 5 | | Trả về transaction đã tạo + audit log ID |

#### ⚠️ Luồng ngoại lệ
| Bước gốc | Điều kiện | Xử lý |
|----------|-----------|-------|
| 1 | Transaction không hợp lệ | Throw exception, không tạo audit |
| 2 | User không đăng nhập | Return error "Unauthorized" |
| 3 | Database lỗi | Retry 3 lần, sau đó throw exception |

---

### AT02 - Query Audit History
**Mục tiêu**: Truy vấn lịch sử thay đổi theo thời gian, user, hoặc record

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán trưởng / `Secondary:` Auditor |
| **Mục tiêu** | Xem lịch sử thay đổi của một record |
| **Tiên quyết** | Có quyền truy cập audit |
| **Kích hoạt** | User truy vấn audit theo filter |

#### Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Gửi query (recordId hoặc dateRange) | |
| 2 | | Validate query parameters |
| 3 | | Truy vấn audit_logs table |
| 4 | | Trả về danh sách audit entries |

---

### AT03 - Generate Audit Report
**Mục tiêu**: Tạo báo cáo audit cho kỳ kế toán

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán trưởng / `Secondary:` Auditor |
| **Mục tiêu** | Xuất báo cáo audit theo kỳ |
| **Tiên quyết** | Kỳ kế toán đã đóng |
| **Kích hoạt** | User yêu cầu báo cáo |

---

## PERIOD LOCKING (PL01-PL03)

### PL01 - Open Accounting Period
**Mục tiêu**: Mở kỳ kế toán mới để ghi nhận nghiệp vụ

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán trưởng |
| **Mục tiêu** | Cho phép ghi bút toán trong kỳ |
| **Tiên quyết** | Kỳ trước đã đóng |
| **Kích hoạt** | Bắt đầu tháng/quý mới |

#### Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Gửi yêu cầu mở kỳ (2026-04) | |
| 2 | | Kiểm tra kỳ trước (2026-03) đã đóng |
| 3 | | Tạo AccountingPeriod với status = OPEN |
| 4 | | Trả về period đã tạo |

---

### PL02 - Close Accounting Period
**Mục tiêu**: Đóng kỳ kế toán, ngăn ghi bút toán bổ sung

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán trưởng |
| **Mục tiêu** | Khóa kỳ kế toán, không cho phép sửa |
| **Tiên quyết** | Đã chạy kết chuyển cuối kỳ |
| **Kích hoạt** | Kết thúc tháng/quý |

#### Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Gửi yêu cầu đóng kỳ (2026-03) | |
| 2 | | Kiểm tra đã chạy G01-G04 |
| 3 | | Cập nhật status = CLOSED |
| 4 | | Lưu audit log |
| 5 | | Trả về period đã đóng |

---

### PL03 - Validate Period Before Posting
**Mục tiêu**: Kiểm tra kỳ kế toán trước khi ghi bút toán

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Hệ thống |
| **Mục tiêu** | Ngăn ghi bút toán vào kỳ đóng |
| **Tiên quyết** | Bút toán đã được validate |
| **Kích hoạt** | Trước khi lưu transaction |

#### Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Gửi transaction với periodId | |
| 2 | | Truy vấn AccountingPeriod |
| 3 | | Kiểm tra status == OPEN |
| 4 | | Cho phép lưu hoặc reject |

#### ⚠️ Luồng ngoại lệ
| Bước | Điều kiện | Xử lý |
|------|-----------|-------|
| 3 | Status = CLOSED | Reject: "Period is closed" |
| 3 | Status = LOCKED | Reject: "Period is locked" |
| 3 | Period not found | Reject: "Period does not exist" |

---

## Định khoản mẫu (Journal Entry Mapping)

### Audit Log Entry
| Debit | Credit | Description |
|-------|--------|-------------|
| 000 | 000 | Không ảnh hưởng sổ cái |

### Period Status Change
| Debit | Credit | Description |
|-------|--------|-------------|
| 000 | 000 | Không ảnh hưởng sổ cái |

---

## File Reference

| Document | Location |
|----------|----------|
| Complete Use Cases | docs/GL_USE_CASES_COMPLETE.md |
| Production Readiness | docs/PRODUCTION_READINESS.md |
| Implementation Roadmap | docs/roadmaps/implementation_roadmap.md |

---

*Last Updated: April 2026*
*Phase 4: Compliance & Audit*