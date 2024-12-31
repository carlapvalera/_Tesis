import faiss
import numpy as np
import os
from gemini_api import Gemini_API

# Inicializar la API Gemini
gemini_API = Gemini_API()

def embed_text(text: str):
    """Convierte texto a un vector utilizando un modelo preentrenado."""
    return gemini_API.get_embeddings_query(text)  # Devuelve como lista de float

def chunk_text(text: str, max_length=200):
    """Divide el texto en chunks de longitud máxima especificada."""
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 > max_length:
            chunks.append(current_chunk.strip())
            current_chunk = sentence  # Comenzar un nuevo chunk
        else:
            current_chunk += " " + sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def save_index(index, filename):
    """Guarda el índice FAISS en un archivo."""
    faiss.write_index(index, filename)

def load_index(filename):
    """Carga el índice FAISS desde un archivo, si existe."""
    if os.path.exists(filename):
        return faiss.read_index(filename)
    else:
        return None

# Ejemplo de uso
if __name__ == "__main__":
    # Cargar el contenido del archivo (ejemplo)
    file_path = 'C:\\blabla\\_Tesis\\temporal\\texto_extraido.txt'  # Cambia esto por la ruta a tu archivo
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Dividir el texto en chunks
    chunks = chunk_text(text, max_length=200)

    # Crear o cargar un índice FAISS
    index_filename = 'mi_indice.faiss'
    index = load_index(index_filename)

    if index is None:
        d = 768  # Ajusta según tu modelo (por ejemplo, si Gemini usa 768 dimensiones)
        index = faiss.IndexFlatIP(d)  # Usar producto interno como métrica para similaridad del coseno

    a = 0
    # Almacenar los embeddings en FAISS
    for chunk in chunks:
        
        if a ==10:
            break

        if chunk:  # Verificar que el chunk no esté vacío
            vector = embed_text(chunk)
            normalized_vector = vector / np.linalg.norm(vector)  # Normalizar el vector
            index.add(np.array([normalized_vector], dtype=np.float32))  # Añadir el vector normalizado al índice

        a = a+1

    print("Embeddings guardados en FAISS.")

    # Guardar el índice al finalizar
    save_index(index, index_filename)

    # Realizar una consulta para buscar el chunk más similar
    query_text = "¿Qué es la inteligencia artificial?"  # Ejemplo de consulta
    query_vector = embed_text(query_text)
    normalized_query_vector = query_vector / np.linalg.norm(query_vector)  # Normalizar el vector de consulta

    # Buscar los k vecinos más cercanos
    k = 5
    D, I = index.search(np.array([normalized_query_vector], dtype=np.float32), k)

    print("Indices de los vecinos más cercanos:\n", I)
    print("Distancias (producto interno):\n", D)
