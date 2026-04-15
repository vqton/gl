# 📋 NGHIỆP VỤ KẾ TOÁN BÁN HÀNG
*Based on: TT99/2025 & ketoanthienung.net*

---

## 📊 USE CASES OVERVIEW (S01-S06)

| ID | Name | Status | Account Codes |
|----|------|--------|------------|
| S01 | Bán hàng tiền mặt | ⚠️ Partial | 111 → 511, 33311 |
| S02 | Bán hàng chịu (công nợ) | ⚠️ Partial | 131 → 511, 33311 |
| S03 | Ghi nhận giá vốn hàng bán | ⚠️ Partial | 632 → 156/155 |
| S04 | Hàng bán bị trả lại | ❌ Not implemented | 5212 |
| S05 | Giảm giá hàng bán | ❌ Not implemented | 5211 |
| S06 | Chiết khấu thanh toán | ❌ Not implemented | 5213 |

---

## 📌 S01 — BÁN HÀNG TIỀN MẶT

### 📌 S01 - Bán hàng thu tiền ngay
- **Tác nhân (Actors):** Kế toán, thu ngân
- **Mục tiêu:** Ghi nhận doanh thu bán hàng khi khách thanh toán tiền mặt hoặc chuyển khoản ngay
- **Điều kiện tiên quyết (Preconditions):**
  - Hóa đơn VAT đã xuất
  - Đã thu tiền (tiền mặt/chuyển khoản)
  - Kỳ kế toán đang mở
- **Luồng chính (Main Flow):**
  1. Nhận hóa đơn bán hàng và phiếu thu
  2. Kiểm tra hóa đơn (mã số thuế, ngày, số tiền, VAT)
  3. Định khoản: Nợ 111/112 / Có 511 / Có 33311
  4. Cập nhật sổ cái và sổ kế toán chi tiết
  5. Lưu chứng từ vào hồ sơ
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 3] → Hóa đơn không hợp lệ: Yêu cầu xuất hóa đơn điều chỉnh
  - [Bước 3] → Sai tài khoản: Điều chỉnh trước khi ghi sổ
- **Điều kiện hậu kiểm (Postconditions):**
  - Sổ cái 111/112 tăng bằng số tiền thu
  - Sổ cái 511 ghi nhận doanh thu
  - Tổng Nợ = Tổng Có
- **Ghi chú/Tham chiếu:** TT99-Đ7 — Kế toán doanh thu

---

## 📌 S02 — BÁN HÀNG CHỊU (CÔNG NỢ)

### 📌 S02 - Bán chịu có xuất hóa đơn VAT
- **Tác nhân (Actors):** Kế toán, sales
- **Mục tiêu:** Ghi nhận doanh thu và công nợ phải thu khi bán chịu
- **Điều kiện tiên quyết (Preconditions):**
  - Hợp đồng kinh tế hoặc đơn đặt hàng
  - Hóa đơn VAT đã xuất
  - Khách hàng có mã số thuế hợp lệ
  - Xác định thời hạn thanh toán
- **Luồng chính (Main Flow):**
  1. Nhận hóa đơn bán hàng
  2. Kiểm tra điều khoản thanh toán (15/30/60 ngày)
  3. Định khoản: Nợ 131 / Có 511 / Có 33311
  4. Cập nhật sổ chi tiết công nợ (theo dõi theo từng khách hàng)
  5. Lập phiếu đòi nợ theo dõi
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 3] → Khách nợ quá hạn: Chuyển sang nợ quá hạn (2293)
  - [Bước 3] → Thanh toán trước hạn: Ghi nhận chiết khấu (5213)
- **Điều kiện hậu kiểm (Postconditions):**
  - Sổ cái 131 tăng (công nợ khách hàng)
  - Sổ chi tiết 131 theo dõi từng KH
  - Cập nhật báo cáo công nợ
- **Ghi chú/Tham chiếu:** TT99-Đ7 — Kế toán phải thu

---

## 📌 S03 — GHI NHẬN GIÁ VỐN HÀNG BÁN

