# INVENTORY USE CASES (I01-I07)
*Based on: TT99/2025, ketoanthienung.net*

---

### 📌 I01 — Nhập kho hàng mua
- **Tác nhân (Actors):** Kế toán, Thủ kho
- **Mục tiêu:** Ghi nhận hàng hóa, NVL, CCDC mua vào được nhập kho
- **Điều kiện tiên quyết (Preconditions):** Có hóa đơn mua hàng, hàng đã về kho
- **Luồng chính (Main Flow):**
  1. Thủ kho nhận hàng, kiểm tra số lượng
  2. Lập phiếu nhập kho (01-VT)
  3. Kế toán kiểm tra và đối chiếu hóa đơn
  4. Ghi nhận: Nợ 156/152/153 / Nợ 1331 / Có 331/111/112
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 1] → Hàng về thiếu: Lập biên bản, theo dõi 151
  - [Bước 1] → Hàng về trước hóa đơn về sau: Theo dõi 151
- **Điều kiện hậu kiểm (Postconditions):** TK 156/152/153 tăng
- **Định khoản:** Nợ 156/152/153 + Nợ 1331 / Có 331

---

### 📌 I02 — Xuất kho hàng bán/sử dụng
- **Tác nhân (Actors):** Kế toán, Thủ kho
- **Mục tiêu:** Ghi nhận xuất kho hàng hóa, NVL để bán hoặc sản xuất
- **Điều kiện tiên quyết (Preconditions):** Có đơn bán hàng, phiếu xuất kho
- **Luồng chính (Main Flow):**
  1. Bộ phận xin xuất kho (Phiếu xuất kho 02-VT)
  2. Thủ kho xuất hàng, giao hàng
  3. Kế toán ghi nhận xuất kho theo pp tính giá (FIFO/BQ/FIFO)
  4. Ghi nhận: Nợ 632/621 / Có 156/152/155
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 3] → Hết hàng: Báo lỗi, chờ nhập hàng
  - [Bước 3] → Giá trị thay đổi: Tính lại theo phương pháp
- **Điều kiện hậu kiểm (Postconditions):** TK 156/152/155 giảm
- **Định khoản:** Nợ 632/621 / Có 156/152/155

---

### 📌 I03 — Chuyển kho nội bộ
- **Tác nhân (Actors):** Kế toán, Thủ kho
- **Mục tiêu:** Chuyển hàng giữa các kho trong cùng doanh nghiệp
- **Điều kiện tiên quyết (Preconditions):** Có lệnh điều chuyển nội bộ
- **Luồng chính (Main Flow):**
  1. Lập phiếu xuất kho chuyển kho
  2. Thủ kho xuất hàng từ kho A
  3. Thủ kho nhập hàng vào kho B
  4. Ghi nhận: Có 156 (kho A) / Nợ 156 (kho B)
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 2] → Hàng hư hỏng: Lập biên bản, xử lý
- **Điều kiện hậu kiểm (Postconditions):** Hàng chuyển sang kho mới
- **Định khoản:** Có 156(A) / Nợ 156(B)

---

### 📌 I04 — Kiểm kê hàng tồn kho
- **Tác nhân (Actors):** Kế toán, Thủ kho, Ban kiểm kê
- **Mục tiêu:** Đối chiếu số lượng hàng thực tế và sổ sách
- **Điều kiện tiên quyết (Preconditions):** Đến kỳ kiểm kê (định kỳ/đột xuất)
- **Luồng chính (Main Flow):**
  1. Ban kiểm kê thực tế đếm hàng tại kho
  2. Lập biên bản kiểm kê (05-VT)
  3. Đối chiếu số thực tế vs sổ sách
  4. Xử lý chênh lệch (nếu có)
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 3] → Thừa: Nợ 156 / Có 338
  - [Bước 3] → Thiếu: Nợ 138 / Có 156
  - [Bước 3] → Hư hỏng: Nợ 811 / Có 156
- **Điều kiện hậu kiểm (Postconditions):** Số liệu kho được xác nhận
- **Định khoản:** Thừa: Nợ 156 / Có 338 | Thiếu: Nợ 138 / Có 156

---

### 📌 I05 — Đánh giá hàng tồn kho cuối kỳ
- **Tác nhân (Actors):** Kế toán
- **Mục tiêu:** Xác định giá trị hàng tồn kho theo giá thị trường
- **Điều kiện tiên quyết (Preconditions):** Cuối kỳ kế toán, lập BCTC
- **Luồng chính (Main Flow):**
  1. Lấy giá thị trường / giá thực tế
  2. So sánh với giá ghi sổ
  3. Nếu giá thị trường < giá ghi sổ: Lập dự phòng
  4. Ghi nhận: Nợ 632 / Có 2294
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 3] → Giá tăng: Không ghi nhận (nguyên tắc thận trọng)
  - [Bước 3] → Đã lập dự phòng năm trước: Điều chỉnh
- **Điều kiện hậu kiểm (Postconditions):** Giá trị kho phản ánh thực tế
- **Định khoản:** Nợ 632 / Có 2294

---

### 📌 I06 — Trích lập/hoàn nhập dự phòng giảm giá hàng tồn kho
- **Tác nhân (Actors):** Kế toán
- **Mục tiêu:** Trích lập dự phòng theo nguyên tắc thận trọng
- **Điều kiện tiên quyết (Preconditions):** Cuối năm tài chính
- **Luồng chính (Main Flow):**
  1. Xác định mặt hàng cần lập dự phòng
  2. Tính chênh lệch giá (thị trường - ghi sổ)
  3. Trích lập: Nợ 632 / Có 2294
  4. Nếu giá phục hồi: Hoàn nhập ngược lại
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 3] → Giá tăng trở lại: Hoàn nhập dự phòng
  - [Bước 3] → Hàng đã bán hết: Không cần trích
- **Điều kiện hậu kiểm (Postconditions):** 2294 phản ánh dự phòng thực tế
- **Định khoản:** Trích: Nợ 632 / Có 2294 | Hoàn nhập: Nợ 2294 / Có 632

---

### 📌 I07 — Xử lý hàng tồn kho hư hỏng, hết hạn
- **Tác nhân (Actors):** Kế toán, Thủ kho, Ban giám đốc
- **Mục tiêu:** Xử lý hàng hóa không còn giá trị sử dụng
- **Điều kiện tiên quyết (Preconditions):** Có biên bản kiểm kê, quyết định xử lý
- **Luồng chính (Main Flow):**
  1. Lập biên bản kiểm kê xác nhận hư hỏng
  2. Xin ý kiến Ban giám đốc xử lý
  3. Ghi nhận: Nợ 811 / Có 156 (giá gốc)
  4. Khấu trừ VAT (nếu đã khấu trừ): Nợ 1331 / Có 156
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 2] → Có bảo hiểm: Thu bồi thường
  - [Bước 2] → Người gây ra phải bồi thường: Thu tiền
- **Điều kiện hậu kiểm (Postconditions):** Hàng hư hỏng được xóa khỏi sổ
- **Định khoản:** Nợ 811 + Nợ 1331 (nếu có) / Có 156

---

*Last Updated: April 2026*
*Source: ketoanthienung.net, TT99/2025*