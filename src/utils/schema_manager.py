"""Utility for managing AUTOSAR XML schemas"""
import os
import logging
import requests
from lxml import etree

class SchemaManager:
    SCHEMA_URLS = {
        'AUTOSAR_4-3-0': 'https://www.autosar.org/fileadmin/standards/R4-3/AUTOSAR_MMOD_XMLSchema.xsd',
        'AUTOSAR_4-2-2': 'https://www.autosar.org/fileadmin/standards/R4-2/AUTOSAR_MMOD_XMLSchema.xsd'
    }
    
    def __init__(self, schema_dir=None):
        if schema_dir is None:
            schema_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'schemas')
        self.schema_dir = schema_dir
        os.makedirs(self.schema_dir, exist_ok=True)
        self.logger = logging.getLogger('arxml_tool')
    
    def get_schema(self, version='AUTOSAR_4-3-0'):
        """Get schema for validation, downloading if needed"""
        schema_path = os.path.join(self.schema_dir, f'{version}.xsd')
        
        if not os.path.exists(schema_path):
            self._download_schema(version, schema_path)
            
        if os.path.exists(schema_path):
            try:
                return etree.XMLSchema(etree.parse(schema_path))
            except Exception as e:
                self.logger.warning(f"Error loading schema: {e}")
                return None
        return None
    
    def _download_schema(self, version, schema_path):
        """Download schema from AUTOSAR website"""
        if version not in self.SCHEMA_URLS:
            self.logger.warning(f"No URL found for schema version {version}")
            return False
            
        try:
            url = self.SCHEMA_URLS[version]
            response = requests.get(url)
            if response.status_code == 200:
                with open(schema_path, 'wb') as f:
                    f.write(response.content)
                self.logger.info(f"Downloaded schema to {schema_path}")
                return True
            else:
                self.logger.warning(f"Failed to download schema: HTTP {response.status_code}")
                return False
        except Exception as e:
            self.logger.warning(f"Error downloading schema: {e}")
            return False