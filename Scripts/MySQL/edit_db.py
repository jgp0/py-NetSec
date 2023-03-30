import mysql.connector
from mysql.connector import Error
from prettytable import PrettyTable
import getpass
import time

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
    column_definitions = ', '.join([f"{name} {data_type}" for name, data_type in columns])
    cursor.execute(f"CREATE TABLE {table_name} ({column_definitions})")
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
        placeholders = ', '.join(['%s'] * len(columns))
        query = f"SELECT {column_names} FROM {table_name} WHERE 1=1"
        cursor.execute(query, ())
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

    show_databases(connection)

    option = input("\n¿Quieres crear o eliminar una base de datos, o trabajar con una existente? (C/E/T): ")
    if option.lower() == "c":
        database_name = input("\nIntroduce el nombre de la nueva base de datos: ")
        create_database(connection, database_name)
    elif option.lower() == "e":
        database_name = input("\nIntroduce el nombre de la base de datos a eliminar: ")
        delete_database(connection, database_name)
    elif option.lower() == "t":
        database_name = input("\nIntroduce el nombre de la base de datos con la que quieres trabajar: ")
        show_tables(connection, database_name)

        option = input("\n¿Quieres crear o eliminar una tabla, o insertar o consultar datos en una existente? (C/E/I/CO): ")
        if option.lower() == "c":
            table_name = input("\nIntroduce el nombre de la nueva tabla: ")
            num_columns = int(input("\n¿Cuántas columnas tiene la tabla? "))
            columns = []
            for i in range(num_columns):
                name = input(f"\nIntroduce el nombre de la columna {i+1}: ")
                data_type = input(f"\nIntroduce el tipo de datos para la columna {name}: ")
                columns.append((name, data_type))
                create_table(connection, database_name, table_name, columns)
        elif option.lower() == "e":
            table_name = input("\nIntroduce el nombre de la tabla a eliminar: ")
            delete_table(connection, database_name, table_name)
        elif option.lower() == "i":
            table_name = input("\nIntroduce el nombre de la tabla en la que quieres insertar los datos: ")
            num_columns = int(input("\n¿Cuántas columnas tiene la tabla? "))
            values = []
            for i in range(num_columns):
                value = input(f"\nIntroduce el valor para la columna {i+1}: ")
                values.append(value)
                insert_into_table(connection, database_name, table_name, values)
        elif option.lower() == "co":
            table_name = input("\nIntroduce el nombre de la tabla que quieres consultar: ")
            column_input = input("\n¿Quieres seleccionar todas las columnas o solo algunas? (T/S): ")
            if column_input.lower() == "t":
                select_from_table(connection, database_name, table_name)
            elif column_input.lower() == "s":
                num_columns = int(input("\n¿Cuántas columnas quieres seleccionar? "))
                columns = []
                for i in range(num_columns):
                    column = input(f"\nIntroduce el nombre de la columna {i+1}: ")
                    columns.append(column)
                    select_from_table(connection, database_name, table_name, columns)
                    connection.close()

if __name__ == "__main__":
    main()
