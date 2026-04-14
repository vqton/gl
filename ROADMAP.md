# GL Accounting System Roadmap

## Overview
This roadmap outlines the strategic direction for the GL Accounting System based on Thông tư 99/2025/TT-BTC requirements.

## Vision
To provide a comprehensive, compliant accounting system that fully implements the Thông tư 99/2025/TT-BTC chart of accounts and core use cases.

## Strategic Goals
1. Full compliance with Thông tư 99/2025/TT-BTC
2. Implementation of all 22 core use cases
3. Support for complete accounting cycle
4. Generation of standard financial statements
5. Extensibility for future regulatory updates

## Phased Implementation Plan

### Phase 1: Foundation (Q1-Q2 2026) ✅ COMPLETED
- Implement core chart of accounts structure (71 level 1 accounts)
- Develop basic transaction processing engine
- Create foundational domain modules:
  - Sales & Revenue (S01-S06)
  - Purchasing & Inventory (P01-P05)
  - Cash & Bank Management (T01-T05)
- Build basic reporting framework

### Phase 2: Core Functionality (Q3-Q4 2026) ✅ COMPLETED
- Implement tax management (X01-X05)
- Develop payroll and social insurance (L01-L07)
- Build fixed assets management (A01-A06)
- Complete period-end closing processes (G01-G08)
- Implement financial statement generation

### Phase 3: Integration & Optimization (Q1-Q2 2027) ✅ COMPLETED
- Integrate all modules for seamless workflow
- Optimize performance for high-volume transactions
- Enhance reporting capabilities with analytics
- Implement audit trail and compliance features
- Conduct user acceptance testing

### Phase 4: Advanced Features (Q3-Q4 2027) ✅ COMPLETED
- Add multi-currency support
- Implement budgeting and forecasting
- Develop role-based access control
- Add API for third-party integrations
- Implement cloud deployment options

## New: Lao Động - Tiền Lương Module (2026)

### Module: Lao Động - Tiền Lương (Labor & Payroll)

#### P0: Core Features ✅ IMPLEMENTED
- **Quản lý hợp đồng lao động** (Labor Contract Management)
  - Entity: `LaborContract.cs`
  - Service: `ContractService.cs`
  - API: `/api/v1/contracts`
- **Tính lương hàng tháng** (Monthly Payroll Calculation)
  - Entity: `Payroll.cs`, `PayrollLine.cs`
  - Service: `PayrollCalculationService.cs`
  - Tính BHXH (17.5%), BHYT (3%), BHTN (1%), Thuế TNCN (lũy tiến 5%-35%)
  - API: `/api/v1/payrolls`
- **Hạch toán tiền lương** (Payroll Accounting)
  - Service: `PayrollAccountingService.cs`
  - Định khoản: Nợ 622 / Có 334, Nợ 622 / Có 338

#### P1: Advanced Features ✅ IMPLEMENTED
- **Tính lương làm thêm giờ** (Overtime Calculation)
  - Entity: `OvertimeRecord.cs`
  - Service: `OvertimeCalculationService.cs`
  - Hệ số: Ngày thường 150%, Nghỉ 200%, Lễ 300%
  - API: `/api/v1/overtimes`
- **Quản lý nghỉ phép năm** (Annual Leave Management)
  - Entity: `LeaveRequest.cs`
  - Service: `LeaveManagementService.cs`
  - Số ngày phép: 12-19 ngày/năm theo thâm niên
  - API: `/api/v1/leaves`
- **Tính trợ cấp thôi việc** (Severance Pay Calculation)
  - Entity: `SeveranceRecord.cs`
  - Service: `SeverancePayCalculator.cs`
  - Điều kiện: ≥12 tháng làm việc
  - Mức hưởng: 0.5 tháng/năm
  - API: `/api/v1/severance`

#### Use Cases Reference
- `/docs/use_cases/laodong_tienluong.md` - 10 use cases documented
- `/docs/roadmaps/laodong_tienluong_roadmap.md` - Implementation roadmap

### Tests: 127 passing ✅

## Success Metrics
- 100% coverage of 22 core use cases
- Ability to generate complete BCĐKT and BCKQHĐKD statements
- Successful completion of full accounting cycle
- User satisfaction score > 4.0/5.0
- Zero critical compliance findings in audits
- Lao Động - Tiền Lương module fully implemented

## Dependencies
- Regulatory stability of Thông tư 99/2025/TT-BTC
- Availability of skilled accounting developers
- Adequate testing resources
- Stakeholder engagement and feedback

## Risk Management
- Regulatory changes: Monitor for updates and maintain flexible architecture
- Technical complexity: Use modular design and incremental delivery
- User adoption: Involve end-users early in development process
- Performance: Implement caching and optimization strategies from Phase 2

## Review Cycle
- Quarterly review of roadmap progress
- Bi-annual stakeholder workshops
- Annual update based on feedback and regulatory changes

---
*Last updated: April 2026*
*Module: Lao Động - Tiền Lương - P0 & P1 Complete (127 tests)*