# LỘ TRÌNH PHÁT TRIỂN & KẾ HOẠCH TRIỂN KHAI (ROADMAP & PLAN)
**Dự án:** Hệ thống Kế toán SME Greenfield (TT 99/2025/TT-BTC)  
**Tổng thời gian dự kiến:** 16 tuần (4 Tháng) | **Đơn vị thực hiện:** Đội dự án Nội bộ.

---

## GIAI ĐOẠN 1: KHỞI TẠO NỀN TẢNG (WEEKS 1 - 2)
*Mục tiêu: Thiết lập môi trường Windows Dev chuẩn và cấu trúc dữ liệu bất biến.*

* **Tuần 1: Setup Môi trường & Core Project**
    * Cài đặt Python 3.12, cấu hình venv trên Windows.
    * Khởi tạo Django 5.x, cấu hình SQLite **WAL Mode** và `pathlib`.
    * Thiết lập **Coding Standard V8.0** vào Git hooks (Pre-commit check).
* **Tuần 2: Master Data Seeding (Pháp lý)**
    * Xây dựng script nạp 71 tài khoản cấp 1 và 101 tài khoản cấp 2 từ Phụ lục II.
    * Viết Unit Test (TDD) xác nhận tính toàn vẹn của danh mục (71/71 bản ghi).
    * Kích hoạt Signal chặn chỉnh sửa Master Data.

---

## GIAI ĐOẠN 2: PHÁT TRIỂN CÁC PHÂN HỆ LÕI (WEEKS 3 - 8)
*Mục tiêu: Hoàn thành các nghiệp vụ phát sinh hàng ngày.*

* **Tuần 3 - 4: Module Tiền tệ & Chứng từ (M4)**
    * UI/UX: Màn hình nhập liệu Phiếu Thu/Chi (No-Icon, Keyboard-first).
    * TDD: Test logic hạch toán Nợ/Có, tự động nhảy số chứng từ.
* **Tuần 5 - 6: Mua hàng, Bán hàng & Thuế (M1, M8)**
    * Xây dựng logic tính thuế GTGT 2024 và thuế TNDN ưu đãi SME 2025.
    * Kết nối API Hóa đơn điện tử (Mock test trong nội bộ).
* **Tuần 7 - 8: Quản lý Kho & Tài sản (M2, M3)**
    * Nghiệp vụ nhập/xuất kho, tính giá xuất kho (FIFO/Bình quân gia quyền).
    * Khấu hao tài sản cố định và tài sản sinh học (TK 215).

---

## GIAI ĐOẠN 3: TỔNG HỢP & BÁO CÁO (WEEKS 9 - 12)
*Mục tiêu: Kết xuất dữ liệu ra Báo cáo tài chính chuẩn pháp luật.*

* **Tuần 9 - 10: Lương & BHXH (M7)**
    * Cập nhật mức đóng BHXH và thuế TNCN theo luật mới 2026.
    * Mã hóa dữ liệu lương (Nghị định 13) trong SQLite.
* **Tuần 11 - 12: Kết chuyển & Báo cáo tài chính (M13)**
    * TDD: Viết test cho bút toán kết chuyển tự động sang TK 911.
    * UI: Thiết kế bảng BCTC (Mẫu A, B - Phụ lục IV) với tính năng **Drill-down**.
    * Xuất file XML/Excel theo chuẩn của Tổng cục Thuế.

---

## GIAI ĐOẠN 4: KIỂM THỬ & TRIỂN KHAI (WEEKS 13 - 16)
*Mục tiêu: Đưa hệ thống vào vận hành Intranet an toàn.*

* **Tuần 13: Stress Test & Security Audit**
    * Giả lập 10-20 kế toán nhập liệu đồng thời trên Windows Server (Test khóa file SQLite).
    * Kiểm tra Audit Trail (Nhật ký thay đổi).
* **Tuần 14: User Acceptance Test (UAT)**
    * Kế toán trưởng trực tiếp kiểm tra 100 kịch bản nghiệp vụ (Sử dụng bàn phím 100%).
* **Tuần 15: Đào tạo & Tài liệu**
    * Viết hướng dẫn sử dụng (User Guide) tập trung vào các phím tắt.
* **Tuần 16: Go-live**
    * Cài đặt Waitress/Nginx trên server Windows nội bộ.
    * Chốt số dư đầu kỳ từ hệ thống cũ sang.

---

## CHI TIẾT KẾ HOẠCH CÀI ĐẶT (INSTALLATION PLAN)

| Hạng mục | Thực hiện | Lưu ý kỹ thuật |
| :--- | :--- | :--- |
| **Server** | Windows Server 2019+ | Cần ổ cứng SSD để SQLite chạy WAL mode tốt nhất. |
| **Web Server** | Waitress (WSGI) | Chạy ổn định và nhẹ trên Windows hơn Gunicorn. |
| **Database** | SQLite 3 | Backup hàng ngày bằng cách copy file `.sqlite3` (vì là file đơn lẻ). |
| **Security** | Firewall Windows | Chỉ mở port 80/443 cho dải IP nội bộ. |
| **Client** | Chrome/Edge | Tối ưu hiển thị font Inter và xử lý Hotkeys JS. |

---

**Rủi ro và Giải pháp:**
* **Rủi ro:** SQLite bị lock khi nhiều người dùng ghi dữ liệu cùng lúc.
* **Giải pháp:** Đã cấu hình `timeout: 30` và `journal_mode: WAL`. Ngoài ra, thiết kế queue xử lý tác vụ ghi nặng (nếu cần) qua `Background Tasks`.

