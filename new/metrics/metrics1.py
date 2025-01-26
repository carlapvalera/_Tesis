import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar los resultados desde el archivo JSON
with open('evaluation_results.json', 'r', encoding='utf-8') as result_file:
    results = json.load(result_file)

# Convertir los resultados a un DataFrame de pandas
df = pd.DataFrame(results)

# Extraer las métricas ROUGE en un DataFrame separado
rouge_df = pd.json_normalize(df['ROUGE Score'])

# Calcular promedios para BLEU y las métricas ROUGE
average_bleu = df['BLEU Score'].mean()
average_rouge = rouge_df.mean()

# Mostrar los resultados promedio
print("Promedio de BLEU Score:", average_bleu)
print("\nPromedios de ROUGE:")
print(average_rouge)

# Guardar los promedios en un archivo JSON
averages = {
    "BLEU Score": average_bleu,
    "ROUGE Scores": average_rouge.to_dict()
}

with open('average_scores.json', 'w', encoding='utf-8') as avg_file:
    json.dump(averages, avg_file, indent=4, ensure_ascii=False)

print("\nPromedios guardados en 'average_scores.json'.")

# Graficar las puntuaciones BLEU y ROUGE
plt.figure(figsize=(12, 6))

# Gráfico de BLEU Score
plt.subplot(1, 2, 1)
sns.boxplot(data=df['BLEU Score'])
plt.title('Distribución de BLEU Score')
plt.ylabel('BLEU Score')

# Gráfico de ROUGE Scores
plt.subplot(1, 2, 2)
sns.boxplot(data=rouge_df[['rouge-1.f', 'rouge-2.f', 'rouge-l.f']])
plt.title('Distribución de ROUGE Scores (F1)')
plt.ylabel('F1 Score')
plt.xticks(ticks=[0, 1, 2], labels=['ROUGE-1', 'ROUGE-2', 'ROUGE-L'])

plt.tight_layout()
plt.show()
