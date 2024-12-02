from transformers import RagTokenizer, RagRetriever, RagSequenceForGeneration
import torch

# Definir el nombre del modelo
model_name = "facebook/rag-sequence"
huggingface_token = "tu_token_aqui"  # Reemplaza esto con tu token

print("Cargando el tokenizador y el modelo...")
try:
    # Cargar el tokenizador y el modelo RAG usando autenticación
    tokenizer = RagTokenizer.from_pretrained(model_name, use_auth_token=huggingface_token)
    model = RagSequenceForGeneration.from_pretrained(model_name, use_auth_token=huggingface_token)
    print("Modelo y tokenizador cargados exitosamente.")
except Exception as e:
    print(f"Error al cargar el modelo o tokenizador: {e}")
    exit()

# Configurar el dispositivo (GPU si está disponible)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Inicializar el recuperador
retriever = RagRetriever.from_pretrained(model_name, use_auth_token=huggingface_token, use_dummy_dataset=True)

# Función para generar respuestas basadas en una entrada
def generate_response(input_text):
    inputs = tokenizer(input_text, return_tensors="pt").to(device)
    retrieved_docs = retriever(input_ids=inputs['input_ids'], return_tensors="pt")
    
    with torch.no_grad():
        outputs = model.generate(input_ids=inputs['input_ids'], 
                                 context_input_ids=retrieved_docs['context_input_ids'], 
                                 max_length=150)

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Ejemplo de uso
input_text = "¿Qué es la realidad aumentada?"
response = generate_response(input_text)

print("Entrada:", input_text)
print("Respuesta del modelo:", response)

# Guardar el modelo y el tokenizador
save_directory = "./saved_rag_model"
tokenizer.save_pretrained(save_directory)
model.save_pretrained(save_directory)
print(f"Modelo y tokenizador guardados en: {save_directory}")