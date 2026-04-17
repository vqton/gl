<!--
📁 TÊN FILE ĐỀ XUẤT: usecases_so_quy_tien_mat_tt99_20260416.md
🕐 Ngày trích xuất: 2026-04-16
🔗 URL gốc: https://ketoanthienung.net/mau-so-quy-tien-mat-theo-thong-tu-99.htm
📦 Độ sâu duyệt: 2 cấp (Cha → Con)
-->

# 📋 Use Cases Tổng hợp (Độ sâu: 2 cấp)

## 🗂️ Mục lục nguồn đã duyệt

| Cấp | URL | Trạng thái | Ghi chú |
|-----|-----|------------|---------|
| 1 | https://ketoanthienung.net/mau-so-quy-tien-mat-theo-thong-tu-99.htm | ✅ | Trang tổng quan mẫu sổ quỹ tiền mặt |
| 2 | https://ketoanthienung.net/mau-so-tien-gui-ngan-hang-khong-ky-han-theo-thong-tu-99.htm | ✅ | Sổ tiền gửi ngân hàng không kỳ hạn |
| 2 | https://ketoanthienung.net/mau-bang-can-doi-so-phat-sinh-s06-dn-theo-thong-tu-99.htm | ✅ | Bảng cân đối số phát sinh |
| 2 | https://ketoanthienung.net/mau-so-cai-dung-cho-hinh-thuc-chung-tu-ghi-so-theo-tt-99.htm | ✅ | Sổ Cái dùng cho hình thức Chứng từ ghi sổ |
| 2 | https://ketoanthienung.net/mau-so-nhat-ky-so-cai-theo-thong-tu-99.htm | ✅ | Sổ Nhật ký - Sổ Cái |
| 2 | https://ketoanthienung.net/mau-so-nhat-ky-chung-theo-thong-tu-99-va-cach-lap.htm | ✅ | Sổ Nhật ký chung |

---

## 📦 Nhóm Use Case

### 📌 [UC-QTM-001] Ghi sổ quỹ tiền mặt (Sổ quỹ tiền mặt)
🔗 Nguồn: [Cấp 1] | URL: https://ketoanthienung.net/mau-so-quy-tien-mat-theo-thong-tu-99.htm

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Thủ quỹ / `Secondary:` Kế toán trưởng (kiểm tra cuối ngày), Giám đốc (phê duyệt) |
| **Mục tiêu** | Phản ánh tình hình thu, chi tồn quỹ tiền mặt bằng tiền Việt Nam |
| **Tiên quyết** | Đã mở sổ S07-DN theo mẫu TT99/2025; có Phiếu thu, Phiếu chi làm căn cứ |
| **Kích hoạt** | Nhận được Phiếu thu (tiền vào) hoặc Phiếu chi (tiền ra) |

#### 🔄 Luồng chính (Main Success Scenario)

| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Thủ quỹ/Kế toán | Kiểm tra Phiếu thu/Phiếu chi hợp lệ |
| 2 | | Ghi ngày tháng ghi sổ vào cột A |
| 3 | | Ghi ngày tháng chứng từ vào cột B |
| 4 | | Ghi số hiệu Phiếu thu/Phiếu chi vào cột C, D |
| 5 | | Ghi nội dung nghiệp vụ vào cột E |
| 6 | | Ghi số tiền nhập vào cột 1 (Thu) |
| 7 | | Ghi số tiền xuất vào cột 2 (Chi) |
| 8 | | Tính và ghi số tồn vào cột 3 |
| 9 | Kế toán trưởng | Kiểm tra và ký xác nhận cuối ngày |

#### ⚠️ Luồng thay thế/Ngoại lệ

| Bước gốc | Điều kiện kích hoạt | Hành động xử lý |
|----------|-------------------|------------------|
| [1] | Phiếu không hợp lệ | Từ chối, yêu cầu lập lại chứng từ |
| [8] | Số tiền mặt trong két chênh lệch | Báo cáo chênh lệch theo Quy chế, điều tra nguyên nhân |
| [9] | Sai số trong phạm vi cho phép | Ghi nhận theo Quy chế tài chính |

