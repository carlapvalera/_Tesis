import json
import uuid
from pymongo import MongoClient, errors

# Crear una conexión al servidor de MongoDB
client = MongoClient('localhost', 27017)

# Probar la conexión
try:
    client.admin.command('ping')  # Esto envía un comando ping para verificar la conexión
    print("Conexión exitosa a MongoDB")
except Exception as e:
    print("Error al conectar a MongoDB:", e)

# Seleccionar la base de datos 'nest'
db = client['nest']

# Seleccionar la colección 'LLM'
collection = db['LLM']

def insert_chat(question, answer, file_detail):
    """Inserta un nuevo chat en la colección 'LLM'."""
    session_id = str(uuid.uuid1())
    try:
        collection.insert_one({
            'session_id': session_id,
            'question': question,
            'answer': answer,
            'file_detail': file_detail,
            'vote': 0
        })
        return session_id
    except errors.PyMongoError as e:
        print("Error al insertar chat:", e)
        return None

def update_vote_by_session_id(vote, session_id):
    """Actualiza el voto para un chat dado su session_id en la colección 'LLM'."""
    try:
        res = collection.update_one(
            {'session_id': session_id},
            {'$set': {'vote': vote}}
        )
        return res.modified_count  # Retorna el número de documentos modificados
    except errors.PyMongoError as e:
        print("Error al actualizar voto:", e)
        return None

def get_random_wtq():
    """Obtiene un documento aleatorio de la colección 'wtq'."""
    try:
        res = list(collection.aggregate([{ '$sample': { 'size': 1 } }]))
        return res[0] if res else None  # Retorna None si no hay resultados
    except errors.PyMongoError as e:
        print("Error al obtener documento aleatorio de wtq:", e)
        return None

def get_random_table_op():
    """Obtiene un documento aleatorio de la colección 'table_op'."""
    try:
        res = list(db.table_op.aggregate([{ '$sample': { 'size': 1 } }]))
        return res[0] if res else None  # Retorna None si no hay resultados
    except errors.PyMongoError as e:
        print("Error al obtener documento aleatorio de table_op:", e)
        return None

def get_random_table_merge():
    """Obtiene un documento aleatorio de la colección 'table_merge'."""
    try:
        res = list(db.table_merge.aggregate([{ '$sample': { 'size': 1 } }]))
        return res[0] if res else None  # Retorna None si no hay resultados
    except errors.PyMongoError as e:
        print("Error al obtener documento aleatorio de table_merge:", e)
        return None
    






def test_mongodb_functions():
    # Crear una conexión al servidor de MongoDB
    client = MongoClient('localhost', 27017)

    # Probar la conexión
    try:
        client.admin.command('ping')  # Esto envía un comando ping para verificar la conexión
        print("Conexión exitosa a MongoDB")
    except Exception as e:
        print("Error al conectar a MongoDB:", e)
        return

    # Seleccionar la base de datos 'nest'
    db = client['nest']
    
    # Seleccionar la colección 'LLM'
    collection = db['LLM']

    # Probar la inserción de un nuevo chat
    print("Probando inserción de chat...")
    session_id = insert_chat("¿Cuál es la capital de Francia?", "París", "Archivo de ejemplo")
    if session_id:
        print(f"Chat insertado con session_id: {session_id}")
    else:
        print("Fallo en la inserción del chat.")

    # Probar la actualización del voto
    print("\nProbando actualización de voto...")
    if session_id:
        updated_count = update_vote_by_session_id( 5, session_id)
        if updated_count is not None:
            print(f"Voto actualizado. Documentos modificados: {updated_count}")
        else:
            print("Fallo en la actualización del voto.")

    # Probar la obtención de un documento aleatorio de 'wtq'
    print("\nProbando obtención aleatoria de documento de 'wtq'...")
    random_wtq = get_random_wtq()
    if random_wtq:
        print("Documento aleatorio obtenido de 'wtq':", random_wtq)
    else:
        print("No se pudo obtener documento aleatorio de 'wtq'.")

    # Probar la obtención de un documento aleatorio de 'table_op'
    print("\nProbando obtención aleatoria de documento de 'table_op'...")
    random_table_op = get_random_table_op()
    if random_table_op:
        print("Documento aleatorio obtenido de 'table_op':", random_table_op)
    else:
        print("No se pudo obtener documento aleatorio de 'table_op'.")

    # Probar la obtención de un documento aleatorio de 'table_merge'



# Ejecutar las pruebas
if __name__ == "__main__":
    test_mongodb_functions()