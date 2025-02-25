import re

def process_loops(text, ctx=None):
    # Verificar si hay $loop sin corchetes
    if re.search(r'\$loop(?!\[)', text):
        raise ValueError("Error: '$loop' no tiene corchetes de apertura y cierre '[]'.")

    # Verificar si hay $loop[ sin corchete de cierre
    if re.search(r'\$loop\[[^\]]*$', text):
        raise ValueError("Error: '$loop[' no tiene el corchete de cierre ']'.")

    # Verificar si hay $loop[;] con ambos argumentos vacíos
    if re.search(r'\$loop\[\s*;\s*\]', text):
        raise ValueError("Error: '$loop[;]' tiene ambos argumentos vacíos.")

    # Verificar si hay $loop[count;] con el segundo argumento vacío
    if re.search(r'\$loop\[\d+;\s*\]', text):
        raise ValueError("Error: '$loop[count;]' tiene el segundo argumento vacío.")

    # Verificar si hay $loop[;content] con el primer argumento vacío
    if re.search(r'\$loop\[\s*;\s*[^\]]+\]', text):
        raise ValueError("Error: '$loop[;content]' tiene el primer argumento vacío.")

    # Patrón para detectar $loop[count; content]
    pattern = r'\$loop\[(\d+);((?:[^\[\]]+|\[.*?\])*)\]'

    def replacer(match):
        count = int(match.group(1))
        content = match.group(2)
        result = ""
        for i in range(1, count + 1):
            result += content.replace("$i", str(i))
        return result

    result = re.sub(pattern, replacer, text)
    return result


