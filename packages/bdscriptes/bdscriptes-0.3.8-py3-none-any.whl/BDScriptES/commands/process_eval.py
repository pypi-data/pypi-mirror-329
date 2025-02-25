
import re

async def process_eval(code, ctx):
    """
    Procesa el código que contiene $eval[] ejecutando su contenido.
    """
    pattern = r"\$eval\[(.*?)\]"  # Captura todo dentro de $eval[]
    
    while "$eval[" in code:
        match = re.search(r"\$eval\[(.*)\]", code, re.DOTALL)  # Captura el último cierre `]`
        if match:
            inner_code = match.group(1)  # Extrae el contenido dentro de $eval[]
            code = code.replace(match.group(0), inner_code, 1)  # Reemplaza solo la primera aparición
    
    return code



