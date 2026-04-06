# PROCESS FLOWS DOCUMENT
# Vietnamese Enterprise Accounting Software
# Compliant with Circular 99/2025/TT-BTC & Internal Control Standards

**Document Version:** 1.0
**Date:** April 2026
**Prepared by:** Lead BA Office
**Status:** Approved for Development

---

## TABLE OF CONTENTS

1.  Process Flow Notation & Standards
2.  Procure to Pay (P2P) - Mua hàng đến Thanh toán
3.  Order to Cash (O2C) - Đặt hàng đến Thu tiền
4.  Record to Report (R2R) - Ghi nhận đến Báo cáo
5.  Hire to Retire (H2R) - Tính lương và BHXH
6.  Electronic Invoice Lifecycle - Quy trình HĐĐT
7.  Fixed Asset Lifecycle - Quy trình TSCĐ
8.  Approval Matrix & Maker-Checker Controls

---

## 1. PROCESS FLOW NOTATION & STANDARDS

### 1.1 Diagram Types
- **Swimlane Flowchart:** Shows responsibilities across roles/departments.
- **Sequence Diagram:** Shows system interactions and API calls over time.

### 1.2 Role Definitions
| Role Code | Role Name | Vietnamese |
|-----------|-----------|------------|
| `REQ` | Requester (Người đề xuất) | Người đề xuất |
| `PUR` | Purchasing (Phòng mua hàng) | Phòng mua hàng |
| `WH` | Warehouse (Kho) | Thủ kho |
| `AP` | Accounts Payable (Kế toán công nợ phải trả) | Kế toán công nợ |
| `AR` | Accounts Receivable (Kế toán công nợ phải thu) | Kế toán công nợ |
| `CA` | Chief Accountant (Kế toán trưởng) | Kế toán trưởng |
| `CFO` | Chief Financial Officer | Giám đốc tài chính |
| `CSH` | Cashier (Thủ quỹ) | Thủ quỹ |
| `GL` | General Ledger (Kế toán tổng hợp) | Kế toán tổng hợp |
| `SYS` | System (Automated Processing) | Hệ thống tự động |

### 1.3 Compliance Notes
- All flows include **Maker-Checker** controls where required by Circular 99.
- All journal entries reference **Circular 99/2025/TT-BTC** account codes.
- Approval thresholds are configurable per enterprise policy.

---

## 2. PROCURE TO PAY (P2P) - MUA HÀNG ĐẾN THANH TOÁN

### 2.1 Swimlane Flowchart

```mermaid
flowchart TD
    subgraph PUR [Phòng Mua Hàng]
        A1[Tạo Yêu Cầu Mua Hàng] --> A2[Lập Đơn Đặt Hàng PO]
        A2 --> A3{Giá trị > Ngưỡng?}
        A3 -- Có --> A4[Trình CFO Duyệt PO]
        A3 -- Không --> A5[Gửi PO cho NCC]
        A4 --> A5
    end

    subgraph WH [Kho]
        A5 --> B1[Nhận Hàng từ NCC]
        B1 --> B2[Kiểm tra SL & Chất lượng]
        B2 --> B3{Đạt?}
        B3 -- Không --> B4[Lập Biên Bản Trả Hàng]
        B4 --> A5
        B3 -- Có --> B5[Lập Phiếu Nhập Kho 01-VT]
    end

    subgraph AP [Kế Toán Công Nợ]
        B5 --> C1[Nhận Hóa Đơn NCC]
        C1 --> C2[Đối chiếu 3 bên: PO-PNK-HĐ]
        C2 --> C3{Khớp?}
        C3 -- Không --> C4[Thông báo PUR/NCC xử lý]
        C4 --> C2
        C3 -- Có --> C5[Hạch toán: DK 152,156,211+1331 / Co 331]
        C5 --> C6[Lập Đề Nghị Thanh Toán]
    end

    subgraph CA [Kế Toán Trưởng]
        C6 --> D1{Kiểm tra chứng từ?}
        D1 -- Sai --> D2[Trả lại AP]
        D2 --> C6
        D1 -- Đúng --> D3[Phê duyệt thanh toán]
    end

    subgraph CSH [Thủ Quỹ]
        D3 --> E1[Nhận lệnh thanh toán]
        E1 --> E2{Phương thức?}
        E2 -- Tiền mặt --> E3[Lập Phiếu Chi 02-TT]
        E3 --> E4[Chi tiền & Ký nhận]
        E2 -- Chuyển khoản --> E5[Lệnh chuyển khoản ngân hàng]
        E5 --> E6[Xác nhận từ Bank]
    end

    subgraph SYS [Hệ Thống]
        E4 --> F1[Tự động ghi nhận bút toán: DK 331 / Co 111]
        E6 --> F2[Tự động ghi nhận bút toán: DK 331 / Co 112]
        F1 --> F3[Cập nhật trạng thái NCC: Đã thanh toán]
        F2 --> F3
    end
```

