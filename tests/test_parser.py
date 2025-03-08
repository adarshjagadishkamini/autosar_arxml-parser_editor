import os
import sys
import unittest

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.arxml_parser import ARXMLParser
from src.arxml_editor import ARXMLEditor

class TestARXMLParser(unittest.TestCase):
    def setUp(self):
        # Path to sample ARXML file for testing
        self.sample_file = os.path.join(os.path.dirname(__file__), '..', 'examples', 'sample.arxml')
        
        # Make sure the sample file exists
        if not os.path.exists(self.sample_file):
            self.skipTest("Sample ARXML file not found")
        
        # Create parser instance
        self.parser = ARXMLParser()
    
    def test_load_file(self):
        """Test loading an ARXML file"""
        result = self.parser.load_file(self.sample_file)
        self.assertTrue(result, "Failed to load ARXML file")
    
    def test_get_software_components(self):
        """Test retrieving software components"""
        self.parser.load_file(self.sample_file)
        components = self.parser.get_software_components()
        self.assertIsNotNone(components, "Software components list is None")
    
    def test_get_parameters(self):
        """Test retrieving parameters"""
        self.parser.load_file(self.sample_file)
        params = self.parser.get_parameters()
        self.assertIsNotNone(params, "Parameters list is None")
    
    def test_invalid_file(self):
        """Test loading an invalid file"""
        with self.assertRaises(FileNotFoundError):
            self.parser.load_file("non_existent_file.arxml")

if __name__ == '__main__':
    unittest.main()