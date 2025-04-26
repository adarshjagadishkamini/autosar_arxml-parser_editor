import os
import autosar
from lxml import etree
from src.arxml_parser import ARXMLParser
from src.utils.backup import create_backup, restore_backup, cleanup_old_backups
from src.utils.logger import ARXMLLogger

class ARXMLEditor:
    def __init__(self):
        self.parser = ARXMLParser()
        self.current_file = None
        self.logger = ARXMLLogger().get_logger()
        
    def load(self, file_path):
        """Load an ARXML file for editing"""
        self.current_file = file_path
        self.logger.info(f"Loading ARXML file for editing: {file_path}")
        return self.parser.load_file(file_path)
    
    def save(self, output_path):
        """Save the modified ARXML file with backup"""
        if not self.parser.workspace:
            self.logger.error("No workspace loaded")
            return False
            
        try:
            # Create backup before saving
            if os.path.exists(output_path):
                backup_path = create_backup(output_path)
                if backup_path:
                    self.logger.info(f"Created backup: {backup_path}")
                    
            self.parser.workspace.saveXML(output_path)
            self.logger.info(f"Saved ARXML file to: {output_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving ARXML file: {e}")
            return False
    
    def restore_from_backup(self, backup_path=None):
        """Restore file from backup"""
        if not self.current_file:
            self.logger.error("No file currently loaded")
            return False
            
        return restore_backup(self.current_file, backup_path)
    
    def cleanup_backups(self, keep_days=30):
        """Clean up old backup files"""
        if not self.current_file:
            self.logger.error("No file currently loaded")
            return False
            
        cleanup_old_backups(self.current_file, keep_days)
        return True

    def _validate_parameter_value(self, param, value):
        """Validate parameter value against its constraints"""
        try:
            # Find parameter constraints if they exist
            param_type = param.find('TYPE-TREF', namespaces=self.parser.ns)
            if param_type is None:
                return True
                
            # Find data constraints
            data_type = self.parser.get_element_by_ref(param_type.text)
            if data_type is None:
                return True
                
            constr_ref = data_type.find('.//DATA-CONSTR-REF', namespaces=self.parser.ns)
            if constr_ref is None:
                return True
                
            # Get constraints
            constraints = self.parser.get_element_by_ref(constr_ref.text)
            if constraints is None:
                return True
                
            # Check value against constraints
            rules = constraints.findall('.//DATA-CONSTR-RULE', namespaces=self.parser.ns)
            for rule in rules:
                lower = rule.find('.//LOWER-LIMIT', namespaces=self.parser.ns)
                upper = rule.find('.//UPPER-LIMIT', namespaces=self.parser.ns)
                
                if lower is not None and upper is not None:
                    try:
                        val = float(value)
                        low = float(lower.text)
                        high = float(upper.text)
                        if not (low <= val <= high):
                            return False
                    except ValueError:
                        # If value can't be converted to float, skip numeric validation
                        pass
                        
            return True
        except Exception as e:
            self.logger.error(f"Error during parameter validation: {e}")
            return False

    def update_parameter_value(self, param_name, new_value):
        """Update a parameter value with validation"""
        if not self.parser.workspace:
            self.logger.error("No workspace loaded")
            return False
            
        try:
            # Find parameter by name
            param = self.parser.root.find(f'.//*[SHORT-NAME="{param_name}"]', namespaces=self.parser.ns)
            if param is None:
                self.logger.error(f"Parameter '{param_name}' not found")
                return False
                
            # Validate new value
            if not self._validate_parameter_value(param, new_value):
                self.logger.error(f"Invalid value '{new_value}' for parameter '{param_name}'")
                return False
                
            # Update parameter value
            value_elem = param.find('.//VALUE/NUMERICAL-VALUE-SPECIFICATION/VALUE', namespaces=self.parser.ns)
            if value_elem is not None:
                value_elem.text = str(new_value)
                return True
            else:
                self.logger.error(f"Value element not found for parameter '{param_name}'")
                return False
        except Exception as e:
            self.logger.error(f"Error updating parameter: {e}")
            return False
    
    def update_component_name(self, old_name, new_name):
        """Update a software component name"""
        if not self.parser.workspace:
            self.logger.error("No workspace loaded")
            return False
            
        try:
            # Find component by name
            component = self.parser.workspace.find(f'**/ComponentType[@name="{old_name}"]')
            if component is None:
                self.logger.error(f"Component '{old_name}' not found")
                return False
                
            # Update component name
            component.name = new_name
            return True
        except Exception as e:
            self.logger.error(f"Error updating component name: {e}")
            return False
    
    def merge_arxml(self, other_file_path):
        """Merge another ARXML file into the current workspace"""
        if not self.parser.workspace:
            self.logger.error("No workspace loaded")
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
            self.logger.error(f"Error merging ARXML files: {e}")
            return False
    
    def add_software_component(self, name, category="APPLICATION_SOFTWARE_COMPONENT"):
        """Add a new software component"""
        if not self.parser.workspace:
            self.logger.error("No workspace loaded")
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
            self.logger.error(f"Error adding software component: {e}")
            return False