"""Utility module for handling ARXML file backups"""
import os
import shutil
from datetime import datetime
import glob

def create_backup(file_path):
    """Create a backup of an ARXML file"""
    if not os.path.exists(file_path):
        return None
        
    # Create backups directory if it doesn't exist
    backup_dir = os.path.join(os.path.dirname(file_path), '.arxml_backups')
    os.makedirs(backup_dir, exist_ok=True)
    
    # Generate backup filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = os.path.basename(file_path)
    backup_path = os.path.join(backup_dir, f"{filename}.{timestamp}.bak")
    
    try:
        shutil.copy2(file_path, backup_path)
        return backup_path
    except Exception as e:
        print(f"Error creating backup: {e}")
        return None

def restore_backup(file_path, backup_path=None):
    """Restore an ARXML file from backup"""
    backup_dir = os.path.join(os.path.dirname(file_path), '.arxml_backups')
    
    if not backup_path:
        # Find most recent backup
        backups = glob.glob(os.path.join(backup_dir, f"{os.path.basename(file_path)}.*"))
        if not backups:
            print("No backups found")
            return False
        backup_path = max(backups, key=os.path.getctime)
    
    if not os.path.exists(backup_path):
        print(f"Backup file not found: {backup_path}")
        return False
        
    try:
        shutil.copy2(backup_path, file_path)
        return True
    except Exception as e:
        print(f"Error restoring backup: {e}")
        return False

def cleanup_old_backups(file_path, keep_days=30):
    """Remove backups older than specified days"""
    backup_dir = os.path.join(os.path.dirname(file_path), '.arxml_backups')
    if not os.path.exists(backup_dir):
        return
        
    current_time = datetime.now().timestamp()
    max_age = keep_days * 24 * 60 * 60  # Convert days to seconds
    
    try:
        for backup in glob.glob(os.path.join(backup_dir, f"{os.path.basename(file_path)}.*")):
            if current_time - os.path.getctime(backup) > max_age:
                os.remove(backup)
    except Exception as e:
        print(f"Error cleaning up old backups: {e}")