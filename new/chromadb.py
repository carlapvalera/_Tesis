import chromadb
from chromadb import Client
import torch
from gemini_api import Gemini_API
# Configuración del modelo de embeddings
gemini_API = Gemini_API()

# Inicializar el cliente de Chroma
client = Client()

# Crear o acceder a una colección en Chroma
collection = client.create_collection("anuarios_embeddings")

def embed_text(text:str):
    """Convierte texto a un vector utilizando un modelo preentrenado."""
    return gemini_API.get_embeddings_query(text)  # Devuelve como lista de float

def embed_list_chuncks(chuncks:list[str]):
    """Convierte una lista de textos a un vector utilizando un modelo preentrenado."""
    return gemini_API.get_embeddings_list(chuncks)

def chunk_text(text:str, max_length=200):
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

