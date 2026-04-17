<!--
📁 TÊN FILE ĐỀ XUẤT: usecases_bao_cao_tai_chinh_tt99_20260416.md
🕐 Ngày trích xuất: 2026-04-16
🔗 URL gốc: https://ketoanthienung.net/bao-cao-tai-chinh-theo-thong-tu-99.htm
📦 Độ sâu duyệt: 2 cấp (Cha → Con)
-->

# 📋 Use Cases Tổng hợp (Độ sâu: 2 cấp)

## 🗂️ Mục lục nguồn đã duyệt

| Cấp | URL | Trạng thái | Ghi chú |
|-----|-----|------------|---------|
| 1 | https://ketoanthienung.net/bao-cao-tai-chinh-theo-thong-tu-99.htm | ✅ | Trang tổng quan Báo cáo tài chính |
| 2 | https://ketoanthienung.net/bao-cao-tai-chinh-gom-nhung-gi-mau-bieu-bang-nao.htm | ✅ | BCTC gồm những gì? Mẫu biểu nào? |
| 2 | https://ketoanthienung.net/cach-lap-bao-cao-tinh-hinh-tai-chinh-theo-thong-tu-99.htm | ✅ | Cách lập Báo cáo tình hình tài chính |
| 2 | https://ketoanthienung.net/cach-lap-bao-cao-ket-qua-hoat-dong-kinh-doanh-theo-thong-tu-99.htm | ✅ | Cách lập Báo cáo kết quả HĐKD |
| 2 | https://ketoanthienung.net/cach-lap-bao-cao-luu-chuyen-tien-te-theo-thong-tu-99.htm | ✅ | Cách lập Báo cáo lưu chuyển tiền tệ |
| 2 | https://ketoanthienung.net/cach-lap-thuyet-minh-bctc-theo-thong-tu-99.htm | ✅ | Cách lập Thuyết minh BCTC |

---

## 📦 Nhóm Use Case

### 📌 [UC-BCTC-001] Lập Báo cáo tình hình tài chính (Balance Sheet)
🔗 Nguồn: [Cấp 2] | URL: https://ketoanthienung.net/cach-lap-bao-cao-tinh-hinh-tai-chinh-theo-thong-tu-99.htm

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán tổng hợp / `Secondary:` Kế toán trưởng (kiểm tra số liệu), Giám đốc (phê duyệt), Kiểm toán (xác nhận) |
| **Mục tiêu** | Phản ánh tổng quát toàn bộ giá trị tài sản hiện có và nguồn hình thành tài sản tại thời điểm nhất định |
| **Tiên quyết** | Hoàn thành khóa sổ kế toán cuối kỳ; đối chiếu sổ Cái ↔ Bảng tổng hợp chi tiết |
| **Kích hoạt** | Cuối kỳ kế toán (tháng/quý/năm) |

#### 🔄 Luồng chính (Main Success Scenario)

| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Kế toán | Lấy số dư cuối kỳ từ Sổ Cái |
| 2 | | Tổng hợp Tài sản ngắn hạn (Mã 100 = 110+120+130+140+150+160) |
| 3 | | Tổng hợp Tài sản dài hạn (Mã 200 = 210+220+230+240+250+260+270) |
| 4 | | Tổng hợp Nợ phải trả ngắn hạn (Mã 300) |
| 5 | | Tổng hợp Nợ phải trả dài hạn (Mã 400) |
| 6 | | Tổng hợp Vốn chủ sở hữu (Mã 500) |
| 7 | | Kiểm tra cân đối: Tổng Tài sản = Tổng Nguồn vốn |
| 8 | Kế toán trưởng | Xác nhận số liệu trước khi in |
| 9 | Giám đốc | Phê duyệt Báo cáo |

#### ⚠️ Luồng thay thế/Ngoại lệ

| Bước gốc | Điều kiện kích hoạt | Hành động xử lý |
|----------|-------------------|------------------|
| [7] | Không cân bằng | Tìm sai sót trong Sổ Cái hoặc Bảng CĐPS |
| [9] | Có điều chỉnh | Lập Báo cáo điều chỉnh hồi tố nếu phát hiện sai sót trọng yếu |

✅ **Hậu kiểm:** Bảng cân đối kế toán: Tổng Tài sản = Tổng Nguồn vốn

---

### 📌 [UC-BCTC-002] Lập Báo cáo kết quả hoạt động kinh doanh
🔗 Nguồn: [Cấp 2] | URL: https://ketoanthienung.net/cach-lap-bao-cao-ket-qua-hoat-dong-kinh-doanh-theo-thong-tu-99.htm

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán tổng hợp / `Secondary:` Kế toán trưởng (kiểm tra), Giám đốc (phê duyệt) |
| **Mục tiêu** | Phản ánh tình hình và kết quả hoạt động kinh doanh trong kỳ (HĐKD chính, hoạt động tài chính, hoạt động khác) |
| **Tiên quyết** | Hoàn thành ghi sổ kế toán các TK loại 5-9 |
| **Kích hoạt** | Cuối kỳ kế toán |

