from gemini_api import Gemini_API
import os
from dotenv import load_dotenv
from data_saver import DataSaver
print ("hola")
from pdf_extractor_textocompleto import PDFExtractor_withCid
print ("hola")
from AnuarioReader import AnuarioReader
print ("hola")
from tables import Tables
print ("hola")
from AnuarioDatabase import AnuarioDatabase

# Crear un directorio temporal si no existe
temp_dir = "C:\\blabla\\_Tesis\\new\\temporal"
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)
load_dotenv()  # Cargar las variables de entorno desde el archivo .env
dir_temporal = os.getenv("PDF_ANUARIOS")
extractor = DataSaver()
ex = PDFExtractor_withCid()
database = AnuarioDatabase()    


# Mostrar archivos en el directorio temporal
files_in_temp = os.listdir(temp_dir)
if files_in_temp:
    # Crear una lista de direcciones completas de los archivos
    file_paths = [os.path.join(temp_dir, file) for file in files_in_temp]
    
#crear la lista de directorios completa
files_full_paths = []
list_anuarios = []
if files_in_temp :
    # Crear una lista de direcciones completas de los archivos
    for dir in file_paths:
        temp_index = dir.find("temporal")
        temp_index += len("temporal")+1
        file_path = os.path.join("C:", "blabla", "_Tesis", "new", "temporal", dir[temp_index:])

        files_full_paths.append(dir_temporal+dir[temp_index:])
        #text= ex.extract_text_and_tables(dir_temporal+dir[temp_index:])
        #extractor.save_text(text)
        #print(file_path)
        #st.write(dir_temporal+dir[temp_index:])



files = os.listdir("C:\\blabla\\_Tesis\\temporal")

for fil in files:
    anuarioreader = AnuarioReader(dir_temporal+dir[temp_index:])
    list_anuarios.append(anuarioreader)




list_anuario_tablas = []
if list_anuarios:
    for anuario in list_anuarios:
        for i in range(0, len(anuario.chapters)-1):

            try:

                tablas = Tables(anuario.tables_anuario[i],anuario.chapters[i][0]) 
                list_anuario_tablas.append((anuario,tablas))   
            except Exception as e:
                list_anuario_tablas.append((None,None)) 
                raise Exception(f"Ocurrió un error al procesar las tablas: {str(e)}")
            
            

if list_anuario_tablas:
    for anuario,tablas in list_anuario_tablas:
        id_anuario =database.insert_anuario(anuario.year,anuario.introduction,anuario.fuentes_info,anuario.abreviaturas,anuario.signos,anuario.local)
        for i in range (0,len(anuario.chapters)-1):
            id_chapter = database.insert_capitulo(id_anuario,anuario.chapters[i][0],anuario.chapters[i][1],anuario.text_anuario[i])

            
            database.insert_tabla(id_chapter,tablas.tables[i],anuario.chapters[i][0])
        


