def process_thumbnail(code):
    """
    Procesa los placeholders $thumbnail[url;(índice opcional)].
    Retorna un diccionario con los thumbnails asociados a los índices de embed.
    """
    thumbnails = {}
    start = 0

    while True:
        start_idx = code.find("$thumbnail[", start)
        if start_idx == -1:
            break

        if start_idx > 0 and code[start_idx - 1].isalnum():
            raise ValueError(f"❌ Invalid format: '{code[start_idx-1:start_idx+11]}...' (Expected '$thumbnail[...]')")

        end_idx = code.find("]", start_idx)
        if end_idx == -1:
            raise ValueError("❌ '$thumbnail[' not closed with ']'")

        placeholder = code[start_idx + len("$thumbnail["):end_idx]
        parts = placeholder.split(";")
        thumbnail_url = parts[0].strip()
        indice_embed = int(parts[1].strip()) if len(parts) > 1 else 1

        if not thumbnail_url:
            raise ValueError("❌ '$thumbnail[]' missing URL")

        thumbnails[indice_embed] = thumbnail_url
        start = end_idx + 1

    return thumbnails
