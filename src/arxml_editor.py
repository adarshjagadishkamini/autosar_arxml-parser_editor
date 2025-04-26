"""ARXML Editor class for modifying AUTOSAR XML files"""
import os
import autosar
from .arxml_parser import ARXMLParser
from .utils import backup
from .utils.logger import ARXMLLogger

class ARXMLEditor:
    def __init__(self):
        self.parser = ARXMLParser()
        self.current_file = None
        self.logger = ARXMLLogger().get_logger()
    
    def load(self, file_path):
        """Load an ARXML file for editing"""
        self.logger.info(f"Loading ARXML file for editing: {file_path}")
        try:
            self.current_file = file_path
            return self.parser.load_file(file_path)
        except Exception as e:
            self.logger.error(f"Error loading file: {e}")
            return False
    
    def save(self, file_path=None):
        """Save changes to ARXML file"""
        if not file_path and not self.current_file:
            self.logger.error("No file path specified for save operation")
            return False
            
        save_path = file_path or self.current_file
        
        try:
            # Create backup before saving
            if os.path.exists(save_path):
                backup_path = backup.create_backup(save_path)
                if backup_path:
                    self.logger.info(f"Created backup: {backup_path}")
            
            # Ensure all required packages exist
            if not hasattr(self.parser, 'app_components_pkg'):
                self.parser.init_default_packages()
            
            # Save the file
            try:
                self.parser.workspace.saveXML(save_path)
                self.logger.info(f"Saved ARXML file to: {save_path}")
                
                # Update current file path if saving to new location
                if file_path:
                    self.current_file = file_path
                    
                return True
            except Exception as e:
                self.logger.error(f"Error saving ARXML file: {e}")
                return False
                    
        except Exception as e:
            self.logger.error(f"Error during save operation: {e}")
            return False
    
    def restore_from_backup(self, backup_file):
        """Restore from a backup file"""
        if not backup_file or not os.path.exists(backup_file):
            self.logger.error(f"Backup file not found: {backup_file}")
            return False

        try:
            # Restore file content from backup
            if not backup.restore_from_backup(self.current_file, backup_file):
                return False
            # Recreate parser and reload file
            self.parser = ARXMLParser()
            if not self.load(self.current_file):
                self.logger.error("Failed to reload file after restore")
                return False
            return True
        except Exception as e:
            self.logger.error(f"Error restoring from backup: {e}")
            return False
    
    def add_software_component(self, name):
        """Add a new software component"""
        if not self.parser.workspace:
            self.logger.error("No ARXML file loaded")
            return False
            
        try:
            # Create component using parser
            component = self.parser.create_software_component(name)
            if component:
                self.logger.info(f"Added software component: {name}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error adding software component: {e}")
            return False
            
    def get_software_components(self):
        """Get list of software components"""
        return self.parser.get_software_components()
        
    def cleanup_old_backups(self, keep_days=30):
        """Clean up old backup files"""
        if not self.current_file:
            return False
        return cleanup_old_backups(self.current_file, keep_days)