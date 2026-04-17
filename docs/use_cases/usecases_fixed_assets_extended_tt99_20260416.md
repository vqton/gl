# Use Cases: Fixed Assets Extended (A04-A06)
*Based on TT99/2025 - Mẫu 02-TSCĐ, 04-TSCĐ*

---

## A04 - Đánh giá lại Tài sản cố định

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán / `Secondary:` Kế toán trưởng |
| **Mục tiêu** | Điều chỉnh giá trị TSCĐ theo quy định |
| **Tiên quyết** | Có quyết định từ cơ quan có thẩm quyền |
| **Kích hoạt** | Thay đổi chính sách, liên doanh, chia tách |

### Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | KT trưởng | Ra quyết định đánh giá lại |
| 2 | Hội đồng | Xác định giá trị thị trường |
| 3 | | Lập Biên bản đánh giá lại (mẫu 04-TSCĐ) |
| 4 | | Tính chênh lệch đánh giá |
| 5 | Kế toán | Lập bút toán điều chỉnh |

### Định khoản
| Trường hợp | Debit | Credit |
|-------------|-------|--------|
| Giá trị tăng | 211/213 | 412 |
| Giá trị giảm | 412 | 211/213 |

### ⚠️ Lưu ý
- Chỉ đánh giá lại khi có quy định từ cơ quan nhà nước
- Không đánh giá lại tự ý trong thông tư 99

---

## A05 - Kiểm kê Tài sản cố định

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Thủ quản / `Secondary:` Kế toán, KT trưởng |
| **Mục tiêu** | Xác định chênh lệch thực tế |
| **Tiên quyết** | Đến kỳ kiểm kê (cuối năm) |
| **Kích hoạt** | Lệnh kiểm kê từ Giám đốc |

### Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Giám đốc | Ra quyết định kiểm kê |
| 2 | Hội đồng | Tiến hành kiểm đếm thực tế |
| 3 | | Đối chiếu sổ sách vs thực tế |
| 4 | | Lập Biên bản kiểm kê |
| 5 | | Xử lý chênh lệch |

### Xử lý chênh lệch
| Trường hợp | Xử lý |
|-------------|-------|
| Thiếu TSCĐ | Ghi giảm, xử lý bồi thường |
| Thừa TSCĐ | Ghi tăng, xác định nguyên giá |
| Hư hỏng | Tính hao mòn, xử lý thanh lý |

---

## A06 - Chuyển nhượng/Thanh lý Tài sản cố định

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán / `Secondary:` KT trưởng, Giám đốc |
| **Mục tiêu** | Thanh lý hoặc nhượng bán TSCĐ |
| **Tiên quyết** | TSCĐ không còn cần dùng hoặc hư hỏng |
| **Kích hoạt** | Quyết định từ Hội đồng quản trị |

### Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Giám đốc | Ra quyết định thanh lý/nhượng bán |
| 2 | Hội đồng | Lập Biên bản thanh lý (mẫu 02-TSCĐ) |
| 3 | | Thực hiện bán/chuyển nhượng |
| 4 | | Thu tiền (hoặc chi phí tháo dỡ) |
| 5 | Kế toán | Ghi nhận thu/chi |
| 6 | | Ghi giảm TSCĐ |

### Định khoản: Nhượng bán TSCĐ
#### Bước 1: Ghi nhận thu
| Debit | Credit | Diễn giải |
|------|--------|-----------|
| 111/112/131 | | Tổng tiền thu |
| | 711 | Thu nhập thanh lý (chưa VAT) |
| | 3331 | Thuế GTGT phải nộp |

#### Bước 2: Ghi giảm TSCĐ
| Debit | Credit | Diễn giải |
|------|--------|-----------|
| 214 | | Hao mòn lũy kế |
| 811 | | Giá trị còn lại |
| | 211 | Nguyên giá |

#### Bước 3: Chi phí thanh lý (nếu có)
| Debit | Credit | Diễn giải |
|------|--------|-----------|
| 811 | | Chi phí tháo dổ |
| | 111/112/331 | Tiền chi |

### Hồ sơ thanh lý/nhượng bán
- Quyết định thanh lý TSCĐ
- Biên bản họp Hội đồng quản trị
- Biên bản thanh lý (mẫu 02-TSCĐ)
- Hợp đồng bán
- Hóa đơn bán TSCĐ
- Biên bản giao nhận

---

## Reference

| Document | Location |
|----------|----------|
| Mẫu 02-TSCĐ | ketoanthienung.net/mau-bien-ban-thanh-ly-tscd-mau-so-02-tscd.htm |
| Mẫu 04-TSCĐ | ketoanthienung.net/bien-ban-danh-gia-lai-tai-san-co-dinh-mau-so-04-tscd.htm |
| Cách hạch toán | ketoanthienung.net/thu-tuc-thanh-ly-tai-san-co-dinh-da-va-chua-het-khau-hao.htm |

---

*Extracted from: ketoanthienung.net*
*Date: 2026-04-16*