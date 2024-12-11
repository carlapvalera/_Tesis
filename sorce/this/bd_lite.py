import sqlite3
import pandas as pd

class Database:
    def __init__(self, db_file):
        """Inicializa la conexión a la base de datos SQLite."""
        self.conn = self.create_connection(db_file)
        self.cursor = self.conn.cursor()

    def create_connection(self, db_file):
        """Crea una conexión a la base de datos SQLite."""
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print("Conexión a la base de datos establecida.")
        except sqlite3.Error as e:
            print(e)
        return conn

    def create_table(self, table_name, columns):
        """Crea una tabla a partir del nombre y las columnas proporcionadas."""
        columns_with_types = ', '.join([f"{col} TEXT" for col in columns])
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types});"
        try:
            self.cursor.execute(create_table_sql)
            print(f"Tabla '{table_name}' creada exitosamente.")
        except sqlite3.Error as e:
            print(e)

    def insert_data(self, table_name, data):
        """Inserta datos en la tabla especificada."""
        placeholders = ', '.join(['?'] * len(data[0]))
        sql = f"INSERT OR IGNORE INTO {table_name} VALUES ({placeholders})"
        try:
            self.cursor.executemany(sql, data)
            self.conn.commit()
            print(f"Datos insertados en '{table_name}' exitosamente.")
        except sqlite3.Error as e:
            print(e)

    def read_data(self, table_name):
        """Lee todos los datos de la tabla especificada."""
        sql = f"SELECT * FROM {table_name}"
        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(e)
            return []

    def close_connection(self):
        """Cierra la conexión a la base de datos."""
        if self.conn:
            self.conn.close()
            print("Conexión a la base de datos cerrada.")

    def create_tables_from_dataframe(self, df_dict):
        """Crea tablas en la base de datos a partir de diccionarios de DataFrames."""
        for table_name, df in df_dict.items():
            # Crear tabla
            self.create_table(table_name, df.columns.tolist())

            # Insertar datos
            data = [tuple(x) for x in df.to_numpy()]
            self.insert_data(table_name, data)

# Ejemplo de uso
def main():
    database = "trabajadores.db"

    # Crear instancia de la base de datos
    db = Database(database)

    # Simulación de DataFrames
    data_edades = {
        "nombre": ["Alice", "Bob", "Charlie", "David", "Eve"],
        "edad": [28, 34, 22, 45, 30]
    }

    data_posiciones = {
        "nombre": ["Alice", "Bob", "Charlie", "David", "Eve"],
        "posicion": ["Técnico", "Gestor", "Técnico", "Analista", "Técnico"]
    }

    # Crear DataFrames
    df_edades = pd.DataFrame(data_edades)
    df_posiciones = pd.DataFrame(data_posiciones)

    # Almacenar los DataFrames en un diccionario para fácil acceso
    df_dict = {
        'trabajadores_edad': df_edades,
        'trabajadores_posicion': df_posiciones
    }

    # Crear tablas y cargar datos desde DataFrames
    db.create_tables_from_dataframe(df_dict)

    # Leer y mostrar datos
    print("\nDatos en trabajadores_edad:")
    for row in db.read_data('trabajadores_edad'):
        print(row)

    print("\nDatos en trabajadores_posicion:")
    for row in db.read_data('trabajadores_posicion'):
        print(row)

    # Cerrar conexión
    db.close_connection()

if __name__ == '__main__':
    main()
