import google.generativeai as genai

# Configura tu clave API
api_key = "AIzaSyB1Jzqer_Ldwrn94YmxbKboyRk5f0UCtws"
genai.configure(api_key=api_key)

# Función para extraer texto y tablas del string
def extract_text_and_tables(input_string):
    model = genai.GenerativeModel("gemini-pro")
    
    # Generar contenido basado en el input
    response = model.generate_content(f"este es el string correspondoente a leer un pdf dame el texto y las tablas q se encuentran en el: {input_string}")
    
    # Suponiendo que la respuesta tiene un formato estructurado
    print(response.text)

    output_text = response.text  # Texto extraído
    tables = []  # Lista para almacenar las tablas

    # Aquí se puede agregar lógica para identificar y extraer tablas del texto
    # Esto dependerá de cómo Gemini formatea las tablas en la respuesta

    return output_text, tables

# Ejemplo de uso
input_string = "1.4 - Extensión superficial, población efectiva y densidad de población, año 2021Extensión superficial (km2         Població Densidad de              CayoÁrea defectiv poblaciónCONCEPTTota  adyacentetierra firm         (U)(hab/km2)Archipiélago cuban109 884,03 126,4106 757,610 885 3499,1    Pinar del Rí8 883,768,48 815,2571 0164,3     Sandin1 710,87,81 703,035 3220,6     Mantu914,615,3899,323 2825,5     Minas de Matahambr857,99,3848,530 9836,1     Viñale693,010,2682,828 5641,2     La Palm641,77,5634,133 3552,0     Los Palacio764,5764,537 2048,7     Consolación del Su1 111,90,11 111,786 6177,9     Pinar del Rí730,916,6714,2187 44256,4     San Lui325,91,2324,631 2195,8     San Juan y Martíne408,2408,242 09103,1     Guan724,0724,034 9248,2   Artemis4 003,21,54 001,7502 38125,5     Bahía Hond784,11,5782,642 3654,0     Marie270,8270,843 82161,8     Guanaja110,2110,227 23247,0     Caimit239,4239,441 53173,5     Baut154,6154,649 54320,4     San Antonio de los Baño126,3126,349 70393,3     Güira de Melen197,9197,939 56199,9     Alquíza194,3194,332 83168,9     Artemis688,6688,684 43122,6     Candelari301,6301,620 9669,5     San Cristóba934,90,0934,970 3675,3  La Haban728,20,0728,22 041 502 803,3     Play35,835,8169 414 730,9     Plaza de la Revolució12,212,2131 4010 718,4     Centro Haban3,43,4126 1036 872,8     La Habana Viej4,34,376 5117 508,2     Regl10,210,242 124 121,9     La Habana del Est141,4141,4166 611 177,6     Guanabaco129,4129,4122 72947,8     San Miguel del Padró25,525,5153 856 021,8     Diez de Octubr12,212,2190 0215 474,3     Cerr10,110,1118 4911 628,5     Mariana23,123,1129 045 569,6     La Lis37,137,1141 563 811,5     Boyero134,8134,8194 961 446,3     Arroyo Naranj82,182,1199 232 424,4     Cotorr65,965,979 411 205,Ó"
output_text, tables = extract_text_and_tables(input_string)

print("Texto extraído:", output_text)
print("Tablas encontradas:", tables)


