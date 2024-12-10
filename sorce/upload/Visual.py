import streamlit as st
from upload_file import process_uploaded_file, list_uploaded_files, delete_all_files, delete_file

# Interfaz de usuario con Streamlit
st.title("Gestor de Archivos")

# Subida de archivos
uploaded_file = st.file_uploader("Sube un archivo (CSV, Excel o PDF)", type=['csv', 'xlsx', 'xls', 'pdf'])

if uploaded_file is not None:
    try:
        result = process_uploaded_file(uploaded_file)
        st.success(f"Archivo procesado: {result['type']} con ID: {result['file_id']}")
    except Exception as e:
        st.error(f"Error al procesar el archivo: {str(e)}")

# Listar archivos existentes
if st.button("Listar Archivos Subidos"):
    existing_files = list_uploaded_files()
    if existing_files:
        st.write("Archivos existentes:")
        for file in existing_files:
            st.write(file)
    else:
        st.write("No hay archivos subidos.")

# Borrar un archivo específico
existing_files = list_uploaded_files()
if existing_files:
    file_to_delete = st.selectbox("Selecciona un archivo para borrar", options=existing_files)
    if st.button("Borrar Archivo"):
        try:
            delete_message = delete_file(file_to_delete)
            st.success(delete_message)
        except Exception as e:
            st.error(f"Error al borrar el archivo: {str(e)}")
else:
    st.write("No hay archivos para borrar.")

# Borrar todos los archivos
if st.button("Borrar Todos los Archivos"):
    try:
        delete_message_all = delete_all_files()
        st.success(delete_message_all)
    except Exception as e:
        st.error(f"Error al borrar todos los archivos: {str(e)}")