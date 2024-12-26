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
    example_text = "Este es un ejemplo con (cid:68) y (cid:97)."
    
    # Reemplazar CIDs en el texto
    replaced_text = replace_cids(example_text, cid_map)
    
    print("Texto original:", example_text)
    print("Texto con CIDs reemplazados:", replaced_text)
    
    # Eliminar CIDs del texto
    cleaned_text = remove_cids(example_text)
    
    print("Texto sin CIDs:", cleaned_text)
