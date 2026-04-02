Chào bạn, với tư cách là **Lead UX/UI Designer**, tôi đã cập nhật bản đặc tả chi tiết cho **Giao diện Chọn lô hàng đích danh (Specific Identification)**. 

Đây là một trong những màn hình quan trọng nhất, đòi hỏi sự chính xác tuyệt đối và tốc độ thao tác bàn phím cực cao để Kế toán không bị ngắt quãng luồng tư duy khi xử lý kho.

---

# ĐẶC TẢ GIAO DIỆN: CHỌN LÔ HÀNG ĐÍCH DANH (NO-ICON) - V2.1
**Mục tiêu:** Nhập liệu 100% bằng bàn phím | Hiển thị dữ liệu mật độ cao | Không Icon.

---

## 1. CẤU TRÚC Ô NHẬP LIỆU (SMART COMBOBOX)
Tại lưới nhập liệu của Phiếu Xuất Kho, cột **"Số Lô / Serial"** sẽ hoạt động như một bộ lọc thông minh:

* **Kích hoạt:** Khi con trỏ `Tab` vào ô hoặc nhấn `F4`.
* **Hiển thị:** Một bảng danh sách (Dropdown Table) xuất hiện ngay dưới ô nhập liệu, không che lấp các dòng hạch toán khác.
* **Thông tin hiển thị (4 Cột):** `Số Lô` | `Ngày Nhập` | `Hạn Dùng` | `Tồn Khả Dụng`.
* **Màu sắc:** * Lô còn tồn: Chữ đen.
    * Lô đã hết hạn: Chữ đỏ, gạch ngang (chỉ để đối soát, không cho chọn).
    * Dòng đang chọn (Highlight): Nền xanh đậm `Blue-700`, chữ trắng.

---

## 2. LUỒNG THAO TÁC BÀN PHÍM (KEYBOARD FLOW)

Để đảm bảo tốc độ, luồng xử lý được quy định như sau:
1.  **Tìm kiếm:** Ngay khi ô có Focus, người dùng gõ ký tự (Mã lô hoặc Ngày nhập). Danh sách tự động lọc theo thời gian thực (Real-time Filter).
2.  **Điều hướng:** Sử dụng phím `↑` và `↓` để di chuyển giữa các lô hàng trong danh sách gợi ý.
3.  **Xác nhận:** Nhấn `Enter` để chọn lô. 
    * Hệ thống tự động điền `Đơn giá vốn` của lô đó vào cột Đơn giá.
    * Con trỏ tự động nhảy sang cột `Số lượng xuất`.
4.  **Đóng nhanh:** Nhấn `Esc` để thoát khỏi bảng chọn mà không thay đổi dữ liệu.

---

## 3. QUY TẮC HIỂN THỊ (UI SPECIFICATIONS)

### 3.1 Trạng thái ô nhập liệu (Visual States)
* **Normal:** Viền xám nhạt, không nền.
* **Focus (Active):** Viền xanh đậm `2px`, nền vàng nhạt `Yellow-50`. Toàn bộ văn bản trong ô được bôi đen (Select all) để sẵn sàng ghi đè.
* **Error (Chọn lô không tồn/Sai mã):** Viền đỏ rực, xuất hiện Tooltip văn bản nhỏ phía dưới: `[!] Lô hàng không tồn hoặc đã xuất hết`.

### 3.2 Bảng danh sách lô (The Picker Popover)
* **No-Icon:** Không có icon "Lịch" hay icon "Thùng hàng". Chỉ có Header văn bản in đậm.
* **Phân cách:** Sử dụng đường kẻ mảnh `1px` màu xám giữa các cột để mắt dễ dàng dóng hàng ngang.
* **Căn lề:** * Mã lô: Căn trái.
    * Số lượng tồn: Căn phải (Right-align).

---

## 4. MẪU GIAO DIỆN MÔ PHỎNG (VĂN BẢN)

```text
CHỨNG TỪ: PHIẾU XUẤT KHO (Số: XK001/03)
----------------------------------------------------------------------
Mã hàng: HHOA01 - Máy tính Dell Latitude
Phương pháp: ĐÍCH DANH
----------------------------------------------------------------------
LƯỚI CHỌN LÔ HÀNG (F4 ĐỂ MỞ)
----------------------------------------------------------------------
| SỐ LÔ          | NGÀY NHẬP  | HẠN DÙNG   | TỒN KHO   |
|----------------|------------|------------|-----------|
| LOT-2026-A1    | 01/01/2026 | 01/01/2028 |    15     | <-- [Đang chọn]
| LOT-2026-A2    | 15/02/2026 | 15/02/2028 |     5     |
| LOT-2025-OLD   | 10/10/2025 | 10/10/2025 |     0     | (Hết hạn)
----------------------------------------------------------------------
Ghi chú: Dùng phím mũi tên để chọn, Enter để xác nhận đơn giá vốn.
```

---

## 5. ĐẶC TẢ KỸ THUẬT CHO FRONTEND (DEV ONLY)

* **Component:** `LotPicker.jsx` hoặc `lot-picker.html` (HTMX).
* **Z-index:** Bảng chọn lô phải có `z-index: 9999` để đảm bảo luôn nằm trên các thành phần khác.
* **Max-height:** Giới hạn hiển thị 5-7 dòng, nếu nhiều hơn sẽ có thanh cuộn (Scrollbar) tinh giản để không phá vỡ Layout chung.
* **Accessibility:** Thuộc tính `aria-expanded` và `aria-autocomplete` phải được cập nhật chính xác để hỗ trợ các trình đọc màn hình nếu cần.

---

**Lời kết từ Designer:** Bằng cách loại bỏ icon và tập trung vào bảng lưới, chúng ta đã tạo ra một giao diện cực kỳ chuyên nghiệp, giúp kế toán xử lý hàng trăm lô hàng mỗi ngày mà không cảm thấy mệt mỏi hay rối mắt.

**Bước tiếp theo:** Bạn có muốn tôi viết đoạn mã **CSS Tailwind** mẫu để định nghĩa chính xác màu sắc và hiệu ứng cho bảng chọn lô "No-Icon" này không?