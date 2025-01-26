import openai

# Configurar tu clave API
openai.api_key = 'AIzaSyB1Jzqer_Ldwrn94YmxbKboyRk5f0UCtws'

# Datos de ejemplo
y_true = [
    "El gato está en el tejado.",
    "Hoy es un día soleado.",
    "El coche rojo está estacionado frente a la casa."
]

y_pred = [
    "El gato está sobre el tejado.",
    "Hoy es un día lluvioso.",
    "El coche azul está estacionado frente a la casa."
]

# Función para evaluar similitud semántica usando Gemini
def evaluate_with_gemini(y_true, y_pred):
    results = []
    
    for true, pred in zip(y_true, y_pred):
        prompt = f"Evalúa qué tan similar es esta respuesta generada respecto a la esperada en una escala del 0 al 10:\n\nRespuesta esperada: {true}\nRespuesta generada: {pred}\n\nProporciona solo un número del 0 al 10."
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=10,
            temperature=0
        )
        similarity_score = response['choices'][0]['text'].strip()
        results.append({
            "expected": true,
            "generated": pred,
            "similarity_score": similarity_score
        })
    
    return results

# Evaluar las respuestas
results = evaluate_with_gemini(y_true, y_pred)

# Mostrar resultados
for result in results:
    print(f"Esperada: {result['expected']}")
    print(f"Generada: {result['generated']}")
    print(f"Puntuación de Similitud: {result['similarity_score']}")
    print("-" * 50)
