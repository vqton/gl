# Use Cases: Payroll & Tiền lương (L01-L07)
*Based on TT99/2025 - Lao động, BHXH, TNCN*

---

## L01 - Quản lý Hợp đồng Lao động

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` HR / `Secondary:` Quản lý |
| **Mục tiêu** | Tạo, lưu trữ và quản lý hợp đồng lao động |
| **Tiên quyết** | Người lao động đã được tuyển dụng |
| **Kích hoạt** | Ký hợp đồng thử việc hoặc chính thức |

### Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | HR | Tạo hợp đồng (thử việc/chính thức) |
| 2 | | Nhập thông tin: họ tên, vị trí, lương, thời hạn |
| 3 | | Lưu vào hệ thống |
| 4 | | Theo dõi ngày hết hạn |

### Luồng ngoại lệ
| Bước | Điều kiện | Xử lý |
|------|-----------|-------|
| 4 | Hết hạn | Cảnh báo gia hạn |

---

## L02 - Tính Lương Hàng tháng

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán |
| **Mục tiêu** | Tính lương thực nhận cho từng NV |
| **Tiên quyết** | Bảng chấm công đã duyệt |
| **Kích hoạt** | Cuối tháng |

### Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | | Lấy dữ liệu chấm công |
| 2 | | Áp dụng công thức: Lương = Lương CB × Ngày làm / Tổng ngày |
| 3 | | Tính phụ cấp, thưởng |
| 4 | | Tính khấu trừ (BHXH, BHYT, BHTN, TNCN) |
| 5 | | Tính lương thực nhận |

### Công thức
- Lương tháng = Lương cơ bản / 26 × Số ngày làm thực tế
- Tăng ca (150%-300% tùy thời gian)
- Phụ cấp xăng xe, điện thoại, ăn trưa...

---

## L03 - Hạch toán Tiền lương

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán |
| **Mục tiêu** | Ghi nhận chi phí lương vào sổ kế toán |
| **Tiên quyết** | Bảng lương đã tính xong |
| **Kích hoạt** | Cuối tháng |

### Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | | Tính các khoản trích theo lương |
| 2 | | Định khoản Nợ 622 / Có 334 |
| 3 | | Định khoản trích BH: Nợ 622 / Có 338 |
| 4 | | Thanh toán: Nợ 334 / Có 111, 112 |

### Tỷ lệ trích 2026
| Khoản trích | DN đóng | NLĐ đóng | Tổng |
|------------|--------|----------|------|
| BHXH | 17.5% | 8% | 25.5% |
| BHYT | 3% | 1.5% | 4.5% |
| BHTN | 1% | 1% | 2% |
| KPCĐ | 2% | - | 2% |

---

## L04 - Tính và Khấu trừ Thuế TNCN

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán |
| **Mục tiêu** | Tính thuế TNCN theo biểu thuế lũy tiến |
| **Tiên quyết** | Lương đã tính, có MST cá nhân |
| **Kích hoạt** | Cuối tháng |

### Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | | Tính thu nhập chịu thuế = Lương - Giảm trừ - BHXH |
| 2 | | Áp dụng biểu thuế lũy tiến |
| 3 | | Tính thuế phải nộp |
| 4 | | Khấu trừ vào lương |

### Biểu thuế TNCN 2026
| Thu nhập tháng | Thuế suất | Khoản giảm trừ |
|---------------|----------|---------------|
| ≤ 5tr | 5% | 0 |
| 5-10tr | 10% | 250,000 |
| 10-18tr | 15% | 750,000 |
| 18-32tr | 20% | 1,650,000 |
| 32-52tr | 25% | 3,250,000 |
| 52-80tr | 30% | 5,850,000 |
| > 80tr | 35% | 9,850,000 |

---

## L05 - Nộp BHXH, BHYT, BHTN

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán |
| **Mục tiêu** | Nộp các khoản BH đúng hạn |
| **Tiên quyết** | Đã tính và trích BH |
| **Kích hoạt** | Hàng tháng, trước ngày 30 |

### Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | | Tổng hợp số tiền BH phải nộp |
| 2 | | Tạo file chuyển khoản |
| 3 | | Nộp qua cổng BHXH điện tử |
| 4 | | Lưu chứng từ nộp |

### Thời hạn nộp
- BHXH, BHYT, BHTN: Trước ngày 30 tháng tiếp theo
- Chậm nộp: Phạt 12%/năm

---

## L06 - Lập Bảng Lương

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán / `Secondary:` KT trưởng |
| **Mục tiêu** | Tổng hợp lương tháng |
| **Tiên quyết** | Đã tính lương từng NV |
| **Kích hoạt** | Cuối tháng |

### Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | | Tổng hợp từng nhân viên |
| 2 | | Tính tổng chi phí lương |
| 3 | | Tính tổng BH, thuế |
| 4 | | In bảng lương |
| 5 | KT trưởng | Ký duyệt |

### Cấu trúc Bảng Lương
| STT | Họ tên | Chức vụ | Lương CB | Phụ cấp | Thưởng | BHXH | Thuế TNCN | Thực nhận |
|-----|--------|---------|---------|----------|--------|------|----------|-----------|-----------|

---

## L07 - Chi Trả Lương

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán / `Secondary:` Thủ quỹ |
| **Mục tiêu** | Chi trả lương cho NV |
| **Tiên quyết** | Bảng lương đã duyệt |
| **Kích hoạt** | Ngày trả lương |

### Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | | Lập phiếu chi (TM) hoặc chuyển khoản |
| 2 | KT trưởng | Ký duyệt |
| 3 | Thủ quỹ | Chi tiền / Chuyển khoản |
| 4 | | Ghi sổ quỹ |

### Định khoản
| Nghiệp vụ | Debit | Credit |
|-----------|-------|--------|
| Chi TM | 334 | 111 |
| Chuyển khoản | 334 | 112 |

---

## Reference

| Document | Location |
|----------|----------|
| Tính lương | ketoanthienung.net/cach-tinh-luong-theo-gio-ngay-tuan-thang |
| BHXH | ketoanthienung.net/cach-hach-toan-tien-luong-va-cac-khoan-trich-theo-luong |
| TNCN | ketoanthienung.net/cach-tinh-thue-thu-nhap-ca-nhan-moi-nhat |

---

*Extracted from: ketoanthienung.net*
*Date: 2026-04-16*