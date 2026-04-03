# THIẾT KẾ KỸ THUẬT CHI TIẾT (TECHNICAL DESIGN) - V5.0
**Dự án:** Hệ thống Kế toán SME Greenfield (TT 99/2025/TT-BTC)  
**Ngôn ngữ:** Python 3.12+ | **Framework:** Django 5.x  
**Database:** SQLite 3 (WAL Mode) | **OS Phát triển:** Windows 10/11  

---

## 1. KIẾN TRÚC HỆ THỐNG (SYSTEM ARCHITECTURE)

### 1.1 Cấu trúc Monolithic-Hybrid
Hệ thống sử dụng kiến trúc Django Monolithic truyền thống để triển khai nhanh trong Intranet, nhưng tách biệt lớp API (Django REST Framework) để sẵn sàng cho các thiết bị ngoại vi (Mobile scan kho, máy POS).

### 1.2 Môi trường phát triển (Windows Environment)
* **OS:** Windows 10/11 64-bit.
* **Interpreter:** CPython 3.12.
* **Tooling:** * **Virtualenv:** Cô lập thư viện.
    * **Line Endings:** Bắt buộc cấu hình Git `core.autocrlf true` nhưng IDE (VS Code/PyCharm) phải đặt `EndOfLine = LF` để tương thích đa nền tảng.
    * **Path Handling:** Sử dụng thư viện `pathlib` để xử lý đường dẫn tệp tin, tránh lỗi dấu xoẹt (`/` vs `\`) giữa Windows và Linux.

---

## 2. THIẾT KẾ CƠ SỞ DỮ LIỆU (DATABASE DESIGN)

### 2.1 Cấu hình SQLite tối ưu cho Intranet
Để khắc phục nhược điểm của SQLite khi có nhiều người dùng trong mạng nội bộ, hệ thống bắt buộc cấu hình:
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db' / 'accounting_tt99.sqlite3',
        'OPTIONS': {
            'timeout': 30,  # Chờ 30s nếu DB đang bị lock
            'init_command': (
                'PRAGMA journal_mode=WAL;'  # Cho phép đọc ghi đồng thời
                'PRAGMA synchronous=NORMAL;' # Tăng tốc độ ghi file
                'PRAGMA foreign_keys=ON;'    # Đảm bảo ràng buộc dữ liệu
            ),
        },
    }
}
```

### 2.2 Master Data Integrity (Dữ liệu Pháp lý nguyên bản)
Các Model thuộc Thông tư 99 (Hệ thống tài khoản, Danh mục chứng từ) được thiết kế **Chỉ đọc (Read-only)** sau khi Seed.
* **Seed Source:** Toàn bộ 71 tài khoản cấp 1 và 101 tài khoản cấp 2 từ Phụ lục II.
* **Bảo vệ:** Sử dụng `Django Signals (pre_save)` để chặn mọi hành vi chỉnh sửa Master Data.

---

## 3. LỚP LOGIC NGHIỆP VỤ (SERVICE LAYER & TDD)

### 3.1 Quy trình phát triển TDD (Test-Driven Development)
Mọi module nghiệp vụ (Thuế, Lương, Kết chuyển) phải tuân thủ quy trình:
1.  **Viết Test Case:** Dựa trên ví dụ số liệu trong TT 99.
2.  **Chạy Test (Fail):** Xác nhận logic chưa tồn tại.
3.  **Viết Service Code:** Thực hiện logic tối thiểu để pass test.
4.  **Refactor:** Tối ưu mã nguồn và cập nhật Docstring.

### 3.2 Tiêu chuẩn Docstring Pháp lý
Mỗi hàm nghiệp vụ bắt buộc trích dẫn văn bản luật để phục vụ mục đích giải trình:
```python
def tinh_thue_tndn_sme(loi_nhuan):
    """
    Tính thuế suất ưu đãi cho SME theo doanh thu.
    Căn cứ: Điều 10 Luật Thuế TNDN 67/2025/QH15.
    """
```

---

## 4. CHIẾN LƯỢC BẢO MẬT & COMPLIANCE

### 4.1 Bảo vệ dữ liệu cá nhân (Nghị định 13)
* **Encryption at Rest:** Sử dụng thư viện `cryptography` để mã hóa các trường nhạy cảm trong SQLite (Lương, số định danh).
* **Audit Trail:** Model nền tảng `AbstractAuditModel` tự động ghi lại: `user_id`, `timestamp`, `action`, `ip_address`.

### 4.2 Triển khai Cross-Platform
* **Windows Host:** Sử dụng `Waitress` làm WSGI Server để chạy ổn định trên môi trường Windows Intranet.
* **Linux Host:** Sử dụng `Gunicorn` + `Nginx`.

---

## 5. CẤU TRÚC THƯ MỤC DỰ ÁN (PROJECT STRUCTURE)

```text
SME_Accounting_TT99/
├── core/                   # Cấu hình Django & Security Middleware
├── apps/
│   ├── danh_muc/           # Master data: Tài khoản, Chứng từ mẫu (Seed only)
│   │   ├── fixtures/       # File JSON chứa 71 TK nguyên bản TT 99
│   │   └── signals.py      # Chặn Update/Delete Master Data
│   ├── nghiep_vu/          # Bán hàng, Mua hàng, Kho, Lương
│   │   ├── services.py     # Logic hạch toán (TDD focus)
│   │   └── tests/          # Bộ Test case nghiệp vụ
│   └── bao_cao/            # Kết xuất BCTC mẫu Phụ lục IV
├── static/                 # CSS/JS phục vụ giao diện Tiếng Việt
├── manage.py
└── requirements.txt        # Bao gồm django, cryptography, pytest-django
```

---

**Kết luận:** Bản thiết kế này đảm bảo hệ thống kế toán sẽ vận hành chính xác như một bản "số hóa" của Thông tư 99, chạy ổn định trên Windows trong mạng nội bộ và cực kỳ dễ bảo trì nhờ bộ máy Test và Docstring trích dẫn luật rõ ràng.
hãy cập nhật technical design