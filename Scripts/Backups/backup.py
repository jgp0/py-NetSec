
import os
import time
import tarfile
import logging
import json
import shutil

# Cargamos la configuración del backup desde el archivo json
with open("/home/whippy/Descargas/backup_config", "r") as f:
    config = json.load(f)

# Extraemos los directorios del archivo de configuración
BACKUP_DIRS = config["backup_dirs"]
BACKUP_LOCATION = config["backup_location"]
MAX_BACKUPS = config["max_backups"]
LOG_FILE = config["log_file"]

# Registro de configuración
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

# Obtenemos la marca de tiempo actual para usar como nombre de la carpeta de copia de seguridad
backup_folder_name = time.strftime("%Y%m%d-%H%M%S")

# Creamos un nuevo directorio de copia de seguridad
backup_folder_path = os.path.join(BACKUP_LOCATION, backup_folder_name)
os.makedirs(backup_folder_path)

# Creamos un archivo tar de cada directorio de copia de seguridad
for backup_dir in BACKUP_DIRS:
    backup_file_name = os.path.basename(backup_dir) + ".tar.gz"
    backup_file_path = os.path.join(backup_folder_path, backup_file_name)
    
    try:
        with tarfile.open(backup_file_path, "w:gz") as tar:
            tar.add(backup_dir, arcname=os.path.basename(backup_dir))
        
        logging.info("Backup of %s completed successfully.", backup_dir)
        
    except Exception as e:
        logging.error("Backup of %s failed: %s", backup_dir, str(e))

# Eliminamos las copias de seguridad más antiguas si hay más del máximo permitido
backup_folders = sorted(os.listdir(BACKUP_LOCATION), reverse=True)
while len(backup_folders) > MAX_BACKUPS:
    oldest_backup_folder = backup_folders.pop()
    oldest_backup_path = os.path.join(BACKUP_LOCATION, oldest_backup_folder)
    logging.info("Removing oldest backup %s.", oldest_backup_path)
    shutil.rmtree(oldest_backup_path)
    backup_folders = sorted(os.listdir(BACKUP_LOCATION), reverse=True)

# Esperamos diez segundos antes de volver a ejecutar la copia de seguridad
time.sleep(10)