#### 🔄 Luồng chính (Main Success Scenario)

| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Kế toán | Lấy số liệu Doanh thu bán hàng (TK 511) |
| 2 | | Lấy số liệu Giảm trừ doanh thu (TK 521) |
| 3 | | Tính Doanh thu thuần = 511 - 521 |
| 4 | | Lấy số liệu Giá vốn hàng bán (TK 632) |
| 5 | | Tính Lợi nhuận gộp = DT thuần - Giá vốn |
| 6 | | Tính Lợi nhuận thuần = Lợi nhuận gộp + DT tài chính - CP tài chính - CP bán hàng - CP quản lý |
| 7 | | Tính Lợi nhuận kế toán trước thuế = Lợi nhuận thuần + Thu nhập khác - Chi phí khác |
| 8 | | Tính Lợi nhuận sau thuế = Lợi nhuận trước thuế - Chi phí thuế TNDN |
| 9 | Kế toán trưởng | Kiểm tra và xác nhận |

✅ **Hậu kiểm:** Báo cáo KQHĐKD hoàn chỉnh với các chỉ tiêu: Doanh thu, Giá vốn, Lợi nhuận gộp, Lợi nhuận thuần, Lợi nhuận trước thuế, Lợi nhuận sau thuế

---

### 📌 [UC-BCTC-003] Lập Báo cáo lưu chuyển tiền tệ
🔗 Nguồn: [Cấp 2] | URL: https://ketoanthienung.net/cach-lap-bao-cao-luu-chuyen-tien-te-theo-thong-tu-99.htm

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán tổng hợp / `Secondary:` Kế toán trưởng (kiểm tra), Giám đốc (phê duyệt) |
| **Mục tiêu** | Phản ánh dòng tiền vào/ra từ HĐKD, hoạt động đầu tư, hoạt động tài chính |
| **Tiên quyết** | Hoàn thành Báo cáo KQHĐKD và Báo cáo tình hình tài chính |
| **Kích hoạt** | Cuối kỳ kế toán |

#### 🔄 Luồng chính (Main Success Scenario)

| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Kế toán | Chọn phương pháp trực tiếp hoặc gián tiếp |
| 2 | | Lập Lưu chuyển từ HĐKD (01-07): Thu từ bán hàng, chi cho NCC, chi cho NLĐ, chi phí đi vay, thuế TNDN, thu/chi khác |
| 3 | | Lập Lưu chuyển từ hoạt động đầu tư: Mua TSCĐ, mua chứng khoán, tiền chi ra |
| 4 | | Lập Lưu chuyển từ hoạt động tài chính: Tiền vay, cổ phiếu phát hành, cổ tức trả |
| 5 | | Tính Lưu chuyển tiền thuần trong kỳ |
| 6 | | Kiểm tra chênh lệch quy đổi ngoại tệ |

#### ⚠️ Luồng thay thế/Ngoại lệ

| Bước gốc | Điều kiện kích hoạt | Hành động xử lý |
|----------|-------------------|------------------|
| [1] | DN áp dụng gián tiếp | Điều chỉnh từ Lợi nhuận trước thuế + các khoản mục không bằng tiền |

✅ **Hậu kiểm:** Lưu chuyển tiền thuần = Tiền cuối kỳ - Tiền đầu kỳ

---

### 📌 [UC-BCTC-004] Lập Bản thuyết minh Báo cáo tài chính
🔗 Nguồn: [Cấp 2] | URL: https://ketoanthienung.net/cach-lap-thuyet-minh-bctc-theo-thong-tu-99.htm

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán tổng họa / `Secondary:` Kế toán trưởng (kiểm tra), Ban lãnh đạo (phê duyệt) |
| **Mục tiêu** | Giải thích chi tiết các chỉ tiêu trong BCTC |
| **Tiên quyết** | Hoàn thành 3 BCTC chính |
| **Kích hoạt** | Cuối kỳ kế toán |

#### 🔄 Luồng chính (Main Success Scenario)

| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Kế toán | Thuyết minh đặc điểm hoạt động của DN |
| 2 | | Thuyết minh kỳ kế toán, đơn vị tiền tệ |
| 3 | | Thuyết minh chuẩn mực CSKT áp dụng |
| 4 | | Thuyết minh TSCĐ, BĐSĐT, hàng tồn kho, nợ phải thu, nợ phải trả |
| 5 | | Thuyết minh doanh thu, chi phí |
| 6 | | Thuyết minh các chỉ tiêu khác theo yêu cầu |
| 7 | Kế toán trưởng | Xác nhận tính đầy đủ, hợp lý |

