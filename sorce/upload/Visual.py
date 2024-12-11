import streamlit as st
import pandas as pd
import os
import pdfplumber

# Carpeta donde se guardarán los archivos subidos
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Funciones para manejar archivos
def save_uploaded_file(uploaded_file):
    """Guarda el archivo subido en la carpeta especificada."""
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def read_csv(file_path):
    """Lee un archivo CSV y devuelve un DataFrame."""
    return pd.read_csv(file_path)

def read_excel(file_path):
    """Lee un archivo Excel y devuelve un DataFrame."""
    return pd.read_excel(file_path)

def extract_text_from_pdf(file_path):
    """Extrae texto de un archivo PDF y devuelve el texto completo."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def process_uploaded_file(uploaded_file):
    """Procesa el archivo subido según su tipo y guarda en la base de datos."""
    file_path = save_uploaded_file(uploaded_file)

    if uploaded_file.name.endswith('.csv'):
        data = read_csv(file_path)
        return {"type": "csv", "data": data}

    elif uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
        data = read_excel(file_path)
        return {"type": "excel", "data": data}

    elif uploaded_file.name.endswith('.pdf'):
        full_text = extract_text_from_pdf(file_path)
        return {"type": "pdf", "text": full_text}

    else:
        raise ValueError("Unsupported file type.")

def list_uploaded_files():
    """Lista los archivos existentes en la carpeta de uploads."""
    return os.listdir(UPLOAD_FOLDER)

def delete_file(file_name):
    """Borra un archivo específico de la carpeta de uploads."""
    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
            return f"Archivo '{file_name}' borrado exitosamente."
        else:
            return f"El archivo '{file_name}' no existe."
    except Exception as e:
        return f"Error al borrar el archivo: {str(e)}"

def delete_all_files():
    """Borra todos los archivos en la carpeta de uploads."""
    try:
        for file_name in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        return "Todos los archivos han sido borrados exitosamente."
    except Exception as e:
        return f"Error al borrar los archivos: {str(e)}"

# Interfaz de usuario con Streamlit
st.title("Gestor de Archivos")

# Subida de archivos
uploaded_file = st.file_uploader("Sube un archivo (CSV, Excel o PDF)", type=['csv', 'xlsx', 'xls', 'pdf'])

if uploaded_file is not None:
    try:
        result = process_uploaded_file(uploaded_file)
        st.success(f"Archivo procesado: {result['type']} con ID: {uploaded_file.name}")
        
        # Mostrar las primeras filas del archivo subido
        if result['type'] in ["csv", "excel"]:
            df = result['data']
            st.write("Primeras filas del archivo:")
            st.dataframe(df.head())  # Muestra las primeras filas del DataFrame
            
        elif result['type'] == "pdf":
            full_text = result['text']
            st.write("Texto extraído del PDF:")
            st.text(full_text)  # Muestra el texto extraído del PDF

    except Exception as e:
        st.error(f"Error al procesar el archivo: {str(e)}")

# Listar archivos existentes
if st.button("Listar Archivos Subidos"):
    existing_files = list_uploaded_files()
    if existing_files:
        st.write("Archivos existentes:")
        for file in existing_files:
            if st.button(f"Ver Contenido de {file}"):
                # Cargar el contenido del archivo seleccionado
                file_path = os.path.join(UPLOAD_FOLDER, file)
                if file.endswith('.csv'):
                    df = read_csv(file_path)
                    st.write(f"Contenido de {file}:")
                    st.dataframe(df)  # Mostrar el contenido del CSV
                
                elif file.endswith('.xlsx') or file.endswith('.xls'):
                    df = read_excel(file_path)
                    st.write(f"Contenido de {file}:")
                    st.dataframe(df)  # Mostrar el contenido del Excel
                
                elif file.endswith('.pdf'):
                    full_text = extract_text_from_pdf(file_path)
                    st.write(f"Contenido de {file}:")
                    st.text(full_text)  # Mostrar el texto extraído del PDF
                
                if st.button("Atrás"):
                    st.experimental_rerun()  # Regresar a la vista anterior

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
