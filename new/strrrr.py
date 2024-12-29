frase = "Todo pasa y todo queda, pero lo nuestro es pasar haciendo caminos."
palabra = "caminos"
indice = frase.find(palabra)

if indice != -1:
    print(f'La palabra "{palabra}" aparece por primera vez en la posición {indice}.')
else:
    print(f'La palabra "{palabra}" no aparece en la frase.')

print(frase[58])