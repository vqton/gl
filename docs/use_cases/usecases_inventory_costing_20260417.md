<!-- 
📁 FILE NAME: usecases_inventory_costing_20260417.md
🕐 Ngày trích xuất: 2026-04-17
🔗 URL gốc: https://ketoanthienung.net/phuong-phap-tinh-gia-xuat-kho-theo-thong-tu-99.htm
📦 Độ sâu duyệt: 1 cấp (Trang chính)
-->

# 📋 Use Cases Tổng hợp (Độ sâu: 1 cấp)

## 🗂️ Mục lục nguồn đã duyệt
| Cấp | URL | Trạng thái | Ghi chú |
|-----|-----|------------|---------|
| 1 | https://ketoanthienung.net/phuong-phap-tinh-gia-xuat-kho-theo-thong-tu-99.htm | ✅ | TT99 inventory costing methods |

---

## 📦 Nhóm Use Case

### 📌 [I-05a] Tính Giá Xuất Kho theo PP Bình Quân Gia Quyền
🔗 Nguồn: [Cấp 1] | URL: https://ketoanthienung.net/phuong-phap-tinh-gia-xuat-kho-theo-thong-tu-99.htm

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán kho / `Secondary:` Thủ kho |
| **Mục tiêu** | Xác định đơn giá xuất kho bình quân cho hàng hóa tồn kho |
| **Tiên quyết** | Có phiếu nhập kho với đơn giá, chưa tính giá xuất kỳ hiện tại |
| **Kích hoạt** | Phát sinh xuất kho hàng hóa |

#### 🔄 Luồng chính (Main Success Scenario)
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | KT kho | Nhập số liệu tồn đầu kỳ + nhập trong kỳ |
| 2 | Hệ thống | Tính tổng giá trị nhập = sum(đơn giá × số lượng) |
| 3 | Hệ thống | Tính tổng số lượng nhập |
| 4 | Hệ thống | Tính đơn giá BQ = Tổng giá trị / Tổng số lượng |
| 5 | Hệ thống | Gán đơn giá BQ cho lần xuất |

✅ **Hậu kiểm:** Đơn giá xuất kho = (Giá tồn đầu + Giá nhập) / (SL tồn + SL nhập)

#### 🔀 Ghi chú:
- Công thức: Đơn giá BQ = (Giá trị tồn đầu kỳ + Tổng giá trị nhập trong kỳ) / (Số lượng tồn đầu + Số lượng nhập trong kỳ)
- Áp dụng: Mọi doanh nghiệp thương mại

---

### 📌 [I-05b] Tính Giá Xuất Kho theo PP FIFO (Nhập Trước Xuất Trước)
🔗 Nguồn: [Cấp 1] | URL: https://ketoanthienung.net/phuong-phap-tinh-gia-xuat-kho-theo-thong-tu-99.htm

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán kho / `Secondary:` Thủ kho |
| **Mục tiêu** | Xác định giá xuất kho theo lô nhập đầu tiên |
| **Tiên quyết** | Có nhiều lô nhập kho với đơn giá khác nhau |
| **Kích hoạt** | Phát sinh xuất kho hàng hóa |

#### 🔄 Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | KT kho | Lấy danh sách lô nhập (排序 theo ngày) |
| 2 | Hệ thống | Lấy lô nhập đầu tiên |
| 3 | Hệ thống | Trừ số lượng xuất khỏi lô cũ nhất |
| 4 | Hệ thống | Nếu lô cũ hết → sang lô tiếp theo |

#### ⚠️ Luồng thay thế/Ngoại lệ
| Bước gốc | Điều kiện kích hoạt | Hành động xử lý |
|----------|-------------------|-----------------|
| [3] | Lô đầu không đủ số lượng | Lấy tiếp lô thứ 2, thứ 3... |
| [3] | Hàng đặc biệt (theo lô) | Đánh dấu từng serialnumber |

✅ **Hậu kiểm:** Giá xuất = Giá của lô nhập cũ nhất còn hàng

---

### 📌 [I-05c] Tính Giá Xuất Kho theo PP Đích Danh (Specific)
🔗 Nguồn: [Cấp 1] | URL: https://ketoanthienung.net/phuong-phap-tinh-gia-xuat-kho-theo-thong-tu-99.htm

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán kho |
| **Mục tiêu** | Xác định giá trị thực tế của từng mặt hàng cụ thể |
| **Tiên quyết** | ít mặt hàng, hàng ổn định, nhận diện được |
| **Kích hoạt** | Xuất kho từng lô cụ thể |

