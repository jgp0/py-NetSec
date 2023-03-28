import nmap
import requests
import xml.etree.ElementTree as ET

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

# Imprimimos los resultados del escaneo
for host in resultados:
    print(f"Host: {host}")
    for proto in nm[host].all_protocols():
        print(f"\tProtocolo: {proto}")
        lport = nm[host][proto].keys()
        for port in lport:
            estado = nm[host][proto][port]['state']
            print(f"\t\tPuerto: {port}\tEstado: {estado}")
            # Buscamos vulnerabilidades en el servicio que se está ejecutando en el puerto
            servicio = nm[host][proto][port]['name']
            version = nm[host][proto][port]['version']
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
                    if num_resultados > 0:
                        print(f"\t\tVulnerabilidades encontradas ({num_resultados}):")
                        for resultado in data['result']['CVE_Items']:
                            descripcion = resultado['cve']['description']['description_data'][0]['value']
                            cves = resultado['cve']['CVE_data_meta']['ID']
                            print(f"\t\t\t{descripcion} (CVE: {cves})")
                    else:
                        print("\t\tNo se encontraron vulnerabilidades para el servicio.")
                else:
                    print("\t\tError al conectar con la API de NVD.")
            else:
                print("\t\tNo se encontró información de versión para el servicio.")
