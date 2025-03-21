import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Database Configuration
DB_CONFIG = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

# Test Database Configuration
TEST_DB_CONFIG = {
    'dbname': os.getenv('TEST_DB_NAME'),
    'user': os.getenv('TEST_DB_USER'),
    'password': os.getenv('TEST_DB_PASSWORD'),
    'host': os.getenv('TEST_DB_HOST'),
    'port': os.getenv('TEST_DB_PORT')
}

# Encryption Configuration
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')

# Export Configuration
EXPORT_DIR = Path(os.getenv('EXPORT_DIR', 'exports'))
EXPORT_FILENAME = os.getenv('EXPORT_FILENAME', 'secure_bills_export.csv')

# Bill Generation Configuration
DEFAULT_DUE_DATE_DAYS = int(os.getenv('DEFAULT_DUE_DATE_DAYS', '30'))
DEFAULT_PAYMENT_STATUS = os.getenv('DEFAULT_PAYMENT_STATUS', 'Pending')

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'telecom_billing.log')

def validate_config():
    """Validate the configuration settings."""
    required_vars = [
        'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT',
        'ENCRYPTION_KEY'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    # Create export directory if it doesn't exist
    EXPORT_DIR.mkdir(exist_ok=True) 