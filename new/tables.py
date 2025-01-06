class Tables:
    def __init__(self, tables_in_text: str, cap: str):
        self.tables_in_text = tables_in_text 
        self.cap = cap
        self.tables = []

    def subcap(self, cap, index):
        for i in range(1, 100):  # Cambié el rango para que funcione correctamente
            try :
                index = self.tables_in_text.find(index, cap + "." + str(i))
            except:
                index= -1
            
            next_index = self.subcap(self.cap + "." + str(i), index)
            if next_index == -1:
                a = i + 1
                next_index = self.tables_in_text.find(cap + "." + str(a))
                if next_index == -1:
                    return self.tables_in_text.find(cap + "." + str(index + 1))

            # Asegúrate de que el índice esté dentro del rango
            if index != -1 and next_index != -1:
                self.tables.append(self.tables_in_text[index:next_index])

    def get_tables(self):
        finish = False
        for i in range(1, 100):  # Cambié el rango para que funcione correctamente
            try :
                temp = self.cap + "." + str(i)
                index = self.tables_in_text.find(index, temp)
            except:
                index= -1
            next_index = self.subcap(self.cap + "." + str(i), index)
            if next_index == -1:
                finish = True
                next_index = self.tables_in_text.find("Teléfono")  # Cambia esto según tu contexto
            if index != -1 and next_index != -1:
                self.tables.append(self.tables_in_text[index:next_index])
            if finish:
                break

# Ejemplo de uso
if __name__ == "__main__":
    # Texto de ejemplo que contiene tablas o secciones numeradas
    example_text = """
    1.1 Introducción
    Este es un texto introductorio.
    
    1.2 Tabla de Datos
    1.2.1 Datos A
    Aquí van algunos datos relevantes.
    
    1.2.2 Datos B
    Aquí van más datos relevantes.
    
    1.3 Conclusiones
    Esta es la conclusión del documento.
    
    Teléfono: 123-456-7890
    """

    # Crear una instancia de la clase Tables
    tables_extractor = Tables(tables_in_text=example_text, cap="1")

    # Obtener las tablas del texto
    tables_extractor.get_tables()

    # Imprimir las tablas extraídas
    for idx, table in enumerate(tables_extractor.tables):
        print(f"Tabla {idx+1}:\n{table}\n")
