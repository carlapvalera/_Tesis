import re
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import camelot
from typing import Dict

# Mapa de caracteres
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

# Completar el mapa con letras y símbolos
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

def to_actual_characters(text: str) -> str:
    ret = ""
    for number in text.replace("(cid:", ";").replace(")", "")[1:].split(";"):
        # Verificar si cleaned_number es un número
        if not number.replace("\n", "").isdigit():
            continue  # Si no es un número, continuar con la siguiente iteración
        
        if int(number.replace("\n", "")) in lang:
            ret += lang[int(number.replace("\n", ""))]
        else:
            ret += "(cid:" + number.replace("\n", "") + ")"
        
        if "\n" in number:
            ret += "\n"
    
    return ret

# Ruta al archivo PDF
pdf_path = 'C:\\blabla\\_Tesis\\01-territorio.pdf'

"""# Extraer texto usando PDFMiner
print("Texto extraído del PDF:")
for page_layout in extract_pages(pdf_path):
    for element in page_layout:
        if isinstance(element, LTTextContainer):
            print(to_actual_characters(element.get_text()))"""

# Extraer tablas usando Camelot
print("\nTablas extraídas del PDF:")
tables = camelot.read_pdf(pdf_path, pages='1-10', flavor='stream')

# Imprimir el número de tablas encontradas y exportar a CSV
print(f"Número de tablas encontradas: {len(tables)}")
for i, table in enumerate(tables):
    table.to_csv(f'tabla_extraida_{i + 1}.csv')
    print(f"Tabla {i + 1} exportada a 'tabla_extraida_{i + 1}.csv'")
