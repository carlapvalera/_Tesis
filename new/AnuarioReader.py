import re
class AnuarioReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.name = None
        self.year = None
        self.text_anuario = []
        self.tables_anuario = []
        self.index = None
        self.chapters = None
        self.introduccion = None
        self.fuentes_info = None
        self.abreviaturas = None
        self.signos = None
        self.text_tablas = []
        self.local = None

        self.load_data()


    def extract_chapters(self,text):
        # Expresión regular para encontrar capítulos en el formato "número. nombre"
        pattern = r'(\d+)\.\s+(.*?)(?=\n\d+\.\s+|$)'  # Busca "número. nombre" hasta el siguiente número o el final del texto
        matches = re.findall(pattern, text, re.DOTALL)  # Usar re.DOTALL para que . incluya saltos de línea

        # Convertir los resultados a una lista de tuplas (número, nombre)
        chapters = [(int(num), name.strip()) for num, name in matches]
        
        return chapters
    def load_data(self):
        """Carga los datos desde el archivo de texto."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                
                text = file.read()
                
                
                capitulo = "CAPÍTULO"
                contenido = "CONTENIDO"
                edicion = "EDICIÓN"
                capitulos = "Capítulos:"
                introduc = "INTRODUCCIÓN"
                fuentes = "FUENTES DE INFORMACIÓN "
                abrev = "ABREVIATURAS "
                signos = "SIGNOS  CONVENCIONALES "
                indice = "ÍNDICE"
                telefono = "Teléfono"
                cuba = "Cuba"
                
                

                #AÑO DEL ANUARIO
                edicion_indice =text.find(edicion)
                año = text[edicion_indice +len(edicion)+1: edicion_indice +len(edicion)+1+4]
                self.year = año

                #INDICE DEL ANUARIO/ capitulos
                contenido_indice = text.find(contenido)
                capitulos_indice = text.find(capitulos,contenido_indice)
                introduc_indice = text.find(introduc,capitulos_indice)
                chapters = self.extract_chapters(text[capitulos_indice:introduc_indice])
                self.chapters = chapters

                #INTRODUCCION
                fuentes_indice = text.find(fuentes,introduc_indice)
                self.introduccion = text[introduc_indice:fuentes_indice]

                #Fuente de informacion
                abrev_indice = text.find(abrev,fuentes_indice)
                self.fuentes_info = text[fuentes_indice:abrev_indice]
                
                #abreviaturas
                signos_indice = text.find(signos,abrev_indice)
                self.abreviaturas = text[abrev_indice:signos_indice]

                #signos convencionales
                indice_indice = text.find(indice,signos_indice)
                self.signos = text[signos_indice:indice_indice]



                text_sin_saltos = text.replace('\n', ' ')
                text = text_sin_saltos
                indice_indice = text.find(indice)



                last = text.find(capitulo,indice_indice)
                telefono_indice = None
                #capitulos
                for number, name in chapters:
                    capitulo_indice = text.find(capitulo,last)
                    if (text[capitulo_indice:capitulo_indice+10]=="CAPÍTULOCO"):
                        capitulo_indice = text.find( "CAPÍTULO 9",capitulo_indice+10)

                    print(text[capitulo_indice:capitulo_indice+10])
                    capitulo_numero = text.find(str(number),capitulo_indice)
                    print(text[capitulo_numero:capitulo_numero+10])
                    capitulo_nombre = text.find(name,capitulo_numero)
                    print(text[capitulo_nombre:capitulo_nombre+10])

                    subcap = str(number)+".1"

                    subcap_indice = text.find(subcap,capitulo_indice)
                    print( text[subcap_indice:subcap_indice+10])

                    text_capitulo = text[capitulo_indice:subcap_indice]
                    self.text_anuario.append(text_capitulo)
                    capitulo_indice = text.find(capitulo,subcap_indice)
                    if(capitulo_indice == -1):
                        capitulo_indice = text.find(telefono,subcap_indice)
                        telefono_indice = capitulo_indice

                    tablas_capitulo = text[subcap_indice:capitulo_indice]

                    self.tables_anuario.append(tablas_capitulo)

                    last = capitulo_indice 

                    print(f"{number}. {name}")  
                
                #telefono correo
                if(telefono_indice!=None):
                    self.local = text[telefono_indice:]

        except FileNotFoundError:
            print(f"Error: El archivo '{self.file_path}' no se encuentra.")
        except Exception as e:
            print(f"Error al leer el archivo: {e}")

    def display_info(self):
        """Muestra la información cargada."""
        print(f"Nombre: {self.name}")
        print(f"Año: {self.year}")
        print(f"Índice del Anuario:{self.index}")
        print(f"Texto del Anuario: {self.text_anuario}")
        print("Tablas del Anuario:")
        for tabla in self.tables_anuario:
            print(f"- {tabla}")

# Ejemplo de uso
if __name__ == "__main__":
    anuario = AnuarioReader("C:\\blabla\\_Tesis\\new\\temporal\\texto_extraido.txt")
    anuario.display_info()
