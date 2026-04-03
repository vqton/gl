# AGENTS.md - Development Guidelines for SME Accounting System

## Project Overview
Greenfield Django 5.x/Python 3.12+ accounting system for Vietnamese SMEs, complying with Thông tư 99/2025/TT-BTC. Uses SQLite with WAL mode for intranet deployment on Windows Server.

## Development Status (Updated 2026-04-02)

### Completed Modules
| Module | Status | Details |
|--------|--------|---------|
| **M4 - Tiền tệ** | Done | Phiếu thu/chi with auto journal, VND auto-calc |
| **M1/M8 - Hóa đơn** | Done | Invoice with VAT rates (0/5/8/10%), auto-numbering |
| **Chart of Accounts** | Done | 68 Tier-1 + 79 Tier-2 accounts from TT 99 |
| **Master Data** | Done | KhachHang, NhaCungCap, HangHoa, NganHang, DonVi |
| **Accounting Engine** | Done | ButToan with Nợ=Có validation, account type rules |
| **Kho (Inventory)** | Done | NhapKho/XuatKho models, TonKho/KhoEntry services |
| **Báo cáo** | Done | B01-DN (Bảng CĐKT), B02-DN (KQKD), B03-DN (LCTT), B09-DN (Thuyết minh), BCĐSPS |
| **Theme** | Done | Unified Google-style layout, fixed header+sidebar |
| **Tax Constants 2026** | Done | TNDN 15%/20%, TNCN brackets, VAT 0/5/8/10% |

### In Progress
| Module | Status | Notes |
|--------|--------|-------|
| **M2 - Kho valuation** | Partial | FIFO/Specific/Average strategies exist, backdating signal skeleton |
| **M3 - Tài sản** | Partial | Model exists, depreciation service TBD |
| **M7 - Lương** | Partial | Model exists, TNCN calculation service TBD |

### Test Status
- **495 tests passing** (seed fixture + constants + models + validators + services + phieu thu/chi + financial reports)
- **4 pre-existing failures** (URL routing test, E2E auth swap, account type auto-detect for 9xx)
- Coverage: ~94% overall

### Key Model Changes (Latest Session)
- `PhieuThu.tk_no`/`tk_co`: CharField → ForeignKey(TaiKhoanKeToan)
- `PhieuChi.tk_no`/`tk_co`: CharField → ForeignKey(TaiKhoanKeToan)
- `HoaDonChiTiet.thue_suat`: CharField → DecimalField with choices
- `HoaDon`: Added `quy_so`, `ma_hang_hoa_gtgt`, `loai_hang_hoa`, auto `so_hoa_don`, `ky_hieu` validation
- `ButToan`: Added `ngay_dua_vao_su_dung`, Nợ=Có validation when posting
- `ButToanChiTiet`: Added `so_chung_tu_goc`, account type vs Nợ/Có validation
- `core/settings.py`: Removed `init_command` from SQLite OPTIONS (incompatible with test DB)
- `services.py`: Updated `tao_phieu_thu`/`tao_phieu_chi` to use ForeignKey lookups

### UI Theme (Unified 2026-04-02)
- All pages use single `base.html` with fixed header + sidebar layout
- CSS variables: `--primary-color: #1a73e8` (Google-style)
- Sidebar sections: Nghiệp vụ, Kho, Báo cáo, Danh mục, Cấu hình
- Status badges: `status-draft` (gray), `status-posted` (green), `status-cancelled` (red)
- Responsive grid, print media query support

## Build & Development Commands

### Environment Setup
```bash
# Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # if exists
```

### Database Operations
```bash
# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Load seed data (68 Tier-1 accounts, 79 Tier-2 accounts)
python manage.py loaddata apps/danh_muc/fixtures/seed_accounts.json

# Create superuser
python manage.py createsuperuser
```

### Testing Commands
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=apps --cov-report=html --cov-report=term

# Run tests for specific app
pytest apps/nghiep_vu/tests/
pytest apps/kho/tests/

# Run a SINGLE TEST FUNCTION
pytest apps/nghiep_vu/tests/test_tax.py::test_calculate_tndn_sme_15_percent

# Run tests matching a pattern
pytest -k "tax"

# Run tests using Django test runner
python manage.py test apps.nghiep_vu
```

### Linting & Formatting
```bash
# Format code with black
black apps/ --line-length=88 --target-version=py312

# Sort imports with isort
isort apps/ --profile=black

# Check code style with flake8
flake8 apps/ --max-line-length=88 --extend-ignore=E203,W503

# Type checking with mypy
mypy apps/ --ignore-missing-imports
```

### Running the Application
```bash
# Development server
python manage.py runserver 0.0.0.0:8000

