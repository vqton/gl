# CASH & BANK USE CASES (T01-T22)
*Based on: TT99/2025, Circular on Cash Management*

---

### 📌 T01 — Rút tiền gửi ngân hàng về nhập quỹ tiền mặt
- **Tác nhân (Actors):** Kế toán, Thủ quỹ
- **Mục tiêu:** Chuyển tiền từ tài khoản ngân hàng (TK 112) sang quỹ tiền mặt (TK 111)
- **Điều kiện tiên quyết (Preconditions):** Doanh nghiệp có số dư tiền gửi ngân hàng tại TK 112
- **Luồng chính (Main Flow):**
  1. Kế toán lập phiếu thu tiền
  2. Thủ quỹ nhận tiền từ ngân hàng về nhập quỹ
  3. Kế toán hạch toán: Nợ TK 111(1111) / Có TK 112
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 2] → Ngân hàng từ chối: Thông báo cho kế toán để kiểm tra
- **Điều kiện hậu kiểm (Postconditions):** Tiền mặt tại quỹ tăng, tiền gửi ngân hàng giảm tương ứng
- **Định khoản:** Nợ 111(1111) / Có 112

---

### 📌 T02 — Thu tiền bán hàng nhập quỹ
- **Tác nhân (Actors):** Kế toán, Thủ quỹ, Khách hàng
- **Mục tiêu:** Thu tiền từ bán hàng hóa, dịch vụ và nhập vào quỹ tiền mặt
- **Điều kiện tiên quyết (Preconditions):** Có giao dịch bán hàng với thanh toán tiền mặt, có hóa đơn GTGT hợp lệ
- **Luồng chính (Main Flow):**
  1. Khách hàng thanh toán tiền mặt
  2. Thủ quỹ kiểm đếm và nhận tiền
  3. Kế toán lập phiếu thu
  4. Hạch toán: Nợ TK 111 / Có TK 511, 515, 711 (doanh thu chưa thuế) / Có TK 333 (33311) thuế GTGT đầu ra
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 4] → DN tính thuế GTGT phương pháp trực tiếp: Nợ TK 111 / Có TK 511 (bao gồm thuế GTGT)
- **Điều kiện hậu kiểm (Postconditions):** Tiền mặt tại quỹ tăng, doanh thu được ghi nhận
- **Định khoản:** Nợ 111(1111) / Có 511,515,711 + Có 333(33311)

---

### 📌 T03 — Chi tiền mặt mua nguyên vật liệu, CCDC, TSCĐ
- **Tác nhân (Actors):** Kế toán, Thủ quỹ, Nhà cung cấp
- **Mục tiêu:** Thanh toán tiền mua hàng hóa, vật tư bằng tiền mặt
- **Điều kiện tiên quyết (Preconditions):** Có hóa đơn GTGT hợp lệ từ nhà cung cấp, đã nhận hàng
- **Luồng chính (Main Flow):**
  1. Nhà cung cấp giao hàng và hóa đơn
  2. Kế toán kiểm tra hóa đơn, nhận hàng
  3. Thủ quỹ chi tiền mặt cho nhà cung cấp
  4. Kế toán lập phiếu chi
  5. Hạch toán: Nợ TK 151,152,153,156,211 / Nợ TK 133 (thuế GTGT đầu vào) / Có TK 111
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 5] → DN tính thuế GTGT phương pháp trực tiếp: Nợ TK 151,152,153,156,211 / Có TK 111
- **Điều kiện hậu kiểm (Postconditions):** Tiền mặt giảm, hàng mua được ghi nhận vào tài sản
- **Định khoản:** Nợ 151,152,153,156,211 + Nợ 133 / Có 111(1111)

---

### 📌 T04 — Nộp tiền mặt vào ngân hàng
- **Tác nhân (Actors):** Kế toán, Thủ quỹ
- **Mục tiêu:** Gửi tiền mặt từ quỹ vào tài khoản ngân hàng
- **Điều kiện tiên quyết (Preconditions):** Có tiền mặt tại quỹ (TK 111)
- **Luồng chính (Main Flow):**
  1. Kế toán lập phiếu chi tiền mặt
  2. Thủ quỹ xuất quỹ nộp ngân hàng
  3. Ngân hàng xác nhận đã nhận tiền
  4. Hạch toán: Nợ TK 112 / Có TK 111
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 3] → Ngân hàng từ chối: Kiểm tra lại tiền và làm lại thủ tục
- **Điều kiện hậu kiểm (Postconditions):** Tiền mặt tại quỹ giảm, tiền gửi ngân hàng tăng
- **Định khoản:** Nợ 112 / Có 111(1111)