✅ **Hậu kiểm:** Số tồn quỹ trên sổ khớp với số tiền mặt thực tế trong két (± sai số cho phép theo Quy chế nội bộ)
🔀 *Ghi chú:* Sổ này dùng cho thủ quỹ; kế toán mở sổ song song "Sổ kế toán chi tiết quỹ tiền mặt" S07a-DN

---

### 📌 [UC-QTM-002] Ghi sổ kế toán chi tiết quỹ tiền mặt
🔗 Nguồn: [Cấp 1] | URL: https://ketoanthienung.net/mau-so-quy-tien-mat-theo-thong-tu-99.htm

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán tiền mặt / `Secondary:` Kế toán trưởng (kiểm tra cuối ngày) |
| **Mục tiêu** | Theo dõi chi tiết tiền mặt với tài khoản đối ứng |
| **Tiên quyết** | Đã mở sổ S07a-DN; có Phiếu thu/Phiếu chi |
| **Kích hoạt** | Cùng thời điểm ghi sổ S07-DN |

#### 🔄 Luồng chính (Main Success Scenario)

| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Kế toán | Ghi các cột như S07-DN |
| 2 | | Ghi thêm cột F - Tài khoản đối ứng (TK Nợ, TK Có) |
| 3 | | Tính số tồn đầu kỳ, phát sinh trong kỳ, tồn cuối kỳ |

✅ **Hậu kiểm:** Số liệu khớp với Sổ quỹ tiền mặt S07-DN

---

### 📌 [UC-TGN-001] Ghi sổ tiền gửi ngân hàng không kỳ hạn
🔗 Nguồn: [Cấp 2] | URL: https://ketoanthienung.net/mau-so-tien-gui-ngan-hang-khong-ky-han-theo-thong-tu-99.htm

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán ngân hàng / `Secondary:` Kế toán trưởng (kiểm tra cuối tháng), Giám đốc (phê duyệt) |
| **Mục tiêu** | Theo dõi chi tiết tiền gửi tại Ngân hàng theo từng tài khoản |
| **Tiên quyết** | Đã mở sổ S08-DN; ghi rõ nơi mở tài khoản và số hiệu tài khoản |
| **Kích hoạt** | Nhận được Giấy báo Nợ, Giấy báo Có từ Ngân hàng |

#### 🔄 Luồng chính (Main Success Scenario)

| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Kế toán | Ghi số dư đầu kỳ vào cột 8 |
| 2 | | Ghi ngày tháng ghi sổ (cột A) |
| 3 | | Ghi số hiệu, ngày tháng chứng từ (cột B, C) |
| 4 | | Ghi nội dung (cột D) |
| 5 | | Ghi số hiệu TK đối ứng (cột E) |
| 6 | | Ghi số tiền gửi vào (cột 1 - Thu) |
| 7 | | Ghi số tiền rút ra (cột 2 - Chi) |
| 8 | | Tính số còn lại (cột 3) |
| 9 | Cuối tháng | Cộng phát sinh, đối chiếu với số dư Ngân hàng |
| 10 | | Xử lý chênh lệch tỷ giá (nếu có giao dịch ngoại tệ) |

#### ⚠️ Luồng thay thế/Ngoại lệ

| Bước gốc | Điều kiện kích hoạt | Hành động xử lý |
|----------|-------------------|------------------|
| [10] | Giao dịch ngoại tệ | Đánh giá lại theo tỷ giá cuối kỳ, phản ánh chênh lệch tỷ giá |
| [9] | Số dư Ngân hàng khác sổ | Yêu cầu Ngân hàng xác nhận, điều chỉnh |

✅ **Hậu kiểm:** Số dư trên sổ khớp với số dư tại Ngân hàng (± ngoại tệ quy đổi)

---

