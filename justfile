# List available recipes
default:
    @just --list

# Install the package with dev dependencies
install:
    pip install -e ".[dev]"

# Run all checks (lint, format, typecheck, test)
check: lint format typecheck test

# Run ruff linter
lint:
    ruff check src/ tests/

# Check code formatting
format:
    ruff format --check src/ tests/

# Auto-fix lint issues and format code
fix:
    ruff check --fix src/ tests/
    ruff format src/ tests/

# Run ty type checker
typecheck:
    ty check src/

# Run tests
test *args:
    pytest {{ args }}

# Run tests with coverage
test-cov:
    pytest --cov=filterframes --cov-report=term-missing

# Build the package
build:
    python -m build
