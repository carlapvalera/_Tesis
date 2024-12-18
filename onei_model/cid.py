from typing import Dict

class Cid:
    def __init__(self):
        # Inicializar el atributo _cid como un diccionario vacío
        self._cid: Dict[int, str] = self.__default_cid_map()

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

    def __default_cid_map(self) -> Dict[int, str]:
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

