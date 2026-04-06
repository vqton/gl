.PHONY: help install run test test-cov lint format clean db-init db-migrate db-upgrade shell

help:
	@echo "Available commands:"
	@echo "  install      Install dependencies"
	@echo "  run          Run Flask development server"
	@echo "  test         Run tests with pytest"
	@echo "  test-cov     Run tests with coverage report"
	@echo "  lint         Run flake8 linting"
	@echo "  format       Format code with black and isort"
	@echo "  clean        Remove cache and build files"
	@echo "  db-init      Initialize database"
	@echo "  db-migrate   Create database migration"
	@echo "  db-upgrade   Apply database migrations"
	@echo "  shell        Open Flask shell"

install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install

run:
	flask run --host=0.0.0.0 --port=5000 --reload

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html

lint:
	flake8 app/ tests/ --max-line-length=100
	black --check app/ tests/
	isort --check-only app/ tests/

format:
	black app/ tests/
	isort app/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache .coverage htmlcov/ build/ dist/
	rm -f data-dev.sqlite data-test.sqlite

db-init:
	flask db init
	flask db migrate -m "Initial migration"
	flask db upgrade

db-migrate:
	flask db migrate -m "$(message)"

db-upgrade:
	flask db upgrade

shell:
	flask shell
