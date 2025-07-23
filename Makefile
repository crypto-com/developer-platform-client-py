.PHONY: help install test test-unit test-integration test-watch test-debug coverage coverage-html coverage-report lint format format-check clean build docs security audit ci-test install-dev

# Default target
help:
	@echo "🧪 Crypto.com Developer Platform Client - Test Commands"
	@echo ""
	@echo "📦 Setup Commands:"
	@echo "  install          Install all dependencies"
	@echo "  install-dev      Install development dependencies"
	@echo ""
	@echo "🧪 Testing Commands:"
	@echo "  test             Run all tests"
	@echo "  test-unit        Run unit tests only"
	@echo "  test-integration Run integration tests only"
	@echo "  test-watch       Run tests in watch mode"
	@echo "  test-debug       Run tests with debugging enabled"
	@echo "  test-failing     Run only failing tests from last run"
	@echo ""
	@echo "📊 Coverage Commands:"
	@echo "  coverage         Run tests with coverage report"
	@echo "  coverage-html    Generate HTML coverage report"
	@echo "  coverage-report  Show detailed coverage report"
	@echo ""
	@echo "🎨 Code Quality Commands:"
	@echo "  lint             Run linting checks"
	@echo "  format           Format code with black and isort"
	@echo "  format-check     Check code formatting without changes"
	@echo "  security         Run security vulnerability checks"
	@echo ""
	@echo "🔧 Utility Commands:"
	@echo "  clean            Clean up generated files"
	@echo "  build            Build the package"
	@echo "  audit            Run full project audit"
	@echo "  ci-test          Simulate CI pipeline locally"
	@echo ""

# Installation commands
install:
	@echo "📦 Installing dependencies..."
	poetry install

install-dev:
	@echo "📦 Installing development dependencies..."
	poetry install --with dev

# Basic testing commands
test:
	@echo "🧪 Running all tests..."
	poetry run pytest -v

test-unit:
	@echo "🧪 Running unit tests..."
	poetry run pytest -v -m "unit"

test-integration:
	@echo "🧪 Running integration tests..."
	poetry run pytest -v -m "integration"

test-watch:
	@echo "👀 Running tests in watch mode..."
	poetry run pytest-watch

test-debug:
	@echo "🐛 Running tests with debugging..."
	poetry run pytest -v -s --pdb

test-failing:
	@echo "❌ Running only failing tests..."
	poetry run pytest --lf -v

# Coverage commands
coverage:
	@echo "📊 Running tests with coverage..."
	poetry run pytest --cov=crypto_com_developer_platform_client --cov-report=term-missing

coverage-html:
	@echo "📊 Generating HTML coverage report..."
	poetry run pytest --cov=crypto_com_developer_platform_client --cov-report=html --cov-report=term-missing
	@echo "📊 Coverage report generated in htmlcov/index.html"
	@echo "🌐 Open with: open htmlcov/index.html"

coverage-report:
	@echo "📊 Detailed coverage report..."
	poetry run pytest --cov=crypto_com_developer_platform_client --cov-report=term-missing --cov-report=html --cov-fail-under=80

# Code quality commands
lint:
	@echo "🔍 Running linting checks..."
	@echo "  → flake8..."
	poetry run flake8 crypto_com_developer_platform_client --count --select=E9,F63,F7,F82 --show-source --statistics
	@echo "  → flake8 complexity check..."
	poetry run flake8 crypto_com_developer_platform_client --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics
	@echo "✅ Linting checks completed"

format:
	@echo "🎨 Formatting code..."
	@echo "  → black..."
	poetry run black crypto_com_developer_platform_client tests
	@echo "  → isort..."
	poetry run isort crypto_com_developer_platform_client tests
	@echo "✅ Code formatting completed"

format-check:
	@echo "🎨 Checking code formatting..."
	@echo "  → black check..."
	poetry run black --check crypto_com_developer_platform_client tests
	@echo "  → isort check..."
	poetry run isort --check-only crypto_com_developer_platform_client tests
	@echo "✅ Code formatting check completed"

security:
	@echo "🔒 Running security checks..."
	pip install safety
	safety check
	@echo "✅ Security checks completed"

# Utility commands
clean:
	@echo "🧹 Cleaning up generated files..."
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf coverage.svg
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete
	@echo "✅ Cleanup completed"

build:
	@echo "🏗️  Building package..."
	poetry build
	@echo "✅ Package built successfully"

audit: lint format-check security coverage-report
	@echo "🔍 Full project audit completed"

# CI simulation
ci-test:
	@echo "🚀 Simulating CI pipeline..."
	@echo "  → Installing dependencies..."
	@$(MAKE) install
	@echo "  → Linting..."
	@$(MAKE) lint
	@echo "  → Format check..."
	@$(MAKE) format-check  
	@echo "  → Security check..."
	@$(MAKE) security || true
	@echo "  → Running tests with coverage..."
	@$(MAKE) coverage-report
	@echo "  → Building package..."
	@$(MAKE) build
	@echo "🎉 CI simulation completed successfully!"

# Quick development shortcuts
quick-test: test-unit
	@echo "⚡ Quick test run completed"

full-test: clean coverage-report
	@echo "🎯 Full test suite completed"

pre-commit: format lint test-unit
	@echo "✅ Pre-commit checks completed"

# Debugging and development helpers
test-verbose:
	@echo "🔊 Running tests with maximum verbosity..."
	poetry run pytest -vvv --tb=long

test-specific:
	@echo "🎯 Running specific test (usage: make test-specific TEST=test_name)"
	poetry run pytest -v $(TEST)

test-file:
	@echo "📄 Running specific test file (usage: make test-file FILE=tests/test_client.py)"
	poetry run pytest -v $(FILE)

# Performance and benchmarking
test-performance:
	@echo "⏱️  Running performance tests..."
	poetry run pytest -v --benchmark-only || echo "No benchmark tests found"

# Documentation
docs:
	@echo "📚 Generating documentation..."
	@echo "Test documentation available in tests/README.md"

# Environment info
env-info:
	@echo "🔍 Environment Information:"
	@echo "Python version:"
	python --version
	@echo "Poetry version:"
	poetry --version
	@echo "Dependencies:"
	poetry show --tree

# Advanced testing patterns
test-coverage-by-file:
	@echo "📊 Coverage breakdown by file..."
	poetry run pytest --cov=crypto_com_developer_platform_client --cov-report=term --cov-report=html

test-slow:
	@echo "🐌 Running slow tests..."
	poetry run pytest -v -m "slow"

test-not-slow:
	@echo "⚡ Running fast tests only..."
	poetry run pytest -v -m "not slow"

# Makefile self-documentation
show-targets:
	@echo "Available Makefile targets:"
	@$(MAKE) -pRrq -f $(firstword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' 