---

### 📌 T05 — Chi tiền mặt trả lương CBCNV
- **Tác nhân (Actors):** Kế toán, Thủ quỹ, CBCNV
- **Mục tiêu:** Thanh toán lương bằng tiền mặt cho cán bộ công nhân viên
- **Điều kiện tiên quyết (Preconditions):** Có bảng lương đã được duyệt, số dư TK 334 > 0
- **Luồng chính (Main Flow):**
  1. Kế toán lập phiếu chi tiền mặt
  2. Thủ quỹ chi tiền mặt cho CBCNV
  3. CBCNV ký nhận lương
  4. Hạch toán: Nợ TK 334 / Có TK 111
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 3] → CBCNV vắng mặt: Giữ lại và thanh toán khi CBCNV đến nhận
- **Điều kiện hậu kiểm (Postconditions):** Số dư TK 334 giảm, tiền mặt tại quỹ giảm
- **Định khoản:** Nợ 334 / Có 111(1111)

---

### 📌 T06 — Xuất quỹ chi tạm ứng, chi trả nợ
- **Tác nhân (Actors):** Kế toán, Thủ quỹ, Người nhận tạm ứng/nhà cung cấp
- **Mục tiêu:** Chi tiền mặt tạm ứng cho nhân viên hoặc trả nợ cho nhà cung cấp
- **Điều kiện tiên quyết (Preconditions):** Có giấy đề nghị tạm ứng được duyệt hoặc có khoản nợ phải trả
- **Luồng chính (Main Flow):**
  1. Nhân viên/nhà cung cấp làm thủ tục nhận tiền
  2. Kế toán kiểm tra và trình duyệt
  3. Thủ quỹ chi tiền mặt
  4. Người nhận ký nhận
  5. Hạch toán: Nợ TK 141 (tạm ứng) hoặc Nợ TK 331,333,334,336,338,341,342 / Có TK 111
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 2] → Không duyệt: Trả lại hồ sơ yêu cầu bổ sung
- **Điều kiện hậu kiểm (Postconditions):** Tiền mặt giảm, các khoản nợ phải trả giảm
- **Định khoản:** Nợ 141/331/333/334/336/338/341/342 / Có 111(1111)

---

### 📌 T07 — Thu hồi nợ phải thu bằng tiền mặt
- **Tác nhân (Actors):** Kế toán, Thủ quỹ, Khách hàng
- **Mục tiêu:** Thu hồi các khoản nợ phải thu từ khách hàng, đối tác bằng tiền mặt
- **Điều kiện tiên quyết (Preconditions):** Có số dư các TK 131,136,138,141 > 0
- **Luồng chính (Main Flow):**
  1. Khách hàng/đối tác thanh toán nợ bằng tiền mặt
  2. Thủ quỹ kiểm đếm tiền
  3. Kế toán lập phiếu thu
  4. Hạch toán: Nợ TK 111 / Có TK 131,136,138,141
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 3] → Phát hiện tiền giả: Từ chối và báo cáo
- **Điều kiện hậu kiểm (Postconditions):** Tiền mặt tại quỹ tăng, các khoản phải thu giảm
- **Định khoản:** Nợ 111(1111) / Có 131,136,138,141

---

### 📌 T08 — Kiểm kê phát hiện thừa tiền mặt
- **Tác nhân (Actors):** Kế toán, Thủ quỹ, Ban kiểm kê
- **Mục tiêu:** Xử lý số tiền mặt thừa phát hiện khi kiểm kê quỹ
- **Điều kiện tiên quyết (Preconditions):** Tiến hành kiểm kê quỹ tiền mặt định kỳ hoặc đột xuất
- **Luồng chính (Main Flow):**
  1. Ban kiểm kê đối chiếu sổ sách và thực tế tại quỹ
  2. Phát hiện số tiền thừa (số thực tế > sổ sách)
  3. Lập biên bản kiểm kê ghi nhận số thừa
  4. Hạch toán: Nợ TK 111 / Có TK 338(3381) - chờ xử lý
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 3] → Xác định được nguyên nhân: Hạch toán vào TK liên quan tương ứng
- **Điều kiện hậu kiểm (Postconditions):** Tiền mặt thừa được ghi nhận, chờ xác định nguyên nhân để xử lý
- **Định khoản:** Nợ 111(1111) / Có 338(3381)