### 📌 S03 - Ghi nhận giá vốn khi giao hàng
- **Tác nhân (Actors):** Kế toán, kho
- **Mục tiêu:** Ghi nhận chi phí giá vốn khi hàng được giao cho khách
- **Điều kiện tiênquyết (Preconditions):**
  - Phiếu xuất kho đã xuất
  - Hóa đơn bán hàng đã xuất (liên kết với phiếu xuất kho)
  - Đủ hàng tồn kho
- **Luồng chính (Main Flow):**
  1. Nhận phiếu xuất kho + hóa đơn bán hàng
  2. Kiểm tra số lượng, đơn giá
  3. Tính giá xuất kho (FIFO/bình quân)
  4. Định khoản: Nợ 632 / Có 156/155
  5. Cập nhật thẻ kho
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 3] → Hết hàng tồn: Báo cáo tồn kho âm
  - [Bước 3] → Giá thay đổi: Tính lại giá bình quân
- **Điều kiện hậu kiểm (Postconditions):**
  - Sổ cái 632 ghi nhận giá vốn
  - Thẻ kho cập nhật tồn kho
  - Lãi/lỗ gộng = Doanh thu - Giá vốn
- **Ghi chú/Tham chiếu:** TT99-Đ7 — Kế toán giá vốn

---

## 📌 S04 — HÀNG BÁN BỊ TRẢ LẠI

### 📌 S04 - Xử lý hàng bán bị trả lại
- **Tác nhân (Actors):** Kế toán, kinh doanh, kho
- **Mục tiêu:** Điều chỉnh doanh thu khi khách trả lại hàng
- **Điều kiện tiên quyết (Preconditions):**
  - Phiếu xuất kho gốc còn lưu
  - Hóa đơn bán gốc
  - Biên bản nghiệm thu hoặc lý do trả hàng
- **Luồng chính (Main Flow):**
  1. Nhận phiếu trả hàng + biên bản
  2. Kiểm tra lý do trả (lỗi do DN/Khách)
  3. Kiểm tra hàng nhập kho
  4. Định khoản điều chỉnh:
     - Nợ 5212 (giảm doanh thu)
     - Nợ 3331 (giảm VAT đầu ra)
     - Có 131 (nếu chưa thu)/111 (nếu đã thu)
  5. Điều chỉnh giá vốn (nếu đã ghi nhận):
     - Nợ 156/155 / Có 632
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 2] → Lỗi do khách: Chỉ điều chỉnh giảm
  - [Bước 2] → Lỗi do DN: Hoàn tiền hoặc đổi hàng mới
  - [Bước 4] → Đã khấu trừ thuế: Điều chỉnh kê khai
- **Điều kiện hậu kiểm (Postconditions):**
  - Doanh thu giảm (5212)
  - VAT đầu ra giảm (3331)
  - Giá vốn điều chỉnh (632)
  - Công nợ điều chỉnh (131)
- **Ghi chú/Tham chiếu:** Khoản 3, Điều 6, Thông tư 200/2014/TT-BTC

---

## 📌 S05 — GIẢM GIÁ HÀNG BÁN

### 📌 S05 - Giảm giá hàng bán do lỗi hàng hóa
- **Tác nhân (Actors):** Kế toán, kinh doanh
- **Mục tiêu:** Ghi nhận giảm giá cho khách do hàng kém chất lượng
- **Điều kiện tiên quyết (Preconditions):**
  - Hóa đơn bán hàng gốc
  - Biên bản kiểm tra hàng
  - Chấp nhận giảm giá từ quản lý
- **Luồng chính (Main Flow):**
  1. Nhận đề nghị giảm giá + biên bản
  2. Xác nhận lý do giảm (hàng lỗi, sai quy cách)
  3. Tính số tiền giảm (theo % hoặc cố định)
  4. Định khoản: Nợ 5211 / Có 131/111
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 3] → Giảm quá 20%: Xin phê duyệt cấp cao hơn
  - [Bước 4] → Đã có chiết khấu: Không giảm thêm
- **Điều kiện hậu kiểm (Postconditions):**
  - Doanh thu giảm qua 5211
  - Công nợ hoặc tiền mặt giảm tương ứng
