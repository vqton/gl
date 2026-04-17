# GL SYSTEM - GAP ANALYSIS
*April 2026 | Consolidated from use case analysis*

---

## 1. COVERAGE MATRIX

| Module | Use Cases | Implemented | Missing/Gap | Priority |
|--------|----------|-------------|-------------|------------|
| COA | COA-01 to COA-09 | 9 | None | - |
| Sales | S01-S06 | 6 | None | - |
| Purchase | P01-P05 | 5 | None | - |
| Cash | T01-T22 | 22 | None | - |
| Bank | B01-B08 | 8 | None | - |
| Inventory | I01-I07 | 7 | None | - |
| Inventory Costing | I05a-I05f | 6 | None | ✅ NEW |
| Fixed Assets | A01-A06 | 6 | None | - |
| Payroll | L01-L07 | 7 | None | - |
| Tax | X01-X05 | 5 | None | - |
| **E-Invoice** | EI01-EI07 | 7 | Full flow | ✅ Implemented |
| **Audit Trail** | AT01-AT03 | 3 | Full flow | ✅ Implemented |
| **Period Locking** | PL01-PL03 | 3 | Full flow | ✅ Implemented |
| **Trial Balance** | TB | 1 | Full flow | ✅ Implemented |
| **Subsidiary Ledger** | SL-01 to SL-03 | 3 | Full flow | ✅ Implemented |
| **General Journal** | NKC | Full | None | ✅ Complete |

---

## 2. MISSING FLOWS - DETAILED SPECS

### 2.1 General Journal (NKC)

**Current Gap:** Only basic transaction flow, missing:
- Correction entries (bút toán điều chỉnh)
- Compound entries (bút toán hợp nhất)
- Recurring entries (bút toán định kỳ)
- Foreign currency entries
- Inter-company entries

**Missing UC: NKC-04** — Correction Entry
```
Actor: Kế toán
Trigger: Phát hiện sai sót sau khi ghi sổ
Flow:
  1. Xác định sai sót (sai tài khoản, sai số tiền)
  2. Lập bút toán điều chỉnh (thay thế hoặc bổ sung)
  3. Ghi chú vào chứng từ gốc
Rules:
  - Không xóa bút toán đã ghi
  - Bút toán điều chỉnh phải có số tham chiếu
```

**Missing UC: NKC-05** — Compound Entry
```
Actor: Kế toán
Trigger: Nhiều định khoản cùng ngày
Flow:
  1. Gom nhóm các bút toán cùng ngày
  2. Định khoản tổng hợp (Nợ tổng / Có tổng)
Rules:
  - Tổng Nợ = Tổng Có
  - Giữ nguyên chi tiết từng dòng
```

---

### 2.2 Trial Balance (Bảng CĐPS)

**Current Gap:** Not defined in detail

**Missing UC: TB-01** — Generate Trial Balance
```
Actor: Kế toán
Purpose: Tổng hợp số dư các tài khoản
Input: Period code (YYYY-MM)
Output: Bảng cân đối số phát sinh

Flow:
  1. Lấy số dư đầu kỳ các TK (lấy từ kỳ trước)
  2. Tính tổng phát sinh Nợ trong kỳ
  3. Tính tổng phát sinh Có trong kỳ
  4. Tính số dư cuối kỳ:
     - Tài khoản Nợ: SDĐK + PS Nợ - PS Có
     - Tài khoản Có: SDĐK + PS Có - PS Nợ
  5. Kiểm tra tổng cân đối:
     - Tổng SDĐK Nợ = Tổng SDĐK Có
     - Tổng PS Nợ = Tổng PS Có
     - Tổng SDCK Nợ = Tổng SDCK Có
  6. Xuất báo cáo

Rules:
  - Chỉ lấy TK có số dư hoặc phát sinh
  - TK 152-159: Tổng hợp theo nhóm
  - Ngoại tệ: Quy đổi VND theo tỷ giá cuối kỳ
```

---

### 2.3 Subsidiary Ledger (Sổ Chi Tiết)

**Current Gap:** Not defined in detail

**Missing UC: SL-01** — AR Subsidiary Ledger (131)
```
Actor: Kế toán
Purpose: Theo dõi công nợ phải thu từng khách hàng
Account: 131

Flow:
  1. Mở sổ theo từng khách hàng
  2. Ghi các giao dịch phát sinh:
     - Bán chịu: Nợ 131 / Có 511
     - Thu tiền: Nợ 111,112 / Có 131
     - Trả hàng: Nợ 5311 / Có 131
     - Giảm giá: Nợ 5211 / Có 131
  3. Tính số dư cuối kỳ theo từng KH
  4. Phân loại theo k��� hạn:
     - Chưa đến hạn (1311)
     - Đến hạn (1312)
     - Quá hạn (1313)
  5. In báo cáo chi tiết theo KH
```

