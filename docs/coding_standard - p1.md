# TIÊU CHUẨN LẬP TRÌNH (CODING STANDARD) - V9.0
**Dự án:** Hệ thống Kế toán SME Greenfield (TT 99/2025/TT-BTC)  
**Trọng tâm:** Độ chính xác tài chính & Engine tính giá kho  
**Nền tảng:** Python 3.12+ | Django 5.x | SQLite (WAL Mode)

---

## 1. TIÊU CHUẨN ĐẶT TÊN & THUẬT NGỮ (CẬP NHẬT)

### 1.3 Thuật ngữ Kho & Giá vốn (Bắt buộc)
Để thống nhất giữa Dev và Kế toán trưởng, cấm sử dụng các từ chung chung:
* **Giá vốn:** `gia_von` (không dùng `cost`).
* **Đích danh:** `dich_danh` (không dùng `manual_match`).
* **Bình quân liên hoàn:** `binh_quan_lien_hoan` (không dùng `moving_average`).
* **Nhập bù / Tính lại:** `tinh_lai_gia_von` (không dùng `recalculate`).

---

## 2. QUY TRÌNH TDD CHO NGHIỆP VỤ KHO (QUY ĐỊNH MỚI)

Mọi thay đổi liên quan đến kho phải vượt qua 3 tầng Test đặc thù:
1.  **Test Case Nhập/Xuất thông thường:** Đảm bảo số lượng tồn kho (Inventory Balance) cập nhật đúng.
2.  **Test Case Giá vốn (Valuation):** Đảm bảo giá vốn xuất kho khớp với phương pháp cấu hình (FIFO/Đích danh/Bình quân).
3.  **Test Case Backdating (Quan trọng):** Giả lập việc chèn một phiếu nhập vào giữa chuỗi giao dịch. Test phải xác nhận các phiếu xuất sau đó đã được tự động cập nhật lại giá vốn (`gia_von_chinh_thuc`).

---

## 4. TIÊU CHUẨN DỮ LIỆU & ĐỘ CHÍNH XÁC (DATA PRECISION)

### 4.1 Quy tắc 4 chữ số thập phân
Đối với các trường liên quan đến giá vốn và đơn giá kho, bắt buộc sử dụng:
* **Đơn giá & Tỷ giá:** `DecimalField(max_digits=20, decimal_places=4)`.
* **Thành tiền (VND):** `DecimalField(max_digits=20, decimal_places=2)`.
* **Lý do:** Tránh sai số làm tròn khi tính toán giá bình quân liên hoàn (Weighted Average).

### 4.4 Xử lý Logic trong Service Layer
* **Cấm tuyệt đối:** Sử dụng `FloatField` hoặc toán tử `/` trực tiếp trên các biến tiền tệ.
* **Bắt buộc:** Sử dụng class `Decimal` từ thư viện standard của Python và thực hiện làm tròn (`quantize`) ở bước cuối cùng trước khi lưu vào Database.

---

## 5. BẢO MẬT & COMPLIANCE (CẬP NHẬT)

### 5.1 Mã hóa theo Nghị định 13
* Sử dụng thư viện `cryptography` để triển khai **Field-level encryption**.
* Các Model chứa thông tin nhạy cảm (Lương, MST cá nhân) phải kế thừa từ `EncryptedModelBase`.
* Key mã hóa phải được nạp từ **Windows Environment Variables**, không được hard-code.

---

## 8. CẤU TRÚC CODE ENGINE (VALUATION STRATEGY)

Để đảm bảo tính mở rộng cho các phương pháp tính giá vốn sau này:
* **Strategy Pattern:** Mỗi phương pháp tính giá (FIFO, BQ, Đích danh) phải là một Class riêng biệt kế thừa từ `BaseValuationStrategy`.
* **Service Interface:**
```python
class InventoryValuationService:
    def recalculate(self, item_id, start_date):
        """
        Logic tính toán lại giá vốn từ một thời điểm nhất định.
        Sử dụng signals để trigger khi có Backdating.
        """
```

---

## 9. QUY TRÌNH COMMIT & LINE ENDINGS (WINDOWS DEV)

* **Line Endings:** Bắt buộc cài đặt `.gitattributes` để ép kiểu `LF` cho toàn bộ file `.py` và `.json`, tránh xung đột khi chạy Test trên môi trường Windows Server.
* **Commit Message:** Phải kèm mã phân hệ (Module ID). 
    * *Ví dụ:* `[M2-KHO] - Update - Implement logic bình quân gia quyền liên hoàn`.

---

**Kết luận:** Bản V9.0 hoàn thiện hóa các kẽ hở về số liệu thập phân và quy trình xử lý kho phức tạp. Đây là tiêu chuẩn cao nhất để đội ngũ Dev bắt đầu hiện thực hóa Engine tính giá vốn.

**Bước tiếp theo:** Bạn có muốn tôi thực hiện **Cập nhật Roadmap** (bổ sung các mốc kiểm thử Backdating cho Kho) dựa trên bản Coding Standard này không?