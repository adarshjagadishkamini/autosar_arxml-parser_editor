import os
import autosar
from lxml import etree

class ARXMLParser:
    def __init__(self):
        self.workspace = None
        self.root = None
        self.ns = None  # Namespace
        
    def load_file(self, file_path):
        """Load and parse an ARXML file"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"ARXML file not found: {file_path}")
            
        if not file_path.lower().endswith('.arxml'):
            raise ValueError("File must be an ARXML file")
            
        try:
            # Parse using lxml for direct XML manipulation if needed
            self.root = etree.parse(file_path).getroot()
            
            # Extract namespace
            self.ns = self._extract_namespace(self.root)
            
            # Parse using autosar-python library
            self.workspace = autosar.workspace()
            self.workspace.loadXML(file_path)
            
            return True
        except Exception as e:
            print(f"Error parsing ARXML file: {e}")
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
            print(f"XPath error: {e}")
            return None
    
    def get_element_by_ref(self, reference):
        """Get element by AUTOSAR reference"""
        if not self.workspace:
            return None
            
        try:
            return self.workspace.find(reference)
        except Exception as e:
            print(f"Reference error: {e}")
            return None
            
    def print_structure(self):
        """Print the ARXML structure"""
        if not self.workspace:
            print("No workspace loaded")
            return
            
        self.workspace.display()