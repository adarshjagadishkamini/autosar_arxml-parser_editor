import os
import sys
# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.arxml_parser import ARXMLParser
from src.arxml_editor import ARXMLEditor

def sample_workflow():
    """Example workflow using the ARXML parser and editor"""
    # Check if sample file exists, if not create a minimal one
    sample_file = "examples/sample.arxml"
    
    if not os.path.exists(sample_file):
        print("Sample file does not exist. Please create a sample ARXML file first.")
        return
    
    # Parse the file
    parser = ARXMLParser()
    if parser.load_file(sample_file):
        print(f"Successfully loaded {sample_file}")
        
        # Display components
        components = parser.get_software_components()
        print(f"Found {len(components)} software components:")
        for comp in components:
            print(f"- {comp.name} ({comp.category})")
        
        # Display parameters
        params = parser.get_parameters()
        print(f"\nFound {len(params)} parameters:")
        for param in params:
            print(f"- {param.name}: {param.value}")
    
    # Edit the file
    editor = ARXMLEditor()
    if editor.load(sample_file):
        # Add a new component
        editor.add_software_component("NewTestComponent")
        
        # Update a parameter if it exists
        if params:
            editor.update_parameter_value(params[0].name, "new_value")
        
        # Save to a new file
        editor.save("examples/modified_sample.arxml")
        print("Saved modified ARXML to examples/modified_sample.arxml")

if __name__ == "__main__":
    sample_workflow()