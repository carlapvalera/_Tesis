import pandas as pd
from io import StringIO

class DataFrameCreator:
    @staticmethod
    def string_to_dataframe(table_string: str) -> pd.DataFrame:
        # Limpiar el string y reemplazar los separadores de tabla por comas
        cleaned_string = table_string.strip().replace('|', ',').replace('---', '').strip()
        
        # Usar StringIO para simular un archivo
        string_data = StringIO(cleaned_string)

        # Leer los datos en un DataFrame usando pd.read_csv()
        df = pd.read_csv(string_data, sep=',', engine='python', skipinitialspace=True)  # Usar ',' como separador
        
        return df

