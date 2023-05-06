import os
import time
import tarfile
import logging
import json
import shutil

print()

# Preguntar al usuario qué ruta desea copiar y en qué ruta desea alojar la copia de seguridad
backup_dir = input("Ingrese la ruta que desea copiar: ")
backup_location = input("Ingrese la ruta donde desea alojar la copia de seguridad: ")

# Registro de configuración
LOG_FILE = "/var/log/backup.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

# Obtenemos la marca de tiempo actual para usar como nombre de la carpeta de copia de seguridad
backup_folder_name = time.strftime("%Y%m%d-%H%M%S")

# Creamos un nuevo directorio de copia de seguridad
backup_folder_path = os.path.join(backup_location, backup_folder_name)
os.makedirs(backup_folder_path)

# Creamos un archivo tar de cada directorio de copia de seguridad
backup_file_name = os.path.basename(backup_dir) + ".tar.gz"
backup_file_path = os.path.join(backup_folder_path, backup_file_name)

try:
    with tarfile.open(backup_file_path, "w:gz") as tar:
        tar.add(backup_dir, arcname=os.path.basename(backup_dir))

    logging.info("Backup of %s completed successfully.", backup_dir)

except Exception as e:
    logging.error("Backup of %s failed: %s", backup_dir, str(e))
