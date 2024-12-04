import pandas as pd
import os
import pdfplumber
from ..database.conection import insert_file_data


# Carpeta donde se guardarán los archivos subidos
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
        # Guardar en la base de datos
        file_id = insert_file_data(
            name=uploaded_file.name,
            file_type='csv',
            description='Archivo CSV subido.',
            content=data.to_string(),  # Convierte el DataFrame a string para almacenar
            embedding=[]
        )
        return {"type": "csv", "data": data, "file_id": file_id}

    elif uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
        data = read_excel(file_path)
        # Guardar en la base de datos
        file_id = insert_file_data(
            name=uploaded_file.name,
            file_type='excel',
            description='Archivo Excel subido.',
            content=data.to_string(),  # Convierte el DataFrame a string para almacenar
            embedding=[]
        )
        return {"type": "excel", "data": data, "file_id": file_id}

    elif uploaded_file.name.endswith('.pdf'):
        full_text = extract_text_from_pdf(file_path)
        # Guardar en la base de datos
        file_id = insert_file_data(
            name=uploaded_file.name,
            file_type='pdf',
            description='Archivo PDF subido.',
            content=full_text,
            embedding=[]
        )
        return {"type": "pdf", "text": full_text, "file_id": file_id}

    else:
        raise ValueError("Unsupported file type.")


# list de la carpeta de upload
def list_uploaded_files():
    """Lista los archivos existentes en la carpeta de uploads."""
    return os.listdir(UPLOAD_FOLDER)



# borar de la carpeta de upload

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










# Ejemplo de uso
if __name__ == "__main__":
    # Aquí puedes simular la subida de un archivo para pruebas
    # uploaded_file = ... (proporcionar un objeto similar al que recibirías en Streamlit)
    
    # Procesar el archivo subido (ejemplo)
    # result = process_uploaded_file(uploaded_file)
    
    # Listar archivos existentes
    existing_files = list_uploaded_files()
    print("Archivos existentes:", existing_files)

    # Procesar un archivo subido (simulación)
    # uploaded_file = ... (proporcionar un objeto similar al que recibirías en Streamlit)

    # Borrar un archivo específico
    result_delete = delete_file("2404.18681v1.pdf")
    print(result_delete)

    # Borrar todos los archivos
    result_delete_all = delete_all_files()
    print(result_delete_all)

    # Listar archivos existentes
    existing_files = list_uploaded_files()
    print("Archivos existentes:", existing_files)