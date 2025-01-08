class Tables:
    def __init__(self, tables_in_text: str, cap: str):
        self.tables_in_text = tables_in_text 
        self.cap = cap
        self.tables = []
        self.get_tables()

    def subcap(self, cap, index):
        for i in range(1, 100):  # Cambié el rango para que funcione correctamente
            index = self.tables_in_text.find( cap + "." + str(i),index)
            if index != -1:
                next_index = self.tables_in_text.find(cap + "." + str(i + 1),index)
                if next_index == 1:
                    return index
                else:
                    self.tables.append(self.tables_in_text[index:next_index])
            else:
                break
              
        return -1

    def get_tables(self):
        finish = False
        for i in range(1, 100):  # Cambié el rango para que funcione correctamente
            # Busca el índice del subtítulo
            index = self.tables_in_text.find(self.cap + "." + str(i))
            next_index = self.subcap(self.cap + "." + str(i), index)
            if next_index == -1:
                next_index = self.tables_in_text.find(self.cap + "." + str(i+1), index)
            if next_index == -1:
                finish = True
                next_index = self.tables_in_text.find("Teléfono")  # Cambia esto según tu contexto
            if index != -1 and next_index != -1:
                self.tables.append(self.tables_in_text[index:next_index])
            if finish:
                break
