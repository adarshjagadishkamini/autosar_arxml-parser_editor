"""Logging utility for ARXML parser and editor"""
import logging
import os
from datetime import datetime

class ARXMLLogger:
    def __init__(self, log_dir=None):
        if log_dir is None:
            log_dir = os.path.join(os.getcwd(), 'logs')
            
        os.makedirs(log_dir, exist_ok=True)
        
        # Create log filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = os.path.join(log_dir, f'arxml_tool_{timestamp}.log')
        
        # Configure logging
        self.logger = logging.getLogger('arxml_tool')
        self.logger.setLevel(logging.DEBUG)
        
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatting
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def get_logger(self):
        """Get the configured logger"""
        return self.logger