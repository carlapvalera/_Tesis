import pandas as pd
from io import StringIO
from gemini_api import Gemini_API
class DataFrameCreator:
    def __init__(self):
        self.gemini_api = Gemini_API()

    def string_to_dataframe(self,table_string: str) -> pd.DataFrame:
        # Limpiar el string y reemplazar los separadores de tabla por comas
        cleaned_string = table_string.strip().replace('|', ',').replace('---', '').strip()
        
        # Usar StringIO para simular un archivo
        string_data = StringIO(cleaned_string)

        # Leer los datos en un DataFrame usando pd.read_csv()
        df = pd.read_csv(string_data, sep=',', engine='python', skipinitialspace=True)  # Usar ',' como separador
        
        return df
    

    def get_table(self,text:str):
        """Extrae una tabla de un texto utilizando un modelo preentrenado."""
        parts = self.gemini_api.give_table(text)

        name_index = parts.find("**Nombre de la tabla:**")
        encabezado_index = parts.find("**Encabezados:**")
        data_index = parts.find("**DataFrame:**")

        name = parts[name_index+len("**Nombre de la tabla:**"):encabezado_index]
        encabezados = parts[encabezado_index+len("**Encabezados:**"):data_index]
        data = parts[data_index+len("**DataFrame:**"):]
        data_table = self.string_to_dataframe(data)

        return name, encabezados, data_table


def get_table(self, text: str):
        """Extrae una tabla de un texto utilizando un modelo preentrenado."""
        parts = self.gemini_api.give_table(text)

        # Suponiendo que 'parts' es un string que contiene el formato esperado
        name_index = parts.find("**Nombre de la tabla:**")
        headers_index = parts.find("**Encabezados:**")
        data_index = parts.find("**DataFrame:**")

        name = parts[name_index + len("**Nombre de la tabla:**"):headers_index]
        headers = parts[headers_index + len("**Encabezados:**"):data_index]
        data = parts[data_index + len("**DataFrame:**"):]

        # Convertir el string de datos a DataFrame
        data_table = self.string_to_dataframe(data)

        return name, headers, data_table

# Ejemplo de uso
if __name__ == "__main__":
    creator = DataFrameCreator()

    # Simulando un texto de entrada para extraer una tabla
    input_text = "1.1 - Situación geográfica de Cuba  CONCEPTO Lugar Provincias Latitud Norte Greenwich Archipiélago Cubano    Extremo septentrional Cayo Cruz del Padre Matanzas 23º16' 80º55'    Extremo meridional Punta del Inglés Granma 19º49' 77º40'    Extremo oriental Punta de Maisí Guantánamo 20º13' 74º08'    Extremo occidental Cabo de San Antonio Pinar del Río 21º52' 84º57'  Isla de Cuba (a)    Extremo septentrional Punta Hicacos Matanzas 23º11' 81º09'  Isla de la Juventud    Extremo septentrional Punta de Tirry - 21º57' 82º58'    Extremo meridional Caleta de Agustín Jol - 21º26' 82º54'    Extremo oriental Punta del Este - 21º34' 82º33'    Extremo occidental Punta Francés - 21º38' 83º11' (a) Los demás puntos extremos de la Isla de Cuba son los mismos señalados para la totalidad del archipiélago. Fuente: Síntesis Geográfica, Económica y Cultural de Cuba, versión digital, año 2017 y mapa plegable, Cuba. División                Político - Administrativa, año 2011. "
    
    # Llamar al método get_table para obtener la tabla
    name, headers, df = creator.get_table(input_text)

    # Mostrar los resultados
    print("Nombre de la Tabla:", name)
    print("Encabezados:", headers)
    print("DataFrame:")
    print(df)