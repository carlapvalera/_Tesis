import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

def compute_mc_metrics(y_true, y_pred):
    """Calcula las métricas de clasificación múltiple."""
    accuracy = accuracy_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred, average='macro')
    precision = precision_score(y_true, y_pred, average='macro')
    f1 = f1_score(y_true, y_pred)
    #f1 = f1_score(y_true, y_pred, average='macro')

    return {
        'Accuracy': accuracy,
        'Recall': recall,
        'Precision': precision,
        'F1-score': f1
    }

def compute_micro_macro_f1(y_true, y_pred):
    """Calcula Micro-F1 y Macro-F1."""
    micro_f1 = f1_score(y_true, y_pred, average='micro')
    macro_f1 = f1_score(y_true, y_pred, average='macro')
    return micro_f1, macro_f1

