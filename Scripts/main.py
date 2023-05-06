import os
import subprocess

# Rutas de los scripts
script_paths = {
    "MySQL": "Tools/mysql_config.py",
    "Backup": "Tools/backup.py",
    "Scan Ports": "Tools/scan_config.py",
    "Passwd": "Tools/create_passwd.py",
    "Create Users (Linux)": "Tools/create_users.py",
    "Delete Users (Linux)": "Tools/delete_users.py",
    "Create Users (Windows)": "Tools/create_users.ps1",
    "Delete Users (Windows)": "Tools/delete_users.ps1",
}

# Función para ejecutar un script
def ejecutar_script(ruta_script):
    if ruta_script.endswith(".py"):
        subprocess.run(["python3", ruta_script])
    elif ruta_script.endswith(".ps1"):
        subprocess.run(["powershell.exe", "-File", ruta_script])
    else:
        print("Tipo de archivo no compatible:", ruta_script)

# Menú interactivo para seleccionar un script
while True:
    print("Seleccione el script que desea ejecutar:")
    for i, script_name in enumerate(script_paths.keys()):
        print(f"{i+1}. {script_name}")

    opcion = input("Ingrese el número del script que desea ejecutar (o 'q' para salir): ")
    if opcion.lower() == "q":
        break

    try:
        opcion = int(opcion)
        script_name = list(script_paths.keys())[opcion-1]
        ruta_script = script_paths[script_name]
        ejecutar_script(ruta_script)

    except (ValueError, IndexError):
        print("Opción inválida. Por favor ingrese un número del menú.")
