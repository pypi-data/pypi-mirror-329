def process_author_url(code):
    """
    Procesa los placeholders $autorURL[url;(índice opcional)].
    Retorna un diccionario con los URLs asociados a los índices de embed.
    """
    author_urls = {}
    start = 0

    while True:
        start_idx = code.find("$autorURL[", start)
        if start_idx == -1:
            break

        # 🔍 Verifica que el marcador empieza correctamente y no tiene caracteres adicionales
        if start_idx > 0 and code[start_idx - 1].isalnum():
            raise ValueError(f"❌ Invalid format: '{code[start_idx-1:start_idx+10]}...' (Expected '$autorURL[...]')")

        end_idx = code.find("]", start_idx)
        if end_idx == -1:
            raise ValueError("❌ '$autorURL[' not closed with ']'")

        placeholder = code[start_idx + len("$autorURL["):end_idx]
        parts = placeholder.split(";")
        author_url = parts[0].strip()
        indice_embed = int(parts[1].strip()) if len(parts) > 1 else 1

        if not author_url:
            raise ValueError("❌ '$autorURL[]' missing URL")

        author_urls[indice_embed] = author_url
        start = end_idx + 1

    return author_urls
