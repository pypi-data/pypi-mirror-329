import re

def process_title(code):
    """
    Procesa el código y extrae los placeholders $title[texto;(índice embed)].
    """
    titles = {}
    matches = re.findall(r"\$title\[(.*?)(?:;(.*?))?\]", code)

    for match in matches:
        texto = match[0].strip()
        indice = int(match[1]) if match[1] and match[1].isdigit() else 1  # Índice por defecto: 1

        if not texto:
            raise ValueError("❌ '$title[]' necesita al menos un texto")

        titles[indice] = texto

    return titles
