import random
import string
import hashlib
import requests
import xerox

print()

def generate_password():
    # Pedir al usuario la longitud de la contraseña
    length = int(input("Longitud de la contraseña: "))

    # Pedir al usuario los tipos de caracteres que desea incluir en la contraseña
    print("Selecciona los tipos de caracteres que quieres incluir:")
    print("1. Solo letras")
    print("2. Letras y números")
    print("3. Letras, números y símbolos")
    choice = int(input("Selecciona una opción: "))

    if choice == 1:
        # Solo letras
        characters = string.ascii_letters
    elif choice == 2:
        # Letras y números
        characters = string.ascii_letters + string.digits
    elif choice == 3:
        # Letras, números y símbolos
        characters = string.ascii_letters + string.digits + string.punctuation
    else:
        print("Opción no válida.")
        return

    # Generar la contraseña aleatoria
    password = ''.join(random.choice(characters) for i in range(length))
    print("Contraseña generada: " + password)

    # Comprobar si la contraseña ha sido comprometida
    check_password(password)

    # Copiar la contraseña al portapapeles
    xerox.copy(password)
    print("Contraseña copiada al portapapeles.")

def check_password(password=None):
    # Pedir al usuario la contraseña que desea comprobar si no se especifica una
    if not password:
        password = input("Introduce la contraseña que deseas comprobar: ")

    # Hash de la contraseña con SHA1
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

    # Hacer una petición al API de haveibeenpwned.com para buscar si la contraseña ha sido comprometida
    url = 'https://api.pwnedpasswords.com/range/' + sha1password[:5]
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError('No se puede acceder al API de haveibeenpwned.com: ' + res.status_code)

    # Buscar si la contraseña aparece en la lista de contraseñas comprometidas
    hash_suffixes = (line.split(':') for line in res.text.splitlines())
    count = next((int(count) for suffix, count in hash_suffixes if sha1password[5:] == suffix), 0)

    if count:
        print(f"La contraseña '{password}' ha sido comprometida {count} veces.")
    else:
        print(f"La contraseña '{password}' no ha sido comprometida.")

# Pedir al usuario si desea generar una nueva contraseña automáticamente o comprobar una existente
print("Configuración de la contraseña:")
print("1. Generar una nueva contraseña automáticamente")
print("2. Comprobar una contraseña existente")
option = int(input("Selecciona una opción: "))

if option == 1:
    generate_password()
elif option == 2:
    check_password()
else:
    print("Opción no válida.")
