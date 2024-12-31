import faiss
import numpy as np
from gemini_api import Gemini_API
import os
import json
from document import Document

class DB_Embed:
    def __init__(self,mapping_filename = 'document_mapping.json',index_filename = 'mi_indice.faiss',dimension = 768):
        # Inicializar la API Gemini
        self.mapping_filename = mapping_filename
        self.index_filename =index_filename
        self.gemini_API = Gemini_API()
        self.unique_embeddings = set()
        self.index = None
        self.document_mapping = None
        self.initial_db(index_filename,dimension,mapping_filename)
        
        
    def initial_db(self,index_filename,d,mapping_filename):
       # Crear o cargar un índice FAISS
        
        self.index = self.load_index(index_filename)

        if self.index is None:
              # Ajusta según tu modelo (por ejemplo, si Gemini usa 768 dimensiones)
            self.index = faiss.IndexFlatIP(d)  # Usar producto interno como métrica para similaridad del coseno

        # Cargar o inicializar el mapeo de documentos
        
        self.document_mapping = self.load_mapping(mapping_filename)
        # Conjunto para rastrear embeddings únicos
        for doc in self.document_mapping:
            self.unique_embeddings.add(doc)

    def embed_text(self,text: str):
        """Convierte texto a un vector utilizando un modelo preentrenado."""
        return self.gemini_API.get_embeddings_query(text)  # Devuelve como lista de float

    def embed_list_text(self,texts: list[str]):
        """Convierte una lista de textos a un vector utilizando un modelo preentrenado."""
        return self.gemini_API.get_embeddings_list(texts)

    def chunk_text(self,text: str, max_length=200):
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

    def save_index(self):
        """Guarda el índice FAISS en un archivo."""
        faiss.write_index(self.index, self.index_filename)

    def load_index(self,filename):
        """Carga el índice FAISS desde un archivo, si existe."""
        if os.path.exists(filename):
            return faiss.read_index(filename)
        else:
            return None

    def save_mapping(self):
        """Guarda el mapeo de documentos en un archivo JSON."""
        with open(self.mapping_filename, 'w', encoding='utf-8') as f:
            json.dump(self.document_mapping, f)

    def load_mapping(self,filename):
        """Carga el mapeo de documentos desde un archivo JSON, si existe."""
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return []
        
    def set_text(self,doc:Document ):
        # Almacenar los embeddings en FAISS
        if doc.textEmbed:  # Verificar que el chunk no esté vacío
            vector = self.gemini_API.embed_text(doc.text)
            normalized_vector = vector / np.linalg.norm(vector)  # Normalizar el vector
            
            

            if doc.direction not in self.unique_embeddings:  # Verificar si ya existe
                self.index.add(np.array([normalized_vector], dtype=np.float32))  # Añadir el vector normalizado al índice
                self.unique_embeddings.add(doc.direction)  # Añadir al conjunto
                
                # Guardar el texto asociado al embedding
                self.document_mapping.append(doc.direction)

        # Guardar el índice y el mapeo al finalizar
        self.save_index()
        self.save_mapping()

    def most_relevant(self,normalized_query_vector, k = 2):
        # Buscar los k vecinos más cercanos
        D, I = self.index.search(np.array([normalized_query_vector], dtype=np.float32), k)
        return (D,I)


