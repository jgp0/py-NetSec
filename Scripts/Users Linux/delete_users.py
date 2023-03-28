import subprocess

# Variable global para almacenar la lista de usuarios
usuarios = []

# Función para listar todos los usuarios en el sistema
def listar_usuarios():
    global usuarios
    comando = "cut -d: -f1 /etc/passwd"
    usuarios = subprocess.check_output(comando.split()).decode().split('\n')[:-1]

    print("Lista de usuarios:")
    for i, usuario in enumerate(usuarios):
        print(f"{i+1}. {usuario}")

# Función para eliminar un usuario
def eliminar_usuario(usuario):
    comando = f"sudo deluser --remove-home {usuario}"
    subprocess.run(comando.split())
    print(f"El usuario '{usuario}' ha sido eliminado.")

# Función principal del script
def main():
    print("Seleccione una opción:")
    print("1. Listar todos los usuarios")
    print("2. Introducir el nombre de usuario manualmente")

    opcion = input("Opción seleccionada: ")

    if opcion == "1":
        listar_usuarios()
        opcion_usuario = input("Ingrese el número del usuario que desea eliminar: ")
        if opcion_usuario.isdigit() and int(opcion_usuario) <= len(usuarios):
            usuario_a_eliminar = usuarios[int(opcion_usuario)-1]
            eliminar_usuario(usuario_a_eliminar)
        else:
            print("Opción inválida.")
    elif opcion == "2":
        usuario_a_eliminar = input("Ingrese el nombre de usuario que desea eliminar: ")
        eliminar_usuario(usuario_a_eliminar)
    else:
        print("Opción inválida.")

if __name__ == "__main__":
    main()
