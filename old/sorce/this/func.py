import pandas as pd

def load_files(file_paths):
    """Carga múltiples archivos y devuelve un diccionario de DataFrames."""
    dataframes = {}
    for file_path in file_paths:
        if file_path.endswith('.csv'):
            dataframes[file_path] = pd.read_csv(file_path)
        elif file_path.endswith(('.xlsx', '.xls')):
            dataframes[file_path] = pd.read_excel(file_path)
    return dataframes

def clean_data(df):
    """Limpia el DataFrame eliminando duplicados y manejando valores nulos."""
    df = df.drop_duplicates()
    df = df.fillna(method='ffill')  # Ejemplo: llenar valores nulos hacia adelante
    return df

def summarize_data(df):
    """Devuelve estadísticas descriptivas del DataFrame."""
    return df.describe()

def filter_data(df, condition):
    """Filtra el DataFrame según una condición dada."""
    return df.query(condition)

def merge_dataframes(df1, df2, on_column):
    """Fusiona dos DataFrames en base a una columna común."""
    return pd.merge(df1, df2, on=on_column)

def generate_report(df):
    """Genera un informe simple basado en el DataFrame."""
    summary = summarize_data(df)
    return summary.to_string()

def list_data(dataframes):
    """Devuelve una lista con la información contenida en cada DataFrame."""
    data_info = []
    for name, df in dataframes.items():
        info = {
            "table_name": name,
            "columns": df.columns.tolist(),
            "num_rows": len(df),
            "data_preview": df.head().to_dict(orient='records')  # Muestra las primeras filas como diccionario
        }
        data_info.append(info)
    return data_info










# Simulación del uso del código

# 1. Cargar los archivos
file_paths = ['C:\\blabla\\_Tesis\\sorce\\this\\trabajadores_edad.csv', 'C:\\blabla\\_Tesis\\sorce\\this\\trabajadores_posicion.csv']
dataframes = load_files(file_paths)

# 2. Limpiar los datos
for key in dataframes:
    dataframes[key] = clean_data(dataframes[key])




# 3. Listar la información de los DataFrames
data_summary = list_data(dataframes)

# Imprimir la información de las tablas
for table_info in data_summary:
    print(f"Tabla: {table_info['table_name']}")
    print(f"Columnas: {table_info['columns']}")
    print(f"Número de filas: {table_info['num_rows']}")
    print("Vista previa de datos:")
    print(table_info['data_preview'])
    print("\n" + "="*40 + "\n")


    
# 3. Resumir los datos de trabajadores por edad
print("Resumen de trabajadores por edad:")
#print(generate_report(dataframes['trabajadores_edad.csv']))

# 4. Filtrar trabajadores mayores de 30 años
filtered_workers = filter_data(dataframes['C:\\blabla\\_Tesis\\sorce\\this\\trabajadores_edad.csv'], 'edad > 30')
print("\nTrabajadores mayores de 30 años:")
print(filtered_workers)

# 5. Fusionar los DataFrames en base al nombre
merged_df = merge_dataframes(dataframes['C:\\blabla\\_Tesis\\sorce\\this\\trabajadores_edad.csv'], dataframes['C:\\blabla\\_Tesis\\sorce\\this\\trabajadores_posicion.csv'], on_column='nombre')
print("\nDatos fusionados:")
print(merged_df)

print( generate_report(dataframes['C:\\blabla\\_Tesis\\sorce\\this\\trabajadores_edad.csv']))

# 6. Simulación de consulta a un modelo LLM (sin implementación real)
def query_llm(question, data_context):
    """Simula el envío de una pregunta al LLM junto con el contexto de los datos."""
    # Aquí iría la lógica para interactuar con el modelo LLM.
    print(f"Pregunta enviada al LLM: {question}")
    print(f"Contexto de datos: {data_context}")

# Ejemplo de pregunta sobre los datos fusionados
query_llm("¿Cuántos trabajadores son técnicos mayores de 30 años?", merged_df)