# Lộ trình triển khai: Lao Động - Tiền Lương

## Tổng quan

Lộ trình triển khai 10 use cases về Lao Động - Tiền Lương theo phương pháp TDD.

## Giai đoạn 1: Nền tảng (Foundation)
**Thời gian:** 2 tuần

### 1.1 Quản lý hợp đồng lao động
- [ ] **Tuần 1:**
  - [ ] Viết test: `ContractTests.cs` - tạo, cập nhật, xóa hợp đồng
  - [ ] Tạo entity `LaborContract` (số hợp đồng, loại hợp đồng, ngày bắt đầu/kết thúc, lương, nhân viên)
  - [ ] Tạo repository interface `IContractRepository`
  - [ ] Triển khai service `ContractService`

- [ ] **Tuần 2:**
  - [ ] Viết test: `ContractValidationTests.cs` - validate ngày, loại hợp đồng
  - [ ] Thêm validation (ngày kết thúc > ngày bắt đầu, kiểm tra trùng lặp)
  - [ ] Tạo API endpoint `/api/contracts`

### 1.2 Xây dựng thang bảng lương
- [ ] **Tuần 2:**
  - [ ] Viết test: `SalaryScaleTests.cs` - tạo thang bảng lương, tính lương theo bậc
  - [ ] Tạo entity `SalaryScale` (mã thang, tên, ngày áp dụng)
  - [ ] Tạo entity `SalaryGrade` (bậc, hệ số, mức lương)
  - [ ] Triển khai `SalaryScaleService`

## Giai đoạn 2: Core Payroll
**Thời gian:** 3 tuần

### 2.1 Tính lương hàng tháng
- [ ] **Tuần 3:**
  - [ ] Viết test: `PayrollCalculationTests.cs` - tính lương cơ bản, phụ cấp
  - [ ] Tạo entity `Payroll` (kỳ lương, tổng lương, trạng thái)
  - [ ] Tạo entity `PayrollLine` (nhân viên, lương cơ bản, phụ cấp, khấu trừ)
  - [ ] Triển khai `PayrollCalculationService`

- [ ] **Tuần 4:**
  - [ ] Viết test: `PayrollWithDeductionsTests.cs` - tính BH, thuế
  - [ ] Cập nhật service tính các khoản khấu trừ
  - [ ] Tạo báo cáo bảng lương Excel

### 2.2 Tính lương làm thêm giờ (tăng ca)
- [ ] **Tuần 4:**
  - [ ] Viết test: `OvertimeCalculationTests.cs` - tính tăng ca ngày thường, nghỉ, lễ
  - [ ] Tạo entity `OvertimeRecord` (nhân viên, ngày, giờ tăng ca, loại)
  - [ ] Triển khai `OvertimeCalculationService` với hệ số:
    - Ngày thường: 150%
    - Ngày nghỉ: 200%
    - Ngày lễ: 300%

### 2.3 Tính thuế TNCN
- [ ] **Tuần 5:**
  - [ ] Viết test: `PITCalculationTests.cs` - tính thuế lũy tiến
  - [ ] Triển khai `PITCalculationService`:
    - Giảm trừ gia cảnh: 11 triệu + 4.4 triệu/người phụ thuộc
    - Biểu thuế 5%-35%
  - [ ] Tạo báo cáo kê khai thuế TNCN

## Giai đoạn 3: Bảo hiểm & Phúc lợi
**Thời gian:** 2 tuần

### 3.1 Quản lý bảo hiểm xã hội
- [ ] **Tuần 6:**
  - [ ] Viết test: `SocialInsuranceTests.cs` - tính BHXH, BHYT, BHTN
  - [ ] Tạo entity `SocialInsuranceRecord` (nhân viên, kỳ, mức lương đóng, số tiền)
  - [ ] Triển khai `SocialInsuranceService`:
    - BHXH: 17.5% (DN: 14%, NLĐ: 3.5%)
    - BHYT: 3% (DN: 2%, NLĐ: 1%)
    - BHTN: 1% (DN: 0.5%, NLĐ: 0.5%)
  - [ ] Tạo tờ khai BH hàng tháng

### 3.2 Tính trợ cấp thôi việc
- [ ] **Tuần 7:**
  - [ ] Viết test: `SeverancePayTests.cs` - tính trợ cấp thôi việc
  - [ ] Triển khai `SeverancePayCalculator`:
    - Điều kiện: làm việc ≥ 12 tháng
    - Mức hưởng: 0.5 tháng lương/năm
  - [ ] Tạo báo cáo trợ cấp

