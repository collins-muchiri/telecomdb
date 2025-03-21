import time
from functools import wraps
from typing import Dict, Optional
import jwt
from datetime import datetime, timedelta
from config import ENCRYPTION_KEY

class RateLimiter:
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = {}

    def is_rate_limited(self, client_id: str) -> bool:
        current_time = time.time()
        
        # Clean old requests
        if client_id in self.requests:
            self.requests[client_id] = [
                req_time for req_time in self.requests[client_id]
                if current_time - req_time < self.window_seconds
            ]
        else:
            self.requests[client_id] = []

        # Check rate limit
        if len(self.requests[client_id]) >= self.max_requests:
            return True

        # Add new request
        self.requests[client_id].append(current_time)
        return False

    def get_remaining_requests(self, client_id: str) -> int:
        current_time = time.time()
        if client_id in self.requests:
            active_requests = [
                req_time for req_time in self.requests[client_id]
                if current_time - req_time < self.window_seconds
            ]
            return max(0, self.max_requests - len(active_requests))
        return self.max_requests

class APIKeyManager:
    def __init__(self):
        self.api_keys: Dict[str, dict] = {}

    def generate_api_key(self, client_name: str, permissions: list) -> str:
        """Generate a new API key for a client."""
        key = jwt.encode(
            {
                'client': client_name,
                'permissions': permissions,
                'created_at': datetime.utcnow().isoformat(),
                'exp': datetime.utcnow() + timedelta(days=365)
            },
            ENCRYPTION_KEY,
            algorithm='HS256'
        )
        self.api_keys[key] = {
            'client_name': client_name,
            'permissions': permissions,
            'created_at': datetime.utcnow()
        }
        return key

    def validate_api_key(self, api_key: str) -> Optional[dict]:
        """Validate an API key and return client information."""
        try:
            payload = jwt.decode(api_key, ENCRYPTION_KEY, algorithms=['HS256'])
            if api_key in self.api_keys:
                return self.api_keys[api_key]
            return None
        except jwt.InvalidTokenError:
            return None

    def revoke_api_key(self, api_key: str) -> bool:
        """Revoke an API key."""
        if api_key in self.api_keys:
            del self.api_keys[api_key]
            return True
        return False

# Initialize rate limiter and API key manager
rate_limiter = RateLimiter()
api_key_manager = APIKeyManager()

def require_api_key(permissions: list = None):
    """Decorator to require API key authentication."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            api_key = kwargs.get('api_key')
            if not api_key:
                raise ValueError("API key is required")

            # Check rate limit
            if rate_limiter.is_rate_limited(api_key):
                raise Exception("Rate limit exceeded")

            # Validate API key
            client_info = api_key_manager.validate_api_key(api_key)
            if not client_info:
                raise ValueError("Invalid API key")

            # Check permissions if specified
            if permissions:
                if not all(perm in client_info['permissions'] for perm in permissions):
                    raise ValueError("Insufficient permissions")

            return f(*args, **kwargs)
        return decorated_function
    return decorator 