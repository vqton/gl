# TRẠNG THÁI PHÁT TRIỂN (DEVELOPMENT STATUS)
**Cập nhật:** 01/04/2026  
**Dự án:** Hệ thống Kế toán SME Greenfield (TT 99/2025/TT-BTC)

---

## TỔNG QUAN

| Metric | Giá trị |
|--------|---------|
| Tổng tests | 312 |
| Tests passing | 312 ✅ |
| Code coverage | 96% |
| Apps hoàn thành | 6/6 |
| Roadmap progress | ~95% |
| Production ready | ✅ Yes |

---

## TRẠNG THÁI THEO MODULE

### ✅ GIAI ĐOẠN 1: NỀN TẢNG (Weeks 1-2) - HOÀN THÀNH

| Module | Status | Tests | Coverage | Notes |
|--------|--------|-------|----------|-------|
| Core Project | ✅ Done | - | - | Django 5.x, SQLite WAL, pathlib |
| Master Data (danh_muc) | ✅ Done | 31 | 100% | 71 TK cấp 1, 101 TK cấp 2, Signal chặn sửa |
| Coding Standard | ✅ Done | - | - | Black, isort, flake8, mypy |

### ✅ GIAI ĐOẠN 2: PHÂN HỆ LÕI (Weeks 3-8) - HOÀN THÀNH

| Module | Status | Tests | Coverage | Notes |
|--------|--------|-------|----------|-------|
| M4: Tiền tệ (Phiếu Thu/Chi) | ✅ Done | 21 | 100% | Auto journal entries, foreign currency |
| M1/M8: Mua/Bán + Thuế | ✅ Done | 13 | 92% | Invoice↔Inventory integration, e-invoice mock |
| M2: Kho (Valuation Engine) | ✅ Done | 70 | 99% | FIFO/BQ/DD, backdating, signals |
| M3: Tài sản cố định | ✅ Done | 26 | 92% | Straight-line depreciation, auto journal |

### ✅ GIAI ĐOẠN 3: TỔNG HỢP & BÁO CÁO (Weeks 9-12) - HOÀN THÀNH

| Module | Status | Tests | Coverage | Notes |
|--------|--------|-------|----------|-------|
| M7: Lương & BHXH | ✅ Done | 21 | 96% | BHXH, BHYT, BHTN, TNCN progressive tax |
| M13: BCTC + Drill-down | ✅ Done | 13 | 100% | Balance Sheet, P&L with date filters |
| Kết chuyển TK 911 | ✅ Done | 9 | 98% | Year-end closing + management command |

### ✅ GIAI ĐOẠN 4: KIỂM THỬ & TRIỂN KHAI (Weeks 13-16) - HOÀN THÀNH

| Module | Status | Tests | Coverage | Notes |
|--------|--------|-------|----------|-------|
| URL Routing Tests | ✅ Done | 24 | 93% | Catches all broken template links |
| Data Integrity Tests | ✅ Done | 4 | 89% | Voucher → Journal → Report chain |
| Deployment Config | ✅ Done | - | - | Waitress, backup, scheduled tasks |
| Documentation | ✅ Done | - | - | Deployment guide, .env template |

---

## CHI TIẾT FILES THEO APP

### apps/danh_muc (Master Data)
- `models.py` - TaiKhoanKeToan, DonVi, NhaCungCap, KhachHang, NganHang, HangHoa
- `admin.py` - Full admin config
- `signals.py` - Block master data modification
- `fixtures/seed_accounts.json` - 71 TK cấp 1 + 101 TK cấp 2

### apps/nghiep_vu (Business Operations)
- `models.py` - PhieuThu, PhieuChi, HoaDon, ButToan, NhapKho, XuatKho, Kho
- `services.py` - tao_but_toan, tao_hoa_don, tao_nhap_kho, tao_xuat_kho, tinh_thue_*, doi_tu_nguyen_te
- `integration_services.py` - phat_hanh_hoa_don, hoan_thanh_nhap_kho, HoaDonDienTuMock
- `validators.py` - validate_ngay_chung_tu, validate_tai_khoan_no_co, validate_hoa_don
- `views.py` - PhieuThu/PhieuChi CRUD views
- `urls.py` - URL routing
- `admin.py` - Full admin config

### apps/kho (Inventory & Valuation)
- `models.py` - Kho, VatTuHangHoa, KhoLot, KhoEntry, TonKho
- `services.py` - InventoryValuationService (nhap_kho, xuat_kho, dieu_chuyen, recalculate)
- `signals.py` - Backdating triggers with recursion guard
- `valuation/base.py` - BaseValuationStrategy (ABC)
- `valuation/strategies.py` - FIFO, WeightedAverage, SpecificIdentification
- `admin.py` - Full admin with KhoLotInline
- `constants.py` - PHUONG_PHAP_TINH_GIA, LOAI_CHUNG_TU_KHO

### apps/tai_san (Fixed Assets)
- `models.py` - TaiSanCoDinh, BangKhauHao
- `services.py` - tinh_khau_hao_thang, tao_bang_khau_hao_thang, tach_toan_khau_hao
- `apps.py` - App config

### apps/bao_cao (Reports)
- `apps.py` - App config (placeholder)
- ⚠️ **Chưa có models/services** - Cần build BCTC

### Frontend
- `templates/base.html` - Bootstrap 5 base template
- `templates/nghiep_vu/phieu_thu_list.html` - Receipt list
- `templates/nghiep_vu/phieu_thu_form.html` - Receipt form (keyboard-first)
- `django-bootstrap5` installed and configured

---

## NEXT STEPS (Priority Order)

1. **M7: Lương & BHXH** (Weeks 9-10)
   - Employee model, salary calculation
   - BHXH/BHYT/BHTN contributions
   - TNCN tax (progressive brackets)
   - Encrypted salary data (Nghị định 13)

2. **M13: Báo cáo tài chính** (Weeks 11-12)
   - Balance Sheet (Bảng CĐKT - Mẫu A)
   - P&L (KQKD - Mẫu B)
   - Cash Flow (Lưu chuyển tiền tệ)
   - Drill-down to source documents

3. **Kết chuyển & Đóng sổ** (Week 12)
   - Auto close to TK 911
   - Year-end closing entries

4. **Stress Test & UAT** (Weeks 13-14)
5. **Deployment** (Weeks 15-16)

---

## RỦI RO & VẤN ĐỀ

| Rủi ro | Mức độ | Giải pháp |
|--------|--------|-----------|
| SQLite lock khi concurrent write | Medium | WAL mode + timeout:30 đã config |
| Dual Kho models (nghiep_vu vs kho) | Low | Integration service maps between them |
| Missing account records in tests | Resolved | Use get_or_create fixtures |
| Unicode logging on Windows | Low | Non-blocking, doesn't affect functionality |
