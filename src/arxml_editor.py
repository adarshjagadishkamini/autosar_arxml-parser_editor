import os
import autosar
from lxml import etree
from src.arxml_parser import ARXMLParser

class ARXMLEditor:
    def __init__(self):
        self.parser = ARXMLParser()
        
    def load(self, file_path):
        """Load an ARXML file for editing"""
        return self.parser.load_file(file_path)
    
    def save(self, output_path):
        """Save the modified ARXML file"""
        if not self.parser.workspace:
            print("No workspace loaded")
            return False
            
        try:
            self.parser.workspace.saveXML(output_path)
            print(f"ARXML file saved to: {output_path}")
            return True
        except Exception as e:
            print(f"Error saving ARXML file: {e}")
            return False
    
    def update_parameter_value(self, param_name, new_value):
        """Update a parameter value"""
        if not self.parser.workspace:
            print("No workspace loaded")
            return False
            
        try:
            # Find parameter by name
            param = self.parser.workspace.find(f'**/ParameterDef[@name="{param_name}"]')
            if param is None:
                print(f"Parameter '{param_name}' not found")
                return False
                
            # Update parameter value
            param.value = new_value
            return True
        except Exception as e:
            print(f"Error updating parameter: {e}")
            return False
    
    def update_component_name(self, old_name, new_name):
        """Update a software component name"""
        if not self.parser.workspace:
            print("No workspace loaded")
            return False
            
        try:
            # Find component by name
            component = self.parser.workspace.find(f'**/ComponentType[@name="{old_name}"]')
            if component is None:
                print(f"Component '{old_name}' not found")
                return False
                
            # Update component name
            component.name = new_name
            return True
        except Exception as e:
            print(f"Error updating component name: {e}")
            return False
    
    def merge_arxml(self, other_file_path):
        """Merge another ARXML file into the current workspace"""
        if not self.parser.workspace:
            print("No workspace loaded")
            return False
            
        try:
            # Create temporary workspace for the other file
            temp_workspace = autosar.workspace()
            temp_workspace.loadXML(other_file_path)
            
            # Merge workspaces (simplified, actual merging is more complex)
            # This is a basic approach - real merging needs conflict resolution
            for package in temp_workspace.packages:
                if package.name not in [p.name for p in self.parser.workspace.packages]:
                    self.parser.workspace.append(package)
            
            return True
        except Exception as e:
            print(f"Error merging ARXML files: {e}")
            return False
    
    def add_software_component(self, name, category="APPLICATION_SOFTWARE_COMPONENT"):
        """Add a new software component"""
        if not self.parser.workspace:
            print("No workspace loaded")
            return False
            
        try:
            # Find or create components package
            components_pkg = None
            for pkg in self.parser.workspace.packages:
                if pkg.role == "ComponentType":
                    components_pkg = pkg
                    break
            
            if components_pkg is None:
                components_pkg = self.parser.workspace.createPackage("Components", role="ComponentType")
            
            # Create new component
            swc = components_pkg.createApplicationSoftwareComponent(name)
            return True
        except Exception as e:
            print(f"Error adding software component: {e}")
            return False