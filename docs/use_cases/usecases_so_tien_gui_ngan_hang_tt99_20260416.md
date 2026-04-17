<!-- 
📁 FILE: usecases_so_tien_gui_ngan_hang_tt99_20260416.md
🕐 Ngày trích xuất: 2026-04-16
🔗 URL gốc: https://ketoanthienung.net/mau-so-tien-gui-ngan-hang-khong-ky-han-theo-thong-tu-99.htm
📦 Độ sâu duyệt: 1 cấp (Cha)
-->

# 📋 Use Cases Sổ Tiền Gửi Ngân hàng (TT99/2025)

## 🗂️ Nguồn đã duyệt
| Cấp | URL | Trạng thái | Ghi chú |
|-----|-----|------------|---------|
| 1 | https://ketoanthienung.net/mau-so-tien-gui-ngan-hang-khong-ky-han-theo-thong-tu-99.htm | ✅ | Mẫu S08-DN |

---

## 📦 Nhóm Use Case

### 📌 [UC-TGNH-01] Theo dõi tiền gửi ngân hàng
🔗 Nguồn: [Cấp 1] | URL: (same page)
| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán ngân hàng |
| **Mục tiêu** | Ghi chép chi tiết tiền VN gửi tại Ngân hàng |
| **Tiên quyết** | Có giấy báo Nợ, báo Có từ ngân hàng |
| **Kích hoạt** | Phát sinh nghiệp vụ thu/chi qua ngân hàng |

#### 🔄 Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Kế toán | Ghi ngày, tháng vào cột A |
| 2 | | Ghi số hiệu, ngày tháng chứng từ (giấy báo Nợ, báo Có) vào cột B, C |
| 3 | | Ghi diễn giải vào cột D |
| 4 | | Ghi số hiệu TK đối ứng vào cột E |
| 5 | | Ghi số tiền gửi vào (cột 1) hoặc rút ra (cột 2) |
| 6 | | Tính và ghi số dư còn lại vào cột 3 |

#### ⚠️ Luồng thay thế/Ngoại lệ
| Bước gốc | Điều kiện kích hoạt | Hành động xử lý |
|----------|-------------------|-----------------|
| 6 | Đối chiếu cuối tháng | Đối chiếu số dư với ngân hàng |

✅ **Hậu kiểm:** Sổ tiền gửi ngân hàng được cập nhật, số dư khớp với ngân hàng

---

### 📌 [UC-TGNH-02] Mở sổ tiền gửi ngân hàng
🔗 Nguồn: [Cấp 1] | URL: (same page)
| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán trưởng |
| **Mục tiêu** | Mở sổ theo dõi cho từng tài khoản ngân hàng |
| **Tiên quyết** | Doanh nghiệp có tài khoản ngân hàng |
| **Kích hoạt** | Bắt đầu kỳ kế toán mới |

#### 🔄 Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Kế toán | Xác định các tài khoản ngân hàng của DN |
| 2 | | Mở sổ riêng cho mỗi TK ngân hàng |
| 3 | | Ghi thông tin: nơi mở TK, số hiệu TK |

✅ **Hậu kiểm:** Sổ tiền gửi ngân hàng được mở cho từng TK

---

### 📌 [UC-TGNH-03] Đối chiếu sổ tiền gửi cuối tháng
🔗 Nguồn: [Cấp 1] | URL: (same page)
| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán / `Secondary:` Ngân hàng |
| **Mục tiêu** | Đối chiếu số dư sổ kế toán với số dư ngân hàng |
| **Tiên quyết** | Có sao kê ngân hàng cuối tháng |
| **Kích hoạt** | Cuối tháng |

#### 🔄 Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Kế toán | Lấy số dư cuối tháng từ sổ |
| 2 | | Đối chiếu với số dư trên sao kê ngân hàng |
| 3 | | Xử lý chênh lệch (nếu có) |

✅ **Hậu kiểm:** Số dư được xác nhận khớp

---

## 📋 MẪU SỔ TIỀN GỬI NGÂN HÀNG (S08-DN)

### Cấu trúc cột:
| Cột | Nội dung |
|-----|----------|
| A | Ngày, tháng ghi sổ |
| B | Số hiệu chứng từ |
| C | Ngày, tháng chứng từ |
| D | Diễn giải |
| E | Tài khoản đối ứng |
| 1 | Thu (gửi vào) |
| 2 | Chi (rút ra) |
| 3 | Còn lại |

---

## 📋 CĂN CỨ GHI SỔ
- Giấy báo Nợ của ngân hàng
- Giấy báo Có của ngân hàng
- Sổ phụ ngân hàng

---

## ⚠️ LƯU Ý
- Mỗi ngân hàng có mở tài khoản → Mở riêng một quyển sổ
- Phải ghi rõ nơi mở TK và số hiệu TK giao dịch

---

🛑 QUY TẮC KIỂM TRA TRƯỚC KHI XUẤT:
☑️ Đã duyệt đúng 1 cấp
☑️ Mỗi UC có ID duy nhất và gắn nguồn URL
☑️ Không suy diễn, chỉ trích xuất từ nguồn
☑️ Định dạng Markdown hợp lệ