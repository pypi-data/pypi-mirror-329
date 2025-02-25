import re

def es_color_hex(codigo):
    """
    Verifica si el código es un color hexadecimal válido.
    Soporta formatos con o sin '#' (ejemplo: #FF5733 o FF5733).
    """
    if not codigo.startswith("#"):
        codigo = "#" + codigo  # Agregar '#' si falta

    return bool(re.fullmatch(r'#([A-Fa-f0-9]{6})', codigo)), codigo

def process_color(code):
    """
    Procesa los placeholders $color[color hex;(índice opcional)].
    Retorna un diccionario con los colores asociados a los índices de embed.
    """
    colors = {}
    start = 0

    while True:
        # Busca el inicio de un placeholder
        start_idx = code.find("$color[", start)
        if start_idx == -1:
            break

        # Busca el final del placeholder
        end_idx = code.find("]", start_idx)
        if end_idx == -1:
            raise ValueError("❌ '$color[' not closed with ']'")

        # Extrae el contenido del placeholder
        placeholder = code[start_idx + len("$color["):end_idx]

        # Divide el texto y el índice (si existe)
        parts = placeholder.split(";")
        color = parts[0].strip()  # El color siempre está presente
        indice_embed = int(parts[1].strip()) if len(parts) > 1 else 1  # Índice predeterminado: 1

        # 📌 Validaciones
        if not color:
            raise ValueError("❌ '$color[]' missing color hex value")

        es_valido, color = es_color_hex(color)
        if not es_valido:
            raise ValueError(f"❌ '{color}' is not a valid hex color (expected format: #RRGGBB)")

        # Asocia el color con el índice del embed
        colors[indice_embed] = color

        # Actualiza el índice de búsqueda
        start = end_idx + 1

    return colors
