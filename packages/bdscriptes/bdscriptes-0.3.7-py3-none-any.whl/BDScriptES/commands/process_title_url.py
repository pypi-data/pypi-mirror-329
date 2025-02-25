def process_title_url(code):
    """
    Procesa los placeholders $titleURL[url;(índice opcional)].
    Retorna un diccionario con los URLs de título asociados a los índices de embed.
    """
    title_urls = {}
    start = 0

    while True:
        start_idx = code.find("$titleURL[", start)
        if start_idx == -1:
            break

        if start_idx > 0 and code[start_idx - 1].isalnum():
            raise ValueError(f"❌ Invalid format: '{code[start_idx-1:start_idx+10]}...' (Expected '$titleURL[...]')")

        end_idx = code.find("]", start_idx)
        if end_idx == -1:
            raise ValueError("❌ '$tituloURL[' not closed with ']'")

        placeholder = code[start_idx + len("$titleURL["):end_idx]
        parts = placeholder.split(";")
        title_url = parts[0].strip()
        indice_embed = int(parts[1].strip()) if len(parts) > 1 else 1

        if not title_url:
            raise ValueError("❌ '$titleURL[]' missing URL")

        title_urls[indice_embed] = title_url
        start = end_idx + 1

    return title_urls
