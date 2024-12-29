import os
from dotenv import load_dotenv
import google.generativeai as genai

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la clave API desde las variables de entorno
api_key = os.getenv("API_KEY")

# Configura Google Generative AI con la clave API
genai.configure(api_key=api_key)

# Función para extraer texto y tablas del string
def count_tokens_in_file(file_path):

    # Leer el contenido del archivo
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    

    model = genai.GenerativeModel("gemini-pro")
    
    # Generar contenido basado en el input
    response = model.count_tokens(text)

    return response




# Ejemplo de uso
file_path = 'C:\\blabla\\_Tesis\\temporal\\texto_extraido.txt' 
 # Cambia esto por la ruta a tu archivo
num_tokens = count_tokens_in_file(file_path)
print(f"Número total de tokens en el archivo: {num_tokens}")



