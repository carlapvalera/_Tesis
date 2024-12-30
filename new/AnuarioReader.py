class AnuarioReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.name = None
        self.year = None
        self.text_anuario = None
        self.tables_anuario = []
        self.index = None
        self.load_data()

    def load_data(self):
        """Carga los datos desde el archivo de texto."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                
                
                capitulo = "CAPÍTULO"
                capitulo_primer_indice = text.find(capitulo)
                num_cap_indice =capitulo_primer_indice + len(capitulo)
                num_cap_indice +=1
                cap = text[num_cap_indice]
                #print(text[num_cap_indice])# tengo el cnumero del capitulo q representa al anuario


                # Buscar la segunda ocurrencia comenzando justo después de la primera
                capitulo_segundo_indice = text.find("CAPÍTULO", num_cap_indice )
                #print(capitulo_segundo_indice)
                #print(text[capitulo_segundo_indice])

                contenido_ind = text.find("CONTENIDO")
                contenido_anuario = text[contenido_ind:capitulo_segundo_indice]
                self.index = contenido_anuario
                #print(contenido_ind)
                #print(text[contenido_ind])

                #NOMBRE DEL ANUARIO
                edicion = "EDICIÓN"
                edicion_indice =text.find(edicion)
                name = text[num_cap_indice +2: edicion_indice]
                self.name = name
                #AÑO 
                año = text[edicion_indice +len(edicion)+1: edicion_indice +len(edicion)+1+4]
                self.year = año
                #INDICE DEL ANUARIO
                # Extraer el texto desde la primera hasta la segunda ocurrencia
                contenido_indice_anuerio = text[num_cap_indice:capitulo_segundo_indice]
                #print(f'Texto entre la primera y segunda ocurrencia: "{contenido_indice_anuerio}"')


                # TEXTO DEL ANUARIO
                subcap = str(cap)+".1"
                tablas_indice = text.find(subcap,capitulo_segundo_indice)
                #print(tablas_indice)
                #print(text[tablas_indice:tablas_indice+20])

                text_anuario = text[capitulo_segundo_indice:tablas_indice]
                #print(text_anuario)
                self.text_anuario = text_anuario
                #TABLAS DEL ANUARIO
                tablas_anuario = text[tablas_indice:]
                self.tables_anuario = tablas_anuario
                #print(año)
                #print(name)

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
    anuario = AnuarioReader("C:\\blabla\\_Tesis\\temporal\\texto_extraido.txt")
    anuario.display_info()
