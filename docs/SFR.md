Chào bạn, với vai trò **Lead BA**, tôi sẽ chuyển đổi bản BRD V3.0 (Final) thành tài liệu **Đặc tả yêu cầu chức năng (SFR - Software Functional Requirements)**. 

Tài liệu này không chỉ nêu "cần làm gì" mà đi sâu vào "hệ thống sẽ xử lý như thế nào" (Logic nghiệp vụ, Input/Output, Quy tắc dữ liệu) để đội ngũ Lập trình (Dev) và Kiểm thử (QC) có thể thực hiện ngay.

---

# ĐẶC TẢ YÊU CẦU CHỨC NĂNG (SFR)
**Dự án:** Hệ thống Kế toán SME Thế hệ mới (Tuân thủ TT 99/2025/TT-BTC)  
**Mã tài liệu:** SFR-ACC-2026-V1.0  
**Ngày soạn:** 31/03/2026

---

## 1. NHÓM CHỨC NĂNG HỆ THỐNG & KẾ TOÁN TỔNG HỢP (CORE)

### SFR-01: Khởi tạo Danh mục Tài khoản (COA) theo TT 99
* **Mô tả:** Hệ thống tự động tạo bộ khung tài khoản kế toán ngay khi kích hoạt dữ liệu năm 2026.
* **Logic xử lý:**
    * Tự động Seed Data 71 tài khoản cấp 1 (ví dụ: 111, 112, 121, 211, 215...) và 101 tài khoản cấp 2 theo Phụ lục II TT 99/2025.
    * **Quy tắc:** Tài khoản con phải kế thừa tính chất (Dư Nợ/Dư Có) từ tài khoản mẹ.
    * Hệ thống cho phép tạo TK cấp 3, 4 (độ dài tối đa 10 ký tự).
* **Input:** Lệnh kích hoạt hệ thống từ Admin.
* **Output:** Danh mục tài khoản (Chart of Accounts) hoàn chỉnh.

### SFR-02: Cơ chế hạch toán dựa trên sự kiện (Event-driven Accounting)
* **Mô tả:** Chuyển đổi các giao dịch kinh tế thành bút toán kế toán tự động.
* **Logic xử lý:**
    * Khi người dùng thực hiện một nghiệp vụ (ví dụ: Xuất hóa đơn bán hàng), hệ thống gọi **Entry Rules Engine**.
    * **Rule mẫu:** Nếu Loại giao dịch = "Bán hàng dịch vụ" -> Tự động sinh bút toán:
        * Nợ TK 131 (Phải thu khách hàng)
        * Có TK 511 (Doanh thu)
        * Có TK 3331 (Thuế GTGT)
* **Yêu cầu:** Cho phép Kế toán trưởng sửa đổi Rule (TK Nợ/Có) mà không cần can thiệp Code.

---

## 2. NHÓM CHỨC NĂNG BÁN HÀNG & THUẾ (SALES & TAX)

### SFR-03: Phát hành Hóa đơn điện tử (HĐĐT) chuẩn 2026
* **Mô tả:** Kết nối trực tiếp với nhà cung cấp (Cổng eTax/HĐĐT) để cấp mã và ký số.
* **Logic xử lý:**
    * Hệ thống kiểm tra thông tin bắt buộc: MST, Tên đơn vị, Thuế suất (theo Luật 149/2025).
    * Gọi API ký số HSM để ký số tập trung.
    * **Trạng thái:** Chờ ký -> Đã ký -> Đã cấp mã CQT -> Gửi khách hàng.
* **Validation:** Không cho phép phát hành hóa đơn nếu số lượng tồn kho âm (trừ trường hợp cấu hình đặc thù).

### SFR-04: Đối soát tự động hóa đơn đầu vào (Auto-Reconcile)
* **Mô tả:** Tự động lấy dữ liệu từ Cơ quan Thuế để kiểm tra tính hợp lệ.
* **Logic xử lý:**
    * Hằng ngày, hệ thống quét cổng eTax bằng MST doanh nghiệp.
    * Tải file XML hóa đơn đầu vào -> Tự động tạo "Phiếu mua hàng nháp".
    * Đối chiếu MST người bán với danh sách "Doanh nghiệp rủi ro về thuế" (Cập nhật từ Blacklist của CQT).
    * Cảnh báo nếu đơn giá/số lượng trên hóa đơn lệch so với Đơn đặt hàng (PO).

---

## 3. NHÓM CHỨC NĂNG LƯƠNG & BẢO HIỂM (PAYROLL & COMPLIANCE)

### SFR-05: Tính lương & Trích nộp BHXH theo Luật 2024
* **Mô tả:** Tính toán lương net và các khoản trích theo lương của năm 2026.
* **Logic xử lý:**
    * Lấy mức lương tham chiếu (thay cho lương cơ sở) theo quy định mới nhất.
    * Áp dụng tỷ lệ đóng BHXH/BHYT/BHTN theo Luật BHXH 2024.
    * **Thuế TNCN:** Tính theo phương pháp lũy tiến từng phần, tự động cập nhật mức giảm trừ gia cảnh (nếu có thay đổi tại 2026).
* **Bảo mật:** Toàn bộ bảng lương trong Database phải được mã hóa theo chuẩn **AES-256**. Chỉ người có Role "Kế toán lương" hoặc "Giám đốc" mới thấy số liệu giải mã.

---

## 4. NHÓM CHỨC NĂNG BÁO CÁO (REPORTING)

### SFR-06: Lập Báo cáo tài chính tự động (TT 99)
* **Mô tả:** Tổng hợp dữ liệu từ Sổ cái để lên 4 báo cáo chính.
* **Logic xử lý:**
    * **Bảng Cân đối kế toán:** Phân loại ngắn hạn/dài hạn dựa trên trường dữ liệu "Ngày đáo hạn" của chứng từ.
    * **BC Kết quả kinh doanh:** Tự động kết chuyển doanh thu, chi phí sang TK 911 để xác định lãi lỗ.
    * **Thuyết minh BCTC:** Tự động trích xuất các bảng chi tiết về TSCĐ, Nợ phải thu quá hạn, Dự phòng giảm giá.
* **Output:** File .xml đúng cấu trúc của ứng dụng HTKK (Tổng cục Thuế).

---

## 5. YÊU CẦU KỸ THUẬT PHI CHỨC NĂNG (NON-FUNCTIONAL SFR)

* **SFR-SEC-01 (Audit Trail):** Mọi bản ghi dữ liệu (Record) phải có 4 trường ẩn: `Created_By`, `Created_At`, `Updated_By`, `Updated_At`.
* **SFR-LOG-01:** Hệ thống lưu trữ lịch sử thay đổi (Data Versioning) cho tất cả chứng từ đã ghi sổ (Post). Nếu sửa chứng từ, hệ thống tạo version mới và giữ lại version cũ để đối soát.
* **SFR-INT-01:** API Ngân hàng lấy sao kê tự động vào 06:00 AM hằng ngày để thực hiện đối soát (Bank Reconciliation).

---

### PHÊ DUYỆT TÀI LIỆU
* **Đại diện Phát triển (CTO/Tech Lead):** Xác nhận tính khả thi về công nghệ.
* **Đại diện Nghiệp vụ (Kế toán trưởng):** Xác nhận tính đúng đắn của logic thuế/kế toán.
* **Lead BA:** Xác nhận độ phủ so với BRD.

**Ghi chú:** Đây là khung SFR chi tiết nhất. Bạn có muốn tôi viết sâu hơn vào **Database Schema (Lược đồ cơ sở dữ liệu)** cho phần Kế toán Tổng hợp không?
