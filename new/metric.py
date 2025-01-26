import json
from gemini_api import Gemini_API

gem = Gemini_API()

with open('interactions.json', 'r', encoding='utf-8') as gen_file:
    generated_data = json.load(gen_file)

with open('expected_responses.json', 'r', encoding='utf-8') as ref_file:
    reference_data = json.load(ref_file)

# Evaluar métricas para cada par de referencia y candidata
results = []

for gen_item, ref_item in zip(generated_data, reference_data):
    reference = ref_item['response']
    candidate = gen_item['response']

        
        
    # Calcular las métricas
    semantic = gem.evaluate_response(reference,candidate)

    results.append({
        "semantic": semantic,
        "len refence": len(reference),
        "len candidate": len(candidate)
        
        })

    # Guardar resultados en un archivo JSON
with open('evaluation_results4.json', 'w', encoding='utf-8') as result_file:
    json.dump(results, result_file, indent=4, ensure_ascii=False)

print("Evaluación completada. Los resultados se han guardado en 'evaluation_results.json'.")

