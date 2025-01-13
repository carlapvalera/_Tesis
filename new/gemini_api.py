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

    Returns:
        el nombre de la tabla, los encabezados y el DataFrame.
    """
)
    
        # Comprobar si la respuesta es válida y estructurada
        if not response or not hasattr(response, 'text'):
            raise ValueError("No se recibió una respuesta válida de la API.")

        return response.text 
    


gem = Gemini_API()

table = gem.give_table("1.1 - Situación geográfica de Cuba  CONCEPTO Lugar Provincias Latitud Norte Greenwich Archipiélago Cubano    Extremo septentrional Cayo Cruz del Padre Matanzas 23º16' 80º55'    Extremo meridional Punta del Inglés Granma 19º49' 77º40'    Extremo oriental Punta de Maisí Guantánamo 20º13' 74º08'    Extremo occidental Cabo de San Antonio Pinar del Río 21º52' 84º57'  Isla de Cuba (a)    Extremo septentrional Punta Hicacos Matanzas 23º11' 81º09'  Isla de la Juventud    Extremo septentrional Punta de Tirry - 21º57' 82º58'    Extremo meridional Caleta de Agustín Jol - 21º26' 82º54'    Extremo oriental Punta del Este - 21º34' 82º33'    Extremo occidental Punta Francés - 21º38' 83º11' (a) Los demás puntos extremos de la Isla de Cuba son los mismos señalados para la totalidad del archipiélago. Fuente: Síntesis Geográfica, Económica y Cultural de Cuba, versión digital, año 2017 y mapa plegable, Cuba. División                Político - Administrativa, año 2011. ")

print( "ya")
print(table)
