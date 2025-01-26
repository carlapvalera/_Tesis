# Importar la clase TokenSimilarity
from Token_Similarity import TokenSimilarity  # Asegúrate de que la clase esté en un archivo llamado metrics.py

# Crear una instancia de TokenSimilarity
similarity_calculator = TokenSimilarity()

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
meteor_score_value = similarity_calculator.compute_meteor(reference_text, candidate_text)
print(f"METEOR Score: {meteor_score_value}")

# Calcular BERTScore
bertscore_value = similarity_calculator.compute_bertscore(reference_text, candidate_text)
print(f"BERTScore: {bertscore_value}")
