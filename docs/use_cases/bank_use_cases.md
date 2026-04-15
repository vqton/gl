# BANK USE CASES (B01-B08)
*Based on: TT99/2025, Circular on Bank Transactions*

---

### 📌 B01 — Đối chiếu sao kê ngân hàng
- **Tác nhân (Actors):** Kế toán, Thủ quỹ
- **Mục tiêu:** Đối chiếu số dư tài khoản ngân hàng giữa sổ sách DN và sao kê ngân hàng
- **Điều kiện tiên quyết (Preconditions):** Có sao kê ngân hàng cuối kỳ, số dư TK 112 tại sổ sách
- **Luồng chính (Main Flow):**
  1. Kế toán tải/tải sao kê ngân hàng
  2. Đối chiếu từng giao dịch trong kỳ
  3. Phát hiện chênh lệch (nếu có)
  4. Điều chỉnh hoặc báo cáo
  5. Xác nhận số dư cuối kỳ
- **Luồng thay thế/Ngoại lệ (Alternate/Frames):**
  - [Bước 3] → Chênh lệch do chưa ghi nhận: Bổ sung bút toán
  - [Bước 3] → Chênh lệch do phí ngân hàng: Ghi nhận vào chi phí
  - [Bước 3] → Gian lận: Báo cáo BTC điều tra
- **Điều kiện hậu kiểm (Postconditions):** Số dư TK 112 khớp với sao kê
- **Định khoản:** Điều chỉnh: Nợ/Có 112 / Nợ/Có 638,811

---

### 📌 B02 — Chuyển khoản thanh toán cho NCC
- **Tác nhân (Actors):** Kế toán, Ngân hàng
- **Mục tiêu:** Chuyển khoản thanh toán cho nhà cung cấp qua ngân hàng
- **Điều kiện tiên quyết (Preconditions):** Có hóa đơn mua hàng, đủ điều kiện thanh toán, số dư TK 112 > 0
- **Luồng chính (Main Flow):**
  1. Kế toán lập ủy nhiệm chi (payment order)
  2. Ký duyệt theo phân quyền
  3. Ngân hàng xử lý giao dịch
  4. Ghi nhận bút toán: Nợ 331 / Có 112
- **Luồng thay thế/Ngoại lệ (Alternate/Frames):**
  - [Bước 3] → TK ngân hàng không đủ số dư: Báo lỗi, yêu cầu nạp thêm
  - [Bước 3] → NCC không đúng tên TK: Dừng giao dịch, xác minh
- **Điều kiện hậu kiểm (Postconditions):** Số dư TK 112 giảm, công nợ NCC giảm
- **Định khoản:** Nợ 331 / Có 112

---

### 📌 B03 — Nhận giải ngân từ ngân hàng (vay ngắn hạn)
- **Tác nhân (Actors):** Kế toán, Ngân hàng, Bộ phận tài chính
- **Mục tiêu:** Nhận tiền vay ngắn hạn được giải ngân vào tài khoản
- **Điều kiện tiên quyết (Preconditions):** Có hợp đồng tín dụng, hồ sơ vay đã được duyệt
- **Luồng chính (Main Flow):**
  1. Ngân hàng giải ngân (giải ngân vào TK DN)
  2. Kế toán nhận giấy báo có
  3. Kiểm tra số tiền và lãi suất
  4. Ghi nhận: Nợ 112 / Có 311
- **Luồng thay thế/Ngoại lệ (Alternate/Frames):**
  - [Bước 3] → Lãi suất trừ trước (discount): Nợ 112, Nợ 635 (lãi vay trả trước) / Có 311
  - [Bước 3] → Phí giải ngân: Ghi nhận vào chi phí
- **Điều kiện hậu kiểm (Postconditions):** TK 112 tăng, nợ vay ngắn hạn tăng
- **Định khoản:** Nợ 112 / Có 311 (vay ngắn hạn)

---

### 📌 B04 — Trả nợ vay ngân hàng (gốc + lãi)
- **Tác nhân (Actors):** Kế toán, Ngân hàng
- **Mục tiêu:** Thanh toán nợ gốc và lãi vay theo hợp đồng
- **Điều kiện tiên quyết (Preconditions):** Đến hạn trả nợ, số dư TK 112 > 0
- **Luồng chính (Main Flow):**
  1. Kế toán lập ủy nhiệm chi trả nợ
  2. Trích tài khoản thanh toán
  3. Ngân hàng xác nhận đã trả
  4. Ghi nhận: Nợ 311 (gốc), Nợ 635 (lãi) / Có 112
- **Luồng thay thế/Ngoại lệ (Alternate/Frames):**
  - [Bước 2] → Trả trước hạn: Tính lãi phạt (nếu có)
  - [Bước 2] → Không đủ số dư: Báo lỗi
