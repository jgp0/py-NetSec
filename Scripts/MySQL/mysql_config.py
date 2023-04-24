import mysql.connector
import getpass

def connect_to_database():
    """Conecta a la base de datos MySQL y devuelve la conexión"""
    host = input("Introduce el host con privilegios sobre la base de datos: ")
    user = input("Introduce el usuario con privilegios sobre la base de datos: ")
    password = getpass.getpass("Introduce la contraseña del usuario con privilegios: ")
    confirm_password = getpass.getpass("Confirma la contraseña: ")

    while password != confirm_password:
        print("Las contraseñas no coinciden. Inténtalo de nuevo.")
        password = getpass.getpass("Introduce la contraseña: ")
        confirm_password = getpass.getpass("Confirma la contraseña: ")
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )

def create_user():
    """Crea un nuevo usuario en la base de datos"""
    host = input("Introduce el host con privilegios sobre la base de datos: ")
    user = input("Introduce el usuario con privilegios sobre la base de datos: ")
    password = getpass.getpass("Introduce la contraseña del usuario con privilegios: ")
    confirm_password = getpass.getpass("Confirma la contraseña: ")

    while password != confirm_password:
        print("Las contraseñas no coinciden. Inténtalo de nuevo.")
        password = getpass.getpass("Introduce la contraseña: ")
        confirm_password = getpass.getpass("Confirma la contraseña: ")
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )
    username = input("Introduce el nombre de usuario que deseas crear: ")
    host_db = input ("Introduce el nombre de host para el usuario que deseas crear: ")
    password = getpass.getpass("Introduce la contraseña: ")
    confirm_password = getpass.getpass("Introduce de nuevo la contraseña: ")

    while password != confirm_password:
        print("Las contraseñas no coinciden. Inténtalo de nuevo.")
        password = getpass.getpass("Introduce la contraseña del usuario con privilegios: ")
        confirm_password = getpass.getpass("Introduce de nuevo la contraseña: ")
    cursor = connection.cursor()
    cursor.execute(f"CREATE USER '{username}'@'{host_db}' IDENTIFIED BY '{password}'")
    cursor.close()
    connection.close()
    print("Usuario creado con éxito")

def delete_user():
    """Elimina un usuario de la base de datos"""
    host = input("Introduce el host con privilegios sobre la base de datos: ")
    user = input("Introduce el usuario con privilegios sobre la base de datos: ")
    password = getpass.getpass(prompt="Introduce la contraseña del usuario con privilegios: ")
    confirm_password = getpass.getpass(prompt="Introduce de nuevo la contraseña: ")

    if password != confirm_password:
        print("Las contraseñas no coinciden.")
        return
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )
    username = input("Introduce el nombre de usuario que deseas eliminar: ")
    host_db = input ("Introduce el nombre de host para el usuario que deseas eliminar: ")
    cursor = connection.cursor()
    cursor.execute(f"DROP USER '{username}'@'{host_db}'")
    cursor.close()
    connection.close()
    print("Usuario eliminado con éxito")

def grant_permissions():
    """Concede permisos a un usuario en la base de datos"""
    host = input("Introduce el host con privilegios sobre la base de datos: ")
    user = input("Introduce el nombre de usuario con privilegios sobre la base de datos: ")
    password = getpass.getpass(prompt="Introduce la contraseña del usuario con privilegios: ")
    confirm_password = getpass.getpass(prompt="Introduce de nuevo la contraseña: ")
    if password != confirm_password:
        print("Las contraseñas no coinciden.")
        return
    database = input("Introduce el nombre de la base de datos: ")
    username = input("Introduce el nombre de usuario al que deseas asignar permisos: ")
    host_db = input ("Introduce el nombre de host para el usuario al que deseas asignar permisos: ")
    permissions = [
    "ALL PRIVILEGES", "SELECT", "INSERT", "UPDATE", "DELETE", 
    "CREATE", "DROP", "INDEX", "ALTER", "GRANT OPTION"
    ]

    print("Elige los permisos que quieres conceder:")
    for i, perm in enumerate(permissions):
        print(f"{i + 1}. {perm}")
    option = int(input("Opción: "))
    permission = permissions[option - 1]

    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )

    cursor = connection.cursor()
    cursor.execute(f"GRANT {permission} ON {database}.* TO '{username}'@'{host_db}'")
    cursor.close()
    connection.close()
    print("Permisos concedidos con éxito")

def revoke_permissions():
    """Revoca los permisos de un usuario en la base de datos"""
    host = input("Introduce el host de la base de datos: ")
    username = input("Introduce el nombre de usuario: ")
    password = getpass.getpass(prompt="Introduce la contraseña del usuario con privilegios: ")
    confirm_password = getpass.getpass(prompt="Introduce de nuevo la contraseña: ")
    if password != confirm_password:
        print("Las contraseñas no coinciden.")
        return
    database = input("Introduce el nombre de la base de datos: ")
    username = input("Introduce el nombre de usuario al que deseas revocar permisos: ")
    host_db = input ("Introduce el nombre de host para el usuario al que deseas revocar permisos: ")
    permissions = [
        "ALL PRIVILEGES", "SELECT", "INSERT", "UPDATE", "DELETE", 
        "CREATE", "DROP", "INDEX", "ALTER", "GRANT OPTION"
    ]

    print("Elige los permisos que quieres revocar:")
    for i, perm in enumerate(permissions):
        print(f"{i + 1}. {perm}")
    option = int(input("Opción: "))
    permission = permissions[option - 1]

    connection = mysql.connector.connect(
        host=host,
        user=username,
        password=password
    )

    cursor = connection.cursor()
    cursor.execute(f"REVOKE {permission} ON {database}.* FROM '{username}'@'{host_db}'")
    cursor.close()
    connection.close()
    print("Permisos revocados con éxito")

def exit_program():
    """Sale del programa"""
    print("Hasta luego")
    exit()

print()

def main():
    """Función principal"""
    while True:
        print("\n¿Qué quieres hacer?")
        print("1. Crear un usuario")
        print("2. Eliminar un usuario")
        print("3. Conceder permisos")
        print("4. Revocar permisos")
        print("5. Salir")
        option = int(input("Opción: "))
        if option == 1:
            create_user()
        elif option == 2:
            delete_user()
        elif option == 3:
            grant_permissions()
        elif option == 4:
            revoke_permissions()
        elif option == 5:
            exit_program()
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()


