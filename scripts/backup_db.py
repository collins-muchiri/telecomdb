import os
import subprocess
from datetime import datetime
from pathlib import Path
import shutil
from config import DB_CONFIG

def create_backup():
    """Create a database backup with timestamp."""
    # Create backups directory if it doesn't exist
    backup_dir = Path('backups')
    backup_dir.mkdir(exist_ok=True)
    
    # Generate timestamp for backup file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = backup_dir / f'backup_{timestamp}.sql'
    
    # Construct pg_dump command
    cmd = [
        'pg_dump',
        '-h', DB_CONFIG['host'],
        '-p', DB_CONFIG['port'],
        '-U', DB_CONFIG['user'],
        '-d', DB_CONFIG['dbname'],
        '-F', 'c',  # Custom format (compressed)
        '-f', str(backup_file)
    ]
    
    # Set PGPASSWORD environment variable
    env = os.environ.copy()
    env['PGPASSWORD'] = DB_CONFIG['password']
    
    try:
        # Execute backup
        subprocess.run(cmd, env=env, check=True)
        print(f"Backup created successfully: {backup_file}")
        
        # Compress backup
        shutil.make_archive(str(backup_file), 'zip', backup_dir, backup_file.name)
        backup_file.unlink()  # Remove uncompressed file
        
        # Rotate old backups (keep last 7 days)
        rotate_backups(backup_dir)
        
    except subprocess.CalledProcessError as e:
        print(f"Error creating backup: {e}")
        raise

def rotate_backups(backup_dir, days_to_keep=7):
    """Remove backups older than specified days."""
    current_time = datetime.now()
    for backup_file in backup_dir.glob('backup_*.zip'):
        file_time = datetime.fromtimestamp(backup_file.stat().st_mtime)
        age = (current_time - file_time).days
        if age > days_to_keep:
            backup_file.unlink()
            print(f"Removed old backup: {backup_file}")

if __name__ == '__main__':
    create_backup() 