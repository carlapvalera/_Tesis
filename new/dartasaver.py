import os
import pandas as pd
from dotenv import load_dotenv
from new.pdf_extractor import PDFExtractor_withCid

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

    def save_tables(self, tables_content: list) -> None:
        """Guarda las tablas extraídas en archivos .csv."""
        for i, table in enumerate(tables_content):
            df = pd.DataFrame(table[1:], columns=table[0])  # Usa la primera fila como encabezados
            
            # Reemplazar CIDs en cada celda del DataFrame
            for col in df.columns:
                df[col] = df[col].apply(lambda x: self.cid.to_actual_characters(x) if isinstance(x, str) else x)

            csv_file_path = os.path.join(self.output_dir, f"tabla_extraida_{i}.csv")
            df.to_csv(csv_file_path, index=False)



# Ejemplo de uso
# extractor = PDFExtractor()
# extractor.extract_text_and_tables("ruta/al/archivo.pdf")
