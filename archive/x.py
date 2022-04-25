import cleantext as ct

text = """
    A bunch of \\u2018new\\u2019 references,
    including [Moana]. »Yóù àré rïght <3!«
    """
 
cleansedtext = ct.clean(text)
print(cleansedtext)