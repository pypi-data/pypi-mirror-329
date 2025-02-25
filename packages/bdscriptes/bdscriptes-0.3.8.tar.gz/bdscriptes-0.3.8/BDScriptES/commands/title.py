def process_title(code):
    """
    Procesa los placeholders $title[texto;(índice opcional)].
    Retorna un diccionario con los títulos asociados a los índices de embed.
    """
    titles = {}
    start = 0

    while True:
        start_idx = code.find("$title[", start)
        if start_idx == -1:
            break

        if start_idx > 0 and code[start_idx - 1].isalnum():
            raise ValueError(f"❌ Invalid format: '{code[start_idx-1:start_idx+7]}...' (Expected '$title[...]')")

        end_idx = code.find("]", start_idx)
        if end_idx == -1:
            raise ValueError("❌ '$title[' not closed with ']'")

        placeholder = code[start_idx + len("$title["):end_idx]
        parts = placeholder.split(";")
        texto = parts[0].strip()
        indice_embed = int(parts[1].strip()) if len(parts) > 1 else 1  # Índice por defecto: 1

        if not texto:
            raise ValueError("❌ '$title[]' necesita al menos un texto")

        titles[indice_embed] = texto
        start = end_idx + 1

    return titles
