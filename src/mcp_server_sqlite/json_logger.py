"""JSON logging utilities"""
import json
import logging
from datetime import datetime

class JsonLogger:
    """JSON-based logging for database operations"""
    
    def __init__(self, config):
        self.config = config
        self.enabled = config.get('enabled', True)
        self.logger = logging.getLogger('json_logger')
    
    def log_operation(self, operation, data):
        """Log database operation"""
        if self.enabled:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'operation': operation,
                'data': data
            }
            self.logger.info(f"Operation: {json.dumps(log_entry)}")
    
    def log_error(self, error, context):
        """Log error with context"""
        if self.enabled:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'error': str(error),
                'error_type': type(error).__name__,
                'context': context
            }
            self.logger.error(f"Error: {json.dumps(log_entry)}")