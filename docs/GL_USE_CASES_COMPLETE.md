# GL ACCOUNTING SYSTEM — COMPLETE USE CASES
*Based on: TT99/2025 | Consolidated: April 2026*

---

## 📊 MODULES OVERVIEW

| Module | Code | Account Codes | Status | Implementation |
|--------|------|--------------|--------|-----------------|
| Sales | S01-S06 | 511, 131, 632, 156 | ✅ Complete | SalesService.cs |
| Purchase | P01-P05 | 156, 152, 331, 1331 | ✅ Complete | PurchaseService.cs |
| Cash & Bank | T01-T22 | 111, 112, 341 | ✅ Complete | CashService.cs |
| Bank Transactions | B01-B08 | 112, 311, 635 | ✅ Complete | BankService.cs |
| Tax | X01-X05 | 3331, 1331 | ✅ Complete | TaxService.cs |
| Fixed Assets | A01-A06 | 211, 214, 641 | ✅ Complete | FixedAssetService.cs |
| Payroll | L01-L07 | 334, 338 | ✅ Complete | PayrollService.cs |
| Period Closing | G01-G04 | 911, 4212 | ✅ Complete | TransactionService.cs |
| Inventory | I01-I07 | 156, 152, 153 | ✅ Complete | InventoryService.cs |
| **GL Central Posting** | **G05** | All accounts | 📌 Next | **New Service** |
| **Cost Accounting** | **C01** | 154, 631 | 📌 Next | **New Service** |
| **Subsidiary Ledgers** | **S01-S03** | 131, 331, 156 | 📌 Next | **New Service** |

---

## 📋 PART 1: SALES (S01-S06) ✅

### S01 — Bán hàng tiền mặt
- **Định khoản:** Nợ 111/112 / Có 511 / Có 33311

### S02 — Bán hàng chịu (công nợ)
- **Định khoản:** Nợ 131 / Có 511 / Có 33311

### S03 — Ghi nhận giá vốn hàng bán
- **Định khoản:** Nợ 632 / Có 156/155

### S04 — Hàng bán bị trả lại
- **Định khoản:** Nợ 5212 / Nợ 33311 / Có 131

### S05 — Giảm giá hàng bán
- **Định khoản:** Nợ 5211 / Có 131

### S06 — Chiết khấu thanh toán
- **Định khoản:** Nợ 111 / Nợ 5213 / Có 131

---

## 📋 PART 2: PURCHASE (P01-P05) ✅

### P01 — Mua hàng trong nước nhập kho
- **Định khoản:** Nợ 156/152/153 / Nợ 1331 / Có 331/111/112

### P02 — Mua hàng không qua kho
- **Định khoản:** Nợ 621/623/627/641 / Nợ 1331 / Có 331

### P03 — Chi phí mua hàng (vận chuyển)
- **Định khoản:** Nợ 1562 / Nợ 1331 / Có 331

### P04 — Chiết khấu thương mại & Giảm giá
- **Định khoản:** Nợ 331 / Có 156 / Có 1331

### P05 — Trả lại hàng mua
- **Định khoản:** Nợ 331 / Có 156 / Có 1331

---

## 📋 PART 3: CASH & BANK (T01-T22) ✅

| T# | Use Case | Định khoản |
|----|----------|------------|
| T01 | Rút tiền ngân hàng về quỹ | Nợ 111 / Có 112 |
| T02 | Thu tiền bán hàng nhập quỹ | Nợ 111 / Có 511 + Có 333 |
| T03 | Chi tiền mua hàng | Nợ 156,133 / Có 111 |
| T04 | Nộp tiền vào ngân hàng | Nợ 112 / Có 111 |
| T05 | Chi lương tiền mặt | Nợ 334 / Có 111 |
| T06 | Chi tạm ứng | Nợ 141 / Có 111 |
| T07 | Thu hồi nợ phải thu | Nợ 111 / Có 131 |
| T08 | Thừa tiền mặt (kiểm kê) | Nợ 111 / Có 338 |
| T09 | Thiếu tiền mặt (kiểm kê) | Nợ 138 / Có 111 |
| T10 | Nhận vốn góp | Nợ 111 / Có 411 |
| T11 | Nhận ký quỹ | Nợ 111 / Có 344 |
| T12 | Hoàn trả ký quỹ | Nợ 344 / Có 111 |
| T13 | Chi phí kinh doanh | Nợ 6xx,133 / Có 111 |
| T14 | Đi vay | Nợ 111 / Có 341/311 |
| T15 | Bán đầu tư | Nợ 111 / Có 121 + 515/635 |
| T16 | Mua đầu tư | Nợ 121 / Có 111 |
| T17 | Thu ngoại tệ (bán hàng) | Nợ 1112 / Có 511 |
| T18 | Thu hồi nợ ngoại tệ | Nợ 1112 / Có 131 |
| T19 | Xuất ngoại tệ mua hàng | Nợ 156 / Có 1112 |
| T20 | Bán ngoại tệ | Nợ 1111 / Có 1112 |
| T21 | Ứng trước NCC ngoại tệ | Nợ 331 / Có 1112 |
| T22 | Thu tiền đặt trước (ngoại tệ) | Nợ 1112 / Có 131 |

