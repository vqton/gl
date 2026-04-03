Chào bạn, với tư cách là **Lead BA**, tôi đã tổng hợp và khôi phục toàn bộ nội dung từ các phiên bản thảo luận trước đó, kết hợp với các yêu cầu kỹ thuật đặc thù (Django, SQLite, Intranet, Greenfield) để tạo ra bản **BRD V5.0 (Final Recovery)**.

Tài liệu này được thiết kế để làm "Kim chỉ nam" cho đội ngũ phát triển, đảm bảo tính **Nguyên bản - Bất biến** đối với các danh mục pháp luật.

---

# TÀI LIỆU YÊU CẦU KINH DOANH (BRD) - PHIÊN BẢN 5.0
**Dự án:** Hệ thống Kế toán SME Thế hệ mới (Tuân thủ TT 99/2025/TT-BTC)  
**Chiến lược:** Xây mới hoàn toàn (Greenfield) | **Nền tảng:** Django/Python | **Database:** SQLite  

---

## 1. GIỚI THIỆU & CĂN CỨ PHÁP LÝ (COMPLIANCE)
Hệ thống được xây dựng để vận hành chính thức từ **01/01/2026**, tuân thủ tuyệt đối các văn bản (Cập nhật Công báo Chính phủ):

| Lĩnh vực | Văn bản căn cứ | Nội dung trọng tâm áp dụng cho hệ thống |
| :--- | :--- | :--- |
| **Kế toán** | **Thông tư 99/2025/TT-BTC** | Chế độ kế toán DN mới (Thay thế TT 200). Hệ thống 71 TK cấp 1. |
| **Thuế GTGT** | **Luật 48/2024 & 149/2025** | Quy định khấu trừ, ngưỡng doanh thu và thuế suất mới 2026. |
| **Thuế TNDN** | **Luật 67/2025/QH15** | **Thuế suất ưu đãi 15% - 17%** cho SME tùy quy mô doanh thu. |
| **Giao dịch số** | **Luật Giao dịch điện tử 2023** | Giá trị pháp lý chứng từ số và chữ ký số từ xa (Remote Signing). |
| **Dữ liệu** | **Nghị định 13/2023/NĐ-CP** | Bảo vệ dữ liệu cá nhân (PII), mã hóa lương và số định danh. |
| **An ninh** | **Luật An ninh mạng** | Yêu cầu lưu trữ dữ liệu tại Việt Nam (Intranet/Local Server). |

---

## 2. PHẠM VI NGHIỆP VỤ & CHỨC NĂNG (FUNCTIONAL SCOPE)

### 2.1 Module M4: Kế toán Tổng hợp (Cốt lõi)
* **FR-4.1 (Seed Data):** Tự động nạp đầy đủ **71 tài khoản cấp 1** và **101 tài khoản cấp 2** theo Phụ lục II TT 99. Không cho phép hiệu chỉnh tên gọi/số hiệu gốc.
* **FR-4.2 (Opening Balance):** Chức năng nhập số dư đầu kỳ thủ công/Excel cho năm tài chính đầu tiên (2026).
* **FR-4.3 (Event-driven):** Cơ chế tự động sinh bút toán từ các giao dịch (Bán hàng -> Nợ 131/Có 511, 3331).

### 2.2 Module M1 & M8: Bán hàng, Hóa đơn & Thuế
* **FR-1.1:** Phát hành HĐĐT theo NĐ 70/2025. Tích hợp ký số tập trung (HSM/Cloud Token).
* **FR-8.1 (eTax Sync):** Tự động tải hóa đơn đầu vào từ cổng Tổng cục Thuế để đối soát 3 bên (Hóa đơn - PO - Kho).
* **FR-8.2:** Cảnh báo các hóa đơn có MST thuộc danh sách rủi ro cao của CQT.

