import os
from dotenv import load_dotenv
import google.generativeai as genai
import pandas as pd

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
    response = model.generate_content(f"Este es el string correspondiente a leer un PDF. Dame el texto y las tablas que se encuentran en el: {input_string}")
    
    # Comprobar si la respuesta es válida y estructurada
    if not response or not hasattr(response, 'text'):
        raise ValueError("No se recibió una respuesta válida de la API.")
    
    output_text = response.text  # Texto extraído
    
    # Aquí se puede agregar lógica para identificar y extraer tablas del texto
    tables = extract_tables_from_text(output_text)  # Suponiendo que tienes una función para esto
    
    # Guardar el texto en un archivo .txt
    with open('texto_extraido.txt', 'w', encoding='utf-8') as text_file:
        text_file.write(output_text)
    
    # Guardar las tablas en un archivo CSV si hay alguna tabla extraída
    if tables:
        df = pd.DataFrame(tables)
        df.to_csv('tablas_extraidas.csv', index=False)

    return output_text, tables

def extract_tables_from_text(text):
    """
    Función para extraer tablas del texto.
    Este es un ejemplo básico; deberías implementar la lógica específica según cómo se estructuran las tablas en el texto.
    """
    tables = []
    
    # Aquí puedes agregar lógica para analizar el texto y extraer las tablas.
    # Por ejemplo, podrías dividir el texto por líneas y buscar patrones específicos.
    
    # Ejemplo ficticio: suponer que las tablas están separadas por líneas con "Table:"
    for line in text.split('\n'):
        if line.startswith("Table:"):
            table_data = line.replace("Table:", "").strip().split(',')
            tables.append(table_data)

    return tables

# Ejemplo de uso
input_string = "1.4 - Extensión superficial, población efectiva y densidad de población, año 2021Extensión superficial (km2         Població Densidad de              CayoÁrea defectiv poblaciónCONCEPTTota  adyacentetierra firm         (U)(hab/km2)Archipiélago cuban109 884,03 126,4106 757,610 885 3499,1 ..."
output_text, extracted_tables = extract_text_and_tables(input_string)

print("Texto extraído:", output_text)
print("\nTablas extraídas:")
for table in extracted_tables:
    print(table)
