import os
from dotenv import load_dotenv
from typing import Dict, Tuple, List
import json
import pdfplumber

class PDFExtractor:
    def __init__(self):
        load_dotenv()  # Cargar las variables de entorno desde el archivo .env
        lang_file = os.getenv("PDF_FILENAME")  # Obtener el nombre del archivo desde las variables de entorno
        self.lang = self.load_lang_from_file(lang_file)

    def load_lang_from_file(self, filename: str) -> Dict[int, str]:
        """Carga el mapa CID desde un archivo JSON."""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"El archivo no se encontró: {filename}")
        except json.JSONDecodeError:
            raise ValueError(f"Error al decodificar el archivo JSON: {filename}")

    def to_actual_characters(self, text: str) -> str:
        ret = ""
        for number in text.replace("(cid:", ";").replace(")", "")[1:].split(";"):
            if not number.replace("\n", "").isdigit():
                continue
            
            cid_value = int(number.replace("\n", ""))
            if cid_value in self.lang:
                ret += self.lang[cid_value]
            else:
                ret += "(cid:" + number.replace("\n", "") + ")"
        
        return ret

    def extract_text_and_tables(self, pdf_path: str) -> Tuple[List[str], List[List]]:
        text_content = []
        tables_content = []

        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    # Extraer texto plano y convertir CID a caracteres reales
                    text = page.extract_text()
                    if text:
                        converted_text = self.to_actual_characters(text)
                        text_content.append(converted_text)

                    # Extraer tablas
                    tables = page.extract_tables()
                    for table in tables:
                        tables_content.append(table)
        except FileNotFoundError:
            raise FileNotFoundError(f"El archivo no se encontró: {pdf_path}")
        except pdfplumber.exceptions.PDFSyntaxError:
            raise ValueError(f"El archivo no es un PDF válido: {pdf_path}")
        except Exception as e:
            raise Exception(f"Ocurrió un error al procesar el archivo: {str(e)}")

        return text_content, tables_content

#Ejemplo de uso
extractor = PDFExtractor()
text, tables = extractor.extract_text_and_tables("ruta/al/archivo.pdf")
