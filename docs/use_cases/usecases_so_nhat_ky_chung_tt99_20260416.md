<!-- 
📁 FILE: usecases_so_nhat_ky_chung_tt99_20260416.md
🕐 Ngày trích xuất: 2026-04-16
🔗 URL gốc: https://ketoanthienung.net/mau-so-nhat-ky-chung-theo-thong-tu-99-va-cach-lap.htm
📦 Độ sâu duyệt: 1 cấp (Cha)
-->

# 📋 Use Cases Sổ Nhật ký chung (TT99/2025)

## 🗂️ Nguồn đã duyệt
| Cấp | URL | Trạng thái | Ghi chú |
|-----|-----|------------|---------|
| 1 | https://ketoanthienung.net/mau-so-nhat-ky-chung-theo-thong-tu-99-va-cach-lap.htm | ✅ | Mẫu Sổ Nhật ký chung theo TT99 |

---

## 📦 Nhóm Use Case

### 📌 [UC-NKC-01] Ghi sổ Nhật ký chung
🔗 Nguồn: [Cấp 1] | URL: (same page)
| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán viên |
| **Mục tiêu** | Ghi chép các nghiệp vụ kinh tế phát sinh theo thứ tự thời gian |
| **Tiên quyết** | Có chứng từ kế toán làm căn cứ |
| **Kích hoạt** | Nghiệp vụ kinh tế phát sinh |

#### 🔄 Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Kế toán | Ghi ngày, tháng vào cột A |
| 2 | | Ghi số hiệu chứng từ vào cột B |
| 3 | | Ghi ngày, tháng chứng từ vào cột C |
| 4 | | Ghi diễn giải vào cột D |
| 5 | | Đánh dấu đã ghi Sổ Cái vào cột E |
| 6 | | Ghi số thứ tự dòng vào cột G |
| 7 | | Ghi số hiệu Tài khoản đối ứng vào cột H (Nợ trước, Có sau) |
| 8 | | Ghi số tiền Nợ vào cột 1, số tiền Có vào cột 2 |

✅ **Hậu kiểm:** Nghiệp vụ được ghi vào Sổ Nhật ký chung, chuẩn bị cho ghi Sổ Cái

---

### 📌 [UC-NKC-02] Chuyển trang Sổ Nhật ký
🔗 Nguồn: [Cấp 1] | URL: (same page)
| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán viên |
| **Mục tiêu** | Cộng số phát sinh và chuyển sang trang mới |
| **Tiên quyết** | Trang sổ hiện tại đã ghi đầy |
| **Kích hoạt** | Cuối trang sổ |

#### 🔄 Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Kế toán | Cộng số phát sinh lũy kế |
| 2 | | Ghi "Cộng chuyển sang trang sau" |
| 3 | | Đầu trang mới ghi "Số trang trước chuyển sang" |

✅ **Hậu kiểm:** Tiếp tục ghi nghiệp vụ trên trang mới

---

### 📌 [UC-NKC-03] Mở Sổ Nhật ký đặc biệt
🔗 Nguồn: [Cấp 1] | URL: (same page)
| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán trưởng |
| **Mục tiêu** | Mở sổ Nhật ký đặc biệt cho đối tượng có số lượng nghiệp vụ lớn |
| **Tiên quyết** | Đánh giá khối lượng phát sinh |
| **Kích hoạt** | Quyết định mở sổ đặc biệt |

#### 🔄 Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Kế toán trưởng | Đánh giá số lượng phát sinh |
| 2 | | Quyết định mở sổ Nhật ký đặc biệt |
| 3 | | Mở một trong các sổ: Thu tiền, Chi tiền, Mua hàng, Bán hàng |

✅ **Hậu kiểm:** Sổ đặc biệt được mở và sử dụng song song với Sổ Nhật ký chung

---

### 📌 [UC-NKC-04] Định khoản vào Sổ Nhật ký
🔗 Nguồn: [Cấp 1] | URL: (same page)
| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán viên |
| **Mục tiêu** | Phản ánh quan hệ đối ứng tài khoản (định khoản) |
| **Tiên quyết** | Xác định tài khoản Nợ và Có |
| **Kích hoạt** | Nghiệp vụ phát sinh |

#### 🔄 Luồng chính
| Bước | Actor | H��� thống phản hồi |
|------|-------|-------------------|
| 1 | Xác định TK ghi Nợ | |
| 2 | Ghi số TK Nợ vào cột H (dòng đầu) | |
| 3 | Ghi số tiền Nợ vào cột 1 | |
| 4 | Xác định TK ghi Có | |
| 5 | Ghi số TK Có vào cột H (dòng tiếp) | |
| 6 | Ghi số tiền Có vào cột 2 | |

✅ **Hậu kiểm:** Định khoản kế toán được phản ánh đầy đủ

---

## 📋 MẪU SỔ NHẬT KÝ CHUNG (S03a-DN)

### Cấu trúc cột:
| Cột | Nội dung |
|-----|----------|
| A | Ngày, tháng ghi sổ |
| B | Số hiệu chứng từ |
| C | Ngày, tháng chứng từ |
| D | Diễn giải |
| E | Đánh dấu đã ghi Sổ Cái |
| G | Số thứ tự dòng |
| H | Số hiệu TK đối ứng |
| 1 | Số phát sinh Nợ |
| 2 | Số phát sinh Có |

---

## 📋 CÁC SỔ NHẬT KÝ ĐẶC BIỆT

| Mã sổ | Tên sổ | Mục đích |
|-------|--------|----------|
| S03a1-DN | Nhật ký thu tiền | Ghi thu tiền mặt/chuyển khoản |
| S03a2-DN | Nhật ký chi tiền | Ghi chi tiền mặt/chuyển khoản |
| S03a3-DN | Nhật ký mua hàng | Ghi mua hàng/nhập kho |
| S03a4-DN | Nhật ký bán hàng | Ghi bán hàng/xuất kho |

---

## ⚠️ LƯU Ý & MÂU THUẪN
- Doanh nghiệp được phép sửa đổi mẫu sổ so với biểu mẫu TT99, nhưng phải đảm bảo: phản ánh đầy đủ, kịp thời, trung thực, minh bạch, dễ kiểm tra, kiểm soát, đối chiếu được
- Phải ban hành Quy chế hạch toán kế toán khi sửa đổi mẫu sổ

---

🛑 QUY TẮC KIỂM TRA TRƯỚC KHI XUẤT:
☑️ Đã duyệt đúng 1 cấp
☑️ Mỗi UC có ID duy nhất và gắn nguồn URL
☑️ Không suy diễn, chỉ trích xuất từ nguồn
☑️ Định dạng Markdown hợp lệ