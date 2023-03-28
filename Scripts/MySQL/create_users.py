import getpass
import mysql.connector

# Se solicitan las credenciales de acceso a la base de datos
db_user = input("Ingresa el nombre de usuario con privilegios sobre la base de datos: ")
db_password = getpass.getpass("Ingresa la contraseña de la base de datos: ")

# Se establece la conexión a la base de datos
db_conn = mysql.connector.connect(user=db_user, password=db_password, host='10.0.2.18')

# Se obtienen las bases de datos disponibles
cursor = db_conn.cursor()
cursor.execute("SHOW DATABASES;")
databases = cursor.fetchall()

# Se muestra una lista de las bases de datos disponibles
print("Bases de datos disponibles:")
for i, db in enumerate(databases):
    print("{}. {}".format(i+1, db[0]))

# Se pide al usuario que seleccione una base de datos
selected_db = None
while not selected_db:
    try:
        db_index = int(input("Selecciona una base de datos: "))
        if db_index < 1 or db_index > len(databases):
            raise ValueError
        selected_db = databases[db_index-1][0]
    except ValueError:
        print("Selecciona un número válido.")

# Se solicitan las credenciales para crear el nuevo usuario
new_user = input("Ingresa el nombre del nuevo usuario: ")
new_password = getpass.getpass("Ingresa la contraseña del nuevo usuario: ")
new_password_confirm = getpass.getpass("Confirma la contraseña del nuevo usuario: ")

# Se verifica que las contraseñas sean iguales
if new_password != new_password_confirm:
    print("Las contraseñas no coinciden. Inténtalo de nuevo.")
    exit()

# Se pregunta si se desea crear un usuario local, remoto o ambos
user_type = input("¿Quieres crear un usuario local, remoto o ambos? (L/R/A): ")

if user_type.upper() == 'L':
    user_host = 'localhost'
elif user_type.upper() == 'R':
    user_host = input("Ingresa la dirección IP del usuario remoto: ")
elif user_type.upper() == 'A':
    user_host = '%'
else:
    print("Opción inválida.")
    exit()

# Se construye la consulta SQL para crear el nuevo usuario
query = "CREATE USER '{}'@'{}' IDENTIFIED BY '{}';".format(new_user, user_host, new_password)

# Se ejecuta la consulta SQL
cursor = db_conn.cursor()
cursor.execute("USE {};".format(selected_db))
cursor.execute(query)

# Se confirma la creación del nuevo usuario
print("Se ha creado el usuario '{}' en la base de datos '{}'.".format(new_user, selected_db))

# Se cierra la conexión a la base de datos
db_conn.close()
