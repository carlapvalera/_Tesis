from pymongo import MongoClient
from bson import ObjectId
import pandas as pd
import tkinter as tk
from tkinter import filedialog

# Conexión a la base de datos MongoDB local
client = MongoClient('localhost', 27017)

# Probar la conexión
try:
    client.admin.command('ping')  # Esto envía un comando ping para verificar la conexión
    print("Conexión exitosa a MongoDB")
except Exception as e:
    print("Error al conectar a MongoDB:", e)

# Seleccionar la base de datos 'anuarios_estadisticos'
db = client['anuarios_estadisticos']

# Seleccionar las colecciones
files_collection = db['files']  # Colección para archivos subidos
precomputed_collection = db['precomputed']  # Colección para respuestas precomputadas

# Función para importar datos desde un archivo Excel
def import_excel_to_mongodb(excel_file_path):
    """Importa datos desde un archivo Excel a MongoDB."""
    df = pd.read_excel(excel_file_path, header=0)
    
    data = []
    current_division = None

    for index, row in df.iterrows():
        if pd.isna(row[0]):  # Si la primera columna está vacía, es un producto
            continue
        
        if row[0].strip():  # Si hay texto, es una nueva división
            current_division = row[0].strip()
        
        product_name = row[1].strip()
        unit_measure = row[2].strip()
        
        values = {
            "2019": row[3] if not pd.isna(row[3]) else None,
            "2020": row[4] if not pd.isna(row[4]) else None,
            "2021": row[5] if not pd.isna(row[5]) else None,
            "2022": row[6] if not pd.isna(row[6]) else None,
            "2023": row[7] if not pd.isna(row[7]) else None,
        }

        data.append({
            "division": current_division,
            "producto": {
                "nombre": product_name,
                "unidad_medida": unit_measure,
                "valores": values
            }
        })

    # Agrupar los datos por división
    grouped_data = {}
    for item in data:
        division = item['division']
        product = item['producto']
        
        if division not in grouped_data:
            grouped_data[division] = {"division": division, "productos": []}
        
        grouped_data[division]["productos"].append(product)

    # Imprimir los datos en consola antes de guardarlos
    print("Datos a importar a MongoDB:")
    for division, content in grouped_data.items():
        print(f"\nDivisión: {content['division']}")
        for product in content["productos"]:
            print(f"  Producto: {product['nombre']}, Unidad: {product['unidad_medida']}, Valores: {product['valores']}")

    # Insertar los datos en MongoDB
    db['estadisticas'].insert_many(grouped_data.values())  # Cambia 'estadisticas' por el nombre de tu colección deseada

    print("\nDatos importados correctamente a MongoDB.")

# Función para abrir una ventana de selección de archivos
def open_file_dialog():
    """Abre una ventana para seleccionar un archivo Excel."""
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    file_path = filedialog.askopenfilename(title="Selecciona un archivo Excel", filetypes=[("Excel files", "*.xls;*.xlsx")])
    
    if file_path:  # Si se seleccionó un archivo
        import_excel_to_mongodb(file_path)

# Ejemplo de uso
if __name__ == "__main__":
    
    # Abrir diálogo para seleccionar el archivo Excel y cargarlo en MongoDB
    open_file_dialog()
