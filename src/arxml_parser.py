"""ARXML Parser class for handling AUTOSAR XML files"""
import os
import autosar
from lxml import etree

from src.utils.logger import ARXMLLogger
from src.utils.schema_manager import SchemaManager

class ARXMLParser:
    def __init__(self):
        self.workspace = autosar.workspace()
        self.root = None
        self.ns = None  # Namespace
        self.logger = ARXMLLogger().get_logger()
        self.schema_manager = SchemaManager()
        
        # Initialize default packages
        self.init_default_packages()
    
    def init_default_packages(self):
        """Initialize default AUTOSAR packages"""
        try:
            # Create main packages with proper roles
            self.datatypes_pkg = self.workspace.createPackage('DataTypes', role='DataType')
            self.component_pkg = self.workspace.createPackage('ComponentTypes', role='ComponentType')
            self.constants_pkg = self.workspace.createPackage('Constants', role='Constant')
            self.system_pkg = self.workspace.createPackage('System', role='SystemDesign')  # Fixed role name
            self.portinterface_pkg = self.workspace.createPackage('PortInterfaces', role='PortInterface')
            
            # Create application components package
            self.app_components_pkg = self.component_pkg.createSubPackage('ApplicationComponents')
            
            return True
        except Exception as e:
            self.logger.error(f"Error initializing packages: {e}")
            return False
    
    def _validate_schema(self, xml_doc):
        """Validate ARXML against schema"""
        try:
            schema_location = self.root.get('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation')
            if not schema_location:
                self.logger.warning("No schema location found in ARXML file")
                return True
                
            locations = schema_location.split()
            if len(locations) < 2:
                self.logger.warning("Invalid schema location format")
                return True
                
            # Get schema version from location
            schema_file = locations[1].split('/')[-1]  # Get filename
            version = schema_file.split('.')[0]  # Extract version part
            
            # Get schema
            schema = self.schema_manager.get_schema(version)
            if schema is None:
                self.logger.warning("Could not load schema, skipping validation")
                return True
                
            try:
                schema.assertValid(xml_doc)
                return True
            except etree.DocumentInvalid as e:
                self.logger.error(f"Schema validation failed: {e}")
                return False
                
        except Exception as e:
            self.logger.error(f"Schema validation error: {e}")
            return False
    
    def load_file(self, file_path):
        """Load and parse an ARXML file with schema validation"""
        if not os.path.exists(file_path):
            self.logger.error(f"ARXML file not found: {file_path}")
            raise FileNotFoundError(f"ARXML file not found: {file_path}")
            
        if not file_path.lower().endswith('.arxml'):
            self.logger.error("Invalid file extension. File must be an ARXML file")
            raise ValueError("File must be an ARXML file")
            
        try:
            self.logger.info(f"Loading ARXML file: {file_path}")
            
            # Create fresh workspace
            self.workspace = autosar.workspace()
            
            # Load existing content first
            try:
                self.workspace.loadXML(file_path)
            except Exception as e:
                self.logger.error(f"Error loading XML content: {e}")
                return False
            
            # Initialize/reinitialize packages after loading to ensure proper structure
            self.init_default_packages()
            
            # Parse with lxml for XML manipulation
            try:
                xml_doc = etree.parse(file_path)
                self.root = xml_doc.getroot()
                
                # Extract namespace
                self.ns = self._extract_namespace(self.root)
                
                # Validate against schema
                if not self._validate_schema(xml_doc):
                    self.logger.warning("ARXML file validation failed")
                    # Continue loading even if validation fails
                
                self.logger.info("Successfully loaded ARXML file")
                return True
            except Exception as e:
                self.logger.error(f"XML parsing error: {e}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error parsing ARXML file: {e}")
            return False
    
    def _extract_namespace(self, root):
        """Extract namespace from ARXML root element"""
        ns = {}
        for prefix, uri in root.nsmap.items():
            if prefix is None:
                ns['default'] = uri
            else:
                ns[prefix] = uri
        return ns
    
    def get_software_components(self):
        """Get all software components"""
        if not self.workspace:
            return []
            
        components = []
        try:
            # First check the application components package
            app_components = self.workspace.findall("/ComponentTypes/ApplicationComponents/ApplicationSoftwareComponent")
            if app_components:
                components.extend(app_components)
            
            # Then check the main component package
            main_components = self.workspace.findall("/ComponentTypes/ApplicationSoftwareComponent")
            if main_components:
                components.extend(main_components)
                
        except Exception as e:
            self.logger.error(f"Error getting software components: {e}")
            
        return components
    
    def get_parameters(self):
        """Get all parameter definitions"""
        if not self.workspace:
            return []
            
        parameters = []
        if hasattr(self, 'datatypes_pkg'):
            parameters.extend(self.datatypes_pkg.findall('/ParameterDef'))
        return parameters
    
    def get_ports(self):
        """Get all ports defined in the ARXML"""
        if not self.workspace:
            return []
            
        ports = []
        if hasattr(self, 'portinterface_pkg'):
            ports.extend(self.portinterface_pkg.findall('/PortInterface'))
        return ports
    
    def get_element_by_xpath(self, xpath):
        """Get elements by XPath"""
        if not self.root:
            return None
            
        try:
            return self.root.xpath(xpath, namespaces=self.ns)
        except Exception as e:
            self.logger.error(f"XPath error: {e}")
            return None
    
    def get_element_by_ref(self, reference):
        """Get element by AUTOSAR reference"""
        if not self.workspace:
            return None
            
        try:
            return self.workspace.find(reference)
        except Exception as e:
            self.logger.error(f"Reference error: {e}")
            return None
            
    def create_software_component(self, name):
        """Create a new software component"""
        try:
            # Ensure packages exist
            if not hasattr(self, 'app_components_pkg'):
                self.init_default_packages()
            
            # Create basic software component in application components package
            swc = self.app_components_pkg.createApplicationSoftwareComponent(name)
            
            if swc:
                self.logger.info(f"Added software component: {name}")
                return swc
            return None
        except Exception as e:
            self.logger.error(f"Error creating software component: {e}")
            return None
            
    def print_structure(self, indent=""):
        """Print the ARXML structure in a hierarchical format"""
        if not self.workspace:
            print("No workspace loaded")
            return

        print("\nAR-PACKAGES:")
        for package in self.root.findall('.//AR-PACKAGE', namespaces=self.ns):
            name = package.find('SHORT-NAME', namespaces=self.ns)
            if name is not None:
                print(f"{indent}├── {name.text}")
                elements = package.find('ELEMENTS', namespaces=self.ns)
                if elements is not None:
                    for elem in elements:
                        elem_name = elem.find('SHORT-NAME', namespaces=self.ns)
                        if elem_name is not None:
                            print(f"{indent}│   ├── {elem.tag.split('}')[-1]}: {elem_name.text}")