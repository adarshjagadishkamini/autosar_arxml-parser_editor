import os
try:
    import autosar
except ImportError:
    print("Error: autosar-python library not found. Please install it using 'pip install autosar'")
    raise
try:
    from lxml import etree
except ImportError:
    print("Error: lxml library not found. Please install it using 'pip install lxml'")
    raise

from src.utils.logger import ARXMLLogger

class ARXMLParser:
    def __init__(self):
        self.workspace = None
        self.root = None
        self.ns = None  # Namespace
        self.logger = ARXMLLogger().get_logger()
        
    def _validate_schema(self, xml_doc):
        """Validate ARXML against the AUTOSAR schema"""
        try:
            # Extract schema location from the root element
            schema_location = self.root.get('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation')
            if not schema_location:
                self.logger.warning("No schema location found in ARXML file")
                return True
                
            # Parse schema locations
            locations = schema_location.split()
            if len(locations) < 2:
                self.logger.warning("Invalid schema location format")
                return True
                
            # Get schema URL (usually the last entry in even positions)
            schema_url = locations[-1]
            
            try:
                # Try to fetch and parse the schema
                schema_doc = etree.parse(schema_url)
                schema = etree.XMLSchema(schema_doc)
                
                # Validate document
                schema.assertValid(xml_doc)
                return True
            except etree.DocumentInvalid as e:
                self.logger.error(f"ARXML validation error: {e}")
                return False
            except Exception as e:
                self.logger.warning(f"Schema validation warning: {e}")
                return True  # Continue despite schema validation issues
                
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
            # Parse using lxml for direct XML manipulation if needed
            xml_doc = etree.parse(file_path)
            self.root = xml_doc.getroot()
            
            # Extract namespace
            self.ns = self._extract_namespace(self.root)
            
            # Validate against schema
            if not self._validate_schema(xml_doc):
                self.logger.warning("ARXML file does not validate against schema")
            
            # Parse using autosar-python library
            self.workspace = autosar.workspace()
            self.workspace.loadXML(file_path)
            self.logger.info("Successfully loaded ARXML file")
            
            return True
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
            
        return self.workspace.findall('/*/ComponentType')
    
    def get_parameters(self):
        """Get all parameter definitions"""
        if not self.workspace:
            return []
            
        return self.workspace.findall('/*/ParameterDef')
    
    def get_ports(self):
        """Get all ports defined in the ARXML"""
        if not self.workspace:
            return []
            
        return self.workspace.findall('/*/PortInterface')
    
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