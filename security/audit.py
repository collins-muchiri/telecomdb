import logging
from datetime import datetime
from pathlib import Path
import json
from typing import Any, Dict, Optional
from config import LOG_FILE

class AuditLogger:
    def __init__(self, log_file: str = LOG_FILE):
        self.logger = logging.getLogger('audit')
        self.logger.setLevel(logging.INFO)
        
        # Create logs directory if it doesn't exist
        log_path = Path(log_file)
        log_path.parent.mkdir(exist_ok=True)
        
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)

    def log_event(
        self,
        event_type: str,
        user_id: str,
        action: str,
        details: Optional[Dict[str, Any]] = None,
        status: str = 'success',
        error: Optional[str] = None
    ):
        """Log an audit event with all relevant details."""
        event = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'user_id': user_id,
            'action': action,
            'status': status,
            'details': details or {},
            'error': error
        }
        
        # Log to file
        self.logger.info(json.dumps(event))
        
        # Log to console if status is error
        if status == 'error':
            self.logger.error(f"Error in {event_type}: {error}")

    def log_login(self, user_id: str, ip_address: str, status: str = 'success'):
        """Log user login attempts."""
        self.log_event(
            event_type='login',
            user_id=user_id,
            action='authentication',
            details={'ip_address': ip_address},
            status=status
        )

    def log_data_access(
        self,
        user_id: str,
        resource_type: str,
        resource_id: str,
        action: str,
        status: str = 'success'
    ):
        """Log data access events."""
        self.log_event(
            event_type='data_access',
            user_id=user_id,
            action=action,
            details={
                'resource_type': resource_type,
                'resource_id': resource_id
            },
            status=status
        )

    def log_config_change(
        self,
        user_id: str,
        config_key: str,
        old_value: Any,
        new_value: Any,
        status: str = 'success'
    ):
        """Log configuration changes."""
        self.log_event(
            event_type='config_change',
            user_id=user_id,
            action='update',
            details={
                'config_key': config_key,
                'old_value': old_value,
                'new_value': new_value
            },
            status=status
        )

    def log_security_event(
        self,
        event_type: str,
        user_id: str,
        details: Dict[str, Any],
        status: str = 'success',
        error: Optional[str] = None
    ):
        """Log security-related events."""
        self.log_event(
            event_type=f'security_{event_type}',
            user_id=user_id,
            action='security_event',
            details=details,
            status=status,
            error=error
        )

# Initialize audit logger
audit_logger = AuditLogger() 