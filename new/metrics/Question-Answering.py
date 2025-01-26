from nltk.translate.bleu_score import sentence_bleu
from rouge import Rouge
import numpy as np
import json

def compute_qa_metrics_text(correct_answers, predicted_answers):
    """
    Calcula métricas para preguntas y respuestas basadas en texto.
    """
    rouge = Rouge()

    # Inicializar variables
    exact_matches = []
    logical_matches = []
    reciprocal_ranks = []

    for correct, predicted in zip(correct_answers, predicted_answers):
        # Verificar que ambas respuestas no estén vacías
        if not correct.strip() or not predicted.strip():
            continue  # Omitir si alguna respuesta está vacía

        # SaCC: Comparación exacta
        exact_matches.append(correct.strip().lower() == predicted.strip().lower())

        # LaCC: Usar ROUGE-L F1 como criterio lógico
        rouge_score = rouge.get_scores(predicted, correct)[0]
        logical_matches.append(rouge_score['rouge-l']['f'] > 0.1)  # Umbral lógico

        # MRR: Usar BLEU como aproximación al rango
        bleu_score = sentence_bleu([correct.split()], predicted.split())
        reciprocal_ranks.append(1 / (1 + (1 - bleu_score)))  # BLEU más alto -> mejor rango

    # Calcular promedios, evitando dividir por cero si no hay coincidencias
    saCC = np.mean(exact_matches) if exact_matches else 0.0
    laCC = np.mean(logical_matches) if logical_matches else 0.0
    mrr = np.mean(reciprocal_ranks) if reciprocal_ranks else 0.0

    return {
        'SaCC': saCC,
        'LaCC': laCC,
        'MRR': mrr
    }

# Ejemplo de uso

with open('interactions.json', 'r', encoding='utf-8') as gen_file:
    generated_data = json.load(gen_file)

with open('expected_responses.json', 'r', encoding='utf-8') as ref_file:
    reference_data = json.load(ref_file)

# Evaluar métricas para cada par de referencia y candidata
results = []

for gen_item, ref_item in zip(generated_data, reference_data):
    correct_answers = [ref_item['response']]  # Asegurarse de que sea una lista
    predicted_answers = [gen_item['response']]  # Asegurarse de que sea una lista

    # Calcular métricas
    metrics = compute_qa_metrics_text(correct_answers, predicted_answers)

    # Imprimir resultados
    print("Métricas de Evaluación:")
    print(f"Semantic Accuracy (SaCC): {metrics['SaCC']:.2f}")
    print(f"Logical Accuracy (LaCC): {metrics['LaCC']:.2f}")
    print(f"Mean Reciprocal Rank (MRR): {metrics['MRR']:.2f}")  

    results.append({
        "Semantic Accuracy (SaCC)": metrics['SaCC'],
        "Logical Accuracy (LaCC)": metrics['LaCC'],
        "Mean Reciprocal Rank (MRR)": metrics['MRR']
    })

# Guardar resultados en un archivo JSON
with open('evaluation_results2.json', 'w', encoding='utf-8') as result_file:
    json.dump(results, result_file, indent=4, ensure_ascii=False)

print("Evaluación completada. Los resultados se han guardado en 'evaluation_results2.json'.")