---

## 📋 PART 4: BANK (B01-B08) ✅

### B01 — Đối chiếu sao kê ngân hàng
- **Định khoản:** Điều chỉnh: Nợ/Có 112 / Nợ/Có 638,811

### B02 — Chuyển khoản thanh toán cho NCC
- **Định khoản:** Nợ 331 / Có 112

### B03 — Nhận giải ngân vay ngắn hạn
- **Định khoản:** Nợ 112 / Có 311

### B04 — Trả nợ vay ngân hàng (gốc + lãi)
- **Định khoản:** Nợ 311 + 635 / Có 112

### B05 — Hạch toán phí ngân hàng
- **Định khoản:** Nợ 641,642 / Có 112

### B06 — Hạch toán lãi tiền gửi ngân hàng
- **Định khoản:** Nợ 112 / Có 515

### B07 — Mở LC (Letter of Credit)
- **Định khoản:** Nợ 144 / Có 112

### B08 — Đối chiếu ngoại hối (FX Revaluation)
- **Định khoản:** Lãi: Nợ 112 / Có 413 | Lỗ: Nợ 635 / Có 112

---

## 📋 PART 5: INVENTORY (I01-I07) ✅

### I01 — Nhập kho hàng mua
- **Định khoản:** Nợ 156/152/153 / Nợ 1331 / Có 331

### I02 — Xuất kho hàng bán/sử dụng
- **Định khoản:** Nợ 632/621 / Có 156/152/155

### I03 — Chuyển kho nội bộ
- **Định khoản:** Có 156(A) / Nợ 156(B)

### I04 — Kiểm kê hàng tồn kho
- **Định khoản:** Thừa: Nợ 156 / Có 338 | Thiếu: Nợ 138 / Có 156

### I05 — Đánh giá hàng tồn kho cuối kỳ
- **Định khoản:** Nợ 632 / Có 2294

### I06 — Trích lập/hoàn nhập dự phòng giảm giá hàng tồn kho
- **Định khoản:** Trích: Nợ 632 / Có 2294 | Hoàn nhập: Nợ 2294 / Có 632

### I07 — Xử lý hàng tồn kho hư hỏng, hết hạn
- **Định khoản:** Nợ 811 / Có 156

---

## 📋 PART 6: TAX (X01-X05) ✅

### X01 — Kê khai VAT đầu vào
- **Định khoản:** Nợ 1331 / Có 3311

### X02 — Kê khai VAT đầu ra
- **Định khoản:** Nợ 511 / Có 33311

### X03 — Khấu trừ thuế TNCN
- **Định khoản:** Nợ 334 / Có 3335

### X04 — Quyết toán thuế TNDN
- **Định khoản:** Nợ 8211 / Có 3334

### X05 — Hóa đơn điện tử
- **Định khoản:** Nợ 131 / Có 511 + 33311

---

## 📋 PART 7: FIXED ASSETS (A01-A06) ✅

### A01 — Thêm TSCĐ mới
- **Định khoản:** Nợ 211 / Nợ 1332 / Có 331/111

### A02 — Tính khấu hao
- **Định khoản:** Nợ 627/641/642 / Có 214

### A03 — Chuyển giao TSCĐ
- **Định khoản:** Nợ 211(bên nhận) / Có 211(bên giao) + 214

### A04 — Thanh lý TSCĐ
- **Định khoản:** Nợ 214 / Nợ 811 / Có 211 + 111

### A05 — Đánh giá lại TSCĐ
- **Định khoản:** Nợ 211 / Có 412

### A06 — Kiểm kê TSCĐ
- **Định khoản:** Thừa: Nợ 211 / Có 338 | Thiếu: Nợ 138 / Có 211

---

## 📋 PART 8: PAYROLL (L01-L07) ✅

### L01 — Quản lý hợp đồng lao động
- **Định khoản:** Nợ 642 / Có 334

### L02 — Tính lương tháng
- **Định khoản:** Nợ 622 / Có 334

### L03 — Tính tăng ca
- **Định khoản:** Nợ 622 / Có 334

### L04 — Quản lý nghỉ phép
- **Định khoản:** Nợ 334 / Có 622

### L05 — Trợ cấp thôi việc
- **Định khoản:** Nợ 642 / Có 334

### L06 — Kê khai BHXH
- **Định khoản:** Nợ 622 / Có 338

### L07 — Thang bảng lương
- **Định khoản:** Nợ 622 / Có 334

---

## 📋 PART 9: PERIOD CLOSING (G01-G04) ✅

