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
        #data_table = self.string_to_dataframe(data)

        return name, headers, data



