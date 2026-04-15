# 📋 NGHIỆP VỤ KẾ TOÁN MUA HÀNG
*Based on: TT99/2025 & MISA AMIS*

---

## 📊 USE CASES OVERVIEW (P01-P05)

| ID | Name | Status | Account Codes |
|----|------|--------|------------|
| P01 | Mua hàng hóa trong nước nhập kho | ❌ Not implemented | 156, 152, 1331, 331 |
| P02 | Mua hàng trong nước không qua kho | ❌ Not implemented | 621, 627, 641 |
| P03 | Chi phí mua hàng (vận chuyển) | ❌ Not implemented | 1562, 331 |
| P04 | Chiết khấu TM & Giảm giá | ❌ Not implemented | 521, 331 |
| P05 | Trả lại hàng mua | ❌ Not implemented | 156, 1331, 331 |

---

## 📌 P01 — MUA HÀNG HÓA TRONG NƯỚC NHẬP KHO

### 📌 P01a - Hàng hóa và hóa đơn cùng về
- **Tác nhân (Actors):** Kế toán, thủ kho
- **Mục tiêu:** Ghi nhận hàng mua vào kho khi có đủ hóa đơn và hàng
- **Điều kiện tiên quyết (Preconditions):**
  - Hóa đơn VAT từ nhà cung cấp
  - Phiếu nhập kho đã xuất
  - Hàng đã nhập kho đầy đủ
- **Luồng chính (Main Flow):**
  1. Nhận hóa đơn + phiếu nhập kho
  2. Kiểm tra số lượng, đơn giá, thuế
  3. Định khoản: Nợ 156/152/153 / Nợ 1331 / Có 111/112/331
  4. Cập nhật thẻ kho
- **Luồng thay thế/Ngoại lệ (Alternate/Exception Flows):**
  - [Bước 3] → Hàng thiếu: Lập biên bản, báo cáo
  - [Bước 3] → Hóa đơn sai: Yêu cầu xuất hóa đơn điều chỉnh
- **Điều kiện hậu kiểm (Postconditions):**
  - 156/152 tăng theo giá trị hàng
  - 1331 tăng (VAT đầu vào)
  - 331 tăng (công nợ phải trả)
- **Ghi chú/Tham chiếu:** MISA - Section 4.1

---

### 📌 P01b - Hóa đơn về trước hàng về sau
- **Tác nhân (Actors):** Kế toán
- **Mục tiêu:** Ghi nhận hàng đang đi đường
- **Luồng chính (Main Flow):**
  1. Nhận hóa đơn trước, hàng chưa về
  2. Định khoản: Nợ 151 / Nợ 1331 / Có 331
  3. Chờ hàng về nhập kho
- **Luồng thay thế:**
  - [Bước 3] → Hàng không về: Theo dõi đến cuối tháng
  - [Bước 3] → Hàng về thiếu: Điều chỉnh 151
- **Điều kiện hậu kiểm (Postconditions):** 151 theo dõi hàng đang đi đường
- **Ghi chú/Tham chiếu:** MISA - Section 4.1b

---

### 📌 P01c - Hàng về trước hóa đơn về sau
- **Tác nhân (Actors):** Kế toán, thủ kho
- **Mục tiêu:** Ghi nhận nhập kho tạm tính
- **Luồng chính (Main Flow):**
  1. Hàng về, chưa có hóa đơn
  2. Nhập kho theo giá ước tính
  3. Định khoản: Nợ 156/152 / Có 331 (tạm)
  4. Khi nhận hóa đơn: Điều chỉnh theo giá thực tế
- **Luồng thay thế:**
  - [Bước 4] → Giá thay đổi: Điều chỉnh chênh lệch
- **Điều kiện hậu kiểm (Postconditions):** Giá trị 156/152 theo giá thực tế
- **Ghi chú/Tham chiếu:** MISA - Section 4.1c

---

## 📌 P02 — MUA HÀNG KHÔNG QUA KHO

