# SOFTWARE FUNCTIONAL SPECIFICATION (SFS)
# Vietnamese Enterprise Accounting Software Platform
# Compliant with Circular 99/2025/TT-BTC

**Document Version:** 1.0
**Date:** April 2026
**Prepared by:** System Analyst Office
**Classification:** Confidential
**Status:** Approved for Development

**Source Document:** SRS v1.0 (SOFTWARE_REQUIREMENTS_SPECIFICATION.md)

---

## TABLE OF CONTENTS

1.  Introduction
2.  System Architecture
3.  Database Design
4.  API Specifications
5.  UI/UX Specifications
6.  Detailed Functional Logic
7.  Security Implementation
8.  Integration Implementation
9.  Deployment & Infrastructure

---

## 1. INTRODUCTION

### 1.1 Purpose
This document translates the SRS requirements into technical specifications for the development team. It defines database schemas, API contracts, UI flows, and business logic implementations.

### 1.2 Scope
Covers all 15 modules defined in the SRS, providing the technical blueprint for implementation.

### 1.3 Technology Stack
| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Next.js 14, TailwindCSS, React Hook Form |
| Backend | Python 3.11, FastAPI, Pydantic v2 |
| Database | PostgreSQL 15, Redis 7 (cache/sessions) |
| Queue | Celery + RabbitMQ |
| Storage | AWS S3 (Vietnam region) / MinIO |
| Auth | JWT (RS256), OAuth2, TOTP (2FA) |

---

## 2. SYSTEM ARCHITECTURE

### 2.1 High-Level Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENT (Browser)                        │
│  React SPA (Next.js) ── HTTPS ──> API Gateway / Load Balancer│
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                    APPLICATION LAYER                        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────────┐ │
│  │ Auth Svc │ │ GL Svc   │ │ Tax Svc  │ │ Invoice Svc    │ │
│  └──────────┘ └──────────┘ └──────────┘ └────────────────┘ │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────────┐ │
│  │ AR Svc   │ │ AP Svc   │ │ Pay Svc  │ │ Report Svc     │ │
│  └──────────┘ └──────────┘ └──────────┘ └────────────────┘ │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                      DATA LAYER                             │
│  PostgreSQL (Primary DB) ── Redis (Cache/Sessions) ── S3    │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Multi-Tenancy Strategy
- **Schema-per-tenant** approach for data isolation.
- Shared `public` schema for tenant metadata, users, and global configurations.
- Each tenant gets a private schema: `tenant_{tenant_id}`.
- Row-Level Security (RLS) as secondary enforcement.

---

## 3. DATABASE DESIGN

### 3.1 Core Tables (Public Schema)

```sql
-- Tenant Registry
CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    tax_code VARCHAR(20) UNIQUE NOT NULL,
    schema_name VARCHAR(63) UNIQUE NOT NULL,
    accounting_regime VARCHAR(20) DEFAULT 'TT99', -- TT99, TT133
    status VARCHAR(20) DEFAULT 'active', -- active, suspended, archived
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Users (Global)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    totp_secret VARCHAR(100),
    is_2fa_enabled BOOLEAN DEFAULT FALSE,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tenant-User Mapping
CREATE TABLE tenant_users (
    tenant_id UUID REFERENCES tenants(id),
    user_id UUID REFERENCES users(id),
    role VARCHAR(50) NOT NULL, -- chief_accountant, accountant, cashier, etc.
    PRIMARY KEY (tenant_id, user_id)
);
```

### 3.2 Tenant Schema Tables (Example: `tenant_xxx`)

