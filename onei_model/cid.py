from typing import Dict

class Cid:
    def __init__(self):
        # Inicializar el atributo _cid como un diccionario vacío
        self._cid: Dict[int, str] = self._default_cid_map()

    @property
    def cid(self):
        return self._cid 

    def set_cid(self, clave: int, valor: str):
        """Agregar un nuevo par clave-valor al diccionario."""
        self._cid[clave] = valor

    def get_cid(self, clave: int) -> str:
        """Obtener el valor asociado a la clave dada."""
        return self._cid.get(clave, "Clave no encontrada")

    def print_cids(self):
        """Mostrar todos los pares clave-valor en el diccionario."""
        for clave, valor in self._cid.items():
            print(f"{clave}: {valor}")

    def _default_cid_map(self) -> Dict[int, str]:
        cid_map = {
            34: "?",
            97: "~",
            108: "ä",
            129: "ü",
            180: '"',
            181: '"',
            183: "'",
            203: "í",
            207: "ó",
        }
        for i, char in enumerate("abcdefghijklmnopqrstuvwxyz"):
            cid_map[68 + i] = char
        for i, char in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            cid_map[36 + i] = char
        for i, char in enumerate(" !\"#$%&'()*+,-./0123456789:"):
            cid_map[3 + i] = char
        return cid_map

# Ejemplo de uso y test
if __name__ == "__main__":
    # Crear una instancia de Cid
    cid_instance = Cid()
    
    # Imprimir los CIDs por defecto
    print("Contenido del diccionario _cid:")
    cid_instance.print_cids()

    # Probar agregar un nuevo CID
    print("\nAgregando un nuevo CID:")
    cid_instance.set_cid(999, "nuevo")
    
    # Verificar que se ha agregado correctamente
    print("Valor para la clave 999:", cid_instance.get_cid(999))  # Salida: nuevo

    # Probar obtener un CID que no existe
    print("Valor para la clave 1000:", cid_instance.get_cid(1000))  # Salida: Clave no encontrada

    # Mostrar todos los CIDs después de agregar uno nuevo
    print("\nContenido del diccionario _cid después de agregar:")
    cid_instance.print_cids()


def to_acctual_characters(text: str):
    ret = ""
    for number in text.replace("(cid:", ";").replace(")", "")[1:].split(";"):
        # Verificar si cleaned_number es un número
        if not number.replace("\n", "").isdigit():
            continue  # Si no es un número, continuar con la 

        if int(number.replace("\n", "")) in lang:
            ret = ret + lang[int(number.replace("\n", ""))]
        else:
            ret = ret + "(cid:" + number.replace("\n", "") + ")"
        if "\n" in number:
            ret = ret + "\n"
    return ret


for page_layout in extract_pages("C:\\blabla\\_Tesis\\01-territorio.pdf"):
    for element in page_layout:
        if isinstance(element, LTTextContainer):
            print(to_acctual_characters(element.get_text()))




# Ejemplo de uso
if __name__ == "__main__":
    # Crear el mapa de CIDs por defecto
    cid_map = default_cid_map()
    
    # Texto de ejemplo que contiene CIDs
    example_text = "(cid:36)(cid:49)(cid:56)(cid:36)(cid:53)(cid:44)(cid:50)(cid:3)" "(cid:40)(cid:54)(cid:55)(cid:36)(cid:39)(cid:203)(cid:54)(cid:55)(cid:44)(cid:38)(cid:50)(cid:3)""(cid:39)(cid:40)(cid:3)(cid:38)(cid:56)(cid:37)(cid:36)(cid:3)(cid:21)(cid:19)(cid:21)(cid:22)""(cid:38)(cid:36)(cid:51)(cid:203)(cid:55)(cid:56)(cid:47)(cid:50)(cid:3)(cid:20)(cid:29)(cid:3)(cid:55)(cid:40)(cid:53)(cid:53)(cid:44)(cid:55)(cid:50)(cid:53)(cid:44)(cid:50)(cid:3)""(cid:40)(cid:39)(cid:44)(cid:38)(cid:44)(cid:207)(cid:49)(cid:3)(cid:21)(cid:19)(cid:21)(cid:23)"

    
    # Reemplazar CIDs en el texto
    replaced_text = replace_cids(example_text, cid_map)
    
    print("Texto original:", example_text)
    print("Texto con CIDs reemplazados:", replaced_text)
    
    # Eliminar CIDs del texto
    cleaned_text = remove_cids(example_text)
    
    print("Texto sin CIDs:", cleaned_text)
