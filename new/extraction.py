import pdfplumber
import pandas as pd
import re
from typing import Dict

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
        120: "ñ",
        121: "ó",
        #123: "ú",
        126: "ú",
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

def extract_text_and_tables(pdf_path):
    text_content = []
    tables_content = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extraer texto plano
            text = page.extract_text()
            if text:
                text_content.append(text)

            # Extraer tablas
            tables = page.extract_tables()
            for table in tables:
                tables_content.append(table)

    return text_content, tables_content

def main():
    pdf_path = "C:\\blabla\\_Tesis\\old\\01-territorio.pdf" # Cambia esto por la ruta de tu PDF
    text_content, tables_content = extract_text_and_tables(pdf_path)

    # Crear el mapa de CIDs
    cid_map = default_cid_map()

    # Procesar y guardar texto en un archivo de texto
    with open("texto_extraido.txt", "w", encoding="utf-8") as f:
        for page_text in text_content:
            processed_text = to_actual_characters(page_text, cid_map)
            f.write(processed_text + "\n\n")

    # Procesar y guardar tablas en archivos CSV
    for i, table in enumerate(tables_content):
        df = pd.DataFrame(table[1:], columns=table[0])  # Usa la primera fila como encabezados
        
        # Reemplazar CIDs en cada celda del DataFrame
        for col in df.columns:
            df[col] = df[col].apply(lambda x: to_actual_characters(x, cid_map) if isinstance(x, str) else x)

        df.to_csv(f"tabla_extraida_{i}.csv", index=False)

if __name__ == "__main__":
    main()
