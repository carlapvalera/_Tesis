import re
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import camelot
from typing import Dict

# Mapa de caracteres CID
def default_cid_map() -> Dict[int, str]:
    lang = {
        3: " ",
        4: "!",
        11: "(",
        12: ")",
        97: "~",
        105: "á",
        108: "ä",
        116: "í",
        121: "ó",
        123: "ú",
        129: "ü",
        203: "Í",
        207: "Ó",
    }
    ind = 68
    for cha in "abcdefghijklmnopqrstuvwxyz":
        lang[ind] = cha
        ind += 1
    ind = 36
    for cha in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        lang[ind] = cha
        ind += 1
    ind = 3
    for cha in " !\"#$%&'()*+,-./0123456789:":
        lang[ind] = cha
        ind += 1
    return lang

def to_actual_characters(text: str, lang: Dict[int, str]) -> str:
    ret = ""
    for number in text.replace("(cid:", ";").replace(")", "")[1:].split(";"):
        if not number.replace("\n", "").isdigit():
            continue
        
        cid_value = int(number.replace("\n", ""))
        if cid_value in lang:
            ret += lang[cid_value]
        else:
            ret += "(cid:" + number.replace("\n", "") + ")"
        
    return ret

# Ruta al archivo PDF
pdf_path = 'C:\\blabla\\_Tesis\\old\\01-territorio.pdf'

# Extraer texto usando PDFMiner
print("Texto extraído del PDF:")
for page_layout in extract_pages(pdf_path):
    for element in page_layout:
        if isinstance(element, LTTextContainer):
            print(to_actual_characters(element.get_text(), default_cid_map()))

# Extraer tablas usando Camelot
print("\nTablas extraídas del PDF:")
tables = camelot.read_pdf(pdf_path, pages='1-10', flavor='stream')

# Imprimir el número de tablas encontradas y procesar cada tabla
print(f"Número de tablas encontradas: {len(tables)}")
for i, table in enumerate(tables):
    # Convertir la tabla a DataFrame y luego a CSV para exportar
    df = table.df
    
    # Reemplazar CIDs en cada celda del DataFrame
    for col in df.columns:
        df[col] = df[col].apply(lambda x: to_actual_characters(x, default_cid_map()))
    
    # Imprimir el contenido procesado de la tabla
    print(f"\nContenido procesado de la Tabla {i + 1}:")
    print(df.to_string(index=False))
    
    # Exportar la tabla a CSV (opcional)
    table.to_csv(f'tabla_extraida_{i + 1}.csv')
    print(f"Tabla {i + 1} exportada a 'tabla_extraida_{i + 1}.csv'")
