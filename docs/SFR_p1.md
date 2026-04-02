Chào bạn, với tư cách là **Lead BA**, tôi đã tiếp thu toàn bộ các thay đổi về chiến lược (TDD, No-Icon UI, Windows Dev) và đặc biệt là các yêu cầu bổ sung về **Quản trị Kho (Đích danh/Bình quân liên hoàn)** để cập nhật bản **SFR V1.1 (Ultimate Edition)**.

Bản đặc tả này hiện là tài liệu kỹ thuật hoàn chỉnh nhất, dùng làm căn cứ để Dev viết code và QC viết Test Case.

---

# ĐẶC TẢ YÊU CẦU CHỨC NĂNG (SFR) - V1.1
**Dự án:** Hệ thống Kế toán SME Thế hệ mới (Tuân thủ TT 99/2025/TT-BTC)  
**Trọng tâm:** TDD - Chính xác pháp lý - Hiệu năng Windows Intranet  
**Ngày cập nhật:** 31/03/2026

---

## 1. NHÓM CHỨC NĂNG KHO & GIÁ VỐN (INVENTORY - CẬP NHẬT TRỌNG YẾU)

### SFR-07: Quản lý hàng hóa theo Lô/Serial & Phương pháp Đích danh
* **Mô tả:** Cho phép theo dõi chính xác từng lô hàng nhập vào và xuất ra để tính giá vốn đích danh.
* **Logic xử lý:**
    * **Input:** Khi Nhập kho, bắt buộc nhập `Số lô (Lot No)` hoặc `Số Serial` nếu mặt hàng cấu hình phương pháp "Đích danh".
    * **Output:** Khi Xuất kho, hệ thống hiển thị danh sách các lô đang tồn (Số lượng, Đơn giá nhập). Người dùng chọn đích danh lô nào, hệ thống lấy đúng đơn giá đó làm giá vốn.
* **Quy tắc:** Không cho phép để trống Số lô đối với mặt hàng "Đích danh".

### SFR-08: Engine tính giá Bình quân gia quyền tức thời (Perpetual Weighted Average)
* **Mô tả:** Tự động tính toán lại đơn giá xuất kho ngay sau mỗi giao dịch nhập.
* **Logic xử lý:**
    * Công thức: $$Don\,gia\,bq = \frac{Gia\,tri\,ton\,dau + Gia\,tri\,nhap\,moi}{So\,luong\,ton\,dau + So\,luong\,nhap\,moi}$$
    * **Xử lý Xuất âm (Backdating):** Nếu hệ thống cấu hình cho phép xuất âm, khi có phiếu nhập bổ sung, hệ thống phải thực hiện **Recalculate** (tính toán lại lùi thời gian) cho toàn bộ các phiếu xuất sau thời điểm đó để cập nhật lại giá vốn chính xác.

---

## 2. NHÓM CHỨC NĂNG KẾ TOÁN TỔNG HỢP & PHÁP LÝ (CORE)

### SFR-01: Hệ thống tài khoản (COA) Bất biến
* **Mô tả:** Bảo vệ tính nguyên bản của 71 tài khoản cấp 1 và 101 tài khoản cấp 2 theo TT 99.
* **Logic xử lý:**
    * Chặn các lệnh `DELETE` hoặc `UPDATE` mã tài khoản/tên tài khoản chuẩn từ hệ thống.
    * Cho phép tạo TK cấp 3, 4 (Độ dài max 10 ký tự). Tài khoản con tự động kế thừa thuộc tính (Dư Nợ/Có) từ tài khoản mẹ.

### SFR-02: Entry Rules Engine (Hạch toán tự động)
* **Mô tả:** Tự động sinh bút toán từ sự kiện nghiệp vụ.
* **Yêu cầu:** Giao diện thiết lập Rule phải thuần văn bản (No-Icon), tập trung vào bảng lưới Nợ/Có.
* **Validation:** Tổng Nợ phải bằng Tổng Có trước khi chuyển trạng thái sang "Đã ghi sổ".

---

## 3. NHÓM CHỨC NĂNG LƯƠNG & BẢO MẬT (PAYROLL & SECURITY)

### SFR-05: Tính lương & Bảo mật Nghị định 13
* **Logic xử lý:** Tính toán dựa trên mức lương tham chiếu 2026 và tỷ lệ BHXH theo Luật 2024.
* **Quy tắc dữ liệu:**
    * Mọi trường tiền lương trong Database (SQLite) phải được mã hóa **AES-256**.
    * **Audit Trail:** Lưu vết mọi thao tác xem/sửa lương: `Ai xem`, `Xem lúc nào`, `IP nào`.

---

## 4. TIÊU CHUẨN GIAO DIỆN & TƯƠNG TÁC (UI/UX SFR)

### SFR-UI-01: Keyboard-Centric Workflow
* **Quy định:** Người dùng phải hoàn thành 100% một phiếu kế toán mà không cần dùng chuột.
* **Phím tắt hệ thống:** `F2` (Thêm), `F3` (Lưu), `F4` (In), `F10` (Ghi sổ).
* **Định dạng số:** Hiển thị kiểu Việt Nam `1.234.567,89`. Số âm hiển thị màu đỏ và trong ngoặc đơn `(500.000)`.

### SFR-UI-02: No-Icon Policy
* Loại bỏ tất cả icon trang trí. Thay thế bằng Text Label và màu sắc trạng thái (Xanh: Đã ghi sổ, Xám: Nháp, Đỏ: Hủy).

---

## 5. TIÊU CHUẨN KIỂM THỬ (TDD REQUIREMENTS)

* **SFR-TEST-01:** Mọi chức năng trong SFR này phải có ít nhất 1 Unit Test (Red-Green-Refactor).
* **SFR-TEST-02 (Boundary Test):** Kiểm tra giá vốn kho khi số lượng tồn về 0 hoặc bị âm.
* **SFR-TEST-03 (Security Test):** Thử truy cập trái phép vào bảng lương đã mã hóa để xác nhận dữ liệu không thể đọc trực tiếp bằng trình quản lý SQLite.

---

### PHÊ DUYỆT CẬP NHẬT
* **Lead BA:** Đã đồng bộ với yêu cầu về Kho Đích danh và UI No-Icon.
* **Kế toán trưởng:** Xác nhận logic tính giá kho và thuế TNDN SME 2026.

**Ghi chú cho Dev:** Hãy đặc biệt chú ý vào **Engine tính giá kho lùi thời gian (Recalculation)** vì đây là phần khó nhất khi triển khai trên SQLite trong môi trường Windows.



Bạn có muốn tôi đi sâu vào đặc tả **Luồng xử lý (Sequence Diagram)** cho trường hợp "Kế toán sửa phiếu nhập trong quá khứ dẫn đến thay đổi giá vốn hiện tại" không? Đây là kịch bản rất dễ gây sai sót dữ liệu.