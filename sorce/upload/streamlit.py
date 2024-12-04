import streamlit as st
from .upload_file import process_uploaded_file, list_uploaded_files, delete_file, delete_all_files

# Interfaz de usuario con Streamlit
st.title("Gestor de Archivos")

# Subida de archivos
uploaded_file = st.file_uploader("Sube un archivo (CSV, Excel o PDF)", type=['csv', 'xlsx', 'xls', 'pdf'])

if uploaded_file is not None:
    result = process_uploaded_file(uploaded_file)
    st.success(f"Archivo procesado: {result['type']} con ID: {result['file_id']}")

# Listar archivos existentes
if st.button("Listar Archivos Subidos"):
    existing_files = list_uploaded_files()
    st.write("Archivos existentes:", existing_files)

# Borrar un archivo específico
file_to_delete = st.selectbox("Selecciona un archivo para borrar", options=list_uploaded_files())
if st.button("Borrar Archivo"):
    delete_message = delete_file(file_to_delete)
    st.success(delete_message)

# Borrar todos los archivos
if st.button("Borrar Todos los Archivos"):
    delete_message_all = delete_all_files()
    st.success(delete_message_all)