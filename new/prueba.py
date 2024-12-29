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
def extract_text_and_tables(input_string):
    model = genai.GenerativeModel("gemini-pro")
    
    # Generar contenido basado en el input
    response = model.generate_content(f"Este es el string correspondiente a leer un PDF posee tanto texto y como tablas que se encuentran en el: {input_string}. A a partir del string[i] solo hay tablas dime el valor d i")
    
    # Comprobar si la respuesta es válida y estructurada
    if not response or not hasattr(response, 'text'):
        raise ValueError("No se recibió una respuesta válida de la API.")

    return response.text 


# Ejemplo de uso
file_path = 'C:\\blabla\\_Tesis\\temporal\\texto_extraido.txt' 
with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
input_string = text
output_text = extract_text_and_tables(input_string)

print("Texto extraído:", output_text)
