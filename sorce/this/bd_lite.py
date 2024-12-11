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
