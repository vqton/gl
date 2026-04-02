# TIÊU CHUẨN LẬP TRÌNH (CODING STANDARD) - V8.0
**Dự án:** Hệ thống Kế toán SME Greenfield (TT 99/2025/TT-BTC)  
**Nền tảng:** Python 3.12+ | Django 5.x | SQLite (WAL Mode)  
**Hệ điều hành Dev:** Windows 10/11  

---

## 1. TIÊU CHUẨN ĐẶT TÊN (NAMING CONVENTIONS)
Áp dụng quy tắc **Hybrid**: Kỹ thuật dùng Tiếng Anh, Nghiệp vụ dùng Tiếng Việt không dấu (theo sát văn bản pháp luật).

### 1.1 Quy tắc chung (PEP 8)
* **Class:** `PascalCase` (Ví dụ: `HeThongTaiKhoan`, `PhieuThu`).
* **Functions/Variables:** `snake_case` (Ví dụ: `tinh_thue_gtgt()`, `so_tien_nguyen_te`).
* **Constants:** `UPPER_SNAKE_CASE` (Ví dụ: `THUE_SUAT_SME_2026 = 0.15`).

### 1.2 Thuật ngữ Pháp lý bắt buộc
Tuyệt đối không dịch sai thuật ngữ để tránh nhầm lẫn khi đối soát với Thông tư 99:
* Dùng `no_tk` / `co_tk` (không dùng `debit`/`credit`).
* Dùng `doi_ung` (không dùng `offset`).
* Dùng `nguyen_gia` / `hao_mon_luy_ke`.

---

## 2. QUY TRÌNH PHÁT TRIỂN TDD (TEST-DRIVEN DEVELOPMENT)
Mọi chức năng nghiệp vụ phải được chứng thực bằng Test Case trước khi viết code.

1.  **Red (Viết Test):** Dựa trên ví dụ số liệu trong Phụ lục TT 99. Chạy Test và xác nhận Thất bại.
2.  **Green (Viết Code):** Viết logic tối thiểu trong `services.py` để Test vượt qua.
3.  **Refactor (Tối ưu):** Chuẩn hóa mã nguồn, cập nhật Docstring mà không làm gãy Test.
* **Yêu cầu Coverage:** Module Kế toán & Thuế phải đạt **>95%**.

---

## 3. TIÊU CHUẨN DOCSTRING (DOCUMENTATION)
Mọi hàm nghiệp vụ phải có Docstring chuẩn Google Style kèm **trích dẫn văn bản luật**.

```python
def tinh_thue_tndn_sme(doanh_thu_nam, loi_nhuan_truoc_thue):
    """
    Tính thuế TNDN ưu đãi cho SME.

    Căn cứ pháp lý:
        - Luật số 67/2025/QH15 về Thuế TNDN.
        - Nghị định 320/2025/NĐ-CP.

    Args:
        doanh_thu_nam (Decimal): Doanh thu thuần lũy kế.
        loi_nhuan_truoc_thue (Decimal): Lợi nhuận kế toán (TK 821).

    Returns:
        Decimal: Số thuế phải nộp.
    """
```

---

## 4. TIÊU CHUẨN DỮ LIỆU & SQLITE (WINDOWS FOCUS)

### 4.1 Kiểu dữ liệu Tiền tệ
* Luôn sử dụng `DecimalField(max_digits=20, decimal_places=2)`. 
* **Cấm** sử dụng `FloatField` để tránh sai số lũy kế.

### 4.2 Master Data Bất biến (TT 99)
* Dữ liệu 71 tài khoản cấp 1 và 101 tài khoản cấp 2 phải được nạp từ **Seed Fixtures**.
* Sử dụng `Signals` để chặn quyền `Update/Delete` đối với các bản ghi Master Data chuẩn pháp luật.

### 4.3 Cấu hình Windows & SQLite
* **Path Handling:** Sử dụng `pathlib` để tương thích Windows/Linux.
* **Concurrency:** Bắt buộc kích hoạt `PRAGMA journal_mode=WAL;` để tránh lỗi "Database is locked" trong mạng nội bộ.

---

## 5. BẢO MẬT & COMPLIANCE (NGHỊ ĐỊNH 13)

* **Mã hóa (Encryption):** Mã hóa AES-256 các trường nhạy cảm (Lương, số định danh) trước khi lưu vào SQLite.
* **Nhật ký (Audit Trail):** Mọi Model nghiệp vụ bắt buộc lưu vết: `user_id`, `timestamp`, `action`, `ip_address`, `data_diff`.
* **Intranet Security:** Cấu hình `ALLOWED_HOSTS` chỉ chấp nhận IP trong dải mạng nội bộ.

---

## 6. GIAO DIỆN & TRẢI NGHIỆM NGƯỜI DÙNG

* **Ngôn ngữ:** 100% Tiếng Việt có dấu, font chữ Inter/Roboto rõ ràng.
* **Định dạng số:** `1.234.567,89` (Dấu chấm phân cách hàng nghìn, dấu phẩy phân cách thập phân).
* **Trạng thái chứng từ:** Màu sắc phân biệt rõ rệt (Đã ghi sổ: Xanh, Nháp: Xám, Hủy: Đỏ).

---

## 7. CẤU TRÚC GIT & COMMIT

* **Line Endings:** Cấu hình IDE dùng `LF` (không dùng CRLF của Windows) để tránh xung đột mã nguồn.
* **Commit Message:** `[Module] - [Hành động] - [Mô tả chi tiết]`
    * *Ví dụ:* `[M4-Ketoan] - Seed - Nạp nguyên bản 71 tài khoản cấp 1 từ Phụ lục II TT 99`.

---

**Kết luận:** Bản tiêu chuẩn V8.0 này đảm bảo hệ thống kế toán có độ tin cậy cực cao, dễ bảo trì và hoàn toàn minh bạch về mặt pháp lý. 

