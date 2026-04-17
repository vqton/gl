# Use Cases: Lao Động - Tiền Lương

---
### 📌 Quản lý hợp đồng lao động
- **Tác nhân (Actors):** Nhân viên HR, Quản lý
- **Mục tiêu:** Tạo, lưu trữ và quản lý các hợp đồng lao động (thử việc, chính thức)
- **Điều kiện tiên quyết (Preconditions):** 
  - Người lao động đã được tuyển dụng
  - Thông tin cá nhân đầy đủ (CMND/CCCD, địa chỉ, số điện thoại)
- **Luồng chính (Main Flow):**
  1. HR tạo hợp đồng thử việc hoặc chính thức
  2. Nhập thông tin: họ tên, vị trí, mức lương, thời hạn hợp đồng
  3. Lưu trữ hợp đồng vào hệ thống
  4. Theo dõi ngày hết hạn hợp đồng
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 1] → Hợp đồng thử việc: Chuyển sang hợp đồng chính thức nếu đạt yêu cầu
- **Điều kiện hậu kiểm (Postconditions):** Hợp đồng được lưu trữ, có thể truy xuất khi cần
- **Ghi chú/Tham chiếu:** Theo Bộ luật Lao động 2019

---
### 📌 Tính lương hàng tháng
- **Tác nhân (Actors):** Kế toán tiền lương
- **Mục tiêu:** Tính toán chính xác lương thực nhận cho từng nhân viên
- **Điều kiện tiên quyết (Preconditions):**
  - Bảng chấm công đã được phê duyệt
  - Hệ thống thang bảng lương đã được thiết lập
- **Luồng chính (Main Flow):**
  1. Lấy dữ liệu chấm công (số ngày làm việc, ngày nghỉ, tăng ca)
  2. Áp dụng công thức tính lương: Lương = Lương cơ bản × Số ngày làm / Tổng ngày
  3. Tính các khoản phụ cấp, thưởng
  4. Tính các khoản khấu trừ (BHXH, BHYT, BHTN, thuế TNCN)
  5. Tính lương thực nhận
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 2] → Có ngày nghỉ không hưởng lương: Trừ lương theo ngày nghỉ
  - [Bước 3] → Làm thêm giờ: Tính lương tăng ca (150%-300%)
- **Điều kiện hậu kiểm (Postconditions):** Bảng lương hoàn thành, sẵn sàng chi trả
- **Ghi chú/Tham chiếu:** ketoanthienung.net/cach-tinh-luong-theo-gio-ngay-tuan-thang

---
### 📌 Hạch toán tiền lương và bảo hiểm
- **Tác nhân (Actors):** Kế toán
- **Mục tiêu:** Ghi nhận chi phí lương và các khoản trích theo lương vào sổ kế toán
- **Điều kiện tiên quyết (Preconditions):** Bảng lương đã tính xong
- **Luồng chính (Main Flow):**
  1. Tính các khoản trích theo lương (BHXH 17.5%, BHYT 3%, BHTN 1%, KPCĐ 2%)
  2. Định khoản Nợ 622 - Chi phí tiền lương / Có 334 - Phải trả người lao động
  3. Định khoản trích BH: Nợ 622 / Có 338 - Phải trả khác
  4. Hạch toán thanh toán lương: Nợ 334 / Có 111, 112
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 1] → Đóng BHXH theo lương cơ sở (2026: 2,300,000đ): Tính trên mức lương tối thiểu vùng
- **Điều kiện hậu kiểm (Postconditions):** Các bút toán được ghi nhận đúng tài khoản
- **Ghi chú/Tham chiếu:** ketoanthienung.net/cach-hach-toan-tien-luong-va-cac-khoan-trich-theo-luong

---
### 📌 Tính thuế thu nhập cá nhân (TNCN)
- **Tác nhân (Actors):** Kế toán
- **Mục tiêu:** Tính và khấu trừ thuế TNCN theo biểu thuế lũy tiến
- **Điều kiện tiên quyết (Preconditions):**
  - Lương tháng đã tính xong
  - Người lao động có MST cá nhân
