from pdf2image import convert_from_path
import pytesseract

# Ruta del archivo PDF
pdf_path = "C:\\blabla\\_Tesis\\01-territorio.pdf"

# Convertir el PDF a imágenes
images = convert_from_path(pdf_path)

# Aplicar OCR a cada imagen y guardar el texto extraído
texto_extraido = []
for i, image in enumerate(images):
    texto = pytesseract.image_to_string(image, lang='eng')  # Cambia 'eng' por el idioma correspondiente si es necesario
    texto_extraido.append(texto)

# Guardar el texto extraído en un archivo
with open('texto_extraido_ocr.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(texto_extraido))

print("Texto extraído usando OCR y guardado.")
print(texto_extraido)