### G01 — Kết chuyển doanh thu (511→911)
- **Định khoản:** Nợ 511+515+711 / Có 911

### G02 — Kết chuyển chi phí (6xx→911)
- **Định khoản:** Nợ 911 / Có 632+635+641+642+811

### G03 — Kết chuyển lợi nhuận (911→4212)
- **Định khoản:** Nợ 911 / Có 4212 (Lãi) | Nợ 4212 / Có 911 (Lỗ)

### G04 — Phân bổ chi phí trả trước (242)
- **Định khoản:** Nợ 627 / Có 242

---

## 📋 PART 10: NEW MODULES (TODO)

### 📌 G05 — GL Central Posting Service
**Mục tiêu:** Tổng hợp tất cả bút toán từ các module vào sổ cái tổng hợp

**Use Cases:**
1. **G05a** — Tổng hợp bút toán cuối ngày
2. **G05b** — Tạo file xuất sổ cái
3. **G05c** — Kiểm tra số dư cuối ngày
4. **G05d** — Báo cáo chênh lệch

**Định khoản:** Aggregate all transactions → General Ledger

---

### 📌 C01 — Cost Accounting (TK 154/631)
**Mục tiêu:** Tính giá thành sản phẩm theo phương pháp chi phí SXKD dở dang

**Use Cases:**
1. **C01a** — Cập nhật chi phí sản xuất trong kỳ (621, 622, 627)
2. **C01b** — Kết chuyển chi phí SXKD dở dang (154→631)
3. **C01c** — Tính giá thành theo phương pháp bình quân
4. **C01d** — Tính giá thành theo phương pháp FIFO
5. **C01e** — Phân bổ chi phí SXC cho sản phẩm

**Định khoản:**
- Nợ 154 / Có 621 (Chi phí NVL trực tiếp)
- Nợ 154 / Có 622 (Chi phí nhân công trực tiếp)
- Nợ 154 / Có 627 (Chi phí SXC)
- Nợ 631 / Có 154 (Kết chuyển giá thành)

---

### 📌 S01 — Subsidiary Ledger: Accounts Receivable (131)
**Mục tiêu:** Theo dõi công nợ phải thu chi tiết theo từng khách hàng

**Use Cases:**
1. **S01a** — Tạo phiếu công nợ phải thu
2. **S01b** — Cập nhật thanh toán
3. **S01c** — Tính tuổi nợ (aging report)
4. **S01d** — Chuyển nợ quá hạn
5. **S01e** — Trích dự phòng nợ phải thu khó đòi

**Định khoản:**
- Nợ 131 / Có 511 (Bán chịu)
- Nợ 111 / Có 131 (Thu tiền)
- Nợ 138 / Có 131 (Nợ quá hạn)
- Nợ 632 / Có 2293 (Dự phòng)

---

### 📌 S02 — Subsidiary Ledger: Accounts Payable (331)
**Mục tiêu:** Theo dõi công nợ phải trả chi tiết theo từng nhà cung cấp

**Use Cases:**
1. **S02a** — Tạo phiếu công nợ phải trả
2. **S02b** — Cập nhật thanh toán
3. **S02c** — Tính tuổi nợ
4. **S02d** — Xử lý chiết khấu thanh toán

**Định khoản:**
- Nợ 156 / Có 331 (Mua chịu)
- Nợ 331 / Có 111 (Trả tiền)
- Nợ 331 / Có 635 (Chiết khấu được hưởng)

---

### 📌 S03 — Subsidiary Ledger: Inventory (156)
**Mục tiêu:** Theo dõi chi tiết tồn kho theo từng mặt hàng

**Use Cases:**
1. **S03a** — Cập nhật thẻ kho
2. **S03b** — Tính giá xuất kho (FIFO/BQ)
3. **S03c** — Báo cáo tồn kho chi tiết
4. **S03d** — Cảnh báo tồn kho âm

**Định khoản:**
- Nợ 156 / Có 331 (Nhập kho)
- Nợ 632 / Có 156 (Xuất kho)

---

## 📋 FILE REFERENCE

| Document | Location |
|----------|----------|
| Complete Use Cases | This document |
| Sales Use Cases | docs/use_cases/sales_use_cases.md |
| Purchase Use Cases | docs/use_cases/purchase_use_cases.md |
| Cash Use Cases | docs/use_cases/cash_use_cases.md |
| Bank Use Cases | docs/use_cases/bank_use_cases.md |
| Inventory Use Cases | docs/use_cases/inventory_use_cases.md |
| Payroll Use Cases | docs/use_cases/laodong_tienluong.md |
| Core TT99/2025 | docs/core_use_cases_TT99_2025_updated.md |

---

*Last Updated: April 2026*
*Consolidated from: Sales, Purchase, Cash, Bank, Inventory, Tax, Fixed Asset, Payroll, Period Closing modules*