import os
from dotenv import load_dotenv
import google.generativeai as genai

class Gemini_API:
    def __init__(self):
        # Cargar las variables de entorno desde el archivo .env
        load_dotenv()
        self.api_key = os.getenv("API_KEY")
        # Configura Google Generative AI con la clave API
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-pro")

    def count_tokens(self, text:str):
        """Cuenta los tokens en el texto utilizando la API de Google Generative AI."""
        return self.model.count_tokens(text)

    def get_embeddings_query(self,query:str):
        "RETRIEVAL_QUERY"
        """Método para obtener embeddings .Especifica que el texto dado es una consulta en un parámetro de configuración de búsqueda/recuperación."""
        result = genai.embed_content(
        model="models/embedding-001",
        content=query,
        task_type="retrieval_document")

        # 1 input > 1 vector output
        print(str(result['embedding'])[:50], '... TRIMMED]')
        return result

    def get_embeddings_list(self,lista:list[str]):
        "RETRIEVAL_QUERY"
        "Especifica que el texto dado es una consulta en un parámetro de configuración de búsqueda/recuperación."
        
        result = genai.embed_content(
        model="models/embedding-001",
        content=lista,
        task_type="retrieval_document")

        # A list of inputs > A list of vectors output
        for v in result['embedding']:
            print(str(v)[:50], '... TRIMMED ...')
        return result
                



# Ejemplo de uso
if __name__ == "__main__":
    # Inicializar la clase Gemini_API
    gemini_api = Gemini_API()

    # Leer el contenido del archivo
    file_path = 'C:\\blabla\\_Tesis\\temporal\\texto_extraido.txt'  # Cambia esto por la ruta a tu archivo
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Contar los tokens en el texto
        num_tokens = gemini_api.count_tokens(text)
        print(f"Número total de tokens en el archivo: {num_tokens}")

        # Obtener embeddings para una consulta específica
        query = "¿Cuáles son los beneficios de usar IA generativa?"
        embeddings_query = gemini_api.get_embeddings_query(query)

        # Obtener embeddings para una lista de consultas
        queries_list = [
            "¿Qué es la inteligencia artificial?",
            "¿Cómo funciona el aprendizaje automático?",
            "Ejemplos de aplicaciones de IA."
        ]
        embeddings_list = gemini_api.get_embeddings_list(queries_list)

    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no se encuentra.")
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")