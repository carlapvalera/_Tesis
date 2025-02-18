from pymongo import MongoClient

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

# Ejemplo: Obtener todos los documentos de la colección 'LLM'
try:
    documents = collection.find()  # Obtiene todos los documentos
    for doc in documents:
        print(doc)  # Imprime cada documento
except Exception as e:
    print("Error al obtener documentos:", e)

# Ejemplo: Insertar un nuevo documento en la colección 'LLM'
new_document = {
    "pregunta": "¿Cuál es la capital de Francia?",
    "respuesta": "París",
    "detalle_archivo": "N/A",
    "voto": 0
}

try:
    result = collection.insert_one(new_document)  
    print (result)# Inserta un nuevo documento
    print("Documento insertado con ID:", result.inserted_id)
except Exception as e:
    print("Error al insertar documento:", e)


# Ejemplo: Eliminar un documento específico (por ejemplo, donde la pregunta sea "¿Cuál es la capital de Francia?")
try:
    result = collection.delete_one({"pregunta": "¿Cuál es la capital de Francia?"})
    print(f"Documentos eliminados: {result.deleted_count}")  # Muestra cuántos documentos fueron eliminados
except Exception as e:
    print("Error al eliminar el documento:", e)


# Ejemplo: Eliminar todos los documentos de la colección 'LLM'
try:
    result = collection.delete_many({})  # Elimina todos los documentos
    print(f"Documentos eliminados: {result.deleted_count}")  # Muestra cuántos documentos fueron eliminados
except Exception as e:
    print("Error al vaciar la colección:", e)