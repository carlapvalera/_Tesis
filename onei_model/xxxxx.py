import pandas as pd

# Ruta del archivo Excel
excel_path = "C:\\blabla\\_Tesis\\01 Territorio.xlsx"  # Cambia esto por la ruta correcta

# Leer todas las hojas del archivo Excel
hojas = pd.read_excel(excel_path, sheet_name=None)  # Lee todas las hojas

# Crear o abrir el archivo de texto para escribir
with open('contenido_anuario.txt', 'w', encoding='utf-8') as f:
    # Iterar sobre cada hoja y extraer datos
    for nombre_hoja, df in hojas.items():
        f.write(f"Datos de la hoja: {nombre_hoja}\n")  # Escribir el nombre de la hoja
        
        # Reemplazar NaN con un valor vacío o una cadena específica
        df.fillna('', inplace=True)  # Reemplaza NaN con una cadena vacía
        
        # Convertir DataFrame a texto y escribirlo
        f.write(df.to_string(index=False))  # Convertir DataFrame a texto sin índices
        f.write("\n\n")  # Añadir dos saltos de línea entre hojas

print("Contenido de todas las hojas guardado en 'contenido_anuario.txt'.")