---

### 📌 T09 — Kiểm kê phát hiện thiếu tiền mặt
- **Tác nhân (Actors):** Kế toán, Thủ quỹ, Ban kiểm kê
- **Mục tiêu:** Xử lý số tiền mặt thiếu phát hiện khi kiểm kê quỹ
- **Điều kiện tiên quyết (Preconditions):** Tiến hành kiểm kê quỹ tiền mặt
- **Luồng chính (Main Flow):**
  1. Ban kiểm kê đối chiếu sổ sách và thực tế tại quỹ
  2. Phát hiện số tiền thiếu (số thực tế < sổ sách)
  3. Lập biên bản kiểm kê ghi nhận số thiếu
  4. Hạch toán: Nợ TK 138(1381) / Có TK 111
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 3] → Xác định được nguyên nhân: Xử lý bồi thường hoặc tính vào chi phí
- **Điều kiện hậu kiểm (Postconditions):** Tiền mặt thiếu được ghi nhận, chờ xác định nguyên nhân để xử lý
- **Định khoản:** Nợ 138(1381) / Có 111(1111)

---

### 📌 T10 — Nhận vốn cấp bằng tiền mặt nhập quỹ
- **Tác nhân (Actors):** Kế toán, Thủ quỹ, Chủ sở hữu/cổ đông
- **Mục tiêu:** Nhận vốn góp bằng tiền mặt từ chủ sở hữu/cổ đông
- **Điều kiện tiên quyết (Preconditions):** Có quyết định góp vốn, biên bản góp vốn
- **Luồng chính (Main Flow):**
  1. Chủ sở hữu/cổ đông nộp tiền mặt vào quỹ
  2. Thủ quỹ kiểm đếm tiền
  3. Kế toán lập phiếu thu
  4. Hạch toán: Nợ TK 111 / Có TK 411
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 2] → Tiền không đủ mệnh giá: Yêu cầu đổi tiền
- **Điều kiện hậu kiểm (Postconditions):** Tiền mặt tăng, vốn chủ sở hữu tăng
- **Định khoản:** Nợ 111(1111) / Có 411

---

### 📌 T11 — Nhận ký quỹ, ký cược bằng tiền mặt
- **Tác nhân (Actors):** Kế toán, Thủ quỹ, Đơn vị khác
- **Mục tiêu:** Nhận tiền ký quỹ, ký cược từ đơn vị khác để đảm bảo thực hiện hợp đồng
- **Điều kiện tiên quyết (Preconditions):** Có hợp đồng ký quỹ, ký cược giữa các bên
- **Luồng chính (Main Flow):**
  1. Đơn vị khác nộp tiền ký quỹ, ký cược
  2. Thủ quỹ kiểm đếm tiền
  3. Kế toán lập phiếu thu
  4. Hạch toán: Nợ TK 111 / Có TK 344 (nhận thế chấp ký quỹ, ký cược dài hạn)
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 1] → Đơn vị nộp vàng bạc, kim khí quý, đá quý: Hạch toán theo giá trị tương ứng
- **Điều kiện hậu kiểm (Postconditions):** Tiền mặt tăng, nợ phải trả về ký quỹ tăng
- **Định khoản:** Nợ 111(1111) / Có 344

---

### 📌 T12 — Hoàn trả ký quỹ, ký cược bằng tiền mặt
- **Tác nhân (Actors):** Kế toán, Thủ quỹ, Đơn vị khác
- **Mục tiêu:** Hoàn trả tiền ký quỹ, ký cược cho đơn vị khác khi hết thời hạn hợp đồng
- **Điều kiện tiên quyết (Preconditions):** Có số dư TK 344 > 0, hết thời hạn hoặc hợp đồng đã hoàn thành
- **Luồng chính (Main Flow):**
  1. Kế toán kiểm tra và xác nhận đủ điều kiện hoàn trả
  2. Thủ quỹ chi tiền mặt cho đơn vị
  3. Đơn vị ký nhận
  4. Hạch toán: Nợ TK 344 / Có TK 111
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 1] → Vi phạm hợp đồng: Không hoàn trả theo quy định
- **Điều kiện hậu kiểm (Postconditions):** Tiền mặt giảm, nợ phải trả về ký quỹ giảm
- **Định khoản:** Nợ 344 / Có 111(1111)

