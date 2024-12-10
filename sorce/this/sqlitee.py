import sqlite3

# Paso 1: Crear una conexión a la base de datos
def create_connection(db_file):
    """Crea una conexión a la base de datos SQLite."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Conexión a la base de datos establecida.")
    except sqlite3.Error as e:
        print(e)
    return conn

# Paso 2: Crear tablas
def create_table(conn):
    """Crea las tablas necesarias en la base de datos."""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS trabajadores_edad (
        nombre TEXT PRIMARY KEY,
        edad INTEGER NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS trabajadores_posicion (
        nombre TEXT PRIMARY KEY,
        posicion TEXT NOT NULL
    );
    """
    try:
        cursor = conn.cursor()
        cursor.executescript(create_table_sql)
        print("Tablas creadas exitosamente.")
    except sqlite3.Error as e:
        print(e)

# Paso 3: Insertar datos en las tablas
def insert_data(conn):
    """Inserta datos en las tablas."""
    workers_edad = [
        ("Alice", 28),
        ("Bob", 34),
        ("Charlie", 22),
        ("David", 45),
        ("Eve", 30)
    ]
    
    workers_posicion = [
        ("Alice", "Técnico"),
        ("Bob", "Gestor"),
        ("Charlie", "Técnico"),
        ("David", "Analista"),
        ("Eve", "Técnico")
    ]
    
    try:
        cursor = conn.cursor()
        
        # Insertar datos en trabajadores_edad
        cursor.executemany("INSERT OR IGNORE INTO trabajadores_edad (nombre, edad) VALUES (?, ?)", workers_edad)
        
        # Insertar datos en trabajadores_posicion
        cursor.executemany("INSERT OR IGNORE INTO trabajadores_posicion (nombre, posicion) VALUES (?, ?)", workers_posicion)
        
        conn.commit()
        print("Datos insertados exitosamente.")
        
    except sqlite3.Error as e:
        print(e)

# Paso 4: Verificar inserciones
def verify_data(conn):
    """Verifica que los datos se hayan insertado correctamente."""
    try:
        cursor = conn.cursor()
        
        # Contar registros en trabajadores_edad
        cursor.execute("SELECT COUNT(*) FROM trabajadores_edad")
        count_edad = cursor.fetchone()[0]
        
        # Contar registros en trabajadores_posicion
        cursor.execute("SELECT COUNT(*) FROM trabajadores_posicion")
        count_posicion = cursor.fetchone()[0]
        
        print(f"Número de registros en 'trabajadores_edad': {count_edad}")
        print(f"Número de registros en 'trabajadores_posicion': {count_posicion}")
        
        # Consultar algunos registros para verificar contenido
        cursor.execute("SELECT * FROM trabajadores_edad LIMIT 5")
        rows = cursor.fetchall()
        print("\nDatos en 'trabajadores_edad':")
        for row in rows:
            print(row)

        cursor.execute("SELECT * FROM trabajadores_posicion LIMIT 5")
        rows = cursor.fetchall()
        print("\nDatos en 'trabajadores_posicion':")
        for row in rows:
            print(row)

    except sqlite3.Error as e:
        print(e)

# Paso 5: Ejecutar consultas SQL
def query_data(conn):
    """Ejecuta una consulta para obtener trabajadores técnicos mayores de 30 años."""
    sql_query = """
    SELECT T1.nombre 
    FROM trabajadores_edad AS T1 
    INNER JOIN trabajadores_posicion AS T2 
    ON T1.nombre = T2.nombre 
    WHERE T2.posicion = 'Técnico' AND T1.edad > 30;
    """
    
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        
        rows = cursor.fetchall()
        
        if rows:
            print("Trabajadores técnicos mayores de 30 años:")
            for row in rows:
                print(row[0])  # Imprimir solo el nombre
        else:
            print("No se encontraron trabajadores técnicos mayores de 30 años.")
            
    except sqlite3.Error as e:
        print(e)

# Función principal para ejecutar el flujo completo
def main():
    database = "trabajadores.db"
    
    # Crear conexión a la base de datos
    conn = create_connection(database)
    
    if conn is not None:
        create_table(conn)  # Crear tablas
        insert_data(conn)   # Insertar datos
        verify_data(conn)   # Verificar inserciones
        query_data(conn)    # Ejecutar consulta
        
        # Cerrar la conexión
        conn.close()
    else:
        print("Error! No se puede establecer la conexión.")

if __name__ == '__main__':
    main()