import os
import numpy as np
import faiss
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Cargar el modelo y el tokenizador
model_name = "facebook/bart-large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Configurar los documentos (puedes cambiar esto por tus propios documentos)
documents = [
    "La realidad aumentada es una tecnología que superpone información digital sobre el mundo real.",
    "La inteligencia artificial se refiere a la simulación de procesos de inteligencia humana por parte de sistemas informáticos.",
    "El aprendizaje automático es una rama de la inteligencia artificial que se centra en el desarrollo de algoritmos que permiten a las computadoras aprender de los datos.",
    "El procesamiento del lenguaje natural es un campo de la inteligencia artificial que permite a las computadoras entender y generar lenguaje humano."
]

# Crear embeddings para los documentos
def create_embeddings(documents):
    inputs = tokenizer(documents, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        # Obtener las salidas del modelo
        outputs = model(**inputs)
        # Usar el embedding del primer token (CLS) como representación del documento
        embeddings = outputs.last_hidden_state[:, 0, :].numpy()  # Cambiar esto para obtener la representación adecuada
    return embeddings

# Crear índice FAISS
def create_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)  # Usar L2 como métrica
    index.add(embeddings)  # Agregar embeddings al índice
    return index

# Recuperar documentos relevantes
def retrieve_documents(query, index, documents):
    query_embedding = create_embeddings([query])
    distances, indices = index.search(query_embedding, k=2)  # Recuperar los dos documentos más cercanos
    return [documents[i] for i in indices[0]]

# Generar respuesta usando el modelo
def generate_response(query):
    relevant_docs = retrieve_documents(query, faiss_index, documents)
    context = " ".join(relevant_docs)  # Concatenar documentos relevantes como contexto
    
    # Preparar entrada para el modelo
    input_text = f"Contexto: {context} Pregunta: {query}"
    
    inputs = tokenizer(input_text, return_tensors="pt", padding=True)
    
    # Generar respuesta
    with torch.no_grad():
        output_ids = model.generate(inputs['input_ids'], max_length=150)
    
    response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return response

# Crear embeddings y FAISS index
embeddings = create_embeddings(documents)
faiss_index = create_faiss_index(embeddings)

# Ejemplo de uso
if __name__ == "__main__":
    query = "¿Qué es la realidad aumentada?"
    response = generate_response(query)
    
    print("Consulta:", query)
    print("Respuesta del modelo:", response)