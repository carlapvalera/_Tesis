from fireworks.client import Fireworks

client = Fireworks(
    api_key="fw_3Zf7HrTqgxNgJFhWovNoxZcZ",
)

# Nueva gramática para manejar diagnósticos
diagnosis_grammar = """
root      ::= action
action    ::= query | merge | single
query     ::= "cuántos trabajadores son técnicos mayores de 30 años"
merge     ::= "merge" | "combine"
single    ::= "single"
"""

# Supongamos que tienes una lista de datos tabulares
lista_data = [
    {"table_name": "trabajadores_edad", "columns": ["nombre", "edad"], "num_rows": 5},
    {"table_name": "trabajadores_posicion", "columns": ["nombre", "posicion"], "num_rows": 5}
]

# Convertir la lista a una representación de cadena
lista_data_str = "\n".join([f"Tabla: {data['table_name']}, Columnas: {data['columns']}, Filas: {data['num_rows']}" for data in lista_data])

messages = [
    {
        "role": "system",
        "content": (
            f"Eres un LLM de ayuda para responder preguntas sobre datos tabulares. "
            f"Tienes esta lista de datos tabulares:\n{lista_data_str}\n"
            f"Debes responder: 'merge' si necesitas datos presentes en más de una tabla para responder "
            f"y 'single' en el caso que respondas solo con la información de una tabla. "
            f"Asegúrate de incluir los nombres de las tablas relevantes en tu respuesta."
        )
    },
    {
        "role": "user",
        "content": "¿Cuántos trabajadores son técnicos mayores de 30 años? Por favor, incluye los nombres de las tablas utilizadas."
    },
]


# Crear una solicitud de completación
try:
    chat_completion = client.chat.completions.create(
        model="accounts/fireworks/models/llama-v3p1-405b-instruct",
        response_format={"type": "grammar", "grammar": diagnosis_grammar},
        messages=messages,
    )

    # Imprimir la respuesta
    print(chat_completion.choices[0].message.content)

except Exception as e:
    print(f"Ocurrió un error: {str(e)}")