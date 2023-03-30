import subprocess
from getpass import getpass

# Pedir al usuario el nombre del nuevo usuario
username = input("Introduzca el nombre del nuevo usuario: ")

# Pedir al usuario que introduzca la contraseña dos veces y verificar que ambas coincidan
while True:
    password = getpass(prompt=f"Introduzca la contraseña para el usuario {username}: ")
    password_confirm = getpass(prompt=f"Introduzca la contraseña de nuevo para confirmar: ")
    if password == password_confirm:
        break
    else:
        print("Las contraseñas no coinciden. Inténtelo de nuevo.")

try:
    # Crear el nuevo usuario y su directorio /home
    useradd_command = f"sudo useradd -m {username}"
    subprocess.run(useradd_command, shell=True, check=True)

    # Establecer la contraseña para el nuevo usuario sin que sea visible
    passwd_command = f"echo '{password}\n{password}' | sudo passwd {username}"
    subprocess.run(passwd_command, shell=True)

    print(f"El usuario {username} ha sido creado exitosamente.")
except subprocess.CalledProcessError:
    print(f"No se pudo crear el usuario {username}.")
