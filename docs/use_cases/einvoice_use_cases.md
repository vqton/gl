<!-- 
📁 TÊN FILE ĐỀ XUẤT: usecases_einvoice_tt99_20260416.md
🕐 Ngày trích xuất: 2026-04-16
🔗 URL gốc: https://ketoanthienung.net/cach-lap-cac-loai-hoa-don-dien-tu.htm
📦 Độ sâu duyệt: 2 cấp (Cha → Con)
-->

# 📋 Use Cases Tổng hợp (Độ sâu: 2 cấp)

## 🗂️ Mục lục nguồn đã duyệt
| Cấp | URL | Trạng thái | Ghi chú |
|-----|-----|------------|---------|
| 1 | https://ketoanthienung.net/cach-lap-cac-loai-hoa-don-dien-tu.htm | ✅ | Trang tổng quan/điều hướng |
| 2 | https://ketoanthienung.net/xu-ly-hoa-don-dien-tu-viet-sai-cac-truong-hop.htm | ✅ | Xử lý hóa đơn sai sót |
| 2 | https://ketoanthienung.net/cach-lap-hoa-don-ban-hang-dien-tu.htm | ✅ | Cách lập hóa đơn bán hàng điện tử |
| 2 | https://ketoanthienung.net/huong-dan-cach-xuat-hoa-don-dien-tu.htm | ✅ | Hướng dẫn xuất hóa đơn điện tử |
| 2 | https://ketoanthienung.net/cach-lap-hoa-don-dieu-chinh-tang-giam.htm | ✅ | Lập hóa đơn điều chỉnh tăng giảm |
| 2 | https://ketoanthienung.net/cach-lap-hoa-don-thay-the.htm | ✅ | Lập hóa đơn thay thế |
| 2 | https://ketoanthienung.net/xu-ly-hoa-don-dien-tu-khong-co-ma-lap-sai-sot.htm | ✅ | Xử lý hóa đơn không có mã bị sai |
| 2 | https://ketoanthienung.net/cach-tra-cuu-hoa-don-dien-tu-dau-vao-dau-ra-tren-trang-thue.htm | ✅ | Tra cứu hóa đơn trên trang thuế |

## 📦 Nhóm Use Case

### 📌 [UC-EI-001] Tạo Hóa đơn bán hàng điện tử (có mã)
🔗 Nguồn: [Cấp 2] | URL: https://ketoanthienung.net/cach-lap-hoa-don-ban-hang-dien-tu.htm
| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán viên / `Secondary:` Hệ thống eInvoice |
| **Mục tiêu** | Lập và xuất hóa đơn điện tử hợp lệ có mã của cơ quan thuế |
| **Tiên quyết** | Đã đăng ký sử dụng hóa đơn điện tử với cơ quan thuế |
| **Kích hoạt** | Sau khi giao dịch bán hàng hoàn thành |

#### 🔄 Luồng chính (Main Success Scenario)
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Chọn loại hóa đơn (01GTKT, 02GTTT...) | |
| 2 | Nhập thông tin người bán | Kiểm tra MST người bán |
| 3 | Nhập thông tin người mua | Kiểm tra MST người mua (nếu B2B) |
| 4 | Nhập danh sách hàng hóa/dịch vụ | Tính thành tiền, thuế GTGT |
| 5 | Chọn thuế suất (0%, 8%, 10%) | Tính tiền thuế |
| 6 | | Tính tổng thanh toán |
| 7 | Xác nhận | Ký số điện tử |
| 8 | | Gửi XML lên Tổng cục Thuế |
| 9 | | Nhận mã cấp từ CQT |
| 10 | | Gửi hóa đơn cho người mua |

#### ⚠️ Luồng thay thế/Ngoại lệ
| Bước gốc | Điều kiện kích hoạt | Hành động xử lý |
|----------|-------------------|-----------------|
| [3] | Người mua không có MST | Chuyển hóa đơn không có mã |
| [5] | Hàng hóa được giảm thuế | Áp dụng thuế suất 8% thay vì 10% |
| [8] | Gửi thất bại | Lưu tạm, retry sau |

✅ **Hậu kiểm:** Hóa đơn có mã CQT, đã gửi cho người mua

---

