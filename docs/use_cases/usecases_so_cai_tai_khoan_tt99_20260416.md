# Use Cases: Sổ Cái Tài khoản (General Ledger)
*Based on TT99/2025 - Phụ lục 4*

---

## Overview

Sổ Cái là sổ kế toán tổng hợp dùng để ghi chép các nghiệp vụ kinh tế, tài chính phát sinh trong niên độ kế toán theo tài khoản kế toán. Mỗi tài khoản được mở một hoặc một số trang liên tiếp trên Sổ Cái đủ để ghi chép trong một niên độ kế toán.

---

## UC-GL-01: Lập Sổ Cái theo Tài khoản

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán viên |
| **Mục tiêu** | Ghi lại phát sinh của một tài khoản cụ thể |
| **Tiên quyết** | Đã có số dư đầu kỳ hoặc có nghiệp vụ phát sinh |
| **Kích hoạt** | Bắt đầu tháng/quý mới |

#### Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Chọn tài khoản cần lập sổ | |
| 2 | | Hiển thị trang Sổ Cái với số hiệu TK, tên TK |
| 3 | Ghi ngày, tháng vào cột A | |
| 4 | Ghi số hiệu chứng từ vào cột B, C | |
| 5 | Ghi nội dung nghiệp vụ vào cột D | |
| 6 | Ghi số trang NKC vào cột E, số dòng vào cột G | |
| 7 | Ghi số hiệu TK đối ứng vào cột H | |
| 8 | Ghi số tiền Nợ/Có vào cột 1, 2 | |

#### ⚠️ Luồng ngoại lệ
| Bước | Điều kiện | Xử lý |
|------|-----------|-------|
| 1 | Tài khoản không tồn tại | Thông báo lỗi, yêu cầu chọn TK hợp lệ |
| 8 | Số tiền = 0 | Bỏ qua dòng này |

---

## UC-GL-02: Ghi Số dư đầu kỳ

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán viên |
| **Mục tiêu** | Ghi số dư đầu tháng/quý |
| **Tiên quyết** | Đã có số dư cuối kỳ trước |
| **Kích hoạt** | Đầu tháng mới |

#### Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Ghi "Số dư đầu năm" hoặc "Số phát sinh tháng trước" | |
| 2 | Ghi số dư Nợ hoặc Có vào dòng đầu tiên | |
| 3 | | Tự động cập nhật vào hệ thống |

---

## UC-GL-03: Tính Số phát sinh và Số dư cuối kỳ

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán viên / `Secondary:` Hệ thống |
| **Mục tiêu** | Tính tổng phát sinh Nợ, Có và số dư cuối kỳ |
| **Tiên quyết** | Đã ghi hết các nghiệp vụ trong tháng |
| **Kích hoạt** | Cuối tháng |

#### Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | | Tính tổng cộng số phát sinh Nợ (cột 1) |
| 2 | | Tính tổng cộng số phát sinh Có (cột 2) |
| 3 | | Tính số dư cuối kỳ theo công thức |
| 4 | | Ghi "Cộng số phát sinh tháng", "Số dư cuối tháng" |
| 5 | | Ghi "Cộng lũy kế từ đầu quý" |

#### Công thức tính số dư
- Nếu đầu kỳ Nợ: Dư cuối = Dư đầu + PS Nợ - PS Có
- Nếu đầu kỳ Có: Dư cuối = Dư đầu + PS Có - PS Nợ (nếu kết quả > 0, ngược lại là Nợ)

---

## UC-GL-04: In Sổ Cái

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán viên / `Secondary:` Kế toán trưởng |
| **Mục tiêu** | In Sổ Cái để lưu trữ hoặc nộp |
| **Tiên quyết** | Đã ghi xong các nghiệp vụ |
| **Kích hoạt** | Cuối tháng/quý |

#### Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Chọn "In Sổ Cái" | |
| 2 | | Kiểm tra đã khóa sổ chưa |
| 3 | | Hiển thị trang in với header: đơn vị, địa chỉ, mẫu số S03b-DNN |
| 4 | | Xuất file PDF/Excel |

#### ⚠️ Luồng ngoại lệ
| Bước | Điều kiện | Xử lý |
|------|-----------|-------|
| 2 | Chưa khóa sổ | Cảnh báo, vẫn cho phép in nháp |

---

## Định khoản mẫu (Journal Entry Mapping)

| Nghiệp vụ | Debit | Credit | Ghi chú |
|-----------|-------|--------|---------|
| Ghi sổ Cái theo NKC | TK phát sinh Nợ | TK phát sinh Có | Theo chứng từ gốc |
| Kết chuyển cuối kỳ | 911 | TK loại 6,7,8,9 | Ghi nhận KQKD |

---

## Reference

| Document | Location |
|----------|----------|
| Mẫu sổ S03b-DNN | ketoanthienung.net/mau-so-cai-tai-khoan-theo-hinh-thuc-nhat-ky-chung.htm |
| Cách lập Bảng CĐPS | ketoanthienung.net |

---

*Extracted from: ketoanthienung.net*
*Date: 2026-04-16*