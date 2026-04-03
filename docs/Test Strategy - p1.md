Chào bạn, với vai trò là **Chuyên gia TDD**, tôi đã tiến hành cập nhật bản **Chiến lược Kiểm thử lên V2.0**.

Lần cập nhật này tập trung vào việc thiết lập các kịch bản kiểm thử "cực đoan" cho **Engine tính giá kho** và quy trình **Backdating**. Chúng ta không chỉ test để xem code có chạy đúng không, mà test để đảm bảo số liệu kế toán luôn có tính **toàn vẹn và giải trình được** ngay cả khi dữ liệu bị sửa đổi trong quá khứ.

---

# CHIẾN LƯỢC KIỂM THỬ (TEST STRATEGY) - V2.0
**Dự án:** Hệ thống Kế toán SME Greenfield (TT 99/2025/TT-BTC)  
**Trọng tâm:** Integrity of Financial Data & Inventory Backdating  
**Phương pháp:** TDD (Red/Green/Refactor)

---

## 1. CẬP NHẬT KIM TỰ THÁP KIỂM THỬ (TEST PYRAMID)

Chúng ta bổ sung thêm một tầng kiểm thử đặc thù gọi là **Data Integrity Tests** nằm giữa Unit và Integration.

| Loại Test | Tỷ trọng | Mục tiêu |
| :--- | :--- | :--- |
| **Unit Tests** | 60% | Logic thuế, lương, hạch toán cơ bản. |
| **Integrity Tests** | 20% | **(MỚI)** Kiểm tra tính đúng đắn của giá vốn sau khi Recalculate (Backdating). |
| **Integration Tests** | 15% | Luồng ghi sổ SQLite WAL, Audit Trail. |
| **E2E Tests** | 5% | Luồng BCTC từ chứng từ gốc. |

---

## 2. DANH MỤC KIỂM THỬ TRỌNG YẾU (CẬP NHẬT V2.0)

### 2.1 Kiểm thử Engine tính giá kho (Valuation Engine)
Đây là phần quan trọng nhất để đáp ứng yêu cầu của Kế toán trưởng:
* **Test Case FIFO:** Nhập 10 cái giá 10k, nhập 10 cái giá 12k. Xuất 15 cái -> Test xác nhận giá vốn = $(10 \times 10.000) + (5 \times 12.000)$.
* **Test Case Đích danh:** Xuất một mặt hàng gắn mã `Lot_001` -> Test xác nhận giá vốn phải lấy từ đúng phiếu nhập có mã `Lot_001`.
* **Test Case Bình quân tức thời:** Kiểm tra đơn giá vốn thay đổi chính xác sau mỗi lần nhập mới (độ chính xác 4 số thập phân).

### 2.2 Kiểm thử Backdating & Recalculation (Kịch bản sửa quá khứ)
* **Kịch bản:** 1. Ngày 01/01: Nhập kho (Phiếu A).
    2. Ngày 05/01: Xuất kho (Phiếu B) -> Giá vốn tính theo Phiếu A.
    3. Ngày 10/01: Sửa lại đơn giá trên Phiếu A (Ngày 01/01).
* **Mong đợi (Assert):** Hệ thống tự động kích hoạt Signal, tính toán lại và cập nhật `gia_von_chinh_thuc` trên Phiếu B (Ngày 05/01) ngay lập tức.

---

## 3. KIỂM THỬ BẢO MẬT & TUÂN THỦ (NGHỊ ĐỊNH 13)

### 3.1 Encryption Integrity Test
* **Test Case:** Truy vấn trực tiếp vào DB SQLite bằng SQL thô (`SELECT so_tien_luong FROM bảng_lương`).
* **Assert:** Dữ liệu trả về phải là chuỗi mã hóa (Binary/Base64), không được hiển thị số tiền rõ ràng.

### 3.2 Audit Trail Test
* **Test Case:** Thực hiện sửa thông tin `Mã số thuế` khách hàng.
* **Assert:** Kiểm tra bảng `audit_logs` phải có dòng ghi nhận: `Giá trị cũ`, `Giá trị mới`, `User thực hiện`, `Thời gian thực tế`.

---

## 4. QUY ĐỊNH ĐỘ BAO PHỦ (CODE COVERAGE) - NGHIÊM NGẶT

* **Module Kho & Giá vốn:** **100% Branch Coverage** (Phải test mọi nhánh rẽ của logic tính giá).
* **Module Thuế & BCTC:** **100% Statement Coverage**.
* **Công cụ giám sát:** `pytest-cov` kết hợp với `Coverage.py` để xuất báo cáo dạng biểu đồ mỗi khi chạy Pipeline.

---

## 5. MẪU TEST CASE CHO BACKDATING (PYTHON/PYTEST)

```python
@pytest.mark.django_db
def test_recalculate_gia_von_khi_sua_phieu_nhap_cu():
    """
    Test logic tự động tính lại giá vốn khi có sự thay đổi trong quá khứ.
    """
    # 1. Setup: Tạo phiếu nhập A và phiếu xuất B sau đó
    item = create_item(phuong_phap='BINH_QUAN')
    phieu_nhap_A = create_phieu_nhap(item, ngay='2026-01-01', gia=10000)
    phieu_xuat_B = create_phieu_xuat(item, ngay='2026-01-05')
    
    assert phieu_xuat_B.gia_von == 10000
    
    # 2. Action: Sửa giá phiếu nhập A (Backdating)
    phieu_nhap_A.gia = 12000
    phieu_nhap_A.save() # Signal sẽ kích hoạt recalculate_inventory()
    
    # 3. Assert: Kiểm tra phiếu xuất B đã được cập nhật
    phieu_xuat_B.refresh_from_db()
    assert phieu_xuat_B.gia_von == 12000
```

---

**Kết luận:** Bản V2.0 chuyển trọng tâm từ "kiểm tra tính năng" sang "kiểm tra tính chính xác của dữ liệu tài chính lùi thời gian". Đây là nền tảng cốt lõi để hệ thống kế toán SME Greenfield đứng vững trước mọi kỳ quyết toán thuế.

**Bước tiếp theo:** Bạn có muốn tôi thiết kế một **Bộ dữ liệu mẫu (Test Data Suite)** bao gồm 50 tình huống nghiệp vụ thực tế từ Thông tư 99 để chạy thử nghiệm tự động không?