✅ **Hậu kiểm:** Bản thuyết minh giải trình đầy đủ các chỉ tiêu trọng yếu

---

### 📌 [UC-BCTC-005] Tổng hợp Báo cáo tài chính hoàn chỉnh
🔗 Nguồn: [Cấp 1] | URL: https://ketoanthienung.net/bao-cao-tai-chinh-gom-nhung-gi-mau-bieu-bang-nao.htm

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán tổng hợp / `Secondary:` Kế toán trưởng (rà soát), Giám đốc (ký duyệt), Kiểm toán (xác nhận độc lập) |
| **Mục tiêu** | Hoàn thiện BCTC theo quy định TT99/2025/TT-BTC |
| **Tiên hoạt động | Hoàn thành ghi sổ kỳ báo cáo |
| **Kích hoạt** | Cuối năm tài chính |

#### 🔄 Luồng chính (Main Success Scenario)

| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Kế toán | Lập Báo cáo tình hình tài chính (B01-DN) |
| 2 | | Lập Báo cáo KQ HĐKD (B02-DN) |
| 3 | | Lập Báo cáo lưu chuyển tiền tệ (B03-DN) |
| 4 | | Lập Bản thuyết minh BCTC (B09-DN) |
| 5 | | In, đóng dấu, ký tên |
| 6 | Kế toán trưởng | Kiểm tra lần cuối |
| 7 | Giám đốc | Ký duyệt |

#### ⚠️ Luồng thay thế/Ngoại lệ

| Bước gốc | Điều kiện kích hoạt | Hành động xử lý |
|----------|-------------------|------------------|
| [1-4] | Phát hiện sai sót | Điều chỉnh hồi tố nếu trọng yếu |

✅ **Hậu kiểm:** BCTC hoàn chỉnh gồm: B01-DN + B02-DN + B03-DN + B09-DN

---

### 📌 [UC-BCTC-006] Nộp Báo cáo tài chính cho cơ quan thuế
🔗 Nguồn: [Cấp 1] | URL: https://ketoanthienung.net/thoi-han-nop-bao-cao-tai-chinh-theo-thong-tu-99.htm

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán / `Secondary:` Kế toán trưởng (soát lại), Giám đốc (ký) |
| **Mục tiêu** | Nộp BCTC đúng thời hạn quy định |
| **Tiên quyết** | BCTC đã được phê duyệt |
| **Kích hoạt** | Đến hạn nộp (trước ngày 30/3 năm sau) |

#### 🔄 Luồng chính (Main Success Scenario)

| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Kế toán | In BCTC theo số liệu đã phê duyệt |
| 2 | | Làm phiên bản điện tử XML theo quy định |
| 3 | | Nộp qua hệ thống thuế điện tử |
| 4 | | In và nộp bản cứng cho CQ thuế |

✅ **Hậu kiểm:** BCTC được nộp đúng thời hạn, đúng định dạng

---

### 📌 [UC-BCTC-007] Công khai Báo cáo tài chính
🔗 Nguồn: [Cấp 2] | URL: https://ketoanthienung.net/cong-khai-bao-cao-tai-chinh-theo-thong-tu-99.htm

| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán / `Secondary:` Ban lãnh đạo |
| **Mục tiêu** | Công khai BCTC theo quy định pháp luật |
| **Tiên quyết** | BCTC đã được phê duyệt |
| **Kích hoạt** | Sau khi nộp cơ quan thuế |

#### 🔄 Luồng chính (Main Success Scenario)

| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Kế toán | Chuẩn bị BCTC đã phê duyệt |
| 2 | | Công khai trên website (nếu có) |
| 3 | | Lưu trữ theo quy định |

✅ **Hậu kiểm:** BCTC được công khai đúng quy định

---

## ⚠️ LƯU Ý & MÂU THUẪN (Nếu có)

- BCTC năm: nộp trước 30/3 năm sau; BCTC giữa niên độ: nộp trong 50 ngày cuối quý
- Chỉ tiêu không có số liệu được miễn trình bày nhưng không được thay đổi mã số
- DN không đáp ứng giả định hoạt động liên tục: áp dụng mẫu B01-DNKLT, B02-DNKLT, B03-DNKLT

🛑 QUY TẮC KIỂM TRA TRƯỚC KHI XUẤT:
☐ Đã duyệt đúng tối đa 2 cấp (Cha → Con)?
☐ Mỗi UC đều có ID duy nhất và gắn nguồn URL rõ ràng?
☐ Đã loại bỏ trùng lặp, ưu tiên chi tiết từ Cấp 2?
☐ Không có nội dung bịa đặt/hallucination?
☐ Định dạng Markdown chuẩn, sẵn sàng lưu file?