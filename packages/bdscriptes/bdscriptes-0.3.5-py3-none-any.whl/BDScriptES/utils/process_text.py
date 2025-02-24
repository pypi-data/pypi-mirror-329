import re

def process_text(code):
    """
    Extrae el texto que no esté dentro de los marcadores con corchetes.
    """
    # Expresión regular para eliminar solo los marcadores con corchetes
    plain_text = re.sub(
        r'\$description\[.*?\]|\$title\[.*?\]|\$titleURL\[.*?\]|\$var\[.*?\]'
        r'|\$color\[.*?\]|\$author\[.*?\]|\$authorURL\[.*?\]|\$authorIcon\[.*?\]'
        r'|\$image\[.*?\]|\$thumbnail\[.*?\]',
        '',
        code
    )
    
    # Eliminar espacios en blanco innecesarios
    plain_text = plain_text.strip()
    
    return plain_text