# Production server (Waitress on Windows)
waitress-serve --listen=0.0.0.0:8000 --threads=8 --call core.wsgi:application
```

## Code Style Guidelines

### Naming Conventions (Hybrid Approach)
- **Classes**: `PascalCase` (e.g., `TaiKhoanKeToan`, `PhieuThu`, `KhoLot`)
- **Functions/Variables**: `snake_case` (e.g., `tinh_thue_gtgt()`, `so_tien_nguyen_te`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `THUE_SUAT_SME_2026 = Decimal('0.15')`)
- **Business Terms**: Vietnamese without accents (e.g., `no_tk`, `co_tk`, `gia_von`, `dich_danh`)
- **Legal Terminology**: Must match exact terms from TT 99 (no translation)

### Inventory & Cost Accounting Terms (Mandatory)
To ensure consistency between Dev and Chief Accountant, NEVER use generic English terms:
- **Giá vốn**: `gia_von` (NOT `cost`)
- **Đích danh**: `dich_danh` (NOT `manual_match`)
- **Bình quân liên hoàn**: `binh_quan_lien_hoan` (NOT `moving_average`)
- **Nhập bù / Tính lại**: `tinh_lai_gia_von` (NOT `recalculate`)
- **Giá vốn tạm tính**: `gia_von_tam_tinh`
- **Giá vốn chính thức**: `gia_von_chinh_thuc`

### Import Organization
```python
# Standard library imports (alphabetical)
import decimal
from datetime import datetime

# Third-party imports (alphabetical)
from cryptography.fernet import Fernet
from django.db import models
from django.core.exceptions import ValidationError

# Local application imports (alphabetical)
from apps.danh_muc.models import TaiKhoanKeToan
from apps.nghiep_vu.constants import THUE_SUAT_GTGT_2026
from apps.kho.valuation.strategies import BaseValuationStrategy
```

### Data Types & Field Specifications
- **Monetary Values (VND)**: `models.DecimalField(max_digits=20, decimal_places=2)`
- **Unit Prices & Exchange Rates**: `models.DecimalField(max_digits=20, decimal_places=4)` (4 decimal places for weighted average precision)
- **NEVER use FloatField** for currency or any financial calculation
- **Account Codes**: `models.CharField(max_length=10, unique=True)`
- **Timestamps**: `models.DateTimeField(auto_now_add=True)` or `auto_now=True`
- **Decimal Inputs**: Use `decimal.Decimal('0.15')` not `0.15`
- **Rounding**: Use `quantize()` at the final step before saving to database

### Documentation & Docstrings
All business functions require Google Style Docstring with legal references:
```python
def tinh_thue_tndn_sme(doanh_thu_nam: decimal.Decimal, loi_nhuan: decimal.Decimal) -> decimal.Decimal:
    """
    Calculate corporate income tax for SME (15% rate for revenue < 3 billion VND).
    
    Legal basis:
        - Luật 67/2025/QH15 about Corporate Income Tax
        - Nghị định 320/2025/NĐ-CP implementation
    
    Args:
        doanh_thu_nam: Annual revenue (decimal)
        loi_nhuan: Pre-tax profit (decimal)
    
    Returns:
        Tax amount as decimal
    """
```

### Error Handling Patterns
```python
from django.core.exceptions import ValidationError
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

@transaction.atomic
def create_transaction_with_validation(data):
    """Create accounting transaction with validation."""
    try:
        # Validate required fields
        if not data.get('so_tien'):
            raise ValidationError({'so_tien': ['Số tiền là bắt buộc']})
        
        # Business logic validation
        validate_accounting_rules(data)
        
        # Create transaction
        return GiaoDich.objects.create(**data)
        
    except ValidationError:
        raise  # Re-raise validation errors
    except Exception as e:
        logger.error(f"Error creating transaction: {e}", exc_info=True)
        raise ValidationError('Lỗi hệ thống khi tạo giao dịch')
```

### Security & Compliance Requirements
- **Encryption**: AES-256 field-level encryption for sensitive data (salaries, personal tax IDs, phone numbers) per Nghị định 13/2023/NĐ-CP
- **Key Management**: Encryption keys from Windows Environment Variables ONLY, never hard-coded
- **Encrypted Models**: Sensitive data models must inherit from `EncryptedModelBase`
- **Audit Trail**: All models must track `created_by`, `created_at`, `updated_by`, `updated_at`
- **Payroll Audit**: Log every view/edit of salary data: Who, When, IP address
- **Intranet Only**: Configure `ALLOWED_HOSTS` for local network IPs only
- **Master Data Protection**: Use Django signals to prevent UPDATE/DELETE on legal master data
- **No raw SQL**: Use Django ORM exclusively

### Testing Patterns (TDD Mandatory)
```python
import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from apps.nghiep_vu.services import tinh_thue_tndn_sme

def test_tinh_thue_tndn_duoi_3_ty():
    """Test TNDN calculation for SME with revenue < 3 billion VND."""
    # Arrange
    doanh_thu = Decimal('2500000000')  # 2.5 billion VND
    loi_nhuan = Decimal('100000000')   # 100 million VND
    
    # Act
    ket_qua = tinh_thue_tndn_sme(doanh_thu, loi_nhuan)
    
    # Assert
    assert ket_qua == Decimal('15000000')  # 15% of 100 million