### 📌 P02a - Mua hàng sử dụng ngay
- **Tác nhân (Actors):** Kế toán
- **Mục tiêu:** Ghi nhận mua hàng không qua kho, dùng ngay cho SXKD
- **Luồng chính (Main Flow):**
  1. Nhận hóa đơn mua hàng dùng ngay
  2. Định khoản: Nợ 621/623/627/641 / Nợ 1331 / Có 111/112/331
  3. Không qua 156/152
- **Điều kiện hậu kiểm (Postconditions):** Chi phí tăng, không có tồn kho
- **Ghi chú/Tham chiếu:** MISA - Section 4.2

---

### 📌 P02b - Mua hàng chuyển thẳng cho khách (bán đại lý)
- **Tác nhân (Actors):** Kế toán
- **Mục tiêu:** Ghi nhận mua hàng chuyển thẳng cho bên thứ ba
- **Luồng chính (Main Flow):**
  1. Nhận hóa đơn mua hàng
  2. Định khoản: Nợ 157 / Nợ 1331 / Có 111/112/331
  3. Chuyển giao cho đại lý
- **Điều kiện hậu kiểm (Postconditions):** 157 theo dõi hàng gửi bán
- **Ghi chú/Tham chiếu:** MISA - Section 4.2

---

## 📌 P03 — CHI PHÍ MUA HÀNG

### 📌 P03 - Chi phí vận chuyển, bảo quản
- **Tác nhân (Actors):** Kế toán
- **Mục tiêu:** Tính chi phí mua hàng vào giá trị hàng nhập kho
- **Điều kiện tiên quyết (Preconditions):** Có hóa đơn vận chuyển/bảo quản
- **Luồng chính (Main Flow):**
  1. Nhận hóa đơn chi phí vận chuyển
  2. Tính phân bổ chi phí theo lô hàng
  3. Định khoản: Nợ 1562 (chi phí mua hàng) / Nợ 1331 / Có 111/331
  4. Kết chuyển vào giá 156: Nợ 156 / Có 1562
- **Luồng thay thế:**
  - [Bước 3] → Chi phí nhỏ: Ghi nhận trực tiếp vào 641
- **Điều kiện hậu kiểm (Postconditions):** Giá trị 156 bao gồm chi phí
- **Ghi chú/Tham chiếu:** MISA - Section 4.3

---

## 📌 P04 — CHIẾT KHẤU THƯƠNG MẠI & GIẢM GIÁ

### 📌 P04a - Chiết khấu thương mại (CKTM)
- **Tác nhân (Actors):** Kế toán
- **Mục tiêu:** Ghi nhận CKTM khi mua đạt doanh số
- **Luồng chính (Main Flow):**
  1. Nhận hóa đơn chiết khấu từ NCC
  2. Định khoản: Nợ 331 / Có 156 (giảm giá) / Có 1331 (giảm VAT)
  3. Điều chỉnh thẻ kho
- **Luồng thay thế:**
  - [Bước 3] → Đã xuất kho: Điều chỉnh giá xuất
- **Điều kiện hậu kiểm (Postconditions):** Giá trị 156 giảm
- **Ghi chú/Tham chiếu:** MISA - Section 4.4

---

### 📌 P04b - Giảm giá hàng mua
- **Tác nhân (Actors):** Kế toán
- **Mục tiêu:** Ghi nhận giảm giá do hàng kém chất lượng
- **Luồng chính (Main Flow):**
  1. Nhận hóa đơn điều chỉnh giảm
  2. Định khoản: Nợ 331 / Có 156 / Có 1331
- **Luồng thay thế:**
  - [Bước 2] → Đã bán: Điều chỉnh giá vốn
- **Điều kiện hậu kiểm (Postconditions):** 156 giảm, thuế giảm
- **Ghi chú/Tham chiếu:** MISA - Section 4.4

---

## 📌 P05 — TRẢ LẠI HÀNG MUA

