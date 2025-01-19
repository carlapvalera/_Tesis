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
        self.save_mapping()

    
    def normalized_query(self,query_vector):
        return query_vector / np.linalg.norm(query_vector)  # Normalizar el vector de consulta

    def most_relevant(self,query_vector, k = 2):
        
        vector = self.gemini_API.get_embeddings_query(query_vector)
        normalized_query_vector = self.normalized_query(vector)
        # Buscar los k vecinos más cercanos
        D, I = self.index.search(np.array([normalized_query_vector], dtype=np.float32), k)
        return D,I
            


    def get_doc_by_id(self, idx):
        return self.document_mapping[idx]




# Ejemplo de uso
if __name__ == "__main__":
    # Crear una instancia de la base de datos
    db = DB_Embed()

    # Cargar un archivo o crear documentos manualmente
    # Aquí se puede cargar desde un archivo o definir textos directamente
    example_texts = [
        "Este es un ejemplo de texto para embebido 1.",
        "Este es otro texto que se almacenará en la base de datos.",
        "Este texto es diferente y también debe ser almacenado."
    ]

    # Insertar documentos en la base de datos
    for text in example_texts:
        doc = Document( text +"1",text)
        db.set_text(doc)

    # Realizar una consulta para buscar el chunk más similar
    query_text = "¿Qué es un ejemplo de texto?"  # Ejemplo de consulta
    query_vector = db.embed_text(query_text)
    normalized_query_vector = db.normalized_query(query_vector)

    # Obtener los k vecinos más cercanos
    k = 2  # Número de resultados deseados
    distances, indices = db.most_relevant(normalized_query_vector, k)

    print("Indices de los vecinos más cercanos:\n", indices)
    print("Distancias (producto interno):\n", distances)

    # Recuperar y mostrar los textos correspondientes a los índices encontrados
    for idx in indices[0]:
        print(f"Texto correspondiente al índice {idx}:\n{db.document_mapping[idx]}\n")