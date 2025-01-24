import faiss
import numpy as np
from gemini_api import Gemini_API
import os
import json
from document import Document
from typing import List, Tuple
import pickle

class Embed:
    def __init__(self, doc :Document, embed):
        self.doc = doc
        self.embed = embed
        
class DB_Embed:
    def __init__(self,mapping_filename = 'document_mapping.json',index_filename = 'mi_indice.faiss',dimension = 768, filename='embeddings.pkl'):
        # Inicializar la API Gemini
        self.mapping_filename = mapping_filename
        self.index_filename =index_filename
        self.gemini_API = Gemini_API()
        self.unique_embeddings = set()
        self.index = None
        self.document_mapping = None
        self.initial_db(index_filename,dimension,mapping_filename)
        self.set = set()
        self.filename = filename
        self.load_embeddings()  # Cargar embeddings al instanciar la clase
        
        
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
        
    """ def set_text(self,doc:Document ):
        # Almacenar los embeddings en FAISS
        if doc.text: 
             # Verificar que el chunk no esté vacío
            if doc.id not in self.unique_embeddings:
                    
                text_to_embed = self.chunk_text(doc.text, 5000)
                normalized_vector = self.gemini_API.get_embeddings_query(text_to_embed)
                
                #vector = self.gemini_API.get_embeddings_query(doc.text)
                #normalized_vector = vector / np.linalg.norm(vector)  # Normalizar el vector
                
                self.index.add(np.array([normalized_vector], dtype=np.float32))  # Añadir el vector normalizado al índice
                self.unique_embeddings.add(doc.id)  # Añadir al conjunto
                
                # Guardar el texto asociado al embedding
                self.document_mapping.append(doc.id)

        # Guardar el índice y el mapeo al finalizar
        self.save_index()
        self.save_mapping()"""

    def set_text(self,doc:Document ):
         # Almacenar los embeddings en FAISS
        if doc.text: 
             # Verificar que el chunk no esté vacío
            if not any(embed.doc.id == doc.id and embed.doc.text == doc.text for embed in self.set):
                    
                text_to_embed = self.chunk_text(doc.text, 5000)
                for vect in text_to_embed:
                    normalized_vector = self.gemini_API.get_embeddings_query(vect)
                
                #vector = self.gemini_API.get_embeddings_query(doc.text)
                #normalized_vector = vector / np.linalg.norm(vector)  # Normalizar el vector
                
                    self.set.add(Embed(doc, normalized_vector))  # Convertir a tupla

                # Guardar los embeddings después de añadir uno nuevo
                self.save_embeddings()
    

    def normalized_query(self,query_vector):
        return query_vector / np.linalg.norm(query_vector)  # Normalizar el vector de consulta

    """def most_relevant(self,query_vector, k = 2):
        
        vector = self.gemini_API.get_embeddings_query(query_vector)
        normalized_query_vector = self.normalized_query(vector)
        # Buscar los k vecinos más cercanos
        D, I = self.index.search(np.array([normalized_query_vector], dtype=np.float32), k)
        return D,I"""
    def cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Calcula la similitud del coseno entre dos vectores."""
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def most_relevant(self, queryvector:str, k=2) -> List[Tuple[Document, float]]:
        """
        Encuentra los k documentos más relevantes para un vector de consulta.
        
        :param query_vector: El embedding de consulta.
        :param k: Número de resultados más relevantes a devolver.
        :return: Lista de tuplas (documento, similitud), ordenadas por relevancia.
        """
        query_vector = self.gemini_API.get_embeddings_query(queryvector)
        similarities = []

        # Calcular la similitud del coseno entre el query_vector y cada embedding almacenado
        for doc_embed  in self.set:
            similarity = self.cosine_similarity(query_vector, doc_embed.embed)
            similarities.append((doc_embed.doc, similarity))

        # Ordenar los documentos por similitud en orden descendente
        similarities = sorted(similarities, key=lambda x: x[1], reverse=True)

        # Devolver los k más relevantes
        return similarities[:k]



    def get_doc_by_id(self, idx):
        return self.document_mapping[idx]

    def save_embeddings(self):
        """Guardar el conjunto de embeddings en un archivo."""
        with open(self.filename, 'wb') as f:
            pickle.dump(self.set, f)

    def load_embeddings(self):
        """Cargar el conjunto de embeddings desde un archivo."""
        try:
            with open(self.filename, 'rb') as f:
                self.set = pickle.load(f)
        except FileNotFoundError:
            print("No se encontró el archivo de embeddings. Se iniciará un nuevo conjunto.")


# Ejemplo de uso
if __name__ == "__main__":
    store = DB_Embed()

    # Crear algunos documentos de ejemplo
    doc1 = "Este es el primer documento."
    doc2 = "Este es el segundo documento."
    
    # Simular la API que devuelve embeddings (reemplazar con tu implementación real)
    api = Gemini_API()
    doc = Document(2,doc1)
    doccc = Document(3,doc2)

    for embed in store.set:
        comparison_result = embed.doc.id == doc.id and embed.doc.text == doc.text  # Comparar el documento en la tupla  

        print(f"Comparando con: {embed}, Resultado: {comparison_result}")

    # Almacenar los documentos
    store.set_text(doc)
    store.set_text(doccc)

    # Crear un vector de consulta aleatorio
    query_embedding = "segundo"
    
    # Encontrar los dos documentos más relevantes
    top_k_results = store.most_relevant(query_embedding, k=2)

    # Imprimir resultados
    for doc, score in top_k_results:
        print(f"Documento: {doc.text}, Similitud: {score}")