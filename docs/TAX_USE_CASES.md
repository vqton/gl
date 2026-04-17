# TAX MANAGEMENT USE CASES (X01-X05)
*Based on TT99/2025*

---

## X01: KÊ KHAI THUẾ GTGT ĐẦU VÀO

| Field | Description |
|-------|-------------|
| Actor | Kế toán thuế |
| Input | Hóa đơn mua hàng, phiếu chi |
| Account | 1331 - Thuế GTGT được khấu trừ |

### Business Rules
- Hóa đơn hợp lệ theo Nghị định 123/2014/NĐ-CP
- Không vượt quá 6 tháng kể từ ngày lập hóa đơn
- Tỷ lệ khấu trừ: 10% (hoặc 8%/5% theo ngành nghề)

### Định khoản
```
Nợ 1331 - Thuế GTGT được khấu trừ
Có 331 - Phải trả cho người bán (nếu chưa trả)
Có 111 - Tiền mặt (nếu đã trả)
```

---

## X02: KÊ KHAI THUẾ GTGT ĐẦU RA

| Field | Description |
|-------|-------------|
| Actor | Kế toán thuế |
| Input | Hóa đơn bán hàng |
| Account | 33311 - Thuế GTGT đầu ra |

### Định khoản
```
Nợ 111, 112 - Tiền nhận được
Có 511 - Doanh thu bán hàng
Có 33311 - Thuế GTGT đầu ra
```

---

## X03: KHẤU TRỪ THUẾ TNCN

| Field | Description |
|-------|-------------|
| Actor | Kế toán |
| Input | Hợp đồng lao động, lương |
| Account | 3335 - Thuế TNCN |

### Lũy tiến thuế TNCN (2024)
| Thu nhập tính thuế (VND) | Thuế suất |
|--------------------------|------------|
| Đến 5 triệu | 5% |
| 5-10 triệu | 10% |
| 10-18 triệu | 15% |
| 18-32 triệu | 20% |
| 32-52 triệu | 25% |
| 52-80 triệu | 30% |
| Trên 80 triệu | 35% |

---

## X04: QUYẾT TOÁN THUẾ TNDN

| Field | Description |
|-------|-------------|
| Actor | Kế toán |
| Account | 8211 - Thuế TNDN |

### TNDN Rate (2024)
- Doanh nghiệp thông thường: 20%
- Doanh nghiệp công nghệ: 17% (3 năm đầu)
- Doanh nghiệp nông nghiệp: 15%

---

## X05: HÓA ĐƠN ĐIỆN TỬ (EI01-EI07)

See: `E_INVOICE_USE_CASES.md`

---

## IMPLEMENTATION

**Service:** `TaxService.cs`
- Methods: 8
- Tests: 12 passing

---

*Last Updated: April 2026*