### 📌 [UC-EI-002] Xử lý Hóa đơn điện tử có sai sót (có mã)
🔗 Nguồn: [Cấp 1/2] | URL: https://ketoanthienung.net/xu-ly-hoa-don-dien-tu-viet-sai-cac-truong-hop.htm
| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán viên / `Secondary:` Người mua, Cơ quan thuế |
| **Mục tiêu** | Xử lý hóa đơn điện tử đã lập có sai sót theo Nghị định 70/2025/NĐ-CP |
| **Tiên quyết** | Hóa đơn đã được cấp mã, phát hiện sai sót trong vòng 30 ngày |
| **Kích hoạt** | Phát hiện hóa đơn có sai sót |

#### 🔄 Luồng chính (Main Success Scenario)
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Xác định loại sai sót | Xác định: Tên/Địa chỉ hay Giá trị |
| 2 | Xác định hình thức xử lý | Điều chỉnh hoặc Thay thế |
| 3 | Lập văn bản thỏa thuận | Ghi rõ nội dung sai |
| 4 | Lập hóa đơn điều chỉnh/thay thế | Có dòng chữ tham chiếu |
| 5 | Ký số | |
| 6 | Gửi CQT cấp mã | |
| 7 | Gửi cho người mua | |

#### ⚠️ Luồng thay thế/Ngoại lệ
| Bước gốc | Điều kiện kích hoạt | Hành động xử lý |
|----------|-------------------|-----------------|
| [1] | Chỉ sai tên, địa chỉ người mua (không sai MST) | Thông báo cho người mua, không cần điều chỉnh |
| [1] | Sai giá trị cao hơn thực tế | Lập hóa đơn điều chỉnh giảm (ghi âm) |
| [1] | Sai giá trị thấp hơn thực tế | Lập hóa đơn điều chỉnh tăng (ghi dương) |
| [2] | Đã xử lý lần 1 bằng điều chỉnh | Các lần sau phải dùng điều chỉnh |

✅ **Hậu kiểm:** Hóa đơn điều chỉnh/thay thế đã có mã, gửi cho người mua
🔀 *Ghi chú:* Theo Nghị định 70/2025: Bắt buộc có văn bản thỏa thuận trước khi điều chỉnh/thay thế

---

### 📌 [UC-EI-003] Lập Hóa đơn điều chỉnh Tăng/Giảm
🔗 Nguồn: [Cấp 2] | URL: https://ketoanthienung.net/cach-lap-hoa-don-dieu-chinh-tang-giam.htm
| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán viên |
| **Mục tiêu** | Điều chỉnh tăng hoặc giảm giá trị hóa đơn đã lập sai |
| **Tiên quyết** | Đã có văn bản thỏa thuận với người mua |
| **Kích hoạt** | Phát hiện hóa đơn sai giá trị |

#### 🔄 Luồng chính (Main Success Scenario)
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Xác định chênh lệch | Tính chênh lệch = Thực tế - Ghi sai |
| 2 | Xác định tăng/giảm | Nếu thực tế > ghi sai = Điều chỉnh tăng |
| 3 | Lập hóa đơn điều chỉnh | Ghi dấu dương (tăng) hoặc âm (giảm) |
| 4 | Ghi dòng chữ "Điều chỉnh cho hóa đơn..." | |
| 5 | Ký số, gửi CQT | Nhận mã |
| 6 | Gửi người mua | |

#### ⚠️ Luồng thay thế/Ngoại lệ
| Bước gốc | Điều kiện kích hoạt | Hành động xử lý |
|----------|-------------------|-----------------|
| [2] | Chênh lệch = 0 | Không cần điều chỉnh |
| [1] | 1 hóa đơn điều chỉnh cho nhiều hóa đơn sai | Phải kèm bảng kê Mẫu 01/BK-ĐCTT |

✅ **Hậu kiểm:** Hóa đơn điều chỉnh đã được cấp mã

---

### 📌 [UC-EI-004] Lập Hóa đơn thay thế
🔗 Nguồn: [Cấp 2] | URL: https://ketoanthienung.net/cach-lap-hoa-don-thay-the.htm
| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán viên |
| **Mục tiêu** | Thay thế hoàn toàn hóa đơn đã lập sai |
| **Tiên quyết** | Đã có văn bản thỏa thuận |
| **Kích hoạt** | Chọn phương án thay thế thay vì điều chỉnh |

#### 🔄 Luồng chính (Main Success Scenario)
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Lập hóa đơn mới với thông tin đúng | |
| 2 | Ghi dòng chữ "Thay thế cho hóa đơn..." | |
| 3 | Ký số | |
| 4 | Gửi CQT cấp mã | |
| 5 | Gửi cho người mua | |

✅ **Hậu kiểm:** Hóa đơn thay thế đã có mã, hóa đơn gốc bị vô hiệu

