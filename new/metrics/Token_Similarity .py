import numpy as np
from nltk.translate.bleu_score import sentence_bleu
from rouge import Rouge
from nltk.translate.meteor_score import meteor_score
from bert_score import score


class TokenSimilarity:
    def __init__(self):
        pass
    def compute_bleu(self,reference, candidate):
        """Calcula la puntuación BLEU."""
        return sentence_bleu([reference], candidate)

    def perplexity(self,probabilities):
        """Calcula la perplexity dada una lista de probabilidades."""
        return np.exp(-np.mean(np.log(probabilities)))


    def compute_rouge(self,reference, candidate):
        """Calcula las puntuaciones ROUGE."""
        rouge = Rouge()
        scores = rouge.get_scores(candidate, reference)
        return scores[0]  # Devuelve la puntuación para el primer conjunto

    def compute_meteor(self,reference, candidate):
        """Calcula la puntuación METEOR."""
        return meteor_score([reference], candidate)


    def compute_bertscore(self,reference, candidate):
        """Calcula la puntuación BertScore."""
        P, R, F1 = score([candidate], [reference], lang="en", verbose=True)
        return F1.mean().item()  # Devuelve el F1 promedio



# Crear una instancia de TokenSimilarity
similarity_calculator = TokenSimilarity()

with open('interactions.json', 'r', encoding='utf-8') as gen_file:
    generated_data = json.load(gen_file)

with open('expected_responses.json', 'r', encoding='utf-8') as ref_file:
    reference_data = json.load(ref_file)

# Evaluar métricas para cada par de referencia y candidata
results = []

for gen_item, ref_item in zip(generated_data, reference_data):
    reference = ref_item['response']
    candidate = gen_item['response']
    
# Datos de ejemplo
reference_text = "Cuba es un país insular en el Caribe."
candidate_text = "Cuba es un país en el Caribe."

# Tokenizar las oraciones (dividir en palabras)
reference_tokens = reference_text.split()
candidate_tokens = candidate_text.split()

# Calcular BLEU
bleu_score = similarity_calculator.compute_bleu(reference_tokens, candidate_tokens)
print(f"BLEU Score: {bleu_score}")

# Calcular ROUGE
rouge_score = similarity_calculator.compute_rouge(reference_text, candidate_text)
print(f"ROUGE Score: {rouge_score}")

# Calcular METEOR
meteor_score_value = similarity_calculator.compute_meteor(reference_tokens, candidate_tokens)
print(f"METEOR Score: {meteor_score_value}")

# Calcular BERTScore
#bertscore_value = similarity_calculator.compute_bertscore(reference_text, candidate_text)
#print(f"BERTScore: {bertscore_value}")
