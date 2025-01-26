import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

with open('evaluation_results2.json', 'r', encoding='utf-8') as result_file:
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
df.mean().plot(kind='bar', color=['skyblue', 'orange', 'lightgreen'])
plt.title('Promedio de Métricas de Evaluación')
plt.ylabel('Valor Promedio')
plt.xticks(rotation=45)
plt.axhline(0, color='black', linewidth=1)
plt.tight_layout()
plt.show()

# Gráfico de dispersión para MRR vs Logical Accuracy
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="Logical Accuracy (LaCC)", y="Mean Reciprocal Rank (MRR)", color='blue', s=100)
plt.title("Relación entre Logical Accuracy y Mean Reciprocal Rank")
plt.xlabel("Logical Accuracy")
plt.ylabel("Mean Reciprocal Rank")
plt.axhline(0, color='black', linewidth=1)
plt.axvline(0, color='black', linewidth=1)
plt.grid(True)
plt.tight_layout()
plt.show()
