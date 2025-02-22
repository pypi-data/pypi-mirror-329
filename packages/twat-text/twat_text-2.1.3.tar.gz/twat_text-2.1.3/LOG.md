---
this_file: LOG.md
---

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

*No unreleased changes yet.*

## [v0.0.1] - 2025-02-15

Initial release of the twat-text package.

### Added

- Basic project structure with modern Python packaging (PEP 621 compliance)
- Initial implementation of `twat_text.py` with:
  - Type hints and dataclass-based configuration
  - Basic logging setup
  - Process data function skeleton
- Development workflow setup with Hatch
- Basic test suite configuration
- MIT License
- Project documentation in README.md

### Changed

- Moved `src/twat_text.py` to `src/twat_text/twat_text.py` for better package structure
- Updated .gitignore to exclude `_private` directory

### Technical Details

- Added proper type hints using modern Python syntax (|)
- Implemented error handling with proper exception messages
- Set up logging with debug mode support
- Added `__future__.annotations` import for modern type hint handling

[Unreleased]: https://github.com/twardoch/twat-text/compare/v0.0.1...HEAD
[v0.0.1]: https://github.com/twardoch/twat-text/releases/tag/v0.0.1 
