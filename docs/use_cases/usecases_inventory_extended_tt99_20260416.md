# Use Cases: Inventory Extended (I04-I07)
*Based on TT99/2025 - Mẫu S11-DN*

---

## I04 - Kiểm kê Hàng tồn kho

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Thủ kho / `Secondary:` Kế toán |
| **Mục tiêu** | Xác định chênh lệch thực tế so với sổ sách |
| **Tiên quyết** | Đến kỳ kiểm kê (cuối năm hoặc định kỳ) |
| **Kích hoạt** | Lệnh kiểm kê từ KT trưởng |

### Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | KT trưởng | Ra lệnh kiểm kê, xác định thời gian, phạm vi |
| 2 | Thủ kho | Tiến hành kiểm đếm thực tế |
| 3 | | Lập Biên bản kiểm kê (số lượng thực tế) |
| 4 | Kế toán | Đối chiếu sổ sách vs thực tế |
| 5 | | Tính chênh lệch (nếu có) |

### Luồng ngoại lệ
| Bước | Điều kiện | Xử lý |
|------|-----------|-------|
| 5 | Thiếu hàng | Lập biên bản, xử lý theo quy định |
| 5 | Thừa hàng | Ghi nhận, điều chỉnh sổ |
| 5 | Hư hỏng | Đánh giá % hao hụt, xử lý |

### Định khoản xử lý
| Trường hợp | Debit | Credit |
|-------------|-------|--------|
| Thiếu | 6321 | 156 |
| Thừa | 156 | 6321 |

---

## I05 - Đánh giá Hàng tồn kho

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán |
| **Mục tiêu** | Xác định giá trị thuần có thể thực hiện |
| **Tiên quyết** | Cuối kỳ kế toán |
| **Kích hoạt** | Lập BCTC |

### Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | | Lấy danh mục hàng tồn kho |
| 2 | | Lấy giá thị trường tại ngày lập báo cáo |
| 3 | | So sánh: Giá gốc vs Giá trị thuần (NRV) |
| 4 | | Tính chênh lệch dự phòng |
| 5 | | Lập bút toán dự phòng giảm giá |

### Công thức
- NRV = Giá bán - Chi phí hoàn thiện - Chi phí bán
- Dự phòng = Giá gốc - NRV (nếu NRV < Giá gốc)

### Định khoản
| Trường hợp | Debit | Credit |
|-------------|-------|--------|
| Trích dự phòng | 6324 | 2294 |
| Hoàn dự phòng | 2294 | 6324 |

---

## I06 - Lập Bảng Tổng hợp Nhập Xuất Tồn

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán / `Secondary:` Kế toán trưởng |
| **Mục tiêu** | Tổng hợp số liệu kho theo giá trị |
| **Tiên quyết** | Đã hoàn thành phiếu NX trong kỳ |
| **Kích hoạt** | Cuối tháng |

### Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | | Truy vấn Sổ chi tiết vật liệu/hàng hóa |
| 2 | | Tính tổng cộng cột 1 (Tồn đầu kỳ) |
| 3 | | Tính tổng cộng cột 2 (Nhập trong kỳ) |
| 4 | | Tính tổng cộng cột 3 (Xuất trong kỳ) |
| 5 | | Tính cột 4 (Tồn cuối = 1 + 2 - 3) |
| 6 | | Hiển thị Bảng Tổng hợp theo mẫu S11-DN |

### Cấu trúc Bảng (Mẫu S11-DN)
| Cột | Nội dung |
|-----|----------|
| A | STT, Tên vật liệu/hàng hóa |
| 1 | Giá trị tồn đầu kỳ |
| 2 | Giá trị nhập trong kỳ |
| 3 | Giá trị xuất trong kỳ |
| 4 | Giá trị tồn cuối kỳ |

### Đối chiếu
- Cột 1 ↔ Số dư đầu TK 152/153/155/156
- Cột 2 ↔ Số phát sinh Nợ TK 152/153/155/156
- Cột 3 ↔ Số phát sinh Có TK 152/153/155/156
- Cột 4 ↔ Số dư cuối TK 152/153/155/156

---

## I07 - Kết chuyển Giá vốn hàng bán

| Trư��ng | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán |
| **Mục tiêu** | Kết chuyển giá vốn xuất bán |
| **Tiên quyết** | Đã lập Bảng Tổng hợp NX |
| **Kích hoạt** | Cuối tháng, trước khi kết chuyển G01-G04 |

### Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | | Lấy tổng xuất trong kỳ từ Bảng Tổng hợp |
| 2 | | Chọn phương pháp tính giá (FIFO/BQ/Thực tế đích danh) |
| 3 | | Tính đơn giá xuất kho |
| 4 | | Tính tổng giá vốn = SL xuất × Đơn giá |
| 5 | | Lập bút toán kết chuyển |

### Định khoản
| Nghiệp vụ | Debit | Credit |
|-----------|-------|--------|
| Kết chuyển GV | 632 | 156/155 |
| Kết chuyển GV (nếu có) | 632 | 155 |

### Đối chiếu sau kết chuyển
| Chỉ tiêu | Phải khớp |
|----------|----------|
| Tổng GV | Tổng cột 3 Bảng Tổng hợp |
| Số dư 632 | 0 (sau kết chuyển) |

---

## Reference

| Document | Location |
|----------|----------|
| Mẫu S11-DN | ketoanthienung.net/cach-lap-bang-tong-hop-chi-tiet-vat-lieu-hang-hoa-dung-cu-san-pham.htm |
| Mẫu Bảng NXT | ketoanthienung.net/mau-bang-tong-hop-nhap-xuat-ton-tren-excel.htm |
| Kiểm kê | ketoanthienung.net/mau-bang-ke-hang-ton-kho-cua-ho-kinh-doanh.htm |

---

*Extracted from: ketoanthienung.net*
*Date: 2026-04-16*