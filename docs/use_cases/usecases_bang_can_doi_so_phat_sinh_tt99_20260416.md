# Use Cases: Bảng Cân đối Số Phát sinh (Trial Balance)
*Based on TT99/2025 - Mẫu S06-DN*

---

## Overview

Bảng cân đối số phát sinh là sổ kế toán phản ánh tổng quát tình hình tăng giảm và hiện có về tài sản và nguồn vốn của đơn vị trong kỳ báo cáo và từ đầu năm đến cuối kỳ báo cáo. Số liệu trên Bảng cân đối số phát sinh là căn cứ để kiểm tra, verify tính đúng đắn của việc ghi sổ kế toán và lập Bảng cân đối kế toán, Báo cáo kết quả hoạt động kinh doanh.

---

## TB01 - Lập Bảng Cân đối Số Phát sinh

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán viên / `Secondary:` Kế toán trưởng |
| **Mục tiêu** | Lập Bảng CĐPS tổng hợp số dư và số phát sinh |
| **Tiên quyết** | Đã hoàn thành ghi Sổ Cái, kiểm tra đối chiếu |
| **Kích hoạt** | Cuối tháng/quý |

#### Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Chọn kỳ báo cáo (tháng/quý) | |
| 2 | | Truy vấn Sổ Cái của tất cả TK cấp 2 |
| 3 | | Tính tổng số dư đầu kỳ (cột 1: Nợ, cột 2: Có) |
| 4 | | Tính tổng số phát sinh trong kỳ (cột 3: Nợ, cột 4: Có) |
| 5 | | Tính số dư cuối kỳ (cột 5: Nợ, cột 6: Có) |
| 6 | | Hiển thị Bảng CĐPS theo mẫu S06-DN |

#### Công thức tính số dư cuối kỳ
- Cột 5 (Dư Nợ cuối) = MAX(Dư Nợ đầu + PS Nợ - Dư Có đầu - PS Có, 0)
- Cột 6 (Dư Có cuối) = MAX(Dư Có đầu + PS Có - Dư Nợ đầu - PS Nợ, 0)

#### ⚠️ Luồng ngoại lệ
| Bước | Điều kiện | Xử lý |
|------|-----------|-------|
| 3-4 | Tổng PS Nợ ≠ Tổng PS Có | Cảnh báo chênh lệch, yêu cầu kiểm tra lại |

---

## TB02 - Kiểm tra Đối chiếu Số liệu

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán trưởng |
| **Mục tiêu** | Verify số liệu Bảng CĐPS khớp với Sổ Cái |
| **Tiên quyết** | Đã lập Bảng CĐPS |
| **Kích hoạt** | Trước khi duyệt báo cáo |

#### Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Chọn "Đối chiếu" | |
| 2 | | So sánh từng TK trên Bảng CĐPS với Sổ Cái |
| 3 | | Hiển thị các TK có chênh lệch (nếu có) |
| 4 | | Tính tổng kiểm tra: Tổng dư Nợ = Tổng dư Có |

#### ⚠️ Luồng ngoại lệ
| Bước | Điều kiện | Xử lý |
|------|-----------|-------|
| 4 | Tổng dư Nợ ≠ Tổng dư Có | Báo lỗi, dừng duyệt |

---

## TB03 - In Bảng Cân đối Số Phát sinh

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán viên / `Secondary:` Kế toán trưởng |
| **Mục tiêu** | Xuất Bảng CĐPS để lưu trữ hoặc nộp |
| **Tiên quyết** | Đã kiểm tra đối chiếu, đã duyệt |
| **Kích hoạt** | Cuối tháng/quý |

#### Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Chọn "In Bảng CĐPS" | |
| 2 | | Hiển thị preview với header: đơn vị, địa chỉ, mẫu số S06-DN |
| 3 | | Xuất file PDF/Excel |

---

## TB04 - Lưu trữ Số liệu Cho Kỳ Sau

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Hệ thống |
| **Mục tiêu** | Lưu số dư cuối kỳ làm số dư đầu kỳ sau |
| **Tiên quyết** | Đã in/complete Bảng CĐPS |
| **Kích hoạt** | Sau khi in thành công |

#### Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | | Copy cột 5,6 (dư cuối) vào cột 1,2 (dư đầu) của kỳ tiếp theo |
| 2 | | Xác nhận đã lưu |

---

## Cấu trúc Bảng CĐPS (Mẫu S06-DN)

| Cột | Nội dung |
|-----|----------|
| A | Số hiệu tài khoản |
| B | Tên tài khoản kế toán |
| 1 | Số dư đầu tháng - Nợ |
| 2 | Số dư đầu tháng - Có |
| 3 | Số phát sinh trong tháng - Nợ |
| 4 | Số phát sinh trong tháng - Có |
| 5 | Số dư cuối tháng - Nợ |
| 6 | Số dư cuối tháng - Có |

---

## Định khoản mẫu (Journal Entry Mapping)

| Nghiệp vụ | Debit | Credit | Ghi chú |
|-----------|-------|--------|---------|
| Kết chuyển số dư cuối kỳ | TK có số dư Nợ | TK có số dư Có | Chuẩn bị cho kỳ sau |

---

## Reference

| Document | Location |
|----------|----------|
| Mẫu S06-DN | ketoanthienung.net/mau-bang-can-doi-so-phat-sinh-s06-dn-theo-thong-tu-99.htm |
| Cách lập BĐPS | ketoanthienung.net/cach-lap-bang-can-doi-so-phat-sinh-tai-khoan-tren-excel.htm |

---

*Extracted from: ketoanthienung.net*
*Date: 2026-04-16*