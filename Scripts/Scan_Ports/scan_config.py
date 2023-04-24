import nmap
import requests
import xml.etree.ElementTree as ET
from prettytable import PrettyTable

print()

# Creamos una instancia de la clase PortScanner de nmap
nm = nmap.PortScanner()

# Pedimos al usuario que elija si desea escanear una dirección IP o un rango de direcciones IP
opcion = input("Seleccione una opción:\n1. Escanear una dirección IP concreta\n2. Escanear un rango de direcciones IP\n")

# Si el usuario elige escanear una dirección IP concreta, solicitamos la dirección IP
if opcion == '1':
    direccion_ip = input("Introduce la dirección IP que deseas escanear: ")
    nm.scan(direccion_ip, arguments='-p- --open -sS -sV --min-rate 5000 -vvv -n -Pn')
    
# Si el usuario elige escanear un rango de direcciones IP, solicitamos el rango
elif opcion == '2':
    rango_ip = input("Introduce el rango de direcciones IP que deseas escanear (ejemplo: 192.168.1.1-10): ")
    nm.scan(rango_ip, arguments='-p- --open -sS -sV --min-rate 5000 -vvv -n -Pn')

# Si el usuario elige una opción no válida, mostramos un mensaje de error y salimos del programa
else:
    print("Opción no válida.")
    exit()

# Obtenemos el resultado del escaneo
resultados = nm.all_hosts()

# Creamos la tabla para mostrar los resultados
tabla = PrettyTable()
tabla.field_names = ["Host", "Protocolo", "Puerto", "Estado", "Servicio", "Versión", "Vulnerabilidades"]

# Rellenamos la tabla con los resultados del escaneo
for host in resultados:
    for proto in nm[host].all_protocols():
        lport = nm[host][proto].keys()
        for port in lport:
            estado = nm[host][proto][port]['state']
            servicio = nm[host][proto][port]['name']
            version = nm[host][proto][port]['version']

            # Buscamos vulnerabilidades en el servicio que se está ejecutando en el puerto
            if servicio and version:
                # Construimos la URL de la API de búsqueda de vulnerabilidades de NVD
                url = f'https://services.nvd.nist.gov/rest/json/cves/1.0?keyword={servicio}%20{version}&resultsPerPage=1'
                response = requests.get(url)

                # Comprobamos que la respuesta sea válida
                if response.status_code == 200:
                    # Parseamos la respuesta en formato JSON
                    data = response.json()

                    # Obtenemos el número de resultados y los CVEs de cada resultado
                    num_resultados = data['totalResults']
                    cves = ""
                    if num_resultados > 0:
                        for resultado in data['result']['CVE_Items']:
                            cve = resultado['cve']['CVE_data_meta']['ID']
                            if cves == "":
                                cves = cve
                            else:
                                cves = f"{cves}, {cve}"
                
                # Añadimos los datos del host y puerto a la tabla
                tabla.add_row([host, proto, port, estado, servicio, version, cves])
                
# Mostramos la tabla
print(tabla)

