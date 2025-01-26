import numpy as np
from nltk.translate.bleu_score import sentence_bleu
from rouge import Rouge
from nltk.translate.meteor_score import meteor_score
from bert_score import score
import json



import numpy as np
from nltk.translate.bleu_score import sentence_bleu
from rouge import Rouge
from nltk.translate.meteor_score import meteor_score
from bert_score import score
from nltk.tokenize import word_tokenize
from nltk.translate.meteor_score import meteor_score
"""import nltk
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('punkt')  # Para tokenización
nltk.download('omw-1.4')  # Para soporte multilingüe en WordNet"""


class TokenSimilarity:
    def __init__(self):
        pass

    def compute_bleu(self, reference, candidate):
        """Calcula la puntuación BLEU."""
        return sentence_bleu([reference], candidate)

    def perplexity(self, probabilities):
        """Calcula la perplexity dada una lista de probabilidades."""
        return np.exp(-np.mean(np.log(probabilities)))

    def compute_rouge(self, reference, candidate):
        """Calcula las puntuaciones ROUGE."""
        rouge = Rouge()
        scores = rouge.get_scores(candidate, reference)
        return scores[0]  # Devuelve la puntuación para el primer conjunto

    def compute_meteor(self, reference, candidate):
        """Calcula la puntuación METEOR."""
        # Tokenizar referencia y candidato
        reference_tokens = word_tokenize(reference)
        candidate_tokens = word_tokenize(candidate)
        
        # Calcular la puntuación METEOR
        return meteor_score([reference_tokens], candidate_tokens)

    def compute_bertscore(self, reference, candidate):
        """Calcula la puntuación BertScore."""
        P, R, F1 = score([candidate], [reference], lang="en", verbose=True)
        return F1.mean().item()  # Devuelve el F1 promedio


# Ejemplo de uso
if __name__ == "__main__":
    # Instanciar la clase




    # Crear una instancia de TokenSimilarity
    token_similarity = TokenSimilarity()

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
        bleu_score = token_similarity.compute_bleu(reference.split(), candidate.split())
        rouge_score = token_similarity.compute_rouge(reference, candidate)
        # Calcular la puntuación METEOR
        #meteor_score = token_similarity.compute_meteor(reference, candidate)
        # Para calcular la perplexity, necesitas una lista de probabilidades (ejemplo ficticio)
        #probabilities = [0.9, 0.8, 0.7]  # Ejemplo de probabilidades
        #perplexity_score = token_similarity.perplexity(probabilities)

        #bert_score = token_similarity.compute_bertscore(reference, candidate)

        # Imprimir los resultados
        print(f"BLEU Score: {bleu_score}")
        print(f"ROUGE Score: {rouge_score}")
        #print(f"METEOR Score: {meteor_score}")
        #print(f"Perplexity: {perplexity_score}")
        #print(f"BertScore: {bert_score}")


        results.append({
            "BLEU Score": bleu_score,
            "ROUGE Score": rouge_score,
            #"METEOR Score": meteor_score,
            #"Perplexity": {perplexity_score}

        })

    # Guardar resultados en un archivo JSON
    with open('evaluation_results.json', 'w', encoding='utf-8') as result_file:
        json.dump(results, result_file, indent=4, ensure_ascii=False)

    print("Evaluación completada. Los resultados se han guardado en 'evaluation_results.json'.")