### 2.2 Key Controls
- **3-Way Match:** System blocks payment if PO ≠ Goods Receipt ≠ Invoice.
- **Segregation of Duties:** Purchaser cannot approve PO; AP cannot execute payment.
- **Tax Validation:** Input VAT (TK 1331) only recorded if e-invoice is valid on GDT portal.

---

## 3. ORDER TO CASH (O2C) - BÁN HÀNG ĐẾN THU TIỀN

### 3.1 Swimlane Flowchart

```mermaid
flowchart TD
    subgraph AR [Kế Toán Công Nợ Phải Thu]
        A1[Nhận đơn đặt hàng KH] --> A2[Kiểm tra hạn mức tín dụng KH]
        A2 --> A3{Đủ hạn mức?}
        A3 -- Không --> A4[Từ chối hoặc yêu cầu trả trước]
        A3 -- Có --> A5[Xác nhận đơn hàng]
    end

    subgraph WH [Kho]
        A5 --> B1[Kiểm tra tồn kho]
        B1 --> B2{Đủ hàng?}
        B2 -- Không --> B3[Thông báo AR & Sản xuất]
        B2 -- Có --> B4[Lập Phiếu Xuất Kho 02-VT]
        B4 --> B5[Giao hàng cho KH]
    end

    subgraph SYS [Hệ Thống]
        B5 --> C1[Tự động ghi nhận giá vốn: DK 632 / Co 156]
        C1 --> C2[Tạo dữ liệu Hóa đơn điện tử]
    end

    subgraph AR [Kế Toán Công Nợ Phải Thu]
        C2 --> D1[Kiểm tra thông tin HĐ]
        D1 --> D2[Ký số & Phát hành HĐ]
        D2 --> D3[Gửi HĐ cho KH]
        D3 --> D4[Hạch toán doanh thu: DK 131 / Co 511, 3331]
    end

    subgraph CSH [Thủ Quỹ]
        D4 --> E1[Nhận thanh toán từ KH]
        E1 --> E2{Phương thức?}
        E2 -- Tiền mặt --> E3[Lập Phiếu Thu 01-TT]
        E2 -- Chuyển khoản --> E4[Nhận sao kê Bank]
    end

    subgraph SYS [Hệ Thống]
        E3 --> F1[Tự động ghi nhận: DK 111 / Co 131]
        E4 --> F2[Tự động ghi nhận: DK 112 / Co 131]
        F1 --> F3[Cập nhật công nợ KH]
        F2 --> F3
    end
```

### 3.2 Key Controls
- **Credit Limit:** System blocks order if AR balance + New order > Credit limit.
- **Revenue Recognition:** Revenue (TK 511) recognized only when control transfers (delivery confirmation), not just invoice issuance.
- **VAT Timing:** VAT liability date determined by law (delivery vs payment vs invoice).

---

## 4. RECORD TO REPORT (R2R) - GHI NHẬN ĐẾN BÁO CÁO

