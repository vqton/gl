# CHIẾN LƯỢC KIỂM THỬ (TEST STRATEGY) - V1.0
**Dự án:** Hệ thống Kế toán SME Greenfield (TT 99/2025/TT-BTC)  
**Phương pháp luận:** Test-Driven Development (TDD) - Red/Green/Refactor  
**Mục tiêu:** Sai sót logic nghiệp vụ = 0.

---

## 1. CẤU TRÚC KIM TỰ THÁP KIỂM THỬ (TEST PYRAMID)
Chúng ta tập trung trọng tâm vào **Unit Tests** để đảm bảo các công thức thuế và hạch toán đúng tuyệt đối.

| Loại Test | Tỷ trọng | Mục tiêu | Công cụ |
| :--- | :--- | :--- | :--- |
| **Unit Tests** | 70% | Kiểm tra các hàm `services.py` (tính thuế, kết chuyển, hạch toán). | `pytest`, `unittest` |
| **Integration Tests** | 20% | Kiểm tra luồng dữ liệu giữa API, Service và SQLite (WAL mode). | `django.test.Client` |
| **System/E2E Tests** | 10% | Kiểm tra luồng nghiệp vụ hoàn chỉnh (Bán hàng -> Thu tiền -> BCTC). | `Playwright` / `Selenium` |

---

## 2. QUY TRÌNH THỰC THI TDD BẮT BUỘC

Lập trình viên phải tuân thủ chu kỳ **3 bước** cho mọi Ticket nghiệp vụ:

1.  **Giai đoạn RED (Viết Test trước):**
    * Dựa vào số liệu ví dụ trong Phụ lục Thông tư 99.
    * Viết Test Case định nghĩa đầu vào (Input) và kết quả mong đợi (Expected Output).
    * Chạy lệnh `pytest` -> Kết quả phải là **FAIL**.
2.  **Giai đoạn GREEN (Viết Code tối thiểu):**
    * Viết mã nguồn trong `services.py` vừa đủ để Test Case vượt qua.
    * Chạy lệnh `pytest` -> Kết quả phải là **PASS**.
3.  **Giai đoạn REFACTOR (Tối ưu):**
    * Chỉnh sửa code cho sạch (Clean code), cập nhật **Docstring trích dẫn luật**.
    * Chạy lại Test -> Đảm bảo vẫn **PASS**.

---

## 3. DANH MỤC KIỂM THỬ TRỌNG YẾU (HIGH-PRIORITY TEST CASES)

### 3.1 Kiểm thử Master Data (Bất biến)
* **Test Case:** Đảm bảo sau khi Seed, hệ thống có đủ 71 tài khoản cấp 1.
* **Test Case:** Thử thực hiện lệnh `DELETE` một tài khoản chuẩn -> Kết quả mong đợi: `PermissionDenied` hoặc `ValidationError`.

### 3.2 Kiểm thử Logic Hạch toán (Accounting Logic)
* **Quy tắc cân đối:** Mọi bút toán phải có Tổng Nợ = Tổng Có.
* **Quy tắc tài khoản:** Ví dụ: TK 111 (Tiền mặt) không được có số dư âm tại bất kỳ thời điểm nào (nếu cấu hình chặn âm).

### 3.3 Kiểm thử Thuế (Tax Compliance)
* **SME Tax Test:** Giả lập doanh thu 2,9 tỷ VNĐ -> Kiểm tra thuế suất TNDN phải là **15%**.
* **GTGT 2024 Test:** Kiểm tra việc tách thuế GTGT đầu vào đối với các hóa đơn > 20 triệu đồng (phải có chứng từ thanh toán ngân hàng).

---

## 4. MÔI TRƯỜNG VÀ CÔNG CỤ (WINDOWS DEV ENVIRONMENT)

* **Test Database:** Sử dụng **SQLite In-memory** (`:memory:`) để chạy Unit Test cực nhanh (tốc độ hàng nghìn test/giây).
* **Isolation:** Sử dụng `@pytest.mark.django_db` để mỗi Test Case chạy trong một Transaction riêng biệt, tự động Rollback sau khi xong (không làm bẩn dữ liệu thật).
* **Mocking:** Sử dụng `unittest.mock` để giả lập các API bên ngoài (Cổng eTax, Chữ ký số) nhằm tránh phụ thuộc mạng Intranet khi đang chạy Test.

---

## 5. QUY ĐỊNH VỀ ĐỘ BAO PHỦ (CODE COVERAGE)

* **Công cụ:** `pytest-cov`.
* **Chỉ tiêu:** * Toàn bộ thư mục `apps/*/services.py`: **100% Coverage**.
    * Toàn bộ thư mục `apps/*/models.py`: **90% Coverage**.
* **Báo cáo:** Mỗi bản Build/Commit phải đi kèm báo cáo Coverage dạng HTML.

---

## 6. MẪU MỘT UNIT TEST CHUẨN (TDD STYLE)

```python
import pytest
from decimal import Decimal
from apps.nghiep_vu.services import tinh_thue_tndn_sme

def test_tinh_thue_tndn_duoi_3_ty():
    """
    TDD Test: Doanh nghiệp có doanh thu < 3 tỷ phải hưởng thuế suất 15%.
    Căn cứ: Luật 67/2025/QH15.
    """
    # 1. Setup (Dữ liệu giả lập)
    doanh_thu = Decimal('2500000000') # 2.5 tỷ
    loi_nhuan = Decimal('100000000')  # 100 triệu
    
    # 2. Action (Thực thi hàm service)
    thue_phai_nop = tinh_thue_tndn_sme(doanh_thu, loi_nhuan)
    
    # 3. Assert (Xác nhận kết quả)
    assert thue_phai_nop == Decimal('15000000') # 15% của 100 triệu
```

---

**Lời khuyên của chuyên gia:** Trong môi trường Windows Dev, bạn nên cài đặt extension **"Python Test Explorer"** trên VS Code để có thể quan sát trực quan các "chấm xanh" (Pass) và "chấm đỏ" (Fail) ngay khi đang gõ code.

Bạn có muốn tôi viết một bộ **Test Cases mẫu cho Module Kết chuyển cuối kỳ (TK 911)** - phần phức tạp nhất của Thông tư 99 không?