### 📌 P05 - Trả lại hàng mua cho nhà cung cấp
- **Tác nhân (Actors):** Kế toán, thủ kho
- **Mục tiêu:** Ghi nhận hàng mua trả lại do lỗi/hư hỏng
- **Điều kiện tiên quyết (Preconditions):**
  - Biên bản trả hàng
  - Hóa đơn mua gốc còn hiệu lực
- **Luồng chính (Main Flow):**
  1. Lập phiếu xuất kho trả hàng
  2. Xuất hóa đơn điều chỉnh (nếu đã nhận)
  3. Định khoản: Nợ 331 / Có 156 / Có 1331
  4. Cập nhật thẻ kho
- **Luồng thay thế:**
  - [Bước 3] → Chưa thanh toán: Giảm công nợ 331
  - [Bước 3] → Đã thanh toán: Thu tiền hoàn lại
- **Điều kiện hậu kiểm (Postconditions):**
  - 156 giảm (nhập kho âm)
  - 1331 giảm (điều chỉnh VAT)
  - 331 giảm
- **Ghi chú/Tham chiếu:** MISA - Section 4.5

---

## 📌 P06 — MUA HÀNG TRẢ CHẬM, TRẢ GÓP

### 📌 P06 - Mua hàng trả góp
- **Tác nhân (Actors):** Kế toán
- **Mục tiêu:** Ghi nhận mua hàng trả chậm với lãi suất
- **Luồng chính (Main Flow):**
  1. Nhận hóa đơn mua hàng trả góp
  2. Tách gốc và lãi trả góp
  3. Định khoản: Nợ 156 (gốc) / Nợ 242 (lãi trả trước) / Có 331
  4. Hàng tháng: Phân bổ lãi = Nợ 635 / Có 242
- **Luồng thay thế:**
  - [Bước 4] → Lãi tính vào giá: Nợ 156 / Có 242
- **Điều kiện hậu kiểm (Postconditions):**
  - 156 ghi nhận theo giá trị gốc
  - 242 theo dõi lãi phân bổ
- **Ghi chú/Tham chiếu:** MISA - Section 4.6

---

## 📊 CÁC ĐỊNH KHOẢN MỞ RỐNG

### Mua hàng nhập khẩu
```
Nợ 156/152    : Giá mua + Thuế NK
Nợ 1331       : Thuế GTGT (nếu khấu trừ)
Có 112       : Thanh toán qua NH
Có 3333      : Thuế xuất nhập khẩu
Có 3332      : Thuế TTĐB (nếu có)
```

### Mua hàng chiết khấu thanh toán (được hưởng)
```
Nợ 111/112   : Số tiền thực nhận
Nợ 635       : Chiết khấu được hưởng
Có 331       : Tổng phải trả
```

---

## 📋 SỔ SÁCH LIÊN QUAN

| Sổ | Mục đích |
|----|---------|
| Sổ cái 151 | Hàng đang đi đường |
| Sổ cái 152 | Nguyên vật liệu |
| Sổ cái 153 | Công cụ dụng cụ |
| Sổ cái 156 | Hàng hóa |
| Sổ cái 331 | Phải trả người bán |
| Sổ cái 133 | Thuế GTGT |
| Thẻ kho | Theo dõi tồn kho |
| Sổ chi tiết 331 | Công nợ theo từng NCC |

---

## 📌 TEST CASES (TDD)

```
P01a_PurchaseWithInvoice_Balanced
P01a_PurchaseWithInvoice_WithVAT
P01b_PurchaseInvoiceFirst_Track151
P01c_PurchaseGoodsFirst_TempPrice
P02_PurchaseDirectToCost_NoInventory
P03_PurchaseWithFreight_IncludeInCost
P04a_TradeDiscount_Applied
P04b_PurchaseDiscount_Applied
P05_PurchaseReturn_ReducePayable
P06_InstallmentPurchase_SplitInterest
```

---

*Document created: April 2026*  
*Based on: MISA AMIS, TT99/2025*