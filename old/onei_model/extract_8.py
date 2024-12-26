import camelot
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
    """Elimina todas las ocurrencias de (cid:<número>) del texto."""
    return re.sub(r"\(cid:\d+\)", "", text)

def replace_cids(text: str, cid_map: Dict[int, str]) -> str:
    """Reemplaza las ocurrencias de (cid:<número>) en el texto con su correspondiente carácter."""
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
    
    # Ruta al archivo PDF
    pdf_path = 'C:\\blabla\\_Tesis\\old\\01-territorio.pdf'

    # Leer todas las tablas del PDF
    tables = camelot.read_pdf(pdf_path, pages='1-10', flavor='stream')

    # Imprimir el número de tablas encontradas
    print(f"Número de tablas encontradas: {len(tables)}")

    # Procesar cada tabla y reemplazar CIDs en su texto
    for i, table in enumerate(tables):
        # Convertir la tabla a un DataFrame y luego a texto
        table_text = table.df.to_string(index=False)  # Convertir a string sin índices
        
        # Reemplazar CIDs en el texto de la tabla
        replaced_text = replace_cids(table_text, cid_map)
        
        # Imprimir el texto procesado
        print(f"\nTexto procesado de la Tabla {i + 1}:")
        print(replaced_text)
        
        # Exportar la tabla a CSV (opcional)
        table.to_csv(f'tabla_extraida_{i + 1}.csv')
        print(f"Tabla {i + 1} exportada a 'tabla_extraida_{i + 1}.csv'")