- **Ghi chú/Tham chiếu:** Thông tư 200/2014 — Tài khoản 5211

---

## 📌 S06 — CHIẾT KHẤU THANH TOÁN

### 📌 S06 - Chiết khấu thanh toán cho khách trả trước
- **Tác nhân (Actors):** Kế toán, thu ngân
- **Mục tiêu:** Ghi nhận chiết khấu khi khách thanh toán trước hạn
- **Điều kiện tiên quyết (Preconditions):**
  - Hợp đồng có điều khoản chiết khấu (VD: thanh toán trong 10 ngày được 2% CK)
  - Khách thanh toán đủ trong thời hạn
- **Luồng chính (Main Flow):**
  1. Khách hàng thanh toán trước hạn
  2. Tính số tiền chiết khấu (số tiền × tỷ lệ)
  3. Định khoản:
     - Nợ 111 (số tiền thực thu)
     - Nợ 5213 (chiết khấu)
     - Có 131 (tổng cần thu)
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 2] → Khách không đủ hạn: Không được chiết khấu
  - [Bước 3] → Chiết khấu > 20%: Xem xét đặc biệt
- **Điều kiện hậu kiểm (Postconditions):**
  - 111: Số tiền thực nhận
  - 5213: Chiết khấu đ�� giảm
  - 131: Công nợ đã thanh toán đủ
- **Ghi chú/Tham chiếu:** TT99 — Chi phí tài chính

---

## 📊 CÁC ĐỊNH KHOẢN MỞ RỘNG

### Bán hàng trả góp
```
Nợ 131    : Tổng phải thu
Có 511   : Doanh thu gốc
Có 33311  : VAT đầu ra

Nợ 635    : Chi phí lãi trả góp (phần chênh lệch)
```

### Bán đại lý
```
Đại lý bán đúng giá:
Nợ 157   : Hàng gửi đại lý
Có 156  : Xuất kho

Khi đại lý bán:
Nợ 641   : Chi phí hoa hồng
Có 111   : Thanh toán

Đại lý bán chậm trả:
Nợ 1388  : Phải thu khác
```

### Hàng về trước hóa đơn về sau
```
Khi nhận hàng (chưa có hóa đơn):
Nợ 151   : Hàng mua đang đi đường
Có 331   : Phải trả người bán

Khi nhận hóa đơn:
Nợ 156/152: Ghi nhận hàng nhập
Nợ 1331  : VAT đầu vào
Có 151   : Đối trừ 151
Có 331   : Số còn lại
```

### Khuyến mãi, quảng cáo
```
Tặng hàng (không thu tiền):
Nợ 6412  : Chi phí khuyến mãi
Có 156   : Giá vốn hàng tặng

Thu tiền một phần:
Nợ 111   : Tiền thu
Nợ 6412  : Phần tặng thêm (thanh toán cho đơn vị KM)
Có 511   : Doanh thu chính
Có 33311 : VAT
```

---

## 📋 SỔ SÁCH LIÊN QUAN

| Sổ | Mục đích |
|-----|---------|
| Sổ cái 111, 112 | Tiền mặt, tiền gửi ngân hàng |
| Sổ cái 131 | Phải thu khách hàng |
| Sổ cái 511, 512 | Doanh thu bán hàng |
| Sổ cái 632 | Giá vốn hàng bán |
| Sổ chi tiết 131 | Theo dõi công nợ từng KH |
| Thẻ kho | Theo dõi tồn kho |

---

## 📌 TEST CASES (TDD)

```
S01_CashSales_Balanced
S01_CashSales_WithVAT
S02_CreditSales_UpdateAging
S02_CreditSales_OverdueFlag
S03_COGS_FIFO
S03_COGS_WeightedAverage
S04_SalesReturn_ReduceRevenue
S04_SalesReturn_AdjustCOGS
S05_SalesDiscount_ValidAmount
S06_PaymentDiscount_CalculatedCorrectly
```

---

*Document created: April 2026*  
*Based on: TT99/2025 & ketoanthienung.net*