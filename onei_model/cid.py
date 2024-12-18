import re
from typing import Dict

def default_cid_map() -> Dict[int, str]:
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

def remove_cids(text: str) -> str:
    """Elimina todas las ocurrencias de (cid:<número> del texto."""
    return re.sub(r"\(cid:\d+\)", "", text)

def replace_cids(text: str, cid_map: Dict[int, str]) -> str:
    """Reemplaza las ocurrencias de (cid:<número> en el texto con su correspondiente carácter."""
    def _replace_cid(m: re.Match) -> str:
        cid = int(m.group(1))
        if cid in cid_map:
            return cid_map[cid]
        return m.group()  # Si no se encuentra el CID, devolverlo sin cambios

    return re.sub(r"\(cid:(\d+)\)", _replace_cid, text)

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
