import os
from dotenv import load_dotenv
from typing import Dict, Tuple, List
import json
import pdfplumber

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
                self.lang =  {int(key): value for key, value in lang.items()}
        except FileNotFoundError:
            raise FileNotFoundError(f"El archivo no se encontró: {filename}")
        except json.JSONDecodeError:
            raise ValueError(f"Error al decodificar el archivo JSON: {filename}")
        ind = 68
        for cha in "abcdefghijklmnopqrstuvwxyz":
            self.lang[ind] = cha
            ind += 1
        ind = 36
        for cha in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            self.lang[ind] = cha
            ind += 1
        ind = 3
        for cha in " !\"#$%&'()*+,-./0123456789:":
            self.lang[ind] = cha
            ind += 1
        return self.lang


    def to_actual_characters(self, text: str) -> str:
        ret = ""
        for number in text.replace("(cid:", ";").replace(")", "")[1:].split(";"):
            if not number.replace("\n", "").isdigit():
                continue
            
            cid_value = int(number.replace("\n", ""))
            
            if cid_value in self.lang:
                if cid_value == 207:
                    pass
                ret += self.lang[cid_value]
                print (self.lang[cid_value])
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
                        text_content.append(text)

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
extractor = PDFExtractor_withCid()
dic = extractor.lang
text, tables = extractor.extract_text_and_tables("C:\\blabla\\_Tesis\\old\\01-territorio.pdf")
aaaaaaaaaaaaaaaa= extractor.to_actual_characters("(cid:36)(cid:49)(cid:56)(cid:36)(cid:53)(cid:44)(cid:50)(cid:3)\n(cid:40)(cid:54)(cid:55)(cid:36)(cid:39)(cid:203)(cid:54)(cid:55)(cid:44)(cid:38)(cid:50)(cid:3)\n(cid:39)(cid:40)(cid:3)(cid:38)(cid:56)(cid:37)(cid:36)(cid:3)(cid:21)(cid:19)(cid:21)(cid:22)\n(cid:38)(cid:36)(cid:51)(cid:203)(cid:55)(cid:56)(cid:47)(cid:50)(cid:3)(cid:20)(cid:29)(cid:3)(cid:55)(cid:40)(cid:53)(cid:53)(cid:44)(cid:55)(cid:50)(cid:53)(cid:44)(cid:50)(cid:3)\n(cid:40)(cid:39)(cid:44)(cid:38)(cid:44)(cid:207)(cid:49)(cid:3)(cid:21)(cid:19)(cid:21)(cid:23)")
print (aaaaaaaaaaaaaaaa)   