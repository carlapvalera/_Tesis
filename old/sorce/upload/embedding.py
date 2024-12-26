from sentence_transformers import SentenceTransformer

# Cargar el modelo
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embeddings(text):
    return model.encode(text)

# Ejemplo de uso
text = "Spiderman was a particularly entertaining movie."
embeddings = generate_embeddings(text)
print(embeddings)