import pandas as pd
from fireworks.client import Fireworks

client = Fireworks(
    api_key="fw_3Zf7HrTqgxNgJFhWovNoxZcZ",
)

# Supongamos que tienes una lista de datos tabulares
lista_data = [
    {"table_name": "trabajadores_edad", "columns": ["nombre", "edad"], "num_rows": 5},
    {"table_name": "trabajadores_posicion", "columns": ["nombre", "posicion"], "num_rows": 5}
]

# Cargar los DataFrames (simulación)
dataframes = {
    "trabajadores_edad": pd.DataFrame({
        "nombre": ["Alice", "Bob", "Charlie", "David", "Eve"],
        "edad": [28, 34, 22, 45, 30]
    }),
    "trabajadores_posicion": pd.DataFrame({
        "nombre": ["Alice", "Bob", "Charlie", "David", "Eve"],
        "posicion": ["Técnico", "Gestor", "Técnico", "Analista", "Técnico"]
    })
}

# Convertir la lista a una representación de cadena
lista_data_str = "\n".join([f"Tabla: {data['table_name']}, Columnas: {data['columns']}, Filas: {data['num_rows']}" for data in lista_data])

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
            "¿Qué tablas debo mezclar para responder a la pregunta: "
            "'¿Cuántos trabajadores son técnicos mayores de 30 años?' "
            "Por favor, devuelve solo los nombres de las tablas necesarias."
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
    response = chat_completion.choices[0].message.content
    print("Respuesta del LLM:", response)

    # Supongamos que el modelo devuelve algo como: 'trabajadores_edad, trabajadores_posicion'
    tables_to_merge = response.split(", ")  # Dividir la respuesta en una lista

    # Verificar que las tablas existen en el diccionario
    dfs_to_merge = [dataframes[table] for table in tables_to_merge if table in dataframes]

    # Fusionar las tablas en base a la columna 'nombre'
    if len(dfs_to_merge) > 1:
        merged_df = dfs_to_merge[0]
        for df in dfs_to_merge[1:]:
            merged_df = pd.merge(merged_df, df, on='nombre', how='inner')  # Puedes cambiar 'inner' a 'outer' según sea necesario

        # Mostrar el resultado de la fusión
        print("\nDatos fusionados:")
        print(merged_df)
    else:
        print("No hay suficientes tablas para fusionar.")

except Exception as e:
    print(f"Ocurrió un error: {str(e)}")