- **Luồng chính (Main Flow):**
  1. Xác định thu nhập chịu thuế = Lương - Các khoản giảm trừ
  2. Giảm trừ gia cảnh: 11 triệu/tháng + 4.4 triệu/người phụ thuộc
  3. Áp dụng biểu thuế lũy tiến (5%-35%)
  4. Tính số thuế phải nộp tháng
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 2] → Không có người phụ thuộc: Chỉ giảm trừ 11 triệu
  - [Bước 3] → Thu nhập < 5 triệu: Không phải nộp thuế
- **Điều kiện hậu kiểm (Postconditions):** Số thuế TNCN được khấu trừ chính xác
- **Ghi chú/Tham chiếu:** ketoanthienung.net/cach-tinh-thue-tncn

---
### 📌 Quản lý bảo hiểm xã hội
- **Tác nhân (Actors):** Kế toán, HR
- **Mục tiêu:** Tính và đóng BHXH, BHYT, BHTN đầy đủ
- **Điều kiện tiên quyết (Preconditions):** Danh sách nhân viên tham gia bảo hiểm
- **Luồng chính (Main Flow):**
  1. Xác định mức lương đóng BH (lương cơ bản + phụ cấp lương)
  2. Tính mức đóng:
     - BHXH: 17.5% (DN: 14%, NLĐ: 3.5%)
     - BHYT: 3% (DN: 2%, NLĐ: 1%)
     - BHTN: 1% (DN: 0.5%, NLĐ: 0.5%)
  3. Làm tờ khai BH hàng tháng
  4. Nộp tiền BH đúng hạn (trước ngày 30 tháng sau)
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 1] → Lương > 149 triệu: Đóng BHXH tối đa ở mức 149 triệu
- **Điều kiện hậu kiểm (Postconditions):** BH được đóng đầy đủ, đúng hạn
- **Ghi chú/Tham chiếu:** ketoanthienung.net/dong-bao-hiem-xa-hoi-theo-muc-luong-nao

---
### 📌 Tính lương làm thêm giờ (tăng ca)
- **Tác nhân (Actors):** Kế toán, Quản lý phòng ban
- **Mục tiêu:** Tính chính xác tiền lương làm thêm giờ theo quy định
- **Điều kiện tiên quyết (Preconditions):** Bảng chấm công có ghi nhận giờ tăng ca
- **Luồng chính (Main Flow):**
  1. Xác định số giờ tăng ca theo ngày thường, ngày nghỉ, ngày lễ
  2. Tính hệ số:
     - Ngày thường: 150%
     - Ngày nghỉ hàng tuần: 200%
     - Ngày lễ, Tết: 300%
  3. Tính tiền lương tăng ca = Lương giờ × Hệ số × Số giờ
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 2] → Tăng ca ban đêm: Cộng thêm 20% lương
- **Điều kiện hậu kiểm (Postconditions):** Tiền tăng ca được tính vào bảng lương
- **Ghi chú/Tham chiếu:** ketoanthienung.net/cach-tinh-luong-lam-tang-ca-them-gio-ngay-le

---
### 📌 Tính trợ cấp thôi việc
- **Tác nhân (Actors):** HR, Kế toán
- **Mục tiêu:** Tính trợ cấp thôi việc khi chấm dứt hợp đồng lao động
- **Điều kiện tiên quyết (Preconditions):**
  - Hợp đồng lao động chấm dứt
  - Người lao động đã làm việc từ 12 tháng trở lên
- **Luồng chính (Main Flow):**
  1. Xác định thời gian làm việc (số tháng)
  2. Tính mức hưởng: 0.5 tháng lương cho mỗi năm làm việc
  3. Lương tính trợ cấp = (Lương tháng × 12) / 12
  4. Chi trả trợ cấp
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 1] → Nghỉ việc do vi phạm: Không được hưởng trợ cấp
- **Điều kiện hậu kiểm (Postconditions):** Trợ cấp được tính và chi trả đúng quy định
- **Ghi chú/Tham chiếu:** ketoanthienung.net/dieu-kien-va-muc-huong-tro-cap-thoi-viec-2024