---

### 📌 T13 — Chi tiền mặt chi trả chi phí kinh doanh
- **Tác nhân (Actors):** Kế toán, Thủ quỹ, Người nhận thanh toán
- **Mục tiêu:** Thanh toán các khoản chi phí phát sinh trong quá trình kinh doanh
- **Điều kiện tiên quyết (Preconditions):** Có hóa đơn, chứng từ chi phí hợp lệ
- **Luồng chính (Main Flow):**
  1. Người nhận thanh toán xuất hóa đơn, chứng từ
  2. Kế toán kiểm tra và xác nhận chi phí
  3. Thủ quỹ chi tiền mặt
  4. Hạch toán: Nợ TK 627,641,642,635,811 (chi phí tương ứng) / Nợ TK 133 (nếu có thuế GTGT) / Có TK 111
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 4] → DN tính thuế GTGT phương pháp trực tiếp: Nợ TK 627,641,642,635,811 / Có TK 111
- **Điều kiện hậu kiểm (Postconditions):** Tiền mặt giảm, chi phí được ghi nhận
- **Định khoản:** Nợ 627,641,642,635,811 + Nợ 133 / Có 111(1111)

---

### 📌 T14 — Đi vay bằng tiền mặt
- **Tác nhân (Actors):** Kế toán, Thủ quỹ, Bên cho vay
- **Mục tiêu:** Nhận tiền vay bằng tiền mặt từ bên cho vay
- **Điều kiện tiên quyết (Preconditions):** Có hợp đồng tín dụng/vay vốn
- **Luồng chính (Main Flow):**
  1. Bên cho vay giải ngân bằng tiền mặt
  2. Thủ quỹ nhận tiền mặt
  3. Kế toán lập phiếu thu
  4. Hạch toán: Nợ TK 111 / Có TK 341
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 4] → Vay ngắn hạn: Có TK 311 thay cho TK 341
- **Điều kiện hậu kiểm (Postconditions):** Tiền mặt tăng, nợ phải trả về vay tăng
- **Định khoản:** Nợ 111(1111) / Có 341 (vay dài hạn) hoặc 311 (vay ngắn hạn)

---

### 📌 T15 — Bán, thu hồi đầu tư nhập quỹ tiền mặt
- **Tác nhân (Actors):** Kế toán, Thủ quỹ, Bên mua
- **Mục tiêu:** Thu tiền từ bán chứng khoán, thu hồi vốn đầu tư nhập quỹ
- **Điều kiện tiên quyết (Preconditions):** Có chứng khoán, vốn đầu tư cần bán hoặc thu hồi
- **Luồng chính (Main Flow):**
  1. Bên mua thanh toán tiền mặt
  2. Thủ quỹ kiểm đếm tiền
  3. Kế toán lập phiếu thu
  4. Hạch toán: Nợ TK 111 / Nợ/Có TK 635 hoặc Có TK 515 (chênh lệch giá) / Có TK 121,128 (chứng khoán) / Có TK 221,222 (vốn góp) / Có TK 244 (ký cược, ký quỹ)
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 4] → Lỗ: Ghi Nợ TK 635 / Lãi: Ghi Có TK 515
- **Điều kiện hậu kiểm (Postconditions):** Tiền mặt tăng, các khoản đầu tư giảm
- **Định khoản:** Nợ 111(1111) + Nợ/Có 635/515 / Có 121,128,221,222,244

---

