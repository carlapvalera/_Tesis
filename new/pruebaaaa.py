import os
from dotenv import load_dotenv
import google.generativeai as genai

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la clave API desde las variables de entorno
api_key = os.getenv("API_KEY")

# Configura Google Generative AI con la clave API
genai.configure(api_key=api_key)

result = genai.embed_content(
    model="models/embedding-001",
    content="What is the meaning of life?",
    task_type="retrieval_document")

# 1 input > 1 vector output
print(str(result['embedding'])[:50], '... TRIMMED]')