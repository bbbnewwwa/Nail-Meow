import subprocess
from datetime import datetime
from pathlib import Path
import shutil

def backup_sqlite():
    """Резервное копирование SQLite базы данных"""
    db_path = Path("nailmeow.db")
    backup_dir = Path("backups")
    backup_dir.mkdir(exist_ok=True)
    
    if db_path.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"nailmeow_backup_{timestamp}.db"
        shutil.copy2(db_path, backup_path)
        print(f" Backup created: {backup_path}")
        return backup_path
    else:
        print(" Database file not found")
        return None

def backup_postgresql(database_url: str):
    """Резервное копирование PostgreSQL базы данных"""
    backup_dir = Path("backups")
    backup_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = backup_dir / f"nailmeow_backup_{timestamp}.sql"
    
    # Парсинг URL базы данных
    # Format: postgresql://user:password@host:port/dbname
    try:
        from urllib.parse import urlparse
        parsed = urlparse(database_url)
        
        cmd = f"pg_dump {database_url} > {backup_file}"
        subprocess.run(cmd, shell=True, check=True)
        print(f" PostgreSQL backup created: {backup_file}")
        return backup_file
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return None

if __name__ == "__main__":
    print(" Starting backup...")
    
    # Для SQLite
    backup_sqlite()
    
    # Для PostgreSQL (раскомментируйте если используете)
    # from app.config import settings
    # backup_postgresql(settings.DATABASE_URL)
    
    print(" Backup completed!")