```sql
-- Chart of Accounts
CREATE TABLE chart_of_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_code VARCHAR(10) UNIQUE NOT NULL,
    account_name_en VARCHAR(255) NOT NULL,
    account_name_vn VARCHAR(255) NOT NULL,
    account_group INT NOT NULL, -- 1-8
    level INT NOT NULL, -- 1-4
    parent_code VARCHAR(10),
    is_active BOOLEAN DEFAULT TRUE,
    is_custom BOOLEAN DEFAULT FALSE,
    justification_doc_id UUID, -- FK to documents table
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Journal Entries
CREATE TABLE journal_entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entry_number VARCHAR(20) UNIQUE NOT NULL,
    entry_date DATE NOT NULL,
    period VARCHAR(7) NOT NULL, -- YYYY-MM
    description TEXT NOT NULL,
    entry_type VARCHAR(30) NOT NULL, -- daily, adjustment, closing, etc.
    currency VARCHAR(3) DEFAULT 'VND',
    exchange_rate DECIMAL(10,4) DEFAULT 1.0000,
    total_debit DECIMAL(18,2) DEFAULT 0,
    total_credit DECIMAL(18,2) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'draft', -- draft, pending, posted, reversed
    created_by UUID NOT NULL,
    approved_by UUID,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    posted_at TIMESTAMPTZ
);

-- Journal Entry Lines
CREATE TABLE journal_entry_lines (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entry_id UUID REFERENCES journal_entries(id) ON DELETE CASCADE,
    line_number INT NOT NULL,
    account_code VARCHAR(10) NOT NULL REFERENCES chart_of_accounts(account_code),
    debit_amount DECIMAL(18,2) DEFAULT 0,
    credit_amount DECIMAL(18,2) DEFAULT 0,
    description TEXT,
    cost_center VARCHAR(50),
    project VARCHAR(50),
    partner_id UUID, -- customer_id or supplier_id
    invoice_ref VARCHAR(50),
    UNIQUE(entry_id, line_number)
);

-- Accounting Periods
CREATE TABLE accounting_periods (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    period VARCHAR(7) UNIQUE NOT NULL, -- YYYY-MM
    status VARCHAR(20) DEFAULT 'open', -- open, locked, closed
    closed_at TIMESTAMPTZ,
    closed_by UUID
);

-- Customers
CREATE TABLE customers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    tax_code VARCHAR(20) NOT NULL,
    address TEXT,
    credit_limit DECIMAL(18,2) DEFAULT 0,
    payment_terms INT DEFAULT 30, -- days
    status VARCHAR(20) DEFAULT 'active'
);

-- Suppliers
CREATE TABLE suppliers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    supplier_code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    tax_code VARCHAR(20) NOT NULL,
    address TEXT,
    bank_account VARCHAR(50),
    bank_name VARCHAR(100),
    payment_terms INT DEFAULT 30,
    status VARCHAR(20) DEFAULT 'active'
);

-- E-Invoices
CREATE TABLE e_invoices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    invoice_number VARCHAR(30) UNIQUE NOT NULL,
    invoice_symbol VARCHAR(20),
    invoice_date DATE NOT NULL,
    invoice_time TIME NOT NULL,
    buyer_tax_code VARCHAR(20),
    buyer_name VARCHAR(255),
    total_amount DECIMAL(18,2) NOT NULL,
    total_vat DECIMAL(18,2) NOT NULL,
    total_with_vat DECIMAL(18,2) NOT NULL,
    invoice_type VARCHAR(30), -- with_cqt, without_cqt
    status VARCHAR(30) DEFAULT 'draft', -- draft, sent, confirmed, replaced, adjusted, cancelled
    cqt_code VARCHAR(50),
    digital_signature_hash TEXT,
    created_by UUID NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- E-Invoice Lines
CREATE TABLE e_invoice_lines (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    invoice_id UUID REFERENCES e_invoices(id) ON DELETE CASCADE,
    line_number INT NOT NULL,
    item_name VARCHAR(255) NOT NULL,
    unit VARCHAR(20),
    quantity DECIMAL(10,2) NOT NULL,
    unit_price DECIMAL(18,2) NOT NULL,
    vat_rate DECIMAL(5,2) NOT NULL,
    vat_amount DECIMAL(18,2) NOT NULL,
    line_total DECIMAL(18,2) NOT NULL
);

-- Fixed Assets
CREATE TABLE fixed_assets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_code VARCHAR(20) UNIQUE NOT NULL,
    asset_name VARCHAR(255) NOT NULL,
    category VARCHAR(50),
    original_cost DECIMAL(18,2) NOT NULL,
    accumulated_depreciation DECIMAL(18,2) DEFAULT 0,
    depreciation_method VARCHAR(30), -- straight_line, declining, units
    useful_life_months INT NOT NULL,
    residual_value DECIMAL(18,2) DEFAULT 0,
    acquisition_date DATE NOT NULL,
    put_into_use_date DATE,
    depreciation_start_date DATE,
    status VARCHAR(30) DEFAULT 'active', -- active, transferred, disposed
    location VARCHAR(100),
    cost_center VARCHAR(50)
);

-- Employees
CREATE TABLE employees (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    employee_code VARCHAR(20) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    tax_code VARCHAR(20),
    contract_type VARCHAR(30), -- indefinite, fixed_term, probation
    base_salary DECIMAL(18,2) NOT NULL,
    insurance_base DECIMAL(18,2),
    dependents_count INT DEFAULT 0,
    status VARCHAR(20) DEFAULT 'active'
);

-- Payroll Records
CREATE TABLE payroll_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    period VARCHAR(7) NOT NULL, -- YYYY-MM
    employee_id UUID REFERENCES employees(id),
    gross_salary DECIMAL(18,2) NOT NULL,
    allowances DECIMAL(18,2) DEFAULT 0,
    overtime_pay DECIMAL(18,2) DEFAULT 0,
    bhxh_employee DECIMAL(18,2) DEFAULT 0,
    hyt_employee DECIMAL(18,2) DEFAULT 0,
    bhtn_employee DECIMAL(18,2) DEFAULT 0,
    pit_withheld DECIMAL(18,2) DEFAULT 0,
    net_salary DECIMAL(18,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending', -- pending, approved, paid
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Audit Log
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL,
    user_id UUID,
    action VARCHAR(50) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id UUID,
    old_value JSONB,
    new_value JSONB,
    ip_address INET,
    device_id VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 3.3 Indexes & Constraints
```sql
-- Performance Indexes
CREATE INDEX idx_je_period ON journal_entries(period);
CREATE INDEX idx_je_status ON journal_entries(status);
CREATE INDEX idx_je_lines_account ON journal_entry_lines(account_code);
CREATE INDEX idx_einv_date ON e_invoices(invoice_date);
CREATE INDEX idx_payroll_period ON payroll_records(period);
CREATE INDEX idx_audit_entity ON audit_log(entity_type, entity_id);

