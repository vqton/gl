# THIẾT KẾ KỸ THUẬT CHI TIẾT (TECHNICAL DESIGN) - V6.0
**Dự án:** Hệ thống Kế toán SME Greenfield (TT 99/2025/TT-BTC)  
**Trọng tâm:** Inventory Valuation Engine & Windows Optimization

---

## 2. THIẾT KẾ CƠ SỞ DỮ LIỆU (DATABASE DESIGN) - CẬP NHẬT

### 2.3 Cấu trúc Kho & Giá vốn (Inventory Schema)
Để hỗ trợ đa phương pháp tính giá (Đích danh, FIFO, Bình quân), Schema được thiết kế theo mô hình **Traceable Logs**:

* **Model `VatTuHangHoa`:** Lưu cấu hình phương pháp tính giá (`VALUATION_METHOD`).
* **Model `KhoLot` (Mới):** Quản lý theo Lô/Serial cho phương pháp **Đích danh**.
* **Model `KhoEntry`:** Lưu vết nhập/xuất.
    * `gia_von_tam_tinh`: Giá trị tại thời điểm ghi sổ.
    * `gia_von_chinh_thuc`: Giá trị sau khi chạy Engine tính toán lại (Recalculated).

### 2.4 Xử lý Concurrency trên Windows (SQLite WAL)
Trong môi trường mạng nội bộ, để tránh lỗi `database is locked` khi nhiều kế toán cùng nhập liệu và Engine tính giá đang chạy ngầm:
* **Busy Timeout:** Tăng lên 30s.
* **Transaction Isolation:** Sử dụng `transaction.atomic()` của Django với cơ chế "Immediate" cho các tác vụ tính toán lại giá vốn toàn bộ sổ kho.

---

## 3. ENGINE TÍNH GIÁ VỐN (VALUATION ENGINE - NEW)

### 3.1 Valuation Strategy Pattern
Hệ thống sử dụng **Strategy Pattern** để tách biệt logic tính toán:
1.  **SpecificIdentificationStrategy:** Khớp `lot_id` của phiếu xuất với `lot_id` của phiếu nhập.
2.  **FIFOStrategy:** Sử dụng cấu trúc dữ liệu **Queue** (First-In, First-Out) dựa trên thời gian thực tế nhập kho.
3.  **WeightedAverageStrategy:** Tính giá bình quân liên hoàn (Perpetual).

### 3.2 Cơ chế Recalculation (Xử lý Backdating)
Đây là logic quan trọng nhất để đảm bảo tính đúng đắn pháp lý khi kế toán sửa/chèn chứng từ trong quá khứ:
* **Trigger:** Khi một phiếu nhập cũ bị sửa đơn giá hoặc chèn mới phiếu nhập vào giữa kỳ.
* **Process:** Engine sẽ tìm tất cả các phiếu xuất của mặt hàng đó có `ngay_chung_tu` lớn hơn hoặc bằng phiếu bị sửa.
* **Action:** Chạy lại luồng tính giá và cập nhật trường `gia_von_chinh_thuc` cho các phiếu xuất đó.

---

## 4. CHIẾN LƯỢC BẢO MẬT & COMPLIANCE

### 4.1 Mã hóa dữ liệu (Nghị định 13)
* **Field-level Encryption:** Sử dụng `django-fernet-fields` hoặc `cryptography` để mã hóa các trường: `so_tien_luong`, `mst_ca_nhan`, `so_dien_thoai_khach_hang`. 
* **Key Management:** Key mã hóa được lưu trong biến môi trường (Environment Variable) trên Windows Server, không commit lên Git.

---

## 5. CẤU TRÚC THƯ MỤC DỰ ÁN (PROJECT STRUCTURE) - CẬP NHẬT

```text
SME_Accounting_TT99/
├── core/
├── apps/
│   ├── danh_muc/
│   ├── kho/                    # MODULE MỚI
│   │   ├── valuation/          # Engine tính giá vốn (FIFO, BQ, Đích danh)
│   │   ├── services.py         # Xử lý nhập/xuất/điều chuyển
│   │   └── signals.py          # Trigger Recalculate giá vốn khi có thay đổi
│   ├── nghiep_vu/              # Bán hàng, Mua hàng, Thuế
│   └── bao_cao/                # Drill-down từ BCTC xuống Sổ kho
├── db/                         # Thư mục chứa file .sqlite3 (Chỉ định quyền Write cho User Windows)
├── requirements.txt            # Thêm: pandas (xử lý tính toán kho nhanh), cryptography
└── .gitignore                  # Chặn file .sqlite3-wal và .sqlite3-shm
```

---

## 6. QUY TRÌNH TRIỂN KHAI TRÊN WINDOWS (DEPLOYMENT)

1.  **WSGI Server:** Sử dụng `Waitress` vì đây là server thuần Python, chạy ổn định nhất trên Windows mà không cần cấu hình phức tạp như Gunicorn.
2.  **Static Files:** Sử dụng `WhiteNoise` để Django tự phục vụ file tĩnh, giúp tối giản hóa việc cài đặt Nginx trên Windows Intranet.
3.  **Scheduled Tasks:** Sử dụng **Windows Task Scheduler** để chạy lệnh `python manage.py recalculate_inventory` vào 23:00 mỗi ngày (đối với phương pháp Bình quân cuối kỳ).

---

**Kết luận:** Bản V6.0 này biến hệ thống từ một phần mềm nhập liệu đơn thuần thành một **Engine kế toán mạnh mẽ**, có khả năng tự sửa lỗi số liệu (Self-correcting) khi có thay đổi trong quá khứ, đáp ứng tiêu chuẩn khắt khe nhất của một Kế toán trưởng dày dạn kinh nghiệm.

**Bước tiếp theo:** Bạn có muốn tôi viết mã nguồn mẫu cho **`InventoryValuationService`** – trái tim của hệ thống này – để xử lý logic Bình quân gia quyền liên hoàn không?