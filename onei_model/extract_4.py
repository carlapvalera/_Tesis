from pdf2image import convert_from_path
import pytesseract

# Ruta del archivo PDF
pdf_path = "C:\\blabla\\_Tesis\\01-territorio.pdf"

# Convertir el PDF a imágenes
images = convert_from_path(pdf_path)

# Extraer texto usando OCR y guardar en un archivo
texto_completo = []
for i, image in enumerate(images):
    # Aplicar OCR a la imagen
    texto = pytesseract.image_to_string(image, lang='eng')  # Cambia 'eng' por el idioma correspondiente si es necesario
    texto_completo.append(texto)

# Guardar todo el texto extraído en un solo archivo
with open('texto_extraido_ocr.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(texto_completo))

print("Texto extraído usando OCR y guardado.")
print ( texto_completo)