-- Check Constraints
ALTER TABLE journal_entries ADD CONSTRAINT chk_je_balance 
    CHECK (total_debit = total_credit);
ALTER TABLE journal_entry_lines ADD CONSTRAINT chk_line_amounts 
    CHECK (debit_amount >= 0 AND credit_amount >= 0);
ALTER TABLE e_invoices ADD CONSTRAINT chk_einv_totals 
    CHECK (total_with_vat = total_amount + total_vat);
```

---

## 4. API SPECIFICATIONS

### 4.1 Authentication & Authorization

```
POST /api/v1/auth/login
Request: { "email": "...", "password": "...", "totp_code": "..." }
Response: { "access_token": "...", "refresh_token": "...", "expires_in": 1800 }

POST /api/v1/auth/refresh
Request: { "refresh_token": "..." }
Response: { "access_token": "..." }

POST /api/v1/auth/logout
Headers: Authorization: Bearer <token>
Response: 204 No Content
```

### 4.2 Journal Entries

```
GET /api/v1/gl/entries
Query: ?period=2026-04&status=posted&page=1&limit=50
Response: { "data": [...], "total": 1200, "page": 1 }

POST /api/v1/gl/entries
Request: {
  "entry_date": "2026-04-15",
  "period": "2026-04",
  "description": "Mua văn phòng phẩm",
  "entry_type": "daily",
  "currency": "VND",
  "lines": [
    { "account_code": "6423", "debit_amount": 5000000, "description": "VP phẩm" },
    { "account_code": "1111", "credit_amount": 5000000, "description": "TM" }
  ]
}
Response: 201 Created { "id": "...", "entry_number": "NKC-000042" }

PUT /api/v1/gl/entries/{id}/approve
Headers: Authorization: Bearer <token>
Response: 200 { "status": "posted", "posted_at": "..." }
```

### 4.3 E-Invoices

```
POST /api/v1/einvoices
Request: {
  "buyer_name": "Công ty ABC",
  "buyer_tax_code": "0100123456",
  "invoice_type": "with_cqt",
  "lines": [
    { "item_name": "Dịch vụ phần mềm", "quantity": 1, "unit_price": 10000000, "vat_rate": 10 }
  ]
}
Response: 201 { "id": "...", "invoice_number": "AA/26E/00001", "status": "sent" }

POST /api/v1/einvoices/{id}/replace
Request: { "reason": "Sai số tiền", "new_lines": [...] }
Response: 200 { "id": "...", "status": "replaced", "replacement_id": "..." }
```

### 4.4 Financial Reports

```
GET /api/v1/reports/trial-balance?period=2026-04
Response: {
  "data": [
    { "account_code": "1111", "opening_dr": 50000000, "period_dr": 20000000, "period_cr": 15000000, "closing_dr": 55000000 }
  ],
  "total_dr": 100000000,
  "total_cr": 100000000
}

