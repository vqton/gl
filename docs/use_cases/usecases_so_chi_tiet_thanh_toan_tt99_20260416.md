# Use Cases: Sổ Chi tiết Thanh toán (Subsidiary Ledger - AR/AP)
*Based on TT99/2025 - Mẫu S12-DNN (S31-DN)*

---

## Overview

Sổ chi tiết thanh toán với người mua (người bán) dùng để theo dõi việc thanh toán với người mua (người bán) theo từng đối tượng, từng thời hạn thanh toán. Áp dụng cho TK 131 (Phải thu khách hàng) và TK 331 (Phải trả người bán).

---

## SL01 - Mở Sổ Chi tiết Thanh toán

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán viên |
| **Mục tiêu** | Mở sổ chi tiết theo dõi cho từng khách hàng/nhà cung cấp |
| **Tiên quyết** | Đã có danh mục KH/NCC |
| **Kích hoạt** | Bắt đầu kỳ kế toán mới |

#### Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Chọn Tài khoản (131 hoặc 331) | |
| 2 | Nhập mã KH/NCC | |
| 3 | | Kiểm tra tồn tại trong danh mục |
| 4 | Nhập thông tin: tên, địa chỉ, MST | |
| 5 | | Tạo trang sổ chi tiết |

---

## SL02 - Ghi Phát sinh Trong kỳ

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán viên |
| **Mục tiêu** | Ghi các nghiệp vụ phát sinh |
| **Tiên quyết** | Đã mở sổ cho KH/NCC |
| **Kích hoạt** | Có nghiệp vụ bán hàng/mua hàng |

#### Luồng chính (TK 131 - Phải thu KH)
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Ghi ngày, tháng vào cột Ngày, tháng ghi sổ | |
| 2 | Ghi số hiệu chứng từ vào cột Chứng từ | |
| 3 | Ghi nội dung nghiệp vụ vào cột Diễn giải | |
| 4 | Ghi TK đối ứng vào cột TK đối ứng | |
| 5 | Ghi số tiền vào cột Số phát sinh (Nợ/Có) | |
| 6 | Tính số dư cuối | |

#### Định khoản mẫu (TK 131)
| Nghiệp vụ | Debit | Credit |
|-----------|-------|--------|
| Bán chịu | 131 | 511/515 |
| Thu tiền | 111/112 | 131 |
| Giảm giá | 531 | 131 |
| Trả hàng | 131 | 531 |

#### Luồng chính (TK 331 - Phải trả NCC)
| Nghiệp vụ | Debit | Credit |
|-----------|-------|--------|
| Mua chịu | 156/152/211 | 331 |
| Trả tiền | 331 | 111/112 |
| Giảm giá | 331 | 531 |

---

## SL03 - Theo dõi Thời hạn Thanh toán

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán viên |
| **Mục tiêu** | Theo dõi kỳ hạn thu hồi/trả |
| **Tiên quyết** | Có phát sinh |
| **Kích hoạt** | Kiểm tra định kỳ |

#### Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Chọn "Theo dõi kỳ hạn" | |
| 2 | | Hiển thị danh sách theo kỳ hạn: ≤12 tháng, >12 tháng |
| 3 | | Cảnh báo các khoản quá hạn |

#### ⚠️ Luồng ngoại lệ
| Bước | Điều kiện | Xử lý |
|------|-----------|-------|
| 3 | Quá hạn >12 tháng | Chuyển sang TK phải thu dài hạn |
| 3 | Khó đòi | Trích lập dự phòng |

---

## SL04 - Đối chiếu Công nợ

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán viên / `Secondary:` KH/NCC |
| **Mục tiêu** | Đối chiếu số liệu công nợ |
| **Tiên quyết** | Cuối kỳ |
| **Kích hoạt** | Định kỳ hoặc theo yêu cầu |

#### Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Chọn "Đối chiếu công nợ" | |
| 2 | | Xuất phiếu đối chiếu |
| 3 | Gửi cho KH/NCC | |
| 4 | Xác nhận từ KH/NCC | |
| 5 | | Điều chỉnh nếu có chênh lệch |

---

## SL05 - In Sổ Chi tiết Thanh toán

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán viên |
| **Mục tiêu** | In sổ để lưu trữ |
| **Tiên quyết** | Đã ghi xong phát sinh |
| **Kích hoạt** | Cuối tháng/quý |

#### Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Chọn "In Sổ" | |
| 2 | | Kiểm tra đã khóa sổ |
| 3 | | Xuất file theo mẫu S12-DNN |

---

## Cấu trúc Sổ (Mẫu S12-DNN)

| Cột | Nội dung |
|-----|----------|
| Ngày, tháng ghi sổ | |
| Chứng từ | Số hiệu, ngày tháng |
| Diễn giải | Nội dung nghiệp vụ |
| TK đối ứng | |
| Thời hạn được chiết khấu | |
| Số phát sinh | Nợ / Có |
| Số dư | Nợ / Có |

---

## Reference

| Document | Location |
|----------|----------|
| Mẫu S12-DNN | ketoanthienung.net/so-chi-tiet-thanh-toan-voi-nguoi-mua-nguoi-ban.htm |
| TK 131 | ketoanthienung.net/hach-toan-tk-131-phai-thu-cua-khach-hang-theo-thong-tu-99.htm |

---

*Extracted from: ketoanthienung.net*
*Date: 2026-04-16*