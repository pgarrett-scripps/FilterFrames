# List available recipes
default:
    @just --list

# Install the package with dev dependencies
install:
    uv sync --extra dev

# Run all checks (lint, format, typecheck, test)
check: lint format typecheck test

# Run ruff linter
lint:
    uvx ruff check src/ tests/

# Check code formatting
format:
    uvx ruff format --check src/ tests/

# Auto-fix lint issues and format code
fix:
    uvx ruff check --fix src/ tests/
    uvx ruff format src/ tests/

# Run ty type checker
typecheck:
    uvx ty check src/

# Run tests
test *args:
    uv run pytest {{ args }}

# Run tests with coverage
test-cov:
    uv run pytest --cov=filterframes --cov-report=term-missing

# Build the package
build:
    uv build
