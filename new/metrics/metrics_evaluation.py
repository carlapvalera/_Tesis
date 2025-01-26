import json
from TokenSimilarity   import TokenSimilarity
# Cargar datos desde archivos JSON
with open('interactions.json', 'r', encoding='utf-8') as gen_file:
    generated_data = json.load(gen_file)

with open('expected_responses.json', 'r', encoding='utf-8') as ref_file:
    reference_data = json.load(ref_file)

# Evaluar métricas para cada par de referencia y candidata
results = []

for gen_item, ref_item in zip(generated_data, reference_data):
    reference = ref_item['response']
    candidate = gen_item['response']

    bleu_score = compute_bleu(reference.split(), candidate.split())
    rouge_score = compute_rouge(ref_item['response'], gen_item['response'])
    meteor_score_value = compute_meteor(ref_item['response'], gen_item['response'])
    
    # BERTScore
    bertscore_value = compute_bertscore(ref_item['response'], gen_item['response'])

    results.append({
        "reference": ref_item['response'],
        "candidate": gen_item['response'],
        "BLEU": bleu_score,
        "ROUGE": rouge_score,
        "METEOR": meteor_score_value,
        "BERTScore": bertscore_value
    })

# Guardar resultados en un archivo JSON
with open('evaluation_results.json', 'w', encoding='utf-8') as result_file:
    json.dump(results, result_file, indent=4, ensure_ascii=False)

print("Evaluación completada. Los resultados se han guardado en 'evaluation_results.json'.")
