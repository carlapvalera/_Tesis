import json

def save_lang_to_file(filename: str, lang: dict) -> None:
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(lang, file, ensure_ascii=False, indent=4)

# Ejemplo de uso
lang = {
    3: " ",
    4: "!",
    11: "(",
    12: ")",
    30: ";",
    97: "~",
    105: "á",
    108: "ä",
    112: "é",
    116: "í",
    120: "ñ",
    121: "ó",
    126: "ú",
    129: "ü",
    131: "º",
    141: "'",
    200: "Á",
    203: "Í",
    207: "Ó",
}
save_lang_to_file('lang.json', lang)