### 4.1 Month-End Close Sequence

```mermaid
sequenceDiagram
    participant GL as Kế Toán Tổng Hợp
    participant Sub as Kế Toán Chi Tiết (AR/AP/Kho/TS)
    participant SYS as Hệ Thống
    participant CA as Kế Toán Trưởng
    participant CFO as CFO

    GL->>Sub: Thông báo khóa sổ kỳ hiện tại
    Sub->>Sub: Rà soát chứng từ tồn đọng
    Sub->>GL: Xác nhận hoàn tất nghiệp vụ
    
    GL->>SYS: Chạy bút toán tự động cuối kỳ
    SYS->>SYS: 1. Khấu hao TSCĐ (DK 6274,6424 / Co 214)
    SYS->>SYS: 2. Phân bổ CCDC (DK 642,641 / Co 242)
    SYS->>SYS: 3. Đánh giá lại chênh lệch tỷ giá (TK 413)
    SYS->>SYS: 4. Kết chuyển chi phí trả trước
    
    SYS->>GL: Thông báo hoàn tất bút toán tự động
    GL->>GL: Đối chiếu số dư Sổ Cái vs Sổ Chi Tiết
    GL->>CA: Trình Bảng Cân Đối Số Phát Sinh
    
    CA->>CA: Review biến động bất thường
    CA-->>GL: Yêu cầu điều chỉnh (nếu có)
    GL->>SYS: Nhập bút toán điều chỉnh
    SYS->>GL: Cập nhật Bảng CĐPS
    
    CA->>CA: Phê duyệt khóa sổ
    CA->>SYS: Lệnh khóa kỳ kế toán
    SYS->>SYS: Khóa trạng thái Period = 'CLOSED'
    SYS->>SYS: Tự động mở kỳ kế toán tiếp theo
    SYS->>CFO: Gửi thông báo & Báo cáo quản trị
```

### 4.2 Year-End Closing (TK 911)

```mermaid
flowchart TD
    A1[Kết thúc năm tài chính] --> A2[Đảm bảo tất cả 12 kỳ đã khóa]
    A2 --> A3[Chạy bút toán kết chuyển TK 911]
    
    A3 --> B1[Kết chuyển Doanh Thu]
    B1 --> B2[DK 511, 515, 711 / Co 911]
    
    A3 --> C1[Kết chuyển Chi Phí]
    C1 --> C2[DK 911 / Co 632, 635, 641, 642, 811, 821]
    
    B2 --> D1[Tính Kết Quả Kinh Doanh]
    C2 --> D1
    D1 --> D2{Lãi hay Lỗ?}
    
    D2 -- Lãi --> D3[DK 911 / Co 4212]
    D2 -- Lỗ --> D4[DK 4212 / Co 911]
    
    D3 --> E1[Phân phối lợi nhuận]
    D4 --> E1
    E1 --> E2[Trích Quỹ: DK 421 / Co 414, 418, 353...]
    E2 --> E3[Chia cổ tức: DK 421 / Co 338]
    E3 --> E4[Chuyển LNST lũy kế: DK 4212 / Co 4211]
    
    E4 --> F1[Số dư TK 911 = 0]
    F1 --> F2[Số dư TK 4212 = 0]
    F2 --> F3[Hoàn tất khóa năm]
```

---

## 5. HIRE TO RETIRE (H2R) - TÍNH LƯƠNG VÀ BHXH

### 5.1 Payroll Processing Flow

