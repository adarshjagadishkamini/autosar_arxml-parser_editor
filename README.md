# ARXML Parser and Editor
A command-line tool for parsing, modifying, and writing AUTOSAR XML (ARXML) files.

## Features
- Parse ARXML files
- View software components, parameters, and ports
- Update parameter values with validation
- Rename software components
- Add new software components
- Merge multiple ARXML files

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/arxml-tool.git
cd arxml-tool

# Install in development mode
pip install -e .
```

## Usage

The tool provides several commands:

### Display ARXML Information
```bash
arxml info path/to/file.arxml
```

### Update Parameter Value
```bash
arxml update-param path/to/file.arxml param_name new_value
```

### Rename Component
```bash
arxml rename-component path/to/file.arxml old_name new_name
```

### Add New Component
```bash
arxml add-component path/to/file.arxml component_name
```

### Merge ARXML Files
```bash
arxml merge base.arxml other.arxml output.arxml
```

## Options

Most commands support the following options:
- `--output`, `-o`: Specify output file path (default: overwrites input)

## Example Usage

```python
from src.arxml_parser import ARXMLParser
from src.arxml_editor import ARXMLEditor

# Parse an ARXML file
parser = ARXMLParser()
parser.load_file("example.arxml")

# Edit the file
editor = ARXMLEditor()
editor.load("example.arxml")
editor.add_software_component("NewComponent")
editor.update_parameter_value("MaxSpeed", "200")
editor.save("modified.arxml")
```

## Development

To run tests:
```bash
python -m unittest discover tests
```

## Requirements
- Python >= 3.6
- autosar-python >= 0.3.2
- lxml >= 4.9.0
- click >= 8.0.0
