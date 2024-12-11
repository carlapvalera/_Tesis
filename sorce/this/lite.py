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
def create_tables(conn):
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

# Paso 4: Ejecutar consultas SQL
def query_data(conn, sql_query):
    """Ejecuta una consulta SQL dada."""
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        
        rows = cursor.fetchall()
        
        if rows:
            return rows
        else:
            return []
            
    except sqlite3.Error as e:
        print(e)
        return []

# Función principal para ejecutar el flujo completo
def main():
    database = "trabajadores.db"
    
    # Crear conexión a la base de datos
    conn = create_connection(database)
    
    if conn is not None:
        create_tables(conn)  # Crear tablas
        insert_data(conn)   # Insertar datos
        
        # Simulación de respuesta del LLM (esto debería ser reemplazado por la llamada real al modelo)
        llm_response = 'SELECT COUNT(*) FROM trabajadores_edad WHERE edad > 30;'
        
        print("Respuesta del LLM:", llm_response)

        # Ejecutar la consulta SQL generada por el LLM
        result = query_data(conn, llm_response)

        # Mostrar el resultado
        if result:
            print("\nResultado de la consulta:")
            for row in result:
                print(row)
        
        # Cerrar la conexión
        conn.close()
    else:
        print("Error! No se puede establecer la conexión.")

if __name__ == '__main__':
    main()
