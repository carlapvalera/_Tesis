import os
import streamlit as st
from dotenv import load_dotenv

st.title("Hi I am CLAUSS")


# Crear un directorio temporal si no existe
temp_dir = "temporal"
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)
load_dotenv()  # Cargar las variables de entorno desde el archivo .env
dir_temporal = os.getenv("PDF_ANUARIOS")


# Mostrar archivos en el directorio temporal
st.subheader("Archivos en el directorio temporal:")
files_in_temp = os.listdir(temp_dir)

if files_in_temp:
    # Crear una lista de direcciones completas de los archivos
    file_paths = [os.path.join(temp_dir, file) for file in files_in_temp]
    
    # Mostrar las rutas completas en un cuadro de texto
    st.write("Rutas completas de los archivos:")
    for path in file_paths:
        st.write(path)
else:
    st.info("No hay archivos en el directorio temporal.")

files_full_paths = []
if files_in_temp :
    # Crear una lista de direcciones completas de los archivos
    for dir in file_paths:
        temp_index = dir.find("temporal")
        temp_index += len("temporal")
        files_full_paths.append(dir_temporal+dir[temp_index:])
        st.write(dir_temporal+dir[temp_index:])

