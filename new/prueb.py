import re

def extract_chapters(text):
    # Expresión regular para encontrar capítulos en el formato "número. nombre"
    pattern = r'(\d+)\.\s+(.*?)(?=\n\d+\.\s+|$)'  # Busca "número. nombre" hasta el siguiente número o el final del texto
    matches = re.findall(pattern, text, re.DOTALL)  # Usar re.DOTALL para que . incluya saltos de línea

    # Convertir los resultados a una lista de tuplas (número, nombre)
    chapters = [(int(num), name.strip()) for num, name in matches]
    
    return chapters

# Ejemplo de uso
input_string = """
1. Territorio    
2. Medio Ambiente 
3. Población 
4. Organización Institucional 
5. Cuentas Nacionales 
6. Finanzas 
7. Empleo y Salarios 
8. Sector Externo 
9. Agricultura, Ganadería, Silvicultura y Pesca 
10. Minería y Energía 
11. Industria Manufacturera 
12. Construcción e Inversiones 
13. Transporte y Seguridad Vial  
14. Comercio Interno   
15. Turismo 
16. Ciencia y Tecnología 
17. Tecnologías de la Información y las Comunicaciones 
18. Educación 
19. Salud Pública y Asistencia Social 
20. Cultura 
21. Deporte y Cultura Física 
22. Proceso Electoral en Cuba
"""

# Extraer capítulos
chapters = extract_chapters(input_string)

# Imprimir resultados
for number, name in chapters:
    print(f"{number}. {name}")