```

### Inventory Testing Requirements (3-Layer TDD)
All inventory-related code must pass 3 test layers:
1. **Normal In/Out Test**: Verify inventory balance updates correctly
2. **Valuation Test**: Verify cost matches configured method (FIFO/Specific/Weighted Average)
3. **Backdating Test**: Simulate inserting a receipt in the middle of transactions; verify subsequent issues are automatically recalculated (`gia_von_chinh_thuc`)

### Line Endings & Formatting
- **Line Endings**: LF (not CRLF) - enforced via `.gitattributes` for all `.py` and `.json` files
- **Line Length**: 88 characters (Black default)
- **Indentation**: 4 spaces (no tabs)
- **Trailing Whitespace**: Remove automatically
- **File Encoding**: UTF-8

### Git Commit & Push Convention
Format: `[Module] - [Action] - [Detailed description]`
Examples:
- `[M4-Ketoan] - Seed - Load original 71 Tier-1 accounts from TT 99 Appendix II`
- `[M1-Banhang] - Fix - Correct invoice date validation for 2026 tax period`
- `[M2-KHO] - Update - Implement logic bình quân gia quyền liên hoàn`

**Push Policy**: Push to remote immediately when:
1. A phase is completed and all quality gates pass
2. A self-contained feature is finished (even mid-phase)
3. Before switching context to a different task
4. NEVER push incomplete code that breaks tests or lints

### Quality Gates
Before any commit, ensure:
1. All tests pass: `pytest`
2. Code formatting: `black --check apps/`
3. Import sorting: `isort --check-only apps/`
4. No lint errors: `flake8 apps/`
5. Type checking passes: `mypy apps/`

### Special Considerations
- **Windows Development**: Use `pathlib` for path handling, configure IDE for LF line endings
- **Master Data**: 68 Tier-1 accounts from TT 99 must be immutable
- **Decimal Precision**: max_digits=20, decimal_places=2 for VND; decimal_places=4 for unit prices/exchange rates
- **Legal Terminology**: Must match exactly with Vietnamese legal documents
- **TDD Mandatory**: Follow Red/Green/Refactor cycle for all business functionality
- **No-Icon UI Policy**: Sidebar uses text labels with emojis for navigation (e.g., 📝 Phiếu thu, 📦 Kho). Data tables use text labels and status colors only.
- **Keyboard-First**: 100% of accounting vouchers must be completable without mouse

## Architecture & Project Structure

### Django Apps
```
apps/
├── danh_muc/           # Master data (accounts, suppliers, customers, goods, banks)
├── nghiep_vu/          # Business operations (sales, purchases, tax, vouchers, journals)
├── kho/                # Inventory management & valuation engine
│   ├── valuation/      # Cost calculation strategies (FIFO, Specific, Weighted Average)
│   ├── services.py     # In/out/transfer operations
│   └── signals.py      # Trigger recalculation on backdating
├── bao_cao/            # Financial reports with drill-down to source documents
├── tai_san/            # Fixed assets management
├── luong/              # Payroll & social insurance
├── users/              # Custom user model (NguoiDung)
└── accounting/         # Dashboard, login, main views
```

### Valuation Engine (Strategy Pattern)
Each costing method is a separate class inheriting from `BaseValuationStrategy`:
- `SpecificIdentificationStrategy`: Match `lot_id` from issue to receipt
- `FIFOStrategy`: Queue-based First-In-First-Out by actual receipt time
- `WeightedAverageStrategy`: Perpetual weighted average calculation

```python
class InventoryValuationService:
    def recalculate(self, item_id, start_date):
        """
        Recalculate cost from a given date point.
        Uses signals to trigger on backdating events.
        """
```

### Backdating/Recalculation Mechanism
When a past receipt is modified or inserted:
1. Trigger fires via Django signals
2. Engine finds all issues for that item with `ngay_chung_tu >= modified_date`
3. Recalculates cost and updates `gia_von_chinh_thuc` on affected issues

## Test Coverage Requirements

| Module | Coverage Target |
|--------|----------------|
| Inventory & Valuation | 100% Branch Coverage |
| Tax & Financial Reports | 100% Statement Coverage |
| Accounting/Tax Core | >95% |
| Overall | 60% Unit, 20% Data Integrity, 15% Integration, 5% E2E |

### Test Pyramid (Updated V2.0)
| Type | Weight | Purpose |
|------|--------|---------|
| Unit Tests | 60% | Tax, payroll, basic accounting logic |
| Data Integrity Tests | 20% | Cost correctness after Recalculate/Backdating |
| Integration Tests | 15% | SQLite WAL recording, Audit Trail |
| E2E Tests | 5% | Financial statement flow from source documents |

## Deployment Notes
- **WSGI**: Waitress (Windows-optimized, no complex config)
- **Static Files**: WhiteNoise for self-serving static files
- **Scheduled Tasks**: Windows Task Scheduler for nightly `python manage.py recalculate_inventory` at 23:00
- **Database Backup**: Daily copy of `.sqlite3` file (single file backup)
- **Firewall**: Only open port 80/443 for internal IP range
