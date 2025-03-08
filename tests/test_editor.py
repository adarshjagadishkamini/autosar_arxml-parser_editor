import os
import sys
import unittest
import tempfile

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.arxml_editor import ARXMLEditor

class TestARXMLEditor(unittest.TestCase):
    def setUp(self):
        # Path to sample ARXML file for testing
        self.sample_file = os.path.join(os.path.dirname(__file__), '..', 'examples', 'sample.arxml')
        
        # Make sure the sample file exists
        if not os.path.exists(self.sample_file):
            self.skipTest("Sample ARXML file not found")
        
        # Create editor instance
        self.editor = ARXMLEditor()
        self.editor.load(self.sample_file)
        
        # Create temp file for saving
        self.temp_file = tempfile.NamedTemporaryFile(suffix='.arxml', delete=False)
        self.temp_file.close()
    
    def tearDown(self):
        # Remove temp file
        if hasattr(self, 'temp_file') and os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_save_file(self):
        """Test saving an ARXML file"""
        result = self.editor.save(self.temp_file.name)
        self.assertTrue(result, "Failed to save ARXML file")
        self.assertTrue(os.path.exists(self.temp_file.name), "Saved file does not exist")
    
    def test_add_component(self):
        """Test adding a software component"""
        result = self.editor.add_software_component("TestComponent")
        self.assertTrue(result, "Failed to add software component")
    
    def test_save_and_reload(self):
        """Test saving and reloading a file"""
        # Add a component
        self.editor.add_software_component("TestReloadComponent")
        
        # Save
        self.editor.save(self.temp_file.name)
        
        # Reload
        new_editor = ARXMLEditor()
        load_result = new_editor.load(self.temp_file.name)
        self.assertTrue(load_result, "Failed to reload saved ARXML file")

if __name__ == '__main__':
    unittest.main()