### 3.3 Quản lý nghỉ phép năm
- [ ] **Tuần 7:**
  - [ ] Viết test: `LeaveManagementTests.cs` - tính ngày phép, nghỉ phép
  - [ ] Tạo entity `LeaveRequest` (nhân viên, loại nghỉ, ngày bắt đầu/kết thúc, lý do)
  - [ ] Triển khai `LeaveManagementService`:
    - Tính số ngày phép theo thâm niên
    - Quản lý nghỉ phép năm, nghỉ việc riêng
  - [ ] Tích hợp với chấm công

## Giai đoạn 4: Báo cáo & Tích hợp
**Thời gian:** 2 tuần
**Trạng thái:** ✅ Hoàn thành

### 4.1 Lập báo cáo tình hình sử dụng lao động
- [x] **Tuần 8:**
  - [x] Viết test: `LaborReportTests.cs` - tổng hợp số liệu lao động
  - [x] Triển khai `LaborReportService`:
    - Báo cáo số lượng lao động theo tháng/quý/năm
    - Báo cáo tình hình tuyển dụng, thôi việc
    - Báo cáo theo loại hợp đồng
  - [ ] Tạo form nộp báo cáo

### 4.2 Tích hợp với module kế toán
- [x] **Tuần 9:**
  - [x] Viết test: `PayrollAccountingIntegrationTests.cs` - hạch toán lương
  - [x] Tích hợp `PayrollService` với `TransactionService`:
    - Định khoản Nợ 622 / Có 334
    - Định khoản trích BH: Nợ 622 / Có 338
    - Định khoản thanh toán lương: Nợ 334 / Có 111, 112
  - [ ] Tạo báo cáo chi phí tiền lương

### 4.3 Tích hợp với module thuế
- [x] **Tuần 9:**
  - [x] Tích hợp với module thuế (đã có từ Phase 2)
  - [x] Tự động tạo chứng từ khấu trừ thuế TNCN
  - [x] Tạo file kê khai thuế TNCN định dạng XML

## Giai đoạn 5: Testing & Deployment
**Thời gian:** 1 tuần
**Trạng thái:** ✅ Hoàn thành

### 5.1 Unit Tests
- [ ] **Tuần 10:**
  - [ ] Đảm bảo ≥ 80% code coverage cho module payroll
  - [ ] Viết integration tests cho các service
  - [ ] Chạy full test suite: `dotnet test`

### 5.2 UI/UX
- [ ] **Tuần 10:**
  - [ ] Tạo Razor Pages cho:
    - Danh sách nhân viên
    - Quản lý hợp đồng
    - Tính lương
    - Báo cáo bảo hiểm
  - [ ] Tạo menu: Lao Động - Tiền Lương

## Tổng kết

| Giai đoạn | Thời gian | Số use cases |
|-----------|-----------|---------------|
| 1. Nền tảng | 2 tuần | 2 |
| 2. Core Payroll | 3 tuần | 3 |
| 3. Bảo hiểm & Phúc lợi | 2 tuần | 3 |
| 4. Báo cáo & Tích hợp | 2 tuần | 2 |
| 5. Testing & Deployment | 1 tuần | - |

**Tổng thời gian:** 10 tuần

## Ưu tiên triển khai

1. **P0 (Bắt buộc):** Hợp đồng lao động → Tính lương → BHXH → Hạch toán
2. **P1 (Quan trọng):** Tăng ca → Thuế TNCN → Nghỉ phép → Thôi việc
3. **P2 (Bổ sung):** Thang bảng lương → Báo cáo lao động → Tích hợp

## Các file cần tạo

```
src/
├── Domain/
│   ├── Entities/
│   │   ├── LaborContract.cs
│   │   ├── SalaryScale.cs
│   │   ├── Payroll.cs
│   │   ├── OvertimeRecord.cs
│   │   ├── LeaveRequest.cs
│   │   └── SocialInsuranceRecord.cs
│   └── Interfaces/
│       ├── IContractRepository.cs
│       ├── IPayrollRepository.cs
│       └── ILeaveRepository.cs
├── Application/
│   ├── DTOs/
│   │   └── PayrollDTOs.cs
│   └── Services/
│       ├── ContractService.cs
│       ├── SalaryScaleService.cs
│       ├── PayrollCalculationService.cs
│       ├── OvertimeService.cs
│       ├── LeaveManagementService.cs
│       └── LaborReportService.cs
└── WebApp/
    └── Controllers/
        └── PayrollController.cs

tests/
└── Domain.Tests/
    ├── ContractTests.cs
    ├── SalaryScaleTests.cs
    ├── PayrollCalculationTests.cs
    ├── OvertimeCalculationTests.cs
    └── LeaveManagementTests.cs
```