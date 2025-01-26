import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar datos desde el JSON proporcionado

with open('evaluation_results3.json', 'r', encoding='utf-8') as result_file:
    data = json.load(result_file)
# Convertir los datos a un DataFrame de pandas
df = pd.DataFrame(data)

# Análisis descriptivo
print("Análisis Descriptivo:")
print(df.describe())

# Configurar estilo de Seaborn
sns.set(style="whitegrid")

# Gráfico de barras para las métricas
plt.figure(figsize=(12, 6))
metrics_means = df[['F1-score', 'Micro-F1', 'Macro-F1']].mean()
metrics_means.plot(kind='bar', color=['skyblue', 'orange', 'lightgreen'])
plt.title('Promedio de Métricas de Evaluación')
plt.ylabel('Valor Promedio')
plt.xticks(rotation=45)
plt.axhline(0, color='black', linewidth=1)
plt.tight_layout()
plt.show()

# Gráfico de dispersión para F1-score vs Micro-F1
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="Micro-F1", y="F1-score", color='blue', s=100)
plt.title("Relación entre Micro-F1 y F1-score")
plt.xlabel("Micro-F1")
plt.ylabel("F1-score")
plt.axhline(0, color='black', linewidth=1)
plt.axvline(0, color='black', linewidth=1)
plt.grid(True)
plt.tight_layout()
plt.show()
