import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
from sklearn.preprocessing import LabelEncoder
import json

def compute_mc_metrics(y_true, y_pred):
    """Calcula las métricas de clasificación múltiple."""
    accuracy = accuracy_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred, average='macro')
    precision = precision_score(y_true, y_pred, average='macro')
    f1 = f1_score(y_true, y_pred, average='macro')

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

# Ejemplo de uso
if __name__ == "__main__":
        # Ejemplo de uso

    with open('interactions.json', 'r', encoding='utf-8') as gen_file:
        generated_data = json.load(gen_file)

    with open('expected_responses.json', 'r', encoding='utf-8') as ref_file:
        reference_data = json.load(ref_file)

    # Evaluar métricas para cada par de referencia y candidata
    results = []

    for gen_item, ref_item in zip(generated_data, reference_data):
        y_true_text = [ref_item['response']]  # Asegurarse de que sea una lista
        y_pred_text = [gen_item['response']]  # Asegurarse de que sea una lista

        
        # Convertir respuestas de texto a etiquetas numéricas
        label_encoder = LabelEncoder()
        all_texts = list(set(y_true_text + y_pred_text))  # Obtener todas las respuestas únicas
        label_encoder.fit(all_texts)

        # Transformar texto a etiquetas numéricas
        y_true = label_encoder.transform(y_true_text)
        y_pred = label_encoder.transform(y_pred_text)


        # Calcular métricas
        metrics = compute_mc_metrics(y_true, y_pred)
        micro_f1, macro_f1 = compute_micro_macro_f1(y_true, y_pred)

        print(f"F1-score: {metrics['F1-score']:.2f}")
    
        print("\nMicro-F1:", micro_f1)
        print("Macro-F1:", macro_f1) 

        # Mostrar etiquetas para referencia
        print("\nEtiquetas asignadas por LabelEncoder:")
        for text, label in zip(label_encoder.classes_, range(len(label_encoder.classes_))):
            print(f"{label}: {text}")

        # Mostrar etiquetas para referencia
        ref = []
        print("\nEtiquetas asignadas por LabelEncoder:")
        for text, label in zip(label_encoder.classes_, range(len(label_encoder.classes_))):
            
            ref.append(str(label)+":"+ str(text))
            print(f"{label}: {text}")


        results.append({
            "F1-score": metrics['F1-score'],
            "Micro-F1": micro_f1,
            "Macro-F1": macro_f1,
            "Etiquetas asignadas por LabelEncoder": ref

        })

    # Guardar resultados en un archivo JSON
    with open('evaluation_results3.json', 'w', encoding='utf-8') as result_file:
        json.dump(results, result_file, indent=4, ensure_ascii=False)

    print("Evaluación completada. Los resultados se han guardado en 'evaluation_results2.json'.")