### 📌 [UC-CDPS-001] Lập bảng cân đối số phát sinh
🔗 Nguồn: [Cấp 2] | URL: https://ketoanthienung.net/mau-bang-can-doi-so-phat-sinh-s06-dn-theo-thong-tu-99.htm

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán tổng hợp / `Secondary:` Kế toán trưởng (kiểm tra số liệu), Giám đốc (phê duyệt BCTC) |
| **Mục tiêu** | Phản ánh tổng quát tình hình tăng giảm và hiện có về tài sản, nguồn vốn trong kỳ |
| **Tiên quyết** | Hoàn thành ghi sổ kế toán chi tiết và tổng hợp; đối chiếu số liệu |
| **Kích hoạt** | Cuối kỳ báo cáo (tháng/quý) |

#### 🔄 Luồng chính (Main Success Scenario)

| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Kế toán | Đối chiếu Sổ Cái ↔ Bảng tổng hợp chi tiết |
| 2 | | Lấy số dư đầu tháng từ Sổ Cái hoặc kỳ trước (cột 1, 2) |
| 3 | | Lấy số phát sinh trong tháng từ Sổ Cái (cột 3, 4) |
| 4 | | Tính số dư cuối tháng (cột 5, 6) |
| 5 | | Tổng cộng các cột |
| 6 | | Kiểm tra cân đối: Tổng Nợ = Tổng Có |
| 7 | Kế toán trưởng | Xác nhận số liệu trước khi in |

#### ⚠️ Luồng thay thế/Ngoại lệ

| Bước gốc | Điều kiện kích hoạt | Hành động xử lý |
|----------|-------------------|------------------|
| [5] | Tổng Nợ ≠ Tổng Có | Tìm sai sót, điều chỉnh trước khi lập Báo cáo tài chính |

✅ **Hậu kiểm:** Bảng cân đối số phát sinh đảm bảo: Tổng Nợ = Tổng Có (cả 6 cột)

---

### 📌 [UC-SC-001] Ghi sổ Cái (hình thức Chứng từ ghi sổ)
🔗 Nguồn: [Cấp 2] | URL: https://ketoanthienung.net/mau-so-cai-dung-cho-hinh-thuc-chung-tu-ghi-so-theo-tt-99.htm

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán / `Secondary:` Kế toán trưởng (kiểm tra cuối tháng) |
| **Mục tiêu** | Ghi các nghiệp vụ kinh tế phát sinh theo tài khoản kế toán |
| **Tiên quyết** | Đã mở sổ Cái cho từng tài khoản (S02c1-DN hoặc S02c2-DN) |
| **Kích hoạt** | Nhận chứng từ kế toán đã qua kiểm tra |

#### 🔄 Luồng chính (Main Success Scenario)

| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Kế toán | Ghi ngày tháng ghi sổ (cột A) |
| 2 | | Ghi số hiệu, ngày tháng chứng từ (cột B, C) |
| 3 | | Ghi nội dung nghiệp vụ (cột D) |
| 4 | | Ghi số hiệu TK đối ứng (cột E) |
| 5 | | Ghi số tiền Nợ (cột 1) |
| 6 | | Ghi số tiền Có (cột 2) |
| 7 | | Tính số dư cuối tháng |
| 8 | Cuối tháng | Cộng phát sinh, tính dư, cộng luỹ kế từ đầu quý |

✅ **Hậu kiểm:** Số liệu Sổ Cái dùng để lập Bảng cân đối số phát sinh và Báo cáo tài chính

---

### 📌 [UC-NKSC-001] Ghi sổ Nhật ký - Sổ Cái (hình thức Nhật ký - Sổ Cái)
🔗 Nguồn: [Cấp 2] | URL: https://ketoanthienung.net/mau-so-nhat-ky-so-cai-theo-thong-tu-99.htm

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán / `Secondary:` Kế toán trưởng (kiểm tra cuối tháng), Giám đốc (phê duyệt) |
| **Mục tiêu** | Phản ánh tất cả nghiệp vụ kinh tế phát sinh theo trình tự thời gian và hệ thống theo tài khoản |
| **Tiên quyết** | Đã mở sổ S01-DN |
| **Kích hoạt** | Nhận chứng từ kế toán hợp lệ |

#### 🔄 Luồng chính (Main Success Scenario)

| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Kế toán | Kiểm tra tính hợp lệ của chứng từ |
| 2 | | Xác định TK ghi Nợ, TK ghi Có |
| 3 | | Ghi vào phần Nhật ký: ngày tháng, số hiệu chứng từ, nội dung, số tiền |
| 4 | | Đồng thời ghi vào phần Sổ Cái: cột Nợ/Có của các TK liên quan |
| 5 | | Ghi số thứ tự dòng (cột H) |
| 6 | | Ghi số hiệu TK đối ứng (cột F, G) |
| 7 | Cuối tháng | Cộng phát sinh, tính số dư, cộng luỹ kế từ đầu quý |

✅ **Hậu kiểm:** Số liệu trên S01-DN dùng trực tiếp để lập Báo cáo tài chính

---

### 📌 [UC-NKC-001] Ghi sổ Nhật ký chung
🔗 Nguồn: [Cấp 2] | URL: https://ketoanthienung.net/mau-so-nhat-ky-chung-theo-thong-tu-99-va-cach-lap.htm

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán / `Secondary:` Kế toán trưởng (kiểm tra cuối tháng), Giám đốc (phê duyệt) |
| **Mục tiêu** | Ghi chép nghiệp vụ kinh tế, tài chính phát sinh theo trình tự thời gian và quan hệ đối ứng tài khoản |
| **Tiên quyết** | Đã mở sổ S03a-DN |
| **Kích hoạt** | Nhận chứng từ kế toán |

#### 🔄 Luồng chính (Main Success Scenario)

| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Kế toán | Ghi ngày tháng ghi sổ (cột A) |
| 2 | | Ghi số hiệu, ngày tháng chứng từ (cột B, C) |
| 3 | | Ghi nội dung nghiệp vụ (cột D) |
| 4 | | Đánh dấu đã ghi Sổ Cái (cột E) |
| 5 | | Ghi số thứ tự dòng (cột G) |
| 6 | | Ghi số hiệu TK đối ứng: TK Nợ trước, TK Có sau (cột H) |
| 7 | | Ghi số tiền phát sinh Nợ (cột 1) |
| 8 | | Ghi số tiền phát sinh Có (cột 2) |
| 9 | | Cộng chuyển trang sang trang sau |

#### ⚠️ Luồng thay thế/Ngoại lệ

| Bước gốc | Điều kiện kích hoạt | Hành động xử lý |
|----------|-------------------|------------------|
| [1] | Nghiệp vụ phát sinh nhiều | Có thể mở Sổ Nhật ký đặc biệt (thu tiền, chi tiền, mua hàng, bán hàng) |

✅ **Hậu kiểm:** Số liệu Sổ Nhật ký chung dùng để ghi Sổ Cái

🔀 *Ghi chú:* Doanh nghiệp được phép sửa đổi mẫu sổ so với biểu mẫu hướng dẫn, nhưng phải đảm bảo tuân thủ Điều 24 Luật Kế toán

---

### 📌 [UC-MS-001] Mở sổ kế toán đầu năm
🔗 Nguồn: [Cấp 1] | URL: https://ketoanthienung.net/mo-so-ghi-so-va-khoa-so-ke-toan-theo-thong-tu-99.htm

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán / `Secondary:` Kế toán trưởng (kiểm tra), Giám đốc (phê duyệt) |
| **Mục tiêu** | Chuẩn bị sổ kế toán để ghi chép nghiệp vụ trong năm tài chính |
| **Tiên quyết** | Đã có quyết định thành lập đơn vị; mở tài khoản kế toán |
| **Kích hoạt** | Đầu năm tài chính (01/01) |

#### 🔄 Luồng chính (Main Success Scenario)

| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Kế toán | Mua sổ, đánh số trang từ 01 đến ... |
| 2 | | Ghi thông tin đơn vị: tên, địa chỉ, mã số thuế |
| 3 | | Ghi năm tài chính |
| 4 | | Ghi số dư đầu năm từ sổ kỳ trước |
| 5 | | Ghi ngày mở sổ |
| 6 | Kế toán trưởng | Kiểm tra, ký xác nhận |
| 7 | Giám đốc | Ký, đóng dấu |

