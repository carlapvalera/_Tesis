from transformers import LlamaForCausalLM, LlamaTokenizer
import torch

# Definir el nombre del modelo
model_name = "RUCKBReasoning/TableLLM-13b"
save_directory = "./saved_model"
# Cargar el tokenizador y el modelo
tokenizer = LlamaTokenizer.from_pretrained(model_name)
tokenizer.save_pretrained(save_directory)
model = LlamaForCausalLM.from_pretrained(model_name)
model.save_pretrained(save_directory)

print(f"Modelo y tokenizador guardados en: {save_directory}")

# Configurar el dispositivo (GPU si está disponible)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Guardar el modelo y el tokenizador en un directorio específico




# Función para generar respuestas basadas en una entrada
def generate_response(input_text):
    # Tokenizar la entrada
    inputs = tokenizer(input_text, return_tensors="pt").to(device)
    
    # Generar la respuesta
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=150)  # Ajusta max_length según sea necesario
    
    # Decodificar la respuesta generada
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Ejemplo de uso
input_text = "¿Cómo puedo insertar un nuevo registro en una tabla?"
response = generate_response(input_text)
print("Respuesta del modelo:", response)

