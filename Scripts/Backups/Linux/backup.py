# Nahuel Ivan Troisi

import os
import time
import tarfile
import logging
import json
import shutil

# Load configuration from the file
with open("/home/whippy/Descargas/backup_config", "r") as f:
    config = json.load(f)

# Extract backup directories and location from the config
BACKUP_DIRS = config["backup_dirs"]
BACKUP_LOCATION = config["backup_location"]
MAX_BACKUPS = config["max_backups"]
LOG_FILE = config["log_file"]

# Setup logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

# Get the current timestamp to use as the backup folder name
backup_folder_name = time.strftime("%Y%m%d-%H%M%S")

# Create a new backup directory
backup_folder_path = os.path.join(BACKUP_LOCATION, backup_folder_name)
os.makedirs(backup_folder_path)

# Create a tar archive of each backup directory
for backup_dir in BACKUP_DIRS:
    backup_file_name = os.path.basename(backup_dir) + ".tar.gz"
    backup_file_path = os.path.join(backup_folder_path, backup_file_name)
    
    try:
        with tarfile.open(backup_file_path, "w:gz") as tar:
            tar.add(backup_dir, arcname=os.path.basename(backup_dir))
        
        logging.info("Backup of %s completed successfully.", backup_dir)
        
    except Exception as e:
        logging.error("Backup of %s failed: %s", backup_dir, str(e))

# Remove oldest backups if there are more than the maximum allowed
backup_folders = sorted(os.listdir(BACKUP_LOCATION), reverse=True)
while len(backup_folders) > MAX_BACKUPS:
    oldest_backup_folder = backup_folders.pop()
    oldest_backup_path = os.path.join(BACKUP_LOCATION, oldest_backup_folder)
    logging.info("Removing oldest backup %s.", oldest_backup_path)
    shutil.rmtree(oldest_backup_path)
    backup_folders = sorted(os.listdir(BACKUP_LOCATION), reverse=True)

# Wait ten seconds before running the backup again
time.sleep(10)