### 2.3 Module M7: Lương & Bảo hiểm (Sửa đổi 2026)
* **FR-7.1:** Tính lương theo mức tham chiếu mới và tỷ lệ trích nộp theo **Luật BHXH 2024**.
* **FR-7.2:** Tự động tính thuế TNCN theo biểu thuế lũy tiến và mức giảm trừ gia cảnh mới nhất.

### 2.4 Module M13 & M14: Báo cáo Tài chính & Quản trị
* **FR-13.1:** Tự động xuất 4 báo cáo chính (Bảng Cân đối, Kết quả KD, Lưu chuyển tiền tệ, Thuyết minh) đúng mẫu Phụ lục IV TT 99.
* **FR-14.1:** Dashboard quản trị (Intranet): Theo dõi dòng tiền, lãi gộp và tuổi nợ khách hàng real-time.

---

## 3. YÊU CẦU KỸ THUẬT & HẠ TRẦN (TECHNICAL DESIGN)

### 3.1 Stack Công nghệ & Môi trường
* **Backend:** Django 5.x (Python 3.12+).
* **Frontend:** Django Templates + Tailwind CSS + Alpine.js (Giao diện Tiếng Việt chuyên ngành).
* **Database:** **SQLite 3** (Cấu hình chế độ WAL để hỗ trợ đa người dùng trong Intranet).
* **Kiến trúc:** Monolithic tích hợp **Django REST Framework (DRF)** cho API giai đoạn sau.

### 3.2 Nguyên tắc Dữ liệu (Master Data Integrity)
* **Bất biến:** Các danh mục (Tài khoản, Loại chứng từ, Chỉ tiêu báo cáo) được nạp qua Fixtures/Seed script.
* **Hàng rào bảo vệ:** Sử dụng Django Signals/Middleware để chặn mọi hành vi UPDATE/DELETE đối với Master Data pháp lý.

### 3.3 Bảo mật & Quyền riêng tư
* **Mã hóa:** Mã hóa AES-256 các trường dữ liệu nhạy cảm (Lương, CCCD) theo Nghị định 13.
* **Audit Trail:** Hệ thống lưu vết 100% thay đổi (Người sửa, thời gian, giá trị cũ/mới).
* **Intranet Only:** Cấu hình Access Control List (ACL) chỉ cho phép truy cập từ dải IP nội bộ doanh nghiệp.

---

## 4. LỘ TRÌNH TRIỂN KHAI (4 SPRINT - 16 TUẦN)

* **Sprint 1 (Tuần 1-4):** Thiết lập Core Django, nạp Seed Data 71 TK và chứng từ mẫu.
* **Sprint 2 (Tuần 5-8):** Phát triển Module Bán hàng, Mua hàng, Công nợ và tích hợp API HĐĐT.
* **Sprint 3 (Tuần 9-12):** Module Lương, Thuế và bộ Báo cáo tài chính chuẩn TT 99.
* **Sprint 4 (Tuần 13-16):** Dashboard quản trị, Kiểm thử bảo mật (VAPT) và Go-live nội bộ.

---

## 5. PHÊ DUYỆT (SIGN-OFF)
*Tài liệu này là căn cứ cuối cùng sau khi khôi phục sự cố HDD.*

| Vai trò | Đại diện | Chữ ký xác nhận |
| :--- | :--- | :--- |
| **Kế toán trưởng** | [Họ tên] | ............................ |
| **Lead BA/Architect**| Gemini | ............................ |
| **Giám đốc dự án** | [Họ tên] | ............................ |

---

**Ghi chú:** Toàn bộ thuật ngữ trong Web App sẽ sử dụng chuẩn 100% tiếng Việt chuyên ngành (Ví dụ: "Hao mòn lũy kế", "Lợi nhuận sau thuế chưa phân phối"). 

Bạn có muốn tôi xuất file **Script Seed Data (JSON)** chứa đầy đủ 71 tài khoản cấp 1 của TT 99 để đội Dev nạp vào SQLite ngay không?