```mermaid
flowchart TD
    subgraph HR [Nhân Sự]
        A1[Cập nhật biến động nhân sự] --> A2[Gửi bảng chấm công]
        A2 --> A3[Danh sách tăng/giảm nhân viên]
    end

    subgraph PAY [Kế Toán Lương]
        A3 --> B1[Nhập dữ liệu vào hệ thống]
        B1 --> B2[Tính Lương Gross]
        B2 --> B3[Tính các khoản trừ bắt buộc]
        
        B3 --> C1[BHXH: 8% (Người lao động)]
        B3 --> C2[BHYT: 1.5% (Người lao động)]
        B3 --> C3[BHTN: 1% (Người lao động)]
        B3 --> C4[Thuế TNCN (Biểu lũy tiến)]
        
        C1 --> D1[Tính Lương Net]
        C2 --> D1
        C3 --> D1
        C4 --> D1
        D1 --> D2[Lập Bảng Thanh Toán Lương]
    end

    subgraph CA [Kế Toán Trưởng]
        D2 --> E1[Phê duyệt bảng lương]
        E1 --> E2{Đúng?}
        E2 -- Sai --> E3[Trả lại PAY chỉnh sửa]
        E3 --> B1
        E2 -- Đúng --> E4[Duyệt chi]
    end

    subgraph SYS [Hệ Thống]
        E4 --> F1[Hạch toán chi phí lương]
        F1 --> F2[DK 642, 622, 641 / Co 334]
        F1 --> F3[DK 642, 622, 641 / Co 3383, 3384, 3386]
        F1 --> F4[DK 642, 622, 641 / Co 3335]
        F1 --> F5[DK 642, 622, 641 / Co 3382 (KPCD 2%)]
    end

    subgraph CSH [Thủ Quỹ / Ngân Hàng]
        E4 --> G1[Thực hiện thanh toán]
        G1 --> G2[Chuyển khoản hàng loạt]
        G2 --> G3[Gửi phiếu lương cho NV]
    end
```

### 5.2 Key Compliance Notes
- **KPCD Base:** 2% calculated on Social Insurance Wage Base (Quỹ lương đóng BHXH), not actual salary.
- **BHTNLĐ-BNN:** Employer contribution 0.5% (handled in Employer cost accounting, not employee deduction).
- **PIT Deductions:** Personal (11M/month) + Dependent (4.4M/month).

---

## 6. ELECTRONIC INVOICE LIFECYCLE - QUY TRÌNH HĐĐT

### 6.1 Issuance & Correction Flow

```mermaid
flowchart TD
    A1[Phát sinh nghiệp vụ bán hàng] --> A2[Lập dữ liệu HĐ]
    A2 --> A3[Ký số hóa đơn]
    A3 --> A4[Gửi dữ liệu đến Cơ Quan Thuế]
    A4 --> A5{CQT phản hồi?}
    A5 -- Thành công --> A6[Nhận Mã CQT]
    A5 -- Thất bại --> A7[Kiểm tra & Gửi lại]
    A7 --> A4
    
    A6 --> A8[Gửi HĐ cho Khách Hàng]
    A8 --> A9[Hạch toán: DK 131 / Co 511, 3331]
    
    A9 --> B1{Phát hiện sai sót?}
    B1 -- Không --> B2[Kết thúc]
    B1 -- Có --> C1[Xác định loại sai sót]
    
    C1 --> C2{Loại sai sót?}
    C2 -- Sai tên/địa chỉ KH --> C3[Thông báo điều chỉnh]
    C3 --> C4[Lập HĐ Điều Chỉnh]
    C4 --> C5[Gửi CQT & KH]
    
    C2 -- Sai số tiền/thuế suất --> C6[Lập HĐ Thay Thế]
    C6 --> C7[Gửi CQT & KH]
    C7 --> C8[Hủy HĐ gốc trên hệ thống]
    
    C2 -- Hàng trả lại --> C9[Lập HĐ Hàng Trả Lại]
    C9 --> C10[Gửi CQT & KH]
    C10 --> C11[Hạch toán giảm doanh thu]
```

### 6.2 Compliance per Decree 70/2025
- **Replacement (Thay thế):** Used for wrong amount, tax rate, or quantity. Original invoice is voided.
- **Adjustment (Điều chỉnh):** Used for wrong buyer info (name, address, tax code) but correct amount. Original remains valid.
- **Timing:** Must notify tax authority via Form 04/SS-HDDT if error discovered after issuance.

