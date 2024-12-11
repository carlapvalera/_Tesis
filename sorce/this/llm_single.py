import pandas as pd
import pandasql as psql
from fireworks.client import Fireworks

client = Fireworks(
    api_key="fw_3Zf7HrTqgxNgJFhWovNoxZcZ",
)

# Simulación de los DataFrames
data_edades = {
    "nombre": ["Alice", "Bob", "Charlie", "David", "Eve"],
    "edad": [28, 34, 22, 45, 30]
}

data_posiciones = {
    "nombre": ["Alice", "Bob", "Charlie", "David", "Eve"],
    "posicion": ["Técnico", "Gestor", "Técnico", "Analista", "Técnico"]
}

# Crear DataFrames
df_edades = pd.DataFrame(data_edades)
df_posiciones = pd.DataFrame(data_posiciones)

# Almacenar los DataFrames en un diccionario para fácil acceso
dataframes = {
    'trabajadores_edad': df_edades,
    'trabajadores_posicion': df_posiciones
}

# Convertir la lista a una representación de cadena
lista_data_str = "\n".join([f"Tabla: {name}, Columnas: {df.columns.tolist()}, Filas: {len(df)}" for name, df in dataframes.items()])

# Mensajes para el modelo LLM
messages = [
    {
        "role": "system",
        "content": (
            "Eres un LLM de ayuda para responder preguntas sobre datos tabulares. "
            f"Tienes esta lista de datos tabulares:\n{lista_data_str}\n"
        )
    },
    {
        "role": "user",
        "content": (
            "¿Cuántos trabajadores son mayores de 30 años? y dime quién es el presidente de España. "
            "Por favor, devuelve solo los nombres de las tablas necesarias y el código SQL."
        )
    },
]

# Crear una solicitud de completación
try:
    chat_completion = client.chat.completions.create(
        model="accounts/fireworks/models/llama-v3p1-405b-instruct",
        messages=messages,
    )

    # Obtener la respuesta del modelo
    response = chat_completion.choices[0].message.content.strip()
    print("Respuesta del LLM:", response)

    # Si el LLM devuelve una consulta SQL:
    if response.startswith("SELECT"):
        # Modificar la consulta para usar los nombres de los DataFrames
        sql_query = response.replace("trabajadores_edad", "df_edades").replace("trabajadores_posicion", "df_posiciones")
        
        # Ejecutar la consulta usando pandasql
        result = psql.sqldf(sql_query)
        
        # Mostrar el resultado
        print("\nResultado de la consulta:")
        print(result)
    
except Exception as e:
    print(f"Ocurrió un error: {str(e)}")
