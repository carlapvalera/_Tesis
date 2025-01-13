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

# Definir el string que representa la tabla
table_string = """
| CONCEPTO | Lugar | Provincias | Latitud Norte | Greenwich |
|---|---|---|---|---|
| Extremo septentrional | Cayo Cruz del Padre | Matanzas | 23º16' | 80º55' |
| Extremo meridional | Punta del Inglés | Granma | 19º49' | 77º40' |
| Extremo oriental | Punta de Maisí | Guantánamo | 20º13' | 74º08' |
| Extremo occidental | Cabo de San Antonio | Pinar del Río | 21º52' | 84º57' |
| Extremo septentrional | Punta Hicacos | Matanzas | 23º11' | 81º09' |
| Extremo septentrional | Punta de Tirry | - | 21º57' | 82º58' |
| Extremo meridional | Caleta de Agustín Jol | - | 21º26' | 82º54' |
| Extremo oriental | Punta del Este | - | 21º34' | 82º33' |
| Extremo occidental | Punta Francés | - | 21º38' | 83º11' |
"""

# Convertir el string a DataFrame
df = DataFrameCreator.string_to_dataframe(table_string)

# Mostrar el DataFrame resultante
print(df)
