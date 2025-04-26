import os
import sys
import unittest
import tempfile
import glob
from src.utils import backup

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
    
    def test_backup_creation(self):
        """Test backup creation when saving"""
        # Add a component and save
        self.editor.add_software_component("BackupTest")
        result = self.editor.save(self.temp_file.name)
        self.assertTrue(result, "Failed to save with backup")
        
        # Check if backup was created
        backup_dir = os.path.join(os.path.dirname(self.temp_file.name), '.arxml_backups')
        self.assertTrue(os.path.exists(backup_dir), "Backup directory not created")
        
        backups = glob.glob(os.path.join(backup_dir, f"{os.path.basename(self.temp_file.name)}.*"))
        self.assertTrue(len(backups) > 0, "No backup file created")
    
    def test_backup_restore(self):
        """Test restoring from backup"""
        # Load the sample file
        self.editor.load(self.sample_file)
        
        # Add a component that should be restored from backup
        self.editor.add_software_component("OriginalComponent")
        
        # Create a temp file and save to it
        with tempfile.NamedTemporaryFile(suffix='.arxml', delete=False) as tf:
            test_file = tf.name
            
        # Save which should create a backup
        self.editor.save(test_file)
        
        # Get the latest backup file
        backup_pattern = os.path.join(backup.BACKUP_DIR, os.path.basename(test_file) + '.*.bak')
        backup_files = glob.glob(backup_pattern)
        latest_backup = max(backup_files, key=os.path.getctime)
        
        # Add a new component
        self.editor.add_software_component("NewComponent")
        self.editor.save(test_file)
        
        # Restore from backup
        self.assertTrue(self.editor.restore_from_backup(latest_backup))
        
        # Verify the original component is restored
        components = self.editor.get_software_components()
        found = any(c.name == "OriginalComponent" for c in components)
        self.assertTrue(found, "Original component not restored from backup")
        
        # Cleanup
        try:
            os.unlink(test_file)
            os.unlink(latest_backup)
        except:
            pass

if __name__ == '__main__':
    unittest.main()