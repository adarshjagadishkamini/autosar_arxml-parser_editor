"""Utility functions for managing ARXML file backups"""
import os
import glob
import shutil
import time
from datetime import datetime, timedelta
from .logger import ARXMLLogger

logger = ARXMLLogger().get_logger()

BACKUP_DIR = '/tmp/.arxml_backups'
os.makedirs(BACKUP_DIR, exist_ok=True)

def create_backup(file_path):
    """Create a backup of an ARXML file"""
    if not os.path.exists(file_path):
        return None
        
    # Create backup filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = os.path.basename(file_path) + '.' + timestamp + '.bak'
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    
    try:
        shutil.copy2(file_path, backup_path)
        return backup_path
    except Exception:
        return None

def restore_from_backup(file_path, backup_file):
    """Restore ARXML file from backup"""
    try:
        if not os.path.exists(backup_file):
            logger.error(f"Backup file not found: {backup_file}")
            return False
            
        # First make sure we can read the backup
        try:
            with open(backup_file, 'r') as f:
                backup_content = f.read()
        except Exception as e:
            logger.error(f"Error reading backup file: {e}")
            return False
            
        # Create a temporary backup of current file
        current_backup = None
        if os.path.exists(file_path):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            current_backup = os.path.join(BACKUP_DIR, f"pre_restore_{timestamp}.bak")
            try:
                shutil.copy2(file_path, current_backup)
            except Exception as e:
                logger.warning(f"Could not backup current file: {e}")
                
        # Write backup content to original file
        try:
            with open(file_path, 'w') as f:
                f.write(backup_content)
            return True
        except Exception as e:
            logger.error(f"Error writing restored content: {e}")
            # Try to restore previous version if we have it
            if current_backup and os.path.exists(current_backup):
                try:
                    shutil.copy2(current_backup, file_path)
                except:
                    pass
            return False
            
    except Exception as e:
        logger.error(f"Error in restore operation: {e}")
        return False

def cleanup_old_backups(file_path, keep_days=30):
    """Remove backups older than specified number of days"""
    try:
        pattern = os.path.join(BACKUP_DIR, os.path.basename(file_path) + '.*.bak')
        backups = glob.glob(pattern)
        
        cutoff = time.time() - (keep_days * 24 * 60 * 60)
        
        for backup in backups:
            if os.path.getmtime(backup) < cutoff:
                try:
                    os.remove(backup)
                except OSError:
                    pass
        return True
    except Exception:
        return False