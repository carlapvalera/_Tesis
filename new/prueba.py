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
from dataframetables import DataFrameCreator
from embed_db import DB_Embed
from document import Document
import json

# Crear un directorio temporal si no existe
temp_dir = "C:\\blabla\\_Tesis\\new\\temporal"
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)
load_dotenv()  # Cargar las variables de entorno desde el archivo .env
dir_temporal = os.getenv("PDF_ANUARIOS")
extractor = DataSaver()
ex = PDFExtractor_withCid()
database = AnuarioDatabase()    
dataframecreator = DataFrameCreator()
embeddb = DB_Embed()

"""
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
        text= ex.extract_text_and_tables(dir_temporal+dir[temp_index:])
        extractor.save_text(text)
        print(file_path)
        
       #st.write(dir_temporal+dir[temp_index:])"""







"""
#for i in range(0,3):
files = os.listdir("C:\\blabla\\_Tesis\\temporal")

for fil in files:
    anuarioreader = AnuarioReader("C:\\blabla\\_Tesis\\temporal\\"+fil)
    list_anuarios.append(anuarioreader)




list_anuario_tablas = []
if list_anuarios:
    for anuario in list_anuarios:
        for i in range(0, len(anuario.chapters)):

            try:

                tablas = Tables(anuario.tables_anuario[i],anuario.chapters[i][0]) 
                list_anuario_tablas.append((anuario,tablas))   
            except Exception as e:
                list_anuario_tablas.append((None,None)) 
                raise Exception(f"Ocurrió un error al procesar las tablas: {str(e)}")
            

if list_anuario_tablas:
    ya = True
    chapter_id = []
    count = 0
    for anuario,tablas in list_anuario_tablas:
        id_anuario =database.insert_anuario(anuario.year,anuario.introduction,anuario.fuentes_info,anuario.abreviaturas,anuario.signos,anuario.local)
        if ya :
            for i in range (0,len(anuario.chapters)):
                print(anuario.chapters[i][0])
                
                id_chapter = database.insert_capitulo(id_anuario,anuario.chapters[i][0],anuario.chapters[i][1],anuario.text_anuario[i])
                chapter_id.append(id_chapter)
                chapter = Document("chapter:" +str(id_chapter),anuario.text_anuario[i])
                try:
                    embeddb.set_text(chapter)
                except:
                   pass
            ya = False
        for tabla in tablas.tables :

            name = "fallo"
            try:
                name, headers, table = dataframecreator.get_table(tabla)
            except:
                id_table =database.insert_tabla(chapter_id[count],tabla[:50],tabla)
                tableembed = Document("table:"+str(id_table),tabla)
                try:
                    embeddb.set_text(tableembed)
                except:
                    continue
                continue

            print(name)
            id_table =database.insert_tabla(chapter_id[count],name + headers ,table)
            tableembed = Document("table:"+str(id_table),name + headers+table)
            try:
                embeddb.set_text(tableembed)
            except:
                pass
        count = count +1

"""







def process_query(query):
    """Función para procesar la consulta y generar una respuesta."""
    # Aquí puedes implementar la lógica para generar una respuesta
    return f"Has preguntado: {query}"


interactions = []
while True:
        # Recibir la consulta del usuario
    query = input("Introduce tu consulta (o escribe 'salir' para terminar): ")
    
    # Salir del bucle si el usuario escribe 'salir'
    if query.lower() == 'salir':
        print("Saliendo del programa.")
        break
        
        # Procesar la consulta (aquí puedes agregar tu lógica)
    response = process_query(query)
        
        # Imprimir la respuesta
    print(f"Respuesta: {response}")
    context = ""

    for i in embeddb.most_relevant(query):
        context +=i[0].text
    gem = Gemini_API()
    response = gem.generate_response(query,context)

         # Guardar la interacción en el registro
    interactions.append({
        "query": query,
        "context": context,
        "response": response
    })

# Guardar todas las interacciones en un archivo JSON al final
with open('interactions.json', 'w') as json_file:
    json.dump(interactions, json_file, indent=4)

print("Todas las interacciones han sido guardadas en 'interactions.json'.")
    

"""# Supongamos que el JSON está guardado en un archivo llamado 'data.json'
with open('expected_responses.json', 'r', encoding='utf-8') as json_file:
    comparations = json.load(json_file)

# Ahora 'comparations' contiene los datos del JSON
print(comparations)
"""