### 📌 T16 — Xuất quỹ tiền mặt chi đầu tư
- **Tác nhân (Actors):** Kế toán, Thủ quỹ
- **Mục tiêu:** Xuất tiền mặt để mua chứng khoán, góp vốn liên doanh, ký quỹ
- **Điều kiện tiên quyết (Preconditions):** Có quyết định đầu tư, hợp đồng góp vốn
- **Luồng chính (Main Flow):**
  1. Kế toán kiểm tra và xác nhận hồ sơ đầu tư
  2. Thủ quỹ xuất tiền mặt từ quỹ
  3. Kế toán lập phiếu chi
  4. Hạch toán: Nợ TK 121,228 (đầu tư chứng khoán) / Nợ TK 222 (góp vốn liên doanh) / Nợ TK 244 (ký cược, ký quỹ) / Có TK 111
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 1] → Hồ sơ không hợp lệ: Yêu cầu bổ sung
- **Điều kiện hậu kiểm (Postconditions):** Tiền mặt giảm, các khoản đầu tư tăng
- **Định khoản:** Nợ 121,228,222,244 / Có 111(1111)

---

### 📌 T17 — Thu tiền bán hàng bằng ngoại tệ
- **Tác nhân (Actors):** Kế toán, Thủ quỹ, Khách hàng nước ngoài
- **Mục tiêu:** Thu tiền từ bán hàng cho khách hàng nước ngoài bằng ngoại tệ
- **Điều kiện tiên quyết (Preconditions):** Có giao dịch bán hàng xuất khẩu hoặc bán hàng cho khách nước ngoài trong nước
- **Luồng chính (Main Flow):**
  1. Khách hàng thanh toán bằng ngoại tệ
  2. Thủ quỹ kiểm đếm ngoại tệ theo tỷ giá thực tế tại thời điểm thu tiền
  3. Kế toán lập phiếu thu
  4. Hạch toán: Nợ TK 111(1112) theo tỷ giá thực tế / Có TK 511 theo tỷ giá thực tế / Có TK 333(3331) thuế GTGT đầu ra
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 2] → Tỷ giá thay đổi: Điều chỉnh theo tỷ giá thực tế tại thời điểm thu tiền
- **Điều kiện hậu kiểm (Postconditions):** Ngoại tệ tại quỹ tăng, doanh thu được ghi nhận
- **Định khoản:** Nợ 111(1112) theo tỷ giá thực tế / Có 511 + Có 333(3331)

---

### 📌 T18 — Thu hồi nợ ngoại tệ
- **Tác nhân (Actors):** Kế toán, Thủ quỹ, Khách hàng
- **Mục tiêu:** Thu hồi các khoản nợ có gốc ngoại tệ
- **Điều kiện tiên quyết (Preconditions):** Có số dư các TK 131,136... có gốc ngoại tệ
- **Luồng chính (Main Flow):**
  1. Khách hàng thanh toán nợ bằng ngoại tệ
  2. Thủ quỹ kiểm đếm theo tỷ giá thực tế tại thời điểm thu hồi
  3. Kế toán lập phiếu thu
  4. Hạch toán: Nợ TK 111(1112) theo tỷ giá thực tế / Nợ/Có TK 635 (chênh lệch tỷ giá) / Có TK liên quan theo tỷ giá ghi sổ trước đây
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 4] → Lãi tỷ giá: Có TK 515 / Lỗ tỷ giá: Nợ TK 635
- **Điều kiện hậu kiểm (Postconditions):** Ngoại tệ tại quỹ tăng, khoản nợ phải thu giảm, chênh lệch tỷ giá được ghi nhận
- **Định khoản:** Nợ 111(1112) + Nợ/Có 635/515 / Có 131,136...

---

### 📌 T19 — Xuất ngoại tệ mua vật tư, hàng hóa
- **Tác nhân (Actors):** Kế toán, Thủ quỹ, Nhà cung cấp
- **Mục tiêu:** Xuất ngoại tệ để thanh toán mua vật tư, hàng hóa, chi phí
- **Điều kiện tiên quyết (Preconditions):** Có hóa đơn mua hàng bằng ngoại tệ, có số dư ngoại tệ tại quỹ
- **Luồng chính (Main Flow):**
  1. Nhà cung cấp giao hàng và hóa đơn bằng ngoại tệ
  2. Kế toán kiểm tra hóa đơn
  3. Thủ quỹ xuất ngoại tệ thanh toán theo tỷ giá thực tế
  4. Hạch toán: Nợ TK liên quan (152,153,156,211,627,641,642...) theo tỷ giá thực tế / Nợ TK 133 (thuế GTGT) / Nợ/Có TK 635 (chênh lệch tỷ giá) / Có TK 111(1112) theo tỷ giá ghi sổ
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 4] → Lãi tỷ giá: Có TK 515 / Lỗ tỷ giá: Nợ TK 635
- **Điều kiện hậu kiểm (Postconditions):** Ngoại tệ tại quỹ giảm, hàng mua được ghi nhận
- **Định khoản:** Nợ 152,153,156,211,627,641,642 + Nợ 133 + Nợ/Có 635/515 / Có 111(1112)

