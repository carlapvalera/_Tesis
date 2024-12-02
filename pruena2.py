from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Definir el nombre del modelo
model_name = "distilgpt2"

print("Cargando el tokenizador y el modelo...")
try:
    # Cargar el tokenizador y el modelo
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)
    print("Modelo y tokenizador cargados exitosamente.")
except Exception as e:
    print(f"Error al cargar el modelo o tokenizador: {e}")
    exit()

# Configurar el dispositivo (GPU si está disponible)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Función para generar respuestas basadas en una entrada
def generate_response(input_text):
    try:
        # Tokenizar la entrada
        inputs = tokenizer(input_text, return_tensors="pt").to(device)
        print("Entrada tokenizada.")

        # Generar la respuesta
        with torch.no_grad():
            outputs = model.generate(**inputs, max_length=150)  # Ajusta max_length según sea necesario
        print("Respuesta generada.")

        # Decodificar la respuesta generada
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
    except Exception as e:
        print(f"Error al generar respuesta: {e}")
        return None

# Ejemplo de uso para comprobar el funcionamiento del modelo
input_text = "¿Cómo puedo insertar un nuevo registro en una tabla?"
print(f"Generando respuesta para la entrada: '{input_text}'")
response = generate_response(input_text)

# Imprimir la respuesta del modelo
if response:
    print("Entrada:", input_text)
    print("Respuesta del modelo:", response)
else:
    print("No se pudo generar una respuesta.")
    