GET /api/v1/reports/b01-dn?period=2026-12
Response: {
  "form": "B01-DN",
  "period": "2026-12",
  "line_items": [
    { "code": "A", "label": "TÀI SẢN NGẮN HẠN", "current_year": 5000000000, "previous_year": 4500000000 }
  ]
}
```

### 4.5 Tax Declarations

```
POST /api/v1/tax/vat/calculate?period=2026-04
Response: { "input_vat": 50000000, "output_vat": 80000000, "payable": 30000000 }

POST /api/v1/tax/vat/submit?period=2026-04
Response: { "submission_ref": "GDT-2026-04-001", "status": "submitted" }
```

---

## 5. UI/UX SPECIFICATIONS

### 5.1 Layout Structure
```
┌─────────────────────────────────────────────────────────┐
│  LOGO  │  Search  │  Notifications  │  User Menu       │  ← Header (64px)
├────────┼────────────────────────────────────────────────┤
│        │                                                 │
│  Nav   │  Main Content Area                             │
│  Menu  │  (Dynamic based on route)                      │
│        │                                                 │
│  - GL  │                                                 │
│  - AR  │                                                 │
│  - AP  │                                                 │
│  - Tax │                                                 │
│  - ... │                                                 │
│        │                                                 │
└────────┴─────────────────────────────────────────────────┘
```

### 5.2 Key Screen Specifications

#### 5.2.1 Journal Entry Screen
- **Left Panel:** Entry form (Date, Description, Type, Currency)
- **Center Panel:** Lines grid (Account, Debit, Credit, Description, Cost Center)
- **Right Panel:** Validation status, Approval button, Audit trail
- **Validation:** Real-time balance check (Debit vs Credit), account code autocomplete
- **Keyboard Shortcuts:** `Ctrl+S` (Save), `Ctrl+Enter` (Submit), `Esc` (Cancel)

#### 5.2.2 E-Invoice Creation Screen
- **Step 1:** Select customer (autocomplete with tax code)
- **Step 2:** Add line items (product/service, qty, price, VAT rate)
- **Step 3:** Review & Sign (digital signature prompt)
- **Step 4:** Send to CQT (progress indicator, success/failure status)

#### 5.2.3 Dashboard (Role-Based)
- **Chief Accountant:** Pending approvals, Period status, Reconciliation alerts, Tax deadlines
- **AR Accountant:** Overdue invoices, Collection rate, Customer aging chart
- **CFO:** Cash position, Revenue vs Budget, Profit margin, Working capital metrics

---

## 6. DETAILED FUNCTIONAL LOGIC

### 6.1 Journal Entry Posting Logic
```python
def post_journal_entry(entry_id: UUID, approver_id: UUID):
    entry = db.get(JournalEntry, entry_id)
    
    # 1. Validate balance
    if entry.total_debit != entry.total_credit:
        raise ValidationError("Entry unbalanced")
    
    # 2. Validate period
    period = db.get(AccountingPeriod, entry.period)
    if period.status != 'open':
        raise ValidationError(f"Period {period.period} is {period.status}")
    
    # 3. Check approval threshold
    if entry.total_debit > threshold and entry.approved_by is None:
        raise ValidationError("Approval required")
    
    # 4. Update status
    entry.status = 'posted'
    entry.approved_by = approver_id
    entry.posted_at = now()
    
    # 5. Update account balances (atomic transaction)
    for line in entry.lines:
        update_account_balance(line.account_code, line.debit_amount, line.credit_amount)
    
    # 6. Log audit
    audit_log(action='POST_ENTRY', entity_id=entry_id, user_id=approver_id)
    
    db.commit()
```

### 6.2 VAT Calculation Logic
```python
def calculate_vat(period: str):
    input_vat = db.query(
        func.sum(JournalEntryLine.debit_amount)
    ).filter(
        JournalEntryLine.account_code.in_(['1331', '1332']),
        JournalEntry.period == period
    ).scalar() or 0
    
    output_vat = db.query(
        func.sum(JournalEntryLine.credit_amount)
    ).filter(
        JournalEntryLine.account_code.in_(['33311', '33312']),
        JournalEntry.period == period
    ).scalar() or 0
    
    payable = output_vat - input_vat
    
    return {
        "input_vat": input_vat,
        "output_vat": output_vat,
        "payable": payable if payable > 0 else 0,
        "refundable": abs(payable) if payable < 0 else 0
    }
