import pandas as pd
import json
import re
import sys
from io import StringIO

def preprocess_code(code, local_path):
    # Aquí puedes agregar cualquier lógica de preprocesamiento que necesites
    return code

def run_code(code, local_path):
    try:
        # Preprocesar el código
        code = preprocess_code(code, local_path)
        
        # Capturar salida estándar
        sys.stdout = StringIO()
        exec(code)
        output_str = sys.stdout.getvalue().rstrip('\n')
        sys.stdout.close()
        sys.stdout = sys.__stdout__  # Restaurar stdout
        
        return output_str
    except Exception as e:
        sys.stdout = sys.__stdout__  # Restaurar stdout en caso de error
        return f'Error occurred while running code: {str(e)}'

def execute_action(action_json):
    action = json.loads(action_json)

    if action['action'] == 'query':
        files = action['files']
        
        # Cargar los archivos CSV en DataFrames
        dfs = [pd.read_csv(file) for file in files]
        
        if action['is_merge']:
            # Si is_merge es True, fusionar los DataFrames
            merged_df = pd.concat(dfs, ignore_index=True)
            print("Merged DataFrame:")
            print(merged_df)
            
            # Aquí puedes agregar lógica para realizar una consulta sobre el DataFrame fusionado
            query_code = f"""
filtered_people = merged_df[merged_df['age'] > 30]  # Ejemplo de consulta
print(filtered_people)
"""
            result = run_code(query_code, files)
            return result
        
        else:
            # Si no hay fusión, simplemente ejecuta la consulta sobre el primer DataFrame
            first_df = dfs[0]
            query_code = f"""
filtered_people = first_df[first_df['age'] > 30]  # Ejemplo de consulta
print(filtered_people)
"""
            result = run_code(query_code, [files[0]])
            return result

# Ejemplo de uso
if __name__ == "__main__":
    action_json = '''
    {
      "action": "query",
      "files": ["data1.csv", "data2.csv"],
      "query": "Devuelve todas las personas mayores de 30 años",
      "is_merge": true
    }
    '''
    
    # Ejecutar la acción a partir del JSON
    result = execute_action(action_json)
    
    # Imprimir el resultado
    print("Resultado:", result)