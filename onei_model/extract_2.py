import PyPDF2
import pandas as pd

# Ruta del archivo PDF
pdf_path = "C:\\blabla\\_Tesis\\01-territorio.pdf"

# Leer el PDF
with open(pdf_path, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    texto = ""
    
    for page in reader.pages:
        texto += page.extract_text() + "\n"

# Procesar el texto para extraer tablas (esto puede requerir ajuste según el formato del texto)
lineas = texto.splitlines()
datos = []

for linea in lineas:
    # Suponiendo que las columnas están separadas por espacios o tabulaciones
    columnas = linea.split()  # Ajusta esto según sea necesario
    if len(columnas) > 1:  # Filtra líneas vacías o irrelevantes
        datos.append(columnas)

# Crear un DataFrame de pandas
df = pd.DataFrame(datos)

# Guardar el DataFrame en un archivo CSV
df.to_csv('datos_extraidos.csv', index=False)

print("Texto extraído y guardado como archivo CSV.")
