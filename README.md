# AUTOSAR ARXML Parser & Editor

A minimal Python tool for editing AUTOSAR ARXML files. Provides basic features to load, modify, and save ARXML files, with backup and restore support.

## Features
- Load ARXML files
- Add software components
- Save ARXML files (with automatic backup)
- Restore ARXML files from backup (basic, see Known Issues)
- List software components

## Known Issues
- The restore from backup feature is basic and may not always fully revert all changes, especially if the ARXML structure changes significantly.
- Some warnings/errors may appear if the ARXML file contains unsupported or custom AUTOSAR roles.

## License
MIT
