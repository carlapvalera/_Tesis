import sqlite3
import pickle

class AnuarioDatabase:
    def __init__(self, db_name='anuarios.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        """Crea las tablas en la base de datos si no existen."""
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS anuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    year TEXT,
                    introduccion TEXT,
                    chapter_count INTEGER
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS capitulos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    anuario_id INTEGER,
                    chapter_number INTEGER,
                    chapter_name TEXT,
                    chapter_text TEXT,
                    FOREIGN KEY (anuario_id) REFERENCES anuarios (id) ON DELETE CASCADE
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS tablas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chapter_id INTEGER,
                    table_name TEXT,
                    table_data BLOB, -- Aquí puedes almacenar el DataFrame como un pickle o similar
                    FOREIGN KEY (chapter_id) REFERENCES capitulos (id) ON DELETE CASCADE
                )
            ''')

    def insert_anuario(self, year, introduccion):
        """Inserta un nuevo anuario en la base de datos."""
        with self.conn:
            cursor = self.conn.execute('''
                INSERT INTO anuarios (year, introduccion, chapter_count)
                VALUES (?, ?, ?)
            ''', (year, introduccion, 0))
            return cursor.lastrowid  # Retorna el ID del nuevo anuario

    def insert_capitulo(self, anuario_id, chapter_number, chapter_name, chapter_text):
        """Inserta un nuevo capítulo en la base de datos y actualiza el contador del anuario."""
        with self.conn:
            cursor = self.conn.execute('''
                INSERT INTO capitulos (anuario_id, chapter_number, chapter_name, chapter_text)
                VALUES (?, ?, ?, ?)
            ''', (anuario_id, chapter_number, chapter_name, chapter_text))
            # Incrementar el contador de capítulos en el anuario
            self.conn.execute('''
                UPDATE anuarios
                SET chapter_count = chapter_count + 1
                WHERE id = ?
            ''', (anuario_id,))
            return cursor.lastrowid  # Retorna el ID del nuevo capítulo

    def insert_tabla(self, chapter_id, table_name, table_data):
        """Inserta una nueva tabla en la base de datos."""
        with self.conn:
            serialized_data = pickle.dumps(table_data)  # Serializar el DataFrame
            cursor = self.conn.execute('''
                INSERT INTO tablas (chapter_id, table_name, table_data)
                VALUES (?, ?, ?)
            ''', (chapter_id, table_name, serialized_data))
            return cursor.lastrowid  # Retorna el ID de la nueva tabla

    def get_anuarios(self):
        """Devuelve todos los anuarios de la base de datos."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM anuarios')
        return cursor.fetchall()

    def get_capitulos(self, anuario_id):
        """Devuelve todos los capítulos de un anuario específico."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM capitulos WHERE anuario_id = ?', (anuario_id,))
        return cursor.fetchall()

    def get_tablas(self, chapter_id):
        """Devuelve todas las tablas de un capítulo específico."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM tablas WHERE chapter_id = ?', (chapter_id,))
        return cursor.fetchall()

    def update_anuario(self, anuario_id, year=None, introduccion=None):
        """Actualiza un anuario existente en la base de datos."""
        set_clause = []
        params = []

        if year is not None:
            set_clause.append("year = ?")
            params.append(year)
        if introduccion is not None:
            set_clause.append("introduccion = ?")
            params.append(introduccion)

        if set_clause:
            sql = f"UPDATE anuarios SET {', '.join(set_clause)} WHERE id = ?"
            params.append(anuario_id)

            with self.conn:
                self.conn.execute(sql, params)

    def update_capitulo(self, capitulo_id, chapter_number=None, chapter_name=None, chapter_text=None):
        """Actualiza un capítulo existente en la base de datos."""
        set_clause = []
        params = []

        if chapter_number is not None:
            set_clause.append("chapter_number = ?")
            params.append(chapter_number)
        if chapter_name is not None:
            set_clause.append("chapter_name = ?")
            params.append(chapter_name)
        if chapter_text is not None:
            set_clause.append("chapter_text = ?")
            params.append(chapter_text)

        if set_clause:
            sql = f"UPDATE capitulos SET {', '.join(set_clause)} WHERE id = ?"
            params.append(capitulo_id)

            with self.conn:
                self.conn.execute(sql, params)

    def update_tabla(self, tabla_id, table_name=None, table_data=None):
        """Actualiza una tabla existente en la base de datos."""
        set_clause = []
        params = []

        if table_name is not None:
            set_clause.append("table_name = ?")
            params.append(table_name)
        if table_data is not None:
            serialized_data = pickle.dumps(table_data)  # Serializar el DataFrame
            set_clause.append("table_data = ?")
            params.append(serialized_data)

        if set_clause:
            sql = f"UPDATE tablas SET {', '.join(set_clause)} WHERE id = ?"
            params.append(tabla_id)

            with self.conn:
                self.conn.execute(sql, params)

    def delete_anuario(self, anuario_id):
        """Elimina un anuario de la base de datos por su ID."""
        with self.conn:
            self.conn.execute('DELETE FROM anuarios WHERE id = ?', (anuario_id,))
    
    def delete_capitulo(self, capitulo_id):
        """Elimina un capítulo de la base de datos por su ID y actualiza el contador del anuario."""
        # Primero obtenemos el anuario_id del capítulo que se va a eliminar
        cursor = self.conn.cursor()
        cursor.execute('SELECT anuario_id FROM capitulos WHERE id = ?', (capitulo_id,))
        anuario_id = cursor.fetchone()

        if anuario_id:
            anuario_id = anuario_id[0]
            with self.conn:
                # Eliminar el capítulo
                self.conn.execute('DELETE FROM capitulos WHERE id = ?', (capitulo_id,))
                # Decrementar el contador de capítulos en el anuario
                self.conn.execute('''
                    UPDATE anuarios
                    SET chapter_count = chapter_count - 1
                    WHERE id = ?
                ''', (anuario_id,))
        else:
            print(f"Capítulo con ID {capitulo_id} no encontrado.")

    
    def delete_tabla(self, tabla_id):
        """Elimina una tabla de la base de datos por su ID."""
        with self.conn:
            self.conn.execute('DELETE FROM tablas WHERE id = ?', (tabla_id,))
    
    def close(self):
        """Cierra la conexión a la base de datos."""
        self.conn.close()

# Ejemplo de uso
if __name__ == "__main__":
    db = AnuarioDatabase()
    
    # Insertar un nuevo anuario
    anuario_id = db.insert_anuario(year="2023", introduccion="Introducción del anuario.")
    
    # Insertar capítulos
    capitulo1_id = db.insert_capitulo(anuario_id=anuario_id, chapter_number=1,
                                        chapter_name="Introducción", 
                                        chapter_text="Texto del capítulo 1.")
    
    capitulo2_id = db.insert_capitulo(anuario_id=anuario_id, chapter_number=2,
                                        chapter_name="Capítulo 1", 
                                        chapter_text="Texto del capítulo 2.")
    
    print("Contador de capítulos después de inserciones:")
    print(db.get_anuarios())  # Muestra los anuarios para verificar el contador

    # Eliminar un capítulo
    db.delete_capitulo(capitulo1_id)  # Eliminar primer capítulo
    
    print("Contador de capítulos después de eliminación:")
    print(db.get_anuarios())  # Muestra los anuarios para verificar el contador

    # Cerrar conexión
    db.close()