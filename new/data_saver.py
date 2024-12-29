import os
import pandas as pd
from dotenv import load_dotenv
from pdf_extractor_textocompleto import PDFExtractor_withCid

class DataSaver:
    def __init__(self):
        load_dotenv()  # Cargar las variables de entorno desde el archivo .env
        self.output_dir = os.getenv("OUTPUT_DIRECTORY", "temporal")  # Obtener el nombre del directorio desde las variables de entorno
        self._create_output_directory()
        self.cid = PDFExtractor_withCid()

    def _create_output_directory(self):
        """Crea el directorio de salida si no existe."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def save_text(self, text_content: list) -> None:
        """Guarda el texto extraído en un archivo .txt."""
        text_file_path = os.path.join(self.output_dir, "texto_extraido.txt")
        with open(text_file_path, "w", encoding="utf-8") as f:
            for page_text in text_content:
                processed_text = self.cid.to_actual_characters(page_text)
                f.write(processed_text + "\n\n")

    

# Ejemplo de uso
extractor = DataSaver()
ex = PDFExtractor_withCid()
text, tables = ex.extract_text_and_tables("C:\\blabla\\_Tesis\\old\\01-territorio.pdf")

extractor.save_text(text)
print ( "hola")