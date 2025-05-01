# AUTOSAR ARXML Parser and Editor Documentation

## Overview
This project provides tools to parse, edit, and manage AUTOSAR ARXML files. It includes a command-line interface, core parsing and editing modules, utilities for backup and logging, and a suite of tests.

---

## Project Structure

- **src/**: Main source code directory
  - **arxml_parser.py**: Parses ARXML files, extracts software components, and provides access to ARXML data structures.
  - **arxml_editor.py**: Provides editing capabilities for ARXML files, such as adding or removing software components, and saving changes.
  - **main.py**: Command-line interface for interacting with the parser and editor.
  - **models/**: Contains data models used by the parser and editor.
  - **utils/**: Utility modules
    - **backup.py**: Handles backup and restore operations for ARXML files.
    - **logger.py**: Configures and manages logging for the tool.
    - **schema_manager.py**: Manages ARXML schema files and validation (with warnings if schema is missing).

- **examples/**: Example files and usage
  - **example_usage.py**: Example script demonstrating how to use the parser/editor programmatically.
  - **sample.arxml**: Sample ARXML file for testing and demonstration.

- **logs/**: Log files generated during tool operation and test runs.

- **tests/**: Unit tests
  - **test_parser.py**: Tests for ARXML parsing functionality.
  - **test_editor.py**: Tests for ARXML editing, backup, and restore features.

- **schemas/**: Directory for ARXML schema files (used for validation).

- **README.md**: Project overview, installation, and usage instructions.
- **setup.py**: Python package setup script.

---

## Main Components

### arxml_parser.py
- Loads and parses ARXML files.
- Extracts software components and other relevant data.
- Handles missing or unhandled ARXML types with warnings.

### arxml_editor.py
- Provides methods to add, remove, and list software components.
- Supports saving ARXML files and creating backups.
- Can attempt to restore from backup (with known limitations).

### main.py
- Command-line interface for loading, editing, and saving ARXML files.
- Supports listing and adding components via CLI commands.

### utils/
- **backup.py**: Manages file backup and restore operations.
- **logger.py**: Sets up logging for all operations and errors.
- **schema_manager.py**: Downloads and manages ARXML schemas, validates files if schema is available.

### models/
- Contains data models and classes representing ARXML entities.

### tests/
- **test_parser.py**: Verifies parsing, extraction, and error handling.
- **test_editor.py**: Verifies editing, backup, and restore features. Includes a test for backup restore that currently fails due to a known limitation.

---

## Known Limitations
- Some ARXML element types (e.g., `INTEGER-TYPE`, `System`) are not fully handled and will generate warnings.
- The backup restore feature does not fully revert to the original state in all cases.
- Schema validation is skipped if the schema cannot be downloaded.

---

## Logging
- All operations, warnings, and errors are logged to files in the `logs/` directory for traceability and debugging.

---

## Example Usage
See `examples/example_usage.py` for a programmatic example, or use the CLI via `main.py` for interactive editing.

---

For further details, refer to the source code and README.md.
