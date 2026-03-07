import subprocess
from datetime import datetime

def backup_database():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"backup_nailmeow_{timestamp}.sql"
    
    command = f"pg_dump postgresql://user:password@localhost:5432/nailmeow > {filename}"
    subprocess.run(command, shell=True)
    print(f"Backup created: {filename}")

if __name__ == "__main__":
    backup_database()