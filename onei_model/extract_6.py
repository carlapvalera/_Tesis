from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer

lang = {
    3:   " ",
    4:   "!",
    11:  "(",
    12:  ")",
    97:  "~",
    108: "ä",
    129: "ü",
}
ind = 68
for cha in "abcdefghijklmnopqrstuvwxyz":
    lang[ind] = cha
    ind += 1
ind = 36
for cha in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    lang[ind] = cha
    ind += 1
ind = 3
for cha in " !\"#$%&'()*+,-./0123456789:":
    lang[ind] = cha
    ind += 1


def to_acctual_characters(text: str):
    ret = ""
    for number in text.replace("(cid:", ";").replace(")", "")[1:].split(";"):
        # Verificar si cleaned_number es un número
        if not number.replace("\n", "").isdigit():
            continue  # Si no es un número, continuar con la 

        if int(number.replace("\n", "")) in lang:
            ret = ret + lang[int(number.replace("\n", ""))]
        else:
            ret = ret + "(cid:" + number.replace("\n", "") + ")"
        if "\n" in number:
            ret = ret + "\n"
    return ret


for page_layout in extract_pages("C:\\blabla\\_Tesis\\01-territorio.pdf"):
    for element in page_layout:
        if isinstance(element, LTTextContainer):
            print(to_acctual_characters(element.get_text()))