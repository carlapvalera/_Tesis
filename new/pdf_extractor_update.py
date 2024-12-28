import os
from dotenv import load_dotenv
from typing import Dict, Tuple, List
import json
import pdfplumber
import re

class PDFExtractor_withCid:
    def __init__(self):
        load_dotenv()  # Cargar las variables de entorno desde el archivo .env
        lang_file = os.getenv("PDF_FILENAME")  # Obtener el nombre del archivo desde las variables de entorno
        self.lang = self.load_lang_from_file(lang_file)

    def load_lang_from_file(self, filename: str) -> Dict[int, str]:
        """Carga el mapa CID desde un archivo JSON."""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                lang = json.load(file)
                # Convertir las claves de string a int
                lang = {int(key): value for key, value in lang.items()}
                
                # Agregar letras y caracteres especiales al diccionario
                lang.update(self.generate_additional_mappings())
                
                return lang
        except FileNotFoundError:
            raise FileNotFoundError(f"El archivo no se encontró: {filename}")
        except json.JSONDecodeError:
            raise ValueError(f"Error al decodificar el archivo JSON: {filename}")

    def generate_additional_mappings(self) -> Dict[int, str]:
        """Genera mapeos adicionales para letras y caracteres especiales."""
        additional_mappings = {}
        
        # Asignar letras minúsculas
        for ind, cha in zip(range(68, 94), "abcdefghijklmnopqrstuvwxyz"):
            additional_mappings[ind] = cha
        
        # Asignar letras mayúsculas
        for ind, cha in zip(range(36, 62), "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            additional_mappings[ind] = cha
        
        # Asignar caracteres especiales y dígitos
        for ind, cha in zip(range(3, 36), " !\"#$%&'()*+,-./0123456789:"):
            additional_mappings[ind] = cha
        
        return additional_mappings

    def to_actual_characters(self, text: str) -> str:
        """Convierte los CIDs en el texto a caracteres reales, manteniendo el texto original."""
        
        def replace_cid(match):
            cid_value = int(match.group(1))
            return self.lang.get(cid_value, f"(cid:{cid_value})")  # Retorna CID si no se encuentra

        # Usar una expresión regular para encontrar todos los CIDs en el texto
        return re.sub(r'\(cid:(\d+)\)', replace_cid, text)

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

# Ejemplo de uso
extractor = PDFExtractor_withCid()
text_content, tables_content = extractor.extract_text_and_tables("C:\\blabla\\_Tesis\\old\\01-territorio.pdf")

