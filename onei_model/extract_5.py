import camelot

# Leer tablas del PDF
tables = camelot.read_pdf('C:\\blabla\\_Tesis\\01-territorio.pdf', flavor='stream')

# Imprimir el número de tablas encontradas
print(f"Número de tablas encontradas: {len(tables)}")

# Exportar la primera tabla a CSV (si existe)
if tables:
    tables[0].to_csv('tabla_extraida.csv')
    print("Tabla exportada a 'tabla_extraida.csv'")
else:
    print("No se encontraron tablas.")
