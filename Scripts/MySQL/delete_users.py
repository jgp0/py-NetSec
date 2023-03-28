import mysql.connector
import getpass

# Solicitar al usuario el nombre de usuario y la contraseña
username = input("Ingrese el nombre de usuario con permisos en la base de datos: ")
password = getpass.getpass("Ingrese la contraseña: ")

# Conexión a la base de datos de MySQL
db = mysql.connector.connect(
  host="10.0.2.18",
  user=username,
  password=password
)

# Crear un cursor
cursor = db.cursor()

# Obtener la lista de bases de datos existentes
cursor.execute("SHOW DATABASES")
databases = cursor.fetchall()

# Mostrar la lista de bases de datos y solicitar al usuario que seleccione una
print("Bases de datos existentes:")
for i, database in enumerate(databases):
    print(f"{i+1}. {database[0]}")
selection = int(input("Seleccione el número de la base de datos en la que desea eliminar un usuario: "))

# Conexión a la base de datos seleccionada
selected_db = databases[selection-1][0]
db = mysql.connector.connect(
  host="10.0.2.18",
  user=username,
  password=password,
  database=selected_db
)

# Crear un cursor para la base de datos seleccionada
cursor = db.cursor()

# Obtener la lista de usuarios existentes en la base de datos seleccionada
cursor.execute("SELECT user, host FROM mysql.user")
users = cursor.fetchall()

# Mostrar la lista de usuarios y solicitar al usuario que seleccione uno para eliminar
print("Usuarios existentes:")
for i, user in enumerate(users):
    print(f"{i+1}. {user[0]}@{user[1]}")
selection = int(input("Seleccione el número del usuario que desea eliminar: "))

# Obtener el usuario seleccionado
user_to_delete = users[selection-1][0]

# Solicitar al usuario que ingrese el host del usuario que desea eliminar
host_to_delete = input("Ingrese el host del usuario que desea eliminar: ")

# Eliminar el usuario seleccionado
cursor.execute(f"DROP USER '{user_to_delete}'@'{host_to_delete}'")
db.commit()

# Cerrar la conexión a la base de datos
db.close()

print(f"El usuario {user_to_delete}@{host_to_delete} ha sido eliminado correctamente.")
