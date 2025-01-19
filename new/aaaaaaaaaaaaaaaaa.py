import numpy as np
from qdrant_client import QdrantClient
from gemini_api import Gemini_API
from qdrant_client.models import VectorParams, Distance
# Inicializar el cliente Qdrant
client = QdrantClient(host='localhost', port=6333)

# Crear una colección en Qdrant
collection_name = 'text_embeddings'
client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=768, distance=Distance.COSINE) 
 ) # Ajusta el tamaño según tu modelo

# Inicializar el modelo para generar embeddings
gem = Gemini_API()
#model = SentenceTransformer('msmarco-MiniLM-L-6-v3')

# Función para insertar textos en Qdrant
def insert_texts(texts):
    # Generar embeddings para los textos
    embeddings = gem.get_embeddings_query(texts)

    # Convertir a tipo float32 para Qdrant
    embeddings = np.array(embeddings, dtype=np.float32)

    # Crear puntos con IDs y payloads opcionales
    points = [
        {
            'id': str(i),  # ID único como string
            'vector': embedding.tolist(),  # Vector como lista
            'payload': {'text': text}  # Payload opcional con el texto original
        }
        for i, (embedding, text) in enumerate(zip(embeddings, texts))
    ]

    # Upsert (insertar o actualizar) los puntos en la colección
    client.upsert(collection_name=collection_name, points=points)

# Ejemplo de uso: insertar textos en Qdrant
texts_to_insert = [
    "Hola, mundo!",
    "Este es un ejemplo de cómo usar Qdrant.",
    "Los embeddings son útiles para la búsqueda semántica."
]

insert_texts(texts_to_insert)

# Consultar los documentos más relevantes para un texto dado
def query_similar_text(query_text, top_k=3):
    query_embedding = model.encode([query_text]).astype(np.float32)
    
    results = client.search(
        collection_name=collection_name,
        query_vector=query_embedding[0].tolist(),
        limit=top_k
    )
    
    return results

# Ejemplo de consulta
query_result = query_similar_text("¿Cómo se usa Qdrant?", top_k=3)
for result in query_result:
    print(f"ID: {result.id}, Score: {result.score}, Text: {result.payload['text']}")