✅ **Hậu kiểm:** Sổ sẵn sàng để ghi nghiệp vụ phát sinh

---

### 📌 [UC-KS-001] Khóa sổ cuối tháng
🔗 Nguồn: [Cấp 1] | URL: https://ketoanthienung.net/mo-so-ghi-so-va-khoa-so-ke-toan-theo-thong-tu-99.htm

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán / `Secondary:` Kế toán trưởng (kiểm tra) |
| **Mục tiêu** | Tổng hợp số phát sinh, tính số dư cuối kỳ, đảm bảo cân đối |
| **Tiên quyết** | Hoàn thành ghi chép tất cả chứng từ trong tháng |
| **Kích hoạt** | Cuối tháng (trước ngày 28-30/31) |

#### 🔄 Luồng chính (Main Success Scenario)

| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Kế toán | Kiểm tra tính đầy đủ của chứng từ |
| 2 | | Tổng hợp số phát sinh Nợ, Có |
| 3 | | Tính số dư cuối tháng |
| 4 | | Cộng luỹ kế từ đầu quý |
| 5 | | Kiểm tra cân đối: Tổng Nợ = Tổng Có |
| 6 | Kế toán trưởng | Xác nhận số liệu, ký |

#### ⚠️ Luồng thay thế/Ngoại lệ

| Bước gốc | Điều kiện kích hoạt | Hành động xử lý |
|----------|-------------------|------------------|
| [5] | Không cân đối | Tìm sai sót, điều chỉnh trước khi khóa sổ |

✅ **Hậu kiểm:** Sổ được khóa, số liệu chính xác, sẵn sàng lập BCTC

---

### 📌 [UC-DC-001] Đối chiếu Sổ Cái với Bảng cân đối số phát sinh
🔗 Nguồn: [Cấp 1] | URL: https://ketoanthienung.net/mau-so-cai-dung-cho-hinh-thuc-chung-tu-ghi-so-theo-tt-99.htm

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán tổng hợp / `Secondary:` Kế toán trưởng (xác nhận) |
| **Mục tiêu** | Đảm bảo số liệu trên Sổ Cái khớp với Bảng CĐPS |
| **Tiên quyết** | Hoàn thành ghi Sổ Cái và Bảng CĐPS |
| **Kích hoạt** | Trước khi lập Báo cáo tài chính |

#### 🔄 Luồng chính (Main Success Scenario)

| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Kế toán | Tổng cộng Sổ Cái từng tài khoản |
| 2 | | So sánh với Bảng CĐPS |
| 3 | | Nếu chênh lệch → tìm nguyên nhân |
| 4 | | Điều chỉnh (nếu có) |
| 5 | Kế toán trưởng | Xác nhận kết quả đối chiếu |
| 6 | | Ký vào Bảng CĐPS |

✅ **Hậu kiểm:** Số liệu Sổ Cái = Bảng CĐPS = Báo cáo tài chính

---

## ⚠️ LƯU Ý & MÂU THUẪN (Nếu có)

- Các mẫu sổ kế toán tại Phụ lục III ban hành kèm theo TT99/2025 là mẫu tham khảo. Doanh nghiệp được phép sửa đổi nhưng phải đảm bảo phản ánh đầy đủ, kịp thời, trung thực, minh bạch.
- Khi sửa đổi mẫu sổ, doanh nghiệp phải ban hành Quy chế hạch toán kế toán làm cơ sở thực hiện.
- Sổ Nhật ký chung và các sổ Nhật ký đặc biệt (thu tiền, chi tiền, mua hàng, bán hàng) là một hệ thống - không ghi trùng lặp.

🛑 QUY TẮC KIỂM TRA TRƯỚC KHI XUẤT:
☐ Đã duyệt đúng tối đa 2 cấp (Cha → Con)?
☐ Mỗi UC đều có ID duy nhất và gắn nguồn URL rõ ràng?
☐ Đã loại bỏ trùng lặp, ưu tiên chi tiết từ Cấp 2?
☐ Không có nội dung bịa đặt/hallucination?
☐ Định dạng Markdown chuẩn, sẵn sàng lưu file?