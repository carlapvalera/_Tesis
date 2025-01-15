import numpy as np


def compute_qa_metrics(correct_answers, predicted_answers):
    """Calcula métricas para preguntas y respuestas."""
    saCC = np.mean(np.array(correct_answers) == np.array(predicted_answers))
    laCC = np.mean(np.array(correct_answers) <= 5)  # Suponiendo que hay un rango hasta 5
    mrr = np.mean(1 / (np.array(predicted_answers) + 1e-10))  # Evitar división por cero

    return {
        'SaCC': saCC,
        'LaCC': laCC,
        'MRR': mrr
    }

def compute_qa_metrics(correct_answers, predicted_answers):
    """Calcula métricas para preguntas y respuestas."""
    saCC = np.mean(np.array(correct_answers) == np.array(predicted_answers))
    laCC = np.mean(np.array(correct_answers) <= 5)  # Suponiendo que hay un rango hasta 5
    mrr = np.mean(1 / (np.array(predicted_answers) + 1e-10))  # Evitar división por cero

    return {
        'SaCC': saCC,
        'LaCC': laCC,
        'MRR': mrr
    }



"""
# Datos de ejemplo
y_true_mc = [0, 1, 2, 0, 1]
y_pred_mc = [0, 2, 1, 0, 0]

# Calcular métricas de clasificación múltiple
mc_metrics = compute_mc_metrics(y_true_mc, y_pred_mc)
print("Métricas de Clasificación Múltiple:", mc_metrics)

# Ejemplo para Perplexity
probabilities = [0.9, 0.8, 0.7]
print("Perplexity:", perplexity(probabilities))

# Ejemplo para BLEU
reference_sentence = "la capital de Francia es París".split()
candidate_sentence = "la capital es París".split()
print("BLEU Score:", compute_bleu(reference_sentence, candidate_sentence))

# Ejemplo para ROUGE
reference_text = "la capital es París"
candidate_text = "París es la capital"
print("ROUGE Score:", compute_rouge(reference_text, candidate_text))

# Ejemplo para QA metrics
correct_answers = [1, 0, 1]
predicted_answers = [1, 0, 0]
qa_metrics = compute_qa_metrics(correct_answers, predicted_answers)
print("Métricas de Preguntas y Respuestas:", qa_metrics)
"""