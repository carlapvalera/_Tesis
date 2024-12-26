import pdfplumber
import pandas as pd
import os

# Ruta del archivo PDF
pdf_path = "C:\\blabla\\_Tesis\\03-poblacion-.pdf"

# Crear listas para almacenar el texto y las tablas
texto_completo = []
tablas_completas = []

# Crear un directorio para guardar las imágenes si no existe
if not os.path.exists('imagenes_extraidas'):
    os.makedirs('imagenes_extraidas')

# Abrir el PDF
with pdfplumber.open(pdf_path) as pdf:
    for pagina in pdf.pages:
        # Extraer texto
        texto = pagina.extract_text()
        if texto:
            texto_completo.append(texto)

        # Extraer tablas
        tablas = pagina.extract_tables()
        for i, tabla in enumerate(tablas):
            df = pd.DataFrame(tabla[1:], columns=tabla[0])  # Convertir la tabla a DataFrame
            tablas_completas.append(df)
            df.to_csv(f'tabla_pagina_{pagina.page_number}_tabla_{i + 1}.csv', index=False)

        # Extraer imágenes
        for j, imagen in enumerate(pagina.images):
            # Obtener los datos de la imagen
            imagen_data = imagen['stream'].get_data()
            # Guardar la imagen como un archivo PNG o JPG
            with open(f'imagenes_extraidas/pagina_{pagina.page_number}_imagen_{j + 1}.png', 'wb') as img_file:
                img_file.write(imagen_data)

# Guardar el texto completo en un archivo
with open('texto_extraido.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(texto_completo))

print("Texto, tablas e imágenes extraídos y guardados.")

# Mostrar el contenido del archivo de texto
print("\nContenido del archivo de texto extraído:")
with open('texto_extraido.txt', 'r', encoding='utf-8') as f:
    contenido_texto = f.read()
    #print(contenido_texto)

# Mostrar el contenido de las tablas extraídas
print("\nContenido de las tablas extraídas:")
for i, archivo in enumerate(os.listdir('.'), start=1):
    if archivo.startswith('tabla_pagina_') and archivo.endswith('.csv'):
        df = pd.read_csv(archivo)
        print(f"\nContenido de {archivo}:")
        print(df)
