from pymongo import MongoClient

# Crear una conexión al servidor de MongoDB
client = MongoClient('localhost', 27017)

# Probar la conexión
try:
    client.admin.command('ping')  # Esto envía un comando ping para verificar la conexión
    print("Conexión exitosa a MongoDB")
except Exception as e:
    print("Error al conectar a MongoDB:", e)

# Seleccionar una base de datos
db = client['nombre_de_tu_base_de_datos']  # Cambia esto por el nombre real de tu base de datos

# Imprimir los nombres de las colecciones en la base de datos
collections = db.list_collection_names()
print("Colecciones en la base de datos:", collections)