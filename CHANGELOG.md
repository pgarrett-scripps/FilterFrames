# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0]

### Changed
- Minimum Python version raised from 3.8 to 3.9
- Added Python 3.12 and 3.13 to CI test matrix
- Updated GitHub Actions to v4/v5 for checkout and setup-python
- Improved exception chaining (`raise ... from exc`) for better tracebacks
- Renamed type alias from `FILE_TYPES` to `FileTypes` (PEP 8 compliance)
- Added `py.typed` marker for PEP 561 typed package support
- Added logging throughout the parsing pipeline
- Added input validation for malformed DTASelect-filter files
- Added `pytest-cov` for test coverage reporting in CI
- Expanded test suite with input type, error handling, and data integrity tests
- Modernized `pyproject.toml` with optional `[dev]` dependencies and tool configs
- Removed legacy `setup.py` (not needed with modern pip)
- Fixed potential crash when `end_lines` is empty
- Pinned minimum pandas version to `>=1.5`

## [0.1.3]

### Changed
- `_get_lines` now works with streamlit uploaded file, and any io-type
