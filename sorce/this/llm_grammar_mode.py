from fireworks.client import Fireworks

client = Fireworks(
    api_key="fw_3Zf7HrTqgxNgJFhWovNoxZcZ",
)

# Nueva gramática para manejar diagnósticos
diagnosis_grammar = """
root      ::= action
action    ::= diagnosis ("," diagnosis)*
diagnosis ::= "merge" | "query" 
"""
list_data = []
# Mensajes para la API
messages = [
    {
        "role": "system",
        "content": "Dada una lista de síntomas, intenta adivinar los posibles diagnósticos. Posibles opciones: arthritis, dengue, urinary tract infection, impetigo, cervical spondylosis. Responde con uno o más diagnósticos separados por comas.",
    },
    {
        "role": "user",
        "content": "He estado teniendo problemas con mis músculos y articulaciones. Mi cuello está muy tenso y mis músculos se sienten débiles.",
    },
]

# Crear una solicitud de completación
chat_completion = client.chat.completions.create(
    model="accounts/fireworks/models/llama-v3p1-405b-instruct",
    response_format={"type": "grammar", "grammar": diagnosis_grammar},
    messages=messages,
)

# Imprimir la respuesta
print(chat_completion.choices[0].message.content)