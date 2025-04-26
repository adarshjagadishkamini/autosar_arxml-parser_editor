# AUTOSAR ARXML Parser & Editor

A minimal Python tool for editing AUTOSAR ARXML files. Provides basic features to load, modify, and save ARXML files, with backup and restore support.

## Features
- Load ARXML files
- Add software components
- Save ARXML files (with automatic backup)
- Restore ARXML files from backup (basic, see Known Issues)
- List software components

## Installation

Clone the repository and install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Programmatic Example

```python
from src.arxml_editor import ARXMLEditor

editor = ARXMLEditor()
editor.load("examples/sample.arxml")
editor.add_software_component("MyComponent")
editor.save()
components = editor.get_software_components()
print(components)
```

### CLI Example

If a CLI is provided in `src/main.py`:

```bash
python src/main.py --help
```

## Manual Verification Steps

1. **Load an ARXML file**
   - Use the editor to load `examples/sample.arxml`.
2. **Add a software component**
   - Add a new component and save the file.
   - Open the ARXML file and check that the new component appears.
3. **Backup and Restore**
   - Save the file to trigger a backup.
   - Modify the ARXML file (e.g., remove a component).
   - Use the restore function to revert from the latest backup.
   - Check if the ARXML file is reverted to its previous state (note: this may not be perfect due to current limitations).
4. **List software components**
   - Use the `get_software_components()` method to list all components and verify the output.

## Known Issues
- The restore from backup feature is basic and may not always fully revert all changes, especially if the ARXML structure changes significantly.
- Some warnings/errors may appear if the ARXML file contains unsupported or custom AUTOSAR roles.

## License
MIT
