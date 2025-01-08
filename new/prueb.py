import os
from dotenv import load_dotenv
from data_saver import DataSaver
from pdf_extractor_textocompleto import PDFExtractor_withCid

# Crear un directorio temporal si no existe
temp_dir = "temporal"
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)
load_dotenv()  # Cargar las variables de entorno desde el archivo .env
dir_temporal = os.getenv("PDF_ANUARIOS")
"""extractor = DataSaver()
ex = PDFExtractor_withCid()
"""

# Mostrar archivos en el directorio temporal

files_in_temp = os.listdir(temp_dir)

if files_in_temp:
    # Crear una lista de direcciones completas de los archivos
    file_paths = [os.path.join(temp_dir, file) for file in files_in_temp]
    
#crear la lista de directorios completa
files_full_paths = []
if files_in_temp :
    # Crear una lista de direcciones completas de los archivos
    for dir in file_paths:
        temp_index = dir.find("temporal")
        temp_index += len("temporal")+1
        file_path = os.path.join("C:", "blabla", "_Tesis", "new", "temporal", dir[temp_index:])

        """files_full_paths.append(dir_temporal+dir[temp_index:])
        text= ex.extract_text_and_tables(dir_temporal+dir[temp_index:])
        extractor.save_text(text)"""
        print(file_path)
C:\blabla\_Tesis\new\pylineejemplo.py
