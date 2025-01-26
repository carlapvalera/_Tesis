import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

# Cargar datos desde el archivo JSON proporcionado
with open('evaluation_results4.json', 'r', encoding='utf-8') as result_file:
    data = json.load(result_file)

# Convertir los datos a un DataFrame de pandas
df = pd.DataFrame(data)

# Verificar las columnas disponibles
print("Columnas disponibles en el DataFrame:")
print(df.columns)

# Agregar una columna con la proporción entre las longitudes (len candidate / len refence)
df['length_ratio'] = df['len candidate'] / df['len refence']

# Análisis descriptivo
print("\nAnálisis Descriptivo:")
print(df.describe())

# Configurar estilo de Seaborn
sns.set(style="whitegrid")

# Gráfico de barras para la puntuación semántica
plt.figure(figsize=(12, 6))
sns.barplot(x=df.index, y='semantic', data=df, palette='Blues_d')  # Agregar data=df
plt.title('Puntuación Semántica por Ejemplo')
plt.ylabel('Puntuación Semántica')
plt.xlabel('Índice del Ejemplo')
plt.axhline(0, color='black', linewidth=1)
plt.tight_layout()
plt.show()

# Gráfico de dispersión para longitud de referencia vs longitud del candidato
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="len refence", y="len candidate", hue="semantic", size="semantic", sizes=(50, 300), palette='viridis', legend=False)
plt.title("Longitud de Referencia vs Longitud del Candidato")
plt.xlabel("Longitud de Referencia")
plt.ylabel("Longitud del Candidato")
plt.axhline(0, color='black', linewidth=1)
plt.axvline(0, color='black', linewidth=1)
plt.grid(True)
plt.tight_layout()
plt.show()

# Gráfico de dispersión para relación entre longitudes y puntuación semántica
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="length_ratio", y="semantic", hue="semantic", size="semantic", sizes=(50, 300), palette='coolwarm', legend=False)
plt.title("Relación entre Proporción de Longitudes y Puntuación Semántica")
plt.xlabel("Proporción (len candidate / len refence)")
plt.ylabel("Puntuación Semántica")
plt.axhline(0, color='black', linewidth=1)
plt.axvline(1, color='red', linestyle='--', linewidth=1, label="Proporción = 1")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Calcular correlaciones entre las métricas
correlation_matrix = df[['semantic', 'len refence', 'len candidate', 'length_ratio']].corr()
print("\nMatriz de Correlación:")
print(correlation_matrix)

# Heatmap para visualizar las correlaciones
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Matriz de Correlación entre Métricas")
plt.tight_layout()
plt.show()
