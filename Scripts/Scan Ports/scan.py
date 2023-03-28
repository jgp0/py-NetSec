import nmap
import mysql.connector
from datetime import datetime

# Pedir al usuario si su sistema operativo es Windows o Linux
print("Elige el sistema operativo en el que deseas realizar el escaneo: ")
print("1. Linux")
print("2. Windows")

sistema_operativo = input("Introduce el número correspondiente a tu sistema operativo: ")

if sistema_operativo == "1":
    sistema_operativo = "Linux"
elif sistema_operativo == "2":
    sistema_operativo = "Windows"
else:
    print("Opción no válida")
    exit()

# Pedir al usuario si desea escanear una dirección IP concreta o un rango de direcciones IP
print("¿Desea escanear una dirección IP concreta o un rango de direcciones IP?")
print("1. Dirección IP concreta")
print("2. Rango de direcciones IP")

tipo_escaneo = input("Introduce el número correspondiente a tu elección: ")

if tipo_escaneo == "1":
    tipo_escaneo = "concreta"
elif tipo_escaneo == "2":
    tipo_escaneo = "rango"
else:
    print("Opción no válida")
    exit()

# Pedir al usuario la dirección IP o el rango de direcciones IP que desea escanear
if tipo_escaneo == "concreta":
    direccion_ip = input("Introduce la dirección IP que deseas escanear: ")
elif tipo_escaneo == "rango":
    direccion_ip = input("Introduce el rango de direcciones IP que deseas escanear: ")

# Iniciar un escaneo de la red con nmap
if sistema_operativo == "Linux":
    nm = nmap.PortScanner()
    nm.scan(direccion_ip, arguments="-p- --open -sS --min-rate 5000 -vvv -n -Pn")
elif sistema_operativo == "Windows":
    try:
        nm = nmap.PortScanner()
        nm.scan(direccion_ip, arguments="-p- --open -sS --min-rate 5000 -vvv -n -Pn")
    except nmap.PortScannerError:
        print("Opción no válida")
        exit()

# Conectarse a una base de datos remota en MYSQL
direccion_ip_bd = "10.0.2.18"
usuario_bd = "nahuel"
contraseña_bd = "1q2w3e4r5T"
db_name = "escaneo_puertos"
table_name = "escaneo_red_" + datetime.now().strftime("%Y%m%d_%H%M%S")

conn = mysql.connector.connect(host=direccion_ip_bd, user=usuario_bd, password=contraseña_bd)
cursor = conn.cursor()

# Crear una nueva tabla en la base de datos para almacenar la información recopilada, pero solo si no existe ya una tabla con ese nombre
try:
    cursor.execute("CREATE DATABASE " + db_name + ";")
except mysql.connector.errors.DatabaseError:
    pass

cursor.execute("USE " + db_name + ";")

try:
    cursor.execute("CREATE TABLE " + table_name + " (id INT AUTO_INCREMENT PRIMARY KEY, host VARCHAR(15), puerto INT, estado_puerto VARCHAR(15), fecha DATE);")
except mysql.connector.errors.ProgrammingError:
    pass

# Exportar la información recopilada a la base de datos
fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
for host in nm.all_hosts():
    for puerto in nm[host]["tcp"].keys():
        cursor.execute(f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'escaneo_red_{fecha}'")
        result = cursor.fetchone()
        if result[0] == 0:
            cursor.execute(f"CREATE TABLE escaneo_red_{fecha} (id INT AUTO_INCREMENT PRIMARY KEY, host VARCHAR(15), puerto INT, estado_puerto VARCHAR(15))")
        cursor.execute(f"SELECT COUNT(*) FROM escaneo_red_{fecha} WHERE host = '{host}' AND puerto = {puerto}")
        result = cursor.fetchone()
        if result[0] == 0:
            cursor.execute(f"INSERT INTO escaneo_red_{fecha} (host, puerto, estado_puerto) VALUES ('{host}', {puerto}, '{nm[host]['tcp'][puerto]['state']}')")
        else:
            cursor.execute(f"UPDATE escaneo_red_{fecha} SET estado_puerto = '{nm[host]['tcp'][puerto]['state']}' WHERE host = '{host}' AND puerto = {puerto}")

# Guardar los cambios en la base de datos
conn.commit()

print("Escaneo finalizado. Los resultados han sido almacenados en la base de datos.")

# Mostrar los resultados obtenidos en el escaneo
cursor.execute(f"SELECT * FROM escaneo_red_{fecha}")
rows = cursor.fetchall()
for row in rows:
    print(row)

