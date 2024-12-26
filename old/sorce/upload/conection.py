from pymongo import MongoClient
from bson import ObjectId

# Conexión a la base de datos MongoDB local
client = MongoClient('localhost', 27017)

# Probar la conexión
try:
    client.admin.command('ping')  # Esto envía un comando ping para verificar la conexión
    print("Conexión exitosa a MongoDB")
except Exception as e:
    print("Error al conectar a MongoDB:", e)

# Seleccionar la base de datos 'anuarios_estadisticos'
db = client['anuarios_estadisticos']

# Seleccionar las colecciones
files_collection = db['files']  # Colección para archivos subidos
precomputed_collection = db['precomputed']  # Colección para respuestas precomputadas


# CRUD para archivos

def insert_file_data(name, file_type, description, content, embedding):
    """Inserta un nuevo archivo en la colección."""
    file_data = {
        "name": name,
        "file_type": file_type,
        "description": description,
        "content": content,
        "embedding": embedding,
        "precomputed_answers": []  # Inicialmente vacío para permitir múltiples respuestas
    }
    result = files_collection.insert_one(file_data)
    return str(result.inserted_id)  # Devuelve el ID del documento insertado

def get_file_by_id(file_id):
    """Obtiene un archivo por su ID."""
    return files_collection.find_one({"_id": ObjectId(file_id)})

def update_file_data(file_id, update_fields):
    """Actualiza los campos de un archivo existente."""
    files_collection.update_one({"_id": ObjectId(file_id)}, {"$set": update_fields})

def delete_file_by_id(file_id):
    """Borra un archivo por su ID y sus datos precomputados asociados."""
    # Primero, obtener los IDs de las respuestas precomputadas asociadas
    file_data = get_file_by_id(file_id)
    
    if file_data:
        precomputed_ids = file_data.get("precomputed_answers", [])
        
        # Borrar las respuestas precomputadas asociadas
        if precomputed_ids:
            precomputed_collection.delete_many({"_id": {"$in": [ObjectId(id) for id in precomputed_ids]}})
    
    # Ahora borrar el archivo
    result = files_collection.delete_one({"_id": ObjectId(file_id)})
    return result.deleted_count > 0  # Devuelve True si se borró con éxito

def delete_all_files():
    """Borra todos los archivos en la colección y sus datos precomputados asociados."""
    all_files = list(files_collection.find())
    
    for file in all_files:
        precomputed_ids = file.get("precomputed_answers", [])
        if precomputed_ids:
            precomputed_collection.delete_many({"_id": {"$in": [ObjectId(id) for id in precomputed_ids]}})
    
    result = files_collection.delete_many({})
    return result.deleted_count  # Devuelve el número de documentos borrados




#CRUD de la data precomputada


def insert_precomputed_data(question, answer, file_id):
    """Inserta una pregunta y respuesta precomputada en la colección."""
    # Verificar si el ID del archivo es válido
    if not files_collection.find_one({"_id": ObjectId(file_id)}):
        raise ValueError(f"El ID del archivo '{file_id}' no es válido.")

    precomputed_data = {
        "question": question,
        "answer": answer,
        "file_id": ObjectId(file_id)  # Referencia al archivo correspondiente
    }
    result = precomputed_collection.insert_one(precomputed_data)
    return str(result.inserted_id)  # Devuelve el ID del documento insertado

def get_precomputed_by_file_id(file_id):
    """Obtiene todas las respuestas precomputadas asociadas a un archivo específico."""
    return list(precomputed_collection.find({"file_id": ObjectId(file_id)}))

def update_precomputed_data(precomputed_id, update_fields):
    """Actualiza los campos de una respuesta precomputada existente."""
    precomputed_collection.update_one({"_id": ObjectId(precomputed_id)}, {"$set": update_fields})

def delete_precomputed_by_id(precomputed_id):
    """Borra una respuesta precomputada por su ID."""
    result = precomputed_collection.delete_one({"_id": ObjectId(precomputed_id)})
    return result.deleted_count > 0  # Devuelve True si se borró con éxito

def delete_precomputed_by_file_id(file_id):
    """Borra todas las respuestas precomputadas asociadas a un archivo específico."""
    result = precomputed_collection.delete_many({"file_id": ObjectId(file_id)})
    return result.deleted_count  # Devuelve el número de documentos borrados

def delete_all_precomputed():
    """Borra todas las respuestas precomputadas en la colección."""
    result = precomputed_collection.delete_many({})
    return result.deleted_count  # Devuelve el número de documentos borrados



# acciones en comun



def link_precomputed_to_file(file_id, precomputed_id):
    """Vincula una respuesta precomputada a un archivo específico."""
    files_collection.update_one(
        {"_id": ObjectId(file_id)},
        {"$push": {"precomputed_answers": precomputed_id}}  # Agrega el ID a la lista
    )


def get_file_with_precomputed(file_id):
    """Obtiene un archivo por su ID junto con sus respuestas precomputadas."""
    file_data = files_collection.find_one({"_id": ObjectId(file_id)})
    if file_data:
        # Obtener las respuestas precomputadas asociadas
        precomputed_ids = file_data.get("precomputed_answers", [])
        precomputed_data = list(precomputed_collection.find({"_id": {"$in": [ObjectId(id) for id in precomputed_ids]}}))
        return {
            "file_data": file_data,
            "precomputed_data": precomputed_data
        }
    return None






# Ejemplo de uso
if __name__ == "__main__":
    # Insertar un archivo (simulación)
    file_id = insert_file_data(
        name="Informe Anual",
        file_type="pdf",
        description="Este es un informe anual sobre el rendimiento.",
        content="Contenido del informe aquí...",
        embedding=[0.1, 0.2, 0.3]  # Ejemplo de embedding
    )
    
    print(f"Archivo insertado con ID: {file_id}")

    # Insertar una pregunta y respuesta precomputada (simulación)
    precomputed_id = insert_precomputed_data(
        question="¿Cuál es el rendimiento anual?",
        answer="El rendimiento anual fue del 10%.",
        file_id=file_id  # Vinculando al archivo correspondiente
    )
    
    print(f"Pregunta precomputada insertada con ID: {precomputed_id}")

    # Vincular la respuesta precomputada al archivo
    link_precomputed_to_file(file_id, precomputed_id)

    # Obtener archivo junto con sus datos precomputados por ID
    file_with_precomputed = get_file_with_precomputed(file_id)
    
    if file_with_precomputed:
        print("Datos del archivo:", file_with_precomputed["file_data"])
        print("Datos precomputados:", file_with_precomputed["precomputed_data"])

    # Borrar un archivo por ID
    if delete_file_by_id(file_id):
        print(f"Archivo con ID {file_id} borrado.")
    
    # Borrar todos los archivos
    deleted_count = delete_all_files()
    print(f"{deleted_count} archivos borrados.")