import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar resultados desde el archivo JSON
with open('evaluation_results.json', 'r', encoding='utf-8') as result_file:
    results = json.load(result_file)

# Convertir resultados a DataFrame para análisis y visualización
results_df = pd.DataFrame(results)

# Imprimir el DataFrame para ver los resultados
print("Resultados de la Evaluación:")
print(results_df)

# Análisis básico
print("\nAnálisis Descriptivo:")
print(results_df.describe())

# Visualización de resultados

# Configurar estilo de Seaborn
sns.set(style="whitegrid")



# Gráfico de barras para las métricas (BLEU, ROUGE, METEOR y BERTScore)
metrics_to_plot = ['reference', 'candidate', 'BLEU', 'ROUGE']
plt.figure(figsize=(12, 6))
results_df[metrics_to_plot].plot(kind='bar', figsize=(10, 6))
plt.title('Comparación de Métricas')
plt.ylabel('Puntuación')
plt.xticks(ticks=range(len(results_df)), labels=results_df['reference'], rotation=45)
plt.legend(title='Métricas')
plt.tight_layout()
plt.show()

# Gráfico de dispersión para comparar BLEU vs METEOR
plt.figure(figsize=(10, 6))
sns.scatterplot(data=results_df, x='BLEU', y='ROUGE', hue='reference', style='reference', s=100)
plt.title('Comparación entre BLEU y METEOR')
plt.xlabel('BLEU Score')
plt.ylabel('METEOR Score')
plt.grid(True)
plt.legend(title='Referencia')
plt.show()

# Gráfico de dispersión para comparar BERTScore vs ROUGE
plt.figure(figsize=(10, 6))
sns.scatterplot(data=results_df, x='BLEU', y='ROUGE', hue='reference', style='reference', s=100)
plt.title('Comparación entre BLEU y ROUGE')
plt.xlabel('BLEU')
plt.ylabel('ROUGE Score')
plt.grid(True)
plt.legend(title='Referencia')
plt.show()