---
### 📌 Quản lý nghỉ phép năm
- **Tác nhân (Actors):** Nhân viên, Quản lý, HR
- **Mục tiêu:** Theo dõi và tính lương cho ngày nghỉ phép
- **iều kiện tiên quyết (Preconditions):** Quy chế nghỉ phép đã ban hành
- **Luồng chính (Main Flow):**
  1. Nhân viên đăng ký nghỉ phép
  2. Quản lý phê duyệt
  3. HR cập nhật số ngày phép đã nghỉ
  4. Kế toán tính lương ngày nghỉ phép (hưởng nguyên lương)
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 4] → Nghỉ phép không được duyệt: Không tính lương
- **Điều kiện hậu kiểm (Postconditions):** Ngày phép được theo dõi chính xác
- **Ghi chú/Tham chiếu:** ketoanthienung.net/quy-dinh-ve-nghi-phep-nam-cua-nguoi-lao-dong

---
### 📌 Lập báo cáo tình hình sử dụng lao động
- **Tác nhân (Actors):** HR, Kế toán
- **Mục tiêu:** Báo cáo định kỳ về tình hình lao động cho cơ quan quản lý
- **Điều kiện tiên quyết (Preconditions):** Dữ liệu lao động được cập nhật đầy đủ
- **Luồng chính (Main Flow):**
  1. Tổng hợp số lượng lao động (đầu kỳ, cuối kỳ)
  2. Phân loại theo loại hợp đồng, ngành nghề
  3. Báo cáo tình hình tuyển dụng, thôi việc
  4. Nộp báo cáo theo quy định (trước 31/12 hàng năm)
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 1] → DN có > 50 lao động: Báo cáo bắt buộc
- **Điều kiện hậu kiểm (Postconditions):** Báo cáo hoàn thành và nộp đúng hạn
- **Ghi chú/Tham chiếu:** ketoanthienung.net/cach-lam-bao-cao-tinh-hinh-su-dung-lao-dong

---
### 📌 Xây dựng thang bảng lương
- **Tác nhân (Actors):** Quản lý, HR
- **Mục tiêu:** Thiết lập hệ thống thang bảng lương theo Nghị định 49
- **Điều kiện tiên quyết (Preconditions):** Có quy chế lương thưởng nội bộ
- **Luồng chính (Main Flow):**
  1. Xác định mức lương tối thiểu vùng (2026: 4.2-6.9 triệu)
  2. Xây dựng thang lương (tối thiểu 5 bậc)
  3. Xây dựng bảng lương theo vị trí công việc
  4. Đăng ký thang bảng lương với Sở LĐ-TB&XH
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 4] → Không đăng ký: Bị phạt theo quy định
- **Điều kiện hậu kiểm (Postconditions):** Thang bảng lương hợp lệ, sẵn sàng áp dụng
- **Ghi chú/Tham chiếu:** ketoanthienung.net/cach-xay-dung-thang-bang-luong-moi-nhat

---
### 📌 Quản lý chấm công
- **Tác nhân (Actors):** Quản lý phòng ban, HR
- **Mục tiêu:** Ghi nhận chính xác thời gian làm việc của nhân viên
- **Điều kiện tiên quyết (Preconditions):** Có hệ thống chấm công (máy chấm công, file Excel)
- **Luồng chính (Main Flow):**
  1. Nhân viên check-in/check-out
  2. Tổng hợp dữ liệu chấm công cuối tháng
  3. Xác định ngày làm việc, ngày nghỉ, ngày phép
  4. Lập bảng chấm công làm căn cứ tính lương
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 2] → Quên chấm công: Căn cứ vào đơn xin nghỉ/phép
- **Điều kiện hậu kiểm (Postconditions):** Bảng chấm công hoàn thành, làm căn cứ tính lương
- **Ghi chú/Tham chiếu:** ketoanthienung.net/mau-bang-cham-cong-tren-excel-cho-nhan-vien