def process_author_icon(code):
    """
    Procesa los placeholders $authorIcon[url;(índice opcional)].
    Retorna un diccionario con los iconos asociados a los índices de embed.
    """
    author_icons = {}
    start = 0

    while True:
        start_idx = code.find("$authorIcon[", start)
        if start_idx == -1:
            break

        # 🔍 Verifica que el marcador empieza correctamente y no tiene caracteres adicionales
        if start_idx > 0 and code[start_idx - 1].isalnum():
            raise ValueError(f"❌ Invalid format: '{code[start_idx-1:start_idx+12]}...' (Expected '$authorIcon[...]')")

        end_idx = code.find("]", start_idx)
        if end_idx == -1:
            raise ValueError("❌ '$authorIcon[' not closed with ']'")

        placeholder = code[start_idx + len("$autorIcon["):end_idx]
        parts = placeholder.split(";")
        icon_url = parts[0].strip()
        indice_embed = int(parts[1].strip()) if len(parts) > 1 else 1

        if not icon_url:
            raise ValueError("❌ '$authorIcon[]' missing URL")

        author_icons[indice_embed] = icon_url
        start = end_idx + 1

    return author_icons
