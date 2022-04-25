import unidecode

text =  b'Il Est L\xc3\xa0'

unaccented_string = unidecode.unidecode(text.decode('utf-8'))
print(unaccented_string)