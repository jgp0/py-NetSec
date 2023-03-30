import mysql.connector
from mysql.connector import Error
from prettytable import PrettyTable
import getpass
import time

data_types = {
    "INTEGER": ["TINYINT", "SMALLINT", "MEDIUMINT", "INT", "BIGINT"],
    "DECIMAL": ["DECIMAL (10,2)", "FLOAT", "DOUBLE"],
    "CHARACTER": ["CHAR", "VARCHAR (255)"],
    "DATE/TIME": ["DATE", "TIME", "DATETIME", "TIMESTAMP"]
}


def connect_to_database(host, user, password):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None


def show_databases(connection):
    cursor = connection.cursor()
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()
    print("\nBases de datos:")
    for db in databases:
        print(f"- {db[0]}")


def create_database(connection, database_name):
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE {database_name}")
    connection.commit()
    print(f"\nBase de datos '{database_name}' creada con éxito.")


def delete_database(connection, database_name):
    cursor = connection.cursor()
    cursor.execute(f"DROP DATABASE {database_name}")
    connection.commit()
    print(f"\nBase de datos '{database_name}' eliminada con éxito.")


def show_tables(connection, database_name):
    cursor = connection.cursor()
    cursor.execute(f"USE {database_name}")
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print(f"\nTablas en la base de datos '{database_name}':")
    for table in tables:
        print(f"- {table[0]}")


def create_table(connection, database_name, table_name, columns):
    cursor = connection.cursor()
    cursor.execute(f"USE {database_name}")

    column_definitions = []
    for name, data_type in columns:
        data_type_options = data_types[data_type]
        data_type_prompt = ", ".join(data_type_options)
        selected_data_type = input(f"Ingrese el tipo de datos para la columna '{name}' ({data_type_prompt}): ")
        while selected_data_type.upper() not in data_type_options:
            print("Tipo de datos no válido.")
            selected_data_type = input(f"Ingrese el tipo de datos para la columna '{name}' ({data_type_prompt}): ")
        column_definitions.append(f"{name} {selected_data_type}")

    column_definitions_str = ', '.join(column_definitions)
    cursor.execute(f"CREATE TABLE {table_name} ({column_definitions_str})")
    connection.commit()
    print(f"\nTabla '{table_name}' creada con éxito en la base de datos '{database_name}'.")


def delete_table(connection, database_name, table_name):
    cursor = connection.cursor()
    cursor.execute(f"USE {database_name}")
    cursor.execute(f"DROP TABLE {table_name}")
    connection.commit()
    print(f"\nTabla '{table_name}' eliminada con éxito de la base de datos '{database_name}'.")


def insert_into_table(connection, database_name, table_name, values):
    cursor = connection.cursor()
    cursor.execute(f"USE {database_name}")
    placeholders = ', '.join(['%s'] * len(values))
    cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", values)
    connection.commit()
    print(f"\nValores insertados correctamente en la tabla '{table_name}' de la base de datos '{database_name}'.")

def select_from_table(connection, database_name, table_name, columns=None):
    while True:
        try:
            cursor = connection.cursor()
            break
        except mysql.connector.errors.OperationalError:
            time.sleep(0)
            connection.reconnect()

    cursor.execute(f"USE {database_name}")

    if not columns:
        cursor.execute(f"SELECT * FROM {table_name}")
    else:
        column_names = ', '.join(['`{}`'.format(col) for col in columns])
        query = f"SELECT {column_names} FROM {table_name}"
        cursor.execute(query)
    rows = cursor.fetchall()

    table = PrettyTable()
    if columns:
        table.field_names = columns
    else:
        table.field_names = [i[0] for i in cursor.description]
    for row in rows:
        table.add_row(row)
    print(f"\nResultados de la consulta en la tabla '{table_name}' de la base de datos '{database_name}':")
    print(table)

def main():
    host = input("Introduce el host de la base de datos: ")
    user = input("Introduce el usuario de la base de datos: ")
    password = getpass.getpass("Introduce la contraseña de la base de datos: ")

    connection = connect_to_database(host, user, password)
    if not connection:
        return

    while True:
        print("\nMenú principal:")
        print("1. Crear una nueva base de datos.")
        print("2. Eliminar una base de datos existente.")
        print("3. Trabajar con una base de datos existente.")
        print("4. Salir.")
        option = input("\nSelecciona una opción: ")

        if option == "1":
            database_name = input("\nIntroduce el nombre de la nueva base de datos: ")
            create_database(connection, database_name)
        elif option == "2":
            database_name = input("\nIntroduce el nombre de la base de datos que deseas eliminar: ")
            delete_database(connection, database_name)
        elif option == "3":
            database_name = input("\nIntroduce el nombre de la base de datos con la que deseas trabajar: ")
            print(f"\nConectando a la base de datos '{database_name}'...")
            show_tables(connection, database_name)

            while True:
                print("\nMenú de la base de datos:")
                print("1. Crear una nueva tabla.")
                print("2. Eliminar una tabla existente.")
                print("3. Insertar valores en una tabla.")
                print("4. Seleccionar valores de una tabla.")
                print("5. Volver al menú principal.")
                option = input("\nSelecciona una opción: ")

                if option == "1":
                    table_name = input("\nIntroduce el nombre de la nueva tabla: ")
                    column_count = int(input("¿Cuántas columnas tendrá la tabla? "))
                    columns = []
                    for i in range(column_count):
                        name = input(f"\nIntroduce el nombre de la columna {i+1}: ")
                        data_type = input("Introduce el tipo de datos (INTEGER, DECIMAL, CHARACTER, DATE/TIME): ")
                        columns.append((name, data_type))
                    create_table(connection, database_name, table_name, columns)

                elif option == "2":
                    table_name = input("\nIntroduce el nombre de la tabla que deseas eliminar: ")
                    delete_table(connection, database_name, table_name)

                elif option == "3":
                    table_name = input("\nIntroduce el nombre de la tabla en la que deseas insertar valores: ")
                    column_count = int(input("¿Cuántas columnas deseas insertar? "))
                    values = []
                    for i in range(column_count):
                        value = input(f"\nIntroduce el valor para la columna {i+1}: ")
                        values.append(value)
                    insert_into_table(connection, database_name, table_name, values)

                elif option == "4":
                    table_name = input("\nIntroduce el nombre de la tabla que deseas seleccionar: ")
                    columns = input("\nIntroduce las columnas que deseas seleccionar (separadas por comas): ")
                    if columns:
                        columns = [c.strip() for c in columns.split(",")]
                    select_from_table(connection, database_name, table_name, columns)

                elif option == "5":
                    break

                else:
                    print("\nOpción no válida. Por favor, selecciona una opción válida.")

        elif option == "4":
            break

    else:
        print("\nSaliendo...")
        connection.close()

if __name__ == "__main__":
    main()

        

