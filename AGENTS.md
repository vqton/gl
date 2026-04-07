# AGENTS.md — Vietnamese Accounting Software (Circular 99/2025)

Flask web app for Vietnamese enterprise accounting, compliant with Circular 99/2025/TT-BTC.

## Project Structure

```
app/
├── __init__.py          # create_app() factory, blueprints, error handlers
├── extensions.py        # db, migrate, login_manager, bcrypt
├── models/              # SQLAlchemy ORM (layered architecture)
├── services/            # Business logic (CRUD, calculations)
├── views/               # Flask Blueprints (controllers/routes)
├── templates/           # Jinja2 templates
└── static/              # CSS, JS
tests/
├── conftest.py          # Fixtures: app, db, client, admin_user, accountant_user
├── models/              # Model unit tests
├── services/            # Service unit tests
└── views/               # Route/integration tests
```

## Commands

### Install & Run
```bash
make install              # pip install + pre-commit
make run                  # flask run --host=0.0.0.0 --port=5000
```

### Database
```bash
make db-init              # flask db init + migrate + upgrade
make db-migrate message="msg"  # Create new migration
make db-upgrade           # Apply migrations
```

### Tests (TDD — write tests BEFORE implementation)
```bash
make test                 # Run all tests
make test-cov             # Run with coverage report

# Run a single test file:
pytest tests/models/test_account.py --no-cov -v

# Run a single test method:
pytest tests/models/test_account.py::TestAccountModel::test_create_account --no-cov -v

# Run a single test class:
pytest tests/services/test_account_service.py::TestAccountService --no-cov -v

# Run with debugger on failure:
pytest tests/ --tb=long --no-cov -x
```

### Lint & Format
```bash
make lint                 # flake8 + black --check + isort --check
make format               # black + isort (auto-fix)
make clean                # Remove cache/build files
```

### CI
Pre-commit hooks run on every commit. GitHub Actions runs on push/PR.

## Architecture

**Layered pattern:** `models → services → views`
- **Models** (`app/models/`): SQLAlchemy ORM, inherit from `BaseModel`
- **Services** (`app/services/`): Business logic, static methods, no Flask imports
- **Views** (`app/views/`): Flask Blueprints, handle HTTP, call services

Each module has its own blueprint: `gl`, `ar`, `ap`, `tax`, `payroll`, `fa`, `inventory`, `reports`, `admin`, `auth`, `main`.

## Code Style

### Imports
```python
# Standard library first
import os
from datetime import datetime

# Third party
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

# Application
from app.services.account_service import AccountService
from app.models.account import Account
```
Use `isort` (configured in `pyproject.toml`) for automatic sorting.

### Formatting
- **Black** with `line-length = 100`
- No trailing whitespace, always end file with newline
- Pre-commit enforces formatting on commit

### Naming Conventions
| Element | Convention | Example |
|---------|-----------|---------|
| Variables/functions | snake_case | `get_by_code`, `entry_date` |
| Classes | PascalCase | `AccountService`, `JournalEntry` |
| Constants | UPPER_SNAKE_CASE | `VAT_RATE_STANDARD` |
| Blueprint vars | `*_bp` suffix | `gl_bp`, `auth_bp` |
| Test classes | `Test*` prefix | `TestAccountModel` |
| Test methods | `test_*` prefix | `test_create_account` |
| Template files | snake_case | `journal_entries.html` |

### Types
- Use SQLAlchemy column types: `db.Column(db.String(255))`, `db.Numeric(18, 2)`
- Service methods use `@staticmethod` — no `self`
- Return domain objects or raise `ValueError` on errors
- View functions return `render_template()`, `redirect()`, or `jsonify()`

### Error Handling
- **Services**: Raise `ValueError` with descriptive messages
- **Views**: Catch `ValueError`, flash message, redirect or re-render
- **Models**: Use `@property` for computed fields, `@classmethod` for queries
- **500 errors**: Always `db.session.rollback()` before rendering error page

### Database
- All models inherit from `BaseModel` (`id`, `created_at`, `updated_at`, `is_active`)
- `BaseModel.save()` / `delete()` / `update()` do NOT commit — caller commits
- Services call `db.session.commit()` after mutations
- Use `db.session.get(Model, id)` instead of legacy `Model.query.get(id)`

### Testing
- **TDD methodology**: Write test first, then implementation
- Use `pytest` with `--no-cov` flag (coverage hangs on Python 3.13 + WSL2)
- Each test gets a fresh in-memory SQLite DB via `StaticPool`
- Fixtures: `app`, `db`, `client`, `admin_user`, `accountant_user`
- Tests that don't need DB should NOT use `db` fixture
- Use `pytest.raises(ValueError, match="pattern")` for error assertions

### Templates
- Extend `layouts/base.html`
- Use `session.get('user_id')` for auth checks (not `current_user`)
- Vietnamese labels for UI, English for code/comments
- Error templates: `errors/400.html`, `403.html`, `404.html`, `500.html`

### Circular 99 Compliance
- Account codes follow Circular 99/2025/TT-BTC structure (3-6 digits)
- Account types: `asset`, `liability`, `equity`, `revenue`, `expense`
- Use `Account.get_circular99_accounts()` to seed the standard chart of accounts
- Financial reports: B01-DN, B02-DN, B03-DN, B09-DN
