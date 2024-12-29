



file_path = 'C:\\blabla\\_Tesis\\temporal\\texto_extraido.txt' 
with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

capitulo = "CAPÍTULO"
capitulo_primer_indice = text.find(capitulo)
num_cap_indice =capitulo_primer_indice + len(capitulo)
num_cap_indice +=1
print(num_cap_indice)
cap = text[num_cap_indice]
print(text[num_cap_indice])# tengo el cnumero del capitulo q representa al anuario


# Buscar la segunda ocurrencia comenzando justo después de la primera
capitulo_segundo_indice = text.find("CAPÍTULO", num_cap_indice )
print(capitulo_segundo_indice)
print(text[capitulo_segundo_indice])

contenido_ind = text.find("CONTENIDO")
print(contenido_ind)
print(text[contenido_ind])

#NOMBRE DEL ANUARIO
edicion = "EDICIÓN"
edicion_indice =text.find(edicion)
name = text[num_cap_indice +2: edicion_indice]

#AÑO 
año = text[edicion_indice +len(edicion)+1: edicion_indice +len(edicion)+1+4]

#INDICE DEL ANUARIO
# Extraer el texto desde la primera hasta la segunda ocurrencia
contenido_indice_anuerio = text[num_cap_indice:capitulo_segundo_indice]
print(f'Texto entre la primera y segunda ocurrencia: "{contenido_indice_anuerio}"')


# TEXTO DEL ANUARIO
subcap = str(cap)+".1"
tablas_indice = text.find(subcap,capitulo_segundo_indice)
print(tablas_indice)
print(text[tablas_indice:tablas_indice+20])

text_anuario = text[capitulo_segundo_indice:tablas_indice]
print(text_anuario)

#TABLAS DEL ANUARIO
tablas_anuario = text[tablas_indice:]

print(año)
print(name)