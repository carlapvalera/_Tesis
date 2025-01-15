import numpy as np
from nltk.translate.bleu_score import sentence_bleu
from rouge import Rouge

def compute_bleu(reference, candidate):
    """Calcula la puntuación BLEU."""
    return sentence_bleu([reference], candidate)

def perplexity(probabilities):
    """Calcula la perplexity dada una lista de probabilidades."""
    return np.exp(-np.mean(np.log(probabilities)))


def compute_rouge(reference, candidate):
    """Calcula las puntuaciones ROUGE."""
    rouge = Rouge()
    scores = rouge.get_scores(candidate, reference)
    return scores[0]  # Devuelve la puntuación para el primer conjunto


from nltk.translate.meteor_score import meteor_score

def compute_meteor(reference, candidate):
    """Calcula la puntuación METEOR."""
    return meteor_score([reference], candidate)

from bert_score import score

def compute_bertscore(reference, candidate):
    """Calcula la puntuación BertScore."""
    P, R, F1 = score([candidate], [reference], lang="en", verbose=True)
    return F1.mean().item()  # Devuelve el F1 promedio
