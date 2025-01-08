import os
import streamlit as st

# Crear un directorio temporal si no existe
temp_dir = "temporal"
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

# Función para guardar el archivo en el directorio temporal
def save_file(uploaded_file):
    with open(os.path.join(temp_dir, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())

# Función para eliminar un archivo del directorio temporal
def delete_file(file_name):
    file_path = os.path.join(temp_dir, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False

# Título de la aplicación
st.title("Gestor de Archivos Temporales")

# Cargar archivos
uploaded_files = st.file_uploader("Elige tus archivos", accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        # Guardar cada archivo en el directorio temporal
        save_file(uploaded_file)
        st.success(f"Archivo {uploaded_file.name} guardado.")

# Mostrar archivos en el directorio temporal
st.subheader("Archivos en el directorio temporal:")
files_in_temp = os.listdir(temp_dir)
if files_in_temp:
    selected_file = st.selectbox("Selecciona un archivo para eliminar:", files_in_temp)

    if st.button("Eliminar archivo"):
        if delete_file(selected_file):
            st.success(f"Archivo {selected_file} eliminado.")
            # Actualizar la lista de archivos después de eliminar
            files_in_temp.remove(selected_file)  # Remover el archivo eliminado de la lista
        else:
            st.error(f"No se pudo eliminar el archivo {selected_file}.")
else:
    st.info("No hay archivos en el directorio temporal.")
