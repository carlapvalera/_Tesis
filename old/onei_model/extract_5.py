import camelot

# Ruta al archivo PDF
pdf_path = 'C:\\blabla\\_Tesis\\01-territorio.pdf'

# Leer todas las tablas del PDF
tables = camelot.read_pdf(pdf_path, pages='1-10', flavor='stream')

# Imprimir el número de tablas encontradas
print(f"Número de tablas encontradas: {len(tables)}")

# Exportar todas las tablas a CSV
for i, table in enumerate(tables):
    table.to_csv(f'tabla_extraida_{i + 1}.csv')
    print(f"Tabla {i + 1} exportada a 'tabla_extraida_{i + 1}.csv'")
