# FRONTEND SPECIFICATIONS & UI/UX GUIDELINE V1.0
**Dự án:** Hệ thống Kế toán SME SME Greenfield (TT 99/2025/TT-BTC)  
**Phong cách:** High-Density / Keyboard-First / Data-Driven  
**Công nghệ:** Django Templates + Tailwind CSS + HTMX (cho các tương tác Real-time nhẹ).

---

## 1. HỆ THỐNG LƯỚI & BỐ CỤC (LAYOUT SYSTEM)

### 1.1 Mật độ hiển thị (Information Density)
* **Compact Mode:** Khoảng cách giữa các dòng (row height) trong bảng chỉ từ **32px - 36px**. 
* **Maximized Workspace:** Sidebar có thể thu nhỏ (collapse) để dành 95% diện tích màn hình cho các bảng tính lớn (Bảng cân đối kế toán).
* **Internal Tabs:** Cho phép mở nhiều chứng từ dưới dạng tab bên trong ứng dụng (giống trình duyệt nhưng quản lý ngay trong Web App) để đối soát song song.

### 1.2 Cấu trúc Trang chứng từ (Voucher Layout)
Mô phỏng 1:1 theo Phụ lục I - TT 99:
* **Top Bar:** Các nút chức năng (F2: Thêm, F3: Lưu, F4: In, F10: Ghi sổ).
* **Header Area:** Thông tin chung (Đối tượng, Ngày, Lý do). Tối đa 2 cột để tránh mỏi mắt.
* **Detail Grid:** Lưới nhập liệu Nợ/Có. Phải chiếm ít nhất 60% chiều cao màn hình.

---

## 2. KEYBOARD-FIRST NAVIGATION (XƯƠNG SỐNG CỦA UX)

### 2.1 Tab & Enter Sequence
* Thứ tự Tab: `Ngày CT` -> `Số CT` -> `Mã đối tượng` -> `Lưới định khoản`.
* Tại lưới định khoản: `Enter` tại cột cuối cùng của dòng 1 sẽ tự động nhảy xuống cột đầu tiên của dòng 2 và tạo dòng mới.

### 2.2 Global Hotkeys (Phím tắt hệ thống)
Sử dụng thư viện `Mousetrap.js` hoặc `Hotkeys.js`:
* `Alt + N`: Thêm mới chứng từ.
* `Alt + S`: Lưu (Save).
* `Alt + P`: In (Print).
* `F4`: Mở nhanh danh mục (Tài khoản/Khách hàng) tại trường đang focus.

---

## 3. UI COMPONENTS SPECIFICATION

### 3.1 Data Grid (Smart Table)
* **Sticky Header & First Column:** Cố định tiêu đề và cột "Số chứng từ" khi cuộn ngang/dọc.
* **Cell Focus State:** Ô đang nhập liệu phải có viền (border) màu xanh đậm (Primary Blue #1E40AF) và nền vàng nhạt để phân biệt rõ vị trí con trỏ.
* **Auto-suggestion (Combobox):** Khi gõ mã tài khoản (ví dụ "111"), danh sách gợi ý phải xuất hiện ngay lập tức (Latency < 100ms).

### 3.2 Nhập liệu số (Numeric Input)
* **Tự động phân cách:** Người dùng gõ `1000000`, hệ thống tự hiển thị `1.000.000` ngay khi đang gõ.
* **Xử lý số âm:** Hiển thị màu đỏ và trong ngoặc đơn. Ví dụ: `(500.000)`.
* **Căn lề:** Luôn căn phải (Right-align) đối với các cột số tiền để dễ so sánh hàng đơn vị, hàng chục.

---

## 4. QUY TẮC MÀU SẮC & TRẠNG THÁI (VISUAL HIERARCHY)

| Trạng thái | Mã màu (Hex) | Ý nghĩa |
| :--- | :--- | :--- |
| **Primary** | `#1E40AF` (Deep Blue) | Sự tin cậy, chuyên nghiệp. |
| **Success** | `#15803D` (Green) | Chứng từ đã ghi sổ (Posted). |
| **Draft** | `#6B7280` (Gray) | Chứng từ tạm/nháp. |
| **Danger** | `#B91C1C` (Red) | Chứng từ hủy, lỗi hạch toán, số âm. |
| **Warning** | `#D97706` (Amber) | Cảnh báo rủi ro thuế, nợ quá hạn. |

---

## 5. DESIGN SYSTEM GUIDELINE (CHO DEV)

* **Font-family:** `Inter, system-ui, -apple-system, sans-serif`. Ưu tiên font hệ thống để tốc độ render nhanh nhất.
* **Iconography:** Sử dụng bộ icon đường nét mảnh (Lucide Icons), không dùng màu mè để tránh gây nhiễu thị giác.
* **Loading State:** Sử dụng thanh tiến trình (Progress bar) ở đầu trang thay vì Spinner che giữa màn hình, giúp kế toán vẫn có thể quan sát số liệu trong lúc đợi.

---

## 6. ĐẶC TẢ DRILL-DOWN (UX TRUY XUẤT)
Mọi con số trên Báo cáo tài chính (BCTC) phải có thuộc tính `hover:underline` và `cursor:pointer`.
* **Action:** Click vào số dư Nợ TK 111 trên Bảng CĐPS -> Mở Tab "Sổ chi tiết TK 111" -> Click vào một dòng nghiệp vụ -> Mở Tab "Phiếu Thu/Chi" gốc.

**Lời kết từ Designer:** Bản Spec này biến Web App thành một "cỗ máy nhập liệu" thực thụ. Chúng ta không bán cái đẹp, chúng ta bán **sự chính xác và tốc độ**.

**Bước tiếp theo:** Bạn có muốn tôi thiết kế mẫu **Wireframe (Bản vẽ khung xương)** cho màn hình "Bảng cân đối kế toán" với đầy đủ tính năng Filter và Drill-down không?