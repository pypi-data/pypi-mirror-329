import re

def process_text(code):
    """
    Extrae el texto que no esté dentro de los marcadores $description o $title.
    """
    # Eliminar todos los marcadores $description y $title
    plain_text = re.sub(r'\$description\[.*?\]|\$title\[.*?\]|\$titleURL\[.*?\]|\$var\[.*?\]|\$color\[.*?\]|\$author\[.*?\]|\$authorURL\[.*?\]|\$authorIcon\[.*?\]|\$image\[.*?\]|\$thumbnail\[.*?\]', '', code)
    
    # Eliminar espacios en blanco innecesarios
    plain_text = plain_text.strip()
    
    return plain_text