**Missing UC: SL-02** — AP Subsidiary Ledger (331)
```
Actor: Kế toán
Purpose: Theo dõi công nợ phải trả từng nhà cung cấp
Account: 331

Flow:
  1. Mở sổ theo từng NCC
  2. Ghi các giao dịch phát sinh:
     - Mua chịu: Nợ 156 / Có 331
     - Trả tiền: Nợ 331 / Có 111,112
     - Trả hàng: Nợ 331 / Có 156
     - Giảm giá: Nợ 331 / Có 156
  3. Tính số dư cuối kỳ theo từng NCC
  4. Phân loại theo kỳ hạn
```

**Missing UC: SL-03** — Inventory Subsidiary Ledger (156)
```
Actor: Kế toán, Thủ kho
Purpose: Theo dõi nhập xuất tồn kho theo từng mặt hàng
Account: 156

Flow:
  1. Mở thẻ kho theo từng mặt hàng
  2. Ghi các giao dịch:
     - Nhập kho: Nợ 156 / Có 331
     - Xuất kho: Nợ 632 / Có 156
     - Điều chỉnh: Nợ/Có 156
  3. Tính tồn kho theo giá xuất (FIFO/bình quân)
  4. In thẻ kho chi tiết
```

---

### 2.4 E-Invoice Integration

**Current Gap:** Not implemented

**Missing UC: EI-01** — Create E-Invoice
```
Actor: Kế toán
Trigger: Bán hàng xuất hóa đơn VAT
Source: Sales transaction

Flow:
  1. Extract sales data (customer, items, amounts)
  2. Map to e-invoice format (XML)
  3. Calculate VAT and totals
  4. Generate invoice number (format: AA/24X00001)
  5. Sign with digital certificate
  6. Send to TCT (Tax Authority)
  7. Store signed invoice

Rules:
  - Customer必须有 MST (tax code)
  - Items: mã hàng, tên, số lượng, đơn giá, thuế GTGT
  - Thời hạn gửi TCT: trước ngày 10 tháng sau
```

**Missing UC: EI-02** — Query E-Invoice Status
```
Actor: Kế toán
Purpose: Kiểm tra trạng thái hóa đơn từ TCT

Flow:
  1. Query by invoice number or tax period
  2. Check response status:
     - NEW: Chưa gửi
     - SENT: Đã gửi, chờ xử lý
     - APPROVED: Đã duyệt (có mã CQT)
     - ERROR: Lỗi, cần điều chỉnh
  3. Display invoice details
```

---

### 2.5 Audit Trail

**Current Gap:** Not implemented spec

**Missing UC: AT-01** — Log Transaction
```
Actor: System (auto)
Trigger: Any create/update/delete transaction

Flow:
  1. Capture: UserId, Timestamp, Action, Entity, OldValue, NewValue
  2. Store in AuditLog table
  3. Preserve for compliance (10 years minimum)

Fields:
  - AuditId (PK)
  - TransactionId
  - UserId
  - ActionType (CREATE/UPDATE/DELETE)
  - EntityType
  - EntityId
  - OldValue (JSON)
  - NewValue (JSON)
  - IpAddress
  - Timestamp
```

---

### 2.6 Period Locking

**Current Gap:** Not implemented

**Missing UC: PL-01** — Open Period
```
Actor: Kế toán trưởng
Purpose: Mở kỳ kế toán mới

Conditions:
  - Kỳ trước đã đóng (Closed status)
  - Không có giao dịch trong tương lai

Flow:
  1. Validate previous period is closed
  2. Create new period (YYYY-MM)
  3. Set status = OPEN
  4. Update fiscal year if January
```

**Missing UC: PL-02** — Close Period
```
Actor: Kế toán trưởng
Purpose: Đóng kỳ kế toán

Conditions:
  - All transactions posted
  - Trial balance balanced
  - No pending approvals

Flow:
  1. Lock all transactions (prevent new entries)
  2. Generate final reports
  3. Archive period data
  4. Set status = CLOSED
Rules:
  - Chỉ Kế toán trưởng được đóng
  - Không thể mở lại sau khi đóng
```

---

## 3. IMPLEMENTATION PRIORITY (Updated: April 2026)

| Priority | Module | Status | Notes |
|----------|--------|--------|-------|
| ✅ Complete | Trial Balance | Implemented via PeriodClosingService.GetTrialBalance() |
| ✅ Complete | Subsidiary Ledger | Implemented via SubsidiaryLedgerService |
| ✅ Complete | E-Invoice | Implemented via EInvoiceService (7 tests) |
| ✅ Complete | Period Locking | Implemented via PeriodLockingService (3 tests) |
| ✅ Complete | Audit Trail | Implemented via AuditTrailService |
| ✅ Complete | Inventory Costing | Implemented via InventoryCostingService (7 tests) |
| MEDIUM | General Journal (NKC) | Partial | Correction/compound entries |

---

## 4. ACTION ITEMS

- [ ] Implement TB service (Bảng CĐPS)
- [ ] Implement SL service (131, 331, 156)
- [ ] Define period locking service
- [ ] Define audit trail service
- [ ] Integrate e-invoice API

---

*Last Updated: April 2026*