#### 🔄 Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | KT kho | Xác định lô hàng cụ thể (serial) |
| 2 | Hệ thống | Lấy đơn giá của lô đó |
| 3 | Hệ thống | Tính giá xuất = đơn giá × số lượng |

✅ **Hậu kiểm:** Giá xuất = Giá thực tế của lô hàng cụ thể

🔀 *Ghi chú:* Chỉ áp dụng cho doanh nghiệp ít chủng loại hoặc hàng giá trị lớn

---

### 📌 [I-05d] Tính Giá Xuất Kho theo PP Giá Bán Lẻ
🔗 Nguồn: [Cấp 1] | URL: https://ketoanthienung.net/phuong-phap-tinh-gia-xuat-kho-theo-thong-tu-99.htm

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán bán lẻ |
| **Mục tiêu** | Tính giá xuất từ giá bán trừ lợi nhuận biên |
| **Tiên quyết** | DN bán lẻ (siêu thị), nhiều mặt hàng thay đổi nhanh |
| **Kích hoạt** | Bán hàng tại quầy |

#### 🔄 Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Hệ thống | Lấy giá bán của hàng tồn kho |
| 2 | KT | Xác định tỷ lệ % lợi nhuận biên |
| 3 | Hệ thống | Tính giá xuất = Giá bán × (1 - Tỷ lệ %) |

✅ **Hậu kiểm:** Giá xuất = Giá bán - Lợi nhuận biên

---

### 📌 [I-05e] Đối chiếu kho khi kết thúc kỳ (Method A - Continuous)
🔗 Nguồn: [Cấp 1] | URL: https://ketoanthienung.net/phuong-phap-tinh-gia-xuat-kho-theo-thong-tu-99.htm

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` KT kho / `Secondary:` Kiểm kê |
| **Mục tiêu** | Đối chiếu sổ kế toán vs kiểm kê thực tế |
| **Tiên quyết** | Theo dõi nhập-xuất-tồn thường xuyên |
| **Kích hoạt** | Cuối kỳ kế toán |

#### 🔄 Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | KT kho | Lấy số dư tồn kho trên sổ |
| 2 | Kiểm kê | Đếm hàng thực tế trong kho |
| 3 | Hệ thống | So sánh chênh lệch (nếu có) |
| 4 | KT | Điều chỉnh hoặc báo cáo nguyên nhân |

✅ **Hậu kiểm:** Số lượng tồn thực tế = Số lượng trên sổ kế toán

---

### 📌 [I-05f] Tính giá xuất từ tồn cuối kỳ (Method B - Periodic)
🔗 Nguồn: [Cấp 1] | URL: https://ketoanthienung.net/phuong-phap-tinh-gia-xuat-kho-theo-thong-tu-99.htm

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán kho |
| **Mục tiêu** | Tính giá trị hàng xuất từ công thức ngược |
| **Tiên quyết** | DN theo dõi tồn cuối kỳ |
| **Kích hoạt** | Kết thúc kỳ kế toán |

#### 🔄 Luồng chính
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Kiểm kê | Đếm hàng tồn cuối kỳ |
| 2 | Hệ thống | Tính SL xuất = Tồn đầu + Nhập - Tồn cuối |
| 3 | Hệ thống | Tính Giá trị xuất = Giá trị tồn đầu + Nhập - Tồn cuối |

✅ **Hậu kiểm:** Giá trị xuất = Tồn đầu + Nhập - Tồn cuối

🔀 *Ghi chú:* Áp dụng cho cửa hàng bán lẻ nhiều chủng loại, giá trị thấp

---

## ⚠️ LƯU Ý & MÂU THUẪN (Nếu có)
- Phương pháp phải áp dụng nhất quán giữa các kỳ kế toán
- Thay đổi phương pháp = coi như thay đổi chính sách kế toán, phải công bố
- TT99 yêu cầu ghi rõ phương pháp trong thuyết minh BCTC

🛑 QUY TẮC KIỂM TRA TRƯỚC KHI XUẤT:
☒️ Đã duyệt đúng tối đa 2 cấp (Cha → Con)?
☒️ Mỗi UC đều có ID duy nhất và gắn nguồn URL rõ ràng?
☒️ Đã loại bỏ trùng lặp, ưu tiên chi tiết từ Cấp 2?
☒️ Không có nội dung bịa đặt/hallucination?
☒️ Định dạng Markdown chuẩn, sẵn sàng lưu file?

---

*Nguồn: ketoanthienung.net - Theo Thông tư 99/2025/TT-BTC*