---

### 📌 T20 — Bán ngoại tệ
- **Tác nhân (Actors):** Kế toán, Thủ quỹ, Người mua ngoại tệ
- **Mục tiêu:** Bán ngoại tệ để thu tiền mặt hoặc quy đổi sang VND
- **Điều kiện tiên quyết (Preconditions):** Có số dư ngoại tệ tại quỹ, có nhu cầu bán ngoại tệ
- **Luồng chính (Main Flow):**
  1. Người mua đề nghị mua ngoại tệ
  2. Thủ quỹ xuất ngoại tệ theo tỷ giá ghi sổ
  3. Kế toán lập phiếu thu tiền
  4. Hạch toán: Nợ TK 111(1111),131 theo giá bán thực tế / Nợ/Có TK 635 (chênh lệch tỷ giá) / Có TK 111(1112) theo tỷ giá ghi sổ
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 4] → Lãi tỷ giá: Có TK 515 / Lỗ tỷ giá: Nợ TK 635
- **Điều kiện hậu kiểm (Postconditions):** Ngoại tệ giảm, tiền VND hoặc khoản phải thu tăng
- **Định khoản:** Nợ 111(1111),131 + Nợ/Có 635/515 / Có 111(1112)

---

### 📌 T21 — Ứng trước cho nhà cung cấp bằng ngoại tệ
- **Tác nhân (Actors):** Kế toán, Thủ quỹ, Nhà cung cấp
- **Mục tiêu:** Ứng trước tiền cho nhà cung cấp bằng ngoại tệ
- **Điều kiện tiên quyết (Preconditions):** Có thỏa thuận ứng trước với nhà cung cấp, có số dư ngoại tệ
- **Luồng chính (Main Flow):**
  1. Kế toán kiểm tra và xác nhận hồ sơ ứng trước
  2. Thủ quỹ xuất ngoại tệ theo tỷ giá thực tế
  3. Hạch toán: Nợ TK liên quan (331,311,341...) theo tỷ giá ghi nhận nợ / Nợ/Có TK 635 (chênh lệch tỷ giá) / Có TK 111(1112) theo tỷ giá ghi sổ
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 3] → Lãi tỷ giá: Có TK 515 / Lỗ tỷ giá: Nợ TK 635
- **Điều kiện hậu kiểm (Postconditions):** Ngoại tệ giảm, khoản phải trả tăng
- **Định khoản:** Nợ 331,311,341 + Nợ/Có 635/515 / Có 111(1112)

---

### 📌 T22 — Thu tiền đặt trước của người mua bằng ngoại tệ
- **Tác nhân (Actors):** Kế toán, Thủ quỹ, Người mua
- **Mục tiêu:** Nhận tiền đặt trước từ người mua bằng ngoại tệ
- **Điều kiện tiên quyết (Preconditions):** Có thỏa thuận đặt trước từ người mua
- **Luồng chính (Main Flow):**
  1. Người mua đặt trước bằng ngoại tệ
  2. Thủ quỹ kiểm đếm theo tỷ giá thực tế tại thời điểm nhận
  3. Kế toán lập phiếu thu
  4. Hạch toán: Nợ TK 111(1112) theo tỷ giá thực tế / Có TK 131 theo tỷ giá thực tế tại thời điểm phát sinh
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 4] → Tỷ giá thay đổi khi giao hàng: Xử lý chênh lệch tỷ giá
- **Điều kiện hậu kiểm (Postconditions):** Ngoại tệ tăng, khoản phải thu tăng
- **Định khoản:** Nợ 111(1112) / Có 131

---

*Last Updated: April 2026*
*Source: docs/cash.md (tamkhoatech.vn)*