```

### 6.3 Payroll Calculation Logic
```python
def calculate_payroll(employee: Employee, period: str):
    base = employee.base_salary
    insurance_base = min(base, 20 * BASE_SALARY_2026)
    
    # Employee deductions
    bhxh = insurance_base * 0.08
    hyt = insurance_base * 0.015
    bhtn = insurance_base * 0.01
    
    # PIT calculation
    personal_deduction = 11_000_000
    dependent_deduction = employee.dependents_count * 4_400_000
    taxable_income = base - bhxh - hyt - bhtn - personal_deduction - dependent_deduction
    
    pit = calculate_progressive_tax(taxable_income) if taxable_income > 0 else 0
    
    net = base - bhxh - hyt - bhtn - pit
    
    return PayrollRecord(
        employee_id=employee.id,
        period=period,
        gross_salary=base,
        bhxh_employee=bhxh,
        hyt_employee=hyt,
        bhtn_employee=bhtn,
        pit_withheld=pit,
        net_salary=net
    )
```

### 6.4 Bank Reconciliation Matching Algorithm
```python
def match_bank_transactions(bank_stmt: List[BankTransaction], system_tx: List[Transaction]):
    matched = []
    unmatched = []
    
    for stmt in bank_stmt:
        # Auto-match by amount + date tolerance (±2 days)
        match = system_tx.find(
            lambda t: abs(t.amount - stmt.amount) < 0.01 
            and abs((t.date - stmt.date).days) <= 2
        )
        if match:
            matched.append({"statement": stmt, "system": match, "confidence": "high"})
        else:
            unmatched.append(stmt)
            
    return matched, unmatched
```

---

## 7. SECURITY IMPLEMENTATION

### 7.1 Authentication Flow
1. User submits email + password
2. Backend verifies bcrypt hash
3. If 2FA enabled, request TOTP code
4. Generate JWT (RS256) with 30-min expiry
5. Return access_token + refresh_token (HTTP-only cookie)

### 7.2 Authorization Middleware
```python
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    token = request.headers.get("Authorization")
    if not token:
        return JSONResponse(status_code=401, content={"detail": "Missing token"})
    
    payload = verify_jwt(token)
    request.state.user_id = payload["sub"]
    request.state.tenant_id = payload["tenant_id"]
    request.state.role = payload["role"]
    
    # Check route permissions
    if not has_permission(request.state.role, request.url.path):
        return JSONResponse(status_code=403, content={"detail": "Forbidden"})
    
    return await call_next(request)
```

### 7.3 Data Encryption
- **At Rest:** AES-256 for sensitive columns (salary, bank accounts)
- **In Transit:** TLS 1.3 enforced
- **Passwords:** bcrypt (cost factor 12)
- **Digital Signatures:** SHA-256 + RSA-2048 via PKCS#11 HSM

---

## 8. INTEGRATION IMPLEMENTATION

### 8.1 Tax Authority (GDT)
- **Protocol:** HTTPS POST with mutual TLS
- **Payload:** XML per GDT schema
- **Retry:** Exponential backoff (3 attempts)
- **Fallback:** Manual XML export for HTKK import

### 8.2 E-Invoice Provider
- **Adapter Pattern:** `InvoiceProvider` interface with implementations for VNPT, Viettel, BKAV
- **Configuration:** Tenant selects provider; system routes via adapter
- **Webhook:** Listen for CQT confirmation callbacks

### 8.3 Bank Integration
- **Import:** SFTP poller (cron every 15 min)
- **Format:** MT940 parser → normalized `BankTransaction` model
- **Export:** Payment file generation (CSV/XML per bank spec)

---

## 9. DEPLOYMENT & INFRASTRUCTURE

### 9.1 Environment Setup
```
├── production/     (AWS Vietnam Region)
├── staging/        (AWS Vietnam Region)
└── development/    (Local Docker Compose)
```

### 9.2 CI/CD Pipeline
1. **Commit** → GitHub Actions trigger
2. **Lint** → ruff, mypy, eslint
3. **Test** → pytest (unit), playwright (e2e)
4. **Build** → Docker image
5. **Deploy** → Helm chart to Kubernetes
6. **Verify** → Health check + smoke tests

### 9.3 Monitoring
- **Logs:** ELK Stack (Elasticsearch, Logstash, Kibana)
- **Metrics:** Prometheus + Grafana
- **Alerts:** PagerDuty integration for P0 incidents
- **APM:** OpenTelemetry tracing

---

**END OF SOFTWARE FUNCTIONAL SPECIFICATION**

**Document Control:**

| Version | Date | Author | Changes | Approved By |
|---------|------|--------|---------|-------------|
| 1.0 | April 2026 | System Analyst Office | Initial release | — |

**Sign-Off:**

| Role | Name | Signature | Date |
|------|------|-----------|------|
| System Analyst | | | |
| Tech Lead | | | |
| Lead BA | | | |
| QA Lead | | | |