---

### 📌 [UC-EI-005] Tra cứu Hóa đơn điện tử trên trang thuế
🔗 Nguồn: [Cấp 2] | URL: https://ketoanthienung.net/cach-tra-cuu-hoa-don-dien-tu-dau-vao-dau-ra-tren-trang-thue.htm
| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán viên / `Secondary:` Người mua |
| **Mục tiêu** | Tra cứu trạng thái hóa đơn, xác nhận tính hợp lệ |
| **Tiên quyết** | Có mã tra cứu hoặc số hóa đơn |
| **Kích hoạt** | Nhập thông tin tra cứu |

#### 🔄 Luồng chính (Main Success Scenario)
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Truy cập website thuế | |
| 2 | Nhập mã tra cứu hoặc số hóa đơn | |
| 3 | | Hiển thị thông tin hóa đơn |
| 4 | | Hiển thị trạng thái (Hợp lệ/Đã hủy/Đã điều chỉnh) |

✅ **Hậu kiểm:** Xem được thông tin chi tiết hóa đơn

---

### 📌 [UC-EI-006] Xử lý Hóa đơn điện tử không có mã bị sai
🔗 Nguồn: [Cấp 2] | URL: https://ketoanthienung.net/xu-ly-hoa-don-dien-tu-khong-co-ma-lap-sai-sot.htm
| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán viên |
| **Mục tiêu** | Xử lý hóa đơn điện tử không có mã của CQT bị sai |
| **Tiên quyết** | Hóa đơn không có mã đã phát hiện sai |
| **Kích hoạt** | Phát hiện sai sót |

#### 🔄 Luồng chính (Main Success Scenario)
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Lập hóa đơn điều chỉnh/thay thế | |
| 2 | Ký số | |
| 3 | Gửi dữ liệu đến CQT | Xác nhận tiếp nhận |
| 4 | Gửi cho người mua | |

✅ **Hậu kiểm:** Hóa đơn điều chỉnh đã gửi cho CQT

---

### 📌 [UC-EI-007] Xuất Hóa đơn cho khách lẻ, cá nhân không lấy hóa đơn
🔗 Nguồn: [Cấp 2] | URL: https://ketoanthienung.net/xuat-hoa-don-cho-khach-le-ca-nhan-nguoi-mua-khong-lay-hoa-don.htm
| Trường | Nội dung |
|--------|----------|
| **Actor** | `Primary:` Kế toán viên bán hàng |
| **Mục tiêu** | Xuất hóa đơn điện tử cho khách lẻ, cá nhân không lấy hóa đơn |
| **Tiên quyết** | Khách hàng không yêu cầu hóa đơn nhưng DN vẫn phải xuất |
| **Kích hoạt** | Sau bán hàng cho khách lẻ |

#### 🔄 Luồng chính (Main Success Scenario)
| Bước | Actor | Hệ thống phản hồi |
|------|-------|-------------------|
| 1 | Không nhập thông tin người mua | Hoặc nhập "Cá nhân không lấy hóa đơn" |
| 2 | Nhập hàng hóa/dịch vụ | Tính tiền |
| 3 | Chọn thuế suất 0% nếu không chịu thuế | |
| 4 | Xuất hóa đơn | Ký số |
| 5 | Lưu trữ theo quy định | Gửi CQT (nếu có mã) |

✅ **Hậu kiểm:** Hóa đơn đã lưu trữ, kê khai đầy đủ

---

## ⚠️ LƯU Ý & MÂU THUẪN (Nếu có)
- Cách xử lý hóa đơn có mã và không có mã khác nhau: Hóa đơn có mã phải gửi CQT cấp mã, hóa đơn không có mã chỉ gửi dữ liệu
- Thời hạn xử lý: Phải xử lý trước khi hết 30 ngày từ ngày lập hóa đơn (theo hướng dẫn mới)
- Không được hủy hóa đơn đã lập sai (theo Nghị định 70/2025) - chỉ được điều chỉnh hoặc thay thế

🛑 QUY TẮC KIỂM TRA TRƯỚC KHI XUẤT:
☑️ Đã duyệt đúng tối đa 2 cấp (Cha → Con)?
☑️ Mỗi UC đều có ID duy nhất và gắn nguồn URL rõ ràng?
☑️ Đã loại bỏ trùng lặp, ưu tiên chi tiết từ Cấp 2?
☑️ Không có nội dung bịa đặt/hallucination?
☑️ Định dạng Markdown chuẩn, sẵn sàng lưu file?