---

## 7. FIXED ASSET LIFECYCLE - QUY TRÌNH TSCĐ

### 7.1 Asset Management Flow

```mermaid
flowchart TD
    subgraph ACQ [Mua Sắm / Xây Dựng]
        A1[Hoàn tất mua sắm/xây dựng] --> A2[Tập hợp chi phí TK 241]
        A2 --> A3[Nghiệm thu đưa vào sử dụng]
    end

    subgraph FA [Kế Toán TSCĐ]
        A3 --> B1[Lập Biên Bản Giao Nhận 01-TSCĐ]
        B1 --> B2[Đăng ký TSCĐ vào hệ thống]
        B2 --> B3[Xác định nguyên giá & thời gian khấu hao]
        B3 --> B4[Hạch toán tăng: DK 211 / Co 111,112,331,241]
    end

    subgraph SYS [Hệ Thống]
        B4 --> C1[Tính khấu hao hàng tháng]
        C1 --> C2[Điều kiện: Đã đưa vào sử dụng]
        C2 --> C3[Hạch toán: DK 6274,6424 / Co 214]
    end

    subgraph FA [Kế Toán TSCĐ]
        C3 --> D1{Sự kiện phát sinh?}
        D1 -- Điều chuyển --> D2[Lập Biên Bản Điều Chuyển]
        D2 --> D3[Cập nhật bộ phận sử dụng]
        
        D1 -- Sửa chữa lớn --> D4[Tập hợp chi phí TK 2413/2414]
        D4 --> D5[Tăng nguyên giá TSCĐ]
        
        D1 -- Thanh lý --> D6[Lập Hội Đồng Thanh Lý]
        D6 --> D7[Tính giá trị còn lại]
        D7 --> D8[Hạch toán giảm: DK 214, 811 / Co 211]
        D8 --> D9[Ghi nhận thu hồi phế liệu: DK 152 / Co 711]
    end
```

---

## 8. APPROVAL MATRIX & MAKER-CHECKER CONTROLS

### 8.1 Transaction Approval Limits

| Transaction Type | Maker (Người lập) | Checker 1 (Người kiểm tra) | Checker 2 (Người duyệt) | Final Approver |
|------------------|-------------------|---------------------------|------------------------|----------------|
| **Journal Entry** | Accountant | Senior Accountant | Chief Accountant | CFO (if > 500M VND) |
| **Payment Request** | AP/AR Accountant | Chief Accountant | CFO | CEO (if > 1B VND) |
| **Asset Disposal** | Asset Accountant | Chief Accountant | CFO | CEO / Board |
| **Payroll** | Payroll Accountant | Chief Accountant | CFO | CEO |
| **Tax Filing** | Tax Accountant | Chief Accountant | CFO | Legal Rep |
| **E-Invoice > 100M** | Sales Accountant | Chief Accountant | - | - |
| **E-Invoice > 100M** | Sales Accountant | Chief Accountant | CFO | - |

### 8.2 Segregation of Duties (SoD) Matrix

| Role | Can Create | Can Approve | Can Execute Payment |
|------|------------|-------------|---------------------|
| **Purchaser** | PO | No | No |
| **Warehouse** | Goods Receipt | No | No |
| **AP Accountant** | Payment Request | No | No |
| **Chief Accountant** | Journal Entry | Yes | No |
| **Cashier** | Payment Voucher | No | Yes |
| **CFO** | - | Yes | Yes (High value) |

### 8.3 System Enforcement Rules
1.  **No Self-Approval:** User cannot approve their own transactions.
2.  **Mandatory Attachment:** Invoices > 5M VND must have scanned attachment.
3.  **Period Lock:** No posting to closed periods (requires CA password to reopen).
4.  **Audit Trail:** All approvals logged with timestamp, IP, and device ID.

---

**END OF PROCESS FLOWS DOCUMENT**
