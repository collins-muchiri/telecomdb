import os
from cryptography.fernet import Fernet
from pathlib import Path

def generate_encryption_key():
    """Generate a new encryption key."""
    key = Fernet.generate_key()
    return key.decode()

def create_env_file():
    """Create or update the .env file with necessary configuration."""
    env_path = Path('.env')
    
    # Generate new encryption key
    encryption_key = generate_encryption_key()
    
    # Read template from .env.example
    with open('.env.example', 'r') as f:
        env_content = f.read()
    
    # Replace placeholder encryption key
    env_content = env_content.replace('your_encryption_key_here', encryption_key)
    
    # Write to .env file
    with open(env_path, 'w') as f:
        f.write(env_content)
    
    print(f"Created/updated .env file with new encryption key: {encryption_key}")
    print("Please review and update the database credentials in the .env file.")

def create_directories():
    """Create necessary directories."""
    directories = ['exports', 'tests', 'schema']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"Created directory: {directory}")

def install_dependencies():
    """Install required Python packages."""
    print("Installing dependencies...")
    os.system('pip install -r requirements.txt')

def main():
    """Main setup function."""
    print("Setting up Telecom Billing System...")
    
    # Create necessary directories
    create_directories()
    
    # Install dependencies
    install_dependencies()
    
    # Create/update .env file
    create_env_file()
    
    print("\nSetup completed successfully!")
    print("\nNext steps:")
    print("1. Review and update the database credentials in the .env file")
    print("2. Run 'python telecom_billing.py' to start the application")

if __name__ == "__main__":
    main() 