- **Điều kiện hậu kiểm (Postconditions):** Nợ vay giảm, chi phí lãi được ghi nhận
- **Định khoản:** Nợ 311 + 635 / Có 112

---

### 📌 B05 — Hạch toán phí ngân hàng
- **Tác nhân (Actors):** Kế toán, Ngân hàng
- **Mục tiêu:** Ghi nhận phí dịch vụ ngân hàng (phí SMS, phí quản lý tài khoản, phí chuyển tiền)
- **Điều kiện tiên quyết (Preconditions):** Ngân hàng thông báo phí hoặc trừ vào TK
- **Luồng chính (Main Flow):**
  1. Nhận thông báo phí ngân hàng
  2. Kiểm tra và xác nhận
  3. Ghi nhận: Nợ 641,642 (chi phí) / Có 112
- **Luồng thay thế/Ngoại lệ (Alternate/Frames):**
  - [Bước 1] → Phí có VAT: Kê khai vào TK 1331
  - [Bước 1] → Phí trừ trực tiếp: Tự động ghi nhận
- **Điều kiện hậu kiểm (Postconditions):** Chi phí ngân hàng được ghi nhận, TK 112 giảm
- **Định khoản:** Nợ 641,642 / Có 112

---

### 📌 B06 — Hạch toán lãi tiền gửi ngân hàng
- **Tác nhân (Actors):** Kế toán, Ngân hàng
- **Mục tiêu:** Ghi nhận lãi suất tiền gửi ngân hàng được hưởng
- **Điều kiện tiên quyết (Preconditions):** Có số dư tiền gửi, ngân hàng tính lãi
- **Luồng chính (Main Flow):**
  1. Nhận thông báo lãi (interest advice)
  2. Kiểm tra lãi suất và số ngày
  3. Ghi nhận: Nợ 112 / Có 515 (lãi tiền gửi)
- **Luồng thay thế/Ngoại lệ (Alternate/Frames):**
  - [Bước 1] → Lãi nhập gốc (compound): Cộng vào TK tiền gửi
  - [Bước 1] → Khấu thuế TNCN (10%): Ghi nhận sau khi trừ thuế
- **Điều kiện hậu kiểm (Postconditions):** Doanh thu tài chính tăng
- **Định khoản:** Nợ 112 / Có 515

---

### 📌 B07 — Mở LC (Letter of Credit) / Thư tín dụng
- **Tác nhân (Actors):** Kế toán, Ngân hàng, Nhà cung cấp
- **Mục tiêu:** Mở LC để thanh toán nhập khẩu
- **Điều kiện tiên quyết (Preconditions):** Có hợp đồng nhập khẩu, hồ sơ xin mở LC
- **Luồng chính (Main Flow):**
  1. DN nộp hồ sơ xin mở LC
  2. Ngân hàng duyệt và phát hành LC
  3. DN đặt cọc (nếu có)
  4. Ghi nhận: Nợ 144 (ký quỹ) / Có 112
- **Luồng thay thế/Ngoại lệ (Alternate/Frames):**
  - [Bước 1] → Không đủ tài sản cấp: Từ chối
  - [Bước 2] → LC trả ngay (sight): Chờ chứng từ xuất khẩu
- **Điều kiện hậu kiểm (Postconditions):** TK ký quỹ tăng (nếu có cọc)
- **Định khoản:** Nợ 144 / Có 112

---

### 📌 B08 — Đối chiếu ngoại hối (Foreign Exchange)
- **Tác nhân (Actors):** Kế toán, Ngân hàng
- **Mục tiêu:** Đánh giá lại các khoản mục có gốc ngoại tệ theo tỷ giá cuối kỳ
- **Điều kiện tiên quyết (Preconditions):** Cuối kỳ kế toán, có số dư ngoại tệ tại ngân hàng
- **Luồng chính (Main Flow):**
  1. Lấy tỷ giá báo cáo cuối kỳ
  2. Tính chênh lệch tỷ giá
  3. Nếu lãi: Nợ 112 / Có 413
  4. Nếu lỗ: Nợ 635 / Có 112
- **Luồng thay thế/Ngoại lệ (Alternate/Frames):**
  - [Bước 2] → Lãi tỷ giá: Ghi vào 515 (doanh thu HO)
  - [Bước 2] → Lỗ tỷ giá: Ghi vào 635 (chi phí HO)
- **Điều kiện hậu kiểm (Postconditions):** TK 112, 413, 635 được đánh giá theo tỷ giá mới
- **Định khoản:** Lãi: Nợ 112 / Có 413 | Lỗ: Nợ 635 / Có 112

---

*Last Updated: April 2026*
*Source: aztax.com.vn, tamkhoatech.vn*