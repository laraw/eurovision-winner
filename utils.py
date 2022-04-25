import unidecode
import pandas as pd
import ast
import re

def remove_non_alpha(text):
    return re.sub(r'\W+', '', text)

def _parse_bytes(bytes_repr):
    result = ast.literal_eval(bytes_repr)

    if not isinstance(result, bytes):
        raise ValueError("Malformed bytes repr")

    return result

def cleanse_string(text):
    
    try:
        byt_text = _parse_bytes(text)
        return unidecode.unidecode(byt_text.decode('utf-8'))
    except:
        try:
            byt_text = text.encode('utf-8')
            return unidecode.unidecode(byt_text.decode('utf-8'))
        except:
            return text