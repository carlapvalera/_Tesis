import os
import unittest
import pandas as pd
from unittest.mock import MagicMock
from dotenv import load_dotenv
from data_saver import DataSaver

class TestDataSaver(unittest.TestCase):
    def setUp(self):
        load_dotenv()  # Cargar las variables de entorno desde el archivo .env
        self.output_dir = os.getenv("OUTPUT_DIRECTORY", "temporal")
        self.data_saver = DataSaver()
        # Asegurarse de que el directorio de salida esté limpio antes de cada prueba
        if os.path.exists(self.output_dir):
            for file in os.listdir(self.output_dir):
                os.remove(os.path.join(self.output_dir, file))
        else:
            os.makedirs(self.output_dir)

    def tearDown(self):
        # Limpiar después de cada prueba
        for file in os.listdir(self.output_dir):
            os.remove(os.path.join(self.output_dir, file))

    def test_save_text(self):
        text_content = ["Texto de prueba 1", "Texto de prueba 2"]
        self.data_saver.save_text(text_content)

        with open(os.path.join(self.output_dir, "texto_extraido.txt"), "r", encoding="utf-8") as f:
            saved_text = f.read().strip().split('\n\n')

        self.assertEqual(saved_text[0], "Texto de prueba 1")
        self.assertEqual(saved_text[1], "Texto de prueba 2")

    def test_save_tables(self):
        tables_content = [
            [["Columna1", "Columna2"], ["Valor1", "Valor2"], ["Valor3", "Valor4"]],
            [["ColumnaA", "ColumnaB"], ["ValorA", "ValorB"], ["ValorC", "ValorD"]]
        ]
        
        self.data_saver.save_tables(tables_content)

        for i in range(len(tables_content)):
            df = pd.read_csv(os.path.join(self.output_dir, f"tabla_extraida_{i}.csv"))
            self.assertEqual(list(df.columns), tables_content[i][0])
            self.assertEqual(df.shape[0], len(tables_content[i]) - 1)  # -1 porque la primera fila son los encabezados

if __name__ == "__main__":
    unittest.main()
