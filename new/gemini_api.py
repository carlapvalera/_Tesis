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
        return result['embedding']

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
        results = []
        for v in result['embedding']:
            results.append(v)
        return results
                

    def give_table(self,text:str):
        "devuelve la tabla correspondiente"
        
        response =self.model.generate_content(f"""
    a partir de un string que representa una tabla.{text}

        dame los siguientes apartados:

        **Nombre de la tabla:**
        **Encabezados:**
        **DataFrame:**separado por |
        el nombre de la tabla, los encabezados y el DataFrame .
    """
)
    
        # Comprobar si la respuesta es válida y estructurada
        if not response or not hasattr(response, 'text'):
            raise ValueError("No se recibió una respuesta válida de la API.")

        return response.text 
    
    def generate_response(self, query: str, context: str) -> str:
        """Genera una respuesta utilizando la Gemini API."""
        
        # Construir el mensaje que se enviará al modelo
        message = (
            f"Contexto: {context}\n"
            f"Consulta: {query}\n"
            "Por favor, responde la query puedes apoyyarte en el contexto proporcionado para darla lo mas detallada posible ."
        )

        # Iniciar un chat con el modelo
        chat = genai.GenerativeModel('gemini-pro').start_chat(history=[])
        response = chat.send_message(message)
        
        return response.text


    def evaluate_response(self, expected_response: str, generated_response: str) -> str:
        """
        Evalúa qué tan buena es una respuesta generada en comparación con una respuesta esperada.
        
        Args:
            expected_response (str): La respuesta esperada.
            generated_response (str): La respuesta generada por el modelo.
        
        Returns:
            str: Una evaluación detallada sobre qué tan buena fue la respuesta generada.
        """
        
        prompt = f"""
            Evalúa qué tan buena es esta respuesta generada respecto a la esperada. Proporciona un análisis detallado y una calificación del 0 al 10.

            Respuesta esperada:
            {expected_response}

            Respuesta generada:
            {generated_response}

            Incluye las siguientes secciones en tu evaluación:
            1. Similitud semántica (del 0 al 10) : ( la calificacion con un número del 0 al 10).
            """ 
        
        response = self.model.generate_content(prompt)
        
        if not response or not hasattr(response, 'text'):
            raise ValueError("No se recibió una respuesta válida de la API.")
        

        number_index = response.text.find(":")+len(":")
        last = response.text.find("**",number_index)
        last1 = response.text.find("/",number_index)
        if last !=-1 and last1!=-1:
            last = min(last,last1)
        elif last ==-1:
            last = last1
        else:
            last = last
        
        number = response.text[number_index:last]

        return int(number)
    
    
    

gem = Gemini_API()
print(gem.evaluate_response("El coche azul está estacionado frente a la casa.","El coche rojo está estacionado frente a la casa."))