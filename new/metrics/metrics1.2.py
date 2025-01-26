import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar resultados desde el archivo JSON
with open('evaluation_results.json', 'r', encoding='utf-8') as result_file:
    results = json.load(result_file)

# Convertir resultados a DataFrame para análisis y visualización
data = []
for idx, item in enumerate(results):
    data.append({
        "Index": idx,
        "BLEU": item["BLEU Score"],
        "ROUGE-1 (F1)": item["ROUGE Score"]["rouge-1"]["f"],
        "ROUGE-2 (F1)": item["ROUGE Score"]["rouge-2"]["f"],
        "ROUGE-L (F1)": item["ROUGE Score"]["rouge-l"]["f"]
    })

results_df = pd.DataFrame(data)

# Imprimir el DataFrame para ver los resultados
print("Resultados de la Evaluación:")
print(results_df)

# Análisis descriptivo
print("\nAnálisis Descriptivo:")
print(results_df.describe())

# Configurar estilo de Seaborn
sns.set(style="whitegrid")

# Gráfico de barras para BLEU
plt.figure(figsize=(12, 6))
sns.barplot(x="Index", y="BLEU", data=results_df, palette="Blues_d")
plt.title("Puntuación BLEU por Texto")
plt.xlabel("Índice del Texto")
plt.ylabel("Puntuación BLEU")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Gráfico comparativo de ROUGE (F1 Scores)
results_df[["ROUGE-1 (F1)", "ROUGE-2 (F1)", "ROUGE-L (F1)"]].plot(
    kind='bar', figsize=(12, 6), color=["skyblue", "orange", "green"]
)
plt.title("Comparación de Métricas ROUGE")
plt.ylabel("Puntuación F1")
plt.xlabel("Índice del Texto")
plt.xticks(ticks=range(len(results_df)), labels=results_df["Index"], rotation=45)
plt.legend(title="Métricas ROUGE")
plt.tight_layout()
plt.show()

# Gráfico de dispersión: BLEU vs ROUGE-L
plt.figure(figsize=(10, 6))
sns.scatterplot(data=results_df, x="BLEU", y="ROUGE-L (F1)", s=100)
plt.title("Relación entre BLEU y ROUGE-L")
plt.xlabel("Puntuación BLEU")
plt.ylabel("Puntuación ROUGE-L (F1)")
plt.grid(True)
plt.tight_layout()
plt.show()
